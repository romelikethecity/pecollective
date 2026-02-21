#!/usr/bin/env python3
"""
Generate tool review pages from data/tool_reviews.json.

Each review produces a page at site/tools/{slug}/index.html with:
- Two-column layout (main content + sidebar)
- Rating display, pricing table, quick facts
- Pros/cons cards, verdict box
- FAQ section with FAQPage schema
- SoftwareApplication + Review JSON-LD schema
- BreadcrumbList schema
- Full SEO meta tags

Matches the visual design of the hand-built Cursor review page,
using the external style.css stylesheet and inline tool-review CSS.
"""

import json
import os
import sys

# Project paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
SITE_DIR = os.path.join(PROJECT_ROOT, 'site')

# Add scripts directory to path
sys.path.insert(0, SCRIPT_DIR)

from nav_config import NAV_ITEMS, SITE_NAME, COPYRIGHT_YEAR

BASE_URL = 'https://pecollective.com'


def load_reviews():
    """Load tool review data from JSON file."""
    data_path = os.path.join(DATA_DIR, 'tool_reviews.json')
    with open(data_path, 'r') as f:
        return json.load(f)


def generate_faq_schema(faqs):
    """Generate FAQPage JSON-LD schema."""
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return json.dumps(schema, indent=4)


def generate_breadcrumb_schema(tool_name, slug):
    """Generate BreadcrumbList JSON-LD schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Tools", "item": f"{BASE_URL}/tools/"},
            {"@type": "ListItem", "position": 3, "name": tool_name, "item": f"{BASE_URL}/tools/{slug}/"}
        ]
    }
    return json.dumps(schema, indent=4)


def generate_software_review_schema(review):
    """Generate SoftwareApplication + Review JSON-LD schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": review["name"],
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": review.get("operating_system", "Windows, macOS, Linux"),
        "url": review["url"],
        "review": {
            "@type": "Review",
            "author": {
                "@type": "Person",
                "name": "Rome Thorndike"
            },
            "publisher": {
                "@type": "Organization",
                "name": "PE Collective"
            },
            "datePublished": review.get("date_published", "2026-02-20"),
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": review["rating"],
                "bestRating": "5"
            },
            "reviewBody": review.get("verdict", "").replace("<p>", "").replace("</p>", " ").strip()[:500]
        }
    }
    return json.dumps(schema, indent=4)


def generate_pricing_rows(pricing):
    """Generate pricing table HTML rows."""
    rows = []
    for item in pricing:
        rows.append(f'''                <div class="pricing-row">
                  <span class="pricing-row__label">{item["label"]}</span>
                  <span class="pricing-row__value">{item["value"]}</span>
                </div>''')
    return '\n'.join(rows)


def generate_quick_facts_rows(facts):
    """Generate quick facts HTML rows."""
    rows = []
    for item in facts:
        rows.append(f'''                <div class="pricing-row">
                  <span class="pricing-row__label">{item["label"]}</span>
                  <span class="pricing-row__value">{item["value"]}</span>
                </div>''')
    return '\n'.join(rows)


def generate_pros_list(pros):
    """Generate pros list items."""
    items = []
    for pro in pros:
        items.append(f'                  <li>{pro}</li>')
    return '\n'.join(items)


def generate_cons_list(cons):
    """Generate cons list items."""
    items = []
    for con in cons:
        items.append(f'                  <li>{con}</li>')
    return '\n'.join(items)


def generate_ideal_for_list(items):
    """Generate ideal-for list items."""
    result = []
    for item in items:
        result.append(f'              <li>{item}</li>')
    return '\n'.join(result)


def generate_related_tools(tools):
    """Generate related tools links."""
    links = []
    for tool in tools:
        links.append(f'                <a href="{tool["url"]}">{tool["icon"]} {tool["name"]}</a>')
    return '\n'.join(links)


def generate_faq_html(faqs):
    """Generate FAQ accordion HTML."""
    items = []
    for faq in faqs:
        items.append(f'''          <details style="background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden;">
            <summary style="padding: var(--space-lg); font-weight: 600; cursor: pointer; color: var(--color-text-primary);">{faq["question"]}</summary>
            <p style="padding: 0 var(--space-lg) var(--space-lg); color: var(--color-text-secondary); line-height: 1.7;">{faq["answer"]}</p>
          </details>''')
    return '\n'.join(items)


def generate_nav_html():
    """Generate the header navigation matching the Cursor page's style.css classes."""
    # Build desktop nav links
    nav_links = []
    for item in NAV_ITEMS:
        active = ' class="active"' if item['href'].strip('/') == 'tools' else ''
        nav_links.append(f'          <a href="{item["href"]}"{active}>{item["label"]}</a>')
    desktop_nav = '\n'.join(nav_links)

    # Build mobile nav links
    mobile_links = []
    for item in NAV_ITEMS:
        mobile_links.append(f'      <li><a href="{item["href"]}">{item["label"]}</a></li>')
    mobile_nav = '\n'.join(mobile_links)

    return f'''  <a href="#main" class="skip-link">Skip to main content</a>

  <!-- Header -->
  <header class="header">
    <div class="container">
      <div class="header__inner">
        <a href="../../" class="header__logo">
          <img src="../../assets/logo.jpeg" alt="PE Collective Logo">
          <span>PE Collective</span>
        </a>

        <nav class="header__nav">
{desktop_nav}
        </nav>

        <div class="header__cta">
          <a href="../../join/" class="btn btn--secondary btn--small">Join Community</a>
          <a href="https://ainewsdigest.substack.com" target="_blank" rel="noopener" class="btn btn--primary btn--small">Newsletter</a>
        </div>
        <button class="header__menu-btn" aria-label="Open menu">&#9776;</button>
      </div>
    </div>
  </header>

  <div class="header__mobile-overlay"></div>
  <nav class="header__mobile-nav" aria-label="Mobile navigation">
    <div class="header__mobile-nav-top">
      <span>PE Collective</span>
      <button class="header__mobile-close" aria-label="Close menu">&#10005;</button>
    </div>
    <ul class="header__mobile-links">
{mobile_nav}
    </ul>
    <a href="../../join/" class="header__mobile-cta">Join Community</a>
  </nav>
  <script>
  (function(){{
    var b=document.querySelector('.header__menu-btn'),c=document.querySelector('.header__mobile-close'),o=document.querySelector('.header__mobile-overlay'),n=document.querySelector('.header__mobile-nav');
    function open(){{n.classList.add('active');o.classList.add('active');document.body.style.overflow='hidden';}}
    function close(){{n.classList.remove('active');o.classList.remove('active');document.body.style.overflow='';}}
    if(b)b.addEventListener('click',open);if(c)c.addEventListener('click',close);if(o)o.addEventListener('click',close);
    document.querySelectorAll('.header__mobile-links a,.header__mobile-cta').forEach(function(l){{l.addEventListener('click',close);}});
  }})();
  </script>'''


def generate_footer_html(slug):
    """Generate footer HTML matching the Cursor page's style."""
    return f'''  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div class="footer__brand">
          <a href="../../" class="footer__logo">
            <img src="../../assets/logo.jpeg" alt="PE Collective">
            <span>PE Collective</span>
          </a>
          <p class="footer__tagline">
            The job board and community built by AI professionals, for AI professionals.
          </p>
        </div>

        <div class="footer__column">
          <h4>Jobs</h4>
          <nav class="footer__links">
            <a href="../../jobs/">All Jobs</a>
            <a href="../../jobs/?category=prompt-engineer">Prompt Engineer</a>
            <a href="../../jobs/?category=ai-engineer">AI Engineer</a>
            <a href="../../jobs/?remote=true">Remote Only</a>
          </nav>
        </div>

        <div class="footer__column">
          <h4>Tools</h4>
          <nav class="footer__links">
            <a href="../">All Tools</a>
            <a href="../cursor/">Cursor</a>
            <a href="../github-copilot/">GitHub Copilot</a>
          </nav>
        </div>

        <div class="footer__column">
          <h4>Community</h4>
          <nav class="footer__links">
            <a href="../../join/">Join Us</a>
            <a href="../../about/">About</a>
            <a href="https://ainewsdigest.substack.com" target="_blank" rel="noopener">Newsletter</a>
          </nav>
        </div>
      </div>

      <div class="footer__bottom">
        <span>&copy; {COPYRIGHT_YEAR} PE Collective. Built with &#129504; for the AI community.</span>
        <span>Part of the <a href="https://ainewsdigest.substack.com" target="_blank" rel="noopener">AI News Digest</a> network.</span>
      </div>
    </div>
  </footer>
<script src="/assets/js/tracking.js" defer></script>'''


# The tool-review inline CSS block (matches Cursor review page exactly)
TOOL_REVIEW_CSS = '''  <style>
    .tool-review {
      padding: var(--space-3xl) 0;
    }

    .tool-review__header {
      display: flex;
      align-items: flex-start;
      gap: var(--space-xl);
      margin-bottom: var(--space-2xl);
      padding-bottom: var(--space-2xl);
      border-bottom: 1px solid var(--color-border);
    }

    .tool-review__icon {
      width: 80px;
      height: 80px;
      background: var(--color-bg-card);
      border-radius: var(--radius-lg);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2.5rem;
      flex-shrink: 0;
    }

    .tool-review__meta {
      flex: 1;
    }

    .tool-review__category {
      font-size: 0.875rem;
      color: var(--color-gold);
      margin-bottom: var(--space-xs);
    }

    .tool-review__title {
      margin-bottom: var(--space-sm);
    }

    .tool-review__subtitle {
      font-size: 1.125rem;
      margin-bottom: var(--space-md);
    }

    .tool-review__actions {
      display: flex;
      gap: var(--space-sm);
      flex-wrap: wrap;
    }

    .tool-review__content {
      display: grid;
      grid-template-columns: 1fr 300px;
      gap: var(--space-3xl);
    }

    @media (max-width: 900px) {
      .tool-review__content {
        grid-template-columns: 1fr;
      }

      .tool-review__header {
        flex-direction: column;
      }
    }

    .tool-review__main h2 {
      font-size: 1.5rem;
      margin: var(--space-2xl) 0 var(--space-md);
      padding-top: var(--space-lg);
      border-top: 1px solid var(--color-border);
    }

    .tool-review__main h2:first-child {
      margin-top: 0;
      padding-top: 0;
      border-top: none;
    }

    .tool-review__main h3 {
      font-size: 1.125rem;
      margin: var(--space-lg) 0 var(--space-sm);
    }

    .tool-review__main p {
      margin-bottom: var(--space-md);
      line-height: 1.7;
    }

    .tool-review__main ul, .tool-review__main ol {
      margin-bottom: var(--space-md);
      padding-left: var(--space-lg);
      color: var(--color-text-secondary);
    }

    .tool-review__main li {
      margin-bottom: var(--space-sm);
    }

    .tool-review__sidebar {
      display: flex;
      flex-direction: column;
      gap: var(--space-lg);
    }

    .sidebar-card {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-lg);
    }

    .sidebar-card__title {
      font-size: 0.875rem;
      font-weight: 600;
      color: var(--color-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: var(--space-md);
    }

    .pricing-table {
      display: flex;
      flex-direction: column;
      gap: var(--space-sm);
    }

    .pricing-row {
      display: flex;
      justify-content: space-between;
      padding: var(--space-sm) 0;
      border-bottom: 1px solid var(--color-border-light);
    }

    .pricing-row:last-child {
      border-bottom: none;
    }

    .pricing-row__label {
      color: var(--color-text-secondary);
    }

    .pricing-row__value {
      font-weight: 600;
      color: var(--color-text-primary);
    }

    .pros-cons {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--space-lg);
      margin: var(--space-lg) 0;
    }

    @media (max-width: 600px) {
      .pros-cons {
        grid-template-columns: 1fr;
      }
    }

    .pros-cons__column h4 {
      font-size: 0.9375rem;
      margin-bottom: var(--space-md);
      display: flex;
      align-items: center;
      gap: var(--space-sm);
    }

    .pros-cons__column ul {
      list-style: none;
      padding: 0;
    }

    .pros-cons__column li {
      padding: var(--space-sm) 0;
      padding-left: var(--space-lg);
      position: relative;
      color: var(--color-text-secondary);
    }

    .pros-cons__column--pros li::before {
      content: '\\2713';
      position: absolute;
      left: 0;
      color: var(--color-success);
      font-weight: 700;
    }

    .pros-cons__column--cons li::before {
      content: '\\2717';
      position: absolute;
      left: 0;
      color: var(--color-error);
      font-weight: 700;
    }

    .rating {
      display: flex;
      align-items: center;
      gap: var(--space-sm);
    }

    .rating__stars {
      color: var(--color-gold);
      letter-spacing: 2px;
    }

    .rating__value {
      font-family: var(--font-display);
      font-weight: 700;
      color: var(--color-text-primary);
    }

    .related-tools {
      display: flex;
      flex-direction: column;
      gap: var(--space-sm);
    }

    .related-tools a {
      display: flex;
      align-items: center;
      gap: var(--space-sm);
      padding: var(--space-sm);
      background: var(--color-bg-darker);
      border-radius: var(--radius-md);
      color: var(--color-text-secondary);
      transition: all var(--transition-fast);
    }

    .related-tools a:hover {
      background: var(--color-bg-card-hover);
      color: var(--color-text-primary);
    }

    .verdict-box {
      background: linear-gradient(135deg, var(--color-teal-primary) 0%, var(--color-bg-card) 100%);
      border: 1px solid var(--color-teal-light);
      border-radius: var(--radius-lg);
      padding: var(--space-xl);
      margin: var(--space-2xl) 0;
    }

    .verdict-box h3 {
      color: var(--color-gold);
      margin-bottom: var(--space-md);
    }

    .affiliate-disclosure {
      font-size: 0.8125rem;
      color: var(--color-text-muted);
      padding: var(--space-md);
      background: var(--color-bg-darker);
      border-radius: var(--radius-md);
      margin-top: var(--space-2xl);
    }
  </style>'''


def generate_page(review):
    """Generate a complete tool review page."""
    slug = review['slug']
    name = review['name']

    # Build comparison CTA button if present
    comparison_btn = ''
    if review.get('comparison_cta'):
        cta = review['comparison_cta']
        comparison_btn = f'\n              <a href="{cta["url"]}" class="btn btn--secondary">{cta["text"]}</a>'

    # Build the full HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-WMWEZTSWM0"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-WMWEZTSWM0');
  </script>

  <meta name="description" content="{review['meta_description']}">

  <title>{review['title']} | PE Collective</title>

  <meta property="og:title" content="{review['title']}">
  <meta property="og:description" content="{review['og_description']}">
  <meta property="og:image" content="https://pecollective.com/assets/social-preview.png">
  <meta property="og:site_name" content="PE Collective">

  <!-- Canonical -->
  <link rel="canonical" href="{BASE_URL}/tools/{slug}/">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@pe_collective">
  <meta name="twitter:title" content="{review['title']}">
  <meta name="twitter:description" content="{review['og_description']}">
  <meta name="twitter:image" content="https://pecollective.com/assets/social-preview.png">

  <!-- BreadcrumbList Schema -->
  <script type="application/ld+json">
  {generate_breadcrumb_schema(name, slug)}
  </script>

  <!-- FAQPage Schema -->
  <script type="application/ld+json">
  {generate_faq_schema(review['faqs'])}
  </script>

  <!-- SoftwareApplication + Review Schema -->
  <script type="application/ld+json">
  {generate_software_review_schema(review)}
  </script>

  <link rel="icon" type="image/jpeg" href="../../assets/logo.jpeg">
  <link rel="apple-touch-icon" sizes="180x180" href="../../assets/logo.jpeg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Space+Grotesk:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="../../assets/css/style.css">

{TOOL_REVIEW_CSS}
</head>
<body>
{generate_nav_html()}

  <main id="main">
    <article class="tool-review">
      <div class="container">
        <!-- Header -->
        <header class="tool-review__header">
          <div class="tool-review__icon">{review['icon']}</div>
          <div class="tool-review__meta">
            <span class="tool-review__category">{review['category']}</span>
            <h1 class="tool-review__title">{review['title']}</h1>
            <p class="tool-review__subtitle">{review['subtitle']}</p>
            <div class="tool-review__actions">
              <!-- AFFILIATE LINK PLACEHOLDER -->
              <a href="{review['url']}" target="_blank" rel="noopener" class="btn btn--primary">{review['cta_text']} &rarr;</a>{comparison_btn}
            </div>
          </div>
        </header>

        <div class="tool-review__content">
          <!-- Main Content -->
          <div class="tool-review__main">
{review['content']}

            <div class="pros-cons">
              <div class="pros-cons__column pros-cons__column--pros">
                <h4>&#10003; Pros</h4>
                <ul>
{generate_pros_list(review['pros'])}
                </ul>
              </div>
              <div class="pros-cons__column pros-cons__column--cons">
                <h4>&#10007; Cons</h4>
                <ul>
{generate_cons_list(review['cons'])}
                </ul>
              </div>
            </div>

            <h2>Who Should Use {name}?</h2>

            <h3>Ideal For:</h3>
            <ul>
{generate_ideal_for_list(review['ideal_for'])}
            </ul>

            <h3>Maybe Not For:</h3>
            <ul>
{generate_ideal_for_list(review['not_for'])}
            </ul>

            <div class="verdict-box">
              <h3>Our Verdict</h3>
              {review['verdict']}
            </div>

            <div class="affiliate-disclosure">
              <strong>Disclosure:</strong> This review contains affiliate links. If you sign up through our links, we may earn a commission at no extra cost to you. We only recommend tools we actually use and believe in. Our reviews are based on hands-on testing, not sponsored content.
            </div>
          </div>

          <!-- Sidebar -->
          <aside class="tool-review__sidebar">
            <div class="sidebar-card">
              <h3 class="sidebar-card__title">Our Rating</h3>
              <div class="rating">
                <span class="rating__stars">{review['rating_stars']}</span>
                <span class="rating__value">{review['rating']}/5</span>
              </div>
            </div>

            <div class="sidebar-card">
              <h3 class="sidebar-card__title">Pricing</h3>
              <div class="pricing-table">
{generate_pricing_rows(review['pricing'])}
              </div>
              <!-- AFFILIATE LINK PLACEHOLDER -->
              <a href="{review['url']}" target="_blank" rel="noopener" class="btn btn--primary btn--small mt-md" style="width: 100%;">Get {name} &rarr;</a>
            </div>

            <div class="sidebar-card">
              <h3 class="sidebar-card__title">Quick Facts</h3>
              <div class="pricing-table">
{generate_quick_facts_rows(review['quick_facts'])}
              </div>
            </div>

            <div class="sidebar-card">
              <h3 class="sidebar-card__title">Related Tools</h3>
              <div class="related-tools">
{generate_related_tools(review['related_tools'])}
              </div>
            </div>
          </aside>
        </div>
      </div>
    </article>

    <!-- FAQ Section (AEO optimized) -->
    <section class="section">
      <div class="container container--narrow">
        <h2 style="color: var(--color-gold); margin-bottom: var(--space-lg);">Frequently Asked Questions</h2>
        <div style="display: flex; flex-direction: column; gap: var(--space-md);">
{generate_faq_html(review['faqs'])}
        </div>
      </div>
    </section>

    <!-- Newsletter CTA -->
    <section class="section">
      <div class="container container--narrow">
        <div class="cta-section">
          <h2 class="cta-section__title">Get Tool Reviews in Your Inbox</h2>
          <p class="cta-section__text">
            Weekly AI tool updates, new releases, and honest comparisons.
          </p>
          <form class="cta-section__form" action="https://ainewsdigest.substack.com/subscribe" method="get" target="_blank">
            <input type="email" name="email" placeholder="your@email.com" class="cta-section__input" required>
            <button type="submit" class="btn btn--primary btn--large">Subscribe Free</button>
          </form>
        </div>
      </div>
    </section>
  </main>

{generate_footer_html(slug)}
</body>
</html>
'''
    return html


def main():
    """Generate all tool review pages."""
    reviews = load_reviews()
    generated = 0

    for review in reviews:
        slug = review['slug']
        output_dir = os.path.join(SITE_DIR, 'tools', slug)
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, 'index.html')
        html = generate_page(review)

        with open(output_path, 'w') as f:
            f.write(html)

        print(f"  Generated: /tools/{slug}/index.html")
        generated += 1

    print(f"\nDone! Generated {generated} tool review pages.")


if __name__ == '__main__':
    main()
