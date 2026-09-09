# Week 5 — The Polite Scraper
Backend Track · Assignment A9

I will not reuse this code on another site without checking its rules and terms first.

Run:
```bash
pip install -r requirements.txt
python -m src.main
```
## Stage 1 — Catalogue fetch

The scraper fetches the first catalogue page with a descriptive User-Agent,
a request timeout, and HTTP status validation. The downloaded page is cached
under `cache/catalogue-page-1.html` so reruns can avoid unnecessary requests.

## Stage 2 — Catalogue discovery

The scraper follows the catalogue pagination using the site's `next` link,
converts discovered links to absolute URLs, removes duplicates, and checkpoints
the expected result of 3 catalogue pages and 60 unique book URLs.

## Stage 3 — Book detail extraction

For each discovered book URL, the scraper collects the raw title, product URL,
price text, availability text, rating text, description, source page, and
fetch timestamp. Each record retains its source URL for provenance.

## Stage 4 — Normalize and validate

Prices are normalized from the raw text into numeric `price_gbp` values while
the original price text is preserved. Book records are validated with Pydantic,
canonical URLs are used for identity, and invalid records are separated into
`output/errors.json`.

## Stage 5 — Error handling and run reporting

Each page is handled independently so a broken page does not stop the run.
Timeouts and server errors may be retried once, while permanent errors such
as 404 are reported and skipped. Each run produces `output/run-report.json`
with request, cache, validation, and failure information.

## Stage 6 — Reproducibility

The repository is designed so another developer can clone it, install the
Python dependencies, and run the scraper with a single command. Cached HTML
files are excluded from version control, while sample JSON outputs are kept
for verification.