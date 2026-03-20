# NJ News Commons dashboard

Interactive dashboard for the Center for Cooperative Media's event calendar and NJ newsletter directory. Live at https://jamditis.github.io/testing-ground/

## Project structure

| File | Purpose |
|------|---------|
| `index.html` | Built output — self-contained dashboard with embedded JSON data. Do not edit directly. |
| `template.html` | HTML template with `__DATA_PLACEHOLDER__` token. Edit this for layout/style changes. |
| `build.py` | Parses CSVs, generates JSON, injects into template to produce `index.html`. |
| `data/*.csv` | Source data exported from Airtable (utf-8-sig encoding, multiline fields). |
| `social/*.html` | Social graphics as HTML files — screenshot at native dimensions to export as images. |

## How to build

```bash
python3 build.py
```

This reads the CSVs from `data/`, parses them with `utf-8-sig` encoding (required — files have BOM), and writes `index.html`. Run this after any CSV or template change.

## Deployment

GitHub Pages serves from `master` branch root. Branch protection is enabled — all changes go through PRs. After merging, Pages rebuilds automatically within ~30 seconds.

## Data notes

- Calendar CSV has multiline `About` fields — the csv module handles these correctly
- Event types are comma-separated in the `Type` column (e.g., "Training,ONA New Jersey")
- Virtual classification is based on Location field keywords: webinar, zoom, online, virtual, video conference
- Newsletter descriptions are truncated to 250 chars in the build to keep payload size reasonable
- The `data_parsed.json` file is an intermediate artifact, not used by the build

## Social graphics

Three formats, all using the same editorial aesthetic as the dashboard:

| File | Dimensions | Use |
|------|-----------|-----|
| `social/og-card.html` | 1200x630 | Link previews, Twitter cards |
| `social/instagram-square.html` | 1080x1080 | Instagram feed posts |
| `social/story-card.html` | 1080x1920 | Instagram/LinkedIn stories |

To export: open in browser at native dimensions and screenshot, or use Playwright.

## Conventions

- All DOM construction uses safe methods (createElement/textContent) — no innerHTML with untrusted data
- Charts are pure CSS (no external chart library)
- Fonts loaded from Google Fonts: Newsreader (serif headlines) + Outfit (sans body)
- Color palette uses CSS variables defined in `:root`
