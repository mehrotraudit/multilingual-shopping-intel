"""
Opportunity Analyzer Module
Uses Claude API to analyze market signals and identify product/feature opportunities
"""

import anthropic
import json
from typing import List, Dict, Any
from datetime import datetime


class OpportunityAnalyzer:
    """Analyzes market signals using Claude to identify opportunities"""
    
    def __init__(self, config, api_key: str = None):
        self.config = config
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set. Please provide API key.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.opportunities = []
    
    def analyze_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze all signals and extract opportunities"""
        print(f"\n🤖 Analyzing {len(signals)} signals with Claude...")
        
        opportunities = []
        
        # Group signals by similarity for batch analysis
        signal_batches = self._batch_signals(signals)
        
        for i, batch in enumerate(signal_batches, 1):
            print(f"  Processing batch {i}/{len(signal_batches)}...")
            
            batch_opportunities = self._analyze_batch(batch)
            opportunities.extend(batch_opportunities)
        
        # Deduplicate and merge similar opportunities
        opportunities = self._deduplicate_opportunities(opportunities)
        
        # Score and rank opportunities
        opportunities = self._score_opportunities(opportunities)
        
        self.opportunities = opportunities
        print(f"✓ Identified {len(opportunities)} unique opportunities")
        
        return opportunities
    
    def _analyze_batch(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze a batch of related signals"""
        
        # Prepare content for analysis
        batch_content = self._format_signals_for_analysis(signals)
        
        prompt = self.config.ANALYSIS_PROMPTS['opportunity_extraction'].format(
            content=batch_content,
            source=signals[0]['source'] if signals else "Multiple",
            date=datetime.now().strftime("%Y-%m-%d")
        )
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis = response.content[0].text
            
            # Parse the analysis into structured opportunities
            opportunities = self._parse_analysis(analysis, signals)
            
            return opportunities
            
        except Exception as e:
            print(f"  ✗ Analysis failed: {e}")
            return []
    
    def _format_signals_for_analysis(self, signals: List[Dict[str, Any]]) -> str:
        """Format signals into text for Claude analysis"""
        formatted = []
        
        for i, signal in enumerate(signals, 1):
            formatted.append(f"""
Signal {i}:
Title: {signal['title']}
Source: {signal['source']} - {signal.get('source_detail', 'N/A')}
Market: {signal['market']}
Content: {signal['content'][:400]}
URL: {signal['url']}
Date: {signal['date']}
""")
        
        return "\n".join(formatted)
    
    def _parse_analysis(self, analysis: str, source_signals: List[Dict]) -> List[Dict[str, Any]]:
        """Parse Claude's analysis into structured opportunities"""
        
        # Simple parsing logic - in production, use more structured output
        opportunities = []
        
        # Look for key sections in the analysis
        lines = analysis.split('\n')
        
        opportunity = {
            "title": "",
            "charter_fit_score": 0,
            "customer_pain_point": "",
            "proposed_solution": "",
            "market_size": "",
            "competitive_intelligence": "",
            "cultural_context": "",
            "charter_expansion_angle": "",
            "source_signals": source_signals,
            "analysis_date": datetime.now().isoformat()
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detect sections
            if "RELEVANCE" in line or "CHARTER FIT" in line:
                # Extract score
                import re
                match = re.search(r'(\d+)', line)
                if match:
                    opportunity['charter_fit_score'] = int(match.group(1))
            
            elif "CUSTOMER PAIN POINT" in line:
                current_section = "pain_point"
            elif "OPPORTUNITY" in line and "MARKET SIZE" not in line:
                current_section = "solution"
            elif "MARKET SIZE" in line:
                current_section = "market_size"
            elif "COMPETITIVE INTELLIGENCE" in line:
                current_section = "competitive"
            elif "CULTURAL CONTEXT" in line:
                current_section = "cultural"
            elif "CHARTER EXPANSION" in line:
                current_section = "charter_expansion"
            
            # Collect content
            elif line and current_section:
                if current_section == "pain_point":
                    opportunity['customer_pain_point'] += line + " "
                elif current_section == "solution":
                    opportunity['proposed_solution'] += line + " "
                elif current_section == "market_size":
                    opportunity['market_size'] += line + " "
                elif current_section == "competitive":
                    opportunity['competitive_intelligence'] += line + " "
                elif current_section == "cultural":
                    opportunity['cultural_context'] += line + " "
                elif current_section == "charter_expansion":
                    opportunity['charter_expansion_angle'] += line + " "
        
        # Generate title if not set
        if not opportunity['title'] and opportunity['proposed_solution']:
            opportunity['title'] = opportunity['proposed_solution'].split('.')[0][:100]
        
        # Only include if relevant
        if opportunity['charter_fit_score'] >= self.config.CHARTER_FIT_THRESHOLD:
            opportunities.append(opportunity)
        
        return opportunities
    
    def _batch_signals(self, signals: List[Dict[str, Any]], batch_size: int = 5) -> List[List[Dict]]:
        """Group signals into batches for analysis"""
        batches = []
        
        for i in range(0, len(signals), batch_size):
            batches.append(signals[i:i+batch_size])
        
        return batches
    
    def _deduplicate_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Remove duplicate opportunities"""
        # Simple deduplication by title similarity
        # In production, use more sophisticated NLP similarity
        
        unique = []
        seen_titles = set()
        
        for opp in opportunities:
            title_key = opp['title'].lower()[:50]
            if title_key not in seen_titles:
                unique.append(opp)
                seen_titles.add(title_key)
        
        return unique
    
    def _score_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Score and rank opportunities"""
        
        for opp in opportunities:
            # Calculate composite score based on criteria
            scores = {
                'charter_fit': opp.get('charter_fit_score', 50),
                'customer_evidence': self._score_customer_evidence(opp),
                'market_size': self._score_market_size(opp),
                'feasibility': 75,  # Default, would be estimated from analysis
                'competitive_advantage': 70  # Default
            }
            
            # Weighted composite score
            criteria = self.config.SCORING_CRITERIA
            composite_score = (
                scores['charter_fit'] * criteria['charter_fit']['weight'] +
                scores['customer_evidence'] * criteria['customer_evidence']['weight'] +
                scores['market_size'] * criteria['market_size']['weight'] +
                scores['feasibility'] * criteria['feasibility']['weight'] +
                scores['competitive_advantage'] * criteria['competitive_advantage']['weight']
            )
            
            opp['composite_score'] = round(composite_score, 1)
            opp['detailed_scores'] = scores
        
        # Sort by composite score
        opportunities.sort(key=lambda x: x['composite_score'], reverse=True)
        
        return opportunities
    
    def _score_customer_evidence(self, opportunity: Dict) -> int:
        """Score strength of customer evidence"""
        signals = opportunity.get('source_signals', [])
        
        if not signals:
            return 50
        
        # Consider number of signals and engagement
        num_signals = len(signals)
        avg_engagement = 0
        
        for signal in signals:
            if 'engagement' in signal:
                avg_engagement += signal['engagement'].get('score', 0)
        
        if num_signals > 0:
            avg_engagement /= num_signals
        
        # Score based on quantity and engagement
        score = min(100, 50 + (num_signals * 5) + (avg_engagement / 10))
        
        return int(score)
    
    def _score_market_size(self, opportunity: Dict) -> int:
        """Estimate market size score"""
        market_text = opportunity.get('market_size', '').lower()
        
        # Look for revenue/user indicators
        if 'billion' in market_text or '$' in market_text and ('b' in market_text or 'bn' in market_text):
            return 95
        elif 'million' in market_text or '$' in market_text and ('m' in market_text or 'mn' in market_text):
            return 85
        elif 'large' in market_text or 'significant' in market_text:
            return 75
        else:
            return 60
    
    def generate_strategic_memos(self, top_n: int = 3) -> List[Dict]:
        """Generate strategic memos for top opportunities"""
        print(f"\n📝 Generating strategic memos for top {top_n} opportunities...")
        
        memos = []
        
        for i, opp in enumerate(self.opportunities[:top_n], 1):
            print(f"  Creating memo {i}/{top_n}...")
            
            memo = self._create_memo(opp)
            memos.append(memo)
        
        return memos
    
    def _create_memo(self, opportunity: Dict) -> Dict:
        """Create a strategic memo for an opportunity"""
        
        evidence = "\n".join([
            f"- {s['title']}" for s in opportunity.get('source_signals', [])[:5]
        ])
        
        prompt = self.config.ANALYSIS_PROMPTS['strategic_memo'].format(
            opportunity_title=opportunity['title'],
            market=opportunity.get('source_signals', [{}])[0].get('market', 'Multiple markets'),
            evidence=evidence
        )
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            memo_text = response.content[0].text
            
            return {
                "opportunity": opportunity,
                "memo": memo_text
            }
            
        except Exception as e:
            print(f"  ✗ Memo generation failed: {e}")
            return {
                "opportunity": opportunity,
                "memo": "Memo generation failed"
            }
    
    def save_opportunities(self, filename: str = "opportunities.json"):
        """Save opportunities to file"""
        import os
        os.makedirs(self.config.DATA_DIR, exist_ok=True)
        
        filepath = os.path.join(self.config.DATA_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.opportunities, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Opportunities saved to {filepath}")
        return filepath


def test_analyzer():
    """Test the opportunity analyzer"""
    import config
    from market_intelligence import test_collector
    
    # Get some test signals
    signals = test_collector()
    
    # Analyze with Claude (requires API key)
    try:
        analyzer = OpportunityAnalyzer(config)
        opportunities = analyzer.analyze_signals(signals[:10])  # Limit for testing
        
        print("\n" + "="*60)
        print("TOP OPPORTUNITIES")
        print("="*60)
        
        for i, opp in enumerate(opportunities[:3], 1):
            print(f"\n{i}. {opp['title']}")
            print(f"   Charter Fit: {opp['charter_fit_score']}/100")
            print(f"   Composite Score: {opp['composite_score']}/100")
            print(f"   Pain Point: {opp['customer_pain_point'][:150]}...")
        
        analyzer.save_opportunities()
        
    except ValueError as e:
        print(f"\n⚠️  {e}")
        print("Set ANTHROPIC_API_KEY environment variable to test analysis")


if __name__ == "__main__":
    test_analyzer()
