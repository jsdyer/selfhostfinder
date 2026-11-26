# Selfhost Finder

[Open Selfhost Finder](https://coolcode.ca/selfhostfinder/) — browse real community-listed self-hosted software, compare purpose/platform/licence and save a private shortlist.

<!-- coolcode:guide -->
Search an application or purpose, narrow by category, platform/language and project licence, and save candidates on your device. The shortlist compares source-reported releases and activity dates and exports CSV. Hardware requirements and security scores are deliberately not inferred. Supported projects link to Rack Recipes; choose the named project there. Searches and saved IDs never leave your browser.
<!-- /coolcode:guide -->

## Data and rights

Adapted from [awesome-selfhosted-data](https://github.com/awesome-selfhosted/awesome-selfhosted-data) by its contributors under **CC BY-SA 3.0**. The adapted `web/data/catalogue.json` is distributed under the same licence; the source licence and author list are bundled. Software projects retain their own licences. Fields are selected/renamed and unsafe links omitted. No project icons are copied.

The source's `updated_at`, archived flag and release values are catalogue observations, not an independent security/support check. Requirements are unknown. Platform labels mix languages and packaging formats. A project appearing in the catalogue is not a recommendation to expose it to the internet. All records are included by default; archived entries are hidden only by the visitor's toggle.

## Refresh and publish

Pages → GitHub Actions. No key or external service is needed. `pages.yml` checks weekly on Monday at 10:53 UTC and on manual dispatch. It downloads one source repository, normalizes the catalogue and retains the last good publication on failure. The separate schedule guard covers this collector. Successful captures are committed, preserving earlier editions in Git history. Source commits and capture dates are recorded independently.

Local commands:

```sh
python3 -m pip install -r scripts/requirements.txt
git clone --depth=1 https://github.com/awesome-selfhosted/awesome-selfhosted-data.git /tmp/selfhost-source
python3 scripts/collect.py --source-dir /tmp/selfhost-source
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
python3 tests/browser_smoke.py
```

The builder is offline. Chromium browser tests require the packages in `tests/browser-requirements.txt`. Deployment publishes only `dist/`, not source/private files.

## Expand or customize

`config/catalogue.json` defines the source reference, whether archived rows are excluded from collection, and exact source-slug → Rack Recipes mappings. The importer scans every YAML record in `software/`; there is no fixed project count or starter-only coverage. Upstream additions become searchable after a refresh without code changes. To fork the upstream catalogue, set the workflow checkout repository/ref and matching config source together. Edit the recipe map only when that project has an actual Rack Recipes entry. Unknown requirements remain unknown.

Modify the source/config, run tests, commit, then use **Actions → Selfhost Finder · Check and refresh → Run workflow**. Root catalogue registration, Worker ID, public-page probe, weekly collector freshness and sitemap belong to the standard CoolCode lifecycle.

## Privacy

Shortlist IDs are stored under `coolcode:selfhostfinder:shortlist` and survive refresh. Clear shortlist removes only that key's contents. CSV exports are generated locally with spreadsheet-formula protection. Shared CoolCode metrics record only tool opens, never searches or selected applications. External project links load only when opened.

## Ready-to-use example

[Self-Hosted RSS Readers](https://coolcode.ca/selfhostfinder/rss-readers.html) opens this scenario in the same tool. Browse the Feed Readers category from the published self-hosted software catalogue. Narrow the list by platform and licence, then compare the projects in your shortlist.
