#!/usr/bin/env python3
"""Generate Top 25 Prompt Engineering Voices page for PE Collective.
Standalone generator — reads data/top_voices.json, writes site/voices/index.html.
Matches existing site HTML structure from about/index.html pattern."""

import json, os

BASE_URL = "https://pecollective.com"
SITE_NAME = "PE Collective"

def load_voices():
    with open('data/top_voices.json', 'r') as f:
        return json.load(f)

def voice_card(v):
    tags = ''.join(f'<span class="voice-tag">{t}</span>' for t in v.get("tags", []))
    rc = "voice-rank-top" if v["rank"] <= 3 else "voice-rank"
    return f'''<div class="voice-card" id="voice-{v["rank"]}">
  <div class="voice-card-header">
    <div class="{rc}">#{v["rank"]}</div>
    <div class="voice-card-info">
      <h3 class="voice-name"><a href="{v["linkedin_url"]}" target="_blank" rel="noopener">{v["name"]}</a></h3>
      <p class="voice-title">{v["title"]} at {v["company"]}</p>
      <div class="voice-tags">{tags}</div>
    </div>
    <a href="{v["linkedin_url"]}" target="_blank" rel="noopener" class="voice-linkedin-btn" aria-label="View {v["name"]} on LinkedIn">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
    </a>
  </div>
  <p class="voice-bio">{v["bio"]}</p>
</div>'''

def generate():
    data = load_voices()
    voices = data["voices"]
    leaders = [v for v in voices if v.get("tier") == "leader"]
    rising = [v for v in voices if v.get("tier") == "rising"]
    last_updated = data.get("last_updated", "2026-04-14")

    leaders_html = ''.join(voice_card(v) for v in leaders)
    rising_html = ''.join(voice_card(v) for v in rising)
    jump_links = ''.join(f'<a href="#voice-{v["rank"]}" class="voice-jump-link">#{v["rank"]} {v["name"].split()[0]}</a>' for v in voices)

    list_items = ','.join(f'{{"@type":"ListItem","position":{v["rank"]},"item":{{"@type":"Person","name":"{v["name"]}","jobTitle":"{v["title"]}","url":"{v["linkedin_url"]}"}}}}' for v in voices)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-WMWEZTSWM0"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-WMWEZTSWM0');</script>
  <meta name="description" content="Data-driven rankings of the 25 most influential prompt engineers, AI engineers, and educators shaping how professionals work with AI systems.">
  <title>Top 25 Prompt Engineering Voices 2026 — PE Collective</title>
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/voices/">
  <meta property="og:title" content="Top 25 Prompt Engineering Voices of 2026">
  <meta property="og:description" content="Rankings of the most influential prompt engineers and AI educators.">
  <meta property="og:image" content="{BASE_URL}/assets/social-preview.png">
  <meta property="og:site_name" content="{SITE_NAME}">
  <link rel="canonical" href="{BASE_URL}/voices/">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Top 25 Prompt Engineering Voices of 2026">
  <meta name="twitter:description" content="Rankings of the most influential prompt engineers and AI educators.">
  <meta name="twitter:image" content="{BASE_URL}/assets/social-preview.png">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"{BASE_URL}/"}},{{"@type":"ListItem","position":2,"name":"Top Voices","item":"{BASE_URL}/voices/"}}]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"ItemList","name":"{data["title"]}","numberOfItems":{len(voices)},"itemListElement":[{list_items}]}}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"Article","headline":"{data["title"]}","author":{{"@type":"Person","name":"Rome Thorndike"}},"publisher":{{"@type":"Organization","name":"{SITE_NAME}"}},"datePublished":"2026-04-14","dateModified":"{last_updated}","url":"{BASE_URL}/voices/"}}
  </script>
  <link rel="icon" type="image/jpeg" href="/assets/logo.jpeg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Space+Grotesk:wght@400;500;600;700&display=swap" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="/assets/css/style.css">
  <style>
.voices-hero {{ text-align: center; padding: var(--space-4xl) 0 var(--space-2xl); }}
.voices-hero .eyebrow {{ color: var(--color-gold); font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem; }}
.voices-hero h1 {{ font-family: var(--font-display); font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 700; margin-bottom: 0.75rem; }}
.voices-subtitle {{ font-size: 1.1rem; color: var(--color-text-secondary); margin-bottom: 0.5rem; }}
.voices-meta {{ font-size: 0.85rem; color: var(--color-text-muted); }}
.voices-content {{ max-width: 800px; margin: 0 auto; padding: 0 1.5rem var(--space-3xl); }}
.voice-methodology {{ margin-bottom: var(--space-xl); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius-lg); background: var(--color-bg-card); }}
.voice-methodology summary {{ padding: 1rem 1.25rem; cursor: pointer; color: var(--color-text-primary); font-weight: 600; }}
.voice-methodology summary:hover {{ color: var(--color-gold); }}
.methodology-content {{ padding: 0 1.25rem 1.25rem; font-size: 0.9rem; color: var(--color-text-secondary); line-height: 1.7; }}
.methodology-content ul {{ padding-left: 1.25rem; margin: 0.75rem 0; }}
.methodology-content li {{ margin-bottom: 0.5rem; }}
.voices-jump-nav {{ display: flex; flex-wrap: wrap; gap: 0.25rem; margin-bottom: var(--space-xl); padding: 0.75rem; background: var(--color-bg-card); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius-lg); }}
.voice-jump-link {{ font-size: 0.75rem; font-family: monospace; padding: 0.25rem 0.5rem; border-radius: 6px; color: var(--color-text-muted); text-decoration: none; transition: background 0.15s, color 0.15s; }}
.voice-jump-link:hover {{ background: var(--color-gold); color: var(--color-bg-dark); }}
.voices-section-heading {{ font-family: var(--font-display); font-size: 1.3rem; margin-bottom: 0.5rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--color-gold); }}
.voices-grid {{ display: flex; flex-direction: column; gap: 1rem; margin-bottom: var(--space-2xl); }}
.voice-card {{ border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius-lg); background: var(--color-bg-card); padding: 1.25rem; transition: border-color 0.25s, box-shadow 0.25s; }}
.voice-card:hover {{ border-color: var(--color-gold); box-shadow: var(--shadow-glow); }}
.voice-card-header {{ display: flex; align-items: flex-start; gap: 0.75rem; }}
.voice-rank, .voice-rank-top {{ font-family: monospace; font-weight: 700; font-size: 1.1rem; min-width: 2.5rem; text-align: center; flex-shrink: 0; color: var(--color-text-muted); }}
.voice-rank-top {{ color: var(--color-gold-light); font-size: 1.25rem; }}
.voice-card-info {{ flex: 1; min-width: 0; }}
.voice-name {{ font-size: 1.1rem; font-weight: 600; margin: 0 0 0.25rem; }}
.voice-name a {{ color: var(--color-text-primary); text-decoration: none; }}
.voice-name a:hover {{ color: var(--color-gold-light); }}
.voice-title {{ font-size: 0.85rem; color: var(--color-text-secondary); margin: 0 0 0.5rem; }}
.voice-tags {{ display: flex; flex-wrap: wrap; gap: 0.35rem; }}
.voice-tag {{ font-size: 0.7rem; font-family: monospace; padding: 0.15rem 0.5rem; border-radius: 999px; background: rgba(232,168,124,0.1); color: var(--color-gold); font-weight: 500; }}
.voice-linkedin-btn {{ flex-shrink: 0; display: flex; align-items: center; justify-content: center; width: 2.25rem; height: 2.25rem; border-radius: 6px; color: var(--color-text-muted); text-decoration: none; }}
.voice-linkedin-btn:hover {{ color: #0077B5; background: rgba(0,119,181,0.15); }}
.voice-bio {{ margin: 0.75rem 0 0; font-size: 0.9rem; color: var(--color-text-secondary); line-height: 1.7; padding-left: calc(2.5rem + 0.75rem); }}
.voices-share-cta {{ text-align: center; padding: var(--space-xl) 1.5rem; max-width: 600px; margin: 0 auto; }}
.voices-share-cta h2 {{ font-family: var(--font-display); font-size: 1.3rem; margin-bottom: 0.5rem; }}
.voices-share-cta p {{ color: var(--color-text-secondary); margin-bottom: 0.5rem; }}
@media (max-width: 640px) {{ .voice-bio {{ padding-left: 0; }} .voice-card-header {{ flex-wrap: wrap; }} .voice-card {{ position: relative; }} .voice-linkedin-btn {{ position: absolute; top: 1rem; right: 1rem; }} .voices-jump-nav {{ display: none; }} }}
  </style>
</head>
<body>
  <a href="#main" class="skip-link">Skip to main content</a>
  <header class="header">
    <div class="container">
      <div class="header__inner">
        <a href="/" class="header__logo">
          <img src="/assets/logo.jpeg" alt="PE Collective Logo" width="36" height="36">
          <span>PE Collective</span>
        </a>
        <nav class="header__nav">
          <a href="/jobs/">AI Jobs</a>
          <a href="/salaries/">Salaries</a>
          <a href="/tools/">Tools</a>
          <a href="/voices/" class="active">Top Voices</a>
          <a href="/blog/">Blog</a>
          <a href="/insights/">Market Intel</a>
          <a href="/about/">About</a>
        </nav>
        <div class="header__cta">
          <a href="/join/" class="btn btn--secondary btn--small">Join Community</a>
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
      <li><a href="/jobs/">AI Jobs</a></li>
      <li><a href="/salaries/">Salaries</a></li>
      <li><a href="/tools/">Tools</a></li>
      <li><a href="/voices/">Top Voices</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/insights/">Market Intel</a></li>
      <li><a href="/about/">About</a></li>
    </ul>
    <a href="/join/" class="header__mobile-cta">Join Community</a>
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
    <section class="voices-hero">
      <div class="container">
        <div class="eyebrow">2026 RANKINGS</div>
        <h1>{data["title"]}</h1>
        <p class="voices-subtitle">{data.get("subtitle", "")}</p>
        <p class="voices-meta">Last updated: {last_updated} &middot; {len(voices)} voices ranked</p>
      </div>
    </section>

    <div class="voices-content">
      <details class="voice-methodology">
        <summary>How We Ranked These Voices</summary>
        <div class="methodology-content">
          <p>{data.get("methodology", "")}</p>
          <ul>
            <li><strong>Topic relevance</strong> (required): Must actively contribute to prompt engineering or AI engineering.</li>
            <li><strong>Published work</strong> (30%): Open-source tools, guides, courses, books that advance the discipline.</li>
            <li><strong>Community impact</strong> (25%): Building communities, teaching, open-source contributions.</li>
            <li><strong>Content reach</strong> (25%): Newsletter subscribers, GitHub stars, LinkedIn following.</li>
            <li><strong>Originality</strong> (20%): Original techniques, frameworks, and tools.</li>
          </ul>
        </div>
      </details>

      <div class="voices-jump-nav">{jump_links}</div>

      <h2 class="voices-section-heading">Top 10 Leaders</h2>
      <p style="color: var(--color-text-secondary); margin-bottom: 1rem;">The most recognized voices shaping prompt engineering and AI engineering.</p>
      <div class="voices-grid">{leaders_html}</div>

      <h2 class="voices-section-heading">Rising Voices (11-25)</h2>
      <p style="color: var(--color-text-secondary); margin-bottom: 1rem;">Educators, builders, and thought leaders gaining momentum.</p>
      <div class="voices-grid">{rising_html}</div>
    </div>

    <section class="voices-share-cta">
      <h2>Made the List?</h2>
      <p>Share it. Tag us on LinkedIn. We will amplify your post.</p>
      <p>Know someone who should be on next year's list? <a href="mailto:rome@getprovyx.com">Let us know</a>.</p>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div class="footer__brand">
          <a href="/" class="footer__logo">
            <img src="/assets/logo.jpeg" alt="PE Collective" width="32" height="32">
            <span>PE Collective</span>
          </a>
          <p class="footer__tagline">The job board and community built by AI professionals, for AI professionals.</p>
        </div>
        <div class="footer__column">
          <h4>Jobs</h4>
          <nav class="footer__links">
            <a href="/jobs/">All Jobs</a>
            <a href="/jobs/?category=prompt-engineer">Prompt Engineer</a>
            <a href="/jobs/?category=ai-engineer">AI Engineer</a>
            <a href="/jobs/?remote=true">Remote Only</a>
          </nav>
        </div>
        <div class="footer__column">
          <h4>Tools</h4>
          <nav class="footer__links">
            <a href="/tools/">All Tools</a>
            <a href="/voices/">Top Voices</a>
            <a href="/glossary/">Glossary</a>
          </nav>
        </div>
        <div class="footer__column">
          <h4>Community</h4>
          <nav class="footer__links">
            <a href="/join/">Join Us</a>
            <a href="/about/">About</a>
            <a href="https://ainewsdigest.substack.com" target="_blank" rel="noopener">Newsletter</a>
          </nav>
        </div>
      </div>
      <div class="footer__bottom">
        <span>&copy; 2026 PE Collective. All rights reserved.</span>
        <span>Part of the <a href="https://ainewsdigest.substack.com" target="_blank" rel="noopener">AI News Digest</a> network.</span>
      </div>
    </div>
  </footer>
</body>
</html>'''

    os.makedirs('site/voices', exist_ok=True)
    with open('site/voices/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated: /voices/ ({len(voices)} voices)")

if __name__ == '__main__':
    print("Generating Top Voices page...")
    generate()
    print("Done!")
