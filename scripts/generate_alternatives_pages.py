#!/usr/bin/env python3
"""
Generate alternatives pages from data/alternatives.json.

Each alternatives page produces site/tools/{slug}/index.html with:
- Introduction and methodology
- List of alternatives with verdicts
- Bottom line recommendation
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


def load_alternatives():
    """Load alternatives data from JSON file."""
    data_path = os.path.join(os.path.dirname(script_dir), 'data', 'alternatives.json')
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
    """Generate a complete alternatives page."""
    slug = entry['slug']

    head = get_html_head(
        title=entry['title'],
        description=entry['meta_description'],
        page_path=f'/tools/{slug}/',
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

    # Build alternatives list HTML
    alternatives_html = ''
    for i, alt in enumerate(entry['alternatives'], 1):
        is_internal = alt['url'].startswith('/')
        target = '' if is_internal else ' target="_blank" rel="noopener"'

        alternatives_html += f'''
        <div class="alternative-card" style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 16px;">
          <div style="display: flex; align-items: flex-start; gap: 16px; margin-bottom: 16px;">
            <span style="font-size: 2rem; flex-shrink: 0;">{alt['icon']}</span>
            <div style="flex: 1;">
              <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                <h3 style="margin: 0; font-size: 1.25rem;">
                  <a href="{alt['url']}"{target} style="color: var(--text-primary); text-decoration: none;">{alt['name']}</a>
                </h3>
                <span style="font-size: 0.875rem; color: var(--gold); font-weight: 600;">{alt['price']}</span>
              </div>
              <p style="margin: 4px 0 0; font-size: 0.9375rem; color: var(--text-secondary);">{alt['best_for']}</p>
            </div>
          </div>

          <div style="background: var(--bg-darker); border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
            <span style="font-size: 0.8125rem; font-weight: 600; color: var(--gold); text-transform: uppercase; letter-spacing: 0.05em;">Key Difference</span>
            <p style="margin: 4px 0 0; color: var(--text-secondary); font-size: 0.9375rem;">{alt['key_difference']}</p>
          </div>

          <p style="color: var(--text-secondary); line-height: 1.7; margin-bottom: 12px;">{alt['summary']}</p>

          <p style="color: var(--gold); font-weight: 600; font-size: 0.9375rem; margin: 0;">{alt['verdict']}</p>
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
    .alternatives-page { max-width: 800px; margin: 0 auto; padding: 48px 24px; }
    .alternatives-page h1 { font-size: 2rem; margin-bottom: 8px; }
    .alternatives-page .subtitle { color: var(--text-secondary); font-size: 1.125rem; margin-bottom: 32px; line-height: 1.7; }
    .alternatives-page h2 { font-size: 1.5rem; margin-top: 48px; margin-bottom: 16px; }
    .alternatives-page .methodology { background: var(--bg-darker); border-radius: 8px; padding: 16px 20px; margin-bottom: 32px; color: var(--text-secondary); font-size: 0.9375rem; line-height: 1.7; }
    .alternatives-page .bottom-line { background: linear-gradient(135deg, rgba(6, 214, 160, 0.1), rgba(245, 158, 11, 0.05)); border: 1px solid rgba(6, 214, 160, 0.2); border-radius: 12px; padding: 24px; margin: 32px 0; }
    .alternatives-page .bottom-line h3 { color: var(--gold); margin-bottom: 12px; }
    .alternatives-page .bottom-line p { color: var(--text-secondary); line-height: 1.7; margin: 0; }
    .alternative-card:hover { border-color: var(--gold) !important; }
    .faq-section { max-width: 800px; margin: 0 auto; }
    .faq-section h2 { font-size: 1.25rem; color: var(--gold); margin-bottom: 16px; }
    .newsletter-cta { max-width: 600px; margin: 48px auto 0; text-align: center; padding: 32px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; }
    .newsletter-cta h2 { font-size: 1.25rem; margin-bottom: 8px; }
    .newsletter-cta p { color: var(--text-secondary); margin-bottom: 16px; }
    .newsletter-cta form { display: flex; gap: 8px; justify-content: center; }
    .newsletter-cta input { padding: 10px 16px; border-radius: 8px; border: 1px solid var(--border); background: var(--bg-darker); color: var(--text-primary); font-size: 0.9375rem; width: 250px; }
    .newsletter-cta button { padding: 10px 20px; border-radius: 8px; border: none; background: var(--gold); color: #000; font-weight: 600; cursor: pointer; white-space: nowrap; }
    .newsletter-cta button:hover { background: var(--gold-hover); }
    @media (max-width: 600px) {
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
    <div class="alternatives-page">
      <h1>{entry['h1']}</h1>
      <p class="subtitle">{entry['intro']}</p>

      <div class="methodology">
        <strong>How we evaluated:</strong> {entry['methodology']}
      </div>

      <h2>The Alternatives</h2>
      {alternatives_html}

      <div class="bottom-line">
        <h3>The Bottom Line</h3>
        <p>{entry['bottom_line']}</p>
      </div>

      <div class="affiliate-disclosure" style="font-size: 0.8125rem; color: var(--text-muted); padding: 12px 16px; background: var(--bg-darker); border-radius: 8px; margin-top: 24px;">
        <strong>Disclosure:</strong> This page may contain affiliate links. If you sign up through our links, we may earn a commission at no extra cost to you. Our recommendations are based on real-world experience, not sponsorships.
      </div>

      {internal_links_html}

      <!-- FAQ Section -->
      <div class="faq-section" style="margin-top: 48px;">
        <h2>Frequently Asked Questions</h2>
        {faq_html}
      </div>

      <!-- Newsletter CTA -->
      <div class="newsletter-cta">
        <h2>Get Tool Recommendations in Your Inbox</h2>
        <p>Weekly AI tool updates, new releases, and honest comparisons.</p>
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
    alternatives = load_alternatives()
    output_base = os.path.join(os.path.dirname(script_dir), 'site', 'tools')

    generated = 0
    for entry in alternatives:
        slug = entry['slug']
        output_dir = os.path.join(output_base, slug)
        os.makedirs(output_dir, exist_ok=True)

        html = generate_page(entry)
        output_path = os.path.join(output_dir, 'index.html')

        with open(output_path, 'w') as f:
            f.write(html)

        print(f"  Generated: /tools/{slug}/")
        generated += 1

    print(f"\nTotal alternatives pages generated: {generated}")


if __name__ == '__main__':
    main()
