# NovaProHome website (V.3)

- `index.html`: home page. It holds the site's styles, header and footer and works on its own as a single file.
- `services/<service>/index.html` and `faq/index.html`: generated pages. Don't edit them by hand.
- `assets/site.css`: generated from the `<style>` block in `index.html`.
- `sitemap.xml`, `robots.txt`: for search engines.

## Editing
1. Change styles, header, footer or follow links in `index.html`. Change page text in `build/build_pages.py`.
2. Rebuild: `python3 v3/build/build_pages.py`

The generated pages use root links (`/services/...`, `/assets/site.css`), so host this folder at the domain root.
