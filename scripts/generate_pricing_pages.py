#!/usr/bin/env python3
"""
Generate pricing pages from data/pricing.json.

Each pricing page produces site/tools/{slug}/index.html with:
- Pricing tiers comparison
- Hidden costs section
- Who needs what recommendations
- Bottom line verdict
- Internal links section
- FAQ section with FAQPage schema
- BreadcrumbList schema
- Full SEO meta tags
"""

import json
import os
import sys

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from templates import get_html_head, get_nav_html, get_footer_html, BASE_URL


def load_pricing():
    """Load pricing data from JSON file."""
    data_path = os.path.join(os.path.dirname(script_dir), 'data', 'pricing.json')
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
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }, indent=4)


def generate_breadcrumb_schema(slug, name):
    """Generate BreadcrumbList JSON-LD schema."""
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Tools", "item": f"{BASE_URL}/tools/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": f"{BASE_URL}/tools/{slug}/"}
        ]
    }, indent=4)


def generate_page(entry):
    """Generate a complete pricing page."""
    slug = entry['slug']

    head = get_html_head(
        title=entry['title'],
        description=entry['meta_description'],
        page_path=f'tools/{slug}/',
        extra_head=f'''
    <!-- BreadcrumbList Schema -->
    <script type="application/ld+json">
    {generate_breadcrumb_schema(slug, entry['title'])}
    </script>

    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {generate_faq_schema(entry['faqs'])}
    </script>
    '''
    )

    nav = get_nav_html(active_page='tools')
    footer = get_footer_html()

    # Build pricing tiers HTML
    tiers_html = ''
    for tier in entry['tiers']:
        popular_badge = '<span style="position: absolute; top: -12px; right: 16px; background: var(--gold); color: #000; font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 12px; text-transform: uppercase; letter-spacing: 0.05em;">Most Popular</span>' if tier.get('popular') else ''
        popular_border = 'border-color: var(--gold) !important;' if tier.get('popular') else ''

        highlights_html = ''
        for h in tier['highlights']:
            highlights_html += f'\n              <li style="padding: 6px 0; color: var(--text-secondary); font-size: 0.9375rem; display: flex; align-items: flex-start; gap: 8px;"><span style="color: var(--gold); flex-shrink: 0;">&#10003;</span> {h}</li>'

        tiers_html += f'''
        <div style="position: relative; background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 28px 24px; {popular_border}">
          {popular_badge}
          <h3 style="font-size: 1.125rem; margin-bottom: 4px;">{tier['name']}</h3>
          <div style="margin-bottom: 16px;">
            <span style="font-size: 2rem; font-weight: 700; color: var(--gold);">{tier['price']}</span>
            <span style="color: var(--text-muted); font-size: 0.875rem;"> {tier['billing']}</span>
          </div>
          <ul style="list-style: none; padding: 0; margin: 0;">{highlights_html}
          </ul>
        </div>'''

    # Build hidden costs HTML
    hidden_costs_html = ''
    if entry.get('hidden_costs'):
        cost_items = ''
        for cost in entry['hidden_costs']:
            cost_items += f'\n          <li style="padding: 8px 0; color: var(--text-secondary); line-height: 1.7; display: flex; align-items: flex-start; gap: 8px;"><span style="color: var(--warning); flex-shrink: 0;">&#9888;</span> {cost}</li>'
        hidden_costs_html = f'''
      <div style="margin-top: 48px;">
        <h2 style="font-size: 1.5rem; margin-bottom: 16px;">Hidden Costs &amp; Gotchas</h2>
        <div style="background: var(--bg-darker); border-radius: 12px; padding: 20px 24px;">
          <ul style="list-style: none; padding: 0; margin: 0;">{cost_items}
          </ul>
        </div>
      </div>'''

    # Build who needs what HTML
    recommendations_html = ''
    if entry.get('who_needs_what'):
        rec_items = ''
        for rec in entry['who_needs_what']:
            rec_items += f'''
          <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 20px 24px; margin-bottom: 12px;">
            <h3 style="font-size: 1rem; color: var(--gold); margin-bottom: 8px;">{rec['persona']}</h3>
            <p style="color: var(--text-secondary); line-height: 1.7; margin: 0;">{rec['recommendation']}</p>
          </div>'''
        recommendations_html = f'''
      <div style="margin-top: 48px;">
        <h2 style="font-size: 1.5rem; margin-bottom: 16px;">Which Plan Do You Need?</h2>
        {rec_items}
      </div>'''

    # Build internal links HTML
    internal_links_html = ''
    if entry.get('internal_links'):
        link_items = ''
        for link in entry['internal_links']:
            link_items += f'\n          <a href="{link["url"]}" style="display: block; padding: 12px 16px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; color: var(--text-secondary); text-decoration: none; transition: all 0.2s;">{link["text"]} &rarr;</a>'
        internal_links_html = f'''
      <div style="margin-top: 48px;">
        <h2 style="font-size: 1.25rem; color: var(--gold); margin-bottom: 16px;">Related Resources</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px;">{link_items}
        </div>
      </div>'''

    # Build FAQ HTML
    faq_html = ''
    for faq in entry['faqs']:
        faq_html += f'''
        <details style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 12px 20px; margin-bottom: 8px;">
          <summary style="cursor: pointer; font-weight: 600; font-size: 1.0625rem; color: var(--text-primary); list-style: none;">{faq['question']}</summary>
          <p style="margin-top: 8px; color: var(--text-secondary); line-height: 1.7;">{faq['answer']}</p>
        </details>'''

    # Custom page styles
    page_css = '''
    <style>
    .pricing-page { max-width: 900px; margin: 0 auto; padding: 48px 24px; }
    .pricing-page h1 { font-size: 2rem; margin-bottom: 8px; }
    .pricing-page .subtitle { color: var(--text-secondary); font-size: 1.125rem; margin-bottom: 32px; line-height: 1.7; }
    .pricing-tiers { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; margin-top: 32px; }
    .pricing-page .bottom-line { background: linear-gradient(135deg, rgba(6, 214, 160, 0.1), rgba(245, 158, 11, 0.05)); border: 1px solid rgba(6, 214, 160, 0.2); border-radius: 12px; padding: 24px; margin: 32px 0; }
    .pricing-page .bottom-line h3 { color: var(--gold); margin-bottom: 12px; }
    .pricing-page .bottom-line p { color: var(--text-secondary); line-height: 1.7; margin: 0; }
    .faq-section { max-width: 900px; margin: 0 auto; }
    .faq-section h2 { font-size: 1.25rem; color: var(--gold); margin-bottom: 16px; }
    .newsletter-cta { max-width: 600px; margin: 48px auto 0; text-align: center; padding: 32px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; }
    .newsletter-cta h2 { font-size: 1.25rem; margin-bottom: 8px; }
    .newsletter-cta p { color: var(--text-secondary); margin-bottom: 16px; }
    .newsletter-cta form { display: flex; gap: 8px; justify-content: center; }
    .newsletter-cta input { padding: 10px 16px; border-radius: 8px; border: 1px solid var(--border); background: var(--bg-darker); color: var(--text-primary); font-size: 0.9375rem; width: 250px; }
    .newsletter-cta button { padding: 10px 20px; border-radius: 8px; border: none; background: var(--gold); color: #000; font-weight: 600; cursor: pointer; white-space: nowrap; }
    .newsletter-cta button:hover { background: var(--gold-hover); }
    @media (max-width: 600px) {
      .pricing-tiers { grid-template-columns: 1fr; }
      .newsletter-cta form { flex-direction: column; align-items: center; }
      .newsletter-cta input { width: 100%; }
    }
    </style>'''

    html = f'''{head}
{page_css}
</head>
<body>
{nav}

  <main>
    <div class="pricing-page">
      <h1>{entry['h1']}</h1>
      <p class="subtitle">{entry['intro']}</p>

      <div class="pricing-tiers">
        {tiers_html}
      </div>

      {hidden_costs_html}

      {recommendations_html}

      <div class="bottom-line">
        <h3>The Bottom Line</h3>
        <p>{entry['bottom_line']}</p>
      </div>

      <div class="affiliate-disclosure" style="font-size: 0.8125rem; color: var(--text-muted); padding: 12px 16px; background: var(--bg-darker); border-radius: 8px; margin-top: 24px;">
        <strong>Disclosure:</strong> Pricing information is sourced from official websites and may change. We update this page regularly but always verify current pricing on the vendor's site before purchasing.
      </div>

      {internal_links_html}

      <!-- FAQ Section -->
      <div class="faq-section" style="margin-top: 48px;">
        <h2>Frequently Asked Questions</h2>
        {faq_html}
      </div>

      <!-- Newsletter CTA -->
      <div class="newsletter-cta">
        <h2>Get Pricing Updates in Your Inbox</h2>
        <p>We track AI tool pricing changes so you don't have to.</p>
        <form action="https://ainewsdigest.substack.com/subscribe" method="get" target="_blank">
          <input type="email" name="email" placeholder="your@email.com" required>
          <button type="submit">Subscribe Free</button>
        </form>
      </div>
    </div>
  </main>

{footer}'''

    return html


def main():
    pricing = load_pricing()
    output_base = os.path.join(os.path.dirname(script_dir), 'site', 'tools')

    generated = 0
    for entry in pricing:
        slug = entry['slug']
        output_dir = os.path.join(output_base, slug)
        os.makedirs(output_dir, exist_ok=True)

        html = generate_page(entry)
        output_path = os.path.join(output_dir, 'index.html')

        with open(output_path, 'w') as f:
            f.write(html)

        print(f"  Generated: /tools/{slug}/")
        generated += 1

    print(f"\nTotal pricing pages generated: {generated}")


if __name__ == '__main__':
    main()
