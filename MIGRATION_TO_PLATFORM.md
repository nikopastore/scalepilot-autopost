# Migration to Social Pilot Platform

This document captures ScalePilot's current automation configuration for migration to the multi-tenant Social Pilot platform.

## Current Configuration

### Brand Information
- **Name:** ScalePilot
- **Slug:** scalepilot
- **Industry:** SaaS / AI Tools
- **Website:** https://scalepilot.com/
- **Target Audience:** Small business owners, operations managers, SMB marketing teams

### Content Configuration

**Topics File:** `content/seeds_topics.txt`
- Location: Local file
- Topics: AI automation, SMB growth, productivity tools, etc.

**Content Rules:** `ops/rules.json`
- Min emojis: 2
- Enforce second person: true
- Allow first person in quotes only: true
- Banned phrases: Listed in rules.json

**Style Weights:** `ops/bandit.json`
- how_to: 1.5
- tool_tip: 1.4
- case_study: 1.2
- quick_win: 1.3
- stats_insight: 1.1
- framework: 1.0
- mistake_avoid: 1.1

### AI Configuration
- **Model:** gpt-4o
- **Temperature:** 0.7
- **Fallback Models:** gpt-4o, gpt-4o-mini

### Quality Gates
- Second-person voice enforcement
- Banned phrase detection
- Tense conflict detection
- Dialogue marker filtering
- Duplicate detection (5-gram similarity, 0.8 threshold)

### Posting Schedule
- **Frequency:** Daily
- **Time:** 3 PM UTC (15:00)
- **Workflow:** GitHub Actions (.github/workflows/build.yml)

### Social Media Platforms
- LinkedIn (via Zapier → Buffer)
- X/Twitter (via Zapier → Buffer)
- Facebook (via Zapier → Buffer)

### RSS Feed URLs
- LinkedIn: `/feeds/rss_li_live.xml`
- X/Twitter: `/feeds/rss_x_live.xml`
- Facebook: `/feeds/rss_fb_live.xml`

### Content History
- **Location:** `analytics/fingerprints.json`
- **Format:** Array of {guid, ngrams}
- **History Size:** 200 posts

### Analytics
- **Metrics File:** `analytics/metrics.json`
- **Tracked Metrics:** views, likes, shares, comments, clicks
- **Platforms:** LinkedIn, Twitter, Facebook

## Migration Steps

### Phase 1: Data Export (Before Migration)

1. **Export Content History**
   ```bash
   # Copy fingerprints for duplicate detection
   cp analytics/fingerprints.json migration/scalepilot_fingerprints.json

   # Export all RSS feeds (historical content)
   cp feeds/rss.xml migration/scalepilot_content_history.xml
   ```

2. **Export Configuration**
   ```bash
   # Brand settings
   cp content/seeds_topics.txt migration/scalepilot_topics.txt
   cp content/tags.json migration/scalepilot_tags.json
   cp ops/rules.json migration/scalepilot_rules.json
   cp ops/bandit.json migration/scalepilot_bandit.json
   ```

3. **Export Analytics**
   ```bash
   cp analytics/metrics.json migration/scalepilot_metrics.json
   ```

### Phase 2: Platform Setup (In New Repo)

1. **Create Account**
   ```sql
   INSERT INTO accounts (name, slug, plan, status)
   VALUES ('ScalePilot', 'scalepilot', 'pro', 'active');
   ```

2. **Create Brand**
   ```sql
   INSERT INTO brands (account_id, name, slug, industry, topics, content_rules, ...)
   VALUES (...);
   ```

3. **Import Content History**
   - Parse `migration/scalepilot_content_history.xml`
   - Insert posts into `posts` table
   - Import fingerprints for duplicate detection

4. **Import Analytics**
   - Parse `migration/scalepilot_metrics.json`
   - Insert into `analytics` table

### Phase 3: Cutover

1. **Test New Platform**
   - Verify content generation works
   - Test posting to social platforms
   - Validate analytics tracking

2. **Run Both in Parallel** (1 week)
   - Old repo continues running
   - New platform also generates content
   - Compare quality and reliability

3. **Switch Traffic**
   - Point Zapier to new RSS feeds
   - Or connect platforms directly to new platform

4. **Deprecate Old Repo**
   - Archive `scalepilot-autopost` repository
   - Keep as reference

## Migration Script (To Be Created)

Location: `socialpilot-platform/scripts/migrate-scalepilot.ts`

```typescript
// Pseudocode for migration script
async function migrateScalePilot() {
  // 1. Create account
  const account = await createAccount({
    name: 'ScalePilot',
    slug: 'scalepilot',
    plan: 'pro'
  });

  // 2. Create brand with configuration
  const brand = await createBrand({
    accountId: account.id,
    name: 'ScalePilot',
    industry: 'saas',
    topics: importTopics('migration/scalepilot_topics.txt'),
    contentRules: importRules('migration/scalepilot_rules.json'),
    // ... more config
  });

  // 3. Import content history
  const posts = parseRSS('migration/scalepilot_content_history.xml');
  await bulkInsertPosts(brand.id, posts);

  // 4. Import fingerprints
  const fingerprints = importFingerprints('migration/scalepilot_fingerprints.json');
  await bulkInsertFingerprints(fingerprints);

  // 5. Import analytics
  const metrics = importMetrics('migration/scalepilot_metrics.json');
  await bulkInsertAnalytics(brand.id, metrics);
}
```

## Reusable Code to Port

### Core Libraries (Move to new platform)

1. **Content Generation** (`build_rss.py`)
   - `call_openai()` - OpenAI API wrapper
   - `quality_gate()` - Content validation
   - `ngrams()` - Duplicate detection
   - `sanitize_xline()` - Content cleaning

2. **Quality Gates** (`build_rss.py`)
   - Second-person enforcement
   - Banned phrase detection
   - Tense conflict detection
   - Emoji validation

3. **RSS Generation** (`build_rss.py`)
   - Feed scaffolding
   - Item creation
   - Platform-specific formatting

4. **Analytics** (`analytics/fetch_metrics.py`)
   - Buffer API integration
   - Metrics normalization
   - Data aggregation

### Platform-Specific Scripts

- `scripts/make_li_feed.py` - LinkedIn formatting
- `scripts/make_x_feed.py` - Twitter formatting
- `scripts/make_fb_feed.py` - Facebook formatting

## Environment Variables to Migrate

```bash
# From current repo
OPENAI_API_KEY=...
BRAND=ScalePilot
SITE_URL=https://scalepilot.com/
MODEL=gpt-4o

# For new platform (add to brand config in DB)
# These become brand settings, not env vars
```

## Testing Checklist

Before fully migrating:
- [ ] Content generation produces same quality
- [ ] Duplicate detection works with imported fingerprints
- [ ] RSS feeds are compatible with Zapier
- [ ] Analytics tracking is accurate
- [ ] Posting schedule matches (3 PM UTC)
- [ ] All social platforms connected

## Rollback Plan

If migration fails:
1. Keep old repo running (don't shut down)
2. Debug issues in new platform
3. Fix and retry migration
4. Only deprecate old repo when new platform is stable for 2+ weeks

## Timeline

- **Week 1:** Build new platform core
- **Week 2:** Build automation engine
- **Week 3:** Test with ScalePilot migration
- **Week 4:** Run both in parallel
- **Week 5:** Full cutover, deprecate old repo

---

**Next Steps:**
1. Continue building Social Pilot platform in new repo
2. Come back here when ready to migrate
3. Run export scripts to capture current state
4. Use migration script to import into new platform
