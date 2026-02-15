#!/usr/bin/env python3
"""
Generate "Best X" roundup pages from data/best_of.json.

Each roundup produces a page at site/tools/{slug}/index.html with:
- Quick picks summary with award badges
- Detailed review cards for each pick
- Methodology section
- Internal links
- FAQ section with FAQPage schema
- Full SEO meta tags + BreadcrumbList schema
"""

import json
import os
import sys

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from templates import get_html_head, get_nav_html, get_footer_html, BASE_URL


def load_best_of():
    """Load best-of data from JSON file."""
    data_path = os.path.join(os.path.dirname(script_dir), 'data', 'best_of.json')
    with open(data_path, 'r') as f:
        return json.load(f)


def generate_faq_schema(faqs):
    """Generate FAQPage JSON-LD schema."""
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


def generate_breadcrumb_schema(slug, display_name):
    """Generate BreadcrumbList JSON-LD schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Tools", "item": f"{BASE_URL}/tools/"},
            {"@type": "ListItem", "position": 3, "name": display_name, "item": f"{BASE_URL}/tools/{slug}/"}
        ]
    }
    return json.dumps(schema, indent=2)


def generate_itemlist_schema(entry):
    """Generate ItemList JSON-LD schema for the picks."""
    items = []
    for i, pick in enumerate(entry['picks'], 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": pick['name'],
            "url": pick['url']
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": entry['title'],
        "description": entry['meta_description'],
        "numberOfItems": len(entry['picks']),
        "itemListElement": items
    }
    return json.dumps(schema, indent=2)


def generate_best_of_page(entry):
    """Generate a full best-of roundup page HTML."""
    slug = entry['slug']

    # Schema markup
    breadcrumb_schema = generate_breadcrumb_schema(slug, entry['title'])
    faq_schema = generate_faq_schema(entry['faqs'])
    itemlist_schema = generate_itemlist_schema(entry)

    extra_head = f'''
    <!-- BreadcrumbList Schema -->
    <script type="application/ld+json">
    {breadcrumb_schema}
    </script>

    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {faq_schema}
    </script>

    <!-- ItemList Schema -->
    <script type="application/ld+json">
    {itemlist_schema}
    </script>
    '''

    # Build head
    page_path = f"tools/{slug}/"
    head = get_html_head(
        title=entry['title'],
        description=entry['meta_description'],
        page_path=page_path,
        extra_head=extra_head
    )

    # Build nav
    nav = get_nav_html(active_page='tools')

    # Build footer
    footer = get_footer_html()

    # Intro paragraphs
    intro_html = '\n            '.join(f'<p>{p}</p>' for p in entry['intro'])

    # Quick picks summary
    quick_picks_html = ''
    for i, pick in enumerate(entry['picks'], 1):
        quick_picks_html += f'''
              <div class="quick-pick">
                <span class="quick-pick__number">{i}</span>
                <div class="quick-pick__info">
                  <span class="quick-pick__name">{pick['name']}</span>
                  <span class="quick-pick__award">{pick['award']}</span>
                </div>
                <span class="quick-pick__price">{pick['price']}</span>
              </div>'''

    # Detailed pick cards
    pick_cards_html = ''
    for i, pick in enumerate(entry['picks'], 1):
        pick_cards_html += f'''
          <div class="pick-card" id="pick-{i}">
            <div class="pick-card__header">
              <div class="pick-card__rank">#{i}</div>
              <div class="pick-card__title-group">
                <h3 class="pick-card__name">{pick['name']}</h3>
                <span class="pick-card__award-badge">{pick['award']}</span>
              </div>
              <div class="pick-card__price">{pick['price']}</div>
            </div>
            <div class="pick-card__body">
              <p>{pick['summary']}</p>
              <div class="pick-card__detail">
                <strong>Best for:</strong> {pick['best_for']}
              </div>
              <div class="pick-card__detail pick-card__caveat">
                <strong>Caveat:</strong> {pick['caveat']}
              </div>
            </div>
            <div class="pick-card__footer">
              <a href="{pick['url']}" target="_blank" rel="noopener" class="btn btn-gold">Visit {pick['name']} &rarr;</a>
            </div>
          </div>'''

    # Internal links
    internal_links_html = ''
    for link in entry.get('internal_links', []):
        internal_links_html += f'''
              <a href="{link['url']}" class="related-link">{link['text']} &rarr;</a>'''

    # FAQ details
    faq_details_html = ''
    for faq in entry['faqs']:
        faq_details_html += f'''
            <details class="faq-item">
              <summary>{faq['question']}</summary>
              <p>{faq['answer']}</p>
            </details>'''

    # Page-specific CSS
    best_of_css = '''
    <style>
    /* Best-of page layout */
    .bestof-header {
      padding: 60px 0 40px;
      max-width: 800px;
      margin: 0 auto;
    }
    .bestof-header .page-label {
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 12px;
    }
    .bestof-header h1 {
      font-size: 2.25rem;
      font-weight: 700;
      margin-bottom: 12px;
    }
    .bestof-header .subtitle {
      color: var(--text-secondary);
      font-size: 1.1rem;
      line-height: 1.7;
      max-width: 700px;
    }
    .bestof-header .date {
      color: var(--text-muted);
      font-size: 0.875rem;
      margin-top: 12px;
    }

    /* Intro */
    .bestof-intro {
      max-width: 800px;
      margin: 0 auto 48px;
    }
    .bestof-intro p {
      color: var(--text-secondary);
      line-height: 1.8;
      margin-bottom: 16px;
      font-size: 1.0625rem;
    }

    /* Quick picks summary */
    .quick-picks {
      max-width: 800px;
      margin: 0 auto 48px;
      background: linear-gradient(135deg, var(--teal-primary) 0%, var(--bg-card) 100%);
      border: 1px solid var(--teal-light);
      border-radius: 16px;
      padding: 32px;
    }
    .quick-picks h2 {
      font-size: 1.25rem;
      color: var(--gold);
      margin-bottom: 20px;
    }
    .quick-pick {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 12px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .quick-pick:last-child {
      border-bottom: none;
      padding-bottom: 0;
    }
    .quick-pick__number {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--gold);
      width: 32px;
      flex-shrink: 0;
      text-align: center;
    }
    .quick-pick__info {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .quick-pick__name {
      font-weight: 600;
      color: var(--text-primary);
      font-size: 1rem;
    }
    .quick-pick__award {
      display: inline-block;
      padding: 2px 10px;
      background: rgba(232, 168, 124, 0.15);
      color: var(--gold);
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .quick-pick__price {
      color: var(--text-muted);
      font-size: 0.875rem;
      flex-shrink: 0;
      text-align: right;
    }

    /* Pick cards */
    .picks-section {
      max-width: 800px;
      margin: 0 auto;
    }
    .picks-section > h2 {
      font-size: 1.5rem;
      margin-bottom: 24px;
    }
    .pick-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      margin-bottom: 24px;
      overflow: hidden;
      transition: border-color 0.25s ease;
    }
    .pick-card:hover {
      border-color: var(--teal-light);
    }
    .pick-card__header {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 24px 28px;
      border-bottom: 1px solid var(--border);
      flex-wrap: wrap;
    }
    .pick-card__rank {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--gold);
      flex-shrink: 0;
    }
    .pick-card__title-group {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      min-width: 0;
    }
    .pick-card__name {
      font-size: 1.25rem;
      font-weight: 600;
      color: var(--text-primary);
      margin: 0;
    }
    .pick-card__award-badge {
      display: inline-block;
      padding: 4px 12px;
      background: var(--gold);
      color: var(--bg-darker);
      border-radius: 6px;
      font-size: 0.6875rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      white-space: nowrap;
    }
    .pick-card__price {
      color: var(--text-muted);
      font-size: 0.9375rem;
      flex-shrink: 0;
    }
    .pick-card__body {
      padding: 24px 28px;
    }
    .pick-card__body > p {
      color: var(--text-secondary);
      line-height: 1.8;
      margin-bottom: 20px;
    }
    .pick-card__detail {
      padding: 12px 16px;
      background: var(--bg-darker);
      border-radius: 8px;
      margin-bottom: 12px;
      color: var(--text-secondary);
      line-height: 1.7;
      font-size: 0.9375rem;
    }
    .pick-card__detail strong {
      color: var(--success);
    }
    .pick-card__caveat strong {
      color: var(--warning);
    }
    .pick-card__footer {
      padding: 0 28px 24px;
    }

    /* Methodology */
    .methodology-section {
      max-width: 800px;
      margin: 48px auto;
      padding-top: 32px;
      border-top: 1px solid var(--border);
    }
    .methodology-section h2 {
      font-size: 1.25rem;
      margin-bottom: 12px;
    }
    .methodology-section p {
      color: var(--text-secondary);
      line-height: 1.8;
    }

    /* Related links */
    .related-section {
      max-width: 800px;
      margin: 48px auto;
      padding-top: 32px;
      border-top: 1px solid var(--border);
    }
    .related-section h2 {
      font-size: 1.25rem;
      margin-bottom: 16px;
    }
    .related-links-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
    }
    .related-link {
      display: block;
      padding: 16px 20px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 10px;
      color: var(--text-primary);
      font-weight: 500;
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .related-link:hover {
      border-color: var(--teal-light);
      background: var(--bg-card-hover);
      transform: translateY(-1px);
      color: var(--gold-light);
    }

    /* FAQ section */
    .faq-section {
      max-width: 800px;
      margin: 48px auto;
      padding-top: 32px;
      border-top: 1px solid var(--border);
    }
    .faq-section h2 {
      font-size: 1.5rem;
      margin-bottom: 16px;
    }
    .faq-item {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 12px 20px;
      margin-bottom: 8px;
    }
    .faq-item summary {
      cursor: pointer;
      font-weight: 600;
      font-size: 1.0625rem;
      color: var(--text-primary);
      list-style: none;
      padding: 4px 0;
    }
    .faq-item summary::-webkit-details-marker {
      display: none;
    }
    .faq-item summary::before {
      content: '+';
      display: inline-block;
      width: 24px;
      color: var(--gold);
      font-weight: 700;
      font-size: 1.125rem;
    }
    .faq-item[open] summary::before {
      content: '\\2212';
    }
    .faq-item p {
      margin-top: 8px;
      color: var(--text-secondary);
      line-height: 1.7;
      padding-left: 24px;
    }

    /* Newsletter CTA */
    .newsletter-cta {
      max-width: 600px;
      margin: 48px auto;
      text-align: center;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
    }
    .newsletter-cta h2 {
      font-size: 1.25rem;
      margin-bottom: 8px;
    }
    .newsletter-cta p {
      color: var(--text-secondary);
      margin-bottom: 16px;
    }
    .newsletter-cta form {
      display: flex;
      gap: 8px;
      justify-content: center;
    }
    .newsletter-cta input {
      padding: 10px 16px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg-darker);
      color: var(--text-primary);
      font-size: 0.9375rem;
      width: 240px;
    }
    .newsletter-cta button {
      padding: 10px 20px;
      border-radius: 8px;
      border: none;
      background: var(--gold);
      color: var(--bg-darker);
      font-weight: 600;
      cursor: pointer;
      transition: background 0.15s ease;
    }
    .newsletter-cta button:hover {
      background: var(--gold-hover);
    }

    /* Disclosure */
    .affiliate-disclosure {
      max-width: 800px;
      margin: 0 auto 32px;
      font-size: 0.8125rem;
      color: var(--text-muted);
      padding: 12px 16px;
      background: var(--bg-darker);
      border-radius: 8px;
    }

    /* Responsive */
    @media (max-width: 700px) {
      .bestof-header h1 {
        font-size: 1.75rem;
      }
      .quick-pick {
        flex-wrap: wrap;
      }
      .quick-pick__price {
        width: 100%;
        text-align: left;
        padding-left: 48px;
      }
      .pick-card__header {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
      }
      .pick-card__price {
        font-size: 0.875rem;
      }
      .related-links-grid {
        grid-template-columns: 1fr;
      }
      .newsletter-cta form {
        flex-direction: column;
        align-items: center;
      }
      .newsletter-cta input {
        width: 100%;
      }
    }
    </style>
    '''

    # Assemble page
    html = f'''{head}
{nav}

    {best_of_css}

    <main>
      <article>
        <div class="bestof-header">
          <div class="page-label">Best Of Roundup</div>
          <h1>{entry['h1']}</h1>
          <p class="subtitle">{entry['subtitle']}</p>
          <p class="date">Last updated: {entry.get('date_updated', 'February 2026')}</p>
        </div>

        <div class="bestof-intro">
            {intro_html}
        </div>

        <div class="quick-picks">
          <h2>Our Top Picks</h2>
          {quick_picks_html}
        </div>

        <div class="picks-section">
          <h2>Detailed Reviews</h2>
          {pick_cards_html}
        </div>

        <div class="methodology-section">
          <h2>How We Tested</h2>
          <p>{entry['methodology']}</p>
        </div>

        <div class="related-section">
          <h2>Related Comparisons &amp; Guides</h2>
          <div class="related-links-grid">
            {internal_links_html}
          </div>
        </div>

        <div class="faq-section">
          <h2>Frequently Asked Questions</h2>
          {faq_details_html}
        </div>

        <div class="affiliate-disclosure">
          <strong>Disclosure:</strong> Some links on this page may be affiliate links. If you sign up through our links, we may earn a commission at no extra cost to you. Our recommendations are based on real-world testing, not sponsorships.
        </div>
      </article>

      <!-- Newsletter CTA -->
      <div class="newsletter-cta">
        <h2>Get Tool Reviews in Your Inbox</h2>
        <p>Weekly AI tool updates, new releases, and honest comparisons.</p>
        <form action="https://ainewsdigest.substack.com/subscribe" method="get" target="_blank">
          <input type="email" name="email" placeholder="your@email.com" required>
          <button type="submit">Subscribe Free</button>
        </form>
      </div>
    </main>

{footer}'''

    return html


def main():
    entries = load_best_of()
    output_base = os.path.join(os.path.dirname(script_dir), 'site', 'tools')

    generated = 0
    for entry in entries:
        slug = entry['slug']
        output_dir = os.path.join(output_base, slug)
        os.makedirs(output_dir, exist_ok=True)

        html = generate_best_of_page(entry)
        output_path = os.path.join(output_dir, 'index.html')

        with open(output_path, 'w') as f:
            f.write(html)

        print(f"  Generated: /tools/{slug}/")
        generated += 1

    print(f"\nTotal best-of pages generated: {generated}")


if __name__ == '__main__':
    main()
