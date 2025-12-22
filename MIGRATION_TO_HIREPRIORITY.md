# Migration to HirePriority Content System

**Date:** 2025-12-22
**Status:** Complete

## What Changed

This repository has been migrated from ScalePilot (AI automation) content to HirePriority (recruitment solutions) content.

## ScalePilot Archive

All ScalePilot configuration has been preserved in `content/archive/scalepilot/`:
- `seeds_topics.txt` - Original 50 AI automation topics
- `scalepilot_features.json` - ScalePilot product features

## Reverting to ScalePilot

To restore ScalePilot content:

1. Move archived files back:
```bash
mv content/archive/scalepilot/seeds_topics.txt content/
mv content/archive/scalepilot/scalepilot_features.json content/strategy/
```

2. Restore original `build_rss.py` from git history:
```bash
git log --all --full-history -- build_rss.py
git checkout <commit-before-migration> -- build_rss.py
```

3. Archive HirePriority configuration:
```bash
mv content/hirepriority content/archive/
```

## HirePriority Content System

### Configuration Files
- `content/hirepriority/features.json` - HirePriority product features
- `content/hirepriority/pain_points.json` - Daily pain point rotation
- `content/hirepriority/content_recipe.json` - Content structure template
- `content/hirepriority/platform_settings.json` - Platform-specific settings

### Content Recipe
All content follows: Hook → Bottleneck → Solution → Pivot

### Platform Optimization
- **LinkedIn:** Professional, 150-200 words
- **X/Twitter:** Punchy, 100-150 words
- **Facebook:** Engaging, 120-180 words

## Testing

To test content generation:
```bash
python scripts/make_li_feed.py
python scripts/make_x_feed.py
python scripts/make_fb_feed.py
```

## Support

See design document: `docs/plans/2025-12-22-hirepriority-content-migration-design.md`
