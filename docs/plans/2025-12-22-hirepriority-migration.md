# HirePriority Content Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate social media automation from ScalePilot to HirePriority with platform-specific content optimization

**Architecture:** Archive existing ScalePilot configuration, create new HirePriority content strategy files (features, pain points, platform settings), update AI prompt system in build_rss.py and platform-specific feed scripts to use HirePriority content recipe (Hook → Bottleneck → Solution → Pivot)

**Tech Stack:** Python 3, OpenAI GPT-4, XML/RSS generation, JSON configuration files

---

## Phase 1: Archive ScalePilot & Create HirePriority Structure

### Task 1: Archive ScalePilot Configuration

**Files:**
- Create: `content/archive/scalepilot/` (directory)
- Move: `content/seeds_topics.txt` → `content/archive/scalepilot/seeds_topics.txt`
- Move: `content/strategy/scalepilot_features.json` → `content/archive/scalepilot/scalepilot_features.json`

**Step 1: Create archive directory**

```bash
mkdir -p content/archive/scalepilot
```

**Step 2: Move ScalePilot files to archive**

```bash
mv content/seeds_topics.txt content/archive/scalepilot/
mv content/strategy/scalepilot_features.json content/archive/scalepilot/
```

**Step 3: Verify files moved**

```bash
ls -la content/archive/scalepilot/
```

Expected: `seeds_topics.txt` and `scalepilot_features.json` present

**Step 4: Commit**

```bash
git add -A
git commit -m "chore: archive ScalePilot configuration for future reactivation"
```

---

### Task 2: Create HirePriority Directory Structure

**Files:**
- Create: `content/hirepriority/` (directory)

**Step 1: Create HirePriority directory**

```bash
mkdir -p content/hirepriority
```

**Step 2: Verify directory created**

```bash
ls -la content/
```

Expected: `hirepriority/` directory present

**Step 3: Commit**

```bash
git add content/hirepriority/
git commit -m "feat: create HirePriority content directory"
```

---

### Task 3: Create HirePriority Features Configuration

**Files:**
- Create: `content/hirepriority/features.json`

**Step 1: Write features.json**

```json
{
  "product_name": "HirePriority",
  "tagline": "AI-Powered Recruiting for Insurance Agencies",
  "cta_url": "https://hirepriority.scalepilotlabs.com/",
  "features": [
    {
      "name": "NIPR Auto-Verification",
      "benefit": "Eliminate unlicensed candidates automatically",
      "use_case": "Insurance agencies wasting time on unqualified applicants"
    },
    {
      "name": "Voice Confidence AI",
      "benefit": "Assess sales capability in 10 seconds",
      "use_case": "Identifying top performers before interviews"
    },
    {
      "name": "One-Click SMS Invites",
      "benefit": "85% response rate vs. traditional emails",
      "use_case": "Engaging passive candidates quickly"
    },
    {
      "name": "Resume Scoring & Ranking",
      "benefit": "AI-powered candidate filtering in seconds",
      "use_case": "Cutting screening time from 20 hours to 2"
    },
    {
      "name": "AES-256 Encryption",
      "benefit": "Secure resume handling and data protection",
      "use_case": "Compliance and candidate privacy"
    }
  ],
  "value_props": [
    "Save 15-20 hours per role",
    "Fill positions in 2 weeks instead of 2 months",
    "Pre-qualified candidates only",
    "85% SMS response rate"
  ]
}
```

**Step 2: Verify JSON is valid**

```bash
python -m json.tool content/hirepriority/features.json
```

Expected: Valid JSON output

**Step 3: Commit**

```bash
git add content/hirepriority/features.json
git commit -m "feat: add HirePriority features configuration"
```

---

### Task 4: Create Pain Points Rotation Configuration

**Files:**
- Create: `content/hirepriority/pain_points.json`

**Step 1: Write pain_points.json**

```json
{
  "pain_points": [
    {
      "category": "Financial Cost",
      "hook": "The average cost of a bad hire is 30% of their first-year salary",
      "bottleneck": "Generic job boards flood you with unqualified resumes, paralyzing decision-making",
      "solution": "Pre-qualification systems reduce noise by 80%, focusing only on high-intent candidates"
    },
    {
      "category": "Time Waste",
      "hook": "Why are you still spending 20 hours a week on initial screenings?",
      "bottleneck": "Manual resume review is the biggest hiring bottleneck in modern recruitment",
      "solution": "AI-powered scoring ranks candidates in seconds based on role-specific criteria"
    },
    {
      "category": "Operational Roadblocks",
      "hook": "Your average time-to-fill is 42 days. Your competitors are at 14.",
      "bottleneck": "Outdated tech and manual processes extend vacancy timelines by weeks",
      "solution": "Automated workflows compress hiring cycles without sacrificing quality"
    },
    {
      "category": "Candidate Experience",
      "hook": "73% of candidates ghost companies with poor communication",
      "bottleneck": "Email-based outreach has less than 15% response rates",
      "solution": "SMS-first engagement drives 5x higher responses and faster pipeline movement"
    },
    {
      "category": "Strategic Solutions",
      "hook": "Reactive hiring costs 3x more than proactive talent pipeline building",
      "bottleneck": "Most companies only recruit when desperate, missing top talent",
      "solution": "Continuous talent pool nurturing keeps high-quality candidates warm"
    },
    {
      "category": "Candidate Bottlenecks",
      "hook": "The myth of 'talent scarcity' is really a targeting problem",
      "bottleneck": "Broad job postings attract volume, not quality",
      "solution": "Niche-focused recruitment models surface pre-qualified specialists"
    },
    {
      "category": "Financial Cost",
      "hook": "Every day a critical role remains open, your revenue potential shrinks",
      "bottleneck": "Traditional hiring processes extend time-to-fill by relying on reactive strategies",
      "solution": "Proactive talent pipelines keep high-quality candidates ready when you need them"
    },
    {
      "category": "Time Waste",
      "hook": "Insurance agencies waste 15+ hours per hire verifying licenses manually",
      "bottleneck": "Calling state registries one-by-one is inefficient and error-prone",
      "solution": "Automated NIPR verification eliminates manual license checks entirely"
    },
    {
      "category": "Candidate Experience",
      "hook": "Top candidates are off the market in 10 days—but your process takes 6 weeks",
      "bottleneck": "Slow communication and delayed interviews lose A-players to competitors",
      "solution": "Instant SMS engagement and streamlined workflows capture talent before they're gone"
    },
    {
      "category": "Operational Roadblocks",
      "hook": "Can't assess sales ability until the interview? You've already wasted 3 hours.",
      "bottleneck": "Traditional screening can't evaluate soft skills like sales confidence remotely",
      "solution": "Voice AI analyzes sales capability in 10 seconds, before you invest interview time"
    }
  ]
}
```

**Step 2: Verify JSON is valid**

```bash
python -m json.tool content/hirepriority/pain_points.json
```

Expected: Valid JSON output

**Step 3: Commit**

```bash
git add content/hirepriority/pain_points.json
git commit -m "feat: add HirePriority pain points rotation"
```

---

### Task 5: Create Content Recipe Template

**Files:**
- Create: `content/hirepriority/content_recipe.json`

**Step 1: Write content_recipe.json**

```json
{
  "structure": [
    {
      "section": "The Hook",
      "purpose": "Start with hard-hitting statistic or relatable frustration",
      "examples": [
        "Why are you still spending 20 hours a week on initial screenings?",
        "The true cost of a vacant seat isn't what you think",
        "73% of top candidates ghost companies with poor communication"
      ]
    },
    {
      "section": "The Bottleneck",
      "purpose": "Briefly explain why this issue persists (1-2 sentences)",
      "approach": "Point to systemic issues: outdated tech, generic platforms, manual processes"
    },
    {
      "section": "The Strategic Solution",
      "purpose": "Provide WHAT to do (high-level), NOT HOW to do it",
      "constraint": "Never provide step-by-step tutorials",
      "approach": "Focus on value of outcomes, not mechanics of process"
    },
    {
      "section": "The Pivot",
      "purpose": "Frame HirePriority as the partner that handles this complexity",
      "approach": "Subtle transition from general advice to specific solution"
    }
  ],
  "mandatory_ending": {
    "cta": "Stop the hiring leak today at https://hirepriority.scalepilotlabs.com/",
    "hashtags_count": "3-5 relevant hashtags per platform"
  }
}
```

**Step 2: Verify JSON is valid**

```bash
python -m json.tool content/hirepriority/content_recipe.json
```

Expected: Valid JSON output

**Step 3: Commit**

```bash
git add content/hirepriority/content_recipe.json
git commit -m "feat: add HirePriority content recipe template"
```

---

### Task 6: Create Platform Settings Configuration

**Files:**
- Create: `content/hirepriority/platform_settings.json`

**Step 1: Write platform_settings.json**

```json
{
  "linkedin": {
    "tone": "Professional, data-driven, authoritative",
    "length": { "min": 150, "max": 200 },
    "style_notes": [
      "Lead with compelling statistics",
      "Use industry terminology",
      "Formal CTA: 'Discover how HirePriority transforms recruitment at [URL]'",
      "Include line breaks for scannability",
      "Professional but not stuffy"
    ],
    "hashtags": [
      "#RecruitmentROI",
      "#TalentAcquisition",
      "#HiringStrategy",
      "#HirePriority",
      "#InsuranceRecruitment",
      "#HRTech",
      "#RecruitmentAutomation"
    ]
  },
  "x": {
    "tone": "Punchy, provocative, direct",
    "length": { "min": 100, "max": 150 },
    "style_notes": [
      "Sharp, attention-grabbing hooks",
      "One core pain point per post",
      "Conversational CTA: 'Stop the hiring leak: [URL]'",
      "Short paragraphs, high impact",
      "Slightly provocative to drive engagement"
    ],
    "hashtags": [
      "#Hiring",
      "#RecruitmentTech",
      "#HirePriority",
      "#TalentStrategy",
      "#HRAutomation"
    ]
  },
  "facebook": {
    "tone": "Engaging, relatable, conversational",
    "length": { "min": 120, "max": 180 },
    "style_notes": [
      "Relatable frustration scenarios",
      "Warmer, more approachable language",
      "Friendly CTA: 'Ready to hire smarter? Visit [URL]'",
      "Balance professional and personable",
      "Story-driven when possible"
    ],
    "hashtags": [
      "#SmartHiring",
      "#RecruitmentSolutions",
      "#HirePriority",
      "#TalentManagement",
      "#HRTech",
      "#HiringMadeEasy"
    ]
  }
}
```

**Step 2: Verify JSON is valid**

```bash
python -m json.tool content/hirepriority/platform_settings.json
```

Expected: Valid JSON output

**Step 3: Commit**

```bash
git add content/hirepriority/platform_settings.json
git commit -m "feat: add platform-specific settings for HirePriority content"
```

---

## Phase 2: Update AI Content Generation System

### Task 7: Update build_rss.py - Load HirePriority Configurations

**Files:**
- Modify: `build_rss.py` (add HirePriority config loading at top)

**Step 1: Read current build_rss.py paths section**

Check lines 25-33 to understand current path configuration structure.

**Step 2: Add HirePriority paths after line 33**

Add these lines after `TOPICS_FILE = "content/seeds_topics.txt"`:

```python
# HirePriority paths
HP_FEATURES_PATH = "content/hirepriority/features.json"
HP_PAIN_POINTS_PATH = "content/hirepriority/pain_points.json"
HP_RECIPE_PATH = "content/hirepriority/content_recipe.json"
HP_PLATFORM_SETTINGS_PATH = "content/hirepriority/platform_settings.json"
```

**Step 3: Test Python syntax**

```bash
python -m py_compile build_rss.py
```

Expected: No syntax errors

**Step 4: Commit**

```bash
git add build_rss.py
git commit -m "feat: add HirePriority configuration paths to build_rss.py"
```

---

### Task 8: Update build_rss.py - Add HirePriority Content Selection Function

**Files:**
- Modify: `build_rss.py` (add function after `choose_style` function around line 100)

**Step 1: Add function to select daily pain point**

Insert after the `choose_style` function (around line 110):

```python
def select_pain_point(pain_points_data):
    """Select a pain point based on daily rotation"""
    import hashlib
    from datetime import datetime

    pain_points = pain_points_data.get("pain_points", [])
    if not pain_points:
        return {
            "category": "General",
            "hook": "Hiring inefficiencies cost companies thousands per role",
            "bottleneck": "Manual processes slow down recruitment",
            "solution": "Automation streamlines candidate selection"
        }

    # Daily rotation based on date
    day_index = datetime.now().timetuple().tm_yday
    selected = pain_points[day_index % len(pain_points)]
    return selected
```

**Step 2: Test Python syntax**

```bash
python -m py_compile build_rss.py
```

Expected: No syntax errors

**Step 3: Commit**

```bash
git add build_rss.py
git commit -m "feat: add pain point selection function for daily rotation"
```

---

### Task 9: Update build_rss.py - Create HirePriority Prompt Generator

**Files:**
- Modify: `build_rss.py` (add function after `select_pain_point`)

**Step 1: Add HirePriority prompt generation function**

Insert after the `select_pain_point` function:

```python
def build_hirepriority_prompt(pain_point, platform, platform_settings, features):
    """Build AI prompt for HirePriority content following the content recipe"""

    platform_config = platform_settings.get(platform, {})
    tone = platform_config.get("tone", "Professional, authoritative")
    length = platform_config.get("length", {"min": 100, "max": 200})
    style_notes = platform_config.get("style_notes", [])
    hashtags = platform_config.get("hashtags", ["#HirePriority"])

    cta_url = features.get("cta_url", "https://hirepriority.scalepilotlabs.com/")

    prompt = f"""You are a Senior Talent Acquisition Strategist and Recruitment ROI Expert for HirePriority.

TODAY'S PAIN POINT:
- Category: {pain_point['category']}
- Hook: {pain_point['hook']}
- Bottleneck: {pain_point['bottleneck']}
- Solution: {pain_point['solution']}

PLATFORM: {platform}
TONE: {tone}
LENGTH: {length['min']}-{length['max']} words

PLATFORM STYLE NOTES:
{chr(10).join('- ' + note for note in style_notes)}

CONTENT RECIPE (MANDATORY STRUCTURE):
1. THE HOOK: Start with the pain point hook or similar hard-hitting stat/frustration
2. THE BOTTLENECK: Explain why this persists in 1-2 sentences (use the bottleneck context)
3. THE STRATEGIC SOLUTION: Provide WHAT to do (high-level), NOT HOW to do it (use solution context)
4. THE PIVOT: Position HirePriority as the partner that handles this complexity

CRITICAL CONSTRAINTS:
- NEVER provide step-by-step how-to guides
- Focus on value of outcomes, not mechanics of process
- Authoritative, professional, slightly provocative tone
- NO phrases like "Step 1", "Here's how", "Follow these steps"

CONTENT MIX:
- 70% General recruitment pain points (applicable to any industry)
- 30% Insurance-specific scenarios (mention features like NIPR verification, Voice AI when relevant)

HIREPRIORITY FEATURES (use subtly when relevant):
{chr(10).join('- ' + f['name'] + ': ' + f['benefit'] for f in features.get('features', []))}

MANDATORY ENDING FORMAT:
- CTA: "Stop the hiring leak today at {cta_url}"
- Hashtags: {' '.join(hashtags[:5])} (use 3-5 tags)

Create engaging {platform} content following this exact structure."""

    return prompt
```

**Step 2: Test Python syntax**

```bash
python -m py_compile build_rss.py
```

Expected: No syntax errors

**Step 3: Commit**

```bash
git add build_rss.py
git commit -m "feat: add HirePriority AI prompt generator function"
```

---

### Task 10: Update build_rss.py - Modify Main Generation Logic

**Files:**
- Modify: `build_rss.py` (update main content generation around line 200-300)

**Step 1: Find the main content generation function**

Search for the function that calls OpenAI API (likely around `def generate_content` or similar).

**Step 2: Replace topic-based generation with pain point-based generation**

Find where topics are loaded and selected (around `read_topics(TOPICS_FILE)`). Replace that section with:

```python
# Load HirePriority configurations
hp_features = load_json(HP_FEATURES_PATH, {})
hp_pain_points = load_json(HP_PAIN_POINTS_PATH, {"pain_points": []})
hp_platform_settings = load_json(HP_PLATFORM_SETTINGS_PATH, {})

# Select today's pain point
pain_point = select_pain_point(hp_pain_points)

# Determine platform (default to generic for now, will be platform-specific in feed scripts)
platform = "linkedin"  # This will be overridden by platform-specific scripts

# Build HirePriority prompt
user_prompt = build_hirepriority_prompt(pain_point, platform, hp_platform_settings, hp_features)
```

**Step 3: Comment out old ScalePilot topic selection**

Find and comment out the lines that use `read_topics` and `choose_style`:

```python
# OLD SCALEPILOT LOGIC (archived)
# topics = read_topics(TOPICS_FILE)
# topic = random.choice(topics) if topics else "AI automation for small business"
# style_key, style_desc = choose_style(weights)
```

**Step 4: Test Python syntax**

```bash
python -m py_compile build_rss.py
```

Expected: No syntax errors

**Step 5: Commit**

```bash
git add build_rss.py
git commit -m "feat: switch to HirePriority pain point-based content generation"
```

---

### Task 11: Update build_rss.py - Add Content Recipe Validation

**Files:**
- Modify: `build_rss.py` (add validation after OpenAI response, around line 250-300)

**Step 1: Find the quality gate validation section**

Search for the quality validation logic (around `quality_gate` or validation checks).

**Step 2: Add content recipe validation function before quality gates**

Insert this function before the quality gate validation:

```python
def validate_content_recipe(content):
    """Validate that content follows the Hook → Bottleneck → Solution → Pivot structure"""

    # Check for how-to indicators (banned)
    how_to_patterns = [
        r'\bstep\s+\d+\b',
        r'\bhere\'s\s+how\b',
        r'\bfollow\s+these\s+steps\b',
        r'\bfirst,\s+.*second,\s+.*third\b'
    ]

    content_lower = content.lower()
    for pattern in how_to_patterns:
        if re.search(pattern, content_lower, re.IGNORECASE):
            return False, f"Content contains how-to pattern: {pattern}"

    # Check for CTA presence
    if "hirepriority.scalepilotlabs.com" not in content.lower():
        return False, "Missing required CTA URL"

    # Check for hashtag presence
    if "#HirePriority" not in content:
        return False, "Missing required #HirePriority hashtag"

    return True, "Content recipe validated"
```

**Step 3: Integrate validation into quality gate flow**

Find the existing quality gate checks and add the recipe validation:

```python
# Add after existing quality checks
recipe_valid, recipe_msg = validate_content_recipe(generated_content)
if not recipe_valid:
    logger.warning(f"Content recipe validation failed: {recipe_msg}")
    continue  # Retry generation
```

**Step 4: Test Python syntax**

```bash
python -m py_compile build_rss.py
```

Expected: No syntax errors

**Step 5: Commit**

```bash
git add build_rss.py
git commit -m "feat: add content recipe validation to quality gates"
```

---

### Task 12: Update scripts/make_li_feed.py - LinkedIn Platform Customization

**Files:**
- Modify: `scripts/make_li_feed.py`

**Step 1: Read current make_li_feed.py**

Understand current structure and where platform-specific prompt modifications happen.

**Step 2: Find platform prompt customization section**

Look for where the script might add LinkedIn-specific instructions or modify the prompt.

**Step 3: Add LinkedIn-specific prompt override**

Add near the top of the script after imports:

```python
# LinkedIn platform configuration
PLATFORM = "linkedin"
PLATFORM_TONE = "Professional, data-driven, authoritative"
WORD_COUNT_MIN = 150
WORD_COUNT_MAX = 200
```

**Step 4: Ensure prompt includes LinkedIn settings**

If the script calls `build_rss.py` functions, ensure it passes `platform="linkedin"` parameter.

**Step 5: Test Python syntax**

```bash
python -m py_compile scripts/make_li_feed.py
```

Expected: No syntax errors

**Step 6: Commit**

```bash
git add scripts/make_li_feed.py
git commit -m "feat: customize LinkedIn feed for professional tone and length"
```

---

### Task 13: Update scripts/make_x_feed.py - X/Twitter Platform Customization

**Files:**
- Modify: `scripts/make_x_feed.py`

**Step 1: Read current make_x_feed.py**

Understand current structure.

**Step 2: Add X/Twitter-specific configuration**

Add near the top after imports:

```python
# X/Twitter platform configuration
PLATFORM = "x"
PLATFORM_TONE = "Punchy, provocative, direct"
WORD_COUNT_MIN = 100
WORD_COUNT_MAX = 150
```

**Step 3: Ensure prompt includes X settings**

If the script calls `build_rss.py` functions, ensure it passes `platform="x"` parameter.

**Step 4: Test Python syntax**

```bash
python -m py_compile scripts/make_x_feed.py
```

Expected: No syntax errors

**Step 5: Commit**

```bash
git add scripts/make_x_feed.py
git commit -m "feat: customize X/Twitter feed for punchy tone and shorter length"
```

---

### Task 14: Update scripts/make_fb_feed.py - Facebook Platform Customization

**Files:**
- Modify: `scripts/make_fb_feed.py`

**Step 1: Read current make_fb_feed.py**

Understand current structure.

**Step 2: Add Facebook-specific configuration**

Add near the top after imports:

```python
# Facebook platform configuration
PLATFORM = "facebook"
PLATFORM_TONE = "Engaging, relatable, conversational"
WORD_COUNT_MIN = 120
WORD_COUNT_MAX = 180
```

**Step 3: Ensure prompt includes Facebook settings**

If the script calls `build_rss.py` functions, ensure it passes `platform="facebook"` parameter.

**Step 4: Test Python syntax**

```bash
python -m py_compile scripts/make_fb_feed.py
```

Expected: No syntax errors

**Step 5: Commit**

```bash
git add scripts/make_fb_feed.py
git commit -m "feat: customize Facebook feed for engaging tone and medium length"
```

---

## Phase 3: Testing & Validation

### Task 15: Test LinkedIn Content Generation

**Files:**
- Test: Run `scripts/make_li_feed.py`

**Step 1: Set OPENAI_API_KEY environment variable**

```bash
# Verify API key is set (don't print it)
echo $OPENAI_API_KEY | grep -q "sk-" && echo "API key set" || echo "API key missing"
```

Expected: "API key set"

**Step 2: Run LinkedIn feed generation**

```bash
python scripts/make_li_feed.py
```

Expected: Content generated with professional tone, 150-200 words

**Step 3: Verify content structure**

Check generated RSS feed contains:
- Hook (hard-hitting stat or frustration)
- Bottleneck explanation
- Strategic solution (no how-to steps)
- CTA with HirePriority URL
- LinkedIn hashtags

**Step 4: Check word count**

Count words in generated content, should be 150-200 words.

**Step 5: Document test results**

If successful, note: "LinkedIn content generation working as expected"
If failed, note specific errors for debugging.

---

### Task 16: Test X/Twitter Content Generation

**Files:**
- Test: Run `scripts/make_x_feed.py`

**Step 1: Run X/Twitter feed generation**

```bash
python scripts/make_x_feed.py
```

Expected: Content generated with punchy tone, 100-150 words

**Step 2: Verify content structure**

Check generated content:
- Sharp hook
- Brief bottleneck
- Quick solution
- CTA with URL
- X-appropriate hashtags

**Step 3: Check word count**

Should be 100-150 words.

**Step 4: Document test results**

Note success or specific errors.

---

### Task 17: Test Facebook Content Generation

**Files:**
- Test: Run `scripts/make_fb_feed.py`

**Step 1: Run Facebook feed generation**

```bash
python scripts/make_fb_feed.py
```

Expected: Content generated with engaging tone, 120-180 words

**Step 2: Verify content structure**

Check generated content:
- Relatable hook
- Conversational bottleneck
- Friendly solution
- Warm CTA
- Facebook hashtags

**Step 3: Check word count**

Should be 120-180 words.

**Step 4: Document test results**

Note success or specific errors.

---

### Task 18: Verify Quality Gates

**Files:**
- Test: Quality gate validation

**Step 1: Verify how-to detection works**

Manually test the `validate_content_recipe` function by creating test content with "Step 1" and verify it's rejected.

**Step 2: Verify CTA enforcement**

Test content without HirePriority URL is rejected.

**Step 3: Verify hashtag requirement**

Test content without #HirePriority is rejected.

**Step 4: Document validation results**

Confirm all quality gates are functioning.

---

### Task 19: Verify RSS Feed Output Format

**Files:**
- Test: Check generated RSS feeds

**Step 1: Verify RSS files exist**

```bash
ls -la feeds/
```

Expected: `rss_li_live.xml`, `rss_x_live.xml`, `rss_fb_live.xml` present

**Step 2: Validate XML syntax**

```bash
python -m xml.etree.ElementTree feeds/rss_li_live.xml
```

Expected: Valid XML

**Step 3: Check feed contents**

Open each RSS file and verify:
- Channel title updated (if applicable)
- Item contains HirePriority content
- CTA URLs present
- Hashtags included

**Step 4: Document feed validation**

Confirm feeds are properly formatted.

---

## Phase 4: Final Integration & Deployment

### Task 20: Update README with HirePriority Information

**Files:**
- Modify: `README.md`

**Step 1: Read current README**

Understand structure around line 1-50 (project description).

**Step 2: Update project description**

Replace ScalePilot-specific description with HirePriority focus:

Change from:
```markdown
AI-powered social media content generation for ScalePilot - AI tools and solutions for SMBs.
```

To:
```markdown
AI-powered social media content generation for HirePriority - Recruitment solutions for insurance agencies.

This system uses OpenAI to automatically generate original, engaging content about recruitment ROI, hiring bottlenecks, and talent acquisition strategies. Content is delivered via RSS feeds that you can connect to your social media management tools.
```

**Step 3: Update customization section**

Update the "Adjusting Content Topics" section around line 74-84:

Replace with:
```markdown
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
```

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: update README for HirePriority migration"
```

---

### Task 21: Create Migration Documentation

**Files:**
- Create: `MIGRATION_TO_HIREPRIORITY.md`

**Step 1: Write migration documentation**

```markdown
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
```

**Step 2: Commit**

```bash
git add MIGRATION_TO_HIREPRIORITY.md
git commit -m "docs: add HirePriority migration documentation"
```

---

### Task 22: Run Full Build and Verify

**Files:**
- Test: Complete build process

**Step 1: Run main build script**

```bash
python build_rss.py
```

Expected: Successful generation with HirePriority content

**Step 2: Check all RSS feeds generated**

```bash
ls -la feeds/
```

Expected: All platform feeds present and updated

**Step 3: Verify content in feeds matches requirements**

Open each feed and spot-check:
- Content follows recipe structure
- Platform-specific tone differences visible
- CTAs present with correct URL
- Hashtags appropriate for each platform

**Step 4: Document build verification**

Confirm: "Full build successful, all feeds generated correctly"

---

### Task 23: Final Commit and Summary

**Files:**
- All modified files

**Step 1: Check git status**

```bash
git status
```

Verify all changes are committed.

**Step 2: Create summary commit (if any remaining changes)**

```bash
git add -A
git commit -m "feat: complete HirePriority content migration

- Archive ScalePilot configuration for future reactivation
- Implement HirePriority pain point-based content system
- Add platform-specific optimization (LinkedIn/X/Facebook)
- Enforce content recipe structure (Hook → Bottleneck → Solution → Pivot)
- Add quality gates for CTA and hashtag validation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**Step 3: Review commit log**

```bash
git log --oneline -10
```

Expected: Clean commit history showing migration steps

**Step 4: Document completion**

Note: "Migration complete - HirePriority content system active"

---

## Success Criteria

- [ ] ScalePilot files archived in `content/archive/scalepilot/`
- [ ] HirePriority configuration files created and valid JSON
- [ ] `build_rss.py` updated to use HirePriority pain points
- [ ] Platform-specific scripts customized (LinkedIn/X/Facebook)
- [ ] Content recipe validation working (no how-to's, CTA required, hashtags required)
- [ ] All three platform feeds generate successfully
- [ ] Content follows Hook → Bottleneck → Solution → Pivot structure
- [ ] Platform tone differences evident (professional/punchy/engaging)
- [ ] Documentation updated (README, MIGRATION guide)
- [ ] All changes committed with clear messages

---

## Rollback Plan

If issues arise:

1. Restore ScalePilot files from archive
2. Revert `build_rss.py` and platform scripts using git
3. Archive HirePriority configuration
4. Resume ScalePilot content generation

---

**Plan Status:** Ready for execution
**Estimated Time:** 2-3 hours for full implementation
**Prerequisites:** OpenAI API key configured, Python 3.x installed
