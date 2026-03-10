"""
fetch_feeds.py - RSS Feed Aggregator with PERSISTENT DATA
Fetches articles and APPENDS to existing data (doesn't overwrite)
"""

import feedparser
import json
import os
from datetime import datetime

# RSS FEEDS (27 sources)
RSS_FEEDS = [
    "https://ustr.gov/about-us/policy-offices/press-office/press-releases/rss.xml",
    "https://www.commerce.gov/news/rss.xml",
    "https://www.cbp.gov/newsroom/national-media-release/rss",
    "https://www.reuters.com/rssFeed/businessNews",
    "https://www.reuters.com/rssFeed/ReutersWorldTrade", 
    "https://feeds.apnews.com/rss/business",
    "https://feeds.npr.org/1006/rss.xml",
    "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "https://www.ft.com/trade-secrets?format=rss",
    "https://www.trade.gov/rss.xml",
    "https://insidetrade.com/rss",
    "https://taxfoundation.org/feed/",
    "https://www.piie.com/rss/research.xml",
    "https://www.brookings.edu/feed/",
    "https://www.aei.org/feed/",
    "https://www.cnbc.com/id/10000664/device/rss/rss.html",
    "https://feeds.bloomberg.com/economics/news.rss",
    "https://feeds.content.dowjones.io/public/rss/mw_marketpulse",
    "https://www.retaildive.com/feeds/news/",
    "https://www.fooddive.com/feeds/news/",
    "https://www.autonews.com/rss",
    "https://www.supplychaindive.com/feeds/news/",
    "https://www.manufacturingdive.com/feeds/news/",
    "https://www.freightwaves.com/feed",
    "https://www.joc.com/rss.xml",
    "https://www.consumerreports.org/cro/index.rss",
    "https://www.kiplinger.com/feeds/rss"
]

def load_existing_articles():
    """Load existing articles from raw_articles.json"""
    input_file = 'data/raw_articles.json'
    
    if not os.path.exists(input_file):
        return []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"⚠️  Warning: Could not load existing articles: {e}")
        return []

def fetch_all_feeds():
    """Fetch articles from all RSS feeds and merge with existing data"""
    
    # Load existing articles
    print("📚 Loading existing articles...")
    existing_articles = load_existing_articles()
    existing_urls = {article['link'] for article in existing_articles if 'link' in article}
    print(f"   Found {len(existing_articles)} existing articles")
    
    # Fetch new articles
    print(f"\n📡 Fetching from {len(RSS_FEEDS)} RSS sources...")
    
    new_articles = []
    new_count = 0
    
    for i, feed_url in enumerate(RSS_FEEDS, 1):
        try:
            print(f"   [{i}/{len(RSS_FEEDS)}] {feed_url[:50]}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                article_url = entry.get('link', '')
                
                # Skip if we already have this article
                if article_url in existing_urls:
                    continue
                
                article = {
                    'title': entry.get('title', 'No Title'),
                    'link': article_url,
                    'published': entry.get('published', ''),
                    'published_parsed': entry.get('published_parsed'),
                    'summary': entry.get('summary', ''),
                    'source': feed.feed.get('title', 'Unknown Source'),
                    'fetched_date': datetime.now().isoformat()
                }
                
                new_articles.append(article)
                existing_urls.add(article_url)  # Track to avoid duplicates in this run
                new_count += 1
                
        except Exception as e:
            print(f"   ⚠️  Error fetching {feed_url[:50]}: {e}")
    
    # Combine old and new articles
    all_articles = existing_articles + new_articles
    
    print(f"\n✅ Fetch complete!")
    print(f"   New articles found: {new_count}")
    print(f"   Total articles in database: {len(all_articles)}")
    
    # Save combined data
    os.makedirs('data', exist_ok=True)
    output_file = 'data/raw_articles.json'
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_articles, file, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Saved to {output_file}")
    print(f"   Total articles: {len(all_articles)}")
    print(f"   New this run: {new_count}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📰 RSS FEED AGGREGATOR (Persistent Mode)")
    print("="*60 + "\n")
    
    fetch_all_feeds()
    
    print("\n" + "="*60)
    print("✅ DONE - Articles accumulated (not replaced)")
    print("="*60 + "\n")
