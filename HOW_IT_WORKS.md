# How the Career Forge (Current) Automation Works

## Overview

Your current Career Forge automation uses a **2-step architecture**:

1. **GitHub Actions generates AI content** and creates RSS feeds
2. **Buffer reads RSS feeds** and posts to social media

This is **NOT** using Buffer's API directly. Instead, Buffer has a built-in RSS feed reader feature.

---

## Step-by-Step Flow

### Step 1: GitHub Actions - Content Generation (Twice Daily)

**When:** Runs 2x per day (7:40 AM and 2:10 PM Arizona time)

**What happens:**

1. **`build_rss.py` runs** (line 38 in post.yml)
   - Calls OpenAI API to generate ONE new career advice post
   - Uses GPT-4 to create content in "career coach voice"
   - Adds the new item to `rss.xml` (the master feed)

2. **`rss.xml` gets committed to GitHub** (lines 86-98)
   - The new post is saved to the repository
   - This makes it available via GitHub Pages URL

3. **Platform-specific feeds are generated** (lines 101-105)
   - `scripts/make_li_feed.py` → Creates `rss_li_live.xml` (for LinkedIn)
   - `scripts/make_x_feed.py` → Creates `rss_x_live.xml` (for X/Twitter)
   - `scripts/make_fb_feed.py` → Creates `rss_fb_live.xml` (for Facebook)

   These "*_live.xml" files contain **ONLY the latest post** (not the full feed)

4. **Social feeds committed to GitHub** (lines 107-119)
   - All the platform feeds are saved to repository
   - Now accessible via GitHub Pages URLs

### Step 2: Buffer - RSS Feed Reading (Continuous)

**Where Buffer is configured:**

You must have manually configured Buffer's RSS feed feature to point to:
- `https://nikopastore.github.io/cf-autopost-feed/rss_li_live.xml` (LinkedIn)
- `https://nikopastore.github.io/cf-autopost-feed/rss_x_live.xml` (X/Twitter)
- `https://nikopastore.github.io/cf-autopost-feed/rss_fb_live.xml` (Facebook)

**How Buffer works:**

1. Buffer checks these RSS feed URLs every 15-30 minutes (Buffer's schedule, not ours)
2. When Buffer sees a NEW item in the feed (new GUID), it adds it to your posting queue
3. Buffer posts according to YOUR Buffer posting schedule

---

## Key Architecture Points

### RSS Feed Structure

Each platform has TWO feeds:

- **Full feed** (`rss_li.xml`, `rss_x.xml`, `rss_fb.xml`) - Contains all historical posts
- **Live feed** (`rss_li_live.xml`, `rss_x_live.xml`, `rss_fb_live.xml`) - Contains ONLY the latest post

**Why two feeds?**
- Buffer only needs to see the latest post
- Using the "live" feed prevents Buffer from re-posting old content
- Each "live" feed contains exactly 1 item

### GitHub Pages as RSS Host

Your RSS feeds are hosted at:
```
https://nikopastore.github.io/cf-autopost-feed/rss_li_live.xml
https://nikopastore.github.io/cf-autopost-feed/rss_x_live.xml
https://nikopastore.github.io/cf-autopost-feed/rss_fb_live.xml
```

These URLs are publicly accessible and Buffer reads from them.

### Content Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: GitHub Actions (2x daily)                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────┐
         │  build_rss.py              │
         │  - Calls OpenAI GPT-4      │
         │  - Generates 1 new post    │
         └────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────┐
         │  rss.xml (master feed)     │
         │  - Contains all posts      │
         └────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────────┐
         │  Platform-specific generators      │
         │  - make_li_feed.py                 │
         │  - make_x_feed.py                  │
         │  - make_fb_feed.py                 │
         └────────────────────────────────────┘
                          │
                          ▼
    ┌─────────────────────┬─────────────────────┐
    │                     │                     │
    ▼                     ▼                     ▼
rss_li_live.xml    rss_x_live.xml     rss_fb_live.xml
(1 latest post)    (1 latest post)    (1 latest post)
    │                     │                     │
    │                     │                     │
    └─────────────────────┴─────────────────────┘
                          │
              Committed to GitHub → GitHub Pages
                          │
                          │
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Buffer (checks every 15-30 min)                    │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────┐
         │  Buffer RSS Feature        │
         │  - Reads RSS feed URLs     │
         │  - Detects new GUID        │
         │  - Adds to posting queue   │
         └────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────┐
         │  Your Social Accounts      │
         │  - LinkedIn                │
         │  - X (Twitter)             │
         │  - Facebook                │
         └────────────────────────────┘
```

---

## Important Notes

### 1. Buffer RSS Feature vs. Buffer API

**Current Career Forge uses: Buffer RSS Feature**
- Buffer automatically polls your RSS feed URLs
- When it finds a new item, it queues it for posting
- You configure this in Buffer's dashboard under "Feeds" or "RSS" section

**ScalePilot will use: Buffer API** (different approach)
- GitHub Actions directly calls Buffer's API to create posts
- No RSS polling - instant posting
- More direct control

### 2. No Direct API Posting

Your current automation does **NOT** call Buffer's API to create posts. It:
1. Generates content
2. Saves to RSS feeds on GitHub Pages
3. Lets Buffer discover and import the posts via RSS polling

### 3. Timing

- **Content Generation:** 2x daily (GitHub Actions schedule)
- **Buffer Check:** Every 15-30 minutes (Buffer's internal schedule)
- **Actual Posting:** Based on YOUR Buffer posting schedule

So there can be a 15-30 minute delay between when GitHub Actions creates content and when Buffer adds it to the queue.

---

## How to Find Your Buffer RSS Configuration

1. Log into Buffer
2. Go to **Settings** → **RSS Feeds** (or "Channels" → "Add Channel" → "RSS")
3. You should see 3 RSS feeds configured pointing to your GitHub Pages URLs
4. Each feed is connected to one social profile (LinkedIn, X, Facebook)

---

## ScalePilot Differences

The **NEW ScalePilot automation** I created works differently:

### ScalePilot Architecture:

1. GitHub Actions fetches content from external RSS feeds (no AI generation)
2. Scores and filters the content for relevance
3. **Directly calls Buffer API** to create posts (no RSS intermediary)
4. Also saves RSS feeds to GitHub for backup/reference

### Why Different?

- **No AI cost:** Uses existing content from industry RSS feeds
- **Faster posting:** Direct API call, no waiting for Buffer to poll
- **More control:** Can customize exactly when posts go out
- **Simpler:** One-step process instead of two-step

---

## Summary

**Career Forge (current):**
```
GitHub Actions → AI generates post → RSS feed → GitHub Pages → Buffer polls RSS → Posts to social
```

**ScalePilot (new):**
```
GitHub Actions → Fetch RSS → Score content → Buffer API → Posts to social
```

Both approaches work! Career Forge uses the RSS intermediary because you're generating unique AI content. ScalePilot uses direct API because it's curating existing content from multiple sources.

---

## Next Steps for Setting Up ScalePilot

You'll need to:

1. Get your Buffer API token (different from RSS setup)
2. Get your Buffer profile IDs for the ScalePilot social accounts
3. Configure GitHub secrets
4. Run the automation

The ScalePilot automation I created will post **directly via Buffer API**, not via RSS feeds (though it still generates RSS feeds for reference).

If you want ScalePilot to work the SAME WAY as Career Forge (RSS-based), let me know and I can modify it!
