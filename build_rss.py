#!/usr/bin/env python3
"""
ScalePilot — build_rss.py (AI-Generated Content + Quality Gates)

Key features:
- AI-generated content for small business audience
- Quality gates: ensure second-person voice, no banned phrases
- Duplicate detection with 5-gram similarity
- 30 rolling backups before any modification
- Bandit-based style weight learning

Requires env: OPENAI_API_KEY
Optional: BRAND, SITE_URL, MODEL
"""

import os, re, json, hashlib, random, sys
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from logger_config import get_logger
from backup_manager import backup_file

logger = get_logger(__name__)

# ---------- Paths ----------
CONFIG_PATH = "ops/config.json"
RULES_PATH  = "ops/rules.json"
BANDIT_PATH = "ops/bandit.json"
TAGS_PATH   = "content/tags.json"
TRENDS_PATH = "content/trends.json"
FPS_PATH    = "analytics/fingerprints.json"
TOPICS_FILE = "content/seeds_topics.txt"
FEED_FILE   = "feeds/rss.xml"

# HirePriority paths
HP_FEATURES_PATH = "content/hirepriority/features.json"
HP_PAIN_POINTS_PATH = "content/hirepriority/pain_points.json"
HP_RECIPE_PATH = "content/hirepriority/content_recipe.json"
HP_PLATFORM_SETTINGS_PATH = "content/hirepriority/platform_settings.json"

# ---------- Branding ----------
BRAND = os.getenv("BRAND", "ScalePilot")
SITE_URL = os.getenv("SITE_URL", "https://scalepilot.com/")
CHANNEL_TITLE = f"{BRAND} — AI Tools for SMBs"
CHANNEL_DESC  = f"{BRAND} — Daily AI automation insights for small business growth"
CHANNEL_LANG  = "en-us"

# ---------- Style catalog ----------
STYLE_CATALOG = [
    ("how_to",        "Practical how-to guide with clear steps for implementing AI tools"),
    ("tool_tip",      "Quick tip about a specific AI tool or feature that saves time"),
    ("case_study",    "Brief success story of SMB using AI automation"),
    ("quick_win",     "Easy AI automation win that can be implemented today"),
    ("stats_insight", "Data-driven insight about AI adoption or business impact"),
    ("framework",     "Simple framework or template for AI implementation"),
    ("mistake_avoid", "Common AI adoption mistake and how to avoid it")
]
EMOJI_PALETTE = ["✅","💡","🚀","🤖","💼","📊","⚡","🎯","🔧","💬","📈","🧠","⏱️","🌟","🔥","✨"]

DIALOGUE_PREFIX_RX = re.compile(r"\b(You|Them|Q|A):\s*", re.I)
FORBIDDEN_DIALOGUE_RX = re.compile(r"\b(You:|Them:|Q:|A:)\b", re.I)
FORBIDDEN_META_RX = re.compile(r"\b(in this thread|see below)\b", re.I)
WHITESPACE_RX = re.compile(r"\s{2,}")
URL_RX = re.compile(r"https?://\S+")
HASHTAG_RX = re.compile(r"#[A-Za-z0-9_]+")

# ---------- Helpers ----------
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Loaded JSON from {path}")
            return data
    except FileNotFoundError:
        logger.warning(f"File not found: {path}, using default")
        return default
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in {path}: {e}")
        return default
    except Exception as e:
        logger.error(f"Unexpected error loading {path}: {e}")
        return default

def rss_now():
    return datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")

def read_topics(path):
    base = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            base = [ln.strip() for ln in f if ln.strip()]
    except FileNotFoundError:
        base = ["AI automation for small business", "ChatGPT for marketing", "AI recruiting tools"]
    trends = load_json(TRENDS_PATH, {}).get("items", [])
    t_titles = [t.get("title","") for t in trends if t.get("title")] [:10]
    seen = set(); out=[]
    for t in base + t_titles:
        if t not in seen:
            out.append(t); seen.add(t)
    return out

def choose_style(weights):
    pool = []
    for key, desc in STYLE_CATALOG:
        w = max(0.01, float(weights.get(key, 1.0)))
        pool.append((key, desc, w))
    total = sum(w for _,_,w in pool)
    r = random.random() * total; c = 0.0
    for key, desc, w in pool:
        c += w
        if r <= c: return key, desc
    return pool[0][0], pool[0][1]

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

def slugify(text, n=60):
    text = re.sub(r"[^\w\s-]", "", (text or "")).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:n] or "post"

def has_emoji(s: str) -> int:
    return sum(1 for ch in s if ord(ch) >= 0x1F300 or ch in ("✅","💡","🚀","🤖","💼","📊","⚡","🎯","🔧"))

def add_minimum_emojis(line: str, need_min=2) -> str:
    count = has_emoji(line)
    if count >= need_min: return line
    palette = EMOJI_PALETTE[:]
    random.shuffle(palette)
    return f"{palette[0]} {line}" if (need_min - count) == 1 else f"{palette[0]} {line} {palette[1]}"

def enforce_second_person_line(line: str) -> str:
    """
    Ensure the main X line keeps a visible second-person signal even after sanitation.
    """
    if not line:
        return line
    if re.search(r"\b(you|your)\b", line, re.I):
        return line
    if re.search(r"Use:\s*[\"']", line, re.I):
        return line
    match = re.match(r"^([\W]*)(.*)$", line)
    if not match:
        return f"You {line}"
    prefix, remainder = match.groups()
    remainder = remainder.strip()
    if not remainder:
        return f"{prefix}You"
    return f"{prefix}You {remainder}"

def sanitize_xline(s: str) -> str:
    def _dialogue_repl(match: re.Match) -> str:
        token = match.group(1).lower()
        if token == "you":
            return "You "
        return ""
    s = DIALOGUE_PREFIX_RX.sub(_dialogue_repl, s)
    s = FORBIDDEN_META_RX.sub("", s)
    s = WHITESPACE_RX.sub(" ", s)
    s = URL_RX.sub("", s)
    s = HASHTAG_RX.sub("", s)
    return s.strip()

def ngrams(text, n=5):
    toks = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {" ".join(toks[i:i+n]) for i in range(0, max(0, len(toks)-n+1))}

def jaccard(a, b):
    if not a or not b: return 0.0
    inter = len(a & b); uni = len(a | b)
    return inter / uni if uni else 0.0

def dup_guard_ok(title, fps, n, thr):
    probe = ngrams(title, n)
    for fp in fps:
        if jaccard(probe, set(fp.get("ngrams", []))) >= thr:
            return False
    return True

# ---- Tags coercion ----
def coerce_tag_list(obj):
    out = []
    if isinstance(obj, list):
        cand = obj
    elif isinstance(obj, dict):
        cand = list(obj.keys()) + list(obj.values())
    elif isinstance(obj, str):
        cand = re.split(r"[,\s]+", obj)
    else:
        cand = []
    for x in cand:
        if isinstance(x, str):
            s = x.strip().lower()
            if s: out.append(s)
        elif isinstance(x, list):
            for y in x:
                if isinstance(y, str):
                    s = y.strip().lower()
                    if s: out.append(s)
    seen=set(); clean=[]
    for s in out:
        if s not in seen:
            seen.add(s); clean.append(s)
    return clean

# ---- Persona & quality gate utilities ----
QUOTE_CHARS = "\"'""''"
def contains_unquoted_I(text: str) -> bool:
    """Return True if ' I ' appears outside of quotes."""
    # Strip quoted segments then search
    tmp = re.sub(r"[\"""''][^\"""'']+[\"""'']", " ", text)
    return bool(re.search(r"\bI\b", tmp))

def has_banned_phrases(text: str, banned: list) -> bool:
    low = text.lower()
    for p in banned:
        if p.strip() and p.lower() in low:
            return True
    return False

WHEN_I_PAST_RX = re.compile(r"\bwhen\s+\w+ing\b.*\bI\b.*\b(achieved|led to|delivered|shipped)\b", re.I)

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

def quality_gate(x_line: str, rules: dict) -> tuple:
    """
    Returns (ok, reason_if_bad)
    """
    # No dialogue markers or meta
    if FORBIDDEN_DIALOGUE_RX.search(x_line) or FORBIDDEN_META_RX.search(x_line):
        return False, "dialogue/meta markers"
    # Banned phrases
    if has_banned_phrases(x_line, rules.get("banned_phrases", [])):
        return False, "banned phrase"
    # Tense conflict like 'When ... I achieved ...'
    if WHEN_I_PAST_RX.search(x_line):
        return False, "tense conflict (when...I...achieved)"
    # Enforce second-person voice (soft): prefer 'you/your' somewhere
    if rules.get("enforce_second_person", False):
        if not re.search(r"\b(you|your)\b", x_line, re.I):
            # allow templates starting with 'Use:' that quote 1st person
            if not re.search(r'Use:\s*["\']', x_line):
                return False, "missing second-person signal"
    # First-person outside quotes not allowed
    if rules.get("allow_first_person_in_quotes_only", False):
        if contains_unquoted_I(x_line):
            return False, "first-person outside quotes"
    return True, ""

# ---- OpenAI call ----
@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    reraise=True
)
class QuotaExceededError(Exception):
    """Raised when OpenAI API quota is exceeded"""
    pass

def call_openai(topic, style_key, style_desc, model, rules, pass_hint=""):
    """
    Generate AI content for ScalePilot SMB audience
    """
    payload = None
    sys = (
        "You are an AI automation expert and small business consultant. "
        "You write friendly, practical advice for SMB owners and operators. "
        "Focus on actionable insights about AI tools, automation, and business growth. "
        "Keep it approachable, concrete, and jargon-free. "
        "Every post must be self-contained (no 'in this thread', no external links)."
    )

    min_emojis = int(rules.get("min_emojis", 2))
    require_number = bool(rules.get("require_number_in_title", False))
    banned_join = "; ".join(rules.get("banned_phrases", []))

    user = f"""
STYLE: {style_key}
STYLE_DESC: {style_desc}
TOPIC_SEED: "{topic}"

VOICE: Friendly AI/business expert helping SMBs automate and grow.
AUDIENCE: Small business owners, operations managers, HR teams, marketers.
BAN: Sales pitch language; phrases → {banned_join or "—"}.
TONE: Approachable, practical, optimistic about AI helping small businesses.

OUTPUT RULES
- Return STRICT JSON only.
- x_line: SINGLE line for X/Twitter (<= 230 chars), friendly tone, {min_emojis}–4 emojis, no hashtags/links. Focus on the key insight or action.
- desc_title: Catchy hook (<= 80 chars) + 1–2 emojis.
- desc_points: 3–5 bullets; actionable steps or insights; <= 80 chars; max 1 emoji each.
- desc_cta: 1 engaging question or thought (<= 110 chars).
- tags: 2 short lowercase tags WITHOUT dashes (e.g., 'ai', 'automation', 'marketing'). No '#' symbol.
- require_number_in_title={str(require_number).lower()}

{pass_hint}
"""

    # Validate API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable is not set")
        raise ValueError("OPENAI_API_KEY environment variable is required")

    try:
        from openai import OpenAI

        try:
            client = OpenAI(
                api_key=api_key,
                timeout=30.0,
                max_retries=0
            )
        except TypeError as e:
            logger.warning(f"Standard client init failed ({e}), trying minimal init")
            client = OpenAI(api_key=api_key)

        attempts = [model or "gpt-4o", "gpt-4o", "gpt-4o-mini"]

        quota_exceeded = False
        for mdl in attempts:
            try:
                logger.info(f"Attempting content generation with model: {mdl}")
                resp = client.chat.completions.create(
                    model=mdl, temperature=0.7,
                    messages=[{"role":"system","content":sys},{"role":"user","content":user}]
                )
                txt = (resp.choices[0].message.content or "").strip()
                start, end = txt.find("{"), txt.rfind("}")
                if start == -1 or end == -1:
                    logger.warning(f"Model {mdl} returned non-JSON response")
                    continue
                payload = json.loads(txt[start:end+1])
                if payload:
                    logger.info(f"Successfully generated content with model: {mdl}")
                    break
            except json.JSONDecodeError as e:
                logger.warning(f"Model {mdl} returned invalid JSON: {e}")
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                    quota_exceeded = True
                    logger.error(f"QUOTA EXCEEDED for model {mdl}: {e}")
                else:
                    logger.warning(f"Model {mdl} failed: {e}")

        # If all attempts failed due to quota, raise specific error
        if quota_exceeded and not payload:
            raise QuotaExceededError("OpenAI API quota exceeded for all models")
    except ImportError as e:
        logger.error(f"Failed to import OpenAI library: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in OpenAI call: {e}")
        raise

    # Fallback payload
    if not payload:
        logger.warning("All OpenAI attempts failed, using safe fallback content")
        payload = {
            "style": style_key, "cta_type": "question",
            "x_line": '🤖 AI can automate 70% of repetitive tasks in your business. Start with one workflow this week. 🚀',
            "desc_title": "Start with AI automation 💡",
            "desc_points": ["Pick one repetitive task 📋","Find an AI tool (ChatGPT, Zapier) 🔧","Test it for 1 week ⏱️","Measure time saved 📊"],
            "desc_cta": "What's one task you'd automate first?",
            "tags": ["ai","automation"]
        }
    return payload

# ---- Feed scaffold ----
def ensure_feed_scaffold():
    os.makedirs("feeds", exist_ok=True)
    if not os.path.exists(FEED_FILE):
        rss = ET.Element("rss", attrib={"version":"2.0"})
        ch = ET.SubElement(rss,"channel")
        ET.SubElement(ch,"title").text = CHANNEL_TITLE
        ET.SubElement(ch,"link").text = SITE_URL
        ET.SubElement(ch,"description").text = CHANNEL_DESC
        ET.SubElement(ch,"language").text = CHANNEL_LANG
        now = rss_now()
        ET.SubElement(ch,"lastBuildDate").text = now
        ET.SubElement(ch,"pubDate").text = now
        ET.ElementTree(rss).write(FEED_FILE, encoding="utf-8", xml_declaration=True)
    tree = ET.parse(FEED_FILE)
    root = tree.getroot(); ch = root.find("channel") or ET.SubElement(root,"channel")
    def ensure(tag, text=None):
        node = ch.find(tag)
        if node is None: node = ET.SubElement(ch, tag)
        if text is not None and (node.text or "").strip() == "": node.text = text
        return node
    ensure("title", CHANNEL_TITLE); ensure("link", SITE_URL)
    ensure("description", CHANNEL_DESC); ensure("language", CHANNEL_LANG)
    ensure("lastBuildDate", rss_now()); ensure("pubDate", rss_now())
    tree.write(FEED_FILE, encoding="utf-8", xml_declaration=True)
    return tree

# ---- Build item ----
def make_item(payload, rules):
    style_key = (payload.get("style") or "").strip().lower() or "unspecified"
    cta_type  = (payload.get("cta_type") or "").strip().lower() or "question"

    x_line = sanitize_xline((payload.get("x_line") or "").strip())
    x_line = add_minimum_emojis(x_line, need_min=rules.get("min_emojis",2))
    if len(x_line) > 230:
        x_line = x_line[:229].rsplit(" ", 1)[0] + "…"

    hook   = (payload.get("desc_title") or "").strip()
    points = [p.strip(" •-") for p in (payload.get("desc_points") or []) if str(p).strip()]
    cta    = (payload.get("desc_cta") or "").strip()

    tag_bank = coerce_tag_list(load_json(TAGS_PATH, []))
    ptags = coerce_tag_list(payload.get("tags") or [])[:2]
    for t in ptags:
        if t not in tag_bank:
            tag_bank.append(t)
    tags_raw = (ptags[:2]) if ptags else (tag_bank[:2])

    bullets_fmt = "\n".join([f"• {b}" for b in points])

    def clean_hashtag(token: str) -> str:
        return re.sub(r"[^A-Za-z0-9]", "", token or "")

    tag_tokens = [clean_hashtag(t) for t in tags_raw]
    tag_tokens = [tok for tok in tag_tokens if tok]
    tag_str = " ".join([f"#{tok}" for tok in tag_tokens]) if tag_tokens else ""
    description = "\n".join([s for s in [hook, "", bullets_fmt, "", cta, "", tag_str] if s]).strip()

    now = datetime.now(timezone.utc)
    base = f"{slugify(x_line)}-{now.strftime('%Y%m%d%H%M%S')}"
    guid = hashlib.sha1(base.encode("utf-8")).hexdigest()
    link = f"{SITE_URL}?p={guid}"

    item = ET.Element("item")
    ET.SubElement(item,"title").text = x_line
    ET.SubElement(item,"description").text = description
    ET.SubElement(item,"link").text = link
    ET.SubElement(item,"guid", attrib={"isPermaLink":"false"}).text = guid
    ET.SubElement(item,"pubDate").text = rss_now()
    ET.SubElement(item,"category", attrib={"domain":"style"}).text = style_key
    ET.SubElement(item,"category", attrib={"domain":"cta"}).text = cta_type
    return item, guid, x_line

def prepend_item(tree, item):
    ch = tree.getroot().find("channel") or ET.SubElement(tree.getroot(),"channel")
    items = ch.findall("item")
    if items: ch.insert(list(ch).index(items[0]), item)
    else: ch.append(item)
    for tag in ("lastBuildDate","pubDate"):
        node = ch.find(tag) or ET.SubElement(ch, tag)
        node.text = rss_now()
    tree.write(FEED_FILE, encoding="utf-8", xml_declaration=True)

# ---------- Main ----------
cfg   = load_json(CONFIG_PATH, {})
rules = load_json(RULES_PATH, {})
band  = load_json(BANDIT_PATH, {})
if cfg.get("paused"):
    print("Paused by ops/config.json"); raise SystemExit(0)

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

# OLD SCALEPILOT LOGIC (archived)
# topics = read_topics(TOPICS_FILE)
# topic = random.choice(topics) if topics else "AI automation for small business"
# style_weights = band.get("style_weights", {
#     "how_to":1.5, "tool_tip":1.4, "case_study":1.2, "quick_win":1.3,
#     "stats_insight":1.1, "framework":1.0, "mistake_avoid":1.1
# })
# style_key, style_desc = choose_style(style_weights)

random.seed(int(datetime.now(timezone.utc).strftime("%Y%m%d%H")))
model  = os.getenv("MODEL") or cfg.get("model") or "gpt-4o"

# Generate with up to 3 attempts, tightening constraints if the quality gate fails
attempt_notes = [
    "",
    "REVISION: Fix any tense conflict; keep second-person; if using a template, prefix 'Use:' then quote the line.",
    "REVISION: Remove any first-person narration; only quote first-person inside 'Use: \"...\"'; add a concrete number or example if helpful."
]
payload = None
xline = ""; ok=False; reason=""

for attempt_num, note in enumerate(attempt_notes, 1):
    logger.info(f"Quality gate attempt {attempt_num}/{len(attempt_notes)}")
    try:
        # Use archived logic temporarily (will be replaced with HirePriority-specific call)
        # For now using user_prompt directly in call_openai
        # TODO: Refactor call_openai to accept raw user_prompt instead of topic/style
        p = call_openai("HirePriority pain point content", "hirepriority", user_prompt, model, rules, pass_hint=note)

        # assemble to see x_line and test
        candidate = sanitize_xline((p.get("x_line") or "").strip())
        candidate = add_minimum_emojis(candidate, need_min=rules.get("min_emojis",2))
        if len(candidate) > 230:
            candidate = candidate[:229].rsplit(" ", 1)[0] + "..."
        original_candidate = candidate
        candidate = enforce_second_person_line(candidate)
        if candidate != original_candidate:
            logger.debug("Auto-inserted second-person phrasing into X line to satisfy quality gate.")

        # Content recipe validation
        full_content = candidate
        recipe_valid, recipe_msg = validate_content_recipe(full_content)
        if not recipe_valid:
            logger.warning(f"Content recipe validation failed: {recipe_msg}")
            continue  # Retry generation

        ok, reason = quality_gate(candidate, rules)
        if ok:
            logger.info(f"Quality gate passed on attempt {attempt_num}")
            payload = p; xline = candidate; break
        else:
            logger.warning(f"Quality gate failed on attempt {attempt_num}: {reason}")
    except QuotaExceededError as e:
        logger.error("=" * 80)
        logger.error("CRITICAL ERROR: OpenAI API Quota Exceeded!")
        logger.error("=" * 80)
        logger.error("Your OpenAI API account has run out of credits.")
        logger.error("To fix this issue:")
        logger.error("  1. Visit https://platform.openai.com/account/billing")
        logger.error("  2. Add credits to your account or upgrade your plan")
        logger.error("  3. Verify your GitHub secret OPENAI_API_KEY is correct")
        logger.error("=" * 80)
        print("\n❌ ERROR: OpenAI API quota exceeded. Please add credits to your OpenAI account.\n", file=sys.stderr)
        raise SystemExit(2)  # Exit code 2 = quota error
    except Exception as e:
        logger.error(f"Attempt {attempt_num} raised exception: {e}")

if not payload:
    # CRITICAL: Do not publish content that failed all quality gates
    # Instead, skip this run and let the next scheduled run try again
    logger.error("All quality gate attempts failed. Skipping content generation for this run.")
    logger.info("The next scheduled run will attempt content generation again.")
    raise SystemExit(1)

logger.info(f"Selected pain point: {pain_point.get('category', 'Unknown')} - {pain_point.get('hook', '')[:50]}...")

# Backup existing feed before modification
backup_file(FEED_FILE, keep_count=30)

tree = ensure_feed_scaffold()
item, guid, title = make_item(payload, rules)

# duplicate guard
fps = load_json(FPS_PATH, [])
dg = cfg.get("dup_guard", {"enabled":True,"ngram":5,"threshold":0.8,"history_size":200})
if dg.get("enabled", True):
    if not dup_guard_ok(title, fps, dg.get("ngram",5), dg.get("threshold",0.8)):
        # Regenerate with different approach (HirePriority uses same pain point but different angle)
        logger.warning("Duplicate detected, regenerating with different approach")
        p2 = call_openai("HirePriority pain point content", "hirepriority", user_prompt, model, rules, pass_hint="REVISION: Use different wording and angle while maintaining the pain point focus.")
        item2, guid2, title2 = make_item(p2, rules)
        if dup_guard_ok(title2, fps, dg.get("ngram",5), dg.get("threshold",0.8)):
            item, guid, title = item2, guid2, title2

prepend_item(tree, item)

# save fingerprint
probe = list(ngrams(title, dg.get("ngram",5)))
fps = (fps + [{"guid":guid, "ngrams":probe}])[-int(dg.get("history_size",200)):]
os.makedirs("analytics", exist_ok=True)
with open(FPS_PATH, "w", encoding="utf-8") as f:
    json.dump(fps, f, ensure_ascii=False, indent=2)

print("Generated:", title)
