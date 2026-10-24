"""Validate the public course files and rebuild catalog.json; uses only Python's standard library."""
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def point(value):
    return all(isinstance(value.get(k), (int, float)) and math.isfinite(value[k]) and lo <= value[k] <= hi
               for k, lo, hi in [("lat", -90, 90), ("lon", -180, 180)])


def validate(course):
    require(re.fullmatch(r"[a-z0-9-]{1,80}", course["id"]), "Invalid course ID")
    require(isinstance(course["version"], int) and course["version"] > 0, "Use a positive version")
    require(all(course.get(key) for key in ["name", "city", "sources", "attribution"]), "Name, city, sources and attribution are required")
    holes = course["holes"]
    n = len(holes)
    require(n in [9, 18], "Use 9 or 18 holes")
    require([h["number"] for h in holes] == list(range(1, n + 1)), "List holes in playing order")
    require(sorted(h["strokeIndex"] for h in holes) == list(range(1, n + 1)), "Stroke indexes must be unique")
    for h in holes:
        require(3 <= h["par"] <= 6 and point(h["center"]), "Invalid par or green center")
        require(len(h["path"]) >= 2 and all(point(p) for p in h["path"]), "Invalid hole path")
    tees = course["tees"]
    require(tees and len({t["id"] for t in tees}) == len(tees), "Use unique tee IDs")
    for t in tees:
        require(20 <= t["rating"] <= 90 and 55 <= t["slope"] <= 155, "Invalid tee rating or slope")
        require(len(t["yardages"]) == n and all(40 <= y <= 900 for y in t["yardages"]), "Invalid tee yardages")
    for shape in course.get("shapes", []):
        require(2 <= len(shape["points"]) <= 10000 and all(point(p) for p in shape["points"]), "Invalid map geometry")
    require(len(course.get("shapes", [])) <= 3000, "Too many map shapes")
    image = course.get("imagery")
    if image:
        require(re.fullmatch(r"[a-z0-9/-]+\.jpg", image["asset"]) and ".." not in image["asset"], "Invalid image path")
        require(-180 <= image["west"] < image["east"] <= 180 and -90 <= image["south"] < image["north"] <= 90, "Invalid image bounds")
    return course


def build(root=ROOT):
    entries = []
    for path in sorted((root / "courses").glob("*.json")):
        data = path.read_bytes()
        require(len(data) <= 4_000_000, f"{path.name} exceeds 4 MB")
        course = validate(json.loads(data))
        require(path.stem == course["id"], "Filename must match course ID")
        entry = {k: course[k] for k in ["id", "name", "city", "version"]}
        entry.update(file=path.relative_to(root).as_posix(), sha256=hashlib.sha256(data).hexdigest())
        if course.get("imagery"):
            image = root / course["imagery"]["asset"]
            image_data = image.read_bytes()
            require(len(image_data) <= 10_000_000 and image_data.startswith(b"\xff\xd8"), "Use a JPEG up to 10 MB (4096 px maximum per side)")
            entry.update(image=image.relative_to(root).as_posix(), imageSha256=hashlib.sha256(image_data).hexdigest())
        entries.append(entry)
    require(len(entries) <= 2000, "Catalog supports up to 2000 courses")
    require(len({e["id"] for e in entries}) == len(entries), "Duplicate course ID")
    result = {"schemaVersion": 1, "courses": entries}
    (root / "catalog.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = build()
    print(f"Validated {len(result['courses'])} courses; catalog.json is ready.")
