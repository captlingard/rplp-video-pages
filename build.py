from pathlib import Path
from html import escape, unescape
from urllib.parse import quote
import re

PUBLIC = Path("public")
BASE_URL = "https://rplp-projects.netlify.app"
COMPANY_URL = "https://raleighparkinglotpainting.com/"

articles = []

for file in sorted(PUBLIC.glob("videos/*/index.html")):
    content = file.read_text(encoding="utf-8")
    match = re.search(
        r"<h1\b[^>]*>(.*?)</h1>",
        content,
        re.IGNORECASE | re.DOTALL
    )

    title = match.group(1) if match else file.parent.name
    title = unescape(re.sub(r"<[^>]+>", "", title)).strip()
    url = "/videos/" + quote(file.parent.name) + "/"

    articles.append((title, url))

links = "\n".join(
    f'<li><a href="{url}">{escape(title)}</a></li>'
    for title, url in articles
)

homepage = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Parking Lot Striping Projects | Raleigh Parking Lot Painting LLC</title>
<meta name="description" content="Explore professional parking lot striping projects, videos and pavement marking guides from Raleigh Parking Lot Painting LLC, family-run since 1985.">
<link rel="canonical" href="{BASE_URL}/">
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    background: #f4f6f8;
    color: #222;
    line-height: 1.7;
}}
header {{
    background: #172b40;
    color: white;
    padding: 40px 20px;
    text-align: center;
}}
main {{
    max-width: 1000px;
    margin: 30px auto;
    padding: 25px;
    background: white;
    border-radius: 8px;
}}
a {{ color: #155da4; }}
li {{ margin-bottom: 18px; }}
footer {{
    text-align: center;
    padding: 25px;
}}
</style>
</head>
<body>
<header>
<h1>Raleigh Parking Lot Painting LLC</h1>
<p>Professional Parking Lot Striping Since 1985</p>
<p>Dedicated to Quality, Built on Family, Focused on Your Business.</p>
</header>
<main>
<h2>Parking Lot Striping Projects and Resources</h2>
<p>Explore our parking lot painting videos, pavement marking projects and educational articles for commercial property managers throughout the Raleigh-Durham Triangle.</p>
<ul>
{links}
</ul>
<p><a href="{COMPANY_URL}">Visit Our Official Website</a></p>
</main>
<footer>
Raleigh Parking Lot Painting LLC | Family-run since 1985
</footer>
</body>
</html>
"""

(PUBLIC / "index.html").write_text(
    homepage, encoding="utf-8"
)

urls = [BASE_URL + "/"]
urls.extend(BASE_URL + url for _, url in articles)

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in urls:
    sitemap += f"  <url><loc>{escape(url)}</loc></url>\n"

sitemap += "</urlset>\n"

(PUBLIC / "sitemap.xml").write_text(
    sitemap, encoding="utf-8"
)

(PUBLIC / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n",
    encoding="utf-8"
)

print(f"Successfully generated homepage and sitemap for {len(articles)} articles.")
