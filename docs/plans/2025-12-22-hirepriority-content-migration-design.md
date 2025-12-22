# HirePriority Content Migration Design

**Date:** 2025-12-22
**Status:** Approved
**Goal:** Pause ScalePilot AI automation content and switch to HirePriority recruitment content with platform-specific optimization

---

## Overview

Migrate the social media automation system from ScalePilot (AI automation for SMBs) to HirePriority (recruitment solutions for insurance agencies), while preserving the ability to resume ScalePilot content in the future.

**Content Strategy Shift:**
- **From:** AI automation, productivity tools, SMB growth
- **To:** Recruitment ROI, hiring bottlenecks, talent acquisition strategy
- **Focus:** General recruitment content (70%) with insurance-specific examples (30%)

---

## Section 1: System Architecture & Preservation

### Preserve ScalePilot System

Create archive structure to pause (not delete) current content:

```
content/archive/scalepilot/
├── seeds_topics.txt (current 50 AI automation topics)
├── scalepilot_features.json (product features)
├── competitors.json (competitive positioning)
└── original_prompts.txt (backup of AI generation prompts)
```

### New HirePriority Structure

```
content/hirepriority/
├── features.json (HirePriority product features)
├── pain_points.json (recruitment bottlenecks rotation)
├── content_recipe.json (Hook → Bottleneck → Solution → Pivot template)
└── platform_settings.json (LinkedIn/X/Facebook configurations)
```

### Files to Modify

1. **`build_rss.py`** - Update AI prompt system to use HirePriority content recipe
2. **`scripts/make_li_feed.py`** - LinkedIn formatting (professional, 150-200 words)
3. **`scripts/make_x_feed.py`** - X/Twitter formatting (punchy, 100-150 words)
4. **`scripts/make_fb_feed.py`** - Facebook formatting (engaging, 120-180 words)

---

## Section 2: Content Strategy Configuration

### HirePriority Features (`content/hirepriority/features.json`)

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

### Pain Points Rotation (`content/hirepriority/pain_points.json`)

Daily rotation through recruitment bottlenecks across 4 categories:

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
    }
  ]
}
```

### Content Recipe Template (`content/hirepriority/content_recipe.json`)

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

---

## Section 3: Platform-Specific Content Generation

### Platform Settings (`content/hirepriority/platform_settings.json`)

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

### Platform Output Examples

**Same pain point, three different platforms:**

#### LinkedIn (Professional, Data-Driven)
```
The True Cost of a Vacant Seat

According to recent industry data, companies spend an average of 23 hours per hire on manual screening—time that rarely translates to better candidate quality.

The Bottleneck: Over-reliance on generic job boards leads to a flood of unqualified applicants, paralyzing HR departments and extending vacancy times by weeks.

The Solution: Shifting to a niche-focused recruitment model ensures you only see high-intent, pre-qualified talent, cutting your time-to-fill in half while improving candidate quality metrics.

Discover how HirePriority transforms recruitment at https://hirepriority.scalepilotlabs.com/

#RecruitmentROI #TalentAcquisition #HiringStrategy #HirePriority
```

#### X/Twitter (Punchy, Provocative)
```
Still burning 20+ hours per hire on manual screening?

Your competitors automated that last year.

The problem: Generic job boards = noise.
The solution: AI-powered pre-qualification = signal.

Stop the hiring leak: https://hirepriority.scalepilotlabs.com/

#Hiring #RecruitmentTech #HirePriority
```

#### Facebook (Engaging, Relatable)
```
Imagine cutting your screening time from 20 hours to 2—without sacrificing quality.

Sounds impossible? It's not.

Most hiring managers waste entire weeks reviewing resumes from unqualified candidates because traditional job boards prioritize volume over fit.

The shift? Smart companies use AI-powered pre-qualification to surface only the candidates worth your time.

Ready to hire smarter? Visit https://hirepriority.scalepilotlabs.com/

#SmartHiring #RecruitmentSolutions #HirePriority #TalentManagement
```

---

## Section 4: AI Prompt Engineering & Quality Gates

### System Prompt Template

Injected into `build_rss.py` AI generation:

```
You are a Senior Talent Acquisition Strategist and Recruitment ROI Expert for HirePriority.

TODAY'S PAIN POINT: {selected_pain_point}
PLATFORM: {linkedin|x|facebook}
TONE: {platform_tone_guidance}
LENGTH: {platform_length_constraints}

CONTENT RECIPE (MANDATORY STRUCTURE):
1. THE HOOK: Start with {pain_point.hook} or similar hard-hitting stat/frustration
2. THE BOTTLENECK: Explain why this persists in 1-2 sentences
3. THE STRATEGIC SOLUTION: Provide WHAT to do (high-level), NOT HOW to do it
4. THE PIVOT: Position HirePriority as the partner that handles this complexity

CRITICAL CONSTRAINTS:
- NEVER provide step-by-step how-to guides
- Focus on value of outcomes, not mechanics of process
- Authoritative, professional, slightly provocative tone
- {platform_specific_style_notes}

CONTENT MIX:
- 70% General recruitment pain points (applicable to any industry)
- 30% Insurance-specific scenarios (use HirePriority features like NIPR verification, Voice AI)

MANDATORY ENDING FORMAT:
- CTA: "Stop the hiring leak today at https://hirepriority.scalepilotlabs.com/"
- Hashtags: {platform_hashtags} (3-5 tags)

EXAMPLES OF GOOD HOOKS:
- "The average cost of a bad hire is 30% of their first-year salary"
- "Why are you still spending 20 hours a week on initial screenings?"
- "73% of candidates ghost companies with poor communication"
- "Your average time-to-fill is 42 days. Your competitors are at 14."

BANNED APPROACHES:
- Step-by-step tutorials ("Step 1: Do this, Step 2: Do that")
- Overly technical implementation details
- Generic hiring advice without strategic framing
```

### Quality Gates

Add to existing validation pipeline in `build_rss.py`:

1. **Content Recipe Validation**
   - Verify all 4 sections present (Hook → Bottleneck → Solution → Pivot)
   - Check for clear section transitions

2. **No How-To Detection**
   - Flag posts containing: "step 1", "step 2", "here's how", "follow these steps"
   - Reject posts with numbered instruction lists

3. **CTA Enforcement**
   - Ensure every post ends with exact CTA format
   - Verify URL is correct: `https://hirepriority.scalepilotlabs.com/`

4. **Length Compliance**
   - LinkedIn: 150-200 words
   - X: 100-150 words
   - Facebook: 120-180 words

5. **Tone Consistency**
   - Check for overly casual language on LinkedIn ("gonna", "wanna", excessive emojis)
   - Check for overly formal language on X (avoid corporate jargon overload)
   - Ensure Facebook maintains warmth without unprofessionalism

6. **Hashtag Validation**
   - Verify 3-5 hashtags present
   - Ensure `#HirePriority` is always included
   - Platform-specific hashtag sets enforced

---

## Implementation Checklist

### Phase 1: Archive & Setup
- [ ] Create `content/archive/scalepilot/` directory
- [ ] Move current ScalePilot files to archive
- [ ] Create `content/hirepriority/` directory structure
- [ ] Write `features.json` with HirePriority product details
- [ ] Write `pain_points.json` with recruitment bottlenecks
- [ ] Write `content_recipe.json` with template structure
- [ ] Write `platform_settings.json` with platform configurations

### Phase 2: Code Modifications
- [ ] Update `build_rss.py` - Replace AI prompt system
- [ ] Update `scripts/make_li_feed.py` - LinkedIn formatting
- [ ] Update `scripts/make_x_feed.py` - X/Twitter formatting
- [ ] Update `scripts/make_fb_feed.py` - Facebook formatting
- [ ] Add new quality gates for content recipe validation
- [ ] Add how-to detection and rejection logic
- [ ] Update CTA enforcement to use HirePriority URL

### Phase 3: Testing & Validation
- [ ] Test content generation for LinkedIn
- [ ] Test content generation for X/Twitter
- [ ] Test content generation for Facebook
- [ ] Verify length compliance across platforms
- [ ] Validate tone differences are appropriate
- [ ] Confirm all quality gates function correctly
- [ ] Check RSS feed output format

### Phase 4: Deployment
- [ ] Update GitHub Actions workflows (if needed)
- [ ] Run initial feed generation
- [ ] Verify RSS feeds are accessible
- [ ] Monitor first week of automated posts
- [ ] Adjust pain point rotation based on performance

---

## Success Criteria

1. **ScalePilot system is fully preserved** and can be resumed by reversing file moves
2. **All posts follow the content recipe** (Hook → Bottleneck → Solution → Pivot)
3. **Platform-specific tone is enforced** (LinkedIn professional, X punchy, Facebook engaging)
4. **No how-to guides generated** - all content focuses on value, not mechanics
5. **Every post includes correct CTA** with HirePriority URL
6. **Content mix achieved**: 70% general recruitment, 30% insurance-specific
7. **Daily content rotation** through pain point categories without repetition

---

## Rollback Plan

If HirePriority content needs to be paused and ScalePilot resumed:

1. Move files from `content/archive/scalepilot/` back to original locations
2. Revert `build_rss.py` prompt changes (keep git history clean)
3. Revert platform-specific script modifications
4. Archive `content/hirepriority/` directory
5. Resume ScalePilot content generation

---

**Design Status:** ✅ Approved
**Ready for Implementation:** Yes
**Estimated Effort:** 3-4 hours for full migration and testing
