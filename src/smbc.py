"""Functions for SMBC."""

from lxml import html
from src.utilities import cache_or_download
from src.utilities import hash_text


def from_smbc(url):
    """Make the work for smbc."""
    content = cache_or_download(url)
    tree = html.fromstring(content)

    img = tree.xpath('//img[@id="cc-comic"]')[0]

    title = img.attrib['title']
    comic_url = img.attrib['src']

    print(f"url: {comic_url}")
    print(f"title: {title}")

    div = tree.xpath('//div[@id="cc-comicbody"]')[0]
    dprint("----")
    dprint(div.attrib)

