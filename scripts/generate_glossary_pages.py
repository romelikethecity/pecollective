#!/usr/bin/env python3
"""
Generate glossary pages for programmatic SEO.
Creates pages like /glossary/rag/, /glossary/chain-of-thought/, etc.
Also creates the /glossary/ hub page listing all terms.
"""

import json
import os
import sys

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from templates import get_html_head, get_nav_html, get_footer_html, get_cta_box, get_breadcrumb_schema, BASE_URL, SITE_NAME, CSS_VARIABLES

DATA_FILE = 'data/glossary.json'
SITE_DIR = 'site'
GLOSSARY_DIR = f'{SITE_DIR}/glossary'


def load_glossary():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def get_glossary_page_css():
    return f'''
    <style>
    {CSS_VARIABLES}

    .glossary-page {{
        padding: 3rem 0;
        min-height: 60vh;
    }}

    .glossary-container {{
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1.5rem;
    }}

    .glossary-term-header {{
        margin-bottom: 2rem;
    }}

    .glossary-term-header h1 {{
        font-size: 2.25rem;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }}

    .glossary-term-header .full-name {{
        color: var(--text-secondary);
        font-size: 1.125rem;
        margin-bottom: 1rem;
    }}

    .glossary-category-badge {{
        display: inline-block;
        padding: 4px 12px;
        background: var(--teal-primary);
        color: var(--gold);
        border-radius: 4px;
        font-size: 0.8125rem;
        font-weight: 600;
    }}

    .glossary-quick-answer {{
        font-size: 1rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
        padding: 0.75rem 1rem;
        background: var(--bg-darker);
        border-radius: 8px;
        line-height: 1.6;
    }}

    .glossary-quick-answer strong {{
        color: var(--gold);
    }}

    .glossary-definition {{
        font-size: 1.125rem;
        line-height: 1.8;
        color: var(--text-primary);
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: var(--bg-card);
        border-left: 3px solid var(--gold);
        border-radius: 0 8px 8px 0;
    }}

    .glossary-definition strong {{
        color: var(--text-primary);
    }}

    .glossary-section {{
        margin-bottom: 2rem;
    }}

    .glossary-section h2 {{
        font-size: 1.25rem;
        color: var(--gold);
        margin-bottom: 0.75rem;
    }}

    .glossary-section p,
    .glossary-section .example-block {{
        color: var(--text-secondary);
        line-height: 1.7;
    }}

    .example-block {{
        background: var(--bg-darker);
        padding: 1.25rem;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9375rem;
        white-space: pre-wrap;
        border: 1px solid var(--teal-primary);
    }}

    .related-terms {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }}

    .related-terms a {{
        display: inline-block;
        padding: 6px 14px;
        background: var(--bg-card);
        color: var(--text-secondary);
        border-radius: 6px;
        font-size: 0.875rem;
        border: 1px solid var(--teal-primary);
        transition: all 0.2s;
    }}

    .related-terms a:hover {{
        background: var(--teal-primary);
        color: var(--text-primary);
    }}

    .related-links {{
        list-style: none;
        padding: 0;
        margin-top: 0.5rem;
    }}

    .related-links li {{
        margin-bottom: 0.5rem;
    }}

    .related-links a {{
        color: var(--gold);
        font-weight: 500;
    }}

    .related-links a:hover {{
        color: var(--gold-light);
    }}

    /* Hub page styles */
    .glossary-hub {{
        padding: 3rem 0;
    }}

    .glossary-hub h1 {{
        font-size: 2.25rem;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }}

    .glossary-hub .hub-subtitle {{
        color: var(--text-secondary);
        font-size: 1.125rem;
        margin-bottom: 2.5rem;
        max-width: 640px;
    }}

    .glossary-category {{
        margin-bottom: 2.5rem;
    }}

    .glossary-category h2 {{
        font-size: 1.25rem;
        color: var(--gold);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--teal-primary);
    }}

    .glossary-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1rem;
    }}

    .glossary-card {{
        display: block;
        padding: 1.25rem;
        background: var(--bg-card);
        border: 1px solid var(--teal-primary);
        border-radius: 8px;
        transition: all 0.2s;
    }}

    .glossary-card:hover {{
        background: var(--bg-card-hover);
        border-color: var(--gold);
        transform: translateY(-2px);
    }}

    .glossary-card h3 {{
        color: var(--text-primary);
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }}

    .glossary-card p {{
        color: var(--text-muted);
        font-size: 0.875rem;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }}

    @media (max-width: 768px) {{
        .glossary-term-header h1,
        .glossary-hub h1 {{
            font-size: 1.75rem;
        }}

        .glossary-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    </style>'''


def generate_term_page(term_data, all_terms):
    """Generate an individual glossary term page."""
    term = term_data['term']
    slug = term_data['slug']
    definition = term_data['definition']
    category = term_data['category']
    full_name = term_data.get('full_name', '')

    page_path = f'glossary/{slug}/'
    title = f"What is {term}? Definition & Examples"
    description = definition[:155].rsplit(' ', 1)[0] + '...' if len(definition) > 155 else definition

    breadcrumbs = [
        ('Home', f'{BASE_URL}/'),
        ('Glossary', f'{BASE_URL}/glossary/'),
        (term, f'{BASE_URL}/{page_path}')
    ]

    # Build schema
    defined_term_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": term,
        "description": definition,
        "inDefinedTermSet": {
            "@type": "DefinedTermSet",
            "name": "AI & Prompt Engineering Glossary",
            "url": f"{BASE_URL}/glossary/"
        }
    }, indent=2)

    faq_qa = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"What is {term}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": definition
                }
            }
        ]
    }
    if term_data.get('why_it_matters'):
        faq_qa['mainEntity'].append({
            "@type": "Question",
            "name": f"Why does {term} matter?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": term_data['why_it_matters']
            }
        })
    # Add extra FAQs from data if present
    for extra_faq in term_data.get('faqs', []):
        faq_qa['mainEntity'].append({
            "@type": "Question",
            "name": extra_faq['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": extra_faq['answer']
            }
        })
    faq_schema = json.dumps(faq_qa, indent=2)

    extra_head = f'''
    {get_glossary_page_css()}
    {get_breadcrumb_schema(breadcrumbs)}
    <script type="application/ld+json">
    {defined_term_schema}
    </script>
    <script type="application/ld+json">
    {faq_schema}
    </script>'''

    # Build related terms HTML
    related_html = ''
    if term_data.get('related_terms'):
        term_lookup = {t['slug']: t['term'] for t in all_terms}
        links = []
        for rt_slug in term_data['related_terms']:
            rt_name = term_lookup.get(rt_slug, rt_slug.replace('-', ' ').title())
            links.append(f'<a href="/glossary/{rt_slug}/">{rt_name}</a>')
        related_html = f'''
    <div class="glossary-section">
        <h2>Related Terms</h2>
        <div class="related-terms">
            {''.join(links)}
        </div>
    </div>'''

    # Build related links HTML
    links_html = ''
    if term_data.get('related_links'):
        items = []
        for link in term_data['related_links']:
            label = link.strip('/').split('/')[-1].replace('-', ' ').title() if '/' in link else link
            if '/blog/' in link:
                label = f"Read: {label}"
            elif '/tools/' in link:
                label = "Browse AI Tools"
            elif '/jobs/' in link:
                label = f"View {label} Jobs"
            items.append(f'<li><a href="{link}">{label}</a></li>')
        links_html = f'''
    <div class="glossary-section">
        <h2>Learn More</h2>
        <ul class="related-links">
            {"".join(items)}
        </ul>
    </div>'''

    full_name_html = f'<p class="full-name">{full_name}</p>' if full_name else ''

    # AEO: Build bold-term definition ("Term is definition...")
    def_lower = definition[0].lower() + definition[1:]
    display_name = full_name if full_name else term
    aeo_definition = f'<strong>{display_name}</strong> is {def_lower}'

    # Quick answer: first sentence, under 30 words ideal
    quick_answer = term_data.get('quick_answer', '')
    if not quick_answer:
        # Auto-generate from first sentence of definition
        first_sentence = definition.split('. ')[0]
        if not first_sentence.endswith('.'):
            first_sentence += '.'
        quick_answer = first_sentence

    example_html = ''
    if term_data.get('example'):
        example_html = f'''
    <div class="glossary-section">
        <h2>Example</h2>
        <div class="example-block">{term_data["example"]}</div>
    </div>'''

    why_html = ''
    if term_data.get('why_it_matters'):
        why_html = f'''
    <div class="glossary-section">
        <h2>Why It Matters</h2>
        <p>{term_data["why_it_matters"]}</p>
    </div>'''

    # Extra FAQ details (visible on page, beyond schema)
    extra_faq_html = ''
    if term_data.get('faqs'):
        faq_items = ''
        for faq in term_data['faqs']:
            faq_items += f'''
        <details style="background: var(--bg-card); border: 1px solid var(--teal-primary); border-radius: 8px; padding: 12px 16px; margin-bottom: 8px;">
            <summary style="cursor: pointer; font-weight: 600; color: var(--text-primary); list-style: none;">{faq["question"]}</summary>
            <p style="margin-top: 8px; color: var(--text-secondary); line-height: 1.7;">{faq["answer"]}</p>
        </details>'''
        extra_faq_html = f'''
    <div class="glossary-section">
        <h2>Frequently Asked Questions</h2>
        {faq_items}
    </div>'''

    html = f'''{get_html_head(title, description, page_path, extra_head=extra_head)}
{get_nav_html()}
    <main>
        <div class="glossary-page">
            <div class="glossary-container">
                <div class="glossary-term-header">
                    <span class="glossary-category-badge">{category}</span>
                    <h1>{term}</h1>
                    {full_name_html}
                </div>

                <div class="glossary-quick-answer">
                    <strong>Quick Answer:</strong> {quick_answer}
                </div>

                <div class="glossary-definition">
                    {aeo_definition}
                </div>

                {example_html}
                {why_html}
                {extra_faq_html}
                {related_html}
                {links_html}
            </div>
        </div>

        {get_cta_box(
            title="Stay Ahead in AI",
            description="Join 1,300+ prompt engineers getting weekly insights on tools, techniques, and career opportunities.",
            button_text="Join the Community",
            button_url="/join/"
        )}
    </main>
{get_footer_html()}'''

    # Write page
    page_dir = os.path.join(GLOSSARY_DIR, slug)
    os.makedirs(page_dir, exist_ok=True)
    with open(os.path.join(page_dir, 'index.html'), 'w') as f:
        f.write(html)

    return True


def generate_hub_page(terms):
    """Generate the glossary hub/index page."""
    page_path = 'glossary/'
    title = 'AI & Prompt Engineering Glossary'
    description = 'Definitions and examples for key AI, prompt engineering, and machine learning terms. From RAG to RLHF, learn the concepts that matter.'

    breadcrumbs = [
        ('Home', f'{BASE_URL}/'),
        ('Glossary', f'{BASE_URL}/glossary/')
    ]

    # ItemList schema
    items_schema = []
    for i, term in enumerate(terms, 1):
        items_schema.append({
            "@type": "ListItem",
            "position": i,
            "url": f"{BASE_URL}/glossary/{term['slug']}/",
            "name": term['term']
        })

    item_list_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "AI & Prompt Engineering Glossary",
        "description": description,
        "numberOfItems": len(terms),
        "itemListElement": items_schema
    }, indent=2)

    extra_head = f'''
    {get_glossary_page_css()}
    {get_breadcrumb_schema(breadcrumbs)}
    <script type="application/ld+json">
    {item_list_schema}
    </script>'''

    # Group terms by category
    categories = {}
    for term in terms:
        cat = term['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(term)

    # Preferred category order
    cat_order = [
        'Core Concepts', 'Prompting Techniques', 'Architecture Patterns',
        'Model Parameters', 'Model Training', 'Infrastructure'
    ]
    sorted_cats = sorted(categories.keys(), key=lambda c: cat_order.index(c) if c in cat_order else 99)

    categories_html = ''
    for cat in sorted_cats:
        cat_terms = sorted(categories[cat], key=lambda t: t['term'])
        cards = ''
        for term in cat_terms:
            short_def = term['definition'][:120].rsplit(' ', 1)[0] + '...' if len(term['definition']) > 120 else term['definition']
            cards += f'''
            <a href="/glossary/{term["slug"]}/" class="glossary-card">
                <h3>{term["term"]}</h3>
                <p>{short_def}</p>
            </a>'''

        categories_html += f'''
        <div class="glossary-category">
            <h2>{cat}</h2>
            <div class="glossary-grid">
                {cards}
            </div>
        </div>'''

    html = f'''{get_html_head(title, description, page_path, extra_head=extra_head)}
{get_nav_html()}
    <main>
        <div class="glossary-hub">
            <div class="glossary-container">
                <h1>AI & Prompt Engineering Glossary</h1>
                <p class="hub-subtitle">
                    {len(terms)} essential terms defined with examples. From foundational concepts to advanced techniques,
                    learn the language of AI engineering.
                </p>

                {categories_html}
            </div>
        </div>

        {get_cta_box(
            title="Go Deeper",
            description="Our complete prompt engineering guide covers these concepts in practice, with real-world examples and techniques you can use today.",
            button_text="Read the Guide",
            button_url="/blog/prompt-engineering-guide/"
        )}
    </main>
{get_footer_html()}'''

    os.makedirs(GLOSSARY_DIR, exist_ok=True)
    with open(os.path.join(GLOSSARY_DIR, 'index.html'), 'w') as f:
        f.write(html)

    return True


def main():
    print("Loading glossary data...")
    terms = load_glossary()
    print(f"Found {len(terms)} terms")

    # Generate individual term pages
    success_count = 0
    for term in terms:
        if generate_term_page(term, terms):
            success_count += 1
            print(f"  Generated: /glossary/{term['slug']}/")

    # Generate hub page
    if generate_hub_page(terms):
        print(f"  Generated: /glossary/ (hub page)")

    print(f"\nDone! Generated {success_count} term pages + 1 hub page")


if __name__ == '__main__':
    main()
