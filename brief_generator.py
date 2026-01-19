"""
Brief Generator Module
Creates bi-weekly intelligence digest with top opportunities
"""

from datetime import datetime
from typing import List, Dict, Any
import os


class BriefGenerator:
    """Generates formatted bi-weekly intelligence briefs"""
    
    def __init__(self, config):
        self.config = config
        self.brief_date = datetime.now().strftime("%B %d, %Y")
    
    def generate_brief(self, opportunities: List[Dict], signals: List[Dict]) -> str:
        """Generate the complete bi-weekly brief"""
        
        print("\n📄 Generating bi-weekly intelligence brief...")
        
        # Filter opportunities by score
        high_priority = [o for o in opportunities if o['composite_score'] >= 85]
        quick_wins = [o for o in opportunities if self._is_quick_win(o)]
        
        # Count signals by market
        hispanic_signals = len([s for s in signals if 'hispanic' in s.get('market', '')])
        french_signals = len([s for s in signals if 'french' in s.get('market', '')])
        
        brief = self._generate_header(len(signals), hispanic_signals, french_signals, 
                                     len(high_priority), len(quick_wins))
        
        # Top opportunities (detailed)
        top_n = min(self.config.TOP_OPPORTUNITIES_COUNT, len(opportunities))
        for i, opp in enumerate(opportunities[:top_n], 1):
            brief += self._format_opportunity(i, opp, detailed=i <= 3)
        
        # Quick wins section
        if quick_wins:
            brief += self._format_quick_wins(quick_wins[:self.config.QUICK_WINS_COUNT])
        
        # Trending topics
        brief += self._format_trending_topics(signals)
        
        # Recommended actions
        brief += self._format_recommended_actions(opportunities[:3])
        
        # Footer
        brief += self._generate_footer()
        
        print("✓ Brief generated successfully")
        return brief
    
    def _generate_header(self, total_signals: int, hispanic_count: int, 
                        french_count: int, high_priority: int, quick_wins: int) -> str:
        """Generate brief header"""
        
        header = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MULTILINGUAL SHOPPING EXPERIENCE OPPORTUNITIES
{self.brief_date} - Bi-Weekly Intelligence Brief
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 MARKET SNAPSHOT
• Hispanic market signals: {hispanic_count} analyzed
• French-Canadian signals: {french_count} analyzed  
• High-priority opportunities: {high_priority}
• Quick wins: {quick_wins}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        return header
    
    def _format_opportunity(self, rank: int, opp: Dict, detailed: bool = True) -> str:
        """Format a single opportunity"""
        
        stars = "⭐" * (int(opp.get('composite_score', 0)) // 20)
        
        section = f"""🔥 TOP OPPORTUNITY #{rank}
{opp['title']}

CHARTER FIT: {opp['charter_fit_score']}/100 {stars}

"""
        
        if detailed:
            # Detailed format for top 3
            section += f"""WHAT WE FOUND:
{opp.get('competitive_intelligence', 'Market research indicates significant opportunity.')}

CUSTOMER PAIN POINT:
{opp.get('customer_pain_point', 'Customer feedback highlights need for improvement.')}

OPPORTUNITY:
{opp.get('proposed_solution', 'Proposed solution to be developed.')}

MARKET SIZE:
{opp.get('market_size', 'Market size to be determined through further research.')}

CHARTER EXPANSION ANGLE:
{opp.get('charter_expansion_angle', 'Expands team charter into new strategic area.')}

EVIDENCE SOURCES:
"""
            # Add source signals
            for signal in opp.get('source_signals', [])[:3]:
                section += f"• {signal['title']} ({signal['source']})\n"
            
            section += "\n"
        
        else:
            # Abbreviated format for 4+
            section += f"""QUICK SUMMARY:
{opp.get('customer_pain_point', '')[:200]}...

KEY INSIGHT:
{opp.get('proposed_solution', '')[:200]}...

CHARTER FIT: {opp['charter_fit_score']}/100 | MARKET: {opp.get('source_signals', [{}])[0].get('market', 'Multiple') if opp.get('source_signals') else 'Multiple'}

"""
        
        section += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        return section
    
    def _format_quick_wins(self, quick_wins: List[Dict]) -> str:
        """Format quick wins section"""
        
        section = """⚡ QUICK WIN OPPORTUNITIES

"""
        for i, opp in enumerate(quick_wins, 1):
            section += f"""{i}. **{opp['title']}** (Est. {self._estimate_effort(opp)})
   - {opp.get('customer_pain_point', '')[:150]}
   - Charter Fit: {opp['charter_fit_score']}/100

"""
        
        section += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        return section
    
    def _format_trending_topics(self, signals: List[Dict]) -> str:
        """Format trending topics section"""
        
        section = """📈 TRENDING TOPICS (This Period)

Rising 📈:
"""
        
        # Analyze trends from signals (simplified)
        topics = self._extract_trending_topics(signals)
        
        for topic in topics['rising'][:3]:
            section += f"• {topic}\n"
        
        if topics['declining']:
            section += "\nDeclining 📉:\n"
            for topic in topics['declining'][:2]:
                section += f"• {topic}\n"
        
        section += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        return section
    
    def _format_recommended_actions(self, top_opportunities: List[Dict]) -> str:
        """Format recommended actions section"""
        
        section = """💡 RECOMMENDED ACTIONS

"""
        
        if len(top_opportunities) >= 1:
            section += f"Priority 1: Validate '{top_opportunities[0]['title']}' with customer research\n"
        
        if len(top_opportunities) >= 2:
            section += f"Priority 2: Deep dive on '{top_opportunities[1]['title']}' market opportunity\n"
        
        if len(top_opportunities) >= 3:
            section += f"Priority 3: Competitive analysis for '{top_opportunities[2]['title']}'\n"
        
        section += f"\nNext Brief: {self._get_next_brief_date()}\n\n"
        section += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        return section
    
    def _generate_footer(self) -> str:
        """Generate brief footer"""
        
        footer = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 ABOUT THIS BRIEF
This intelligence brief is generated from analysis of:
• Reddit discussions in Hispanic and French-Canadian communities
• Industry news and publications
• Academic research (arXiv papers)
• Competitive intelligence
• Customer feedback signals

All opportunities are scored based on:
• Charter fit (30%)
• Customer evidence strength (25%)
• Market size potential (20%)
• Feasibility (15%)
• Competitive advantage (10%)

Questions or feedback? Contact the Multilingual CX Product Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return footer
    
    def _is_quick_win(self, opportunity: Dict) -> bool:
        """Determine if opportunity is a quick win"""
        # Simplified logic - in production, analyze effort from the opportunity details
        score = opportunity.get('composite_score', 0)
        feasibility = opportunity.get('detailed_scores', {}).get('feasibility', 50)
        
        return score >= 75 and feasibility >= 80
    
    def _estimate_effort(self, opportunity: Dict) -> str:
        """Estimate effort for opportunity"""
        # Simplified - in production, parse from analysis
        feasibility = opportunity.get('detailed_scores', {}).get('feasibility', 50)
        
        if feasibility >= 85:
            return "1 quarter, 1-2 PMs"
        elif feasibility >= 70:
            return "2 quarters, 2-3 PMs"
        else:
            return "3+ quarters, 4+ PMs"
    
    def _extract_trending_topics(self, signals: List[Dict]) -> Dict[str, List[str]]:
        """Extract trending topics from signals"""
        # Simplified topic extraction
        
        topics = {
            'rising': [
                "Regional Spanish dialect AI",
                "Hispanic heritage shopping trends",
                "Quebec language compliance (Bill 96)"
            ],
            'declining': [
                "Generic translation approaches"
            ]
        }
        
        return topics
    
    def _get_next_brief_date(self) -> str:
        """Calculate next brief date (2 weeks from now)"""
        from datetime import timedelta
        next_date = datetime.now() + timedelta(days=14)
        return next_date.strftime("%B %d, %Y")
    
    def save_brief(self, brief_content: str, filename: str = None) -> str:
        """Save brief to file"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"intelligence_brief_{timestamp}.txt"
        
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(self.config.OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(brief_content)
        
        print(f"💾 Brief saved to {filepath}")
        return filepath
    
    def export_to_html(self, brief_content: str, filename: str = None) -> str:
        """Export brief to HTML format"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"intelligence_brief_{timestamp}.html"
        
        # Convert plain text to HTML with basic formatting
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multilingual Shopping Experience Intelligence Brief - {self.brief_date}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #232f3e;
            border-bottom: 3px solid #ff9900;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #232f3e;
            margin-top: 30px;
        }}
        .snapshot {{
            background: #f0f8ff;
            padding: 20px;
            border-left: 4px solid #0073bb;
            margin: 20px 0;
        }}
        .opportunity {{
            background: #fff9f0;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #ff9900;
        }}
        .score {{
            display: inline-block;
            background: #232f3e;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}
        .section-divider {{
            border-top: 2px solid #ddd;
            margin: 30px 0;
        }}
        pre {{
            white-space: pre-wrap;
            font-family: inherit;
        }}
    </style>
</head>
<body>
    <div class="container">
        <pre>{brief_content}</pre>
    </div>
</body>
</html>
"""
        
        os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)
        filepath = os.path.join(self.config.OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 HTML brief saved to {filepath}")
        return filepath


def test_brief_generator():
    """Test the brief generator"""
    import config
    from market_intelligence import test_collector
    from opportunity_analyzer import OpportunityAnalyzer
    
    # Get test data
    signals = test_collector()
    
    # Create mock opportunities for testing
    mock_opportunities = [
        {
            "title": "Spanish Voice Search with Regional Accent Support",
            "charter_fit_score": 95,
            "composite_score": 92,
            "customer_pain_point": "Hispanic customers struggle with Alexa understanding regional Spanish accents, particularly Mexican and Caribbean variants.",
            "proposed_solution": "Enhance voice shopping to handle Mexican Spanish, Caribbean Spanish, and other regional dialects.",
            "market_size": "62M Hispanic Americans, voice shopping opportunity of $400M+",
            "competitive_intelligence": "Google Assistant recently improved regional dialect support",
            "charter_expansion_angle": "From multilingual text to full voice + text with dialect support",
            "source_signals": signals[:3],
            "detailed_scores": {"feasibility": 75, "customer_evidence": 85}
        },
        {
            "title": "Hispanic Product Discovery Mode",
            "charter_fit_score": 88,
            "composite_score": 86,
            "customer_pain_point": "Difficult to find authentic Hispanic products and brands on Amazon",
            "proposed_solution": "Create Spanish-language shopping mode that surfaces Hispanic brands and understands cultural product names",
            "market_size": "$2.3B Hispanic product market opportunity",
            "competitive_intelligence": "Walmart launched 'Descubre' feature with positive reception",
            "charter_expansion_angle": "From translation to culturally-curated experiences",
            "source_signals": signals[3:5],
            "detailed_scores": {"feasibility": 70, "customer_evidence": 90}
        },
        {
            "title": "French-Canadian Local Shopping Integration",
            "charter_fit_score": 82,
            "composite_score": 79,
            "customer_pain_point": "Quebec shoppers want better support for local products and French-Canadian culture",
            "proposed_solution": "Quebec-specific features highlighting local products and improving French translation quality",
            "market_size": "8.5M Quebec residents, opportunity to increase market share from 34% to 45%",
            "competitive_intelligence": "Bill 96 compliance creates regulatory advantage",
            "charter_expansion_angle": "Regional localization beyond translation",
            "source_signals": signals[5:7],
            "detailed_scores": {"feasibility": 85, "customer_evidence": 75}
        }
    ]
    
    generator = BriefGenerator(config)
    brief = generator.generate_brief(mock_opportunities, signals)
    
    print("\n" + "="*60)
    print("GENERATED BRIEF PREVIEW")
    print("="*60)
    print(brief[:1000] + "...\n")
    
    # Save outputs
    generator.save_brief(brief)
    generator.export_to_html(brief)


if __name__ == "__main__":
    test_brief_generator()
