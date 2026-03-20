# NJ News Commons events and newsletter dashboard

An interactive dashboard for exploring the [Center for Cooperative Media](https://centerforcooperativemedia.org/)'s event history and New Jersey newsletter directory.

**Live site:** https://jamditis.github.io/testing-ground/

## What's in it

- **293 events** from 2018 to 2026 — trainings, webinars, press briefings, conferences, workshops, and more
- **35 NJ newsletters** with descriptions, frequency info, and subscribe links
- Year-over-year trends, event type breakdowns, monthly heatmap, and virtual vs. in-person analysis
- Full-text search and filtering by year, type, and format

## How it works

The dashboard is a single self-contained HTML file with all data embedded as JSON. No server, no database, no build tools beyond Python's standard library.

Source data lives in `data/` as CSV exports from Airtable. A build script parses the CSVs and injects the data into an HTML template:

```
data/*.csv  -->  build.py  -->  index.html
                    ^
              template.html
```

To rebuild after updating the CSVs:

```bash
python3 build.py
```

## Social graphics

Pre-built social card templates in `social/`:

| File | Size | Use case |
|------|------|----------|
| `og-card.html` | 1200x630 | Link previews, Twitter/X |
| `instagram-square.html` | 1080x1080 | Instagram feed |
| `story-card.html` | 1080x1920 | Instagram/LinkedIn stories |

Open at native dimensions and screenshot to export as images.

## Tech

- Pure HTML/CSS/JS, no frameworks or external chart libraries
- Charts built with CSS (animated bar fills, heatmap cells, stacked segments)
- Typography: [Newsreader](https://fonts.google.com/specimen/Newsreader) + [Outfit](https://fonts.google.com/specimen/Outfit) via Google Fonts
- All DOM manipulation uses safe methods (createElement/textContent)

## Data sources

- **Events calendar:** Center for Cooperative Media Airtable, exported as CSV
- **Newsletter directory:** NJ News Commons Airtable, exported as CSV

## License

Data belongs to the [Center for Cooperative Media](https://centerforcooperativemedia.org/) at Montclair State University.
