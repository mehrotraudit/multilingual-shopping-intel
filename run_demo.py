"""
Demo script with rich mock data to show full system capabilities
Run this to see what the intelligence brief looks like when fully populated
"""

import config
from brief_generator import BriefGenerator
from datetime import datetime

# Create rich mock opportunities
mock_opportunities = [
    {
        "title": "Spanish Voice Search with Regional Accent Support",
        "charter_fit_score": 95,
        "composite_score": 92,
        "customer_pain_point": "Hispanic customers report frustration with Alexa not understanding regional Spanish accents (Mexican, Puerto Rican, Colombian). Multiple Reddit threads cite having to switch to English for voice shopping. Quote from Reddit user in Miami: 'I have to switch to English when talking to Alexa about shopping because she doesn't understand my Colombian accent.'",
        "proposed_solution": "Enhance Rufus/Alexa voice shopping to handle: (1) Mexican Spanish (60% of US Hispanic population), (2) Caribbean Spanish variants (Puerto Rican, Cuban - 15%), (3) Central American dialects. Partner with Alexa team for regional training data. Test with focus groups in LA, Miami, and Houston. Implement regional dialect detection layer.",
        "market_size": "62M Hispanic Americans, 38M Spanish speakers at home. Voice shopping penetration could grow from 24% to 45% with better accent support. Revenue opportunity: $400M+ annually based on increased voice commerce adoption and reduced English-switching friction.",
        "competitive_intelligence": "Google Assistant recently improved regional Spanish dialect recognition and receiving positive customer feedback on social media. Walmart has not addressed this gap in their voice shopping. Opportunity to differentiate and capture voice shopping market share in Hispanic segment before competitors catch up.",
        "cultural_context": "Mexican Spanish has significantly different pronunciation, vocabulary, and expressions than European Spanish (e.g., 'computadora' vs 'ordenador'). Caribbean Spanish has unique characteristics with different rhythm and dropped consonants. One-size-fits-all approach alienates largest customer segment. Regional pride is strong - Mexican Americans don't want to sound like they're from Madrid.",
        "charter_expansion_angle": "From: 'Multilingual text experience' To: 'Full multilingual voice + text experience with dialect support'. Positions team as THE experts in culturally-aware AI and voice commerce. Opens door to lead all voice internationalization efforts across Amazon. Establishes precedent for regional dialect handling (could extend to Indian English, UK vs US English, etc.).",
        "source_signals": [
            {"title": "Alexa doesn't understand Mexican Spanish", "source": "reddit", "market": "hispanic_us", "url": "https://reddit.com/r/latino/example1"},
            {"title": "Voice shopping fails for Colombian accent", "source": "reddit", "market": "hispanic_us", "url": "https://reddit.com/r/latino/example2"},
            {"title": "Google improves dialect recognition", "source": "competitor", "market": "hispanic_us", "url": "https://blog.google/example"}
        ],
        "detailed_scores": {
            "charter_fit": 95,
            "customer_evidence": 88,
            "market_size": 92,
            "feasibility": 75,
            "competitive_advantage": 85
        }
    },
    {
        "title": "Hispanic Product Discovery - 'Encuentra en Español' Mode",
        "charter_fit_score": 88,
        "composite_score": 86,
        "customer_pain_point": "Hispanic customers struggle to find authentic products from their home countries. Amazon reviews in Spanish mention 'hard to find authentic Mexican products' 47+ times in past month. Searches for cultural products like 'piloncillo' (Mexican unrefined sugar), 'queso fresco', or 'masa harina' don't surface relevant results well. Generic search treats these as unfamiliar terms rather than specific products.",
        "proposed_solution": "Create Spanish-language shopping mode called 'Encuentra en Español' that: (1) Surfaces Hispanic brands prominently (Goya, La Costeña, Bimbo, etc.), (2) Understands cultural product names ('piloncillo' not just 'brown sugar', 'quinceañera dress' not 'formal gown'), (3) Curates collections for Hispanic holidays (Día de los Muertos altar supplies, Three Kings Day gifts, Quinceañera party supplies), (4) Partners with Hispanic brands for better product data and exclusive offerings. Implement cultural product taxonomy.",
        "market_size": "$2.3B Hispanic product market on Amazon currently underserved. Hispanic Heritage Month drives 3x spike in searches for 'productos latinos' but conversion lags due to poor discovery. Year-round opportunity as Hispanic consumers seek authentic products. Market research shows 67% of Hispanic shoppers prefer buying from brands that understand their culture. Average basket size 18% higher when cultural products included.",
        "competitive_intelligence": "Walmart launched 'Descubre' feature in 2024 highlighting Hispanic products and cultural collections - receiving very positive press coverage in Hispanic media and customer response on social media. Target has 'Más Que' program featuring Hispanic-owned brands. Amazon currently behind in cultural curation and losing market share in Hispanic grocery/specialty items to these competitors. Window of opportunity closing.",
        "cultural_context": "Hispanic shoppers actively seek authentic brands and products that connect them to their heritage - not just translations. Product names carry cultural meaning: 'piloncillo' evokes the cone-shaped Mexican sugar loaf used in traditional recipes, while 'brown sugar' doesn't capture this. Holidays like Día de los Muertos (altar offerings, marigolds, sugar skulls) and Quinceañeras (elaborate 15th birthday celebrations) are massive shopping occasions with specific product needs that generic search doesn't understand.",
        "charter_expansion_angle": "From: 'Translation of existing experience' To: 'Culturally-curated shopping experiences'. Establishes Amazon as understanding Hispanic culture, not just language. Creates blueprint that could extend to other cultural shopping experiences (Lunar New Year for Asian customers, Diwali for Indian customers, Ramadan for Muslim customers). Positions team to own all cultural commerce initiatives.",
        "source_signals": [
            {"title": "Can't find authentic Mexican products on Amazon", "source": "reddit", "market": "hispanic_us", "url": "https://reddit.com/r/mexico/example3"},
            {"title": "Walmart Descubre feature getting positive response", "source": "competitor", "market": "hispanic_us", "url": "https://corporate.walmart.com/example"},
            {"title": "Hispanic shoppers want cultural products", "source": "industry", "market": "hispanic_us", "url": "https://portada-online.com/example"}
        ],
        "detailed_scores": {
            "charter_fit": 88,
            "customer_evidence": 90,
            "market_size": 85,
            "feasibility": 72,
            "competitive_advantage": 80
        }
    },
    {
        "title": "French-Canadian 'Achat Local' Integration",
        "charter_fit_score": 82,
        "composite_score": 80,
        "customer_pain_point": "Quebec customers complain about poor French translation quality on Amazon.ca - it's clearly France French, not Quebec French, with awkward expressions that don't match how Quebecers actually speak. Strong 'Achat Local' (buy local) movement in Quebec not supported by Amazon's platform. Bill 96 enforcement creating regulatory pressure for better French compliance. Multiple Reddit threads about Amazon.ca's 'terrible French' and lack of local product visibility.",
        "proposed_solution": "Quebec-specific features: (1) Highlight Quebec-made products with 'Fait au Québec' badges and dedicated collections, (2) Improve French-Canadian translation quality (hire Quebec translators, not just France French speakers - different vocabulary like 'magasiner' vs 'faire du shopping'), (3) Support local Quebec sellers more prominently in search results and recommendations, (4) Quebec holiday shopping guides (Saint-Jean-Baptiste party supplies, Sugar Shack season maple products), (5) Partner with Quebec brands, artisans, and local businesses.",
        "market_size": "8.5M Quebecers, 85% speak French primarily. Quebec e-commerce market: $15B annually and growing 12% per year. Amazon.ca currently has 34% market share in Quebec - could reach 45%+ with better localized experience (represents $1.6B+ additional revenue). Bill 96 compliance also opens B2B opportunities as Quebec businesses increasingly need compliant suppliers. Government procurement opportunities.",
        "competitive_intelligence": "No major e-commerce player has solved Quebec localization well yet - clear first-mover advantage. Shopify has better French but lacks Amazon's inventory and logistics. Local Quebec platforms (like Panier Bleu) exist but are fragmented with poor selection. Bill 96 compliance could position Amazon favorably vs. US competitors who ignore Quebec market nuances. Regulatory advantage over non-compliant competitors.",
        "cultural_context": "Quebec has very distinct culture and strong local pride - not just 'French Canada'. 'Achat Local' movement is significant - people actively seek and prefer Quebec-made products, especially post-pandemic. Quebec French differs substantially from France French in vocabulary ('magasiner' vs 'faire du shopping', 'courriel' vs 'email'), pronunciation, and cultural references. Using France French is like using British English for Americans - technically understandable but feels foreign. Bill 96 requires businesses operating in Quebec to operate primarily in French with quality standards.",
        "charter_expansion_angle": "From: 'Translation service' To: 'Regional localization with deep cultural understanding'. Opens opportunities for other Canadian francophone markets (New Brunswick Acadians, Ontario francophone communities) and demonstrates capability for regional adaptations globally (e.g., Swiss vs German vs Austrian German). Creates framework for 'hyper-local' commerce experiences.",
        "source_signals": [
            {"title": "Amazon.ca French translation is terrible", "source": "reddit", "market": "french_canadian", "url": "https://reddit.com/r/quebec/example2"},
            {"title": "Bill 96 compliance pressure on e-commerce", "source": "reddit", "market": "french_canadian", "url": "https://reddit.com/r/quebec/example4"},
            {"title": "Shopify improves French-Canadian localization", "source": "competitor", "market": "french_canadian", "url": "https://www.shopify.com/blog/example"}
        ],
        "detailed_scores": {
            "charter_fit": 82,
            "customer_evidence": 78,
            "market_size": 81,
            "feasibility": 85,
            "competitive_advantage": 76
        }
    },
    {
        "title": "Hispanic Holiday Calendar Integration",
        "charter_fit_score": 78,
        "composite_score": 77,
        "customer_pain_point": "Rufus and Alexa don't suggest appropriate gifts or products for major Hispanic holidays. Customers manually search for Quinceañera gifts (dresses, decorations, invitations, party favors), Día de los Muertos supplies (altar items, marigolds, sugar skulls, papel picado, traditional foods), Three Kings Day gifts (January 6th, when many Hispanic families exchange gifts instead of Christmas) without any AI shopping assistance. These are massive shopping occasions being completely missed by recommendation engines.",
        "proposed_solution": "Integrate Hispanic holiday calendar into Rufus so it proactively suggests culturally-appropriate items: Quinceañera planning support (January-August peak season), Día de los Muertos altar supplies and decorations (October), Three Kings Day gift suggestions (late December/early January), Cinco de Mayo party supplies (April-May), Las Posadas items (December pre-Christmas tradition). Train Rufus on cultural context and significance of each holiday. Create curated collections and shopping guides.",
        "market_size": "Hispanic Heritage Month alone drives 3x search volume spike for 'productos latinos' on Amazon. Quinceañeras: 500K+ celebrated annually in US, average family spending $10-15K per event on venue, dress, decorations, gifts, party supplies. Día de los Muertos rapidly growing beyond traditional Mexican-American communities - mainstream adoption increasing. Three Kings Day represents $800M+ in gift spending. Year-round cultural event shopping opportunity worth $2B+ annually.",
        "competitive_intelligence": "No major competitor has cultural holiday intelligence built into their AI shopping assistants. Pinterest has some cultural holiday boards but not commerce-integrated. Target has some Hispanic Heritage Month merchandising but not personalized/AI-driven. Clear differentiation opportunity with relatively low effort required - mostly knowledge engineering and content curation.",
        "cultural_context": "Quinceañeras are huge cultural milestone celebrations marking a girl's 15th birthday transition to young womanhood - requiring elaborate dresses, church ceremony, reception, court of honor, gifts. Second only to weddings in cultural importance and spending. Día de los Muertos (Day of the Dead) is major holiday honoring deceased family members, requiring specific items for home altars (ofrendas): marigolds, sugar skulls, pan de muerto, photos, candles, favorite foods of the deceased. Not 'Mexican Halloween' - entirely different cultural meaning. Three Kings Day (Epiphany) is when many Hispanic families traditionally exchange gifts, not Christmas - reflects different religious/cultural calendar.",
        "charter_expansion_angle": "From: 'Generic product recommendations based on browsing history' To: 'Culturally-aware shopping assistant that understands life moments, celebrations, and traditions'. Could extend to other cultural calendars and celebrations (Lunar New Year, Diwali, Ramadan/Eid, etc.). Positions Rufus as culturally intelligent, not just transactionally smart.",
        "source_signals": [
            {"title": "Looking for Quinceañera supplies on Amazon", "source": "reddit", "market": "hispanic_us", "url": "https://reddit.com/r/latino/example5"},
            {"title": "Can't find Día de los Muertos decorations", "source": "reddit", "market": "hispanic_us", "url": "https://reddit.com/r/latino/example6"}
        ],
        "detailed_scores": {
            "charter_fit": 78,
            "customer_evidence": 72,
            "market_size": 76,
            "feasibility": 90,
            "competitive_advantage": 75
        }
    },
    {
        "title": "Spanglish Search Support",
        "charter_fit_score": 75,
        "composite_score": 74,
        "customer_pain_point": "Bilingual Hispanic customers naturally mix Spanish and English when searching on Amazon ('quiero un phone case rojo', 'looking for zapatos de soccer', 'necesito batteries para el remote') but Amazon search doesn't handle code-switching well - often returns poor results or gets confused. Forces customers to consciously think about which language to use rather than shopping naturally and intuitively. Multiple Reddit complaints about this friction. Google Search handles this much better.",
        "proposed_solution": "Enhance search engine to handle mixed Spanish/English queries (Spanglish) seamlessly. Understand that bilingual customers code-switch naturally in daily conversation - it's not confusion or poor language skills, it's linguistic behavior. Train search models specifically on Spanglish patterns and natural bilingual search behavior. Allow customers to shop in their natural voice without forcing them to pick a single language. Implement bilingual query understanding layer.",
        "market_size": "Millions of bilingual Hispanic Americans who naturally code-switch in daily life and online behavior. Improved search experience and conversion opportunity - reducing this friction could increase conversion rate by 2-5% for bilingual shoppers (represents tens of millions in revenue). Low hanging fruit for immediate customer experience improvement. Growing segment as second/third generation Hispanic Americans are increasingly bilingual.",
        "competitive_intelligence": "Google Search handles Spanglish queries significantly better than Amazon search - clear quality gap to close. Shopify search also struggles with code-switching. Opportunity to match or exceed Google's natural language understanding capability in the shopping domain. Could become competitive advantage vs. other e-commerce platforms that only support monolingual search.",
        "cultural_context": "Code-switching (Spanglish) is completely natural and normal linguistic behavior for bilingual speakers - not confusion, laziness, or poor language skills. It's how many Hispanic Americans actually speak in daily life, mixing languages fluidly based on context, audience, and which language has the better word for what they want to express. Forcing them to consciously 'pick a language' for search creates unnecessary cognitive friction and feels exclusionary - like the platform doesn't understand how they actually communicate. Respecting code-switching shows cultural intelligence.",
        "charter_expansion_angle": "From: 'Monolingual experiences available in multiple languages' To: 'Truly bilingual experience that respects and supports how people actually speak'. Could extend to other bilingual populations with different code-switching patterns (Franglais for French-Canadians mixing French/English, Hinglish for Indian Americans mixing Hindi/English, etc.). Establishes Amazon as understanding real-world multilingual behavior, not just academic language categories.",
        "source_signals": [
            {"title": "Spanglish search doesn't work on Amazon", "source": "reddit", "market": "hispanic_us", "url": "https://reddit.com/r/spanglish/example5"},
            {"title": "Google handles mixed language queries better", "source": "reddit", "market": "hispanic_us", "url": "https://reddit.com/r/latino/example7"}
        ],
        "detailed_scores": {
            "charter_fit": 75,
            "customer_evidence": 80,
            "market_size": 70,
            "feasibility": 88,
            "competitive_advantage": 72
        }
    }
]

# Create minimal mock signals
mock_signals = [
    {
        "source": "reddit",
        "source_detail": "r/latino",
        "title": "Alexa doesn't understand my Mexican Spanish accent",
        "content": "I keep having to switch to English when shopping with Alexa because she doesn't understand my accent.",
        "url": "https://reddit.com/r/latino/example",
        "date": datetime.now().isoformat(),
        "engagement": {"score": 234, "comments": 67},
        "market": "hispanic_us"
    },
    {
        "source": "reddit",
        "source_detail": "r/quebec",
        "title": "Amazon.ca's French translation is terrible",
        "content": "The French on Amazon.ca is clearly translated from English by France French speakers, not Quebecers.",
        "url": "https://reddit.com/r/quebec/example",
        "date": datetime.now().isoformat(),
        "engagement": {"score": 456, "comments": 123},
        "market": "french_canadian"
    },
    {
        "source": "competitor",
        "source_detail": "Walmart",
        "title": "Walmart launches 'Descubre' Hispanic product discovery",
        "content": "Walmart announced new feature to help Hispanic customers find authentic Latino products.",
        "url": "https://corporate.walmart.com/example",
        "date": datetime.now().isoformat(),
        "market": "hispanic_us"
    }
]

print("=" * 70)
print("DEMO: MULTILINGUAL SHOPPING EXPERIENCE INTELLIGENCE BRIEF")
print("=" * 70)
print("Generating demonstration brief with rich mock data...")
print("This shows what the system produces when fully operational.\n")

generator = BriefGenerator(config)
brief = generator.generate_brief(mock_opportunities, mock_signals)

text_file = generator.save_brief(brief, filename="demo_intelligence_brief.txt")
html_file = generator.export_to_html(brief, filename="demo_intelligence_brief.html")

print("\n" + "=" * 70)
print("✅ DEMO BRIEF GENERATED SUCCESSFULLY!")
print("=" * 70)
print(f"\nOutput files created:")
print(f"  📄 Text version: {text_file}")
print(f"  🌐 HTML version: {html_file}")
print(f"\nOpening HTML brief in your browser...")
print("=" * 70)

import os
os.system(f'open {html_file}')

print("\n📌 What you're seeing:")
print("   • 5 fully-detailed product opportunities")
print("   • Charter fit scores (75-95/100)")
print("   • Customer pain points with evidence")
print("   • Market size estimates")
print("   • Competitive intelligence")
print("   • Charter expansion angles")
print("   • Strategic recommendations")
print("\nThis demonstrates the system's full output format.")
print("Next step: Fix the real Claude API analysis to produce similar results.")
