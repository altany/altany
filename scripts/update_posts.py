"""Rewrites the latest-posts list in README.md from tany4.com's RSS feed."""
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://tany4.com/rss.xml"
COUNT = 4
START, END = "<!-- POSTS:START -->", "<!-- POSTS:END -->"

with urllib.request.urlopen(FEED, timeout=30) as res:
    items = ET.fromstring(res.read()).findall("./channel/item")

posts = sorted(
    ((parsedate_to_datetime(i.findtext("pubDate")), i.findtext("title"), i.findtext("link")) for i in items),
    reverse=True,
)[:COUNT]
lines = "\n".join(f"- [{title}]({link}) · {date:%-d %b %Y}" for date, title, link in posts)

with open("README.md") as f:
    readme = f.read()
updated = re.sub(f"{START}.*?{END}", f"{START}\n{lines}\n{END}", readme, flags=re.S)
with open("README.md", "w") as f:
    f.write(updated)
