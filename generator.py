import csv
import os
import re

# Create covers folder if not exists
os.makedirs("covers", exist_ok=True)

base_url = "https://chrislin2k.github.io/image-search-site"

sitemap_urls = []

def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.lower()

import requests
from io import StringIO

csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS9iUTdte3K7UVyRPSeZ0euorASk4mo00oCJOjK8ZyGVUxD1uXJrt5oxVrU_0fu_-DjPjKAdRqc8YkM/pub?gid=388996334&single=true&output=csv"

response = requests.get(csv_url)
csvfile = StringIO(response.text)
reader = csv.DictReader(csvfile)
    headers = next(reader)

    for row in reader:
        image = row[1]
        title = row[2]
        author = row[3]

        slug = slugify(title)
        filename = f"covers/{slug}.html"

        with open("template.html", encoding="utf-8") as f:
            template = f.read()

        html = template.replace("{{TITLE}}", title)\
                       .replace("{{AUTHOR}}", author)\
                       .replace("{{IMAGE}}", image)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        sitemap_urls.append(f"{base_url}/covers/{slug}.html")

# Generate sitemap
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    
    for url in sitemap_urls:
        f.write(f"  <url><loc>{url}</loc></url>\n")
    
    f.write('</urlset>')
