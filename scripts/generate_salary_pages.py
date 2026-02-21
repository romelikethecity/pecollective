#!/usr/bin/env python3
"""
Generate salary benchmark pages for programmatic SEO.
Creates pages like /salaries/ml-engineer/, /salaries/san-francisco/, /salaries/senior/
"""

import pandas as pd
from datetime import datetime
import glob
import os
import json
import sys
import traceback

# Add scripts directory to path using absolute path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from templates import get_html_head, get_nav_html, get_footer_html, get_cta_box, get_breadcrumb_schema, BASE_URL, SITE_NAME
except Exception as e:
    print(f"ERROR importing templates: {e}")
    traceback.print_exc()
    sys.exit(1)

DATA_DIR = 'data'
SITE_DIR = 'site'
SALARIES_DIR = f'{SITE_DIR}/salaries'

# Define salary categories
ROLE_CATEGORIES = [
    ('AI/ML Engineer', 'ai-ml-engineer', 'AI/ML Engineer'),
    ('Prompt Engineer', 'prompt-engineer', 'Prompt Engineer'),
    ('LLM Engineer', 'llm-engineer', 'LLM Engineer'),
    ('MLOps Engineer', 'mlops-engineer', 'MLOps Engineer'),
    ('Research Engineer', 'research-engineer', 'Research Engineer'),
    ('AI Agent Developer', 'ai-agent-developer', 'AI Agent Developer'),
    ('AI Product Manager', 'ai-product-manager', 'AI Product Manager'),
    ('Data Scientist', 'data-scientist', 'Data Scientist'),
]

METRO_CATEGORIES = [
    ('San Francisco', 'san-francisco'),
    ('New York', 'new-york'),
    ('Seattle', 'seattle'),
    ('Austin', 'austin'),
    ('Boston', 'boston'),
    ('Los Angeles', 'los-angeles'),
    ('Remote', 'remote'),
]

EXPERIENCE_CATEGORIES = [
    ('senior', 'senior', 'Senior'),
    ('mid', 'mid-level', 'Mid-Level'),
    ('entry', 'entry-level', 'Entry-Level'),
]


SALARY_CONTENT = {
    'prompt-engineer': {
        'description': 'Prompt engineers design and optimize inputs to LLMs. Demand has surged since 2024, with companies paying premium salaries for engineers who can reliably get production-quality outputs from AI models. The role combines writing skill, Python proficiency, and systematic testing methodology.',
        'skills': ['Python', 'Claude/GPT-4', 'RAG', 'Evaluation', 'A/B Testing'],
        'faqs': [
            ('How much do prompt engineers make?', 'Prompt engineer salaries range from $90K at entry level to $250K+ at senior positions in major AI labs. The median sits around $145K. Remote roles typically pay 85-95% of Bay Area rates.'),
            ('Are prompt engineering salaries increasing?', 'Yes. As companies move from experimenting with AI to shipping production features, demand for prompt engineers has grown faster than supply. Salaries have increased roughly 15-20% year-over-year since 2024.'),
            ('What skills increase prompt engineer pay?', 'Python proficiency, RAG architecture experience, and evaluation framework development command the highest premiums. Engineers who can build end-to-end prompt pipelines (not just write prompts) earn significantly more.'),
        ],
    },
    'san-francisco': {
        'description': 'San Francisco and the Bay Area pay the highest AI salaries in the world. The concentration of AI labs (OpenAI, Anthropic, Google DeepMind) and well-funded startups creates intense competition for talent. Cost of living is high, but AI salaries more than compensate.',
        'skills': [],
        'faqs': [
            ('What is the average AI salary in San Francisco?', 'AI engineers in SF earn $180K-$350K in base salary. Total compensation at major companies (including equity) ranges from $250K to $600K+ depending on level and company.'),
            ('How does SF AI pay compare to other cities?', 'SF AI salaries run 15-25% higher than NYC and Seattle, 40-60% higher than Austin or Denver, and roughly double most non-tech-hub cities. However, California state income tax and housing costs offset some of this advantage.'),
        ],
    },
    'remote': {
        'description': 'Remote AI positions offer competitive salaries without the geographic constraints of traditional roles. Most remote AI jobs pay 85-95% of Bay Area rates, making them financially attractive for engineers outside major tech hubs. Companies like Scale AI, Hugging Face, and numerous startups hire remote-first.',
        'skills': [],
        'faqs': [
            ('Do remote AI jobs pay less than in-office roles?', 'Slightly. Most remote AI positions pay 85-95% of equivalent Bay Area salaries. Some companies (GitLab, Automattic) apply location-based adjustments, while others pay flat rates regardless of location.'),
            ('Which companies hire remote AI engineers?', 'Major remote-friendly AI employers include Scale AI, Hugging Face, Weights & Biases, Jasper, Cohere, and many venture-backed startups. Large tech companies occasionally offer remote AI roles but tend to prefer hybrid arrangements.'),
        ],
    },
    'senior': {
        'description': 'Senior AI roles (5+ years experience) represent a significant salary jump from mid-level positions. At this level, companies expect architectural decision-making, team leadership, and the ability to translate business needs into ML solutions. Total compensation packages at major companies can exceed $400K.',
        'skills': [],
        'faqs': [
            ('What is the salary premium for senior AI roles?', 'Senior AI engineers earn 30-50% more than mid-level. A mid-level engineer earning $175K can expect $230K-$280K at senior, with staff/principal roles reaching $350K-$500K in total compensation.'),
            ('What differentiates senior from mid-level AI pay?', 'Beyond base salary, senior roles come with larger equity grants, higher bonuses, and often sign-on bonuses. The equity component becomes increasingly significant at staff level and above.'),
        ],
    },
    'mid-level': {
        'description': 'Mid-level AI positions (2-5 years experience) form the largest segment of the AI job market. These roles expect independent contribution: designing and shipping ML features without constant oversight. Companies hire heavily at this level as they scale their AI teams.',
        'skills': [],
        'faqs': [
            ('What is the typical mid-level AI engineer salary?', 'Mid-level AI/ML engineers earn $150K-$220K in base salary. Total compensation at major tech companies ranges from $200K-$350K including equity and bonuses.'),
            ('How do I get to mid-level AI?', 'Most companies consider you mid-level after 2-3 years of relevant experience. Key milestones: independently designed and shipped an ML feature, demonstrated ability to evaluate and improve model performance, and experience with production ML infrastructure.'),
        ],
    },
    'ai-ml-engineer': {
        'description': 'AI/ML engineers build the models and systems that power everything from recommendation feeds to fraud detection. It\'s the broadest category in AI hiring, and salaries reflect that range. At the junior end, you\'re training and evaluating models. At the senior end, you\'re designing entire ML architectures and leading teams. Companies like Meta, Google, Netflix, and Stripe pay top dollar for engineers who can ship production ML systems that work at scale.',
        'skills': ['Python', 'PyTorch', 'TensorFlow', 'Distributed Training', 'Feature Engineering', 'Model Serving'],
        'faqs': [
            ('What do AI/ML engineers earn in 2026?', 'Base salaries range from $100K for entry-level roles to $320K+ for staff positions at top companies. The median sits around $195K. Total compensation at FAANG-tier companies often exceeds $350K at the senior level when you factor in equity.'),
            ('What\'s the difference between an ML engineer and a data scientist?', 'ML engineers focus on building and deploying models in production. Data scientists focus on analysis, experimentation, and extracting insights from data. In practice, the lines blur, but ML engineering roles tend to require stronger software engineering skills and pay about 10-15% more on average.'),
            ('Which companies pay the most for AI/ML engineers?', 'Meta, Google, Apple, Netflix, and Stripe consistently offer the highest total compensation packages. Startups like Anthropic, OpenAI, and Scale AI also pay competitively, with significant equity upside.'),
        ],
    },
    'llm-engineer': {
        'description': 'LLM engineers specialize in building applications on top of large language models. This is one of the fastest-growing roles in tech since 2024. Day-to-day work includes RAG system design, fine-tuning, prompt pipeline development, and integrating LLMs into production applications. Companies want engineers who understand both the capabilities and the limitations of models like GPT-4 and Claude, and can build reliable systems around them.',
        'skills': ['Python', 'RAG', 'Fine-tuning', 'LangChain', 'Vector Databases', 'Transformers'],
        'faqs': [
            ('How much do LLM engineers make?', 'LLM engineer salaries range from $90K at entry level to $280K+ for senior roles. The median is around $200K. Companies building core LLM products (Anthropic, OpenAI, Cohere) tend to pay 15-20% above market for this role.'),
            ('Is LLM engineering a long-term career?', 'Yes, though the specifics will evolve. The underlying skills (system design, evaluation methodology, retrieval architecture) transfer across model generations. Engineers who focus on building reliable AI systems rather than chasing specific model APIs will stay in demand.'),
            ('What separates a good LLM engineer from an average one?', 'The best LLM engineers think in systems, not prompts. They build evaluation frameworks before writing prompts, design for failure modes, and understand when RAG, fine-tuning, or prompt engineering is the right approach for a given problem.'),
        ],
    },
    'mlops-engineer': {
        'description': 'MLOps engineers keep ML systems running in production. They build the infrastructure for model training, deployment, monitoring, and retraining. As companies move from ML experiments to production workloads, demand for MLOps has grown steadily. The role sits at the intersection of DevOps, data engineering, and machine learning, and it pays accordingly.',
        'skills': ['Kubernetes', 'Docker', 'AWS/GCP', 'CI/CD', 'Model Monitoring', 'Python'],
        'faqs': [
            ('What is the salary range for MLOps engineers?', 'MLOps engineer salaries range from $85K at entry level to $270K for senior roles at top companies. The median is around $190K. Companies with large-scale ML systems (autonomous vehicles, ad tech, financial services) tend to pay at the higher end.'),
            ('How is MLOps different from regular DevOps?', 'MLOps adds model-specific concerns on top of standard DevOps: data versioning, model performance monitoring, GPU cluster management, feature stores, and A/B testing infrastructure. The tooling is specialized (MLflow, Kubeflow, Weights & Biases), and you need enough ML knowledge to debug model-related issues in production.'),
            ('What background leads to MLOps roles?', 'Most MLOps engineers come from either DevOps/SRE backgrounds (adding ML knowledge) or ML engineering backgrounds (adding infrastructure skills). Both paths work. Strong Kubernetes and Python skills are table stakes.'),
        ],
    },
    'research-engineer': {
        'description': 'Research engineers bridge the gap between academic ML research and production systems. They implement novel architectures, scale up training runs, and turn research papers into working code. Top AI labs (OpenAI, DeepMind, Anthropic, Meta FAIR) hire heavily for this role. The work is technically demanding, often requiring expertise in distributed computing, GPU programming, and deep learning frameworks at a level that goes well beyond typical ML engineering.',
        'skills': ['PyTorch', 'CUDA', 'Distributed Training', 'Transformers', 'C++', 'Research'],
        'faqs': [
            ('What do research engineers earn?', 'Research engineer salaries range from $95K at entry level to $350K+ at senior positions in top labs. Median is around $230K. At companies like OpenAI and Google DeepMind, total compensation can exceed $500K for senior research engineers when equity is included.'),
            ('Do I need a PhD to be a research engineer?', 'Not necessarily, but it helps at top labs. About 60% of research engineers at places like DeepMind and FAIR have PhDs. However, strong open-source contributions, published papers, or demonstrated ability to implement complex research can substitute for formal credentials.'),
            ('How does research engineering differ from ML engineering?', 'Research engineers focus on advancing the state of the art and supporting researchers. ML engineers focus on building production systems with existing techniques. Research engineering involves more experimentation, novel implementations, and pushing model capabilities, while ML engineering emphasizes reliability, scaling, and business impact.'),
        ],
    },
    'ai-agent-developer': {
        'description': 'AI agent development is one of the newest and hottest specializations in AI. Agent developers build autonomous systems that can reason, plan, and execute multi-step tasks using LLMs. The role exploded in 2025 as companies like Anthropic, OpenAI, Cognition, and Microsoft shipped increasingly capable agent products. Salaries reflect the scarcity of engineers who can build reliable, safe agent systems.',
        'skills': ['Python', 'LLMs', 'Tool Use', 'Agent Frameworks', 'Multi-Agent Systems', 'Planning'],
        'faqs': [
            ('How much do AI agent developers earn?', 'AI agent developer salaries range from $100K for entry-level roles to $340K+ at companies like Cognition and OpenAI. The median is around $220K. Because the field is so new, experienced agent developers can command above-market rates.'),
            ('What skills do AI agent developers need?', 'Strong Python fundamentals, deep understanding of LLM capabilities and limitations, experience with tool use and function calling, and systems thinking. The best agent developers also understand safety and reliability concerns, because agents that fail unpredictably are worse than no agent at all.'),
            ('Is AI agent development a stable career path?', 'The specific frameworks will change, but the core challenge of building AI systems that can take actions in the real world isn\'t going away. If anything, demand is accelerating as enterprises move from chatbots to agents that can handle real workflows.'),
        ],
    },
    'ai-product-manager': {
        'description': 'AI product managers sit between engineering teams and business stakeholders, defining what AI features to build and how they should work. The role requires enough technical depth to understand model capabilities without needing to write the code yourself. Companies are hiring AI PMs at every level as they integrate LLMs and ML into their products. The best AI PMs combine product intuition with a realistic understanding of what AI can and can\'t do today.',
        'skills': ['Product Strategy', 'LLMs', 'User Research', 'Roadmapping', 'A/B Testing', 'Data Analysis'],
        'faqs': [
            ('What do AI product managers earn?', 'AI PM salaries range from $105K at the associate level to $280K+ for senior roles at companies like Google and Adobe. The median is around $200K. AI PMs typically earn 10-20% more than general product managers at the same company because of the specialized knowledge required.'),
            ('Do AI product managers need to code?', 'You don\'t need to write production code, but you do need to understand technical concepts well enough to evaluate trade-offs. Knowing Python basics, understanding how LLMs work at a high level, and being able to read evaluation metrics are all important. PMs who can prototype with APIs tend to be more effective.'),
            ('How do I transition from regular PM to AI PM?', 'Start by shipping AI features at your current company, even small ones. Build hands-on experience with LLM APIs. Take an ML fundamentals course. The biggest gap for most transitioning PMs isn\'t technical knowledge but understanding how to set quality bars for non-deterministic AI outputs.'),
        ],
    },
    'data-scientist': {
        'description': 'Data scientists analyze data, build models, and run experiments to drive product and business decisions. While the "data scientist" title has broadened over the years, AI-focused data science roles emphasize ML modeling, causal inference, and experimentation design. Companies like Airbnb, Lyft, DoorDash, and Etsy rely on data scientists to optimize everything from search ranking to pricing to user engagement.',
        'skills': ['Python', 'SQL', 'Machine Learning', 'Experimentation', 'Statistical Modeling', 'A/B Testing'],
        'faqs': [
            ('What is the salary range for data scientists in AI?', 'Data scientist salaries in AI range from $85K at entry level to $275K for senior roles at top tech companies. The median is around $180K. Data scientists at companies where ML directly drives revenue (ad tech, fintech, marketplaces) tend to earn at the higher end.'),
            ('How does data science differ from data analytics?', 'Data scientists build predictive models and run experiments. Data analysts create dashboards and answer business questions with existing data. In practice, most data science roles involve some analytics work, but the core expectation is that you can build and evaluate ML models independently.'),
            ('Is data science still a good career with AI automation?', 'Yes, but the role is evolving. Routine analysis tasks are getting automated by AI tools, which means data scientists who focus on experimentation design, causal reasoning, and complex modeling will stay valuable. The ones at risk are those whose work is primarily SQL queries and dashboard building.'),
        ],
    },
    'new-york': {
        'description': 'New York City is the second-largest AI job market in the US, trailing only the San Francisco Bay Area. The city\'s strength is its diversity of industries hiring for AI: fintech (Bloomberg, Two Sigma, Citadel), media (NYT, Spotify), e-commerce (Etsy, Shopify), and big tech (Meta, Google). AI salaries in NYC run about 10-15% below SF but significantly above most other markets.',
        'skills': [],
        'faqs': [
            ('What is the average AI salary in New York?', 'AI engineers in NYC earn $150K-$310K in base salary depending on role and seniority. Total compensation at hedge funds and top tech companies can exceed $400K. The financial sector tends to pay a premium for ML talent compared to media or retail.'),
            ('How does NYC AI pay compare to San Francisco?', 'NYC AI salaries run about 10-15% below SF on average. However, NYC has more diversity in employer types. Quant funds and fintech firms often match or exceed SF rates, while media and non-tech companies pay closer to the national average.'),
            ('Which NYC neighborhoods have the most AI jobs?', 'Most AI roles are in Midtown (Google, Microsoft), Hudson Yards/Chelsea (Meta, Amazon), and the Flatiron/Union Square area (numerous startups). Finance AI roles cluster in Midtown and the Financial District.'),
        ],
    },
    'seattle': {
        'description': 'Seattle punches above its weight in AI hiring thanks to Amazon, Microsoft, Google, and a strong startup ecosystem. AWS and Azure both have major AI teams in Seattle, making it a hub for cloud ML infrastructure roles. The lack of state income tax makes Seattle\'s effective compensation higher than the headline numbers suggest, especially compared to California.',
        'skills': [],
        'faqs': [
            ('What is the average AI salary in Seattle?', 'AI engineers in Seattle earn $150K-$280K in base salary. Total compensation at Amazon and Microsoft ranges from $200K to $450K+ at senior levels. The no-income-tax advantage adds roughly 5-8% to take-home pay compared to California.'),
            ('Is Seattle a good city for AI careers?', 'Absolutely. Amazon, Microsoft, and Google together employ thousands of AI engineers in the Seattle area. Apple and Meta also have growing Seattle offices. The cost of living is high but below SF, and the absence of state income tax is a real financial benefit.'),
        ],
    },
    'austin': {
        'description': 'Austin\'s AI job market has grown significantly since 2023, fueled by company relocations and remote-friendly policies. The city offers a compelling combination of growing tech presence, lower cost of living than coastal cities, and no state income tax. Companies like Tesla, Indeed, Oracle, and a wave of AI startups are building teams in Austin.',
        'skills': [],
        'faqs': [
            ('What is the average AI salary in Austin?', 'AI engineers in Austin earn $130K-$230K in base salary. Total compensation is lower than SF or NYC, but the cost of living difference more than compensates. A $180K salary in Austin stretches further than $250K in San Francisco.'),
            ('Is Austin growing as an AI hub?', 'Yes. Austin added more AI job postings per capita than any US metro in 2025. The combination of Texas tax advantages, quality of life, and proximity to major companies makes it attractive for both companies and engineers relocating from higher-cost cities.'),
        ],
    },
    'boston': {
        'description': 'Boston\'s AI scene draws from its concentration of world-class universities (MIT, Harvard) and a deep bench of biotech and financial services companies. The city is particularly strong in healthcare AI, robotics, and quantitative finance. Salaries are competitive with NYC for senior roles, though the market is smaller.',
        'skills': [],
        'faqs': [
            ('What is the average AI salary in Boston?', 'AI engineers in Boston earn $140K-$250K in base salary. Healthcare AI and fintech roles pay at the top of this range. Total compensation at companies like Moderna, Capital One, and local quant firms can exceed $350K for senior engineers.'),
            ('What makes Boston unique for AI careers?', 'The university pipeline is Boston\'s biggest asset. MIT and Harvard produce a steady stream of ML talent, and many graduates stay local. Healthcare AI is a particular strength, with companies like Moderna, Flagship Pioneering, and numerous hospital-affiliated research groups hiring ML engineers.'),
        ],
    },
    'los-angeles': {
        'description': 'Los Angeles is an emerging AI market with particular strength in entertainment, gaming, and creative applications. Netflix, Snap, Disney, and a growing number of AI startups are building teams in LA. Salaries trail SF and NYC but the cost of living is lower than either, and the entertainment industry creates unique AI roles you won\'t find anywhere else.',
        'skills': [],
        'faqs': [
            ('What is the average AI salary in Los Angeles?', 'AI engineers in LA earn $140K-$295K in base salary. Entertainment and media AI roles (Netflix, Snap, gaming studios) pay at the higher end. The market is smaller than SF, NYC, or Seattle, but it\'s growing fast.'),
            ('What types of AI jobs are unique to LA?', 'LA has strong demand for ML engineers working on recommendation systems (Netflix, Spotify LA office), computer vision for entertainment (VFX studios, gaming), content moderation and safety (Snap, TikTok), and generative AI for creative tools. These roles are harder to find in other markets.'),
        ],
    },
    'entry-level': {
        'description': 'Entry-level AI roles (0-2 years experience) are the hardest to land but offer the fastest salary growth in tech. Companies hiring at this level want strong fundamentals: Python, linear algebra, probability, and hands-on experience with ML frameworks. A portfolio of projects matters more than credentials. Once you\'re in, expect rapid salary growth as the gap between junior and mid-level AI pay is significant.',
        'skills': [],
        'faqs': [
            ('What is the starting salary for AI engineers?', 'Entry-level AI/ML engineers earn $85K-$140K in base salary depending on company and location. At top tech companies, total compensation for new graduates can reach $180K-$200K including equity and bonuses. Entry-level roles at AI startups tend to pay slightly less in base but offer more equity upside.'),
            ('Do I need a master\'s degree for entry-level AI roles?', 'Not always, but it helps. About 50% of entry-level AI hires have a master\'s or PhD. The other half have bachelor\'s degrees plus strong portfolios (Kaggle competitions, open-source contributions, personal projects). Bootcamp graduates can break in too, especially for prompt engineering and LLM application roles.'),
            ('How fast do entry-level AI salaries grow?', 'Faster than almost any other tech specialization. Most AI engineers see 20-30% salary increases in their first two years as they move from entry to mid-level. The supply-demand imbalance means companies are willing to promote and pay up to retain junior AI talent.'),
        ],
    },
}


def escape_html(text):
    if pd.isna(text):
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def generate_salary_page(filtered_df, slug, title, category_type, salary_col, min_col):
    """Generate a salary page for a specific category"""
    if len(filtered_df) < 3:
        return False

    try:
        avg_min = int(filtered_df[min_col].mean()) if filtered_df[min_col].notna().any() else 0
        avg_max = int(filtered_df[salary_col].mean())
        median = int(filtered_df[salary_col].median())
    except (ValueError, TypeError):
        avg_min = 0
        avg_max = 0
        median = 0

    sample_size = len(filtered_df)

    # Top paying companies
    company_col = 'company' if 'company' in filtered_df.columns else 'company_name'
    if company_col in filtered_df.columns:
        top_companies = filtered_df.nlargest(5, salary_col)[[company_col, salary_col]].to_dict('records')
    else:
        top_companies = []

    companies_html = ""
    for c in top_companies:
        company_name = c.get('company', c.get('company_name', 'Unknown'))
        try:
            sal = int(c[salary_col])
        except (ValueError, TypeError):
            sal = 0
        companies_html += f'''
            <div class="company-row">
                <span class="company-name">{escape_html(str(company_name))}</span>
                <span class="company-salary">${sal:,}</span>
            </div>
        '''

    # Get enrichment content
    sal_content = SALARY_CONTENT.get(slug, {})
    desc_text = sal_content.get('description', '')
    top_skills = sal_content.get('skills', [])
    faqs = sal_content.get('faqs', [])

    # Build description HTML
    desc_html = ''
    if desc_text:
        desc_html = f'''
            <div style="margin-bottom: 32px; line-height: 1.8; color: var(--text-secondary);">
                <p>{escape_html(desc_text)}</p>
            </div>'''

    # Build skills HTML
    skills_html = ''
    if top_skills:
        skill_tags = ''.join(f'<span style="display: inline-block; padding: 6px 14px; background: var(--teal-primary); border-radius: 20px; font-size: 0.875rem; color: var(--gold); margin: 4px;">{s}</span>' for s in top_skills)
        skills_html = f'''
            <div style="margin-bottom: 32px;">
                <h2 style="margin-bottom: 12px; font-size: 1.125rem;">Key Skills That Drive Higher Pay</h2>
                <div style="display: flex; flex-wrap: wrap; gap: 4px;">{skill_tags}</div>
            </div>'''

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
        faq_schema_obj = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities}
        faq_schema = f'<script type="application/ld+json">\n{json.dumps(faq_schema_obj, indent=2)}\n</script>'

    breadcrumbs = get_breadcrumb_schema([("Home", "/"), ("Salaries", "/salaries/"), (title, f"/salaries/{slug}/")])
    extra_head = breadcrumbs + '\n' + faq_schema
    html = f'''{get_html_head(
        f"{title} Salary 2026 - ${avg_max//1000}K Average",
        f"{title} salary benchmarks based on {sample_size} job postings. Average ${avg_min//1000}K-${avg_max//1000}K. Median ${median//1000}K. Updated weekly with real compensation data.",
        f"salaries/{slug}/",
        extra_head=extra_head
    )}
{get_nav_html('salaries')}

    <div class="page-header">
        <div class="container">
            <div class="breadcrumb">
                <a href="/">Home</a> → <a href="/salaries/">Salaries</a> → {escape_html(title)}
            </div>
            <h1>{escape_html(title)} Salary 2026</h1>
            <p class="lead">Salary benchmarks based on {sample_size} job postings with disclosed compensation.</p>

            <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-number">${avg_min//1000}K</div>
                    <div class="stat-label">Avg Min</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">${avg_max//1000}K</div>
                    <div class="stat-label">Avg Max</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">${median//1000}K</div>
                    <div class="stat-label">Median</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{sample_size}</div>
                    <div class="stat-label">Sample Size</div>
                </div>
            </div>
        </div>
    </div>

    <main>
        <div class="container">
            <style>
                .company-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 16px;
                    background: var(--bg-card);
                    border: 1px solid var(--border);
                    border-radius: 8px;
                    margin-bottom: 8px;
                }}
                .company-name {{ color: var(--text-primary); font-weight: 500; }}
                .company-salary {{ color: var(--gold); font-weight: 600; }}
            </style>

            {desc_html}
            {skills_html}

            {'<div class="section"><h2 style="margin-bottom: 20px;">Top Paying Companies</h2>' + companies_html + '</div>' if companies_html else ''}

            <div class="section" style="text-align: center; padding: 24px 0;">
                <a href="/salaries/" style="color: var(--teal-light); font-weight: 600; text-decoration: none;">&larr; Browse All Salary Data</a>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                <a href="/jobs/" style="color: var(--teal-light); font-weight: 600; text-decoration: none;">View AI Job Listings &rarr;</a>
            </div>

            {faq_html}

            <div class="section" style="background: var(--bg-card); border-radius: 12px; padding: 24px; border: 1px solid var(--border); margin-top: 32px;">
                <h3>Methodology</h3>
                <p style="color: var(--text-secondary); margin-top: 12px;">
                    Salary data is collected from job postings on Indeed and company career pages.
                    Only jobs with disclosed compensation are included. Data is updated weekly.
                </p>
            </div>

            {get_cta_box()}
        </div>
    </main>

{get_footer_html()}'''

    page_dir = f'{SALARIES_DIR}/{slug}'
    os.makedirs(page_dir, exist_ok=True)
    with open(f'{page_dir}/index.html', 'w') as f:
        f.write(html)
    return True


def main():
    print("="*70)
    print("  PE COLLECTIVE - GENERATING SALARY PAGES")
    print("="*70)

    os.makedirs(SALARIES_DIR, exist_ok=True)

    # Load job data
    files = glob.glob(f"{DATA_DIR}/ai_jobs_*.csv")
    print(f"  Looking for CSV files in {DATA_DIR}/")
    print(f"  Found: {files}")

    if files:
        df = pd.read_csv(max(files, key=os.path.getmtime))
    elif os.path.exists(f"{DATA_DIR}/jobs.json"):
        with open(f"{DATA_DIR}/jobs.json") as f:
            df = pd.DataFrame(json.load(f).get('jobs', []))
    else:
        print(" No job data found")
        sys.exit(1)

    print(f"\n Loaded {len(df)} jobs")
    print(f"  Columns: {list(df.columns)}")

    # Filter to jobs with salary
    salary_col = 'salary_max' if 'salary_max' in df.columns else 'max_amount'
    min_col = 'salary_min' if 'salary_min' in df.columns else 'min_amount'

    if salary_col not in df.columns:
        print(f" ERROR: No salary column found ({salary_col})")
        sys.exit(1)

    df_salary = df[df[salary_col].notna() & (df[salary_col] > 0)].copy()
    print(f" Jobs with salary: {len(df_salary)}")

    # Track which pages were actually generated
    generated_roles = []
    generated_metros = []
    generated_experience = []

    # Generate role-based salary pages
    print("\n Generating role-based salary pages...")
    for category, slug, display in ROLE_CATEGORIES:
        filtered = df_salary[df_salary['job_category'] == category] if 'job_category' in df_salary.columns else pd.DataFrame()
        if generate_salary_page(filtered, slug, display, 'role', salary_col, min_col):
            generated_roles.append((category, slug, display))
            print(f"   Generated /salaries/{slug}/ ({len(filtered)} jobs)")

    # Generate metro-based salary pages
    print("\n Generating metro-based salary pages...")
    for metro, slug in METRO_CATEGORIES:
        if metro == 'Remote':
            if 'remote_type' in df_salary.columns:
                filtered = df_salary[df_salary['remote_type'].astype(str).str.contains('remote', case=False, na=False)]
            else:
                filtered = pd.DataFrame()
        else:
            if 'metro' in df_salary.columns:
                filtered = df_salary[df_salary['metro'] == metro]
            elif 'location' in df_salary.columns:
                filtered = df_salary[df_salary['location'].str.contains(metro, case=False, na=False)]
            else:
                filtered = pd.DataFrame()
        if generate_salary_page(filtered, slug, metro, 'metro', salary_col, min_col):
            generated_metros.append((metro, slug))
            print(f"   Generated /salaries/{slug}/ ({len(filtered)} jobs)")

    # Generate experience-based salary pages
    print("\n Generating experience-based salary pages...")
    for level, slug, display in EXPERIENCE_CATEGORIES:
        filtered = df_salary[df_salary['experience_level'] == level] if 'experience_level' in df_salary.columns else pd.DataFrame()
        if generate_salary_page(filtered, slug, display, 'experience', salary_col, min_col):
            generated_experience.append((level, slug, display))
            print(f"   Generated /salaries/{slug}/ ({len(filtered)} jobs)")

    # Generate index page
    overall_avg = int(df_salary[salary_col].mean()) if len(df_salary) > 0 else 0
    salary_index_breadcrumbs = get_breadcrumb_schema([("Home", "/"), ("Salaries", "/salaries/")])

    # Build category sections (only link to pages that were actually generated)
    role_cards = ''.join([f'<a href="/salaries/{slug}/" class="category-card"><h3>{display}</h3><p>View salary data</p></a>' for _, slug, display in generated_roles])
    role_section = f'<h2 style="margin-bottom: 20px;">By Role</h2><div class="category-grid">{role_cards}</div>' if generated_roles else ''

    metro_cards = ''.join([f'<a href="/salaries/{slug}/" class="category-card"><h3>{metro}</h3><p>View salary data</p></a>' for metro, slug in generated_metros])
    metro_section = f'<h2 style="margin-bottom: 20px;">By Location</h2><div class="category-grid">{metro_cards}</div>' if generated_metros else ''

    exp_cards = ''.join([f'<a href="/salaries/{slug}/" class="category-card"><h3>{display}</h3><p>View salary data</p></a>' for _, slug, display in generated_experience])
    exp_section = f'<h2 style="margin-bottom: 20px;">By Experience</h2><div class="category-grid">{exp_cards}</div>' if generated_experience else ''

    index_html = f'''{get_html_head(
        "AI & ML Engineer Salary Benchmarks 2026",
        f"Comprehensive salary data for AI engineers, ML engineers, and prompt engineers. Average ${overall_avg//1000}K based on {len(df_salary)} job postings with disclosed compensation. Updated weekly.",
        "salaries/",
        extra_head=salary_index_breadcrumbs
    )}
{get_nav_html('salaries')}

    <div class="page-header">
        <div class="container">
            <h1>AI Salary Benchmarks 2026</h1>
            <p class="lead">Real salary data from {len(df_salary)} AI and ML job postings. Updated weekly.</p>
        </div>
    </div>

    <main>
        <div class="container">
            <div style="margin-bottom: 32px; line-height: 1.8; color: var(--text-secondary);">
                <p>AI engineering is one of the highest-paying specializations in tech. Prompt engineers, ML engineers, and AI researchers routinely earn $150K-$350K depending on experience, location, and specialization. Our salary data comes directly from job postings with disclosed compensation, so you're seeing what companies actually offer, not self-reported estimates.</p>
                <p style="margin-top: 12px;">Browse by role type, location, or experience level to find benchmarks relevant to your situation. Each page includes top-paying companies, salary ranges, and answers to common compensation questions.</p>
            </div>
            <style>
                .category-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin-bottom: 40px; }}
                .category-card {{
                    display: block;
                    background: var(--bg-card);
                    border: 1px solid var(--border);
                    border-radius: 12px;
                    padding: 24px;
                    text-decoration: none;
                    transition: all 0.2s;
                }}
                .category-card:hover {{ border-color: var(--teal-light); transform: translateY(-2px); }}
                .category-card h3 {{ color: var(--text-primary); margin-bottom: 8px; }}
                .category-card p {{ color: var(--text-secondary); font-size: 0.9rem; }}
            </style>

            {role_section}

            {metro_section}

            {exp_section}

            {get_cta_box()}
        </div>
    </main>

{get_footer_html()}'''

    with open(f'{SALARIES_DIR}/index.html', 'w') as f:
        f.write(index_html)

    print(f"\n Generated salary index page")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
