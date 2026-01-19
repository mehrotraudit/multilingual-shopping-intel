"""
Configuration for Multilingual Shopping Experience Opportunity Discovery System
Target Markets: US Hispanic (Spanish) and French-Canadian shoppers
"""

import os
from datetime import datetime

# System Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OUTPUT_DIR = "intelligence_briefs"
DATA_DIR = "market_data"

# Analysis Parameters
CHARTER_FIT_THRESHOLD = 50  # Minimum score to include in brief
TOP_OPPORTUNITIES_COUNT = 8
QUICK_WINS_COUNT = 3
LOOKBACK_DAYS = 14  # Bi-weekly cadence

# Target Markets Configuration
TARGET_MARKETS = {
    "hispanic_us": {
        "name": "US Hispanic (Spanish)",
        "population": "62M Hispanic Americans",
        "languages": ["Spanish", "Spanglish"],
        "key_segments": [
            "Mexican Spanish (60%)",
            "Caribbean Spanish (15%)",
            "Central American",
            "South American"
        ]
    },
    "french_canadian": {
        "name": "French-Canadian",
        "population": "8.5M Quebecers",
        "languages": ["French (Quebec variant)"],
        "key_segments": [
            "Quebec residents",
            "Francophone Canadians"
        ]
    }
}

# Reddit Sources
REDDIT_SOURCES = {
    "hispanic": [
        "r/latino",
        "r/hispanic",
        "r/spanglish",
        "r/mexico",
        "r/colombia",
        "r/puertorico",
        "r/amazon"  # For Spanish reviews/discussions
    ],
    "french_canadian": [
        "r/quebec",
        "r/montreal",
        "r/canada",  # Filter for French content
        "r/francophonie"
    ]
}

# News & Industry Sources (RSS Feeds)
RSS_SOURCES = {
    "hispanic_industry": [
        {"name": "Portada", "url": "https://www.portada-online.com/feed/"},
        {"name": "Hispanic Executive", "url": "https://hispanicexecutive.com/feed/"},
        {"name": "AdAge Hispanic", "url": "https://adage.com/section/hispanic-marketing/rss.xml"},
        {"name": "Retail Dive", "url": "https://www.retaildive.com/feeds/news/"}
    ],
    "french_canadian_industry": [
        {"name": "La Presse Affaires", "url": "https://www.lapresse.ca/affaires/rss"},
        {"name": "Les Affaires", "url": "https://www.lesaffaires.com/rss/"},
        {"name": "Marketing Magazine", "url": "https://marketingmag.ca/feed/"}
    ],
    "technology": [
        {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
        {"name": "VentureBeat", "url": "https://venturebeat.com/feed/"},
        {"name": "Product Hunt", "url": "https://www.producthunt.com/feed"}
    ]
}

# Search Keywords by Category
SEARCH_KEYWORDS = {
    "hispanic_customer_pain": [
        "amazon spanish",
        "amazon en español",
        "latino shopping",
        "hispanic products",
        "productos latinos",
        "spanish alexa",
        "voice search spanish",
        "amazon translation",
        "mexican products amazon",
        "quinceañera shopping"
    ],
    "french_canadian_customer_pain": [
        "amazon quebec",
        "amazon français",
        "achat local quebec",
        "fait au québec",
        "amazon.ca french",
        "bill 96 ecommerce",
        "commerce en ligne quebec",
        "produits québécois"
    ],
    "competitor_intelligence": [
        "walmart spanish",
        "walmart descubre",
        "target hispanic",
        "shopify multilingual",
        "mercado libre",
        "walmart canada french"
    ],
    "language_technology": [
        "spanish nlp",
        "french nlp",
        "multilingual ai",
        "regional dialect recognition",
        "spanish voice assistant",
        "french voice assistant",
        "translation quality"
    ]
}

# Twitter/X Search Terms
TWITTER_SEARCH_TERMS = {
    "hispanic": [
        "#LatinoTwitter shopping",
        "#HispanicHeritage amazon",
        "amazon español",
        "alexa español",
        "productos latinos"
    ],
    "french_canadian": [
        "#AchatLocal",
        "amazon quebec",
        "amazon français",
        "commerce québécois"
    ]
}

# Academic Sources (arXiv categories)
ARXIV_CATEGORIES = [
    "cs.CL",  # Computation and Language (NLP)
    "cs.AI",  # Artificial Intelligence
    "cs.HC"   # Human-Computer Interaction
]

ARXIV_KEYWORDS = [
    "spanish nlp",
    "french nlp",
    "multilingual",
    "dialect recognition",
    "cross-lingual",
    "translation quality",
    "cultural adaptation"
]

# Competitive Intelligence Targets
COMPETITORS = {
    "walmart": {
        "focus_areas": ["Spanish initiatives", "Descubre feature", "Hispanic marketing", "Canada French experience"],
        "urls": ["https://corporate.walmart.com/newsroom"]
    },
    "target": {
        "focus_areas": ["Hispanic programs", "Multicultural marketing"],
        "urls": ["https://corporate.target.com/press"]
    },
    "shopify": {
        "focus_areas": ["Multilingual features", "International commerce"],
        "urls": ["https://www.shopify.com/blog"]
    },
    "mercado_libre": {
        "focus_areas": ["Latin America innovations", "Spanish-first features"],
        "urls": ["https://www.mercadolibre.com"]
    }
}

# Opportunity Scoring Criteria
SCORING_CRITERIA = {
    "charter_fit": {
        "description": "How well does this align with Hispanic/French-Canadian shopping experience?",
        "weight": 0.30
    },
    "customer_evidence": {
        "description": "Strength of customer pain point signals",
        "weight": 0.25
    },
    "market_size": {
        "description": "Potential revenue impact",
        "weight": 0.20
    },
    "feasibility": {
        "description": "Technical and operational feasibility",
        "weight": 0.15
    },
    "competitive_advantage": {
        "description": "Differentiation opportunity",
        "weight": 0.10
    }
}

# Charter Expansion Themes
CHARTER_THEMES = [
    "Multilingual text experience",
    "Voice + text experience with dialect support",
    "Culturally-curated shopping experiences",
    "Regional product discovery",
    "Cultural event-driven commerce",
    "Language technology leadership",
    "Regulatory compliance (Bill 96, etc.)"
]

# Cultural Events Calendar
CULTURAL_EVENTS = {
    "hispanic": [
        {"name": "Hispanic Heritage Month", "dates": "Sep 15 - Oct 15", "shopping_opportunity": "Cultural products, books, decorations"},
        {"name": "Día de los Muertos", "dates": "Nov 1-2", "shopping_opportunity": "Decorations, altar supplies, traditional foods"},
        {"name": "Quinceañera Season", "dates": "Year-round peak: Spring/Summer", "shopping_opportunity": "Dresses, decorations, gifts"},
        {"name": "Three Kings Day", "dates": "Jan 6", "shopping_opportunity": "Gifts, traditional foods"},
        {"name": "Cinco de Mayo", "dates": "May 5", "shopping_opportunity": "Party supplies, foods, decorations"}
    ],
    "french_canadian": [
        {"name": "Saint-Jean-Baptiste Day", "dates": "Jun 24", "shopping_opportunity": "Quebec flags, party supplies"},
        {"name": "Fête Nationale", "dates": "Jun 24", "shopping_opportunity": "Quebec-made products"},
        {"name": "Sugar Shack Season", "dates": "Mar-Apr", "shopping_opportunity": "Maple products, cooking supplies"},
        {"name": "Quebec Winter Carnival", "dates": "Feb", "shopping_opportunity": "Winter clothing, party supplies"}
    ]
}

# Output Email Configuration
EMAIL_CONFIG = {
    "subject_template": "Multilingual Shopping Experience Opportunities - {date}",
    "recipients": [
        "product-leadership@example.com",
        "cx-team@example.com"
    ],
    "send_day": "Tuesday",  # Bi-weekly
    "send_hour": 9  # 9 AM
}

# Prompt Templates for Claude Analysis
ANALYSIS_PROMPTS = {
    "opportunity_extraction": """
You are analyzing market signals for Amazon's Multilingual Shopping Experience team, 
focused on Hispanic (US Spanish) and French-Canadian shoppers.

Analyze this content and identify product/feature opportunities:

CONTENT:
{content}

SOURCE: {source}
DATE: {date}

Provide a structured analysis:
1. RELEVANCE (0-100): How relevant is this to Hispanic/French-Canadian shopping?
2. CUSTOMER PAIN POINT: What specific problem do customers face?
3. OPPORTUNITY: What product/feature could address this?
4. CHARTER FIT (0-100): How well does this fit the multilingual CX charter?
5. MARKET SIZE: Estimated impact (users/revenue)
6. COMPETITIVE INTELLIGENCE: What are competitors doing?
7. CULTURAL CONTEXT: Any cultural nuances relevant here?
8. CHARTER EXPANSION ANGLE: How could this expand the team's scope?

Be specific and data-driven. If not relevant, explain why.
""",
    
    "opportunity_ranking": """
You are helping prioritize product opportunities for Amazon's Multilingual Shopping 
Experience team (Hispanic US and French-Canadian markets).

Rank these opportunities from highest to lowest priority based on:
- Charter fit (30%)
- Customer evidence strength (25%)
- Market size potential (20%)
- Feasibility (15%)
- Competitive advantage (10%)

OPPORTUNITIES:
{opportunities}

Provide:
1. Ranked list with scores
2. Top 3 "must pursue" with rationale
3. Quick wins (< 1 quarter effort)
4. Strategic bets (2+ quarters, high impact)
""",

    "strategic_memo": """
Create a strategic 1-pager memo for this opportunity:

OPPORTUNITY: {opportunity_title}
MARKET: {market}
EVIDENCE: {evidence}

Structure:
1. EXECUTIVE SUMMARY (3 sentences)
2. CUSTOMER PAIN POINT (specific examples)
3. PROPOSED SOLUTION
4. MARKET OPPORTUNITY (quantified)
5. CHARTER EXPANSION RATIONALE
6. TECHNICAL APPROACH
7. EFFORT ESTIMATE
8. NEXT ACTIONS

Write in Amazon's narrative style: data-driven, customer-obsessed, specific.
"""
}

# Data Processing Configuration
PROCESSING_CONFIG = {
    "max_signals_per_source": 50,
    "min_relevance_score": 60,
    "dedupe_similarity_threshold": 0.85,
    "sentiment_analysis": True,
    "trend_detection_window": 30  # days
}

# GitHub Actions Schedule (Cron)
GITHUB_SCHEDULE = "0 9 * * 2"  # Every Tuesday at 9 AM (bi-weekly filtering in code)
