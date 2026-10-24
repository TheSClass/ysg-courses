# You suck at golf — course catalog

Public course downloads for **You suck at golf**, the Android and Wear OS golf app. This repository contains course information, green coordinates and aerial imagery. It contains no app installers, signing keys, player GPS readings, rounds or other player data.

## Included courses

| Course | Holes | Par | Round choices | Package |
| --- | --- | --- | --- | --- |
| City Park Nine, Fort Collins | 9 | 36 | 9 holes | Version 1 |
| Collindale, Fort Collins | 18 | 71 | 18, front 9, back 9 | Version 3 |
| Southridge, Fort Collins | 18 | 71 | 18, front 9, back 9 | Version 1 |

All three include tee yardages, green-center coordinates, hole routes and offline aerial images. The new City Park Nine and Southridge packages were checked against the city's linked 2026 scorecards and course diagrams on October 23, 2026. Community-mapped green centers still need an on-course check.

City Park Nine uses its nine physical holes once. Its scorecard prints two loops with 18-hole ratings; these are retained under the explicit category **18-hole card**, with `ratingsVerified: false`. They are not nine-hole ratings. The main stroke-index row is ranked from 1-9; Red's separate handicap row is not supported by the app's current single-row schema. Nine-hole rounds do not enter the app's handicap estimate.

Southridge's printed Red back-nine/full totals omit the last hole's 99 yards. The package keeps every individual printed hole length, which sums to 2,521 on the back and 4,911 overall. Other tee totals match the card. Each package's `mappingNote` records these details.

## Connect the app

1. Install app version 0.1.6 or later on the phone and watch.
2. In the phone app, open **Settings → Courses** and enter:

   ```text
   https://raw.githubusercontent.com/TheSClass/ysg-courses/main/catalog.json
   ```

3. Tap **Refresh catalog**, then **Download** or **Update** next to the desired course.
4. Let the phone sync with the watch. Your friend can use the same catalog URL; downloading does not need a GitHub login or token.

No Pages hosting, API key, paid server, or app rebuild is required. A repository owner can update the files; app users can only download them. Course metadata, green coordinates, and map images remain on each device for offline play. Starting a new round uses the latest installed course; existing rounds retain their original course snapshot.

For a fork or separate host, keep `catalog.json`, `courses/` and `imagery/` in the same relative layout and use that host's direct HTTPS catalog URL.

## Add or correct a course

1. Add `courses/<course-id>.json`, using Collindale as the schema example. Use a new stable ID for each course. For corrections, keep the ID and increase `version` (Collindale is currently version 3).
2. Verify hole numbering, pars, stroke indexes, and every tee's yardages against the current official scorecard. Check green centers and routes against a map and on-course observations. Do not assume map-provider hole numbers match today's scorecard.
3. Include the source URLs, attribution, and any limitations in `mappingNote`. Ratings are only eligible for the personal handicap estimate when `ratingsVerified` is true. Use verified values; do not invent ratings. The existing schema requires rating/slope values for each tee.
4. An optional `imagery` object refers to `imagery/<course-id>-v<version>.jpg` and gives its west/east/north/south geographic bounds. Add the JPEG to that path. Use imagery you have permission to redistribute, at most 10 MB and 4096 pixels on each side. Without imagery, the app still draws the hole route and available map shapes. Keep the same image bytes within a course version.
5. Run `python tools/build_catalog.py` from this folder. It validates course structure and generates all listing checksums. The app validates downloads again before installing them. This checks file structure, not real-world course accuracy.
6. Commit/upload the course, optional image, and regenerated `catalog.json` together. Users tap **Refresh catalog**, then **Download** or **Update**. GitHub caching can briefly delay new files; a checksum failure is safe to retry after refreshing.

The phone sends downloaded courses and images to its paired watch through normal sync. Keep both apps up to date for phone GPS and nine-hole round support. Previously downloaded courses still work when GitHub or the internet is unavailable. Downloads are explicit; no network access is required during a round. Course files/images are separate from the exported round-event backup; save this repository as their source of truth.

## Included sources and licensing

Each course JSON identifies its City of Fort Collins scorecard, course page, OpenStreetMap geometry and USGS aerial imagery sources; Collindale also identifies its USGA tee-rating source. OpenStreetMap-derived geometry is attributed to © OpenStreetMap contributors and distributed under the [Open Database License](https://www.openstreetmap.org/copyright). The included USGS aerial images are public-domain material from The National Map. Keep these credits with redistributed course data; check each future source's terms separately. The catalog is not affiliated with the courses, USGA, or map providers.
