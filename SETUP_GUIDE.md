# ScalePilot Setup Guide

Complete setup instructions for your ScalePilot AI-powered social media automation.

## Prerequisites

- GitHub account
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Social media management tool that supports RSS feeds (Zapier, IFTTT, Dlvr.it, Hootsuite, etc.)

## Step-by-Step Setup

### 1. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your OpenAI account
3. Click "Create new secret key"
4. Copy the API key (you won't be able to see it again!)
5. Save it somewhere safe

**Note:** You'll need a paid OpenAI account with credits. The automation uses GPT-4, which costs approximately $0.01-0.03 per post.

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Repository name: `scalepilot-autopost`
3. Make it **Public** (required for RSS feed access and GitHub Pages)
4. Do NOT initialize with README (we already have one)
5. Click "Create repository"

### 3. Push Code to GitHub

From your local `scalepilot-autopost` directory:

```bash
git init
git add .
git commit -m "Initial commit: ScalePilot AI social media automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/scalepilot-autopost.git
git push -u origin main
```

### 4. Add OpenAI API Key to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `OPENAI_API_KEY`
5. Value: Paste your OpenAI API key from step 1
6. Click **Add secret**

### 5. Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. You should see "Build Social Feeds" workflow

### 6. Test the Automation

1. Go to **Actions** tab
2. Click "Build Social Feeds" workflow
3. Click "Run workflow" → "Run workflow"
4. Wait for it to complete (should take 1-2 minutes)
5. Check the **Code** tab - you should see a `feeds/` directory with:
   - `feeds/rss.xml` (main AI-generated feed)
   - `feeds/rss_li.xml` and `feeds/rss_li_live.xml` (LinkedIn)
   - `feeds/rss_x.xml` and `feeds/rss_x_live.xml` (X/Twitter)
   - `feeds/rss_fb.xml` and `feeds/rss_fb_live.xml` (Facebook)

### 7. Get Your RSS Feed URLs

Your RSS feeds are now available at these URLs:

**Option A: Direct GitHub Raw URLs (Works immediately)**
```
https://raw.githubusercontent.com/YOUR_USERNAME/scalepilot-autopost/main/feeds/rss_li_live.xml
https://raw.githubusercontent.com/YOUR_USERNAME/scalepilot-autopost/main/feeds/rss_x_live.xml
https://raw.githubusercontent.com/YOUR_USERNAME/scalepilot-autopost/main/feeds/rss_fb_live.xml
```

**Option B: GitHub Pages URLs (Requires enabling Pages - see step 9)**
```
https://YOUR_USERNAME.github.io/scalepilot-autopost/feeds/rss_li_live.xml
https://YOUR_USERNAME.github.io/scalepilot-autopost/feeds/rss_x_live.xml
https://YOUR_USERNAME.github.io/scalepilot-autopost/feeds/rss_fb_live.xml
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 8. Connect RSS Feeds to Social Media

Now connect these RSS feeds to your social media accounts using one of these tools:

#### Option 1: Zapier (Recommended)
1. Go to [Zapier](https://zapier.com)
2. Create a new Zap
3. Trigger: "RSS by Zapier" → "New Item in Feed"
4. Enter your feed URL
5. Action: Choose your platform (LinkedIn, Twitter, Facebook)
6. Configure posting settings
7. Test and enable

#### Option 2: IFTTT
1. Go to [IFTTT](https://ifttt.com)
2. Create a new Applet
3. If: "RSS Feed" → "New feed item"
4. Enter your feed URL
5. Then: Choose your social media platform
6. Configure posting format
7. Save and enable

#### Option 3: Dlvr.it (Great for multiple platforms)
1. Go to [Dlvr.it](https://dlvr.it)
2. Add a new source
3. Choose "RSS Feed"
4. Enter your feed URL
5. Connect your social media accounts
6. Configure posting schedule
7. Save

#### Option 4: Hootsuite
1. Go to Hootsuite dashboard
2. Add content source
3. Choose RSS/Atom feed
4. Enter your feed URL
5. Configure auto-posting
6. Save

### 9. Enable GitHub Pages (Optional - for cleaner URLs)

1. Go to repository **Settings** → **Pages**
2. Under "Source", select **Deploy from a branch**
3. Branch: `main`, Folder: `/ (root)`
4. Click **Save**
5. Wait a few minutes for deployment
6. Your feeds will be available at: `https://YOUR_USERNAME.github.io/scalepilot-autopost/feeds/`

## Customization

### Change Content Topics

Edit `content/seeds_topics.txt` to add or modify topics:

```
AI automation tools for small business workflows
ChatGPT prompts for marketing and customer service
How to use AI to automate recruiting and hiring
```

Add one topic per line. The AI will randomly select a topic each time it generates content.

### Change Posting Schedule

Edit `.github/workflows/build.yml`:

```yaml
schedule:
  - cron: "0 14 * * *"   # Change this time
```

Use [crontab.guru](https://crontab.guru/) to create your schedule.

Current default: Daily at 2 PM UTC (9 AM EST)

### Adjust Content Style

Edit `ops/rules.json` to control content generation:

```json
{
  "min_emojis": 2,
  "banned_phrases": ["click here", "buy now"],
  "style_weights": {
    "how_to": 1.5,
    "tool_tip": 1.4,
    "case_study": 1.2
  }
}
```

- `min_emojis`: Minimum emojis per post
- `banned_phrases`: Phrases to avoid
- `style_weights`: Higher weights = more likely to be selected

### Change AI Model

Edit `ops/config.json`:

```json
{
  "model": "gpt-4o"
}
```

Options: `gpt-4o`, `gpt-4o-mini` (cheaper), `gpt-4-turbo`

### Pause Automation

Edit `ops/config.json`:

```json
{
  "paused": true
}
```

Set to `true` to pause content generation temporarily.

## Troubleshooting

### No Feeds Generated

1. Check GitHub Actions logs for errors
2. Verify `OPENAI_API_KEY` is set correctly in GitHub Secrets
3. Ensure your OpenAI account has available credits
4. Check if the workflow ran successfully

### OpenAI API Errors

1. Verify API key is correct
2. Check OpenAI account has credits: [OpenAI Usage](https://platform.openai.com/usage)
3. Review GitHub Actions logs for specific error messages
4. API rate limits: Default workflow runs once daily to stay within limits

### Feeds Not Accessible

1. Ensure repository is **Public**
2. Verify feeds exist in the `feeds/` directory
3. Check GitHub Actions completed successfully
4. Try accessing raw GitHub URL first before Pages URL

### Content Quality Issues

1. Edit `content/seeds_topics.txt` to refine topics
2. Adjust `ops/rules.json` to control style and tone
3. Check `analytics/fingerprints.json` for duplicate detection
4. Modify `ops/bandit.json` to adjust style weights

### Duplicate Content Generated

The system has built-in duplicate detection, but you can adjust it:

Edit `ops/config.json`:

```json
{
  "dup_guard": {
    "enabled": true,
    "ngram": 5,
    "threshold": 0.80
  }
}
```

Lower `threshold` = stricter duplicate detection

## Cost Estimation

- GPT-4o: ~$0.01-0.03 per post
- Daily posting: ~$0.30-0.90/month
- 3 platforms daily: ~$1-3/month

**Tip:** Use `gpt-4o-mini` for lower costs (~70% cheaper)

## Advanced Configuration

### Multiple Posting Times

To post multiple times per day, edit `.github/workflows/build.yml`:

```yaml
schedule:
  - cron: "0 9 * * *"   # 9 AM UTC
  - cron: "0 14 * * *"  # 2 PM UTC
  - cron: "0 18 * * *"  # 6 PM UTC
```

### Custom Hashtags

Edit platform-specific scripts:
- `scripts/make_li_feed.py` - LinkedIn hashtags
- `scripts/make_x_feed.py` - X/Twitter hashtags
- `scripts/make_fb_feed.py` - Facebook hashtags

### Add Custom Tags

Edit `content/tags.json`:

```json
["ai", "automation", "smb", "productivity", "marketing"]
```

These tags are used in generated content.

## Support

For issues:
- Check GitHub Actions logs first
- Review this setup guide
- Verify OpenAI API key and credits
- Test RSS feeds in an RSS reader
- Open an issue in the repository

## Next Steps

Once everything is running:

1. Monitor your social media posts for the first week
2. Adjust topics and styles based on engagement
3. Fine-tune posting times for your audience
4. Review OpenAI usage and costs
5. Expand topics as needed

---

**You're all set!** Your ScalePilot AI automation will now generate original content daily about AI tools and small business growth, automatically posting to your social channels.
