#!/usr/bin/env python3
"""
ScalePilot Facebook Feed Generator
Creates Facebook-optimized feeds from master feed with ScalePilot branding
"""

import xml.etree.ElementTree as ET
import re
import hashlib
import html
import os
import sys

# Facebook platform configuration
PLATFORM = "facebook"
PLATFORM_TONE = "Engaging, relatable, conversational"
WORD_COUNT_MIN = 120
WORD_COUNT_MAX = 180

# File paths
IN_FEED = "feeds/rss.xml"
OUT_ALL = "feeds/rss_fb.xml"
OUT_LIVE = "feeds/rss_fb_live.xml"

# Facebook branding - friendly and approachable
FB_SUFFIX = "#ScalePilot #AIForSMB #SmallBusinessAI"


def clean(s):
    """Remove HTML tags and clean text"""
    s = re.sub(r"<[^>]+>", "", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def fb_text(title, desc):
    """Format text for Facebook with friendly tone"""
    # Facebook allows longer posts, prefer description
    base = desc if desc else title
    base = base.strip()

    # Don't duplicate suffix if already present
    if base.lower().endswith(FB_SUFFIX.lower()):
        return base

    return (base + "\n\n" + FB_SUFFIX).strip() if base else FB_SUFFIX


def build(items, ch_src, out_path):
    """Build RSS feed with specified items"""
    root = ET.Element("rss", attrib={"version": "2.0"})
    ch = ET.SubElement(root, "channel")

    # Copy channel metadata
    for t in ["title", "link", "description", "language", "lastBuildDate", "pubDate"]:
        src = ch_src.find(t)
        if src is not None:
            val = (src.text or "")
            if t == "title":
                val = "ScalePilot (Facebook)"
            ET.SubElement(ch, t).text = val

    # Add items
    for it in items:
        ch.append(it)

    ET.ElementTree(root).write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"✓ Created {out_path}")


def main():
    if not os.path.exists(IN_FEED):
        print(f"Error: {IN_FEED} not found. Run build_rss.py first.", file=sys.stderr)
        sys.exit(1)

    # Parse input feed
    t = ET.parse(IN_FEED)
    ch = t.getroot().find("channel")

    items = []
    for it in ch.findall("item"):
        title = clean(it.findtext("title"))
        desc = clean(it.findtext("description"))
        link = (it.findtext("link") or "").strip()

        # Format for Facebook
        text = fb_text(title, desc)

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

        items.append(n)

    # Build feeds
    os.makedirs("feeds", exist_ok=True)
    build(items, ch, OUT_ALL)        # All items
    build(items[:1], ch, OUT_LIVE)  # Latest 1 item only

    print(f"Facebook feed ready with {len(items)} total items, 1 live item")


if __name__ == "__main__":
    main()
