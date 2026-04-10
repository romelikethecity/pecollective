#!/usr/bin/env python3
"""
Generate XML sitemap and update robots.txt for SEO.
"""

import os
from datetime import datetime

SITE_DIR = 'site'
BASE_URL = 'https://pecollective.com'

print("="*70)
print("  PE COLLECTIVE - GENERATING SITEMAP")
print("="*70)

today = datetime.now().strftime('%Y-%m-%d')

# Collect all pages
pages = []

def add_page(path, priority, changefreq='weekly'):
    pages.append({
        'loc': f'{BASE_URL}/{path}' if path else f'{BASE_URL}/',
        'priority': priority,
        'changefreq': changefreq,
        'lastmod': today,
    })

# Core pages
add_page('', 1.0, 'weekly')
add_page('jobs/', 0.9, 'weekly')
add_page('salaries/', 0.8, 'weekly')
add_page('insights/', 0.8, 'weekly')
add_page('tools/', 0.7, 'monthly')
add_page('about/', 0.5, 'monthly')
add_page('join/', 0.6, 'monthly')

# Paths to exclude from sitemap (redirect stubs, old WordPress URLs)
EXCLUDE_PREFIXES = ('2023/', '2024/', 'member-competitions/')

# Walk site directory for generated pages
for root, dirs, files in os.walk(SITE_DIR):
    for fname in files:
        if fname == 'index.html':
            rel_path = os.path.relpath(root, SITE_DIR)
            if rel_path == '.':
                continue  # Skip root (already added)

            url_path = rel_path.replace(os.sep, '/') + '/'

            # Skip redirect stubs and old WordPress paths
            if url_path.startswith(EXCLUDE_PREFIXES):
                continue

            # Skip if already added
            if any(p['loc'].endswith(url_path) for p in pages):
                continue

            # Determine priority and changefreq
            if '/tools/' in url_path and '-vs-' in url_path:
                priority = 0.7  # Comparison pages
                changefreq = 'monthly'
            elif '/glossary/' in url_path and len(url_path.split('/')) > 3:
                priority = 0.6  # Individual glossary terms
                changefreq = 'monthly'
            elif url_path == 'glossary/':
                priority = 0.7  # Glossary hub
                changefreq = 'weekly'
            elif '/blog/' in url_path and len(url_path.split('/')) > 3:
                changefreq = 'monthly'  # Blog posts don't change often
                priority = 0.6
            elif '/jobs/' in url_path and len(url_path.split('/')) > 3:
                priority = 0.6  # Individual job pages
            elif '/salaries/' in url_path and len(url_path.split('/')) > 3:
                priority = 0.7  # Salary category pages
            elif '/jobs/' in url_path:
                priority = 0.8  # Job category pages
            else:
                priority = 0.5

            add_page(url_path, priority)

# Generate XML
xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

for page in pages:
    xml += f'''  <url>
    <loc>{page['loc']}</loc>
    <lastmod>{page['lastmod']}</lastmod>
    <changefreq>{page['changefreq']}</changefreq>
    <priority>{page['priority']}</priority>
  </url>
'''

xml += '</urlset>\n'

# Save sitemap
with open(f'{SITE_DIR}/sitemap.xml', 'w') as f:
    f.write(xml)

print(f"\n Generated sitemap with {len(pages)} URLs")

# Update robots.txt with explicit AI bot allowlists
robots = f'''# PE Collective - robots.txt
User-agent: *
Allow: /
Disallow: /wp-admin/
Disallow: /wp-content/
Disallow: /wp-includes/
Disallow: /comments/

# AI/LLM crawlers - explicitly allowed for AI search citations
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: GoogleOther
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

# Sitemap location
Sitemap: {BASE_URL}/sitemap.xml
'''

with open(f'{SITE_DIR}/robots.txt', 'w') as f:
    f.write(robots)

print(f" Updated robots.txt")
print("="*70)
