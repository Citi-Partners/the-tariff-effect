"""
analyze_tariffs.py - AI-Powered Article Analyzer with PERSISTENT DATA
Only analyzes NEW articles, merges with existing analyzed data
"""

import anthropic
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

if not api_key:
    print("❌ ERROR: ANTHROPIC_API_KEY not found in .env file")
    exit(1)

client = anthropic.Anthropic(api_key=api_key)

# 16 product categories
CATEGORIES = [
    'food', 'appliances', 'auto', 'electronics', 'clothing', 'construction',
    'beauty', 'jewelry', 'energy', 'realestate', 'alcohol', 'tobacco',
    'furniture', 'toys', 'sports', 'health'
]

def load_existing_analyzed_articles():
    """Load previously analyzed articles"""
    output_file = 'data/analyzed_articles.json'
    
    if not os.path.exists(output_file):
        return []
    
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            existing = json.load(file)
        print(f"📚 Found {len(existing)} existing analyzed articles")
        return existing
    except Exception as e:
        print(f"⚠️  Warning: Could not load existing analyzed articles: {e}")
        return []

def load_raw_articles():
    """Load raw articles from fetch_feeds.py"""
    input_file = 'data/raw_articles.json'
    
    if not os.path.exists(input_file):
        print(f"❌ ERROR: {input_file} not found")
        print("Please run 'python3 fetch_feeds.py' first")
        exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def analyze_article(article):
    """Analyze a single article with Claude"""
    
    prompt = f"""Analyze this tariff-related news article for consumer impact.

Article Title: {article['title']}
Article Summary: {article['summary'][:500]}
Source: {article['source']}

Determine:
1. Is this relevant to consumer prices? (yes/no)
2. Which product categories are affected? Choose from: {', '.join(CATEGORIES)}
3. What's the price impact? (e.g., "+$50-100 on washing machines", "5-8% increase on groceries")
4. Timeline urgency? (immediate, 30-days, 90-days, long-term)
5. Brief consumer explanation (2-3 sentences, plain English, how does this affect household budgets?)

Respond ONLY with valid JSON:
{{
  "consumer_relevant": true/false,
  "affected_categories": ["category1", "category2"],
  "price_impact": "dollar/percentage estimate",
  "urgency": "immediate|30-days|90-days|long-term",
  "consumer_explanation": "plain English explanation",
  "affected_products": "specific products affected"
}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        # Clean up response
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        analysis = json.loads(response_text)
        
        # Only return if consumer relevant
        if analysis.get('consumer_relevant'):
            return {
                'title': article['title'],
                'summary': analysis.get('consumer_explanation', ''),
                'price_impact': analysis.get('price_impact', 'Unknown'),
                'urgency': analysis.get('urgency', 'long-term'),
                'affected_categories': analysis.get('affected_categories', []),
                'affected_products': analysis.get('affected_products', ''),
                'original_article': {
                    'link': article['link'],
                    'source': article['source'],
                    'published': article.get('published', ''),
                    'published_parsed': article.get('published_parsed'),
                    'fetched_date': article.get('fetched_date', '')
                }
            }
        
        return None
        
    except Exception as e:
        print(f"   ⚠️  Error analyzing article: {e}")
        return None

def main():
    print("\n" + "="*60)
    print("🤖 AI-POWERED TARIFF ANALYZER (Persistent Mode)")
    print("="*60 + "\n")
    
    # Load existing analyzed articles
    existing_analyzed = load_existing_analyzed_articles()
    existing_urls = {a.get('original_article', {}).get('link') for a in existing_analyzed}
    
    # Load raw articles
    raw_articles = load_raw_articles()
    print(f"📰 Loaded {len(raw_articles)} total raw articles from database")
    
    # Filter to only NEW articles that haven't been analyzed
    new_articles = [a for a in raw_articles if a.get('link') not in existing_urls]
    
    if not new_articles:
        print("\n✅ No new articles to analyze! All articles already processed.")
        print(f"   Total analyzed articles in database: {len(existing_analyzed)}")
        return
    
    print(f"🆕 Found {len(new_articles)} NEW articles to analyze")
    print(f"⏭️  Skipping {len(raw_articles) - len(new_articles)} already analyzed articles\n")
    
    analyzed_articles = []
    
    for i, article in enumerate(new_articles, 1):
        print(f"Analyzing article {i}/{len(new_articles)}: {article['title'][:60]}...")
        
        result = analyze_article(article)
        
        if result:
            analyzed_articles.append(result)
            print(f"   ✓ Consumer relevant - Categories: {', '.join(result['affected_categories'])}")
        else:
            print(f"   ⊘ Not consumer relevant")
    
    # Merge with existing analyzed articles
    all_analyzed = existing_analyzed + analyzed_articles
    
    print(f"\n📊 Analysis complete!")
    print(f"   New articles analyzed: {len(new_articles)}")
    print(f"   New consumer-relevant: {len(analyzed_articles)}")
    print(f"   Total in database: {len(all_analyzed)} ({len(existing_analyzed)} existing + {len(analyzed_articles)} new)")
    
    # Save combined results
    os.makedirs('data', exist_ok=True)
    output_file = 'data/analyzed_articles.json'
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_analyzed, file, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Saved to {output_file}")
    print(f"   Total articles: {len(all_analyzed)}")
    print(f"   New this run: {len(analyzed_articles)}")
    
    print("\n" + "="*60)
    print("✅ DONE - Articles accumulated (not replaced)")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
