# Embryly website

Static HTML, CSS and JavaScript for https://www.embryly.com.

The journal includes 30 food safety and nutrition guides with Ink and blush artwork. Article sources and the editorial ledger live in content/blog. Run python3 blog_build.py to rebuild the journal without rewriting the landing page or legal content. The legacy full-site generator is build.py; its final journal step restores the expanded index and shared metadata.

blog_config.json controls the production origin, indexing, publication date, Google verification and App Store link. The app remains in review, so app_store_url is null and blog download badges display Coming soon. A pending App Store URL is recorded for activation after the listing is live.

The 30 editorial dates span August 25 through October 14, 2026. First publication is October 14, 2026; structured data uses the actual publication date. Editorial dates do not claim earlier web publication.

Preview locally with python3 -m http.server 4317 --bind 127.0.0.1. Production robots.txt allows crawling and advertises the sitemap. Google Search Console property: https://www.embryly.com/.
