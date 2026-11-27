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



# Automatically format individual video article pages

def plain_text(value):
    return " ".join(unescape(re.sub(r"<[^>]+>", "", value)).split())


for file in sorted(PUBLIC.glob("videos/*/index.html")):
    content = file.read_text(encoding="utf-8")
    video_id = file.parent.name

    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        continue

    # Prevent duplicate formatting
    if "<!-- RPLP formatted page -->" in content:
        continue

    # Only format HTML article fragments
    if re.search(r"<html\b", content, re.IGNORECASE):
        continue

    heading = re.search(
        r"<h1\b[^>]*>(.*?)</h1>",
        content,
        re.IGNORECASE | re.DOTALL
    )

    title = plain_text(heading.group(1)) if heading else "Parking Lot Striping Project"

    article = content

    if heading:
        article = content[:heading.start()] + content[heading.end():]

    paragraph = re.search(
        r"<p\b[^>]*>(.*?)</p>",
        article,
        re.IGNORECASE | re.DOTALL
    )

    description = plain_text(paragraph.group(1)) if paragraph else title

    if len(description) > 160:
        description = description[:157].rsplit(" ", 1)[0] + "..."

    canonical = BASE_URL + "/videos/" + quote(video_id) + "/"
    thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    embed_url = f"https://www.youtube.com/embed/{video_id}"

    page = f"""<!DOCTYPE html>
<!-- RPLP formatted page -->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Raleigh Parking Lot Painting LLC</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{thumbnail}">
<meta name="twitter:card" content="summary_large_image">

<style>
* {{
    box-sizing: border-box;
}}
body {{
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f4f6f8;
    color: #222;
    line-height: 1.75;
}}
header {{
    background: #172b40;
    color: white;
    text-align: center;
    padding: 40px 20px;
}}
.brand {{
    font-size: 30px;
    font-weight: bold;
}}
nav {{
    margin-top: 20px;
}}
nav a {{
    color: white;
    margin: 0 12px;
}}
main {{
    max-width: 1000px;
    margin: 30px auto;
    padding: 35px;
    background: white;
    border-radius: 8px;
}}
h1 {{
    color: #172b40;
    font-size: 32px;
    line-height: 1.3;
}}
h2, h3 {{
    color: #172b40;
}}
a {{
    color: #17649c;
}}
.video {{
    width: 100%;
    aspect-ratio: 16 / 9;
    margin: 25px 0;
}}
.video iframe {{
    width: 100%;
    height: 100%;
    border: 0;
    border-radius: 8px;
}}
img {{
    max-width: 100%;
    height: auto;
}}
.cta {{
    background: #edf2f6;
    padding: 25px;
    margin-top: 35px;
    border-radius: 8px;
    text-align: center;
}}
footer {{
    background: #172b40;
    color: white;
    text-align: center;
    padding: 30px 20px;
}}
footer a {{
    color: white;
}}
@media (max-width: 600px) {{
    main {{
        margin: 12px;
        padding: 20px;
    }}
    h1 {{
        font-size: 26px;
    }}
    .brand {{
        font-size: 24px;
    }}
}}
</style>
</head>

<body>

<header>
<div class="brand">Raleigh Parking Lot Painting LLC</div>
<p>Professional Parking Lot Striping Since 1985</p>
<nav>
<a href="/">All Projects</a>
<a href="{COMPANY_URL}">Official Website</a>
</nav>
</header>

<main>
<article>

<h1>{escape(title)}</h1>

<div class="video">
<iframe
    src="{embed_url}"
    title="{escape(title)}"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
</iframe>
</div>

<p><a href="{video_url}">Watch this video on YouTube</a></p>

{article}

</article>

<div class="cta">
<h2>Professional Parking Lot Striping</h2>
<p>Serving Raleigh and surrounding North Carolina communities since 1985.</p>
<p><a href="{COMPANY_URL}">Visit Raleigh Parking Lot Painting LLC</a></p>
<p><a href="/">Explore More Parking Lot Striping Projects</a></p>
</div>

</main>

<footer>
<p>Raleigh Parking Lot Painting LLC | Family-run since 1985</p>
<p>Dedicated to Quality, Built on Family, Focused on Your Business.</p>
<a href="{COMPANY_URL}">Official Company Website</a>
</footer>

</body>
</html>
"""

    file.write_text(page, encoding="utf-8")
    print(f"Formatted video article: {video_id}")

print("RPLP article formatting complete.")


# Automatically publish authentic RPLP photographs
import shutil

image_dir = Path("public/images")
image_dir.mkdir(parents=True, exist_ok=True)

image_count = 0

for photo in Path(".").iterdir():
    if photo.is_file() and photo.suffix.lower() in (
        ".jpg", ".jpeg", ".png", ".webp"
    ):
        shutil.copy2(photo, image_dir / photo.name)
        image_count += 1

print(f"Published {image_count} RPLP photographs.")
