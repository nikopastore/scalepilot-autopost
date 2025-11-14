#!/usr/bin/env python3
"""
Content Calibration Tool

Interactive tool to adjust content strategy and vibes.
Use this to fine-tune what gets posted over time.
"""

import json
from pathlib import Path
from content_director import ContentDirector


def show_menu():
    print("\n" + "="*60)
    print("CONTENT CALIBRATION TOOL")
    print("="*60)
    print("\nWhat would you like to adjust?\n")
    print("TONE & VIBE:")
    print("  1. Make content more professional / less casual")
    print("  2. Make content more friendly / approachable")
    print("  3. Make content more authoritative / expert")
    print("  4. Add more playfulness / humor")
    print("")
    print("PROMOTIONAL INTENSITY:")
    print("  5. Increase product mentions (sell more)")
    print("  6. Decrease product mentions (pure value)")
    print("  7. Balance promotional vs educational")
    print("")
    print("CONTENT FOCUS:")
    print("  8. Focus more on solopreneurs")
    print("  9. Focus more on small teams (2-10 people)")
    print(" 10. Focus more on marketing managers")
    print("")
    print("THEMES & SCHEDULE:")
    print(" 11. Change weekly theme rotation")
    print(" 12. Add feature announcement campaign")
    print("")
    print("REVIEW:")
    print(" 13. Show current settings")
    print(" 14. Export strategy for AI")
    print(" 15. Reset to defaults")
    print("")
    print(" 0. Exit")
    print("\n" + "="*60)


def adjust_professional(director):
    print("\nHow professional should the content be?")
    print("1 = Very casual, like talking to a friend")
    print("5 = Balanced, professional but approachable")
    print("10 = Very formal, corporate tone")
    choice = input("\nEnter 1-10: ").strip()
    try:
        level = int(choice) / 10.0
        director.adjust_vibe("tone", {
            "professional": level,
            "casual": 1.0 - level
        })
        print(f"\n✓ Content will now be {'more professional' if level > 0.5 else 'more casual'}")
    except:
        print("Invalid input")


def adjust_friendliness(director):
    print("\nHow friendly should the content be?")
    print("1 = Distant and formal")
    print("5 = Balanced")
    print("10 = Very warm and friendly")
    choice = input("\nEnter 1-10: ").strip()
    try:
        level = int(choice) / 10.0
        director.adjust_vibe("tone", {"friendly": level})
        print(f"\n✓ Content friendliness set to {int(level*100)}%")
    except:
        print("Invalid input")


def adjust_authority(director):
    print("\nHow authoritative/expert should the tone be?")
    print("1 = Humble, questions more than answers")
    print("5 = Balanced")
    print("10 = Very confident expert voice")
    choice = input("\nEnter 1-10: ").strip()
    try:
        level = int(choice) / 10.0
        director.adjust_vibe("tone", {"authoritative": level})
        print(f"\n✓ Content authority level set to {int(level*100)}%")
    except:
        print("Invalid input")


def adjust_playfulness(director):
    print("\nHow playful/humorous should content be?")
    print("1 = Serious, no humor")
    print("5 = Occasional light humor")
    print("10 = Fun and playful throughout")
    choice = input("\nEnter 1-10: ").strip()
    try:
        level = int(choice) / 10.0
        director.adjust_vibe("tone", {"playful": level})
        print(f"\n✓ Content playfulness set to {int(level*100)}%")
    except:
        print("Invalid input")


def increase_promotional(director):
    print("\nIncreasing promotional intensity...")
    print("This will make content mention ScalePilot more frequently.")
    director.adjust_vibe("promotional_intensity", {
        "direct_sales": 0.2,   # 20% hard sell
        "soft_sell": 0.5,      # 50% subtle mention
        "educational": 0.3     # 30% pure value
    })
    print("\n✓ Content will now be MORE promotional")
    print("  - More frequent product mentions")
    print("  - Clearer calls-to-action")
    print("  - Stronger benefit statements")


def decrease_promotional(director):
    print("\nDecreasing promotional intensity...")
    print("This will focus on pure value with minimal product mentions.")
    director.adjust_vibe("promotional_intensity", {
        "direct_sales": 0.05,  # 5% hard sell
        "soft_sell": 0.15,     # 15% subtle mention
        "educational": 0.8     # 80% pure value
    })
    print("\n✓ Content will now be LESS promotional")
    print("  - Mostly educational value")
    print("  - Rare product mentions")
    print("  - Focus on helping, not selling")


def balance_promotional(director):
    print("\nBalancing promotional and educational content...")
    director.adjust_vibe("promotional_intensity", {
        "direct_sales": 0.1,   # 10% hard sell
        "soft_sell": 0.3,      # 30% subtle mention
        "educational": 0.6     # 60% pure value
    })
    print("\n✓ Content balanced between value and promotion")


def focus_solopreneurs(director):
    director.adjust_vibe("audience_focus", {
        "solopreneurs": 0.6,
        "small_teams": 0.2,
        "marketing_managers": 0.1,
        "operations": 0.1
    })
    print("\n✓ Content will now focus on solopreneurs")
    print("  - One-person business challenges")
    print("  - Time management and automation")
    print("  - Budget-conscious solutions")


def focus_small_teams(director):
    director.adjust_vibe("audience_focus", {
        "solopreneurs": 0.2,
        "small_teams": 0.5,
        "marketing_managers": 0.2,
        "operations": 0.1
    })
    print("\n✓ Content will now focus on small teams (2-10 people)")
    print("  - Team collaboration")
    print("  - Delegation and scaling")
    print("  - Process optimization")


def focus_marketing(director):
    director.adjust_vibe("audience_focus", {
        "solopreneurs": 0.2,
        "small_teams": 0.3,
        "marketing_managers": 0.4,
        "operations": 0.1
    })
    print("\n✓ Content will now focus on marketing managers")
    print("  - Campaign management")
    print("  - Content strategy")
    print("  - Lead generation")


def show_current_settings(director):
    strategy = director.get_current_strategy()
    print("\n" + "="*60)
    print("CURRENT CONTENT STRATEGY")
    print("="*60)

    print("\nTONE SETTINGS:")
    for key, value in strategy["vibes"]["tone"].items():
        bars = "█" * int(value * 20)
        print(f"  {key:20s} {bars} {int(value*100)}%")

    print("\nPROMOTIONAL INTENSITY:")
    for key, value in strategy["vibes"]["promotional_intensity"].items():
        bars = "█" * int(value * 20)
        print(f"  {key:20s} {bars} {int(value*100)}%")

    print("\nAUDIENCE FOCUS:")
    for key, value in strategy["vibes"]["audience_focus"].items():
        bars = "█" * int(value * 20)
        print(f"  {key:20s} {bars} {int(value*100)}%")

    print("\n" + "="*60)


def main():
    director = ContentDirector()

    while True:
        show_menu()
        choice = input("\nEnter your choice (0-15): ").strip()

        if choice == "0":
            print("\nSaving changes...")
            print("✓ Content strategy updated!")
            break
        elif choice == "1":
            adjust_professional(director)
        elif choice == "2":
            adjust_friendliness(director)
        elif choice == "3":
            adjust_authority(director)
        elif choice == "4":
            adjust_playfulness(director)
        elif choice == "5":
            increase_promotional(director)
        elif choice == "6":
            decrease_promotional(director)
        elif choice == "7":
            balance_promotional(director)
        elif choice == "8":
            focus_solopreneurs(director)
        elif choice == "9":
            focus_small_teams(director)
        elif choice == "10":
            focus_marketing(director)
        elif choice == "13":
            show_current_settings(director)
        elif choice == "14":
            strategy = director.get_strategy_prompt()
            print("\n" + json.dumps(strategy, indent=2))
        else:
            print("\nComing soon!")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
