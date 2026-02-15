# PE Collective SEO Improvement Plan

**Date:** 2026-02-14
**Based on:** [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) framework + full site audit
**Current SEO score estimate:** 7/10 (up from 5/10 after Jan 28 fixes)
**Target:** 9/10

---

## Phase 1: Fix Critical & High-Priority Technical Issues

These are bugs/gaps that actively hurt rankings or user experience right now.

### 1.1 Mobile Navigation on Static Pages (CRITICAL)

**Problem:** `header__nav` is `display: none` at 768px on 8 static pages (homepage, about, join, tools index, cursor review, copilot review, comparison, root jobs) with no hamburger menu. Generated pages already have mobile nav via `templates.py`.

**Fix:** Port the mobile nav pattern from `templates.py` into all static page templates. This means adding:
- Hamburger toggle button in the header
- Mobile nav overlay/drawer HTML
- Toggle JS (inline, same as generated pages)
- CSS for mobile nav states

**Files:** `index.html`, `about/index.html`, `join/index.html`, `tools/index.html`, `tools/cursor/index.html`, `tools/github-copilot/index.html`, `tools/cursor-vs-github-copilot/index.html`, `assets/css/style.css`

### 1.2 Kill Dead `#` Links on Tools Index (HIGH)

**Problem:** 10 tool/comparison cards on `/tools/` link to `#`. Dead links waste crawl budget and signal low-quality content to Google.

**Options (pick one):**
- **A) Remove unlaunched tool cards entirely** until pages exist
- **B) Keep cards but remove links** (make them non-clickable "coming soon" cards)
- **C) Create stub pages** for each tool with basic info + "full review coming soon"

**Recommendation:** Option B for tools without enough content to review yet; Option C for tools you plan to cover soon (creates indexable pages).

### 1.3 Consistent Templates Between Static and Generated Pages (HIGH)

**Problem:** Static pages have different footer layout, missing `twitter:site`, missing `apple-touch-icon`, 2025 copyright year, and different nav structure compared to generated pages.

**Fix:** Create a shared HTML template fragment (or just manually align) so all pages have:
- Same footer with 2026 copyright
- `twitter:site` = `@pe_collective`
- `<link rel="apple-touch-icon">` referencing the correct icon
- Matching nav links
- Consistent `og:url` trailing slash format

**Files:** All 8 static page HTML files

### 1.4 Font Loading Performance (HIGH)

**Problem:** Google Fonts loaded via `@import` in CSS (render-blocking).

**Fix:** Replace the `@import url(...)` in `style.css` line 4 with `<link rel="preconnect">` + `<link rel="stylesheet">` in the `<head>` of every HTML file, with `font-display: swap`. Generated pages already have `preconnect` hints.

### 1.5 Organization Schema Completion (MEDIUM)

**Problem:** `sameAs` array is empty in Organization schema.

**Fix:** Add social profile URLs:
```json
"sameAs": [
  "https://twitter.com/pe_collective",
  "https://www.linkedin.com/company/pe-collective",
  "https://pecollective.substack.com"
]
```

---

## Phase 2: Schema Markup Enrichment

Based on the marketingskills `schema-markup` skill, these are missed rich snippet opportunities.

### 2.1 Review Schema on Tool Pages

**Opportunity:** Cursor (4.8/5) and Copilot (4.3/5) reviews have explicit ratings but no `Review` or `SoftwareApplication` schema. Adding these can trigger review star rich snippets in Google.

**Implementation:**
```json
{
  "@type": "SoftwareApplication",
  "name": "Cursor",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Windows, macOS, Linux",
  "review": {
    "@type": "Review",
    "author": { "@type": "Person", "name": "Rome Thorndike" },
    "reviewRating": { "@type": "Rating", "ratingValue": "4.8", "bestRating": "5" },
    "reviewBody": "..."
  }
}
```

**Files:** `tools/cursor/index.html`, `tools/github-copilot/index.html`

### 2.2 ItemList Schema on Index Pages

**Opportunity:** Jobs index, tools index, and blog index can use `ItemList` schema for potential rich results (carousel appearance).

**Files:** `tools/index.html`, `scripts/generate_job_board.py`, blog template in `scripts/templates.py`

### 2.3 ComparisonPage / ItemList on Comparison Pages

**Opportunity:** The Cursor vs Copilot page can use a structured comparison schema combining two `SoftwareApplication` entities.

**File:** `tools/cursor-vs-github-copilot/index.html`

---

## Phase 3: Content Strategy (Programmatic SEO)

This is the biggest growth lever. The marketingskills repo outlines 12 programmatic SEO playbooks. Here's which ones apply to PE Collective and how:

### 3.1 Glossary Pages — "What is [AI/ML Term]?" (Playbook #9)

**Search pattern:** "what is prompt engineering", "what is RAG", "what is fine-tuning", "what is an AI agent"

**Implementation:**
- Create `/glossary/` hub page listing all terms
- Individual pages at `/glossary/{term}/` (e.g., `/glossary/rag/`, `/glossary/chain-of-thought/`)
- Each page: definition, examples, how it relates to prompt engineering, link to relevant blog posts/tools
- Add `DefinedTerm` schema markup
- Target 20-30 terms initially, expand to 100+

**Data source:** Extract terms from existing job posting data (skills/requirements fields) + manual curation

**Template additions needed in `scripts/`:** `generate_glossary_pages.py`

### 3.2 Comparison Pages — "[Tool A] vs [Tool B]" (Playbook #4)

**Search pattern:** "cursor vs windsurf", "copilot vs codeium", "langchain vs llamaindex"

**Current state:** 1 comparison page exists (Cursor vs Copilot). The tools index has placeholder cards for 2 more comparisons.

**Implementation:**
- Build comparison data file (YAML/JSON) per the marketingskills `competitor-alternatives` content architecture pattern
- Create `/tools/{a}-vs-{b}/` pages for high-volume AI tool comparisons
- Include: feature table, pricing breakdown, "best for" recommendations, FAQ schema
- Target 5-10 comparisons initially

**Priority comparisons:**
- Cursor vs Windsurf
- GitHub Copilot vs Amazon CodeWhisperer
- LangChain vs LlamaIndex
- Pinecone vs Weaviate vs Chroma (three-way)
- Claude vs ChatGPT for coding

### 3.3 Salary Pages by Role/Location/Seniority (Playbook #6 + #8)

**Search pattern:** "prompt engineer salary NYC", "AI engineer salary remote", "senior ML engineer salary"

**Current state:** 5 salary filter pages exist. This can scale significantly.

**Implementation:**
- Cross-multiply: roles x locations x seniority levels
- `/salaries/prompt-engineer/` (exists)
- `/salaries/prompt-engineer/new-york/`
- `/salaries/senior-ai-engineer/remote/`
- Only create pages where you have >= 5 data points (avoid thin content)
- Include comparison charts, trends over time, related job listings

**Template additions:** Extend `generate_salary_pages.py` with location/seniority cross-filters

### 3.4 "Best [Tools] for [Use Case]" Curation Pages (Playbook #2)

**Search pattern:** "best AI coding tools 2026", "best prompt engineering tools", "best vector databases"

**Implementation:**
- Create `/tools/best-{category}/` pages
- Each curates 5-7 tools with mini-reviews, pricing, pros/cons
- Categories: AI coding assistants, vector databases, LLM frameworks, prompt testing tools
- Link each tool to its individual review page (when available)
- Add `ItemList` schema

### 3.5 Job Category Landing Pages (Playbook #7 — Personas)

**Search pattern:** "prompt engineer jobs remote", "AI engineer jobs San Francisco", "entry level ML jobs"

**Current state:** ~10 category pages exist for role type, location, and seniority.

**Implementation:**
- Ensure all meaningful combinations are covered
- Add unique intro copy per category (not just filtered job listings)
- Add salary range data inline
- Add "related categories" cross-links
- FAQ schema per category with common questions

### 3.6 Blog Content Expansion

**Current state:** 3 blog posts. This is thin for building topical authority.

**Content calendar priorities (based on marketingskills keyword-by-buyer-stage framework):**

**Awareness stage:**
- "What Does a Prompt Engineer Do? (2026 Guide)"
- "How to Become a Prompt Engineer with No Experience"
- "Is Prompt Engineering a Real Career?"
- "AI Engineer vs ML Engineer vs Prompt Engineer: What's the Difference?"

**Consideration stage:**
- "Top 10 Prompt Engineering Certifications Worth Getting in 2026"
- "Best Prompt Engineering Courses (Free & Paid)"
- "Prompt Engineering Portfolio: What to Include + Examples"

**Decision stage:**
- "Prompt Engineering Interview Questions & Answers"
- "Prompt Engineering Resume Template"
- "How to Negotiate Your AI Engineer Salary"

**Implementation stage:**
- "Prompt Engineering Templates for [Use Case]" (multiple)
- "Chain of Thought Prompting: Complete Tutorial"
- "System Prompts: Best Practices & Examples"

Target: 2-4 posts/month, each 2,000+ words, with proper Article schema, internal links to tools/jobs/salaries.

---

## Phase 4: Answer Engine Optimization (AEO/GEO)

Based on the marketingskills `aeo-geo-patterns.md` reference. This optimizes content to appear in AI-generated answers (ChatGPT, Claude, Perplexity, Google AI Overviews).

### 4.1 Add AEO-Optimized Content Blocks

**Definition blocks** on glossary pages:
```html
<p><strong>Prompt engineering</strong> is the practice of designing and optimizing
inputs to large language models (LLMs) to produce accurate, relevant, and useful
outputs. Prompt engineers...</p>
```

**Step-by-step blocks** on tutorial blog posts:
```html
<ol>
  <li><strong>Define the task clearly.</strong> Start by...</li>
  <li><strong>Provide context and constraints.</strong> Include...</li>
</ol>
```

**FAQ blocks** on category and tool pages (already have FAQ schema on homepage — extend to all key pages).

### 4.2 Add GEO-Optimized Content Blocks

**Statistic citations** from your job posting data:
> "According to PE Collective's analysis of 1,300+ job postings, the median prompt engineer salary is $145,000 as of February 2026."

**Self-contained answer blocks** that AI can quote directly:
> "The three most in-demand prompt engineering skills in 2026 are: Python proficiency (mentioned in 78% of listings), experience with RAG architectures (62%), and chain-of-thought prompting (51%)."

Your proprietary job posting data is a massive GEO advantage — AI models cite sources with original data at significantly higher rates.

### 4.3 Voice Search Optimization

Add conversational Q&A content targeting "People Also Ask" patterns:
- "How much do prompt engineers make?"
- "Do you need a degree to be a prompt engineer?"
- "What's the difference between prompt engineering and AI engineering?"

Keep answers under 30 words for the direct answer, then expand.

---

## Phase 5: Technical SEO Polish

### 5.1 Custom 404 Page

Create `404.html` with:
- Navigation to key sections
- Search suggestion
- Links to popular pages (jobs, salaries, tools)
- Proper meta tags (noindex)

### 5.2 CSS Minification

Add a CSS minification step to the GitHub Actions build workflow. Options:
- `csso` or `clean-css-cli` (Node)
- Python `cssmin` or `rcssmin`
- Or just inline critical CSS on static pages like generated pages already do

### 5.3 Image Strategy

The site has almost zero images. Add:
- Screenshots to tool review pages
- Data visualization charts to salary/insights pages (can be SVG or generated PNGs)
- Author photo on about page and blog post schema
- All images with descriptive `alt` text and `loading="lazy"`

### 5.4 Blog Post Visible Dates

Add publication date and "last updated" date to blog post templates. Visible dates build trust and are a soft ranking signal. Update `templates.py` to render dates.

### 5.5 Sitemap Tuning

- Change blog post `changefreq` from "weekly" to "monthly"
- Add `lastmod` dates that actually reflect content changes
- Consider separate sitemaps per content type (jobs, blog, tools, glossary) as content grows

---

## Phase 6: Off-Page & Authority Building

### 6.1 Free Tool Strategy (from marketingskills `free-tool-strategy`)

Create a free tool that attracts backlinks and establishes authority:

**Recommendation: "AI Salary Calculator"**
- Input: role, location, seniority, skills
- Output: estimated salary range based on your job posting data
- URL: `/tools/ai-salary-calculator/`
- Search target: "AI engineer salary calculator", "prompt engineer salary calculator"
- Backlink magnet: journalists, career blogs, and LinkedIn posts will link to this

**Alternative: "Prompt Tester"**
- Input: a prompt
- Output: analysis of prompt quality, suggestions for improvement
- Higher build effort but extremely shareable

### 6.2 Proprietary Data Content

Your 1,300+ job posting dataset is a competitive moat. Publish:
- Monthly or quarterly "State of AI Jobs" reports
- "AI Salary Trends" with charts
- "Most In-Demand AI Skills" rankings

These attract backlinks from journalists and industry blogs covering AI career trends. The marketingskills framework ranks proprietary data as the #1 content type for link building.

### 6.3 Platform Publishing (Parasite SEO)

Republish summarized versions of your best content on:
- Medium (tag: artificial-intelligence, prompt-engineering)
- LinkedIn articles
- Substack (if not already)
- Dev.to / Hashnode for developer audience

Always link back to the full version on pecollective.com. This builds domain authority and referral traffic.

---

## Implementation Priority Matrix

| Phase | Effort | SEO Impact | Timeline |
|-------|--------|------------|----------|
| **Phase 1:** Technical fixes | Low | High | Week 1 |
| **Phase 2:** Schema enrichment | Low | Medium | Week 1-2 |
| **Phase 3:** Content strategy | High | Very High | Ongoing (weeks 2-12+) |
| **Phase 4:** AEO/GEO optimization | Medium | High | Weeks 3-6 |
| **Phase 5:** Technical polish | Low-Medium | Medium | Weeks 2-4 |
| **Phase 6:** Off-page & authority | Medium-High | Very High | Ongoing |

### Quick Wins (do first):
1. Fix mobile nav on static pages (Phase 1.1)
2. Kill dead `#` links (Phase 1.2)
3. Add Review schema to tool pages (Phase 2.1)
4. Fill Organization `sameAs` (Phase 1.5)
5. Add visible dates to blog posts (Phase 5.4)
6. Fix font loading (Phase 1.4)

### Biggest Growth Levers:
1. Glossary pages (Phase 3.1) — high-volume informational queries
2. More comparison pages (Phase 3.2) — high-intent, low-competition
3. Blog content expansion (Phase 3.6) — topical authority building
4. AI Salary Calculator tool (Phase 6.1) — backlink magnet
5. Proprietary data reports (Phase 6.2) — authority + backlinks + GEO citations

### Content Volume Targets:
- **Month 1:** 10 glossary pages, 2 comparisons, 2 blog posts
- **Month 2:** 15 glossary pages, 3 comparisons, 3 blog posts, salary calculator launch
- **Month 3:** 15 glossary pages, 2 comparisons, 4 blog posts, first data report
- **Ongoing:** 10+ pages/month across all content types

---

## Measurement

Track these metrics monthly:

| Metric | Tool | Baseline | Target (3 months) |
|--------|------|----------|-------------------|
| Indexed pages | Google Search Console | ~49 | 150+ |
| Organic impressions | GSC | Measure now | 3x current |
| Organic clicks | GSC | Measure now | 3x current |
| Average position | GSC | Measure now | Improve top queries |
| Pages with rich results | GSC Enhancements | 0 | 10+ |
| Referring domains | Ahrefs/SEMrush | Measure now | +20 |
| AI citation rate | Manual checks in ChatGPT/Perplexity | 0 | Cited for salary queries |

---

## Appendix: marketingskills Playbooks Not Applicable

These playbooks from the repo don't apply to PE Collective:

| Playbook | Why N/A |
|----------|---------|
| Conversions (X to Y) | No conversion tools relevant |
| Locations | Not a local service |
| Integrations | Not a SaaS product |
| Translations | English-only audience |
| Directory | Covered by tools section already |
| Profiles | Not enough entities to profile |
