# Multilingual Shopping Experience Opportunity Discovery System

An automated intelligence system that discovers product and feature opportunities for Hispanic (US Spanish) and French-Canadian shopping experiences at Amazon.

## 🎯 Purpose

Help Amazon's Multilingual Customer Experience Product team identify and prioritize opportunities to expand their charter by:
- Monitoring customer pain points across Reddit, industry news, and academic research
- Analyzing market signals using AI (Claude)
- Generating actionable bi-weekly intelligence briefs
- Scoring opportunities based on charter fit, customer evidence, and market size

## 🎨 Target Markets

**US Hispanic (Spanish)**
- 62M Hispanic Americans
- 38M Spanish speakers at home
- Key segments: Mexican Spanish (60%), Caribbean Spanish (15%), Central/South American

**French-Canadian**
- 8.5M Quebecers
- 85% speak French primarily
- Quebec-specific culture and language needs

## 📊 System Architecture

```
┌─────────────────────────────────────────────────┐
│           DATA COLLECTION (Weekly)              │
├─────────────────────────────────────────────────┤
│ • Reddit API (Hispanic/French-Canadian subs)    │
│ • RSS Feeds (Hispanic marketing, Quebec news)   │
│ • Twitter/X API (Spanish/French shopping talk)  │
│ • arXiv (Spanish/French NLP papers)             │
│ • Competitor intelligence                       │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│        AI ANALYSIS (Claude API)                 │
├─────────────────────────────────────────────────┤
│ For each signal:                                │
│ 1. Relevance to Hispanic/French markets        │
│ 2. Customer pain point identified               │
│ 3. Product/feature opportunity                  │
│ 4. Charter fit score (0-100)                    │
│ 5. Market size estimate                         │
│ 6. Competitive intelligence                     │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│           OPPORTUNITY BRIEF GENERATION          │
├─────────────────────────────────────────────────┤
│ • Top 8-12 opportunities ranked                 │
│ • Market signals & customer evidence            │
│ • Charter expansion angles                      │
│ • Strategic memo starters                       │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│      BI-WEEKLY EMAIL (Every Other Tuesday)      │
└─────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Anthropic API key (for Claude analysis)
- Optional: Reddit API, Twitter API for enhanced data collection

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd multilingual-shopping-intel

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Basic Usage

**Run the full pipeline:**
```bash
python main.py
```

**Run with your own API key:**
```bash
python main.py --api-key "sk-ant-..."
```

**Run with cached data (no new collection):**
```bash
python main.py --dry-run
```

**Test individual components:**
```bash
# Test data collection only
python market_intelligence.py

# Test opportunity analysis
python opportunity_analyzer.py

# Test brief generation
python brief_generator.py
```

## 📁 Project Structure

```
multilingual-shopping-intel/
├── config.py                      # Configuration and data sources
├── market_intelligence.py         # Data collection from multiple sources
├── opportunity_analyzer.py        # Claude-powered opportunity analysis
├── brief_generator.py            # Intelligence brief formatting
├── main.py                       # Main orchestration script
├── requirements.txt              # Python dependencies
├── .github/
│   └── workflows/
│       └── biweekly-intel.yml   # GitHub Actions automation
├── market_data/                 # Collected signals (generated)
│   ├── market_signals.json
│   └── opportunities.json
└── intelligence_briefs/         # Generated briefs (generated)
    ├── intelligence_brief_YYYYMMDD.txt
    └── intelligence_brief_YYYYMMDD.html
```

## 🔧 Configuration

Edit `config.py` to customize:

**Data Sources:**
- Reddit subreddits to monitor
- RSS feeds to track
- Search keywords by category
- Competitor websites

**Analysis Parameters:**
- Charter fit threshold (default: 70/100)
- Number of top opportunities (default: 8)
- Lookback period (default: 14 days)

**Scoring Criteria Weights:**
- Charter fit: 30%
- Customer evidence: 25%
- Market size: 20%
- Feasibility: 15%
- Competitive advantage: 10%

## 📈 Output Examples

### Intelligence Brief Structure

Each bi-weekly brief includes:

1. **Market Snapshot**
   - Signals analyzed by market
   - High-priority opportunity count
   - Quick wins identified

2. **Top Opportunities (Detailed)**
   - Title and charter fit score
   - Customer pain points
   - Proposed solutions
   - Market size estimates
   - Competitive intelligence
   - Charter expansion angles
   - Evidence sources

3. **Quick Win Opportunities**
   - Lower effort, high impact items
   - 1-2 quarter implementation timeline

4. **Trending Topics**
   - Rising themes in the market
   - Declining trends to note

5. **Recommended Actions**
   - Prioritized next steps
   - Research recommendations

### Sample Opportunity

```
🔥 TOP OPPORTUNITY #1
Spanish Voice Search with Regional Accent Support

CHARTER FIT: 95/100 ⭐⭐⭐⭐⭐

WHAT WE FOUND:
• Reddit: 8 threads about Alexa not understanding Mexican Spanish
• Customer pain: "Alexa speaks like she's from Madrid, not Miami"
• Competitor gap: Google Assistant improved regional dialects

CUSTOMER EVIDENCE:
"I have to switch to English when talking to Alexa about shopping 
because she doesn't understand my Colombian accent" - Reddit user

OPPORTUNITY:
Enhance Rufus/Alexa voice shopping to handle:
• Mexican Spanish (largest US Hispanic group - 60%)
• Caribbean Spanish (Puerto Rican, Cuban - 15%)
• Central American variants

MARKET SIZE:
• 62M Hispanic Americans
• Voice shopping penetration: 24% → 45% with better support
• Revenue opportunity: $400M+ annually

CHARTER EXPANSION ANGLE:
From: "Multilingual text experience"
To: "Full multilingual voice + text with dialect support"
```

## 🤖 Automated Execution

### GitHub Actions Setup

The system can run automatically every other Tuesday:

1. **Add repository secrets:**
   - `ANTHROPIC_API_KEY`: Your Claude API key
   - Optional: `EMAIL_USERNAME`, `EMAIL_PASSWORD` for notifications

2. **Enable GitHub Actions:**
   - Workflow file is at `.github/workflows/biweekly-intel.yml`
   - Runs on schedule: `0 9 * * 2` (9 AM UTC every Tuesday)
   - Manual trigger available via GitHub UI

3. **Access outputs:**
   - Download artifacts from GitHub Actions runs
   - Intelligence briefs saved as both .txt and .html

### Alternative: Cron Job

```bash
# Edit crontab
crontab -e

# Add line to run every other Tuesday at 9 AM
0 9 * * 2 cd /path/to/project && /usr/bin/python3 main.py --scheduled
```

## 📊 Data Sources Monitored

### Customer Voice
- **Reddit**: r/latino, r/hispanic, r/spanglish, r/mexico, r/colombia, r/quebec, r/montreal
- **Twitter/X**: #LatinoTwitter, #HispanicHeritage, #AchatLocal, Spanish/French shopping discussions
- **Amazon Reviews**: Spanish/French review analysis

### Industry Intelligence
- **Hispanic Market**: Portada, Hispanic Executive, AdAge Hispanic Marketing
- **French-Canadian**: La Presse, Les Affaires, Marketing Magazine
- **Technology**: TechCrunch, VentureBeat, Product Hunt

### Academic Research
- **arXiv**: NLP papers on Spanish/French language technology
- **Keywords**: Multilingual AI, dialect recognition, translation quality

### Competitive Intelligence
- **Walmart**: Spanish initiatives, Descubre feature, Canada French experience
- **Target**: Hispanic marketing programs
- **Shopify**: Multilingual commerce features
- **Mercado Libre**: Latin America innovations

## 🎯 Opportunity Scoring

Each opportunity is scored on five criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Charter Fit** | 30% | Alignment with Hispanic/French-Canadian CX charter |
| **Customer Evidence** | 25% | Strength of customer pain point signals |
| **Market Size** | 20% | Revenue/user impact potential |
| **Feasibility** | 15% | Technical and operational feasibility |
| **Competitive Advantage** | 10% | Differentiation opportunity |

**Composite Score** = Weighted sum of all criteria (0-100)

**Categorization:**
- 85+: High priority / Must pursue
- 70-84: Strong opportunity
- 60-69: Consider if resources available
- <60: Monitor but don't pursue

## 🔍 Cultural Events Tracked

### Hispanic Market
- Hispanic Heritage Month (Sep 15 - Oct 15)
- Día de los Muertos (Nov 1-2)
- Three Kings Day (Jan 6)
- Cinco de Mayo (May 5)
- Quinceañera season (year-round, peak Spring/Summer)

### French-Canadian Market
- Saint-Jean-Baptiste Day (Jun 24)
- Sugar Shack Season (Mar-Apr)
- Quebec Winter Carnival (Feb)

## 🚀 Roadmap & Enhancements

### Phase 1 (Current - MVP)
- ✅ Multi-source signal collection
- ✅ Claude-powered opportunity analysis
- ✅ Bi-weekly brief generation
- ✅ GitHub Actions automation

### Phase 2 (Next 2 Weeks)
- [ ] Amazon review mining (Spanish/French)
- [ ] Trend detection algorithms
- [ ] Competitive gap analysis
- [ ] Market size estimator
- [ ] Strategic memo generator (full 1-pagers)

### Phase 3 (Future)
- [ ] Real-time Reddit/Twitter monitoring
- [ ] Customer interview insights integration
- [ ] A/B test results correlation
- [ ] Charter expansion simulator
- [ ] Interactive dashboard (Streamlit/Gradio)

## 🛠️ Customization Guide

### Adding New Data Sources

Edit `config.py`:

```python
RSS_SOURCES = {
    "your_category": [
        {"name": "Source Name", "url": "https://example.com/feed"},
    ]
}
```

### Adding New Keywords

```python
SEARCH_KEYWORDS = {
    "new_category": [
        "keyword1",
        "keyword2"
    ]
}
```

### Adjusting Scoring Weights

```python
SCORING_CRITERIA = {
    "charter_fit": {"weight": 0.35},  # Increase importance
    "customer_evidence": {"weight": 0.30},
    # ... adjust other weights (must sum to 1.0)
}
```

### Customizing Brief Format

Edit `brief_generator.py`:
- Modify `_format_opportunity()` for different layouts
- Adjust `_generate_header()` for custom branding
- Update `export_to_html()` for visual styling

## 📧 Email Integration

To enable automated email delivery:

1. **Set up email credentials:**
```bash
export EMAIL_USERNAME="your-email@company.com"
export EMAIL_PASSWORD="your-app-password"
```

2. **Configure recipients in `config.py`:**
```python
EMAIL_CONFIG = {
    "recipients": [
        "product-lead@company.com",
        "cx-team@company.com"
    ]
}
```

3. **Uncomment email step in GitHub Actions workflow**

## 🐛 Troubleshooting

**Issue: "No module named 'anthropic'"**
```bash
pip install anthropic
```

**Issue: "ANTHROPIC_API_KEY not set"**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**Issue: RSS feed fails to parse**
- Check feed URL is accessible
- Some feeds may require User-Agent headers
- Add error handling for specific feeds

**Issue: Rate limiting**
- Add delays between API calls
- Implement exponential backoff
- Cache results to reduce calls

## 📚 Additional Resources

- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [arXiv API Documentation](https://arxiv.org/help/api/)

## 🤝 Contributing

This is an internal tool. For improvements:
1. Test changes locally with `python main.py --dry-run`
2. Update documentation
3. Submit PR with clear description

## 📄 License

Internal Amazon tool - proprietary and confidential

## 👥 Team

**Owner**: Head of Product, Multilingual Customer Experience
**Maintainer**: [Your name]
**Stakeholders**: CX Product Leadership Team

## 📞 Support

Questions or issues:
- Slack: #multilingual-cx-product
- Email: multilingual-cx@amazon.com

---

**Last Updated**: January 2026
**Version**: 1.0.0 (MVP)
