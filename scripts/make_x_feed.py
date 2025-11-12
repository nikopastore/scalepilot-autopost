#!/usr/bin/env python3
"""
ScalePilot X (Twitter) Feed Generator
Creates X-optimized feeds with 280 character limit and ScalePilot branding
"""

import xml.etree.ElementTree as ET
import re
import hashlib
import html
import sys
import os
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

# File paths
IN_FEED = "feeds/rss.xml"
OUT_ALL = "feeds/rss_x.xml"
OUT_LIVE = "feeds/rss_x_live.xml"

# X (Twitter) settings
RESERVED_SUFFIX = " #ScalePilot"
BASE_LIMIT = 280

# Regex patterns
HASHTAG_RE = re.compile(r"(?<!\w)#[A-Za-z0-9_]+")


def strip_hashtags(s):
    """Remove hashtags from text"""
    s = HASHTAG_RE.sub("", s or "")
    return re.sub(r"\s{2,}", " ", s).strip()


def collapse_ws(s):
    """Remove HTML and collapse whitespace"""
    s = re.sub(r"<[^>]+>", "", s or "")
    s = (s.replace("&nbsp;", " ")
          .replace("&mdash;", "—")
          .replace("&#8212;", "—")
          .replace("&ndash;", "–")
          .replace("&#8211;", "–"))
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


# Emoji handling for safe truncation
ZWJ = "\u200d"


def is_vs(ch):
    o = ord(ch)
    return 0xFE0E <= o <= 0xFE0F


def is_skin(ch):
    o = ord(ch)
    return 0x1F3FB <= o <= 0x1F3FF


def is_regional(ch):
    o = ord(ch)
    return 0x1F1E6 <= o <= 0x1F1FF


def is_keycap(ch):
    return ord(ch) == 0x20E3


def emoji_safe_truncate(text, limit):
    """Truncate text without breaking emoji sequences"""
    if limit <= 0:
        return ""
    if len(text) <= limit:
        return text

    cut = max(0, limit - 1)
    s = text[:cut]

    def unsafe_tail(chrs):
        return chrs.endswith(ZWJ) or (chrs and (
            is_vs(chrs[-1]) or is_skin(chrs[-1]) or
            is_keycap(chrs[-1]) or is_regional(chrs[-1])
        ))

    # Remove unsafe trailing characters
    while s and unsafe_tail(s):
        s = s[:-1]

    # Break at word boundary
    if " " in s:
        s = s.rsplit(" ", 1)[0]

    return s + "…"


def smart_text(body):
    """Format text for X with character limit"""
    # Remove any existing hashtags
    body = strip_hashtags(body)

    # Calculate available space
    reserve = len(RESERVED_SUFFIX)
    txt = emoji_safe_truncate(body, max(0, BASE_LIMIT - reserve))

    # Add suffix
    txt = f"{txt}{RESERVED_SUFFIX}"

    # Final safety check
    if len(txt) > BASE_LIMIT:
        txt = emoji_safe_truncate(txt, BASE_LIMIT)

    return txt


def load_items():
    """Load and sort items from master feed"""
    if not os.path.exists(IN_FEED):
        print(f"Error: {IN_FEED} not found. Run build_rss.py first.", file=sys.stderr)
        sys.exit(1)

    t = ET.parse(IN_FEED)
    ch = t.getroot().find("channel")
    items = []

    for it in ch.findall("item"):
        pub = it.findtext("pubDate") or ""
        try:
            dt = parsedate_to_datetime(pub)
            dt = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except:
            dt = datetime.min.replace(tzinfo=timezone.utc)
        items.append((dt, it))

    # Sort by date (newest first)
    items.sort(key=lambda x: x[0], reverse=True)
    return [i for _, i in items], ch


def transform(src_items):
    """Transform items for X format"""
    out = []

    for it in src_items:
        title = collapse_ws(it.findtext("title") or "")
        desc = collapse_ws(it.findtext("description") or "")
        link = (it.findtext("link") or "").strip()

        # Use title first, fall back to description
        body = title or desc
        text = smart_text(body)

        # Create new item
        n = ET.Element("item")
        ET.SubElement(n, "title").text = text
        ET.SubElement(n, "description").text = text
        ET.SubElement(n, "link").text = link

        # Generate GUID
        base = (it.findtext("guid") or link or title or desc).encode("utf-8", "ignore")
        ET.SubElement(n, "guid", attrib={"isPermaLink": "false"}).text = hashlib.sha1(base).hexdigest()

        # Copy publish date
        pub = it.findtext("pubDate")
        if pub:
            ET.SubElement(n, "pubDate").text = pub

        out.append(n)

    return out


def write_feed(path, ch_src, items):
    """Write RSS feed to file"""
    root = ET.Element("rss", attrib={"version": "2.0"})
    ch = ET.SubElement(root, "channel")

    for tag in ["title", "link", "description", "language", "lastBuildDate", "pubDate"]:
        src = ch_src.find(tag)
        if src is not None:
            val = (src.text or "")
            if tag == "title":
                val = "ScalePilot (X)"
            ET.SubElement(ch, tag).text = val

    for it in items:
        ch.append(it)

    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    print(f"✓ Created {path}")


def main():
    all_src, ch = load_items()
    all_x = transform(all_src)

    os.makedirs("feeds", exist_ok=True)
    write_feed(OUT_ALL, ch, all_x)        # All items
    write_feed(OUT_LIVE, ch, all_x[:1])   # Latest 1 item

    print(f"X feed ready with {len(all_x)} total items, 1 live item")


if __name__ == "__main__":
    main()
