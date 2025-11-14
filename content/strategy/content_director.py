#!/usr/bin/env python3
"""
ScalePilot Content Strategy Director

An intelligent agent that helps you:
1. Control what content gets posted
2. Tune content vibes and tone over time
3. Push product features professionally
4. Track competitors and market trends
5. Calibrate content strategy based on feedback

This is your AI marketing strategist - talk to it, refine strategy, adjust tactics.
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

STRATEGY_DIR = Path(__file__).parent
FEATURES_FILE = STRATEGY_DIR / "scalepilot_features.json"
COMPETITORS_FILE = STRATEGY_DIR / "competitors.json"
CONTENT_CALENDAR_FILE = STRATEGY_DIR / "content_calendar.json"
VIBE_SETTINGS_FILE = STRATEGY_DIR / "vibe_settings.json"


class ContentDirector:
    """
    Your AI Content Strategy Director.

    Responsibilities:
    - Understand ScalePilot's features, benefits, and positioning
    - Track competitors and market landscape
    - Control content themes and messaging
    - Adjust tone, vibe, and promotional intensity
    - Ensure posts align with business goals
    """

    def __init__(self):
        self.features = self._load_json(FEATURES_FILE, {})
        self.competitors = self._load_json(COMPETITORS_FILE, {})
        self.calendar = self._load_json(CONTENT_CALENDAR_FILE, self._default_calendar())
        self.vibes = self._load_json(VIBE_SETTINGS_FILE, self._default_vibes())

    def _load_json(self, path, default):
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default

    def _save_json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _default_calendar(self):
        """Default content calendar with balanced themes"""
        return {
            "theme_rotation": [
                {"day": "Monday", "theme": "productivity", "focus": "AI tools that save time"},
                {"day": "Tuesday", "theme": "education", "focus": "How-to guides and tips"},
                {"day": "Wednesday", "theme": "product", "focus": "ScalePilot features and benefits"},
                {"day": "Thursday", "theme": "industry", "focus": "SMB challenges and solutions"},
                {"day": "Friday", "theme": "inspiration", "focus": "Success stories and wins"},
                {"day": "Saturday", "theme": "free_choice", "focus": "Mix of trending topics"},
                {"day": "Sunday", "theme": "free_choice", "focus": "Community and engagement"}
            ],
            "promotional_frequency": {
                "direct_product_pitch": "1_per_week",  # Wednesday
                "soft_product_mention": "2_per_week",  # Subtle feature mentions
                "pure_value": "4_per_week"  # No product mention at all
            },
            "feature_spotlight_schedule": [
                {"week": 1, "feature": "AI Content Automation", "angle": "time_savings"},
                {"week": 2, "feature": "Quality Gates", "angle": "brand_consistency"},
                {"week": 3, "feature": "Analytics", "angle": "data_driven"},
                {"week": 4, "feature": "Platform Integration", "angle": "ease_of_use"}
            ]
        }

    def _default_vibes(self):
        """Default vibe settings for content tone"""
        return {
            "tone": {
                "professional": 0.6,  # 60% professional, formal
                "friendly": 0.8,      # 80% friendly, approachable
                "casual": 0.3,        # 30% casual, informal
                "authoritative": 0.7, # 70% expert, confident
                "playful": 0.2        # 20% fun, light-hearted
            },
            "promotional_intensity": {
                "direct_sales": 0.1,   # 10% hard sell (very rare)
                "soft_sell": 0.3,      # 30% subtle product mention
                "educational": 0.6     # 60% pure value, no pitch
            },
            "content_angles": {
                "problem_solution": 0.4,    # 40% identify pain + solution
                "how_to_guide": 0.3,        # 30% step-by-step instructions
                "industry_insight": 0.15,   # 15% trends and analysis
                "inspiration": 0.15         # 15% motivation and success stories
            },
            "audience_focus": {
                "solopreneurs": 0.4,
                "small_teams": 0.35,
                "marketing_managers": 0.15,
                "operations": 0.1
            }
        }

    def get_strategy_prompt(self):
        """
        Generate a strategic prompt that guides AI content generation.
        This gets injected into the content generation system.
        """
        today = datetime.now().strftime("%A")

        # Get today's theme
        theme_info = next((t for t in self.calendar["theme_rotation"] if t["day"] == today), None)
        if not theme_info:
            theme_info = {"theme": "free_choice", "focus": "General AI and business automation"}

        # Determine promotional approach
        week_num = datetime.now().isocalendar()[1] % 4 or 4
        feature_spotlight = self.calendar["feature_spotlight_schedule"][week_num - 1]

        # Build strategic context
        strategy = {
            "today_theme": theme_info["theme"],
            "focus_area": theme_info["focus"],
            "feature_to_highlight": feature_spotlight["feature"] if theme_info["theme"] == "product" else None,
            "tone_guidance": self._get_tone_guidance(),
            "promotional_approach": self._get_promotional_approach(theme_info["theme"]),
            "target_audience": self._get_primary_audience(),
            "competitor_context": self._get_competitor_context(),
            "key_differentiators": self.features.get("differentiators", [])
        }

        return strategy

    def _get_tone_guidance(self):
        """Get tone guidance based on vibe settings"""
        tone = self.vibes["tone"]
        guidance = []

        if tone["professional"] > 0.5:
            guidance.append("Professional and credible")
        if tone["friendly"] > 0.6:
            guidance.append("Friendly and approachable")
        if tone["authoritative"] > 0.6:
            guidance.append("Confident and expert")
        if tone["playful"] > 0.4:
            guidance.append("Occasional light humor")

        return ", ".join(guidance) or "Balanced and professional"

    def _get_promotional_approach(self, theme):
        """Determine how promotional today's content should be"""
        if theme == "product":
            return "Direct product feature highlight with benefits and use cases"
        elif theme in ["productivity", "education"]:
            return "Soft mention of how ScalePilot solves this problem (if relevant)"
        else:
            return "Pure value - no product mention unless extremely natural fit"

    def _get_primary_audience(self):
        """Get primary audience focus for today"""
        audience = self.vibes["audience_focus"]
        primary = max(audience.items(), key=lambda x: x[1])
        return primary[0].replace("_", " ").title()

    def _get_competitor_context(self):
        """Get relevant competitor positioning"""
        competitors = self.competitors.get("competitor_landscape", {})
        direct = competitors.get("direct_competitors", [])
        if direct:
            top_competitor = direct[0]  # Buffer is #1
            return f"Position against {top_competitor['name']}: {top_competitor['our_advantage']}"
        return "Emphasize unique value proposition"

    def adjust_vibe(self, dimension, value):
        """
        Adjust content vibe settings.

        dimension: 'tone', 'promotional_intensity', 'content_angles', 'audience_focus'
        value: dict of adjustments
        """
        if dimension in self.vibes:
            self.vibes[dimension].update(value)
            self._save_json(VIBE_SETTINGS_FILE, self.vibes)
            return f"Updated {dimension}: {value}"
        return f"Unknown dimension: {dimension}"

    def set_theme_schedule(self, schedule):
        """Update the weekly theme rotation"""
        self.calendar["theme_rotation"] = schedule
        self._save_json(CONTENT_CALENDAR_FILE, self.calendar)
        return "Theme schedule updated"

    def add_feature_announcement(self, feature_name, launch_date, announcement_plan):
        """
        Schedule a feature announcement campaign.

        feature_name: Name of the feature
        launch_date: When it launches (YYYY-MM-DD)
        announcement_plan: Dict with teaser, launch, and follow-up messaging
        """
        if "feature_announcements" not in self.calendar:
            self.calendar["feature_announcements"] = []

        self.calendar["feature_announcements"].append({
            "feature": feature_name,
            "launch_date": launch_date,
            "plan": announcement_plan,
            "created": datetime.now().isoformat()
        })

        self._save_json(CONTENT_CALENDAR_FILE, self.calendar)
        return f"Scheduled announcement for {feature_name} on {launch_date}"

    def get_current_strategy(self):
        """Get current content strategy overview"""
        return {
            "vibes": self.vibes,
            "calendar": self.calendar,
            "features": self.features,
            "positioning": self.competitors.get("market_positioning", {})
        }

    def interactive_session(self):
        """
        Start an interactive session to discuss and adjust strategy.
        This is where you chat with the Content Director.
        """
        print("\n" + "="*60)
        print("SCALEPILOT CONTENT STRATEGY DIRECTOR")
        print("="*60)
        print("\nHi! I'm your AI Content Strategy Director.")
        print("I help you control what gets posted, tune the vibes,")
        print("and ensure content aligns with your business goals.\n")

        print("Current Strategy Overview:")
        print("-" * 40)

        # Show current strategy
        strategy = self.get_strategy_prompt()
        print(f"Today's Theme: {strategy['today_theme']}")
        print(f"Focus: {strategy['focus_area']}")
        print(f"Tone: {strategy['tone_guidance']}")
        print(f"Promotional Approach: {strategy['promotional_approach']}")
        print(f"Target Audience: {strategy['target_audience']}")

        print("\n" + "-" * 40)
        print("\nWhat would you like to do?")
        print("1. Adjust content vibe/tone")
        print("2. Change theme schedule")
        print("3. Add feature announcement")
        print("4. Review competitor positioning")
        print("5. Export strategy for AI generation")
        print("6. Exit")

        # This would be interactive in practice
        # For now, we'll create the framework
        return strategy


def main():
    """Main entry point for Content Director"""
    director = ContentDirector()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "strategy":
            # Output today's strategy for injection into content generation
            strategy = director.get_strategy_prompt()
            print(json.dumps(strategy, indent=2))

        elif command == "interactive":
            director.interactive_session()

        elif command == "export":
            # Export full strategy to file
            strategy = director.get_current_strategy()
            output_path = Path("content/strategy/current_strategy.json")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(strategy, f, indent=2)
            print(f"Strategy exported to {output_path}")

    else:
        print("ScalePilot Content Strategy Director")
        print("\nUsage:")
        print("  python content_director.py strategy    # Get today's content strategy")
        print("  python content_director.py interactive # Interactive strategy session")
        print("  python content_director.py export      # Export full strategy")


if __name__ == "__main__":
    main()
