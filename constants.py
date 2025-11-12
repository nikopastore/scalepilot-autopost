"""
Configuration and constants for ScalePilot Social Media Automation
"""

# RSS Feeds - AI, SMB, Productivity, Recruiting, Training
RSS_FEEDS = [
    # AI & Automation
    "https://www.artificialintelligence-news.com/feed/",
    "https://blogs.nvidia.com/feed/",
    "https://openai.com/blog/rss/",
    "https://www.deeplearning.ai/feed/",
    "https://machinelearningmastery.com/feed/",

    # Small Business & Entrepreneurship
    "https://www.entrepreneur.com/latest.rss",
    "https://feeds.feedburner.com/SmallBusinessTrends",
    "https://www.inc.com/rss/",
    "https://www.forbes.com/small-business/feed/",

    # Productivity & Business Tools
    "https://zapier.com/blog/feed/",
    "https://www.productivityist.com/feed/",
    "https://blog.getclockwise.com/rss/",
    "https://blog.asana.com/feed/",
    "https://todoist.com/inspiration/feed/",

    # Marketing Automation
    "https://blog.hubspot.com/marketing/rss.xml",
    "https://www.mailchimp.com/feed/",
    "https://blog.hootsuite.com/feed/",
    "https://buffer.com/resources/feed/",

    # HR, Recruiting & Training
    "https://www.shrm.org/resourcesandtools/rss/pages/default.aspx",
    "https://www.recruiter.com/feed/",
    "https://www.hrbartender.com/feed/",
    "https://www.td.org/rss",
    "https://elearningindustry.com/feed",
    "https://www.talentlms.com/blog/feed/",

    # Business Growth & Strategy
    "https://hbr.org/feed",
    "https://www.fastcompany.com/latest/rss",
    "https://www.mckinsey.com/featured-insights/rss",
]

# Content Keywords - Topics to prioritize
PRIORITY_KEYWORDS = [
    # AI & Automation
    "artificial intelligence", "AI automation", "machine learning", "chatgpt", "generative ai",
    "automation", "workflow automation", "ai tools", "ai assistant", "llm", "gpt",

    # Small Business
    "small business", "smb", "small and medium business", "startup", "entrepreneur",
    "solopreneur", "business owner", "local business",

    # Productivity
    "productivity", "efficiency", "time management", "collaboration", "remote work",
    "hybrid work", "project management", "task management",

    # Marketing
    "marketing automation", "digital marketing", "social media marketing", "content marketing",
    "email marketing", "crm", "customer engagement",

    # Recruiting & HR
    "recruiting", "recruitment", "talent acquisition", "hiring", "employee", "hr tech",
    "applicant tracking", "onboarding", "retention", "company culture",

    # Training & Development
    "training", "learning", "employee development", "skill development", "upskilling",
    "e-learning", "online training", "professional development", "coaching",

    # Business Growth
    "business growth", "scale", "revenue growth", "customer acquisition", "roi",
    "analytics", "data-driven", "optimization", "strategy",
]

# Negative Keywords - Content to avoid
EXCLUDE_KEYWORDS = [
    "casino", "gambling", "crypto scam", "get rich quick", "weight loss",
    "adult", "nsfw", "conspiracy", "clickbait",
]

# Tone & Style - Friendly and approachable
TONE_INDICATORS = [
    "how to", "guide", "tips", "best practices", "learn", "easy",
    "simple", "practical", "helpful", "proven", "success", "strategy",
    "improve", "boost", "grow", "optimize", "streamline", "efficient",
]

# Platform-specific settings
LINKEDIN_MAX_LENGTH = 3000
X_MAX_LENGTH = 280
FACEBOOK_MAX_LENGTH = 5000

# Feed item limits
ITEMS_PER_FEED = 10  # Number of items to include in each RSS feed
POSTS_PER_DAY = 1

# File paths
FEEDS_DIR = "feeds"
ANALYTICS_DIR = "analytics"
BACKUP_DIR = "backups"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "autopost.log"

# Health check settings
MAX_AGE_HOURS = 48  # Alert if feeds haven't updated in 48 hours
MIN_ITEMS_PER_FEED = 5  # Minimum expected items per feed
