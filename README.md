# You suck at golf — course catalog

Public course downloads for **You suck at golf**, the Android and Wear OS golf app. This repository contains course information, green coordinates and aerial imagery. It contains no app installers, signing keys, player GPS readings, rounds or other player data.

## Included courses

| Course | Holes | Par | Round choices | Package |
| --- | --- | --- | --- | --- |
| Bridlewood Golf Club, Flower Mound, TX | 18 | 72 | 18, front 9, back 9 | Version 1 |
| City Park Nine, Fort Collins | 9 | 36 | 9 holes | Version 1 |
| Collindale, Fort Collins | 18 | 71 | 18, front 9, back 9 | Version 3 |
| Firewheel - Lakes, Garland, TX | 18 | 72 | 18, front 9, back 9 | Version 1 |
| Firewheel Bridges - Champion / Masters, Garland, TX | 18 | 72 | 18, front 9, back 9 | Version 1 |
| Firewheel Bridges - Masters / Tradition, Garland, TX | 18 | 71 | 18, front 9, back 9 | Version 1 |
| Firewheel Bridges - Tradition / Champion, Garland, TX | 18 | 71 | 18, front 9, back 9 | Version 1 |
| Indian Creek - Creek, Carrollton, TX | 18 | 72 | 18, front 9, back 9 | Version 1 |
| Indian Creek - Lakes, Carrollton, TX | 18 | 72 | 18, front 9, back 9 | Version 1 |
| Southridge, Fort Collins | 18 | 71 | 18, front 9, back 9 | Version 1 |

All ten entries include tee yardages, green-center coordinates, approximate hole routes and offline aerial images. City Park Nine and Southridge were checked against the city's linked 2026 scorecards and course diagrams on October 23, 2026. The seven Texas entries were checked against the operators' linked scorecards and available maps on October 26, 2026. Map-derived green centers still need an on-course check; imagery is archival and does not establish current tee-marker or pin positions.

The Bridges names give the playing order: **Front 9** selects the first named loop and **Back 9** the second. For example, Champion / Masters → Back 9 plays Masters as holes 10-18. All three combinations reuse the same 27 physical holes.

**Firewheel limitations:** Old is not included pending verification following its 2025 green renovation. Lakes uses par 4 on hole 10 and total par 72; the linked card's main row permits 4/5 and 72/73, while the Red row and course description use 4 and 72. The app currently has one par per hole. Bridges uses the official card's per-nine stroke-index ranks, normalized to odd indexes on the first nine and even on the second; this is an app allocation, not a verified official combined-course allocation. Published Bridges ratings either disagree with the card lengths or lack a matching official rating table. Every Firewheel tee therefore has `ratingsVerified: false` and these rounds do not enter handicap estimates. Scoring, yardages and history work normally.

Bridlewood and both Indian Creek courses include official scorecard tee lengths and verified ratings, including women's tees. The app currently uses the main men's stroke-index row for all tees; separate women's stroke-index rows are not supported. Bridlewood's mislabeled community-map hole 1 was corrected, and its Black hole 14 follows the linked card's 402 yards.

City Park Nine uses its nine physical holes once. Its scorecard prints two loops with 18-hole ratings; these are retained under the explicit category **18-hole card**, with `ratingsVerified: false`. They are not nine-hole ratings. The main stroke-index row is ranked from 1-9; Red's separate handicap row is not supported by the app's current single-row schema. Nine-hole rounds do not enter the app's handicap estimate.

Southridge's printed Red back-nine/full totals omit the last hole's 99 yards. The package keeps every individual printed hole length, which sums to 2,521 on the back and 4,911 overall. Other tee totals match the card. Each package's `mappingNote` records these details.

## Connect the app

1. Install app version 0.1.6 or later on the phone and watch.
2. In the phone app, open **Settings → Courses** and enter:

   ```text
   https://raw.githubusercontent.com/TheSClass/ysg-courses/main/catalog.json
   ```

3. Tap **Refresh catalog**, then **Download** or **Update** next to the desired course.
4. Choose the downloaded course when starting a new round, then select 18 holes, Front 9 or Back 9 where available. Let the phone sync with the watch. Your friend can use the same catalog URL; downloading does not need a GitHub login or token.

No Pages hosting, API key, paid server, or app rebuild is required. A repository owner can update the files; app users can only download them. Course metadata, green coordinates, and map images remain on each device for offline play. Starting a new round uses the chosen installed course's latest version; existing rounds retain their original course snapshot.

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

Each course JSON identifies its official scorecard, course page and mapping sources, plus separate rating references where needed. Firewheel hole identification was compared with Garland's numbered course diagram and public GolfTraxx references. Green centers use OpenStreetMap polygons where available and explicit USGS aerial picks otherwise. Bridges tee/route lines were traced approximately from the aerial because the reference site's calculated tee positions use mismatched scorecards. No commercial map screenshots or scorecard artwork are redistributed here.

OpenStreetMap-derived geometry is attributed to © OpenStreetMap contributors and distributed under the [Open Database License](https://www.openstreetmap.org/copyright). The included USGS aerial images are public-domain material from The National Map. Keep these credits with redistributed course data; check each future source's terms separately. The catalog is not affiliated with the courses, USGA, or map providers.
