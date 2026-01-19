"""
IMPROVED Opportunity Analyzer Module
Fixed version with better prompts and JSON parsing for live data analysis
"""

import anthropic
import json
from typing import List, Dict, Any
from datetime import datetime
import re


class ImprovedOpportunityAnalyzer:
    """Analyzes market signals using Claude with structured JSON output"""
    
    def __init__(self, config, api_key: str = None):
        self.config = config
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set. Please provide API key.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.opportunities = []
    
    def analyze_signals(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze all signals and extract opportunities"""
        print(f"\n🤖 Analyzing {len(signals)} signals with Claude (improved prompts)...")
        
        if len(signals) == 0:
            print("⚠️  No signals to analyze")
            return []
        
        # Batch signals into manageable groups
        batch_size = 8
        all_opportunities = []
        
        for i in range(0, len(signals), batch_size):
            batch = signals[i:i+batch_size]
            print(f"  Processing batch {i//batch_size + 1} ({len(batch)} signals)...")
            
            batch_opps = self._analyze_batch_structured(batch)
            all_opportunities.extend(batch_opps)
            
            if batch_opps:
                print(f"    ✓ Found {len(batch_opps)} opportunities in this batch")
            else:
                print(f"    ⚠️  No opportunities found in this batch")
        
        # Deduplicate
        all_opportunities = self._deduplicate_opportunities(all_opportunities)
        
        # Score and rank
        all_opportunities = self._score_and_rank(all_opportunities, signals)
        
        self.opportunities = all_opportunities
        print(f"\n✅ Total unique opportunities identified: {len(all_opportunities)}")
        
        return all_opportunities
    
    def _analyze_batch_structured(self, signals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze a batch with structured JSON output"""
        
        # Format signals clearly
        signals_text = self._format_signals_for_analysis(signals)
        
        # Improved prompt that explicitly requests JSON
        prompt = f"""You are analyzing market signals for Amazon's Multilingual Customer Experience team focused on Hispanic (US Spanish) and French-Canadian shoppers.

ANALYZE THESE MARKET SIGNALS:

{signals_text}

TASK: Identify product/feature opportunities from these signals.

For EACH opportunity you identify, create a JSON object with these fields:
- title: Brief descriptive title (5-10 words)
- charter_fit_score: Score 0-100 (how well this fits Hispanic/French-Canadian CX charter)
- customer_pain_point: Specific customer problem described in the signals
- proposed_solution: What product/feature could address this
- market_size: Market size estimate with specific numbers if available
- competitive_intelligence: What competitors are doing related to this
- cultural_context: Cultural nuances relevant to this opportunity
- charter_expansion_angle: How this could expand the team's charter scope
- relevant_signal_indices: List of signal numbers (1-based) that support this

IMPORTANT:
- Look for patterns across multiple signals
- Be specific about customer pain points
- Quantify market opportunities when possible
- Only score 70+ if it DIRECTLY relates to Hispanic or French-Canadian shopping experience
- Respond with ONLY a JSON array, no other text

Example format:
[
  {{
    "title": "Spanish Voice Search with Regional Accents",
    "charter_fit_score": 95,
    "customer_pain_point": "Hispanic customers report Alexa doesn't understand Mexican/Caribbean Spanish accents",
    "proposed_solution": "Enhance voice shopping to handle regional Spanish dialects",
    "market_size": "62M Hispanic Americans, $400M+ voice shopping opportunity",
    "competitive_intelligence": "Google improved dialect recognition recently",
    "cultural_context": "Mexican Spanish differs significantly from European Spanish",
    "charter_expansion_angle": "From text-only to full voice+text multilingual experience",
    "relevant_signal_indices": [1, 2, 5]
  }}
]

Now analyze the signals and respond with JSON array:"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text.strip()
            
            # Parse JSON from response
            opportunities = self._extract_json_from_response(response_text)
            
            if not opportunities:
                print(f"    ⚠️  Could not parse opportunities from response")
                # Try alternative parsing
                opportunities = self._fallback_parse(response_text, signals)
            
            # Enrich with source signals
            for opp in opportunities:
                signal_indices = opp.get('relevant_signal_indices', [])
                opp['source_signals'] = [signals[i-1] for i in signal_indices if 0 < i <= len(signals)]
                
                if not opp['source_signals']:
                    # If no specific signals referenced, include all from batch
                    opp['source_signals'] = signals[:3]
                
                opp['analysis_date'] = datetime.now().isoformat()
            
            return opportunities
            
        except Exception as e:
            print(f"    ✗ Analysis error: {e}")
            return []
    
    def _extract_json_from_response(self, response_text: str) -> List[Dict]:
        """Extract JSON array from Claude's response"""
        
        # Try to find JSON array
        # Look for [ ... ] pattern
        json_match = re.search(r'\[\s*\{.*?\}\s*\]', response_text, re.DOTALL)
        
        if json_match:
            try:
                json_str = json_match.group()
                opportunities = json.loads(json_str)
                return opportunities if isinstance(opportunities, list) else [opportunities]
            except json.JSONDecodeError as e:
                print(f"    JSON parse error: {e}")
                # Try to fix common JSON issues
                json_str = json_match.group()
                # Remove trailing commas
                json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
                try:
                    opportunities = json.loads(json_str)
                    return opportunities if isinstance(opportunities, list) else [opportunities]
                except:
                    pass
        
        return []
    
    def _fallback_parse(self, response_text: str, signals: List[Dict]) -> List[Dict]:
        """Fallback parsing if JSON extraction fails"""
        
        # Look for structured text patterns
        opportunities = []
        
        # Try to extract title and score at minimum
        lines = response_text.split('\n')
        current_opp = {}
        
        for line in lines:
            line = line.strip()
            
            if 'title' in line.lower() and ':' in line:
                if current_opp and 'title' in current_opp:
                    opportunities.append(current_opp)
                current_opp = {'title': line.split(':', 1)[1].strip().strip('"')}
            
            elif 'charter_fit_score' in line.lower() or 'score' in line.lower():
                score_match = re.search(r'(\d+)', line)
                if score_match:
                    current_opp['charter_fit_score'] = int(score_match.group(1))
            
            elif 'pain_point' in line.lower() or 'customer' in line.lower():
                if ':' in line:
                    current_opp['customer_pain_point'] = line.split(':', 1)[1].strip()
            
            elif 'solution' in line.lower():
                if ':' in line:
                    current_opp['proposed_solution'] = line.split(':', 1)[1].strip()
        
        if current_opp and 'title' in current_opp:
            opportunities.append(current_opp)
        
        # Fill in missing fields with defaults
        for opp in opportunities:
            opp.setdefault('charter_fit_score', 75)
            opp.setdefault('customer_pain_point', 'Customer feedback indicates opportunity')
            opp.setdefault('proposed_solution', 'Solution to be developed')
            opp.setdefault('market_size', 'Market size to be determined')
            opp.setdefault('competitive_intelligence', 'Competitive analysis needed')
            opp.setdefault('cultural_context', 'Cultural context relevant')
            opp.setdefault('charter_expansion_angle', 'Expands charter scope')
            opp.setdefault('source_signals', signals[:3])
        
        return opportunities
    
    def _format_signals_for_analysis(self, signals: List[Dict[str, Any]]) -> str:
        """Format signals clearly for Claude"""
        formatted = []
        
        for i, signal in enumerate(signals, 1):
            formatted.append(f"""
Signal {i}:
Source: {signal['source']} ({signal.get('source_detail', 'N/A')})
Market: {signal.get('market', 'unknown')}
Title: {signal['title']}
Content: {signal['content'][:400]}
Date: {signal.get('date', 'N/A')}
URL: {signal.get('url', 'N/A')}
""")
        
        return "\n".join(formatted)
    
    def _deduplicate_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Remove duplicate opportunities"""
        unique = []
        seen_titles = set()
        
        for opp in opportunities:
            title_key = opp.get('title', '').lower().strip()[:50]
            if title_key and title_key not in seen_titles:
                unique.append(opp)
                seen_titles.add(title_key)
        
        return unique
    
    def _score_and_rank(self, opportunities: List[Dict], all_signals: List[Dict]) -> List[Dict]:
        """Score and rank opportunities"""
        
        for opp in opportunities:
            # Calculate composite score
            scores = {
                'charter_fit': opp.get('charter_fit_score', 50),
                'customer_evidence': self._score_customer_evidence(opp),
                'market_size': self._score_market_size(opp),
                'feasibility': 75,  # Default
                'competitive_advantage': 70  # Default
            }
            
            # Weighted composite
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
        opportunities.sort(key=lambda x: x.get('composite_score', 0), reverse=True)
        
        return opportunities
    
    def _score_customer_evidence(self, opportunity: Dict) -> int:
        """Score strength of customer evidence"""
        signals = opportunity.get('source_signals', [])
        
        if not signals:
            return 60
        
        # Consider number of signals and engagement
        num_signals = len(signals)
        total_engagement = 0
        
        for signal in signals:
            if 'engagement' in signal:
                total_engagement += signal['engagement'].get('score', 0)
        
        avg_engagement = total_engagement / num_signals if num_signals > 0 else 0
        
        # Score: base 50 + up to 30 for signals + up to 20 for engagement
        score = 50 + min(30, num_signals * 6) + min(20, avg_engagement / 20)
        
        return int(min(100, score))
    
    def _score_market_size(self, opportunity: Dict) -> int:
        """Score market size based on text analysis"""
        market_text = opportunity.get('market_size', '').lower()
        
        # Look for indicators
        if any(term in market_text for term in ['billion', '$b', 'bn']):
            return 95
        elif any(term in market_text for term in ['million', '$m', 'mn', '$100', '$200', '$300', '$400']):
            return 85
        elif any(term in market_text for term in ['large', 'significant', 'substantial']):
            return 75
        elif market_text:
            return 65
        else:
            return 55
    
    def save_opportunities(self, filename: str = "opportunities.json"):
        """Save opportunities to file"""
        import os
        os.makedirs(self.config.DATA_DIR, exist_ok=True)
        
        filepath = os.path.join(self.config.DATA_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.opportunities, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Opportunities saved to {filepath}")
        return filepath


def test_improved_analyzer():
    """Test the improved analyzer"""
    import config
    import os
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set")
        return
    
    # Load signals
    try:
        with open('market_data/market_signals.json', 'r') as f:
            signals = json.load(f)
    except FileNotFoundError:
        print("❌ No signals file found. Run market_intelligence.py first")
        return
    
    print(f"Testing improved analyzer with {len(signals)} signals...")
    
    analyzer = ImprovedOpportunityAnalyzer(config, api_key)
    opportunities = analyzer.analyze_signals(signals)
    
    print("\n" + "="*70)
    print("ANALYSIS RESULTS")
    print("="*70)
    
    if opportunities:
        print(f"\n✅ Successfully identified {len(opportunities)} opportunities!")
        
        for i, opp in enumerate(opportunities[:5], 1):
            print(f"\n{i}. {opp['title']}")
            print(f"   Charter Fit: {opp['charter_fit_score']}/100")
            print(f"   Composite Score: {opp.get('composite_score', 0)}/100")
            print(f"   Pain Point: {opp.get('customer_pain_point', 'N/A')[:100]}...")
        
        analyzer.save_opportunities()
    else:
        print("\n⚠️  No opportunities were identified")
        print("This might mean:")
        print("  - Signals don't relate strongly to Hispanic/French-Canadian markets")
        print("  - Charter fit threshold is too high")
        print("  - Claude is being conservative in scoring")


if __name__ == "__main__":
    test_improved_analyzer()
