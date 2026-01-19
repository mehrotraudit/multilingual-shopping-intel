#!/usr/bin/env python3
"""
Quick Test Script for Improved Real-Time Analysis
Tests the improved analyzer with your existing signals
"""

import os
import json

# Check if API key is set
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("=" * 70)
    print("❌ ANTHROPIC_API_KEY NOT SET")
    print("=" * 70)
    print("\nPlease set your API key:")
    print("  export ANTHROPIC_API_KEY='sk-ant-your-key-here'")
    print("\nThen run this script again:")
    print("  python3 test_improved_analysis.py")
    print("=" * 70)
    exit(1)

print("=" * 70)
print("TESTING IMPROVED REAL-TIME ANALYSIS")
print("=" * 70)

# Check for signals file
if not os.path.exists('market_data/market_signals.json'):
    print("\n⚠️  No signals file found.")
    print("Running market intelligence collection first...\n")
    
    import config
    from market_intelligence import MarketIntelligenceCollector
    
    collector = MarketIntelligenceCollector(config)
    signals = collector.collect_all_signals()
    collector.save_signals()
else:
    print("\n✓ Found existing signals file")
    with open('market_data/market_signals.json', 'r') as f:
        signals = json.load(f)
    print(f"✓ Loaded {len(signals)} signals")

# Now test improved analyzer
print("\n" + "-" * 70)
print("RUNNING IMPROVED ANALYZER")
print("-" * 70)

import config
from opportunity_analyzer_improved import ImprovedOpportunityAnalyzer

analyzer = ImprovedOpportunityAnalyzer(config, api_key)
opportunities = analyzer.analyze_signals(signals)

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

if opportunities:
    print(f"\n✅ SUCCESS! Found {len(opportunities)} opportunities\n")
    
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp['title']}")
        print(f"   Charter Fit: {opp.get('charter_fit_score', 0)}/100")
        print(f"   Composite: {opp.get('composite_score', 0)}/100")
        print(f"   Pain Point: {opp.get('customer_pain_point', 'N/A')[:80]}...")
        print()
    
    analyzer.save_opportunities()
    
    print("=" * 70)
    print("✅ IMPROVED ANALYSIS WORKING!")
    print("=" * 70)
    print("\nNow you can run the full pipeline:")
    print("  python3 main_improved.py")
    print("\nThis will generate a complete intelligence brief with your")
    print("real-time analyzed opportunities!")
    print("=" * 70)
    
else:
    print("\n⚠️  No opportunities found")
    print("\nThis could mean:")
    print("  1. Signals aren't strongly related to Hispanic/French markets")
    print("  2. Claude is being conservative with scoring")
    print("  3. Charter fit threshold needs adjustment")
    print("\nYou can still run the full pipeline with mock data:")
    print("  python3 main_improved.py")
    print("=" * 70)
