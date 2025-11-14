# ScalePilot Content Strategy System

Your AI-powered content strategy director that helps you control what gets posted, tune the vibes, and professionally promote your product.

## What This System Does

**Content Director** = Your AI marketing strategist
- Understands ScalePilot features, benefits, and positioning
- Tracks competitors and market landscape
- Controls content themes and messaging
- Adjusts tone, vibe, and promotional intensity
- Ensures posts align with business goals

## Quick Start

### 1. Review Current Strategy

```bash
cd content/strategy
python content_director.py strategy
```

This shows you what the AI will focus on today:
- Theme (e.g., "productivity", "product", "education")
- Tone guidance
- Promotional approach
- Target audience
- Competitor positioning

### 2. Calibrate Content Vibes

```bash
python calibrate_content.py
```

This opens an interactive menu where you can:

**Adjust Tone:**
- Make content more professional or casual
- Increase friendliness
- Adjust authority/expert level
- Add/remove playfulness

**Change Promotional Intensity:**
- Sell more (increase product mentions)
- Sell less (pure educational value)
- Balance promotion and education

**Shift Audience Focus:**
- Target solopreneurs
- Target small teams
- Target marketing managers

**Review Settings:**
- See current content strategy
- View tone/promotional/audience percentages

### 3. Plan Feature Announcements

When you launch a new feature, schedule announcement content:

```python
from content_director import ContentDirector

director = ContentDirector()
director.add_feature_announcement(
    feature_name="Multi-Brand Management",
    launch_date="2025-02-01",
    announcement_plan={
        "teaser": "Coming soon: Manage multiple brands from one place",
        "launch": "NEW: Multi-Brand Management is here!",
        "follow_up": "Here's how agencies are using Multi-Brand Management"
    }
)
```

## How It Works

### Weekly Theme Rotation

| Day | Theme | Focus |
|-----|-------|-------|
| Monday | Productivity | AI tools that save time |
| Tuesday | Education | How-to guides and tips |
| **Wednesday** | **Product** | **ScalePilot features** (main pitch day) |
| Thursday | Industry | SMB challenges and solutions |
| Friday | Inspiration | Success stories and wins |
| Weekend | Free Choice | Mix of trending topics |

### Promotional Mix

**Default Balance:**
- 10% Direct sales pitch (very rare)
- 30% Soft product mention (subtle)
- 60% Pure educational value (no pitch)

**Wednesday = Product Day:**
- Highlights one ScalePilot feature
- Explains benefits and use cases
- Professional but not pushy

### Content Angles

The system rotates through different angles:
- **Problem → Solution** (40%): "Still doing X manually? Try Y"
- **How-To Guide** (30%): "3 steps to automate your content"
- **Industry Insight** (15%): "Why SMBs are adopting AI in 2025"
- **Inspiration** (15%): "How one solopreneur saves 10hrs/week"

## Knowledge Base Files

### scalepilot_features.json
Contains:
- All current features with benefits and use cases
- Upcoming features ("coming soon")
- Key differentiators
- Target audience pain points and goals

**Update this when:**
- Launching new features
- Changing positioning
- Adding new use cases

### competitors.json
Contains:
- Direct competitors (Buffer, Hootsuite, etc.)
- AI content competitors (Jasper, Copy.ai)
- Automation competitors (Zapier, Make)
- Our advantages over each
- Market positioning statements

**Update this when:**
- Competitors launch new features
- Pricing changes
- New competitors enter market
- Your positioning evolves

### vibe_settings.json (auto-generated)
Contains your calibrated settings:
- Tone percentages
- Promotional intensity
- Content angle mix
- Audience focus

**This file is created when you run calibrate_content.py**

## Examples: Tuning Your Content

### Make Content MORE Promotional

```bash
python calibrate_content.py
# Choose option 5: "Increase product mentions"
```

Result:
- More frequent ScalePilot mentions
- Clearer calls-to-action
- Stronger benefit statements
- 20% direct sales content

### Make Content LESS Promotional (Pure Value)

```bash
python calibrate_content.py
# Choose option 6: "Decrease product mentions"
```

Result:
- 80% educational value
- Rare product mentions
- Focus on helping, not selling
- Build authority first

### Focus on Solopreneurs

```bash
python calibrate_content.py
# Choose option 8: "Focus more on solopreneurs"
```

Result:
- One-person business challenges
- Time management focus
- Budget-conscious solutions
- "I" language instead of "we/team"

### Make Content More Professional

```bash
python calibrate_content.py
# Choose option 1: "Make content more professional"
# Set to 8/10 for high professionalism
```

Result:
- Formal tone
- Less casual language
- More data/stats
- Corporate-friendly

## Competitor Battle Cards

When creating content against competitors, use these angles:

### vs Buffer/Hootsuite
**Their Weakness:** Manual content creation
**Our Strength:** AI generates content for you
**Angle:** "Scheduling is the easy part. Creating GOOD content is the hard part."

### vs Jasper/Copy.ai
**Their Weakness:** Requires daily manual prompting
**Our Strength:** Fully automated, runs on schedule
**Angle:** "Stop prompting AI every day. Let it run automatically."

### vs Agencies
**Their Weakness:** Expensive ($2000+/month)
**Our Strength:** Affordable ($20-50/month equivalent)
**Angle:** "Agency quality at solopreneur prices"

### vs DIY/Manual
**Their Weakness:** Time-consuming (10+ hours/week)
**Our Strength:** 10 seconds of AI work
**Angle:** "Still manually posting in 2025?"

## Integrating Strategy into Content Generation

The Content Director's strategy automatically feeds into `build_rss.py`.

To manually inject strategy:

```python
from content.strategy.content_director import ContentDirector

director = ContentDirector()
strategy = director.get_strategy_prompt()

# Use strategy in your AI prompts:
# - strategy['today_theme']
# - strategy['tone_guidance']
# - strategy['promotional_approach']
# - strategy['feature_to_highlight']
```

## Tips for Working with the Content Director

**1. Start Conservative**
- Begin with low promotional intensity (60% educational)
- Build trust and authority first
- Gradually increase promotion as audience grows

**2. Test and Iterate**
- Run one week with current settings
- Review analytics
- Adjust based on what's working

**3. Seasonal Adjustments**
- Q4: More promotional (holiday sales)
- Q1: More educational (New Year learning)
- Pre-launch: Teaser content
- Post-launch: Feature highlights

**4. Audience Evolution**
- Start: Focus on solopreneurs (easier to reach)
- Growth: Shift to small teams (higher LTV)
- Scale: Target marketing managers (enterprise entry)

**5. Competitor Response**
- Monitor competitor announcements
- Adjust positioning when they launch features
- Maintain your unique angle

## Troubleshooting

**Content feels too salesy**
→ Run `calibrate_content.py` and choose option 6 (decrease promotional)

**Not enough product mentions**
→ Run `calibrate_content.py` and choose option 5 (increase promotional)

**Tone doesn't match brand**
→ Adjust tone sliders (options 1-4) until it feels right

**Want to announce new feature**
→ Use `director.add_feature_announcement()` to schedule campaign

## Next Steps

1. Review [scalepilot_features.json](scalepilot_features.json) - Add any missing features
2. Review [competitors.json](competitors.json) - Update competitor info
3. Run `python calibrate_content.py` - Set your initial vibe
4. Run `python content_director.py strategy` - See what AI will post today
5. Integrate strategy into `build_rss.py` (coming next)

---

**You now have a professional AI marketing strategist.**
Talk to it, tune it, and let it guide your content to match your business goals.
