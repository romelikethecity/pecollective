#!/usr/bin/env python3
"""
Generate the AI Tools Directory hub page at site/tools/index.html.

Reads every tool data JSON file and builds a comprehensive hub page that
links to ALL existing tool pages — reviews, pricing pages, comparisons,
alternatives, and best-of lists. Replaces the hand-coded hub that was
marking existing pages as "Coming Soon" and breaking internal linking.

Sections produced:
  1. Featured Comparisons
  2. Best-Of Lists
  3. Pricing Pages (grouped by category)
  4. Tool Reviews (grouped by category)
  5. Alternatives
  6. All Comparisons

Card classes reuse the existing style.css (.tool-card, .tools-grid,
.tools-section, .comparison-card, etc.) and the existing site navigation
pattern from the old tools hub.

Run:
    python3 scripts/generate_tools_hub.py
"""

import html
import json
import os
import re
import sys
from collections import OrderedDict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
SITE_DIR = os.path.join(PROJECT_ROOT, 'site')
OUTPUT_PATH = os.path.join(SITE_DIR, 'tools', 'index.html')

BASE_URL = 'https://pecollective.com'
SITE_NAME = 'PE Collective'

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_json(name):
    path = os.path.join(DATA_DIR, f'{name}.json')
    with open(path, 'r') as f:
        return json.load(f)


def short(text, limit=160):
    """Trim text to a single-sentence-ish blurb."""
    if not text:
        return ''
    if isinstance(text, list):
        text = ' '.join(str(x) for x in text if x)
    text = re.sub(r'<[^>]+>', '', str(text))
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= limit:
        return text
    # Prefer a clean sentence break
    cut = text[:limit]
    last_period = cut.rfind('. ')
    if last_period > 60:
        return cut[: last_period + 1]
    last_space = cut.rfind(' ')
    if last_space > 0:
        cut = cut[:last_space]
    return cut.rstrip(',;:') + '…'


def esc(text):
    return html.escape(str(text or ''), quote=True)


# ---------------------------------------------------------------------------
# Category inference for pricing pages (pricing JSON has no category field)
# ---------------------------------------------------------------------------

# Map a tool_slug → category label so pricing pages can be grouped.
# Keys align with tool_reviews.json `category` values where possible.
PRICING_CATEGORY_MAP = {
    'cursor': 'Code Editors',
    'github-copilot': 'Code Editors',
    'windsurf': 'Code Editors',
    'replit': 'Code Editors',
    'openai-api': 'LLM APIs',
    'anthropic-api': 'LLM APIs',
    'cohere': 'LLM APIs',
    'aws-bedrock': 'LLM APIs',
    'gpt-4o': 'LLM APIs',
    'gpt-4o-mini': 'LLM APIs',
    'pinecone': 'Vector Databases',
    'weaviate': 'Vector Databases',
    'chroma': 'Vector Databases',
    'langchain': 'Frameworks',
}


def pricing_category(entry):
    slug = entry.get('tool_slug') or entry.get('slug', '').replace('-pricing', '')
    return PRICING_CATEGORY_MAP.get(slug, 'Other')


# ---------------------------------------------------------------------------
# Card renderers
# ---------------------------------------------------------------------------

DEFAULT_ICON = '🛠️'


def tool_review_card(entry, featured=False):
    slug = entry['slug']
    name = entry.get('name', slug)
    icon = entry.get('icon') or DEFAULT_ICON
    category = entry.get('category', 'AI Tool')
    description = short(entry.get('subtitle') or entry.get('meta_description') or '', 180)
    rating = entry.get('rating')
    rating_stars = entry.get('rating_stars')

    classes = 'tool-card tool-card--featured' if featured else 'tool-card'
    rating_html = ''
    if rating and rating_stars:
        rating_html = (
            f'<div class="tool-card__rating" aria-label="Rating {esc(rating)} of 5">'
            f'<span class="tool-card__stars">{esc(rating_stars)}</span> '
            f'<span class="tool-card__rating-num">{esc(rating)}/5</span>'
            f'</div>'
        )

    return (
        f'<a href="{esc(slug)}/" class="{classes}">'
        f'<div class="tool-card__icon">{esc(icon)}</div>'
        f'<h3 class="tool-card__name">{esc(name)}</h3>'
        f'<span class="tool-card__category">{esc(category)}</span>'
        f'{rating_html}'
        f'<p class="tool-card__description">{esc(description)}</p>'
        f'</a>'
    )


def pricing_card(entry):
    slug = entry['slug']
    tool_name = entry.get('tool_name', slug.replace('-pricing', '').title())
    tool_slug = entry.get('tool_slug', slug.replace('-pricing', ''))
    description = short(entry.get('meta_description') or entry.get('intro') or '', 170)

    # Try to extract a price range from tiers
    price_range = ''
    tiers = entry.get('tiers') or []
    prices = []
    for tier in tiers:
        if isinstance(tier, dict):
            p = tier.get('price') or tier.get('cost') or ''
            if p:
                prices.append(str(p))
    if prices:
        # Keep it short — just show first + last distinct entries
        unique = []
        for p in prices:
            if p not in unique:
                unique.append(p)
        if len(unique) == 1:
            price_range = unique[0]
        else:
            price_range = f'{unique[0]} → {unique[-1]}'

    price_html = (
        f'<div class="tool-card__price">{esc(price_range)}</div>' if price_range else ''
    )

    return (
        f'<a href="{esc(slug)}/" class="tool-card">'
        f'<span class="tool-card__category">Pricing</span>'
        f'<h3 class="tool-card__name">{esc(tool_name)} Pricing</h3>'
        f'{price_html}'
        f'<p class="tool-card__description">{esc(description)}</p>'
        f'</a>'
    )


def comparison_card(entry):
    slug = entry['slug']
    tool_a = entry.get('tool_a') or {}
    tool_b = entry.get('tool_b') or {}
    a_name = tool_a.get('name') if isinstance(tool_a, dict) else None
    b_name = tool_b.get('name') if isinstance(tool_b, dict) else None
    title_parts = slug.split('-vs-')
    if not a_name and len(title_parts) == 2:
        a_name = title_parts[0].replace('-', ' ').title()
    if not b_name and len(title_parts) == 2:
        b_name = title_parts[1].replace('-', ' ').title()
    card_title = f'{a_name} vs {b_name}' if a_name and b_name else slug.replace('-', ' ').title()
    description = short(
        entry.get('subtitle') or entry.get('meta_description') or entry.get('h1') or '',
        170,
    )

    return (
        f'<a href="{esc(slug)}/" class="comparison-card">'
        f'<span class="comparison-card__vs">VS</span>'
        f'<div>'
        f'<h3 class="comparison-card__title">{esc(card_title)}</h3>'
        f'<p class="comparison-card__description">{esc(description)}</p>'
        f'</div>'
        f'</a>'
    )


def alternatives_card(entry):
    slug = entry['slug']
    tool_name = entry.get('tool_name', slug.replace('-alternatives', '').title())
    description = short(entry.get('meta_description') or entry.get('intro') or '', 170)
    return (
        f'<a href="{esc(slug)}/" class="tool-card">'
        f'<span class="tool-card__category">Alternatives</span>'
        f'<h3 class="tool-card__name">{esc(tool_name)} Alternatives</h3>'
        f'<p class="tool-card__description">{esc(description)}</p>'
        f'</a>'
    )


def best_of_card(entry):
    slug = entry['slug']
    title = entry.get('h1') or entry.get('title') or slug.replace('-', ' ').title()
    # Strip trailing year suffix for cleaner card titles
    title = re.sub(r'\s*\(\d{4}\)\s*$', '', title)
    title = re.sub(r'\s*\d{4}\s*-\s*.*$', '', title)
    description = short(
        entry.get('subtitle') or entry.get('meta_description') or entry.get('intro') or '',
        180,
    )
    return (
        f'<a href="{esc(slug)}/" class="tool-card">'
        f'<span class="tool-card__category">Best-Of Guide</span>'
        f'<h3 class="tool-card__name">{esc(title)}</h3>'
        f'<p class="tool-card__description">{esc(description)}</p>'
        f'</a>'
    )


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

# Slugs to surface in the featured comparisons section.
FEATURED_COMPARISON_SLUGS = [
    'cursor-vs-windsurf',
    'cursor-vs-github-copilot',
    'cursor-vs-claude-code',
    'langchain-vs-llamaindex',
    'pinecone-vs-weaviate',
    'claude-vs-chatgpt-coding',
    'gpt4-vs-claude',
    'openai-api-vs-anthropic-api',
]


def build_featured_comparisons(comparisons):
    lookup = {c['slug']: c for c in comparisons}
    cards = []
    for slug in FEATURED_COMPARISON_SLUGS:
        if slug in lookup:
            cards.append(comparison_card(lookup[slug]))
    if not cards:
        return ''
    return (
        '<section class="tools-section" id="featured-comparisons">\n'
        '  <div class="container">\n'
        '    <h2 class="tools-section__title">Featured Comparisons</h2>\n'
        '    <p class="tools-section__desc">The head-to-heads our readers hit most — pricing, workflow differences, and when to pick each tool.</p>\n'
        '    <div class="comparison-cards">\n'
        '      ' + '\n      '.join(cards) + '\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def build_best_of_section(best_of):
    cards = [best_of_card(e) for e in best_of]
    return (
        '<section class="tools-section" id="best-of-lists">\n'
        '  <div class="container">\n'
        '    <h2 class="tools-section__title">Best-Of Lists</h2>\n'
        '    <p class="tools-section__desc">Curated, tested rankings across every category we cover.</p>\n'
        '    <div class="tools-grid">\n'
        '      ' + '\n      '.join(cards) + '\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def build_pricing_section(pricing):
    # Group by inferred category
    groups = OrderedDict()
    category_order = ['Code Editors', 'LLM APIs', 'Vector Databases', 'Frameworks', 'Other']
    for cat in category_order:
        groups[cat] = []
    for entry in pricing:
        cat = pricing_category(entry)
        groups.setdefault(cat, []).append(entry)

    blocks = []
    for cat in category_order:
        entries = groups.get(cat) or []
        if not entries:
            continue
        cards = [pricing_card(e) for e in entries]
        blocks.append(
            f'<h3 class="tools-subsection__title">{esc(cat)}</h3>\n'
            f'<div class="tools-grid">\n      ' + '\n      '.join(cards) + '\n    </div>'
        )

    return (
        '<section class="tools-section" id="pricing-pages">\n'
        '  <div class="container">\n'
        '    <h2 class="tools-section__title">Pricing Pages</h2>\n'
        '    <p class="tools-section__desc">Every plan, hidden cost, and credit system — broken down and updated for 2026.</p>\n'
        '    ' + '\n    '.join(blocks) + '\n'
        '  </div>\n'
        '</section>'
    )


def build_reviews_section(reviews):
    # Group by the `category` field on each review
    groups = OrderedDict()
    category_order = [
        'AI Code Editor',
        'AI Code Assistant',
        'AI Coding Agent',
        'AI Development Environment',
        'LLM Framework',
        'AI Agent Framework',
        'Vector Database',
        'AI API',
        'AI Model Hub',
        'AI Testing & Evaluation',
    ]
    for cat in category_order:
        groups[cat] = []
    for entry in reviews:
        cat = entry.get('category', 'Other')
        groups.setdefault(cat, []).append(entry)

    blocks = []
    for cat, entries in groups.items():
        if not entries:
            continue
        cards = [tool_review_card(e) for e in entries]
        blocks.append(
            f'<h3 class="tools-subsection__title">{esc(cat)}</h3>\n'
            f'<div class="tools-grid">\n      ' + '\n      '.join(cards) + '\n    </div>'
        )

    return (
        '<section class="tools-section" id="tool-reviews">\n'
        '  <div class="container">\n'
        '    <h2 class="tools-section__title">Tool Reviews</h2>\n'
        '    <p class="tools-section__desc">Hands-on reviews of the tools we actually use. Pros, cons, ratings, and where each fits.</p>\n'
        '    ' + '\n    '.join(blocks) + '\n'
        '  </div>\n'
        '</section>'
    )


def build_alternatives_section(alternatives):
    cards = [alternatives_card(e) for e in alternatives]
    return (
        '<section class="tools-section" id="alternatives">\n'
        '  <div class="container">\n'
        '    <h2 class="tools-section__title">Alternatives</h2>\n'
        '    <p class="tools-section__desc">Cheaper, different, or just better-for-you swaps for the most popular AI tools.</p>\n'
        '    <div class="tools-grid">\n'
        '      ' + '\n      '.join(cards) + '\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def build_all_comparisons_section(comparisons):
    # Sort alphabetically for predictability
    sorted_comps = sorted(comparisons, key=lambda c: c['slug'])
    cards = [comparison_card(e) for e in sorted_comps]
    return (
        '<section class="tools-section" id="all-comparisons">\n'
        '  <div class="container">\n'
        '    <h2 class="tools-section__title">All Comparisons</h2>\n'
        f'    <p class="tools-section__desc">Every head-to-head on the site ({len(sorted_comps)} comparisons).</p>\n'
        '    <div class="comparison-cards">\n'
        '      ' + '\n      '.join(cards) + '\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


# ---------------------------------------------------------------------------
# Schema builders
# ---------------------------------------------------------------------------

def build_itemlist_schema(reviews, pricing, comparisons, alternatives, best_of):
    items = []
    position = 1

    def add(slug, name):
        nonlocal position
        items.append(
            {
                '@type': 'ListItem',
                'position': position,
                'url': f'{BASE_URL}/tools/{slug}/',
                'name': name,
            }
        )
        position += 1

    for e in reviews:
        add(e['slug'], f"{e.get('name', e['slug'])} Review")
    for e in pricing:
        add(e['slug'], f"{e.get('tool_name', e['slug'])} Pricing")
    for e in comparisons:
        tool_a = e.get('tool_a') or {}
        tool_b = e.get('tool_b') or {}
        a = tool_a.get('name') if isinstance(tool_a, dict) else ''
        b = tool_b.get('name') if isinstance(tool_b, dict) else ''
        name = f'{a} vs {b}' if a and b else e.get('h1') or e['slug']
        add(e['slug'], name)
    for e in alternatives:
        add(e['slug'], f"{e.get('tool_name', e['slug'])} Alternatives")
    for e in best_of:
        title = e.get('h1') or e.get('title') or e['slug']
        add(e['slug'], title)

    return {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': 'AI Tools Directory',
        'description': 'Reviews, pricing pages, comparisons, alternatives, and best-of lists for AI tools.',
        'numberOfItems': len(items),
        'itemListElement': items,
    }


BREADCRUMB_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{BASE_URL}/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Tools', 'item': f'{BASE_URL}/tools/'},
    ],
}


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = '''<!DOCTYPE html>
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

  <meta name="description" content="{meta_description}">

  <title>AI Tools Directory — 100+ Reviews, Pricing & Comparisons | PE Collective</title>

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://pecollective.com/tools/">
  <meta property="og:title" content="AI Tools Directory — PE Collective">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:image" content="https://pecollective.com/assets/social-preview.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="PE Collective - AI jobs, salaries, and tools for prompt engineers">
  <meta property="og:site_name" content="PE Collective">
  <meta property="og:locale" content="en_US">

  <link rel="canonical" href="https://pecollective.com/tools/">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@pe_collective">
  <meta name="twitter:title" content="AI Tools Directory — PE Collective">
  <meta name="twitter:description" content="{meta_description}">
  <meta name="twitter:image" content="https://pecollective.com/assets/social-preview.png">
  <meta name="twitter:image:alt" content="PE Collective - AI jobs, salaries, and tools for prompt engineers">

  <script type="application/ld+json">
{breadcrumb_schema}
  </script>

  <script type="application/ld+json">
{itemlist_schema}
  </script>

  <link rel="icon" type="image/jpeg" href="../assets/logo.jpeg">
  <link rel="apple-touch-icon" sizes="180x180" href="../assets/logo.jpeg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Space+Grotesk:wght@400;500;600;700&display=swap" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="../assets/css/style.css">

  <style>
    .tools-header {{
      padding: var(--space-3xl) 0 var(--space-xl);
      text-align: center;
    }}
    .tools-header h1 {{
      margin-bottom: var(--space-md);
    }}
    .tools-stats {{
      display: flex;
      justify-content: center;
      gap: var(--space-xl);
      flex-wrap: wrap;
      margin-top: var(--space-xl);
      color: var(--color-text-muted);
      font-size: 0.9375rem;
    }}
    .tools-stats strong {{
      color: var(--color-gold);
      font-size: 1.25rem;
      font-family: var(--font-display);
      display: block;
    }}
    .tools-nav {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: var(--space-sm);
      margin-top: var(--space-xl);
    }}
    .tools-nav a {{
      padding: var(--space-sm) var(--space-md);
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-full);
      font-size: 0.875rem;
      color: var(--color-text-secondary);
      text-decoration: none;
      transition: all var(--transition-fast);
    }}
    .tools-nav a:hover {{
      background: var(--color-teal-primary);
      border-color: var(--color-teal-light);
      color: var(--color-text-primary);
    }}
    .tools-section {{
      padding: var(--space-2xl) 0;
    }}
    .tools-section + .tools-section {{
      border-top: 1px solid var(--color-border);
    }}
    .tools-section__title {{
      font-size: 1.5rem;
      margin-bottom: var(--space-sm);
      font-family: var(--font-display);
    }}
    .tools-section__desc {{
      color: var(--color-text-muted);
      margin-bottom: var(--space-xl);
      max-width: 720px;
    }}
    .tools-subsection__title {{
      font-size: 1rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--color-gold);
      margin: var(--space-xl) 0 var(--space-md);
      font-family: var(--font-display);
    }}
    .tools-subsection__title:first-of-type {{
      margin-top: var(--space-sm);
    }}
    .tool-card {{
      position: relative;
    }}
    .tool-card--featured {{
      background: linear-gradient(135deg, var(--color-bg-card) 0%, rgba(26, 188, 156, 0.15) 100%);
      border-color: var(--color-teal-light);
    }}
    .tool-card__rating {{
      font-size: 0.8125rem;
      color: var(--color-gold);
      margin-bottom: var(--space-sm);
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .tool-card__stars {{
      letter-spacing: 1px;
    }}
    .tool-card__rating-num {{
      color: var(--color-text-muted);
    }}
    .tool-card__price {{
      font-size: 0.875rem;
      color: var(--color-text-primary);
      font-weight: 600;
      margin-bottom: var(--space-sm);
      font-family: var(--font-display);
    }}
    .comparison-cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: var(--space-lg);
    }}
    .comparison-card {{
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-xl);
      text-decoration: none;
      transition: all var(--transition-base);
      display: flex;
      align-items: center;
      gap: var(--space-lg);
    }}
    .comparison-card:hover {{
      border-color: var(--color-teal-light);
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg);
    }}
    .comparison-card__vs {{
      font-family: var(--font-display);
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--color-gold);
      flex-shrink: 0;
    }}
    .comparison-card__title {{
      font-family: var(--font-display);
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: var(--space-xs);
      font-size: 1rem;
    }}
    .comparison-card__description {{
      font-size: 0.875rem;
      color: var(--color-text-muted);
      line-height: 1.5;
    }}
  </style>
</head>
<body>
  <a href="#main" class="skip-link">Skip to main content</a>

  <!-- Header -->
  <header class="header">
    <div class="container">
      <div class="header__inner">
        <a href="../" class="header__logo">
          <img src="../assets/logo.jpeg" alt="PE Collective Logo" width="36" height="36">
          <span>PE Collective</span>
        </a>

        <nav class="header__nav">
          <a href="../jobs/">AI Jobs</a>
          <a href="../salaries/">Salaries</a>
          <a href="./" class="active">Tools</a>
          <a href="../blog/">Blog</a>
          <a href="../insights/">Market Intel</a>
          <a href="../about/">About</a>
        </nav>

        <div class="header__cta">
          <a href="../join/" class="btn btn--secondary btn--small">Join Community</a>
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
      <li><a href="../jobs/">AI Jobs</a></li>
      <li><a href="../salaries/">Salaries</a></li>
      <li><a href="./">Tools</a></li>
      <li><a href="../blog/">Blog</a></li>
      <li><a href="../insights/">Market Intel</a></li>
      <li><a href="../about/">About</a></li>
    </ul>
    <a href="../join/" class="header__mobile-cta">Join Community</a>
  </nav>
  <script>
  (function(){{
    var b=document.querySelector('.header__menu-btn'),c=document.querySelector('.header__mobile-close'),o=document.querySelector('.header__mobile-overlay'),n=document.querySelector('.header__mobile-nav');
    function open(){{n.classList.add('active');o.classList.add('active');document.body.style.overflow='hidden';}}
    function close(){{n.classList.remove('active');o.classList.remove('active');document.body.style.overflow='';}}
    if(b)b.addEventListener('click',open);if(c)c.addEventListener('click',close);if(o)o.addEventListener('click',close);
    document.querySelectorAll('.header__mobile-links a,.header__mobile-cta').forEach(function(l){{l.addEventListener('click',close);}});
  }})();
  </script>

  <main id="main">
    <section class="tools-header">
      <div class="container">
        <h1>AI Tools Directory</h1>
        <p class="section__subtitle">{page_subtitle}</p>

        <div class="tools-stats">
          <div><strong>{review_count}</strong> Tool Reviews</div>
          <div><strong>{pricing_count}</strong> Pricing Pages</div>
          <div><strong>{comparison_count}</strong> Comparisons</div>
          <div><strong>{alternatives_count}</strong> Alternatives</div>
          <div><strong>{best_of_count}</strong> Best-Of Lists</div>
        </div>

        <nav class="tools-nav" aria-label="Jump to section">
          <a href="#featured-comparisons">Featured Comparisons</a>
          <a href="#best-of-lists">Best-Of Lists</a>
          <a href="#pricing-pages">Pricing</a>
          <a href="#tool-reviews">Reviews</a>
          <a href="#alternatives">Alternatives</a>
          <a href="#all-comparisons">All Comparisons</a>
        </nav>
      </div>
    </section>

    {featured_comparisons}

    {best_of_section}

    {pricing_section}

    {reviews_section}

    {alternatives_section}

    {all_comparisons_section}

    <!-- Newsletter CTA -->
    <section class="section">
      <div class="container container--narrow">
        <div class="cta-section">
          <h2 class="cta-section__title">Get Tool Reviews in Your Inbox</h2>
          <p class="cta-section__text">
            We cover new AI tools and updates in our weekly newsletter. No spam, unsubscribe anytime.
          </p>
          <form class="cta-section__form" action="https://ainewsdigest.substack.com/subscribe" method="get" target="_blank">
            <input type="email" name="email" placeholder="your@email.com" class="cta-section__input" required>
            <button type="submit" class="btn btn--primary btn--large">Subscribe Free</button>
          </form>
        </div>
      </div>
    </section>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div class="footer__brand">
          <a href="../" class="footer__logo">
            <img src="../assets/logo.jpeg" alt="PE Collective" width="32" height="32">
            <span>PE Collective</span>
          </a>
          <p class="footer__tagline">
            The job board and community built by AI professionals, for AI professionals.
          </p>
        </div>

        <div class="footer__column">
          <h4>Jobs</h4>
          <nav class="footer__links">
            <a href="../jobs/">All Jobs</a>
            <a href="../jobs/?category=prompt-engineer">Prompt Engineer</a>
            <a href="../jobs/?category=ai-engineer">AI Engineer</a>
            <a href="../jobs/?remote=true">Remote Only</a>
          </nav>
        </div>

        <div class="footer__column">
          <h4>Tools</h4>
          <nav class="footer__links">
            <a href="./">All Tools</a>
            <a href="cursor/">Cursor</a>
            <a href="github-copilot/">GitHub Copilot</a>
            <a href="../glossary/">Glossary</a>
          </nav>
        </div>

        <div class="footer__column">
          <h4>Community</h4>
          <nav class="footer__links">
            <a href="../join/">Join Us</a>
            <a href="../about/">About</a>
            <a href="https://ainewsdigest.substack.com" target="_blank" rel="noopener">Newsletter</a>
          </nav>
        </div>
      </div>

      <div class="footer__bottom">
        <span>&copy; 2026 PE Collective. Built with 🧠 for the AI community.</span>
        <span>Part of the <a href="https://ainewsdigest.substack.com" target="_blank" rel="noopener">AI News Digest</a> network.</span>
      </div>
    </div>
  </footer>
<script src="/assets/js/tracking.js" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    reviews = load_json('tool_reviews')
    pricing = load_json('pricing')
    comparisons = load_json('comparisons')
    alternatives = load_json('alternatives')
    best_of = load_json('best_of')

    meta_description = (
        '100+ AI tools reviewed: code editors, LLM frameworks, vector databases, '
        'embedding models, and more. Pricing data and head-to-head comparisons '
        'updated April 2026.'
    )
    page_subtitle = (
        'Reviews, pricing breakdowns, alternatives, and head-to-head comparisons for '
        'the AI tools professionals actually use. Updated continuously.'
    )

    featured_html = build_featured_comparisons(comparisons)
    best_of_html = build_best_of_section(best_of)
    pricing_html = build_pricing_section(pricing)
    reviews_html = build_reviews_section(reviews)
    alternatives_html = build_alternatives_section(alternatives)
    all_comparisons_html = build_all_comparisons_section(comparisons)

    itemlist = build_itemlist_schema(
        reviews, pricing, comparisons, alternatives, best_of
    )

    page = PAGE_TEMPLATE.format(
        meta_description=esc(meta_description),
        page_subtitle=esc(page_subtitle),
        review_count=len(reviews),
        pricing_count=len(pricing),
        comparison_count=len(comparisons),
        alternatives_count=len(alternatives),
        best_of_count=len(best_of),
        breadcrumb_schema=json.dumps(BREADCRUMB_SCHEMA, indent=2),
        itemlist_schema=json.dumps(itemlist, indent=2),
        featured_comparisons=featured_html,
        best_of_section=best_of_html,
        pricing_section=pricing_html,
        reviews_section=reviews_html,
        alternatives_section=alternatives_html,
        all_comparisons_section=all_comparisons_html,
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(page)

    # Summary
    total_pages = (
        len(reviews) + len(pricing) + len(comparisons) + len(alternatives) + len(best_of)
    )
    print(f'Generated {OUTPUT_PATH}')
    print(f'  Reviews:      {len(reviews)}')
    print(f'  Pricing:      {len(pricing)}')
    print(f'  Comparisons:  {len(comparisons)}')
    print(f'  Alternatives: {len(alternatives)}')
    print(f'  Best-Of:      {len(best_of)}')
    print(f'  Total linked: {total_pages}')


if __name__ == '__main__':
    main()
