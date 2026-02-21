#!/usr/bin/env python3
"""
Generate category filter pages for programmatic SEO.
Creates pages like /jobs/prompt-engineer/, /jobs/remote/, /jobs/san-francisco/
"""

import pandas as pd
from datetime import datetime
import glob
import os
import json
import sys
import hashlib
import re
import traceback

# Add scripts directory to path using absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from templates import get_html_head, get_nav_html, get_footer_html, get_cta_box, get_breadcrumb_schema, format_salary, is_remote, BASE_URL, SITE_NAME
except Exception as e:
    print(f"ERROR importing templates: {e}")
    traceback.print_exc()
    sys.exit(1)

DATA_DIR = 'data'
SITE_DIR = 'site'
JOBS_DIR = f'{SITE_DIR}/jobs'

print("="*70)
print("  PE COLLECTIVE - GENERATING CATEGORY PAGES")
print("="*70)

# Load job data
files = glob.glob(f"{DATA_DIR}/ai_jobs_*.csv")
if files:
    df = pd.read_csv(max(files, key=os.path.getctime))
elif os.path.exists(f"{DATA_DIR}/jobs.json"):
    with open(f"{DATA_DIR}/jobs.json") as f:
        df = pd.DataFrame(json.load(f).get('jobs', []))
else:
    print(" No job data found")
    exit(1)

print(f"\n Loaded {len(df)} jobs")


def make_slug(text):
    if pd.isna(text):
        return ''
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')[:50]


def escape_html(text):
    if pd.isna(text):
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


CATEGORY_CONTENT = {
    'prompt-engineer': {
        'intro': '''<p>Prompt engineers design, test, and optimize the inputs that make AI systems useful. It's one of the fastest-growing roles in tech, with companies like Anthropic, OpenAI, and Jasper hiring dedicated prompt engineering teams.</p>
<p>The role sits at the intersection of writing, logic, and software engineering. You'll spend your days crafting system prompts, building evaluation frameworks, running A/B tests on prompt variations, and figuring out why a model that worked perfectly yesterday is hallucinating today. Most positions require Python fluency and hands-on experience with at least two major LLM providers.</p>
<p>Salaries range from $90K for entry-level positions to $250K+ at top AI labs. Remote roles are common, especially at startups building AI-native products.</p>''',
        'faqs': [
            ('What does a prompt engineer do?', 'Prompt engineers design and optimize inputs to large language models. Day-to-day work includes writing system prompts, building evaluation pipelines, running A/B tests on prompt variations, and integrating LLM outputs into production applications.'),
            ('Do prompt engineers need to code?', 'Yes. Most job postings require Python proficiency. You\'ll work with LLM APIs, build evaluation scripts, and often integrate prompts into larger software systems. Pure "no-code" prompt engineering jobs exist but are rare and pay less.'),
            ('What salary can a prompt engineer expect?', 'Entry-level prompt engineers earn $90K-$130K. Mid-level roles pay $130K-$180K. Senior positions at major AI companies range from $180K-$300K, with total compensation (including equity) often higher.'),
        ],
    },
    'ai-ml-engineer': {
        'intro': '''<p>AI/ML engineers build the systems that power machine learning in production. Unlike research roles, this is about shipping: taking models from prototype to products that handle millions of requests.</p>
<p>You'll work across the full ML stack. Training pipelines, feature stores, model serving infrastructure, monitoring and retraining loops. Most teams expect strong Python and at least one deep learning framework (PyTorch or TensorFlow). Cloud experience with AWS, GCP, or Azure is nearly universal in job requirements.</p>
<p>This is one of the highest-paying engineering specializations. Companies are competing aggressively for engineers who can build reliable ML systems at scale, and salaries reflect that demand.</p>''',
        'faqs': [
            ('What\'s the difference between an AI engineer and an ML engineer?', 'ML engineers focus on model training, evaluation, and deployment. AI engineers have a broader scope that includes LLM integration, agent development, and AI product architecture. In practice, many job postings use the terms interchangeably.'),
            ('What skills do AI/ML engineers need?', 'Python, PyTorch or TensorFlow, cloud platforms (AWS/GCP), SQL, and experience with ML pipelines. Senior roles add system design, distributed computing, and the ability to evaluate research papers for production viability.'),
            ('What is the average AI/ML engineer salary?', 'Mid-level AI/ML engineers earn $160K-$220K. Senior and staff roles at major tech companies pay $220K-$400K+ in total compensation. Remote positions typically pay 85-95% of Bay Area rates.'),
        ],
    },
    'ai-agent-developer': {
        'intro': '''<p>AI agent developers build autonomous systems that can reason, plan, and execute multi-step tasks. This is one of the newest roles in AI, emerging as companies move beyond simple chatbots to agentic AI products.</p>
<p>The work involves designing agent architectures, implementing tool-use patterns, building memory systems, and creating guardrails that keep autonomous agents from going off the rails. You'll use frameworks like LangGraph, CrewAI, or custom architectures, and spend significant time on evaluation and safety testing.</p>
<p>Demand is growing fast. Every major tech company is investing in agent capabilities, and startups focused on agentic AI are raising significant funding. If you have experience building reliable multi-step AI workflows, you're in high demand.</p>''',
        'faqs': [
            ('What is an AI agent developer?', 'An AI agent developer builds autonomous AI systems that can break down goals into steps, use tools (APIs, databases, web browsers), and execute complex workflows with minimal human oversight. It\'s a specialized role combining LLM expertise with software architecture.'),
            ('What skills do AI agent developers need?', 'Strong Python, experience with LLM APIs (OpenAI, Anthropic), familiarity with agent frameworks (LangGraph, CrewAI), understanding of tool-use patterns, and solid software engineering fundamentals. Safety and evaluation experience is increasingly important.'),
            ('How much do AI agent developers make?', 'AI agent developer salaries range from $145K-$230K at mid-level to $200K-$300K+ for senior positions. This is a specialized, high-demand role, and compensation reflects the scarcity of experienced candidates.'),
        ],
    },
    'research-engineer': {
        'intro': '''<p>Research engineers work at the frontier of AI, turning research ideas into working systems. You'll find these roles at AI labs like DeepMind, Anthropic, and Meta AI, as well as at universities and corporate research divisions.</p>
<p>The job combines engineering rigor with research intuition. You'll implement papers, run large-scale experiments, build custom training infrastructure, and collaborate closely with research scientists. Most positions expect familiarity with transformer architectures, training dynamics, and at least one publication or equivalent project experience.</p>
<p>These are among the highest-paying AI roles, especially at major labs where research engineers work directly on frontier models. Competition is intense, but the work is some of the most interesting in the field.</p>''',
        'faqs': [
            ('Do I need a PhD to be a research engineer?', 'Not always, but it helps. Many AI labs hire research engineers with strong MS degrees or exceptional project portfolios. Publications in top venues (NeurIPS, ICML, ICLR) significantly strengthen applications, regardless of degree level.'),
            ('What\'s the difference between a research engineer and a research scientist?', 'Research scientists focus on designing experiments and developing new methods. Research engineers focus on building the infrastructure to run those experiments at scale. In practice, the roles overlap significantly, especially at smaller labs.'),
            ('What do research engineers earn?', 'Research engineers at top AI labs earn $180K-$320K in base salary, with total compensation (including equity and bonuses) often reaching $400K-$600K at staff level. Academic positions pay significantly less.'),
        ],
    },
    'senior': {
        'intro': '''<p>Senior AI positions require 5+ years of experience and a track record of shipping production ML systems. These roles come with higher compensation, more autonomy, and the expectation that you'll mentor junior engineers and influence technical direction.</p>
<p>At this level, companies expect you to make architectural decisions, evaluate build-vs-buy tradeoffs, and translate business requirements into technical specifications. You'll spend less time writing code from scratch and more time designing systems, reviewing code, and unblocking your team.</p>
<p>Titles at this level include Senior Engineer, Staff Engineer, Principal Engineer, and Engineering Manager. Compensation jumps significantly from mid-level, with total packages at major companies often exceeding $300K.</p>''',
        'faqs': [
            ('What experience do senior AI roles require?', 'Most postings require 5-8 years of software engineering experience with 3+ years focused on ML/AI. Demonstrated ability to ship production systems, mentor others, and make architectural decisions is more important than specific years.'),
            ('What is the salary difference between mid and senior AI roles?', 'Senior AI engineers typically earn 30-50% more than mid-level. A mid-level AI engineer earning $175K might see $230K-$280K at senior level, with staff/principal roles reaching $350K-$500K in total compensation.'),
        ],
    },
    'entry-level': {
        'intro': '''<p>Entry-level AI positions are competitive but growing. Companies increasingly hire junior engineers who can work with LLMs, build simple ML pipelines, and contribute to AI product development from day one.</p>
<p>Most entry-level roles expect a CS degree (or equivalent), Python fluency, and demonstrated interest in AI through projects, coursework, or open-source contributions. You won't need to have trained a foundation model, but you should be comfortable using LLM APIs, understanding basic ML concepts, and writing production-quality code.</p>
<p>The best path in: build something. A portfolio project that uses RAG, fine-tuning, or agent architectures will get you further than another certification. Companies want to see that you can ship working AI features, not just complete tutorials.</p>''',
        'faqs': [
            ('Can I get an AI job with no experience?', 'Yes, but you need to demonstrate skills. Build projects using LLM APIs, contribute to open-source AI tools, or complete hands-on courses from DeepLearning.AI or fast.ai. A strong portfolio compensates for lack of professional experience.'),
            ('What entry-level AI roles are available?', 'Common entry-level titles include Junior Prompt Engineer, AI Engineer I, ML Engineer (Associate), and AI/ML Intern. Some companies also hire "AI Support Engineers" or "LLM Specialists" at junior levels.'),
            ('What do entry-level AI jobs pay?', 'Entry-level AI positions pay $90K-$140K depending on location and company. Remote entry-level roles average around $100K. Top AI companies (Anthropic, OpenAI, Google) pay toward the higher end even for junior positions.'),
        ],
    },
    'remote': {
        'intro': '''<p>Remote AI jobs let you work from anywhere while building cutting-edge AI products. The AI industry has embraced remote work more than most tech sectors, with many companies operating fully distributed teams.</p>
<p>Remote positions span every role type: prompt engineering, ML engineering, AI research, and product management. Salaries for remote roles typically run 85-95% of Bay Area rates, which makes them an excellent value proposition for engineers outside major tech hubs.</p>
<p>Companies offering remote AI roles range from AI-native startups to enterprise teams building AI features into existing products. The key differentiator: remote-first companies (Hugging Face, Scale AI, etc.) tend to have better remote culture than traditional companies that added remote options post-pandemic.</p>''',
        'faqs': [
            ('Do remote AI jobs pay less?', 'Slightly. Most remote AI positions pay 85-95% of Bay Area rates. Some companies (like GitLab) use location-based adjustments, while others pay the same regardless of location. The cost-of-living savings usually make remote positions financially advantageous.'),
            ('What remote AI companies are hiring?', 'Major remote-friendly AI employers include Scale AI, Hugging Face, Weights & Biases, Jasper, and many AI startups. Larger companies like Meta, Google, and Amazon offer remote options for some AI roles.'),
        ],
    },
    'san-francisco': {
        'intro': '''<p>San Francisco remains the global capital of AI development. OpenAI, Anthropic, and dozens of well-funded AI startups are headquartered here, creating the densest concentration of AI jobs anywhere in the world.</p>
<p>Bay Area AI salaries are the highest in the industry, reflecting both the cost of living and the intense competition for talent. Most positions offer hybrid arrangements (2-3 days in office), with fewer fully remote options than other markets.</p>
<p>The tradeoff: you'll earn more but spend more. A $250K salary in SF has roughly the same purchasing power as $175K in Austin or $165K in a smaller metro. That said, the networking, career growth, and caliber of colleagues are hard to replicate elsewhere.</p>''',
        'faqs': [
            ('What is the average AI salary in San Francisco?', 'AI engineers in San Francisco earn $180K-$350K in base salary, with total compensation (base + equity + bonus) often reaching $300K-$500K at senior levels. Entry-level positions start around $140K-$180K.'),
            ('Which AI companies are in San Francisco?', 'Major AI employers in SF include OpenAI, Anthropic, Scale AI, Databricks, Stripe (ML team), and hundreds of AI startups. The broader Bay Area adds Google DeepMind (Mountain View), Meta AI (Menlo Park), and Apple ML (Cupertino).'),
        ],
    },
    'new-york': {
        'intro': '''<p>New York City is a growing hub for AI talent, driven by fintech, media, and enterprise AI adoption. Companies like Bloomberg, Two Sigma, and Notion have significant AI teams in NYC, alongside a thriving startup ecosystem.</p>
<p>NYC AI salaries are 5-10% below San Francisco but well above most other markets. The city's strength is in applied AI: using ML for trading, content generation, advertising, and enterprise applications. Research roles are less common than in the Bay Area.</p>
<p>Most NYC AI positions offer hybrid work, typically 2-3 days in office. The financial services sector drives strong demand for ML engineers with experience in real-time systems, risk modeling, and quantitative analysis.</p>''',
        'faqs': [
            ('What is the average AI salary in New York?', 'AI engineers in NYC earn $170K-$300K in base salary. Financial services firms and hedge funds (Two Sigma, Citadel, DE Shaw) pay at the top of this range, often with substantial bonuses.'),
        ],
    },
    'seattle': {
        'intro': '''<p>Seattle is home to Amazon, Microsoft, and a growing ecosystem of AI companies. The city offers Bay Area-competitive salaries at a slightly lower cost of living, making it an attractive option for AI professionals.</p>
<p>Amazon's AI division (including Bedrock, SageMaker, and Alexa) is the largest AI employer in Seattle, followed by Microsoft (Azure AI, Copilot). Smaller companies like Tableau (Salesforce), Zillow, and numerous startups also hire AI engineers.</p>
<p>Seattle has no state income tax, which adds 7-10% to your effective compensation compared to California. Combined with lower housing costs, a $220K salary in Seattle goes further than $260K in San Francisco.</p>''',
        'faqs': [
            ('What AI companies are in Seattle?', 'Major AI employers include Amazon (AWS AI, Alexa), Microsoft (Azure AI, Copilot, Research), and numerous startups. The University of Washington also drives significant AI research activity in the area.'),
        ],
    },
}


def generate_category_page(filtered_df, slug, title, description):
    """Generate a category listing page"""
    if len(filtered_df) < 1:
        return False

    # Calculate stats
    total = len(filtered_df)
    salary_col = 'salary_max' if 'salary_max' in filtered_df.columns else 'max_amount'
    min_col = 'salary_min' if 'salary_min' in filtered_df.columns else 'min_amount'
    salaries = filtered_df[salary_col].dropna()
    avg_salary = int(salaries.mean() / 1000) if len(salaries) > 0 else 0
    min_salaries = filtered_df[min_col].dropna() if min_col in filtered_df.columns else pd.Series([])
    avg_min = int(min_salaries.mean() / 1000) if len(min_salaries) > 0 else 0

    # Get category content
    cat_content = CATEGORY_CONTENT.get(slug, {})
    intro_html = cat_content.get('intro', '')
    faqs = cat_content.get('faqs', [])

    # Build FAQ HTML + schema
    faq_html = ''
    faq_schema = ''
    if faqs:
        faq_items = ''
        faq_entities = []
        for q, a in faqs:
            faq_items += f'''
        <details style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 12px 20px; margin-bottom: 8px;">
            <summary style="cursor: pointer; font-weight: 600; font-size: 1.0625rem; color: var(--text-primary); list-style: none;">{escape_html(q)}</summary>
            <p style="margin-top: 8px; color: var(--text-secondary); line-height: 1.7;">{escape_html(a)}</p>
        </details>'''
            faq_entities.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            })
        faq_html = f'''
            <div style="margin-top: 32px;">
                <h2 style="margin-bottom: 16px; font-size: 1.25rem;">Frequently Asked Questions</h2>
                {faq_items}
            </div>'''
        import json as _json2
        faq_schema_obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities}
        faq_schema = f'<script type="application/ld+json">\n{_json2.dumps(faq_schema_obj, indent=2)}\n</script>'

    # Build salary context
    salary_context = ''
    if avg_salary > 0 and avg_min > 0:
        salary_context = f'''
            <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-top: 24px;">
                <h3 style="margin-bottom: 12px;">Salary Overview</h3>
                <p style="color: var(--text-secondary); line-height: 1.7;">Based on {total} open positions, {escape_html(title.replace(" Jobs", "").replace("AI Jobs in ", ""))} roles pay an average of <strong style="color: var(--gold);">${avg_min}K - ${avg_salary}K</strong>. <a href="/salaries/" style="color: var(--teal-light);">View detailed salary benchmarks →</a></p>
            </div>'''

    # Generate job cards
    job_cards = ""
    for idx, row in filtered_df.head(50).iterrows():
        company = escape_html(str(row.get('company', row.get('company_name', 'Unknown'))))
        job_title = escape_html(str(row.get('title', 'AI Role')))
        location = escape_html(str(row.get('location', ''))) if pd.notna(row.get('location')) else ''
        category = escape_html(str(row.get('job_category', ''))) if pd.notna(row.get('job_category')) else ''
        remote_status = is_remote(row)
        salary = format_salary(row.get('salary_min', row.get('min_amount')), row.get('salary_max', row.get('max_amount')))

        job_slug = f"{make_slug(row.get('company', row.get('company_name', '')))}-{make_slug(row.get('title', ''))}"
        hash_suffix = hashlib.md5(f"{row.get('company', row.get('company_name', ''))}{row.get('title','')}{row.get('location','')}".encode()).hexdigest()[:6]
        job_slug = f"{job_slug}-{hash_suffix}"

        job_cards += f'''
            <a href="/jobs/{job_slug}/" class="job-card">
                <div class="job-card__content">
                    <div class="job-card__company">{company}</div>
                    <div class="job-card__title">{job_title}</div>
                    <div class="job-card__meta">
                        {f'<span class="job-card__tag job-card__tag--salary">{salary}</span>' if salary else ''}
                        {f'<span class="job-card__tag job-card__tag--remote">Remote</span>' if remote_status else ''}
                        {f'<span class="job-card__tag">{location}</span>' if location and not remote_status else ''}
                    </div>
                </div>
            </a>
        '''

    # Build schemas
    breadcrumbs = get_breadcrumb_schema([("Home", "/"), ("AI Jobs", "/jobs/"), (title, f"/jobs/{slug}/")])

    import json as _json
    item_list_items = []
    for idx, row in filtered_df.head(50).iterrows():
        jt = str(row.get('title', 'AI Role'))
        jc = str(row.get('company', row.get('company_name', '')))
        js = f"{make_slug(jc)}-{make_slug(jt)}"
        jh = hashlib.md5(f"{jc}{jt}{row.get('location','')}".encode()).hexdigest()[:6]
        item_list_items.append({
            "@type": "ListItem",
            "position": len(item_list_items) + 1,
            "url": f"{BASE_URL}/jobs/{js}-{jh}/"
        })
    itemlist_schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": title,
        "numberOfItems": total,
        "itemListElement": item_list_items
    }
    itemlist_json = f'<script type="application/ld+json">\n{_json.dumps(itemlist_schema, indent=2)}\n</script>'

    extra_head_content = breadcrumbs + '\n' + itemlist_json + '\n' + faq_schema
    html = f'''{get_html_head(
        f"{title} - {total} Jobs",
        description,
        f"jobs/{slug}/",
        extra_head=extra_head_content
    )}
{get_nav_html('jobs')}

    <div class="page-header">
        <div class="container">
            <div class="breadcrumb"><a href="/">Home</a> → <a href="/jobs/">AI Jobs</a> → {escape_html(title)}</div>
            <h1>{escape_html(title)}</h1>
            <p class="lead">{escape_html(description)}</p>
            <div class="stats-row">
                <div class="stat-box"><div class="stat-number">{total}</div><div class="stat-label">Open Roles</div></div>
                <div class="stat-box"><div class="stat-number">${avg_salary}K</div><div class="stat-label">Avg Salary</div></div>
            </div>
        </div>
    </div>

    <main>
        <div class="container">
            {f'<div style="margin-bottom: 32px; line-height: 1.8; color: var(--text-secondary);">{intro_html}</div>' if intro_html else ''}
            {salary_context}
            <style>.jobs-grid {{ display: flex; flex-direction: column; gap: 12px; }}</style>
            <h2 style="margin: 32px 0 16px; font-size: 1.25rem;">Open Positions</h2>
            <div class="jobs-grid">{job_cards}</div>
            {faq_html}
            {get_cta_box()}
        </div>
    </main>

{get_footer_html()}'''

    page_dir = f'{JOBS_DIR}/{slug}'
    os.makedirs(page_dir, exist_ok=True)
    with open(f'{page_dir}/index.html', 'w') as f:
        f.write(html)
    return True


# Define categories
CATEGORIES = [
    # By Role
    ('job_category', 'Prompt Engineer', 'prompt-engineer', 'Prompt Engineer Jobs',
     'Browse prompt engineer positions at top AI companies. Salary data, requirements, and application links updated weekly from our community of 1,300+ professionals.'),
    ('job_category', 'AI/ML Engineer', 'ai-ml-engineer', 'AI/ML Engineer Jobs',
     'AI and machine learning engineer jobs with salary data and requirements. Browse open roles at companies building production AI systems, updated weekly.'),
    ('job_category', 'LLM Engineer', 'llm-engineer', 'LLM Engineer Jobs',
     'Large language model engineer positions at companies working with GPT-4, Claude, and open-source models. Salary data and requirements included.'),
    ('job_category', 'MLOps Engineer', 'mlops-engineer', 'MLOps Engineer Jobs',
     'MLOps and ML infrastructure engineer roles. Build and maintain production ML pipelines at top AI companies. Salary data and requirements included.'),
    ('job_category', 'Research Engineer', 'research-engineer', 'Research Engineer Jobs',
     'AI research engineer and applied scientist positions at leading AI labs. Work on frontier models with competitive salaries and full job details.'),
    ('job_category', 'AI Agent Developer', 'ai-agent-developer', 'AI Agent Developer Jobs',
     'AI agent and autonomous systems developer roles. Build agentic AI products at top companies. Browse positions with salary data and requirements.'),
    # By Experience
    ('experience_level', 'senior', 'senior', 'Senior AI Jobs',
     'Senior and lead AI/ML positions for experienced professionals. Staff, principal, and director-level roles with salary data at top AI companies.'),
    ('experience_level', 'entry', 'entry-level', 'Entry-Level AI Jobs',
     'Entry-level and junior AI/ML positions for people starting their AI career. Browse roles with salary data, requirements, and application links.'),
    # By Location
    ('metro', 'San Francisco', 'san-francisco', 'AI Jobs in San Francisco',
     'AI and ML jobs in the San Francisco Bay Area. Browse roles at companies like OpenAI, Anthropic, and leading startups with salary data included.'),
    ('metro', 'New York', 'new-york', 'AI Jobs in New York',
     'AI and ML jobs in New York City. Browse prompt engineering, ML engineering, and AI research roles at top companies with salary data included.'),
    ('metro', 'Seattle', 'seattle', 'AI Jobs in Seattle',
     'AI and ML jobs in Seattle. Browse roles at Amazon, Microsoft, and leading AI companies with salary data, requirements, and application links.'),
    ('metro', 'Remote', 'remote', 'Remote AI Jobs',
     'Remote AI and ML engineering positions you can work from anywhere. Browse prompt engineering, ML, and AI research roles with salary data included.'),
]

print("\n Generating category pages...")
for field, value, slug, title, desc in CATEGORIES:
    if field == 'metro' and value == 'Remote':
        filtered = df[df.get('remote_type', df.get('is_remote', '')).astype(str).str.contains('remote', case=False, na=False)]
    elif field in df.columns:
        filtered = df[df[field] == value]
    else:
        filtered = df[df['location'].str.contains(value, case=False, na=False)] if 'location' in df.columns else pd.DataFrame()

    if generate_category_page(filtered, slug, title, desc):
        print(f"   Generated /jobs/{slug}/ ({len(filtered)} jobs)")

print("="*70)
