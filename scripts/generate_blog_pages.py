#!/usr/bin/env python3
"""
Generate blog pages for PE Collective.
Reads data/blog.json and generates:
  - Individual blog post pages at site/blog/{slug}/index.html
  - Blog index page at site/blog/index.html
"""

import json
import os
import sys
from datetime import datetime

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from nav_config import NAV_ITEMS, SUBSCRIBE_LINK, SUBSCRIBE_LABEL, NEWSLETTER_LINK, NEWSLETTER_LABEL, SITE_NAME, COPYRIGHT_YEAR

BASE_URL = 'https://pecollective.com'
DATA_FILE = os.path.join(os.path.dirname(script_dir), 'data', 'blog.json')
SITE_DIR = os.path.join(os.path.dirname(script_dir), 'site')
BLOG_DIR = os.path.join(SITE_DIR, 'blog')

# Author info
AUTHOR_NAME = "Rome Thorndike"
AUTHOR_URL = "https://www.linkedin.com/in/romethorndike/"
AUTHOR_BIO = (
    '<a href="https://www.linkedin.com/in/romethorndike/" target="_blank" rel="noopener">Rome Thorndike</a> '
    'is the founder of the Prompt Engineer Collective, a community of over 1,300 prompt engineering professionals, '
    'and author of The AI News Digest, a weekly newsletter with 2,700+ subscribers. Rome brings hands-on AI/ML '
    'experience from Microsoft, where he worked with Dynamics and Azure AI/ML solutions, and later led sales at '
    'Datajoy (acquired by Databricks).'
)


def load_blog_data():
    """Load blog articles from JSON."""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def format_date_display(date_str):
    """Convert 2026-02-15 to February 15, 2026."""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt.strftime('%B %d, %Y').replace(' 0', ' ')


def get_head_html(title, description, canonical_path, og_type='article', og_title=None, og_description=None):
    """Generate the full <head> section matching existing blog pages."""
    og_title = og_title or title
    og_description = og_description or description

    return f'''<!DOCTYPE html>
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

  <meta name="description" content="{description}">

  <title>{title} | {SITE_NAME}</title>

  <link rel="canonical" href="{BASE_URL}/{canonical_path}">

  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{BASE_URL}/{canonical_path}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_description}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:locale" content="en_US">
  <meta property="og:image" content="{BASE_URL}/assets/og-blog.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{SITE_NAME} - AI jobs, salaries, and tools for prompt engineers">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@pe_collective">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{og_description}">
  <meta name="twitter:image" content="{BASE_URL}/assets/og-blog.png">
  <meta name="twitter:image:alt" content="{SITE_NAME} - AI jobs, salaries, and tools for prompt engineers">
'''


def get_breadcrumb_schema(breadcrumbs):
    """Generate BreadcrumbList JSON-LD."""
    items = []
    for i, (name, url) in enumerate(breadcrumbs, 1):
        full_url = f"{BASE_URL}{url}" if url.startswith('/') else url
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": full_url
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    return json.dumps(schema, indent=2)


def get_article_schema(article):
    """Generate Article JSON-LD schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": article.get('og_title', article['title']),
        "image": f"{BASE_URL}/assets/og-blog.png",
        "author": {
            "@type": "Person",
            "name": AUTHOR_NAME,
            "url": AUTHOR_URL
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": BASE_URL
        },
        "datePublished": article['date_published'],
        "dateModified": article['date_modified'],
        "description": article['meta_description']
    }
    return json.dumps(schema, indent=2)


def get_faq_schema(faqs):
    """Generate FAQPage JSON-LD schema."""
    if not faqs:
        return ''

    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq['answer']
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return json.dumps(schema, indent=2)


def get_header_html(active_page='blog', relative_prefix='../../'):
    """Generate header matching existing blog post pages."""
    nav_links = []
    for item in NAV_ITEMS:
        page_id = item['href'].strip('/')
        active_class = ' class="active"' if page_id == active_page else ''
        nav_links.append(f'          <a href="{relative_prefix}{page_id}/"{active_class}>{item["label"]}</a>')

    mobile_links = []
    for item in NAV_ITEMS:
        page_id = item['href'].strip('/')
        mobile_links.append(f'      <li><a href="{relative_prefix}{page_id}/">{item["label"]}</a></li>')

    # Blog link uses ../ for posts (one level up from slug dir)
    blog_nav_href = '../'
    if relative_prefix == '../':
        blog_nav_href = './'

    # Fix blog link to use relative ../ instead of ../../blog/
    nav_links_str = '\n'.join(nav_links)
    nav_links_str = nav_links_str.replace(f'href="{relative_prefix}blog/"', f'href="{blog_nav_href}"')

    mobile_links_str = '\n'.join(mobile_links)
    mobile_links_str = mobile_links_str.replace(f'href="{relative_prefix}blog/"', f'href="{blog_nav_href}"')

    return f'''<body>
  <a href="#main" class="skip-link">Skip to main content</a>

  <!-- Header -->
  <header class="header">
    <div class="container">
      <div class="header__inner">
        <a href="{relative_prefix}" class="header__logo">
          <img src="{relative_prefix}assets/logo.jpeg" alt="{SITE_NAME} Logo" width="36" height="36">
          <span>{SITE_NAME}</span>
        </a>

        <nav class="header__nav">
{nav_links_str}
        </nav>

        <div class="header__cta">
          <a href="{relative_prefix}join/" class="btn btn--secondary btn--small">{SUBSCRIBE_LABEL}</a>
          <a href="{NEWSLETTER_LINK}" target="_blank" rel="noopener" class="btn btn--primary btn--small">{NEWSLETTER_LABEL}</a>
        </div>
        <button class="header__menu-btn" aria-label="Open menu">&#9776;</button>
      </div>
    </div>
  </header>

  <div class="header__mobile-overlay"></div>
  <nav class="header__mobile-nav" aria-label="Mobile navigation">
    <div class="header__mobile-nav-top">
      <span>{SITE_NAME}</span>
      <button class="header__mobile-close" aria-label="Close menu">&#10005;</button>
    </div>
    <ul class="header__mobile-links">
{mobile_links_str}
    </ul>
    <a href="{relative_prefix}join/" class="header__mobile-cta">{SUBSCRIBE_LABEL}</a>
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
'''


def get_footer_html(relative_prefix='../../'):
    """Generate footer matching existing blog post pages."""
    blog_href = '../'
    if relative_prefix == '../':
        blog_href = './'

    return f'''
  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div class="footer__brand">
          <a href="{relative_prefix}" class="footer__logo">
            <img src="{relative_prefix}assets/logo.jpeg" alt="{SITE_NAME}" width="32" height="32">
            <span>{SITE_NAME}</span>
          </a>
          <p class="footer__tagline">
            The job board and community built by AI professionals, for AI professionals.
          </p>
        </div>

        <div class="footer__column">
          <h4>Jobs</h4>
          <nav class="footer__links">
            <a href="{relative_prefix}jobs/">All Jobs</a>
            <a href="{relative_prefix}jobs/?category=prompt-engineer">Prompt Engineer</a>
            <a href="{relative_prefix}jobs/?category=ai-engineer">AI Engineer</a>
            <a href="{relative_prefix}jobs/?remote=true">Remote Only</a>
          </nav>
        </div>

        <div class="footer__column">
          <h4>Resources</h4>
          <nav class="footer__links">
            <a href="{blog_href}">Blog</a>
            <a href="{relative_prefix}tools/">Tools</a>
            <a href="{relative_prefix}glossary/">Glossary</a>
            <a href="{relative_prefix}insights/">Market Intel</a>
          </nav>
        </div>

        <div class="footer__column">
          <h4>Community</h4>
          <nav class="footer__links">
            <a href="{relative_prefix}join/">Join Us</a>
            <a href="{relative_prefix}about/">About</a>
            <a href="{NEWSLETTER_LINK}" target="_blank" rel="noopener">Newsletter</a>
          </nav>
        </div>
      </div>

      <div class="footer__bottom">
        <span>&copy; {COPYRIGHT_YEAR} {SITE_NAME}. Built with \U0001f9e0 for the AI community.</span>
      </div>
    </div>
  </footer>
<script src="/assets/js/tracking.js" defer></script>
</body>
</html>
'''


def get_newsletter_cta():
    """Generate newsletter CTA section matching existing posts."""
    return f'''
    <!-- Newsletter CTA -->
    <section class="section">
      <div class="container container--narrow">
        <div class="cta-section">
          <h2 class="cta-section__title">Join 1,300+ Prompt Engineers</h2>
          <p class="cta-section__text">
            Get job alerts, salary insights, and weekly AI tool reviews.
          </p>
          <form class="cta-section__form" action="{NEWSLETTER_LINK}/subscribe" method="get" target="_blank">
            <input type="email" name="email" placeholder="your@email.com" class="cta-section__input" required>
            <button type="submit" class="btn btn--primary btn--large">Subscribe Free</button>
          </form>
        </div>
      </div>
    </section>'''


# =============================================================================
# INLINE CSS (matches existing blog pages exactly)
# =============================================================================

ARTICLE_CSS = '''    .article-page {
      padding: var(--space-3xl) 0;
    }

    .article-header {
      max-width: 800px;
      margin: 0 auto var(--space-3xl);
      text-align: center;
    }

    .article-header__category {
      font-size: 0.875rem;
      color: var(--color-gold);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: var(--space-sm);
    }

    .article-header__title {
      font-size: 2.5rem;
      line-height: 1.2;
      margin-bottom: var(--space-md);
    }

    @media (max-width: 768px) {
      .article-header__title {
        font-size: 1.75rem;
      }
    }

    .article-header__meta {
      color: var(--color-text-muted);
      font-size: 0.9375rem;
    }

    .article-header__meta a {
      color: var(--color-gold);
    }

    .article-content {
      max-width: 720px;
      margin: 0 auto;
    }

    .article-content h2 {
      font-size: 1.5rem;
      margin: var(--space-3xl) 0 var(--space-md);
      padding-top: var(--space-xl);
      border-top: 1px solid var(--color-border);
    }

    .article-content h2:first-child {
      margin-top: 0;
      padding-top: 0;
      border-top: none;
    }

    .article-content h3 {
      font-size: 1.125rem;
      margin: var(--space-xl) 0 var(--space-sm);
      color: var(--color-gold);
    }

    .article-content p {
      margin-bottom: var(--space-md);
      line-height: 1.8;
      color: var(--color-text-secondary);
    }

    .article-content ul, .article-content ol {
      margin-bottom: var(--space-lg);
      padding-left: var(--space-lg);
      color: var(--color-text-secondary);
    }

    .article-content li {
      margin-bottom: var(--space-sm);
      line-height: 1.7;
    }

    .article-content strong {
      color: var(--color-text-primary);
    }

    .article-content code {
      background: var(--color-bg-card);
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.875em;
    }

    .article-content pre {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      padding: var(--space-lg);
      overflow-x: auto;
      margin-bottom: var(--space-lg);
    }

    .article-content pre code {
      background: none;
      padding: 0;
    }

    .article-content details {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      margin-bottom: var(--space-sm);
      overflow: hidden;
    }

    .article-content details summary {
      padding: var(--space-md) var(--space-lg);
      cursor: pointer;
      font-weight: 600;
      color: var(--color-text-primary);
      list-style: none;
    }

    .article-content details summary::-webkit-details-marker {
      display: none;
    }

    .article-content details summary::before {
      content: '+';
      display: inline-block;
      width: 1.5em;
      color: var(--color-gold);
      font-weight: 700;
    }

    .article-content details[open] summary::before {
      content: '\\2212';
    }

    .article-content details p {
      padding: 0 var(--space-lg) var(--space-md);
      margin-bottom: 0;
    }

    .technique-card {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-lg);
      margin-bottom: var(--space-lg);
    }

    .technique-card__title {
      font-size: 1rem;
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: var(--space-sm);
    }

    .technique-card__description {
      color: var(--color-text-secondary);
      margin-bottom: var(--space-md);
    }

    .technique-card__example {
      background: var(--color-bg-darker);
      border-radius: var(--radius-md);
      padding: var(--space-md);
      font-family: monospace;
      font-size: 0.875rem;
      color: var(--color-text-muted);
    }

    .rate-card {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-lg);
      margin-bottom: var(--space-lg);
    }

    .rate-card__title {
      font-size: 1rem;
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: var(--space-sm);
    }

    .rate-card__range {
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--color-gold);
      margin-bottom: var(--space-sm);
    }

    .rate-card__description {
      color: var(--color-text-secondary);
      font-size: 0.9375rem;
    }

    .platform-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: var(--space-md);
      margin: var(--space-lg) 0;
    }

    .platform-card {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-lg);
    }

    .platform-card__name {
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: var(--space-xs);
    }

    .platform-card__type {
      font-size: 0.8125rem;
      color: var(--color-gold);
      margin-bottom: var(--space-sm);
    }

    .platform-card__description {
      color: var(--color-text-secondary);
      font-size: 0.9375rem;
    }

    .best-practice {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-left: 4px solid var(--color-gold);
      border-radius: var(--radius-lg);
      padding: var(--space-lg);
      margin-bottom: var(--space-lg);
    }

    .best-practice__number {
      font-size: 0.8125rem;
      font-weight: 700;
      color: var(--color-gold);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: var(--space-xs);
    }

    .best-practice__title {
      font-size: 1.125rem;
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: var(--space-sm);
    }

    .best-practice__content {
      color: var(--color-text-secondary);
      line-height: 1.7;
    }

    .example-box {
      background: var(--color-bg-darker);
      border-radius: var(--radius-md);
      padding: var(--space-md);
      margin: var(--space-md) 0;
    }

    .example-box__label {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--color-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: var(--space-xs);
    }

    .example-box__bad {
      color: var(--color-error);
      font-family: monospace;
      font-size: 0.9375rem;
      margin-bottom: var(--space-md);
      padding-bottom: var(--space-md);
      border-bottom: 1px solid var(--color-border);
    }

    .example-box__good {
      color: var(--color-success);
      font-family: monospace;
      font-size: 0.9375rem;
    }

    .mistake-card {
      background: rgba(248, 113, 113, 0.1);
      border: 1px solid rgba(248, 113, 113, 0.3);
      border-radius: var(--radius-lg);
      padding: var(--space-lg);
      margin-bottom: var(--space-lg);
    }

    .mistake-card__title {
      color: var(--color-error);
      font-weight: 600;
      margin-bottom: var(--space-sm);
    }

    .mistake-card__content {
      color: var(--color-text-secondary);
    }

    .author-bio {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-xl);
      margin-top: var(--space-3xl);
      display: flex;
      gap: var(--space-lg);
      align-items: flex-start;
    }

    @media (max-width: 600px) {
      .author-bio {
        flex-direction: column;
      }
    }

    .author-bio__avatar {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: var(--color-bg-darker);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      flex-shrink: 0;
    }

    .author-bio__content {
      flex: 1;
    }

    .author-bio__name {
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: var(--space-xs);
    }

    .author-bio__text {
      color: var(--color-text-secondary);
      font-size: 0.9375rem;
      line-height: 1.6;
    }

    .author-bio__text a {
      color: var(--color-gold);
    }

    .related-links {
      margin-top: var(--space-2xl);
      padding-top: var(--space-lg);
      border-top: 1px solid var(--color-border);
      color: var(--color-text-muted);
      font-size: 0.9375rem;
    }

    .related-links a {
      color: var(--color-gold);
    }'''

BLOG_INDEX_CSS = '''    .blog-header {
      text-align: center;
      padding: var(--space-3xl) 0;
      border-bottom: 1px solid var(--color-border);
    }

    .blog-header__title {
      font-size: 2.5rem;
      margin-bottom: var(--space-md);
    }

    .blog-header__description {
      color: var(--color-text-secondary);
      font-size: 1.125rem;
      max-width: 600px;
      margin: 0 auto;
    }

    .blog-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: var(--space-xl);
      padding: var(--space-3xl) 0;
    }

    @media (max-width: 768px) {
      .blog-grid {
        grid-template-columns: 1fr;
      }
    }

    .blog-card {
      background: var(--color-bg-card);
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-xl);
      transition: all var(--transition-base);
      display: flex;
      flex-direction: column;
    }

    .blog-card:hover {
      border-color: var(--color-teal-light);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }

    .blog-card__category {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--color-gold);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: var(--space-sm);
    }

    .blog-card__title {
      font-size: 1.25rem;
      font-weight: 600;
      color: var(--color-text-primary);
      margin-bottom: var(--space-sm);
      line-height: 1.3;
    }

    .blog-card__title a {
      color: inherit;
      text-decoration: none;
    }

    .blog-card__title a:hover {
      color: var(--color-gold);
    }

    .blog-card__excerpt {
      color: var(--color-text-secondary);
      font-size: 0.9375rem;
      line-height: 1.6;
      margin-bottom: var(--space-md);
      flex: 1;
    }

    .blog-card__meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: var(--space-md);
      border-top: 1px solid var(--color-border);
      font-size: 0.8125rem;
      color: var(--color-text-muted);
    }

    .blog-card__read-more {
      color: var(--color-gold);
      font-weight: 500;
    }

    .blog-card__read-more:hover {
      color: var(--color-gold-light);
    }'''


def generate_css_file(css_content, filename_prefix):
    """Write CSS to an inline file and return the filename."""
    import hashlib
    css_hash = hashlib.md5(css_content.encode()).hexdigest()[:8]
    filename = f"inline-{css_hash}.css"
    css_path = os.path.join(SITE_DIR, 'assets', 'css', filename)

    os.makedirs(os.path.dirname(css_path), exist_ok=True)
    with open(css_path, 'w') as f:
        f.write(css_content)

    return filename


def generate_blog_post(article, all_articles):
    """Generate a single blog post page."""
    slug = article['slug']
    canonical_path = f"blog/{slug}/"
    relative_prefix = '../../'

    # Head
    html = get_head_html(
        title=article['title'],
        description=article['meta_description'],
        canonical_path=canonical_path,
        og_type='article',
        og_title=article.get('og_title', article['title']),
        og_description=article.get('og_description', article['meta_description'])
    )

    # Breadcrumb schema
    breadcrumbs = [
        ("Home", "/"),
        ("Blog", "/blog/"),
        (article['title'].split(':')[0].strip() if ':' in article['title'] else article['title'], f"/blog/{slug}/")
    ]
    html += f'''
  <!-- BreadcrumbList Schema -->
  <script type="application/ld+json">
  {get_breadcrumb_schema(breadcrumbs)}
  </script>

  <link rel="icon" type="image/jpeg" href="{relative_prefix}assets/logo.jpeg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{relative_prefix}assets/css/style.css">

  <script type="application/ld+json">
  {get_article_schema(article)}
  </script>
'''

    # FAQ schema (if article has FAQs)
    faqs = article.get('faqs', [])
    if faqs:
        html += f'''
  <!-- FAQPage Schema -->
  <script type="application/ld+json">
  {get_faq_schema(faqs)}
  </script>
'''

    # Generate and link inline CSS
    css_filename = generate_css_file(ARTICLE_CSS, 'article')
    html += f'    <link rel="stylesheet" href="/assets/css/{css_filename}">\n'
    html += '    </head>\n'

    # Body/header
    html += get_header_html(active_page='blog', relative_prefix=relative_prefix)

    # Article
    date_display = format_date_display(article['date_published'])
    read_time = article.get('read_time', '10 min')

    html += f'''
  <main id="main">
    <article class="article-page">
      <div class="container">
        <header class="article-header">
          <span class="article-header__category">{article['category']}</span>
          <h1 class="article-header__title">{article['title']}</h1>
          <p class="article-header__meta">
            By <a href="{AUTHOR_URL}" target="_blank" rel="noopener">{AUTHOR_NAME}</a> &middot; {date_display} &middot; {read_time} read
          </p>
        </header>

        <div class="article-content">
          {article['content']}

          <!-- Author Bio -->
          <div class="author-bio">
            <div class="author-bio__avatar">RT</div>
            <div class="author-bio__content">
              <div class="author-bio__name">About the Author</div>
              <p class="author-bio__text">
                {AUTHOR_BIO}
              </p>
            </div>
          </div>

          <!-- Related Links -->
          <p class="related-links">
            Related: {' | '.join(f'<a href="{link["url"]}">{link["text"]}</a>' for link in article.get('related_links', []))}
          </p>
        </div>
      </div>
    </article>
{get_newsletter_cta()}
  </main>
'''

    # Footer
    html += get_footer_html(relative_prefix=relative_prefix)

    return html


def generate_blog_index(articles):
    """Generate the blog index page at site/blog/index.html."""
    relative_prefix = '../'
    canonical_path = 'blog/'

    html = get_head_html(
        title='Blog \u2014 Prompt Engineering Guides & Tutorials',
        description='Prompt engineering guides, tutorials, and best practices from the PE Collective community of 1,300+ AI professionals.',
        canonical_path=canonical_path,
        og_type='website',
        og_title='Blog \u2014 Prompt Engineering Guides & Tutorials',
        og_description='Prompt engineering guides, tutorials, and best practices from the PE Collective community of 1,300+ AI professionals.'
    )

    # Breadcrumb schema
    breadcrumbs = [
        ("Home", "/"),
        ("Blog", "/blog/")
    ]
    html += f'''
  <!-- BreadcrumbList Schema -->
  <script type="application/ld+json">
  {get_breadcrumb_schema(breadcrumbs)}
  </script>

  <link rel="icon" type="image/jpeg" href="{relative_prefix}assets/logo.jpeg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{relative_prefix}assets/css/style.css">
'''

    # Generate and link inline CSS
    css_filename = generate_css_file(BLOG_INDEX_CSS, 'blog-index')
    html += f'    <link rel="stylesheet" href="/assets/css/{css_filename}">\n'
    html += '    </head>\n'

    # Body/header
    html += get_header_html(active_page='blog', relative_prefix=relative_prefix)

    # Blog grid
    html += '''
  <main id="main">
    <div class="container">
      <header class="blog-header">
        <h1 class="blog-header__title">Blog</h1>
        <p class="blog-header__description">Guides, tutorials, and insights on prompt engineering from our community of 1,300+ AI professionals.</p>
      </header>

      <div class="blog-grid">
'''

    # Sort articles by date, newest first
    sorted_articles = sorted(articles, key=lambda a: a['date_published'], reverse=True)

    for article in sorted_articles:
        date_display = format_date_display(article['date_published'])
        read_time = article.get('read_time', '10 min').replace(' read', '')
        # Strip " read" if present, and also strip " min" to get just the number
        read_min = read_time.replace(' min', '').replace(' read', '').strip()

        html += f'''        <!-- Article: {article['title']} -->
        <article class="blog-card">
          <span class="blog-card__category">{article['category']}</span>
          <h2 class="blog-card__title">
            <a href="./{article['slug']}/">{article['title']}</a>
          </h2>
          <p class="blog-card__excerpt">{article['excerpt']}</p>
          <div class="blog-card__meta">
            <span>{date_display} &middot; {read_min} min</span>
            <a href="./{article['slug']}/" class="blog-card__read-more">Read more &rarr;</a>
          </div>
        </article>

'''

    html += '''      </div>
    </div>
'''

    # Newsletter CTA for index page
    html += f'''
    <!-- Newsletter CTA -->
    <section class="section">
      <div class="container container--narrow">
        <div class="cta-section">
          <h2 class="cta-section__title">Get New Articles in Your Inbox</h2>
          <p class="cta-section__text">
            Weekly AI insights, prompt engineering tips, and community updates.
          </p>
          <form class="cta-section__form" action="{NEWSLETTER_LINK}/subscribe" method="get" target="_blank">
            <input type="email" name="email" placeholder="your@email.com" class="cta-section__input" required>
            <button type="submit" class="btn btn--primary btn--large">Subscribe Free</button>
          </form>
        </div>
      </div>
    </section>
  </main>
'''

    html += get_footer_html(relative_prefix=relative_prefix)

    return html


def main():
    """Main entry point."""
    print("Loading blog data...")
    articles = load_blog_data()
    print(f"Found {len(articles)} articles")

    # Ensure blog directory exists
    os.makedirs(BLOG_DIR, exist_ok=True)

    # Generate individual blog posts
    for article in articles:
        slug = article['slug']
        post_dir = os.path.join(BLOG_DIR, slug)
        os.makedirs(post_dir, exist_ok=True)

        html = generate_blog_post(article, articles)
        output_path = os.path.join(post_dir, 'index.html')
        with open(output_path, 'w') as f:
            f.write(html)
        print(f"  Generated: blog/{slug}/index.html")

    # Generate blog index
    html = generate_blog_index(articles)
    index_path = os.path.join(BLOG_DIR, 'index.html')
    with open(index_path, 'w') as f:
        f.write(html)
    print(f"  Generated: blog/index.html")

    print(f"\nDone! Generated {len(articles)} blog posts + index page.")


if __name__ == '__main__':
    main()
