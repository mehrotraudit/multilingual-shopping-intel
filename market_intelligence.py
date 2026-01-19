"""
Market Intelligence Data Collection Module
Collects signals from Reddit, RSS feeds, Twitter/X, arXiv, and competitor sites
"""

import requests
import json
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time
import re

class MarketIntelligenceCollector:
    """Collects market signals from multiple sources"""
    
    def __init__(self, config):
        self.config = config
        self.lookback_days = config.LOOKBACK_DAYS
        self.cutoff_date = datetime.now() - timedelta(days=self.lookback_days)
        self.all_signals = []
        
    def collect_all_signals(self) -> List[Dict[str, Any]]:
        """Orchestrate collection from all sources"""
        print("🔍 Starting market intelligence collection...")
        
        # Collect from different sources
        signals = []
        
        try:
            reddit_signals = self.collect_reddit_signals()
            signals.extend(reddit_signals)
            print(f"✓ Reddit: {len(reddit_signals)} signals")
        except Exception as e:
            print(f"✗ Reddit collection failed: {e}")
        
        try:
            rss_signals = self.collect_rss_signals()
            signals.extend(rss_signals)
            print(f"✓ RSS Feeds: {len(rss_signals)} signals")
        except Exception as e:
            print(f"✗ RSS collection failed: {e}")
        
        try:
            arxiv_signals = self.collect_arxiv_signals()
            signals.extend(arxiv_signals)
            print(f"✓ arXiv: {len(arxiv_signals)} signals")
        except Exception as e:
            print(f"✗ arXiv collection failed: {e}")
        
        # Twitter/X collection would go here (requires API access)
        # For MVP, we'll simulate with placeholder data
        
        self.all_signals = signals
        print(f"\n📊 Total signals collected: {len(signals)}")
        return signals
    
    def collect_reddit_signals(self) -> List[Dict[str, Any]]:
        """Collect signals from Reddit using Pushshift/Reddit API alternative"""
        signals = []
        
        # In production, use Reddit API or Pushshift
        # For MVP, we'll create a method that could integrate with Reddit API
        # Here's the structure for what it would return:
        
        # Simulated Reddit data structure for demonstration
        simulated_reddit_posts = [
            {
                "title": "Alexa doesn't understand my Mexican Spanish accent",
                "subreddit": "r/latino",
                "content": "I keep having to switch to English when shopping with Alexa because she doesn't understand my accent. She sounds like she's from Spain, not Mexico.",
                "score": 234,
                "comments": 67,
                "created_utc": datetime.now() - timedelta(days=3),
                "url": "https://reddit.com/r/latino/example1"
            },
            {
                "title": "Amazon.ca's French translation is terrible",
                "subreddit": "r/quebec",
                "content": "The French on Amazon.ca is clearly translated from English, not written by a Quebecer. Many expressions don't make sense.",
                "score": 456,
                "comments": 123,
                "created_utc": datetime.now() - timedelta(days=5),
                "url": "https://reddit.com/r/quebec/example2"
            },
            {
                "title": "Can't find authentic Mexican products on Amazon",
                "subreddit": "r/mexico",
                "content": "Looking for real piloncillo and Mexican chocolate but Amazon search doesn't understand what I'm looking for. Walmart has a better selection.",
                "score": 189,
                "comments": 45,
                "created_utc": datetime.now() - timedelta(days=7),
                "url": "https://reddit.com/r/mexico/example3"
            },
            {
                "title": "Quebec's Bill 96 and online shopping",
                "subreddit": "r/quebec",
                "content": "With Bill 96 now enforced, I wonder if Amazon will improve their French. Right now it's bare minimum compliance.",
                "score": 312,
                "comments": 89,
                "created_utc": datetime.now() - timedelta(days=2),
                "url": "https://reddit.com/r/quebec/example4"
            },
            {
                "title": "Spanglish search doesn't work on Amazon",
                "subreddit": "r/spanglish",
                "content": "I naturally mix Spanish and English when searching, like 'quiero un phone case rojo' but Amazon gets confused. Google handles it fine.",
                "score": 167,
                "comments": 34,
                "created_utc": datetime.now() - timedelta(days=4),
                "url": "https://reddit.com/r/spanglish/example5"
            }
        ]
        
        for post in simulated_reddit_posts:
            if post['created_utc'] >= self.cutoff_date:
                signal = {
                    "source": "reddit",
                    "source_detail": post['subreddit'],
                    "title": post['title'],
                    "content": post['content'],
                    "url": post['url'],
                    "date": post['created_utc'].isoformat(),
                    "engagement": {
                        "score": post['score'],
                        "comments": post['comments']
                    },
                    "market": self._detect_market(post['subreddit'] + " " + post['content'])
                }
                signals.append(signal)
        
        return signals
    
    def collect_rss_signals(self) -> List[Dict[str, Any]]:
        """Collect signals from RSS feeds"""
        signals = []
        
        all_feeds = []
        all_feeds.extend(self.config.RSS_SOURCES.get('hispanic_industry', []))
        all_feeds.extend(self.config.RSS_SOURCES.get('french_canadian_industry', []))
        all_feeds.extend(self.config.RSS_SOURCES.get('technology', []))
        
        for feed_info in all_feeds[:5]:  # Limit for MVP
            try:
                feed = feedparser.parse(feed_info['url'])
                
                for entry in feed.entries[:10]:  # Top 10 per feed
                    published = self._parse_date(entry.get('published', ''))
                    
                    if published and published >= self.cutoff_date:
                        # Check if relevant to our markets
                        content = entry.get('summary', '') + entry.get('title', '')
                        if self._is_relevant(content):
                            signal = {
                                "source": "rss",
                                "source_detail": feed_info['name'],
                                "title": entry.get('title', ''),
                                "content": entry.get('summary', ''),
                                "url": entry.get('link', ''),
                                "date": published.isoformat(),
                                "market": self._detect_market(content)
                            }
                            signals.append(signal)
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"  Failed to fetch {feed_info['name']}: {e}")
                continue
        
        return signals
    
    def collect_arxiv_signals(self) -> List[Dict[str, Any]]:
        """Collect signals from arXiv (academic papers)"""
        signals = []
        
        # arXiv API endpoint
        base_url = "http://export.arxiv.org/api/query?"
        
        for keyword in self.config.ARXIV_KEYWORDS[:3]:  # Limit for MVP
            try:
                # Build query
                search_query = f"all:{keyword}"
                query = f"search_query={search_query}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
                
                response = requests.get(base_url + query)
                
                if response.status_code == 200:
                    # Parse XML response
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.content)
                    
                    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
                    
                    for entry in root.findall('atom:entry', namespace):
                        title = entry.find('atom:title', namespace).text.strip()
                        summary = entry.find('atom:summary', namespace).text.strip()
                        published = entry.find('atom:published', namespace).text
                        link = entry.find('atom:id', namespace).text
                        
                        published_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                        
                        if published_date.replace(tzinfo=None) >= self.cutoff_date:
                            signal = {
                                "source": "arxiv",
                                "source_detail": keyword,
                                "title": title,
                                "content": summary[:500],  # Truncate long abstracts
                                "url": link,
                                "date": published,
                                "market": "technology"
                            }
                            signals.append(signal)
                
                time.sleep(3)  # arXiv rate limiting
                
            except Exception as e:
                print(f"  Failed to fetch arXiv for '{keyword}': {e}")
                continue
        
        return signals
    
    def _is_relevant(self, text: str) -> bool:
        """Check if content is relevant to our markets"""
        text_lower = text.lower()
        
        relevant_terms = [
            'hispanic', 'latino', 'spanish', 'multilingual', 'translation',
            'quebec', 'french', 'canadian', 'francophone', 'bilingual',
            'ecommerce', 'e-commerce', 'shopping', 'retail', 'amazon',
            'voice', 'alexa', 'search', 'product discovery'
        ]
        
        return any(term in text_lower for term in relevant_terms)
    
    def _detect_market(self, text: str) -> str:
        """Detect which market (hispanic/french-canadian) the signal relates to"""
        text_lower = text.lower()
        
        hispanic_terms = ['hispanic', 'latino', 'spanish', 'mexico', 'spanglish', 'español']
        french_terms = ['quebec', 'french', 'canadian', 'français', 'francophone']
        
        hispanic_score = sum(1 for term in hispanic_terms if term in text_lower)
        french_score = sum(1 for term in french_terms if term in text_lower)
        
        if hispanic_score > french_score:
            return "hispanic_us"
        elif french_score > hispanic_score:
            return "french_canadian"
        else:
            return "both"
    
    def _parse_date(self, date_string: str) -> datetime:
        """Parse various date formats"""
        if not date_string:
            return None
        
        try:
            # Try common formats
            for fmt in ['%a, %d %b %Y %H:%M:%S %Z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d']:
                try:
                    return datetime.strptime(date_string, fmt)
                except:
                    continue
            return None
        except:
            return None
    
    def save_signals(self, filename: str = "market_signals.json"):
        """Save collected signals to file"""
        import os
        os.makedirs(self.config.DATA_DIR, exist_ok=True)
        
        filepath = os.path.join(self.config.DATA_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.all_signals, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Signals saved to {filepath}")
        return filepath


class CompetitorIntelligence:
    """Track competitor activities"""
    
    def __init__(self, config):
        self.config = config
    
    def collect_competitor_signals(self) -> List[Dict[str, Any]]:
        """Collect signals about competitor activities"""
        # In production, this would scrape competitor news pages
        # For MVP, return structured placeholders
        
        simulated_signals = [
            {
                "source": "competitor",
                "competitor": "Walmart",
                "title": "Walmart launches 'Descubre' Hispanic product discovery feature",
                "content": "Walmart announced a new 'Descubre' feature to help Hispanic customers find authentic Latino products more easily.",
                "url": "https://corporate.walmart.com/newsroom/example",
                "date": (datetime.now() - timedelta(days=10)).isoformat(),
                "market": "hispanic_us",
                "impact": "high"
            },
            {
                "source": "competitor",
                "competitor": "Google Assistant",
                "title": "Google improves Spanish dialect recognition",
                "content": "Google Assistant now better understands regional Spanish accents including Mexican, Puerto Rican, and Colombian variants.",
                "url": "https://blog.google/example",
                "date": (datetime.now() - timedelta(days=6)).isoformat(),
                "market": "hispanic_us",
                "impact": "high"
            },
            {
                "source": "competitor",
                "competitor": "Shopify",
                "title": "Shopify enhances French-Canadian localization",
                "content": "Shopify rolled out improved Quebec French translations and local payment methods for Canadian merchants.",
                "url": "https://www.shopify.com/blog/example",
                "date": (datetime.now() - timedelta(days=8)).isoformat(),
                "market": "french_canadian",
                "impact": "medium"
            }
        ]
        
        return simulated_signals


def test_collector():
    """Test the market intelligence collector"""
    import config
    
    collector = MarketIntelligenceCollector(config)
    signals = collector.collect_all_signals()
    
    print("\n" + "="*60)
    print("SAMPLE SIGNALS")
    print("="*60)
    
    for i, signal in enumerate(signals[:3], 1):
        print(f"\n{i}. {signal['title']}")
        print(f"   Source: {signal['source']} ({signal.get('source_detail', 'N/A')})")
        print(f"   Market: {signal['market']}")
        print(f"   Date: {signal['date']}")
        print(f"   Content: {signal['content'][:150]}...")
    
    collector.save_signals()
    
    return signals


if __name__ == "__main__":
    test_collector()
