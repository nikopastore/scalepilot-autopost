# ScalePilot Social Media Automation

AI-powered social media content generation for HirePriority - Recruitment solutions for insurance agencies.

This system uses OpenAI to automatically generate original, engaging content about recruitment ROI, hiring bottlenecks, and talent acquisition strategies. Content is delivered via RSS feeds that you can connect to your social media management tools.

## Features

- **AI-Generated Content**: Uses GPT-4 to create original, engaging posts tailored for SMBs
- **Daily Automated Posts**: Generates fresh content daily for LinkedIn, X (Twitter), and Facebook
- **AI & SMB Focused**: Topics cover AI automation, productivity, marketing, recruiting, training, and business growth
- **Friendly, Practical Tone**: Content written in an approachable, actionable style
- **RSS Feed Output**: Platform-specific RSS feeds you can use with any social media tool
- **GitHub Actions**: Fully automated - runs daily without manual intervention
- **Duplicate Detection**: Smart filtering prevents repetitive content
- **Easy Integration**: Connect the RSS feeds to tools like Zapier, IFTTT, or your social media scheduler

## Quick Start

### 1. Prerequisites

- GitHub account
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Social media management tool that supports RSS feeds (Zapier, IFTTT, Hootsuite, etc.)

### 2. Fork or Clone Repository

1. Fork this repository or clone it to your GitHub account
2. Push to your repository

### 3. Add OpenAI API Key

1. Go to your GitHub repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `OPENAI_API_KEY`
4. Value: Paste your OpenAI API key
5. Click **Add secret**

### 4. Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. Manually run the "Build Social Feeds" workflow to test

### 5. Get Your RSS Feed URLs

After the workflow runs, your RSS feeds will be available at:

- **LinkedIn Feed**: `https://raw.githubusercontent.com/YOUR_USERNAME/scalepilot-autopost/main/feeds/rss_li_live.xml`
- **X (Twitter) Feed**: `https://raw.githubusercontent.com/YOUR_USERNAME/scalepilot-autopost/main/feeds/rss_x_live.xml`
- **Facebook Feed**: `https://raw.githubusercontent.com/YOUR_USERNAME/scalepilot-autopost/main/feeds/rss_fb_live.xml`

Or if you enable GitHub Pages:
- `https://YOUR_USERNAME.github.io/scalepilot-autopost/feeds/rss_li_live.xml`
- `https://YOUR_USERNAME.github.io/scalepilot-autopost/feeds/rss_x_live.xml`
- `https://YOUR_USERNAME.github.io/scalepilot-autopost/feeds/rss_fb_live.xml`

### 6. Connect to Your Social Media Tool

Use these RSS feed URLs with tools like:
- **Zapier**: Create a "RSS by Zapier" trigger → "LinkedIn/Twitter/Facebook" action
- **IFTTT**: Use RSS feed trigger → Social media action
- **Hootsuite**: Add RSS feed as a content source
- **Buffer**: Use RSS feed integration (if available)
- **Dlvr.it**: Connect RSS feeds to social accounts
- **SocialBee**: Import RSS feeds for auto-posting

### 7. Enable GitHub Pages (Optional)

1. Go to **Settings** → **Pages**
2. Enable GitHub Pages from the `main` branch, `/` (root) folder
3. Access feeds via your GitHub Pages URL

## Customization

### Adjusting Content Strategy

Edit HirePriority pain points in `content/hirepriority/pain_points.json`:

```json
{
  "category": "Your Category",
  "hook": "Your compelling hook",
  "bottleneck": "Why this problem persists",
  "solution": "High-level strategic solution"
}
```

Customize platform tone in `content/hirepriority/platform_settings.json`.

### Adjusting Posting Frequency

Edit [.github/workflows/build.yml](.github/workflows/build.yml) to change the schedule:

```yaml
schedule:
  - cron: '0 14 * * *'  # Daily at 2 PM UTC (9 AM EST)
```

Use [crontab.guru](https://crontab.guru/) to create custom schedules.

### Content Style and Rules

Modify AI generation rules in [ops/rules.json](ops/rules.json):
- `min_emojis`: Minimum emojis per post (default: 2)
- `banned_phrases`: Phrases to avoid in content
- `style_weights`: Adjust content style preferences (how_to, tool_tip, case_study, etc.)

### Platform Customization

Platform-specific formatting scripts:
- [scripts/make_li_feed.py](scripts/make_li_feed.py) - LinkedIn (longer content, hashtags)
- [scripts/make_x_feed.py](scripts/make_x_feed.py) - X/Twitter (280 char limit)
- [scripts/make_fb_feed.py](scripts/make_fb_feed.py) - Facebook (friendly, engaging)

### Xquik or TweetClaw Trend Signals

Reviewed Xquik/TweetClaw exports can be added to `content/trends.json`, which
`build_rss.py` already reads when selecting feed topics:

```bash
python scripts/import_xquik_trends.py \
  --input path/to/xquik-export.jsonl \
  --output content/trends.json \
  --limit 10
```

The importer accepts CSV, JSON, and JSONL rows. It skips rows marked
`unreviewed`, `needs_review`, `not_approved`, `pending`, or `rejected` by
default so draft social data does not enter the automated RSS topic pool.

## How It Works

1. **AI Content Generation**: OpenAI GPT-4 creates original posts from topic seeds
2. **Style Selection**: Randomly selects content styles (how-to, tool tip, case study, etc.)
3. **Quality Checks**: Validates tone, length, and duplicate detection
4. **Platform Optimization**: Formats content for LinkedIn, X, and Facebook
5. **RSS Feed Creation**: Generates platform-specific RSS feeds updated daily
6. **Automation Ready**: Use feeds with any social media scheduling tool

## File Structure

```
scalepilot-autopost/
├── README.md                      # This file
├── build_rss.py                   # Main RSS builder
├── constants.py                   # Configuration and settings
├── logger_config.py               # Logging setup
├── backup_manager.py              # Backup and recovery
├── health_check.py                # System health monitoring
├── scripts/
│   ├── make_li_feed.py           # LinkedIn feed generator
│   ├── make_x_feed.py            # X (Twitter) feed generator
│   ├── make_fb_feed.py           # Facebook feed generator
│   ├── build_analytics.py        # Analytics dashboard builder
│   ├── optimize_times.py         # Optimal posting time analyzer
│   └── suggest_cron.py           # Cron schedule suggestions
├── tools/
│   └── buffer_list_profiles.py   # List your Buffer profiles
├── analytics/
│   ├── fetch_metrics.py          # Fetch engagement data
│   └── dashboard.html            # Analytics dashboard (auto-generated)
├── .github/workflows/
│   ├── build.yml                 # Daily feed update workflow
│   └── metrics.yml               # Weekly analytics workflow
└── feeds/                        # Generated RSS feeds (auto-created)
```

## Troubleshooting

### RSS Feeds Not Updating

1. Check GitHub Actions logs for errors
2. Verify workflow is enabled and running on schedule
3. Manually trigger "Build Social Feeds" workflow to test

### No Content Being Generated

1. Check RSS feeds are accessible in [constants.py](constants.py)
2. Verify content filters aren't too restrictive
3. Review GitHub Actions logs for fetch errors
4. Test locally: `python build_rss.py`

### RSS Feeds Not Accessible

1. Ensure GitHub repository is public
2. Check that feeds are being committed to the repository
3. Verify the file path: `feeds/rss_li_live.xml`, `feeds/rss_x_live.xml`, `feeds/rss_fb_live.xml`
4. If using GitHub Pages, ensure it's enabled and deployed

## Support

For issues or questions:
- Check GitHub Actions logs
- Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
- Open an issue in this repository

## License

MIT License - Feel free to customize for your needs!

---

**Built for ScalePilot** - Empowering SMBs with AI automation 🚀
