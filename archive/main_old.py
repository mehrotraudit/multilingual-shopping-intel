"""
Main Orchestration Script
Runs the complete Multilingual Shopping Experience Opportunity Discovery System
"""

import os
import sys
from datetime import datetime
import argparse

import config
from market_intelligence import MarketIntelligenceCollector, CompetitorIntelligence
from opportunity_analyzer import OpportunityAnalyzer
from brief_generator import BriefGenerator


def main(api_key: str = None, dry_run: bool = False):
    """
    Main execution pipeline
    
    Args:
        api_key: Anthropic API key for Claude analysis
        dry_run: If True, use cached data instead of collecting new signals
    """
    
    print("=" * 70)
    print("MULTILINGUAL SHOPPING EXPERIENCE OPPORTUNITY DISCOVERY SYSTEM")
    print("=" * 70)
    print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target Markets: Hispanic US (Spanish) & French-Canadian")
    print("=" * 70)
    
    # Step 1: Collect Market Intelligence
    print("\n" + "▶" * 35)
    print("STEP 1: MARKET INTELLIGENCE COLLECTION")
    print("▶" * 35)
    
    if not dry_run:
        collector = MarketIntelligenceCollector(config)
        signals = collector.collect_all_signals()
        
        # Add competitor intelligence
        comp_intel = CompetitorIntelligence(config)
        competitor_signals = comp_intel.collect_competitor_signals()
        signals.extend(competitor_signals)
        print(f"✓ Added {len(competitor_signals)} competitor signals")
        
        # Save signals
        signals_file = collector.save_signals()
        
    else:
        print("📂 Using cached signals (dry run mode)")
        import json
        signals_file = os.path.join(config.DATA_DIR, "market_signals.json")
        
        if not os.path.exists(signals_file):
            print("❌ No cached signals found. Run without --dry-run first.")
            return
        
        with open(signals_file, 'r', encoding='utf-8') as f:
            signals = json.load(f)
        
        print(f"✓ Loaded {len(signals)} cached signals")
    
    # Step 2: Analyze Opportunities with Claude
    print("\n" + "▶" * 35)
    print("STEP 2: OPPORTUNITY ANALYSIS (Claude API)")
    print("▶" * 35)
    
    if not api_key:
        api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("\n⚠️  WARNING: No API key provided.")
        print("Set ANTHROPIC_API_KEY environment variable or pass --api-key")
        print("Using mock opportunities for demonstration...")
        
        # Use mock opportunities for demo
        opportunities = create_mock_opportunities(signals)
    else:
        try:
            analyzer = OpportunityAnalyzer(config, api_key)
            opportunities = analyzer.analyze_signals(signals)
            
            # Generate strategic memos for top opportunities
            memos = analyzer.generate_strategic_memos(top_n=3)
            
            # Save opportunities
            analyzer.save_opportunities()
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            print("Using mock opportunities for demonstration...")
            opportunities = create_mock_opportunities(signals)
    
    # Step 3: Generate Intelligence Brief
    print("\n" + "▶" * 35)
    print("STEP 3: INTELLIGENCE BRIEF GENERATION")
    print("▶" * 35)
    
    generator = BriefGenerator(config)
    brief = generator.generate_brief(opportunities, signals)
    
    # Save outputs
    text_file = generator.save_brief(brief)
    html_file = generator.export_to_html(brief)
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETE")
    print("=" * 70)
    print(f"Signals Analyzed: {len(signals)}")
    print(f"Opportunities Found: {len(opportunities)}")
    print(f"High Priority (85+): {len([o for o in opportunities if o['composite_score'] >= 85])}")
    print("\nOutput Files:")
    print(f"  📄 {text_file}")
    print(f"  🌐 {html_file}")
    print("\nNext Steps:")
    print("  1. Review the intelligence brief")
    print("  2. Share with product leadership")
    print("  3. Schedule deep-dive sessions on top opportunities")
    print("=" * 70)
    
    return brief, opportunities


def create_mock_opportunities(signals):
    """Create mock opportunities for demonstration when API key is not available"""
    
    mock_opportunities = [
        {
            "title": "Spanish Voice Search with Regional Accent Support",
            "charter_fit_score": 95,
            "composite_score": 92,
            "customer_pain_point": "Hispanic customers report frustration with Alexa not understanding regional Spanish accents (Mexican, Puerto Rican, Colombian). Multiple Reddit threads cite having to switch to English for voice shopping.",
            "proposed_solution": "Enhance Rufus/Alexa voice shopping to handle: (1) Mexican Spanish (60% of US Hispanic population), (2) Caribbean Spanish variants (Puerto Rican, Cuban - 15%), (3) Central American dialects. Partner with Alexa team for regional training data.",
            "market_size": "62M Hispanic Americans, 38M Spanish speakers at home. Voice shopping penetration could grow from 24% to 45% with better accent support. Revenue opportunity: $400M+ annually.",
            "competitive_intelligence": "Google Assistant recently improved regional Spanish dialect recognition and receiving positive customer feedback. Opportunity to differentiate and capture voice shopping market share.",
            "cultural_context": "Mexican Spanish has significantly different pronunciation, vocabulary, and expressions than European Spanish. Caribbean Spanish has unique characteristics. One-size-fits-all approach alienates largest customer segment.",
            "charter_expansion_angle": "From: 'Multilingual text experience' To: 'Full multilingual voice + text experience with dialect support'. Positions team as experts in culturally-aware AI.",
            "source_signals": [s for s in signals if 'spanish' in s.get('content', '').lower() or 'alexa' in s.get('content', '').lower()][:5],
            "detailed_scores": {
                "charter_fit": 95,
                "customer_evidence": 85,
                "market_size": 90,
                "feasibility": 75,
                "competitive_advantage": 88
            }
        },
        {
            "title": "Hispanic Product Discovery - 'Encuentra en Español' Mode",
            "charter_fit_score": 88,
            "composite_score": 86,
            "customer_pain_point": "Hispanic customers struggle to find authentic products from their home countries. Reviews mention 'hard to find authentic Mexican products' repeatedly. Searches for cultural products don't surface relevant results.",
            "proposed_solution": "Create Spanish-language shopping mode that: (1) Surfaces Hispanic brands prominently, (2) Understands cultural product names ('piloncillo' not just 'brown sugar'), (3) Curates for Hispanic holidays (Día de los Muertos, Quinceañera), (4) Partners with Hispanic brands for discovery.",
            "market_size": "$2.3B Hispanic product market on Amazon currently underserved. Hispanic Heritage Month drives 3x searches for 'productos latinos'. Untapped revenue opportunity.",
            "competitive_intelligence": "Walmart launched 'Descubre' feature highlighting Hispanic products, receiving positive press and customer response. Amazon currently behind in cultural curation.",
            "cultural_context": "Hispanic shoppers seek authentic brands and products that connect them to their heritage. Generic translation isn't enough - need cultural understanding of what products matter.",
            "charter_expansion_angle": "From: 'Translation of existing experience' To: 'Culturally-curated shopping experiences'. Establishes Amazon as understanding Hispanic culture, not just language.",
            "source_signals": [s for s in signals if 'product' in s.get('content', '').lower() or 'mexican' in s.get('content', '').lower()][:5],
            "detailed_scores": {
                "charter_fit": 88,
                "customer_evidence": 90,
                "market_size": 85,
                "feasibility": 70,
                "competitive_advantage": 82
            }
        },
        {
            "title": "French-Canadian 'Achat Local' Integration",
            "charter_fit_score": 82,
            "composite_score": 79,
            "customer_pain_point": "Quebec customers complain about poor French translation quality (France French vs. Quebec French). Strong 'buy local' movement (#AchatLocal) not supported. Bill 96 creating pressure for better French compliance.",
            "proposed_solution": "Quebec-specific features: (1) Highlight Quebec-made products ('Fait au Québec'), (2) Improve French-Canadian translation (not France French), (3) Support local Quebec sellers more prominently, (4) Quebec holiday shopping (Saint-Jean-Baptiste, Sugar Shack season).",
            "market_size": "8.5M Quebecers, 85% speak French primarily. Quebec e-commerce: $15B annually. Amazon.ca market share 34% - could reach 45% with better localized experience.",
            "competitive_intelligence": "No major player has solved this well. Bill 96 compliance could position Amazon favorably. Regulatory bonus on top of customer experience improvement.",
            "cultural_context": "Quebec has distinct culture and strong local pride. 'Achat local' movement significant. Quebec French differs substantially from France French in vocabulary and expressions.",
            "charter_expansion_angle": "From: 'Translation service' To: 'Regional localization with cultural understanding'. Opens opportunities for other Canadian francophone markets.",
            "source_signals": [s for s in signals if 'quebec' in s.get('content', '').lower() or 'french' in s.get('content', '').lower()][:5],
            "detailed_scores": {
                "charter_fit": 82,
                "customer_evidence": 75,
                "market_size": 80,
                "feasibility": 85,
                "competitive_advantage": 78
            }
        },
        {
            "title": "Hispanic Holiday Calendar Integration (Quick Win)",
            "charter_fit_score": 78,
            "composite_score": 76,
            "customer_pain_point": "Rufus doesn't suggest appropriate gifts for Hispanic holidays. Customers manually search for Quinceañera gifts, Día de los Muertos supplies without AI assistance.",
            "proposed_solution": "Integrate Hispanic holiday calendar into Rufus so it proactively suggests: Quinceañera gifts (dresses, decorations), Día de los Muertos supplies (altar items, marigolds, sugar skulls), Three Kings Day gifts, etc.",
            "market_size": "Hispanic Heritage Month alone drives significant shopping spikes. Year-round cultural event shopping opportunity.",
            "competitive_intelligence": "No major competitor has cultural holiday intelligence built in. Clear differentiation opportunity.",
            "cultural_context": "Hispanic holidays are major shopping occasions but different from mainstream US calendar. Quinceañeras are huge cultural milestone celebrations.",
            "charter_expansion_angle": "From: 'Generic recommendations' To: 'Culturally-aware shopping assistant'.",
            "source_signals": [s for s in signals if 'holiday' in s.get('content', '').lower()][:3],
            "detailed_scores": {
                "charter_fit": 78,
                "customer_evidence": 70,
                "market_size": 75,
                "feasibility": 90,
                "competitive_advantage": 72
            }
        },
        {
            "title": "Spanglish Search Support (Quick Win)",
            "charter_fit_score": 75,
            "composite_score": 74,
            "customer_pain_point": "Bilingual customers naturally mix Spanish and English when searching ('quiero un phone case rojo') but Amazon search doesn't handle code-switching well.",
            "proposed_solution": "Enhance search to handle mixed Spanish/English queries. Understand that bilingual customers code-switch naturally and shouldn't be forced to choose one language.",
            "market_size": "Millions of bilingual Hispanic Americans who naturally code-switch. Improved search conversion opportunity.",
            "competitive_intelligence": "Google handles Spanglish queries better than Amazon. Search quality gap to close.",
            "cultural_context": "Code-switching (Spanglish) is natural linguistic behavior for bilingual speakers, not confusion. Should be supported, not penalized.",
            "charter_expansion_angle": "From: 'Monolingual experiences' To: 'Truly bilingual experience that respects code-switching'.",
            "source_signals": [s for s in signals if 'spanglish' in s.get('content', '').lower()][:3],
            "detailed_scores": {
                "charter_fit": 75,
                "customer_evidence": 78,
                "market_size": 72,
                "feasibility": 88,
                "competitive_advantage": 70
            }
        }
    ]
    
    return mock_opportunities


def run_scheduled():
    """Run as scheduled task (called by GitHub Actions or cron)"""
    
    # Check if it's bi-weekly (every other week)
    import datetime
    week_number = datetime.date.today().isocalendar()[1]
    
    if week_number % 2 != 0:  # Only run on even weeks
        print("Skipping: Not a bi-weekly run week")
        return
    
    main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multilingual Shopping Experience Opportunity Discovery System"
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use cached signals instead of collecting new ones"
    )
    parser.add_argument(
        "--scheduled",
        action="store_true",
        help="Run as scheduled task (bi-weekly check)"
    )
    
    args = parser.parse_args()
    
    if args.scheduled:
        run_scheduled()
    else:
        main(api_key=args.api_key, dry_run=args.dry_run)
