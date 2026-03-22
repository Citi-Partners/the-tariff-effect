"""
generate_site.py - Website generator (v4.0)
Generates homepage + 16 category pages + mission + history pages
Category pages are output as /category/index.html for Cloudflare Pages compatibility
"""

import json
import os
from datetime import datetime, timedelta
from time import mktime

SITE_TITLE = "The Tariff Effect"
SITE_TAGLINE = "How tariffs impact YOUR budget"
BASE_URL = "https://thetariffeffect.com"

# ALL 16 CATEGORIES
CATEGORIES = {
    "food": "🍎 Food & Groceries",
    "appliances": "🏠 Appliances",
    "auto": "🚗 Auto & Transportation",
    "electronics": "💻 Electronics",
    "clothing": "👕 Clothing & Apparel",
    "construction": "🏗️ Construction Materials",
    "beauty": "💄 Beauty & Personal Care",
    "jewelry": "💍 Jewelry & Accessories",
    "energy": "⚡ Energy & Fuel",
    "realestate": "🏡 Real Estate & Housing",
    "alcohol": "🍷 Alcohol & Spirits",
    "tobacco": "🚬 Tobacco Products",
    "furniture": "🛋️ Furniture & Decor",
    "toys": "🎮 Toys & Games",
    "sports": "⚽ Sports & Outdoors",
    "health": "💊 Health & Medical",
}


def ensure_dir(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def write_file(path, content):
    """Write UTF-8 file, creating directories as needed."""
    directory = os.path.dirname(path)
    if directory:
        ensure_dir(directory)
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def get_page_title(active_page=""):
    """Build browser title."""
    if not active_page or active_page == "Home":
        return f"{SITE_TITLE} - Latest Tariff News"
    return f"{SITE_TITLE} - {active_page}"


def get_header(active_page=""):
    """Generate HTML header with navigation."""

    category_items = ""
    for key, name in CATEGORIES.items():
        active_class = "class='active'" if active_page == name else ""
        category_items += f'<a href="/{key}/" {active_class}>{name}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{get_page_title(active_page)}</title>
    <meta name="description" content="Daily updates on how tariffs affect prices for groceries, cars, electronics, and more. Plain-English analysis for American families.">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="stylesheet" href="/styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5122718379856409"
         crossorigin="anonymous"></script>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="branding">
                    <a href="/" style="text-decoration: none;">
                        <img src="/the tariff effect logo.png" alt="{SITE_TITLE}" class="site-logo">
                    </a>
                    <p class="tagline">{SITE_TAGLINE}</p>
                </div>
                <nav>
                    <a href="/" {"class='active'" if active_page == "Home" else ""}>Home</a>
                    <div class="category-dropdown">
                        <a href="#">Categories</a>
                        <div class="dropdown-menu">
                            {category_items}
                        </div>
                    </div>
                    <a href="/history.html" {"class='active'" if active_page == "History" else ""}>History</a>
                    <a href="/mission.html" {"class='active'" if active_page == "Mission" else ""}>Mission</a>
                    <a href="#" class="donate-btn" onclick="openDonateModal(); return false;">Donate</a>
                </nav>
            </div>
        </div>
    </header>
    <main class="container">
"""


def get_footer():
    """Generate HTML footer."""
    update_time = datetime.now().strftime("%B %d, %Y at %I:%M %p ET")

    return f"""
    </main>

    <footer>
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2026 Citi Partners Inc. | Tracking tariff impacts on American families</p>
                <p style="font-size: 0.9em; color: var(--text-medium);">Last updated: {update_time}</p>
            </div>
        </div>
    </footer>

    <!-- Donation Modal -->
    <div id="donateModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeDonateModal()">&times;</span>
            <h2 style="margin-bottom: 1rem; color: var(--text-dark);">Support The Tariff Effect</h2>
            <p style="margin-bottom: 1.5rem; color: var(--text-medium);">
                Help us keep tracking tariff impacts for American families. Your donation keeps this service free and independent.
            </p>
            <givebutter-widget id="gGP7Vp"></givebutter-widget>
            <script async src="https://widgets.givebutter.com/latest.umd.cjs?acct=tNu1xZUaiyXMkQzO&p=other"></script>
        </div>
    </div>

    <script>
    function openDonateModal() {{
        document.getElementById('donateModal').style.display = 'block';
        document.body.style.overflow = 'hidden';
    }}

    function closeDonateModal() {{
        document.getElementById('donateModal').style.display = 'none';
        document.body.style.overflow = 'auto';
    }}

    window.onclick = function(event) {{
        const modal = document.getElementById('donateModal');
        if (event.target == modal) {{
            closeDonateModal();
        }}
    }}

    document.addEventListener('DOMContentLoaded', function() {{
        const dropdown = document.querySelector('.category-dropdown');
        if (dropdown) {{
            dropdown.addEventListener('click', function(e) {{
                e.preventDefault();
                const menu = this.querySelector('.dropdown-menu');
                if (menu) {{
                    menu.classList.toggle('show');
                }}
            }});

            document.addEventListener('click', function(e) {{
                if (!dropdown.contains(e.target)) {{
                    const menu = dropdown.querySelector('.dropdown-menu');
                    if (menu) {{
                        menu.classList.remove('show');
                    }}
                }}
            }});
        }}
    }});
    </script>
</body>
</html>
"""


def parse_article_datetime(article):
    """Return normalized naive datetime for article if available, else None."""
    original = article.get("original_article", {})
    pub_date = original.get("published_parsed")

    if pub_date:
        try:
            dt = datetime.fromtimestamp(mktime(pub_date))
            return dt.replace(tzinfo=None)
        except Exception:
            return None

    published = original.get("published", "")
    if published:
        try:
            from dateutil import parser
            dt = parser.parse(published)

            # Normalize timezone-aware datetimes to naive
            if dt.tzinfo is not None:
                dt = dt.astimezone().replace(tzinfo=None)

            return dt
        except Exception:
            return None

    return None


def format_article_date(article):
    """Format article date for display."""
    dt = parse_article_datetime(article)
    if dt:
        return dt.strftime("%A, %m/%d/%Y")

    original = article.get("original_article", {})
    published = original.get("published", "")
    if published:
        return published[:10] if len(published) > 10 else published

    return ""


def article_sort_key(article):
    """Sort newest first, falling back safely."""
    dt = parse_article_datetime(article)
    if dt:
        return dt
    return datetime.min


def create_article_card(article):
    """Generate HTML for one tariff card."""
    original = article.get("original_article", {})

    title = article.get("title") or original.get("title", "No title")
    link = original.get("link", "#")
    source = original.get("source", "Unknown")
    article_date = format_article_date(article)

    family_summary = article.get("summary") or article.get("family_summary", "")

    products_raw = article.get("affected_products") or article.get("products_affected", [])
    if isinstance(products_raw, list):
        products = ", ".join(products_raw)
    else:
        products = products_raw

    price_impact = article.get("price_impact", "Impact being assessed")
    urgency = article.get("urgency", "long-term")

    urgency_class = {
        "immediate": "urgent",
        "30-days": "soon",
        "90-days": "moderate",
        "long-term": "low",
    }.get(urgency, "low")

    urgency_label = urgency.replace("-", " ").title()

    return f"""
        <div class="tariff-card" data-urgency="{urgency}">
            <div class="card-header">
                <span class="urgency-badge {urgency_class}">{urgency_label}</span>
                <span class="source">{source}</span>
            </div>
            <div class="card-body">
                <h3><a href="{link}" target="_blank" rel="noopener noreferrer">{title}</a></h3>
                {f'<div class="article-date" style="color: var(--text-medium); font-size: 0.9em; margin-bottom: 0.75rem;">{article_date}</div>' if article_date else ''}
                <div class="family-impact">
                    {family_summary}
                </div>
                <div class="impact-details">
                    <div class="detail-item">
                        <strong>Products:</strong>
                        <span>{products if products else 'Various consumer goods'}</span>
                    </div>
                    <div class="detail-item">
                        <strong>Price Impact:</strong>
                        <span>{price_impact}</span>
                    </div>
                </div>
            </div>
            <div class="card-footer">
                <a href="{link}" target="_blank" rel="noopener noreferrer" class="read-more">Read full article</a>
            </div>
        </div>
    """


def load_analyzed_articles():
    """Load analyzed articles from JSON and filter to only 3/1/26 and newer."""
    input_file = "data/analyzed_articles.json"

    if not os.path.exists(input_file):
        print(f"❌ ERROR: {input_file} not found")
        print("Please run 'python analyze_tariffs.py' first")
        raise SystemExit(1)

    with open(input_file, "r", encoding="utf-8") as file:
        all_articles = json.load(file)

min_date = datetime(2026, 3, 1)
filtered_articles = []

for article in all_articles:
    article_datetime = parse_article_datetime(article)

    if article_datetime is not None and getattr(article_datetime, "tzinfo", None) is not None:
        article_datetime = article_datetime.astimezone().replace(tzinfo=None)

    if article_datetime is None or article_datetime >= min_date:
        filtered_articles.append(article)
        
    print(f"Loaded {len(all_articles)} total articles, showing {len(filtered_articles)} from 3/1/26 onward")
    return filtered_articles


def filter_recent_articles(articles, days=7):
    """Filter articles to only show those from the last N days."""
    cutoff_date = datetime.now() - timedelta(days=days)
    recent = []

    for article in articles:
        article_datetime = parse_article_datetime(article)
        if article_datetime is None or article_datetime >= cutoff_date:
            recent.append(article)

    return recent


def add_historical_timeline():
    """Add last 5 historical tariffs when no new articles."""
    hist_file = "historical-data.json"
    if not os.path.exists(hist_file):
        return ""

    try:
        with open(hist_file, "r", encoding="utf-8") as file:
            hist_data = json.load(file)

        tariffs = hist_data.get("historical_tariffs", [])
        if not tariffs:
            return ""

        recent = tariffs[-5:]
        recent.reverse()

        html = """
        <section class="info-box" style="margin-top: 2rem;">
            <h3 style="font-size: 1.5em; margin-bottom: 1rem;">Recent Tariff History</h3>
            <p style="color: var(--text-medium); margin-bottom: 1.5rem;">While there's no new tariff news today, here are recent historical impacts:</p>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
        """

        for tariff in recent:
            impact_color = "#10b981" if tariff.get("impact_type") == "positive" else "#dc2626"
            html += f"""
                <div style="padding: 1rem; border-left: 4px solid {impact_color}; background: var(--light-blue-bg); border-radius: 6px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <strong style="color: var(--text-dark);">{tariff.get('title', '')}</strong>
                        <span style="color: var(--text-medium); font-size: 0.9em;">{tariff.get('date', '')}</span>
                    </div>
                    <p style="margin-bottom: 0.5rem; color: var(--text-medium); font-size: 0.95em;">{tariff.get('details', '')}</p>
                    <p style="font-weight: 600; color: {impact_color}; font-size: 0.95em;">{tariff.get('price_impact', '')}</p>
                </div>
            """

        html += """
            </div>
            <div style="text-align: center; margin-top: 1.5rem;">
                <a href="/history.html" style="color: var(--primary-blue); text-decoration: none; font-weight: 600;">
                    View Full History (2016-2025) →
                </a>
            </div>
        </section>
        """

        return html

    except Exception:
        return ""


def generate_homepage(articles):
    """Generate homepage index.html."""
    print("Generating homepage...")

    recent_articles = filter_recent_articles(articles, days=7)
    cutoff_7days = datetime.now() - timedelta(days=7)

    older_articles = []
    for article in articles:
        article_datetime = parse_article_datetime(article)
        if article_datetime and article_datetime < cutoff_7days:
            older_articles.append(article)

    older_articles_sorted = sorted(older_articles, key=article_sort_key, reverse=True)
    recent_updates = older_articles_sorted[:10]

    html = get_header("Home")

    html += """
        <section class="page-header">
            <h2>The Tariff Effect</h2>
            <p style="font-size: 1.15em; font-weight: 600; line-height: 1.7;">See how recent tariff changes affect the prices you pay for everyday products. Updated daily with AI-powered analysis that translates complex policy into real family budget impacts.</p>
        </section>
    """

    html += """
        <section class="info-box">
            <h3>How to Read This Tracker</h3>
            <div class="badge-guide">
                <div class="badge-guide-item urgent">
                    <strong>🔴 Immediate</strong>
                    <span>Price changes happening now or within days</span>
                </div>
                <div class="badge-guide-item soon">
                    <strong>🟡 30 Days</strong>
                    <span>Changes expected within the next month</span>
                </div>
                <div class="badge-guide-item moderate">
                    <strong>🔵 90 Days</strong>
                    <span>Changes expected in 2-3 months</span>
                </div>
                <div class="badge-guide-item longterm">
                    <strong>⚪ Long-Term</strong>
                    <span>Gradual changes over 6+ months</span>
                </div>
            </div>
            <p style="color: var(--text-medium); font-size: 0.95em; margin-top: 1rem;">
                <strong>What you'll see:</strong> Each card shows which products are affected, estimated price impacts, and a plain-English explanation of how this tariff affects your household budget. We analyze 27+ official sources daily to bring you accurate, non-partisan information.
            </p>
        </section>
    """

    html += '<h2 style="margin: 2rem 0 0.5rem; font-size: 1.8em; color: var(--text-dark);">Latest Tariff Updates</h2>'

    html += """
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; gap: 1rem; flex-wrap: wrap;">
        <h3 style="margin: 0; font-size: 1.2em; color: var(--text-medium); font-weight: 500;">This Week's Tariff News (Last 7 Days)</h3>
        <div style="display: flex; gap: 0.5rem; align-items: center;">
            <label for="urgency-filter" style="color: var(--text-medium); font-size: 0.95em;">Filter by:</label>
            <select id="urgency-filter" style="padding: 0.5rem 1rem; border: 2px solid var(--border-light); border-radius: 6px; background: white; color: var(--text-dark); font-size: 0.95em; cursor: pointer;">
                <option value="all">All Updates</option>
                <option value="immediate">🔴 Immediate</option>
                <option value="30-days">🟡 30 Days</option>
                <option value="90-days">🔵 90 Days</option>
                <option value="long-term">⚪ Long-Term</option>
            </select>
        </div>
    </div>
    """

    html += '<div class="articles-grid" id="latest-articles-grid">'

    if recent_articles:
        sorted_recent = sorted(recent_articles, key=article_sort_key, reverse=True)
        for article in sorted_recent:
            html += create_article_card(article)
    else:
        html += """
            <div class="no-articles">
                <div class="no-articles-icon">📊</div>
                <h3>No New Tariff News This Week</h3>
                <p>Our AI scanned 27+ sources but found no consumer-relevant tariff updates in the last 7 days. Check the recent updates below or visit our <a href="/history.html">full history</a>.</p>
            </div>
        """
        html += add_historical_timeline()

    html += "</div>"

    html += """
        <h2 style="margin: 3rem 0 1.5rem; font-size: 2em; color: var(--text-dark); border-top: 2px solid var(--border-light); padding-top: 2rem;">Recent Updates (Last 10 Articles)</h2>
        <p style="margin-bottom: 1.5rem; color: var(--text-medium);">Earlier tariff analyses from this month.</p>
    """

    html += '<div class="articles-grid">'
    if recent_updates:
        for article in recent_updates:
            html += create_article_card(article)
    else:
        html += """
            <div class="info-box" style="text-align: center; padding: 3rem 2rem;">
                <p style="font-size: 1.1em; color: var(--text-medium); margin-bottom: 0.5rem;">
                    📅 <strong>Check back in a few days!</strong>
                </p>
                <p style="color: var(--text-medium);">
                    Articles older than 7 days will appear here as our archive grows.
                    For now, all our latest analysis is in "This Week's Tariff News" above.
                </p>
            </div>
        """
    html += "</div>"

    html += """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const filterSelect = document.getElementById('urgency-filter');
        const articlesGrid = document.getElementById('latest-articles-grid');

        if (filterSelect && articlesGrid) {
            filterSelect.addEventListener('change', function() {
                const selectedUrgency = this.value;
                const cards = articlesGrid.querySelectorAll('.tariff-card');

                cards.forEach(card => {
                    if (selectedUrgency === 'all') {
                        card.style.display = '';
                    } else {
                        const cardUrgency = card.getAttribute('data-urgency');
                        card.style.display = (cardUrgency === selectedUrgency) ? '' : 'none';
                    }
                });
            });
        }
    });
    </script>
    """

    html += get_footer()
    write_file("index.html", html)

    print(f"✓ Created index.html (showing {len(recent_articles)} from last 7 days + {len(recent_updates)} in recent updates)")


def generate_category_pages(articles):
    """Generate all 16 category pages under /category/index.html."""
    print("Generating category pages...")

    by_category = {cat: [] for cat in CATEGORIES.keys()}

    for article in articles:
        for cat in article.get("affected_categories", []):
            if cat in by_category:
                by_category[cat].append(article)

    for category_key, category_name in CATEGORIES.items():
        category_articles = sorted(by_category[category_key], key=article_sort_key, reverse=True)

        html = get_header(category_name)

        html += f"""
            <section class="page-header">
                <h2>{category_name}</h2>
                <p>Tariff impacts on {category_name.replace("🏠 ", "").replace("🍎 ", "").replace("🚗 ", "").replace("💻 ", "").replace("👕 ", "").replace("🏗️ ", "").replace("💄 ", "").replace("💍 ", "").replace("⚡ ", "").replace("🏡 ", "").replace("🍷 ", "").replace("🚬 ", "").replace("🛋️ ", "").replace("🎮 ", "").replace("⚽ ", "").replace("💊 ", "").lower()} products and pricing.</p>
            </section>
        """

        html += '<div class="articles-grid">'

        if not category_articles:
            html += f"""
                <div class="no-articles">
                    <div class="no-articles-icon">📊</div>
                    <h3>No Recent {category_name} Tariff News</h3>
                    <p>Check the <a href="/">latest updates</a> or <a href="/history.html">historical data</a>.</p>
                </div>
            """
        else:
            for article in category_articles:
                html += create_article_card(article)

        html += "</div>"
        html += get_footer()

        output_path = os.path.join(category_key, "index.html")
        write_file(output_path, html)

        print(f"✓ Created {output_path}")


def generate_history_page(analyzed_articles=None):
    """Generate history.html from historical-data.json + archived analyzed articles."""
    print("Generating history page...")

    hist_file = "historical-data-COMPLETE.json" if os.path.exists("historical-data-COMPLETE.json") else "historical-data.json"

    if not os.path.exists(hist_file):
        print(f"❌ ERROR: {hist_file} not found")
        return

    try:
        with open(hist_file, "r", encoding="utf-8") as file:
            hist_data = json.load(file)
    except Exception as e:
        print(f"❌ ERROR loading {hist_file}: {e}")
        return

    tariffs = hist_data.get("historical_tariffs", [])
    if not tariffs:
        print("❌ ERROR: No tariffs found in historical data")
        return

    by_year = {}
    for tariff in tariffs:
        year = tariff.get("year", "Unknown")
        by_year.setdefault(year, []).append(tariff)

    html = get_header("History")

    html += """
        <section class="page-header">
            <h2>Historical Tariff Impacts (2016-2026)</h2>
            <p>Learn from the past: How tariffs affected American wallets over the last decade</p>
        </section>
    """

    year_colors = {
        2026: "#1e40af",
        2025: "#f59e0b",
        2024: "#1e40af",
        2023: "#f59e0b",
        2022: "#1e40af",
        2021: "#f59e0b",
        2020: "#1e40af",
        2019: "#f59e0b",
        2018: "#1e40af",
        2017: "#f59e0b",
        2016: "#1e40af",
    }

    sorted_years = sorted(by_year.keys(), reverse=True)

    for year in sorted_years:
        year_tariffs = by_year[year]
        try:
            color = year_colors.get(int(year), "#1e40af")
        except Exception:
            color = "#1e40af"

        year_summary = year_tariffs[0].get("year_summary", f"{year}: Tariff Policy Developments")

        html += f"""
            <div class="info-box" style="border-left: 4px solid {color};">
                <h3 style="color: {color};">{year_summary}</h3>
        """

        for i, tariff in enumerate(year_tariffs):
            if i > 0:
                html += '<div style="margin: 1.5rem 0; border-bottom: 1px solid var(--border-light);"></div>'

            impact_color = "#10b981" if tariff.get("impact_type") == "positive" else "#dc2626"

            products = tariff.get("products_affected", "Various products")
            if isinstance(products, list):
                products = ", ".join(products)

            html += f"""
                <div style="margin-bottom: 1rem;">
                    <h4 style="font-size: 1.1em; margin-bottom: 0.5rem;">{tariff.get('title', 'Tariff Event')}</h4>
                    <p><strong>Impact:</strong> <span style="color: {impact_color}; font-weight: 600;">{tariff.get('price_impact', 'Impact varies')}</span></p>
                    <p><strong>Products:</strong> {products}</p>
                    <p style="margin-top: 0.5rem; color: var(--text-medium);">{tariff.get('details', '')}</p>
                </div>
            """

        html += "</div>"

    archived_articles = []

    if analyzed_articles:
        cutoff_7days = datetime.now() - timedelta(days=7)

        older_articles = []
        for article in analyzed_articles:
            article_datetime = parse_article_datetime(article)
            if article_datetime and article_datetime < cutoff_7days:
                older_articles.append(article)

        older_articles_sorted = sorted(older_articles, key=article_sort_key, reverse=True)
        archived_articles = older_articles_sorted[10:]

        if archived_articles:
            html += """
                <h2 style="margin: 3rem 0 1.5rem; font-size: 2em; color: var(--text-dark); border-top: 2px solid var(--border-light); padding-top: 2rem;">Older Articles</h2>
                <p style="margin-bottom: 1.5rem; color: var(--text-medium);">Earlier tariff analyses beyond our Recent Updates section.</p>
                <div class="articles-grid">
            """

            for article in archived_articles:
                html += create_article_card(article)

            html += "</div>"

    html += get_footer()
    write_file("history.html", html)

    print(f"✓ Created history.html (showing {len(sorted_years)} years, {len(tariffs)} timeline events, {len(archived_articles)} archived articles)")


def generate_mission_page():
    """Generate mission.html."""
    print("Generating mission page...")

    html = get_header("Mission")

    html += """
        <section class="page-header" style="margin-bottom: 3rem;">
            <h2 style="font-size: 2.5em; margin-bottom: 1.5rem;">Our Mission</h2>
            <p style="font-size: 1.2em; max-width: 800px; margin: 0 auto; line-height: 1.8;">
                To provide clear, non-partisan information about how tariffs affect the prices American families pay for everyday goods.
            </p>
        </section>

        <div style="max-width: 800px; margin: 0 auto;">
            <section class="info-box" style="margin-bottom: 2rem;">
                <h3 style="font-size: 1.6em; margin-bottom: 1.5rem; text-align: center; color: var(--primary-blue);">Why We Exist</h3>
                <p style="font-size: 1.05em; line-height: 1.8; margin-bottom: 1rem;">
                    Tariff news is confusing. Articles are filled with technical jargon, partisan spin, and policy minutiae that obscure the simple question most Americans want answered: <strong>"How will this affect my wallet?"</strong>
                </p>
                <p style="font-size: 1.05em; line-height: 1.8; margin-bottom: 1rem;">
                    We believe every American deserves to understand how trade policy impacts their household budget—without needing an economics degree or wading through political rhetoric.
                </p>
                <p style="font-size: 1.05em; line-height: 1.8;">
                    That's why we created <strong>The Tariff Effect</strong>.
                </p>
            </section>

            <section class="info-box" style="margin-bottom: 2rem;">
                <h3 style="font-size: 1.6em; margin-bottom: 1.5rem; text-align: center; color: var(--accent-orange);">What We Do</h3>
                <div style="display: grid; gap: 1.5rem;">
                    <div>
                        <h4 style="color: var(--primary-blue); font-size: 1.2em; margin-bottom: 0.5rem; text-align: center;">📡 Monitor Official Sources</h4>
                        <p style="line-height: 1.7;">We track 27+ authoritative sources including the U.S. Trade Representative, Commerce Department, Federal Reserve, and major trade publications.</p>
                    </div>
                    <div>
                        <h4 style="color: var(--accent-orange); font-size: 1.2em; margin-bottom: 0.5rem; text-align: center;">🤖 AI-Powered Analysis</h4>
                        <p style="line-height: 1.7;">Advanced AI analyzes each article to determine consumer relevance and translate policy-speak into plain English.</p>
                    </div>
                    <div>
                        <h4 style="color: var(--primary-blue); font-size: 1.2em; margin-bottom: 0.5rem; text-align: center;">💰 Price Impact Translation</h4>
                        <p style="line-height: 1.7;">We estimate how tariff changes affect real prices: "Your washing machine will cost $50-80 more" instead of "25% steel tariff announced."</p>
                    </div>
                    <div>
                        <h4 style="color: var(--accent-orange); font-size: 1.2em; margin-bottom: 0.5rem; text-align: center;">📅 Daily Updates</h4>
                        <p style="line-height: 1.7;">Automated daily analysis means you always have the latest information without manual research.</p>
                    </div>
                    <div>
                        <h4 style="color: var(--primary-blue); font-size: 1.2em; margin-bottom: 0.5rem; text-align: center;">🆓 Free for Everyone</h4>
                        <p style="line-height: 1.7;">No paywalls, no subscriptions. Critical information about how policy affects your budget should be accessible to all Americans.</p>
                    </div>
                </div>
            </section>

            <section class="info-box" style="margin-bottom: 2rem;">
                <h3 style="font-size: 1.6em; margin-bottom: 1.5rem; text-align: center; color: var(--primary-blue);">Our Values</h3>
                <div style="display: grid; gap: 1rem;">
                    <div style="padding: 1rem; background: white; border: 2px solid var(--border-light); border-radius: 8px; border-left: 4px solid var(--primary-blue);">
                        <strong style="font-size: 1.1em; color: var(--primary-blue);">Transparency:</strong>
                        <span>We cite our sources and show our methodology.</span>
                    </div>
                    <div style="padding: 1rem; background: white; border: 2px solid var(--border-light); border-radius: 8px; border-left: 4px solid var(--accent-orange);">
                        <strong style="font-size: 1.1em; color: var(--accent-orange);">Accuracy:</strong>
                        <span>We rely on official data and credible economic research.</span>
                    </div>
                    <div style="padding: 1rem; background: white; border: 2px solid var(--border-light); border-radius: 8px; border-left: 4px solid var(--primary-blue);">
                        <strong style="font-size: 1.1em; color: var(--primary-blue);">Accessibility:</strong>
                        <span>We write for real people, not economists.</span>
                    </div>
                    <div style="padding: 1rem; background: white; border: 2px solid var(--border-light); border-radius: 8px; border-left: 4px solid var(--accent-orange);">
                        <strong style="font-size: 1.1em; color: var(--accent-orange);">Non-Partisanship:</strong>
                        <span>We report the facts, not political opinions.</span>
                    </div>
                </div>
            </section>

            <section class="info-box" style="text-align: center; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 2px solid #bfdbfe;">
                <h3 style="font-size: 1.5em; margin-bottom: 1rem; color: var(--primary-blue);">Support Our Work</h3>
                <p style="font-size: 1.05em; margin-bottom: 1.5rem; line-height: 1.7;">
                    We're a small, independent team committed to keeping this resource free and accessible. Your support helps us maintain daily updates and expand our coverage.
                </p>
                <a href="#" onclick="openDonateModal(); return false;" style="display: inline-block; padding: 1rem 2.5rem; background: var(--accent-orange); color: white; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 1.1em; transition: all 0.2s;">
                    Support The Tariff Effect →
                </a>
            </section>
        </div>
    """

    html += get_footer()
    write_file("mission.html", html)

    print("✓ Created mission.html")


def generate_sitemap():
    """Generate sitemap.xml for SEO."""
    print("Generating sitemap...")

    today = datetime.now().strftime("%Y-%m-%d")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{BASE_URL}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{BASE_URL}/history.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{BASE_URL}/mission.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""

    for key in CATEGORIES.keys():
        sitemap += f"""    <url>
        <loc>{BASE_URL}/{key}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.9</priority>
    </url>
"""

    sitemap += "</urlset>"
    write_file("sitemap.xml", sitemap)

    print("✓ Created sitemap.xml")


def print_summary(articles):
    """Print generation summary."""
    print("\n" + "=" * 60)
    print("📊 SITE GENERATION COMPLETE")
    print("=" * 60)
    print(f"Total articles analyzed: {len(articles)}")

    recent = filter_recent_articles(articles, days=7)
    print(f"Articles from last 7 days (on Latest page): {len(recent)}")
    print(f"Older articles (move to History): {len(articles) - len(recent)}")

    total_pages = 3 + len(CATEGORIES)  # homepage + mission + history + categories
    print(f"Pages created: {total_pages} (homepage + {len(CATEGORIES)} categories + mission + history)")
    print("\n✅ To view locally: open index.html in your browser")
    print("✅ To deploy: push to GitHub\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌐 GENERATING WEBSITE (v4.0)")
    print("=" * 60 + "\n")

    articles = load_analyzed_articles()
    generate_homepage(articles)
    generate_category_pages(articles)
    generate_history_page(articles)
    generate_mission_page()
    generate_sitemap()
    print_summary(articles)
