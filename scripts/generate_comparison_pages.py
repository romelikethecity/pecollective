#!/usr/bin/env python3
"""
Generate comparison pages from data/comparisons.json.

Each comparison produces a page at site/tools/{slug}/index.html with:
- Feature comparison table
- Quick verdict section
- Deep dive analysis
- Use case recommendations
- Pricing breakdown
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


def load_comparisons():
    """Load comparison data from JSON file."""
    data_path = os.path.join(os.path.dirname(script_dir), 'data', 'comparisons.json')
    with open(data_path, 'r') as f:
        return json.load(f)


def generate_feature_rows(features, tool_a_name, tool_b_name):
    """Generate HTML table rows for feature comparison."""
    rows = []
    for feat in features:
        a_class = ' class="winner"' if feat.get('winner') == 'a' else ''
        b_class = ' class="winner"' if feat.get('winner') == 'b' else ''

        a_val = feat['a']
        b_val = feat['b']

        # Add check/cross marks if specified
        if feat.get('a_check'):
            a_val = f'✓ {a_val}'
        if feat.get('b_check'):
            b_val = f'✓ {b_val}'

        rows.append(f'''              <tr>
                <td><strong>{feat['feature']}</strong></td>
                <td{a_class}>{a_val}</td>
                <td{b_class}>{b_val}</td>
              </tr>''')
    return '\n'.join(rows)


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


def generate_software_schema(tool, base_url):
    """Generate SoftwareApplication JSON-LD schema for a tool."""
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": tool['name'],
        "url": tool['url'],
        "applicationCategory": "DeveloperApplication",
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "USD",
            "lowPrice": "0",
            "offerCount": "4",
            "offers": [
                {"@type": "Offer", "name": "Free", "description": tool['price_free']},
                {"@type": "Offer", "name": "Individual", "description": tool['price_individual']},
                {"@type": "Offer", "name": "Business", "description": tool['price_business']},
                {"@type": "Offer", "name": "Enterprise", "description": tool['price_enterprise']}
            ]
        }
    }
    return json.dumps(schema, indent=2)


def generate_comparison_page(comp):
    """Generate a full comparison page HTML."""
    slug = comp['slug']
    tool_a = comp['tool_a']
    tool_b = comp['tool_b']

    # Schema markup
    breadcrumb_name = f"{tool_a['name']} vs {tool_b['name']}"
    breadcrumb_schema = generate_breadcrumb_schema(slug, breadcrumb_name)
    faq_schema = generate_faq_schema(comp['faqs'])
    software_schema_a = generate_software_schema(tool_a, BASE_URL)
    software_schema_b = generate_software_schema(tool_b, BASE_URL)

    extra_head = f'''
    <!-- BreadcrumbList Schema -->
    <script type="application/ld+json">
    {breadcrumb_schema}
    </script>

    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {faq_schema}
    </script>

    <!-- SoftwareApplication Schema: {tool_a['name']} -->
    <script type="application/ld+json">
    {software_schema_a}
    </script>

    <!-- SoftwareApplication Schema: {tool_b['name']} -->
    <script type="application/ld+json">
    {software_schema_b}
    </script>
    '''

    # Feature table rows
    feature_rows = generate_feature_rows(comp['features'], tool_a['name'], tool_b['name'])

    # Deep dive sections
    deep_dive_html = ''
    for section in comp.get('deep_dive', []):
        paragraphs = '\n            '.join(f'<p>{p}</p>' for p in section['paragraphs'])
        deep_dive_html += f'''
          <div class="section-divider">
            <h3>{section['icon']} {section['heading']}</h3>
            {paragraphs}
          </div>'''

    # Use case cards
    use_cases_a = '\n                  '.join(f'<li>→ {uc}</li>' for uc in comp.get('use_cases_a', []))
    use_cases_b = '\n                  '.join(f'<li>→ {uc}</li>' for uc in comp.get('use_cases_b', []))

    # Recommendation sections
    rec_html = ''
    for rec in comp.get('recommendation_sections', []):
        rec_html += f'''
            <p><strong>{rec['audience']}:</strong> {rec['text']}</p>'''

    # Migration guidance section
    migration_html = ''
    if comp.get('migration'):
        mig = comp['migration']
        transfers_items = '\n                  '.join(f'<li>{item}</li>' for item in mig.get('what_transfers', []))
        reconfig_items = '\n                  '.join(f'<li>{item}</li>' for item in mig.get('what_needs_reconfiguration', []))
        time_est = mig.get('time_estimate', '')
        migration_html = f'''
          <div class="section-divider">
            <h2>Switching Between {tool_a['name']} and {tool_b['name']}</h2>
            <div class="migration-section">
              <h3>What Transfers Directly</h3>
              <ul>
                  {transfers_items}
              </ul>
              <h3>What Needs Reconfiguration</h3>
              <ul>
                  {reconfig_items}
              </ul>
              <h3>Estimated Migration Time</h3>
              <p>{time_est}</p>
            </div>
          </div>'''

    # FAQ details
    faq_details = ''
    for faq in comp['faqs']:
        faq_details += f'''
        <details style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 12px 20px; margin-bottom: 8px;">
          <summary style="cursor: pointer; font-weight: 600; font-size: 1.0625rem; color: var(--text-primary); list-style: none;">{faq['question']}</summary>
          <p style="margin-top: 8px; color: var(--text-secondary); line-height: 1.7;">{faq['answer']}</p>
        </details>'''

    # Related resources links
    related_links_html = ''
    if comp.get('internal_links'):
        link_items = ''
        for link in comp['internal_links']:
            link_items += f'\n            <a href="{link["url"]}" style="display: block; padding: 12px 16px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; color: var(--text-secondary); text-decoration: none; transition: all 0.2s;">{link["text"]} &rarr;</a>'
        related_links_html = f'''<div style="max-width: 800px; margin: 48px auto 0;">
        <h2 style="font-size: 1.25rem; color: var(--gold); margin-bottom: 16px;">Related Resources</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px;">{link_items}
        </div>
      </div>'''

    # Pricing table rows
    pricing_rows = f'''              <tr>
                <td><strong>Free / Trial</strong></td>
                <td>{tool_a['price_free']}</td>
                <td>{tool_b['price_free']}</td>
              </tr>
              <tr>
                <td><strong>Individual</strong></td>
                <td>{tool_a['price_individual']}</td>
                <td>{tool_b['price_individual']}</td>
              </tr>
              <tr>
                <td><strong>Business</strong></td>
                <td>{tool_a['price_business']}</td>
                <td>{tool_b['price_business']}</td>
              </tr>
              <tr>
                <td><strong>Enterprise</strong></td>
                <td>{tool_a['price_enterprise']}</td>
                <td>{tool_b['price_enterprise']}</td>
              </tr>'''

    # Build head
    page_path = f"tools/{slug}/"
    head = get_html_head(
        title=comp['title'],
        description=comp['meta_description'],
        page_path=page_path,
        extra_head=extra_head
    )

    # Build nav
    nav = get_nav_html(active_page='tools')

    # Build footer
    footer = get_footer_html()

    # Comparison-specific CSS
    comp_css = '''
    <style>
    .comparison-header {
      padding: 60px 0 40px;
      text-align: center;
      max-width: 800px;
      margin: 0 auto;
    }
    .comparison-header__tools {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 32px;
      flex-wrap: wrap;
    }
    .comparison-header__tool {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .comparison-header__icon {
      width: 60px;
      height: 60px;
      background: var(--bg-card);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2rem;
    }
    .comparison-header__name {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.5rem;
      font-weight: 600;
    }
    .comparison-header__vs {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 3rem;
      font-weight: 700;
      color: var(--gold);
    }
    .comparison-header h1 {
      margin-top: 24px;
      font-size: 2rem;
    }
    .comparison-header .subtitle {
      color: var(--text-secondary);
      margin-top: 8px;
    }
    .quick-verdict {
      background: linear-gradient(135deg, var(--teal-primary) 0%, var(--bg-card) 100%);
      border: 1px solid var(--teal-light);
      border-radius: 16px;
      padding: 32px;
      margin: 32px auto;
      max-width: 800px;
    }
    .quick-verdict h2 {
      color: var(--gold);
      margin-bottom: 12px;
      font-size: 1.25rem;
    }
    .quick-verdict p {
      line-height: 1.7;
      margin-bottom: 8px;
    }
    .comparison-content {
      max-width: 800px;
      margin: 0 auto;
    }
    .comparison-content h2 {
      font-size: 1.5rem;
      margin-bottom: 16px;
    }
    .comparison-content h3 {
      font-size: 1.125rem;
      margin: 24px 0 8px;
      color: var(--gold);
    }
    .comparison-content p {
      margin-bottom: 12px;
      line-height: 1.7;
      color: var(--text-secondary);
    }
    .comparison-table {
      width: 100%;
      border-collapse: collapse;
      margin: 24px 0;
    }
    .comparison-table th,
    .comparison-table td {
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    .comparison-table th {
      background: var(--bg-card);
      font-weight: 600;
      color: var(--text-primary);
    }
    .comparison-table th:first-child { width: 35%; }
    .comparison-table td { color: var(--text-secondary); }
    .comparison-table tr:hover td { background: var(--bg-card); }
    .comparison-table .winner {
      color: var(--success);
      font-weight: 600;
    }
    .section-divider {
      margin: 48px 0;
      padding-top: 32px;
      border-top: 1px solid var(--border);
    }
    .use-case-cards {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin: 24px 0;
    }
    .use-case-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
    }
    .use-case-card h4 {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
    }
    .use-case-card ul { list-style: none; padding: 0; }
    .use-case-card li {
      padding: 4px 0;
      color: var(--text-secondary);
    }
    .cta-comparison {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 32px;
    }
    .cta-comparison__card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      text-align: center;
    }
    .cta-comparison__card h4 { margin-bottom: 8px; }
    .cta-comparison__card p {
      margin-bottom: 12px;
      font-size: 0.9375rem;
    }
    .cta-comparison__card .btn {
      display: inline-block;
      padding: 10px 20px;
      border-radius: 8px;
      font-weight: 600;
      background: var(--gold);
      color: var(--bg-darker);
      text-decoration: none;
    }
    .cta-comparison__card .btn:hover {
      background: var(--gold-hover);
    }
    .comparison-header__date {
      color: var(--text-muted);
      font-size: 0.875rem;
      margin-top: 8px;
    }
    .migration-section {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      margin-top: 24px;
    }
    .migration-section h3 {
      font-size: 1.125rem;
      color: var(--gold);
      margin-bottom: 12px;
    }
    .migration-section ul {
      padding-left: 1.25rem;
      margin: 8px 0 16px;
    }
    .migration-section li {
      color: var(--text-secondary);
      line-height: 1.7;
      margin-bottom: 4px;
    }
    .affiliate-disclosure {
      font-size: 0.8125rem;
      color: var(--text-muted);
      padding: 12px;
      background: var(--bg-darker);
      border-radius: 8px;
      margin-top: 32px;
    }
    .faq-section { max-width: 800px; margin: 0 auto; }
    .faq-section h2 {
      font-size: 1.75rem;
      margin-bottom: 16px;
    }
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
    }
    .newsletter-cta button:hover { background: var(--gold-hover); }
    @media (max-width: 700px) {
      .use-case-cards, .cta-comparison { grid-template-columns: 1fr; }
      .comparison-table { font-size: 0.875rem; }
      .comparison-table th, .comparison-table td { padding: 8px; }
      .newsletter-cta form { flex-direction: column; align-items: center; }
      .newsletter-cta input { width: 100%; }
    }
    </style>
    '''

    # Assemble page
    html = f'''{head}
{nav}

    {comp_css}

    <main>
      <article>
        <div class="comparison-header">
          <div class="comparison-header__tools">
            <div class="comparison-header__tool">
              <span class="comparison-header__icon">{tool_a['icon']}</span>
              <span class="comparison-header__name">{tool_a['name']}</span>
            </div>
            <span class="comparison-header__vs">VS</span>
            <div class="comparison-header__tool">
              <span class="comparison-header__icon">{tool_b['icon']}</span>
              <span class="comparison-header__name">{tool_b['name']}</span>
            </div>
          </div>
          <h1>{comp['h1']}</h1>
          <p class="subtitle">{comp['subtitle']}</p>
          <p class="comparison-header__date">Last updated: {comp.get('date_updated', 'February 2026')}</p>
        </div>

        <div class="quick-verdict">
          <h2>Quick Verdict</h2>
          <p><strong>Choose {tool_a['name']} if:</strong> {comp['verdict_a']}</p>
          <p><strong>Choose {tool_b['name']} if:</strong> {comp['verdict_b']}</p>
        </div>

        <div class="comparison-content">
          <h2>Feature Comparison</h2>
          <table class="comparison-table">
            <thead>
              <tr>
                <th>Feature</th>
                <th>{tool_a['name']}</th>
                <th>{tool_b['name']}</th>
              </tr>
            </thead>
            <tbody>
{feature_rows}
            </tbody>
          </table>

          <div class="section-divider">
            <h2>Deep Dive: Where Each Tool Wins</h2>
            {deep_dive_html}
          </div>

          <div class="section-divider">
            <h2>Use Case Recommendations</h2>
            <div class="use-case-cards">
              <div class="use-case-card">
                <h4>{tool_a['icon']} Use {tool_a['name']} For:</h4>
                <ul>
                  {use_cases_a}
                </ul>
              </div>
              <div class="use-case-card">
                <h4>{tool_b['icon']} Use {tool_b['name']} For:</h4>
                <ul>
                  {use_cases_b}
                </ul>
              </div>
            </div>
          </div>

          <div class="section-divider">
            <h2>Pricing Breakdown</h2>
            <table class="comparison-table">
              <thead>
                <tr>
                  <th>Tier</th>
                  <th>{tool_a['name']}</th>
                  <th>{tool_b['name']}</th>
                </tr>
              </thead>
              <tbody>
{pricing_rows}
              </tbody>
            </table>
          </div>

          <div class="section-divider">
            <h2>Our Recommendation</h2>
            {rec_html}
          </div>

          {migration_html}

          <div class="cta-comparison">
            <div class="cta-comparison__card">
              <h4>{tool_a['icon']} {tool_a['cta_text']}</h4>
              <p>{tool_a['name']} - AI-powered development</p>
              <a href="{tool_a['url']}" target="_blank" rel="noopener" class="btn">{tool_a['cta_text']} →</a>
            </div>
            <div class="cta-comparison__card">
              <h4>{tool_b['icon']} {tool_b['cta_text']}</h4>
              <p>{tool_b['name']} - AI-powered development</p>
              <a href="{tool_b['url']}" target="_blank" rel="noopener" class="btn">{tool_b['cta_text']} →</a>
            </div>
          </div>

          <div class="affiliate-disclosure">
            <strong>Disclosure:</strong> This comparison may contain affiliate links. If you sign up through our links, we may earn a commission at no extra cost to you. Our recommendations are based on real-world experience, not sponsorships.
          </div>
        </div>
      </article>

      <!-- FAQ Section -->
      <div class="faq-section" style="margin-top: 48px;">
        <h2>Frequently Asked Questions</h2>
        {faq_details}
      </div>

      <!-- Related Resources -->
      {related_links_html}

      <!-- Newsletter CTA -->
      <div class="newsletter-cta">
        <h2>Get Tool Comparisons in Your Inbox</h2>
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
    comparisons = load_comparisons()
    output_base = os.path.join(os.path.dirname(script_dir), 'site', 'tools')

    generated = 0
    for comp in comparisons:
        slug = comp['slug']
        output_dir = os.path.join(output_base, slug)
        os.makedirs(output_dir, exist_ok=True)

        html = generate_comparison_page(comp)
        output_path = os.path.join(output_dir, 'index.html')

        with open(output_path, 'w') as f:
            f.write(html)

        print(f"  Generated: /tools/{slug}/")
        generated += 1

    print(f"\nTotal comparison pages generated: {generated}")


if __name__ == '__main__':
    main()
