#!/usr/bin/env python3
"""
Content enrichment engine for PE Collective stale job pages.

Converts thin "Position Filled" stubs into comprehensive role guide pages
with skills, salary benchmarks, market context, career paths, and FAQ schema.

Pattern: Fractional Pulse content_generator.py adapted for AI/ML engineering roles.
"""

import json
import re


# Role descriptions by role_type
ROLE_DATA = {
    'prompt_engineer': {
        'title': 'Prompt Engineer',
        'full_title': 'Prompt Engineer',
        'description': (
            'A Prompt Engineer designs, tests, and optimizes prompts and prompt chains '
            'for large language models to produce reliable, high-quality outputs. They sit '
            'at the intersection of linguistics, software engineering, and applied AI, '
            'translating business requirements into structured LLM interactions.'
        ),
        'day_in_life': (
            'A typical week includes designing prompt templates for new product features, '
            'running A/B evaluations on prompt variants, building evaluation harnesses to '
            'measure output quality, collaborating with product managers on use case scoping, '
            'documenting prompt libraries, and monitoring production prompt performance for '
            'regressions after model updates.'
        ),
        'skills': [
            'Prompt design and chain-of-thought engineering',
            'LLM evaluation and benchmarking',
            'Python scripting and automation',
            'RAG (Retrieval-Augmented Generation) architecture',
            'Few-shot and zero-shot prompting strategies',
            'Token optimization and cost management',
            'JSON/structured output parsing',
            'Red-teaming and adversarial testing',
        ],
        'compensation': {
            'entry': '$90K - $120K',
            'mid': '$130K - $170K',
            'senior': '$175K - $220K',
            'staff': '$220K - $280K',
        },
        'ideal_company': (
            'AI-native startups shipping LLM-powered products, PE-backed SaaS companies adding '
            'AI features to existing platforms, and enterprise teams building internal copilot tools. '
            'Demand is highest at Series A-C companies where prompt quality directly impacts product UX.'
        ),
        'career_path': (
            'Prompt Engineering is one of the newest roles in tech, with most practitioners coming '
            'from NLP research, technical writing, software engineering, or QA backgrounds. Career '
            'progression typically moves from individual contributor to Lead Prompt Engineer, then '
            'into AI Product Manager or LLM Engineer roles as the discipline matures.'
        ),
        'market_context': (
            'Prompt Engineer demand exploded in 2024-2025 as companies realized that LLM output quality '
            'depends heavily on prompt design. PE-backed portfolio companies are hiring prompt engineers '
            'to add AI features quickly without rebuilding core infrastructure. The role is evolving fast; '
            'pure prompt engineering is merging with LLM engineering as the tooling matures.'
        ),
    },
    'ml_engineer': {
        'title': 'ML Engineer',
        'full_title': 'Machine Learning Engineer',
        'description': (
            'An ML Engineer builds, trains, and deploys machine learning models in production '
            'environments. They bridge the gap between research and engineering, turning prototype '
            'models into scalable, reliable systems that serve predictions at scale.'
        ),
        'day_in_life': (
            'A typical week includes training and evaluating model iterations, building feature '
            'pipelines, debugging model performance issues in production, optimizing inference '
            'latency, reviewing pull requests from teammates, meeting with data scientists on '
            'experiment results, and monitoring model drift dashboards.'
        ),
        'skills': [
            'PyTorch and/or TensorFlow',
            'Model training, fine-tuning, and evaluation',
            'Feature engineering and pipeline design',
            'MLflow, Weights & Biases, or equivalent tracking',
            'Docker and Kubernetes for model serving',
            'SQL and distributed data processing (Spark)',
            'CI/CD for ML (model versioning, A/B testing)',
            'Cloud ML services (SageMaker, Vertex AI, Azure ML)',
        ],
        'compensation': {
            'entry': '$110K - $140K',
            'mid': '$150K - $195K',
            'senior': '$200K - $260K',
            'staff': '$260K - $340K',
        },
        'ideal_company': (
            'Companies with real ML workloads in production: recommendation engines, fraud detection, '
            'forecasting systems, computer vision pipelines, or NLP products. PE-backed companies '
            'often hire ML Engineers when scaling a proven AI product post-acquisition to handle '
            'increased data volume and model complexity.'
        ),
        'career_path': (
            'Most ML Engineers have a CS or math background with 2-5 years of software engineering '
            'before specializing. The path typically runs from ML Engineer to Senior ML Engineer to '
            'Staff ML Engineer or ML Architect. Some move into ML Platform or MLOps leadership roles. '
            'Strong ML Engineers with business instincts often transition into AI Product Management.'
        ),
        'market_context': (
            'ML Engineer remains one of the most in-demand AI roles. PE firms acquiring companies with '
            'ML products need engineers who can maintain and improve existing models while keeping '
            'infrastructure costs under control. The shift toward foundation models has not reduced '
            'demand; it has shifted the work toward fine-tuning, evaluation, and production optimization.'
        ),
    },
    'data_scientist': {
        'title': 'Data Scientist',
        'full_title': 'Data Scientist',
        'description': (
            'A Data Scientist extracts insights from data using statistical analysis, machine learning, '
            'and experimentation to drive business decisions. They combine domain expertise with '
            'technical skills to identify patterns, build predictive models, and communicate findings '
            'to stakeholders.'
        ),
        'day_in_life': (
            'A typical week includes exploratory data analysis on new datasets, building and validating '
            'predictive models, designing A/B experiments, presenting findings to leadership, writing '
            'SQL queries to answer business questions, collaborating with engineering on data pipeline '
            'requirements, and documenting methodology for reproducibility.'
        ),
        'skills': [
            'Python (pandas, scikit-learn, NumPy)',
            'SQL and data warehousing (Snowflake, BigQuery)',
            'Statistical modeling and hypothesis testing',
            'A/B testing and experimentation design',
            'Data visualization (Matplotlib, Plotly, Tableau)',
            'Feature engineering and selection',
            'Jupyter notebooks and reproducible analysis',
            'Causal inference and uplift modeling',
        ],
        'compensation': {
            'entry': '$95K - $125K',
            'mid': '$135K - $175K',
            'senior': '$180K - $230K',
            'staff': '$230K - $300K',
        },
        'ideal_company': (
            'Companies with enough data to make analytics meaningful: SaaS platforms with user behavior '
            'data, fintech companies needing risk models, healthcare companies analyzing outcomes, and '
            'e-commerce platforms optimizing conversion. PE-backed companies often hire data scientists '
            'to quantify value creation opportunities post-acquisition.'
        ),
        'career_path': (
            'Data Scientists typically have advanced degrees in statistics, math, economics, or CS, '
            'though bootcamp and self-taught paths are increasingly common. Career progression goes '
            'from Data Scientist to Senior Data Scientist to Staff/Principal Data Scientist or into '
            'management as a Data Science Manager or Head of Analytics.'
        ),
        'market_context': (
            'Data Science demand has matured from the hype cycle into stable, sustained hiring. '
            'PE-backed companies particularly value data scientists who can quantify operational '
            'improvements and identify revenue opportunities through data. The role is increasingly '
            'expected to include LLM and GenAI skills alongside traditional statistical methods.'
        ),
    },
    'llm_engineer': {
        'title': 'LLM Engineer',
        'full_title': 'Large Language Model Engineer',
        'description': (
            'An LLM Engineer specializes in building applications powered by large language models, '
            'including fine-tuning, RAG systems, agent frameworks, and production LLM infrastructure. '
            'They combine software engineering fundamentals with deep knowledge of how language models '
            'work under the hood.'
        ),
        'day_in_life': (
            'A typical week includes building and optimizing RAG pipelines, fine-tuning models on '
            'domain-specific data, implementing guardrails and content filtering, benchmarking model '
            'performance across providers, debugging hallucination issues, setting up vector databases, '
            'and collaborating with product on new AI feature specifications.'
        ),
        'skills': [
            'LLM APIs (OpenAI, Anthropic, Google, open-source)',
            'RAG architecture and vector databases (Pinecone, Weaviate)',
            'Fine-tuning (LoRA, QLoRA, full fine-tuning)',
            'LangChain, LlamaIndex, or equivalent frameworks',
            'Prompt engineering and output parsing',
            'Model evaluation and red-teaming',
            'Token cost optimization and caching strategies',
            'Agent and tool-use architectures',
        ],
        'compensation': {
            'entry': '$120K - $155K',
            'mid': '$160K - $210K',
            'senior': '$215K - $275K',
            'staff': '$275K - $360K',
        },
        'ideal_company': (
            'AI-first startups building LLM-native products, PE-backed SaaS companies bolting AI '
            'onto existing platforms, and enterprise companies building internal AI tools. The highest '
            'comp packages are at well-funded startups (Series B+) where LLM capabilities are the '
            'core product differentiator.'
        ),
        'career_path': (
            'LLM Engineering emerged as a distinct role in 2023-2024. Most practitioners transitioned '
            'from backend engineering, ML engineering, or NLP research. Career progression is still '
            'being defined, but typically moves from LLM Engineer to Senior LLM Engineer to AI Architect '
            'or Head of AI. The role carries a premium over general software engineering.'
        ),
        'market_context': (
            'LLM Engineer is the fastest-growing AI role by job posting volume. PE firms see LLM '
            'integration as a value creation lever for portfolio companies, driving demand for engineers '
            'who can ship production AI features quickly. Competition for experienced LLM Engineers is '
            'intense, with total comp packages 20-40% above equivalent backend engineering roles.'
        ),
    },
    'mlops_engineer': {
        'title': 'MLOps Engineer',
        'full_title': 'MLOps Engineer',
        'description': (
            'An MLOps Engineer builds and maintains the infrastructure, pipelines, and tooling that '
            'enable machine learning models to run reliably in production. They apply DevOps principles '
            'to the ML lifecycle: training, deployment, monitoring, and retraining.'
        ),
        'day_in_life': (
            'A typical week includes maintaining model training pipelines, setting up automated '
            'retraining schedules, monitoring model performance and data drift, managing GPU cluster '
            'resources, optimizing CI/CD for ML artifacts, debugging failed training jobs, and '
            'collaborating with ML Engineers on deployment requirements.'
        ),
        'skills': [
            'Kubernetes and Docker for ML workloads',
            'ML pipeline orchestration (Kubeflow, Airflow, Prefect)',
            'Model serving (TorchServe, Triton, BentoML)',
            'Infrastructure as code (Terraform, Pulumi)',
            'Monitoring and observability (Prometheus, Grafana)',
            'GPU resource management and cost optimization',
            'Feature stores (Feast, Tecton)',
            'Cloud platforms (AWS, GCP, Azure) for ML',
        ],
        'compensation': {
            'entry': '$105K - $135K',
            'mid': '$145K - $185K',
            'senior': '$190K - $245K',
            'staff': '$245K - $310K',
        },
        'ideal_company': (
            'Companies running ML models in production that need reliability and scale. Common at '
            'companies with multiple models in production, data-intensive industries (fintech, '
            'healthcare, adtech), and PE-backed platforms where ML infrastructure cost optimization '
            'directly impacts margins.'
        ),
        'career_path': (
            'MLOps Engineers typically come from DevOps, site reliability engineering, or platform '
            'engineering backgrounds. The specialization emerged around 2020 as ML teams realized they '
            'needed dedicated infrastructure expertise. Career path leads to Senior MLOps Engineer, '
            'ML Platform Lead, or Head of ML Infrastructure.'
        ),
        'market_context': (
            'MLOps demand grows in lockstep with ML adoption. As PE-backed companies scale ML products, '
            'they discover that model performance in production requires dedicated infrastructure '
            'engineering. The role is particularly valued at companies transitioning from notebook-based '
            'ML to production-grade systems.'
        ),
    },
    'research_engineer': {
        'title': 'Research Engineer',
        'full_title': 'AI Research Engineer',
        'description': (
            'A Research Engineer implements and scales AI research ideas, bridging the gap between '
            'academic research and production systems. They write high-performance code for training '
            'runs, build experiment infrastructure, and help researchers iterate faster on new models '
            'and techniques.'
        ),
        'day_in_life': (
            'A typical week includes implementing research papers, running large-scale training '
            'experiments, optimizing distributed training code, analyzing experiment results with '
            'researchers, building evaluation benchmarks, managing GPU cluster jobs, and contributing '
            'to internal research tooling.'
        ),
        'skills': [
            'PyTorch (advanced: custom modules, distributed training)',
            'CUDA and GPU optimization',
            'Distributed training (DeepSpeed, FSDP, Megatron)',
            'Research paper implementation',
            'Experiment tracking and reproducibility',
            'High-performance Python and C++',
            'Large-scale data processing',
            'Linux systems and cluster management',
        ],
        'compensation': {
            'entry': '$120K - $160K',
            'mid': '$165K - $220K',
            'senior': '$225K - $300K',
            'staff': '$300K - $400K',
        },
        'ideal_company': (
            'AI labs (OpenAI, Anthropic, Google DeepMind, Meta FAIR), well-funded AI startups with '
            'research teams, and large tech companies with dedicated AI research divisions. PE-backed '
            'companies rarely hire Research Engineers directly, but acqui-hires of AI research teams '
            'bring them into portfolio companies.'
        ),
        'career_path': (
            'Research Engineers typically have MS or PhD backgrounds in CS, math, or physics with '
            'strong software engineering skills. Career progression goes from Research Engineer to '
            'Senior Research Engineer to Research Scientist (if pursuing publications) or to Staff '
            'Engineer / AI Architect roles (if staying on the engineering track).'
        ),
        'market_context': (
            'Research Engineer roles are concentrated at well-funded AI companies but carry some of '
            'the highest compensation in the industry. Demand is driven by the computational scale of '
            'modern AI research. PE firms targeting AI acquisitions evaluate research engineering talent '
            'as a key asset during due diligence.'
        ),
    },
    'ai_product_manager': {
        'title': 'AI Product Manager',
        'full_title': 'AI Product Manager',
        'description': (
            'An AI Product Manager owns the product strategy and roadmap for AI-powered features and '
            'products. They translate business goals into AI use cases, define success metrics, manage '
            'the unique constraints of ML-powered features (latency, accuracy, cost), and bridge '
            'communication between technical AI teams and business stakeholders.'
        ),
        'day_in_life': (
            'A typical week includes defining AI feature requirements with engineering, reviewing model '
            'performance metrics, conducting user research on AI-powered features, managing the AI '
            'product roadmap, scoping data requirements with data engineering, presenting AI strategy '
            'to leadership, and evaluating build-vs-buy decisions for AI capabilities.'
        ),
        'skills': [
            'AI/ML product strategy and roadmapping',
            'Model performance metrics and evaluation',
            'Data requirements and pipeline scoping',
            'UX design for AI-powered features',
            'Build vs buy analysis for AI capabilities',
            'Stakeholder communication and alignment',
            'A/B testing and experimentation',
            'AI ethics, fairness, and responsible deployment',
        ],
        'compensation': {
            'entry': '$110K - $145K',
            'mid': '$150K - $195K',
            'senior': '$200K - $260K',
            'staff': '$260K - $330K',
        },
        'ideal_company': (
            'Any company shipping AI-powered products: SaaS platforms with ML features, AI-native '
            'startups, and enterprise companies building AI tools. PE-backed companies adding AI to '
            'existing products need AI PMs who understand both the technology constraints and the '
            'business case for AI investment.'
        ),
        'career_path': (
            'AI Product Managers typically come from technical product management or data science '
            'backgrounds. The role requires enough technical depth to evaluate AI capabilities and '
            'enough product sense to prioritize business impact. Career path leads to Senior AI PM, '
            'Director of AI Product, VP Product (AI), or Chief AI Officer at smaller companies.'
        ),
        'market_context': (
            'AI Product Management is a rapidly growing specialty. PE firms increasingly require '
            'portfolio companies to have dedicated AI product leadership to guide AI investment and '
            'avoid expensive mis-scoped AI projects. The role commands a 15-25% premium over '
            'general product management.'
        ),
    },
    'ai_agent_developer': {
        'title': 'AI Agent Developer',
        'full_title': 'AI Agent Developer',
        'description': (
            'An AI Agent Developer builds autonomous and semi-autonomous AI systems that can plan, '
            'use tools, and execute multi-step tasks. They design agent architectures, implement tool '
            'integrations, build orchestration layers, and ensure agents operate reliably and safely '
            'in production environments.'
        ),
        'day_in_life': (
            'A typical week includes designing agent workflows and state machines, implementing tool '
            'integrations (APIs, databases, code execution), building evaluation harnesses for agent '
            'behavior, debugging agent failure modes, optimizing multi-step reasoning chains, testing '
            'guardrails and safety constraints, and collaborating with product on new automation use cases.'
        ),
        'skills': [
            'Agent frameworks (LangGraph, CrewAI, AutoGen)',
            'Tool-use and function calling patterns',
            'State management and workflow orchestration',
            'LLM APIs and prompt engineering',
            'Error handling and retry strategies for AI systems',
            'Evaluation and testing of non-deterministic systems',
            'API design and integration',
            'Safety guardrails and content filtering',
        ],
        'compensation': {
            'entry': '$115K - $150K',
            'mid': '$155K - $205K',
            'senior': '$210K - $270K',
            'staff': '$270K - $350K',
        },
        'ideal_company': (
            'AI-native startups building agent-powered products (customer support automation, coding '
            'assistants, research tools), PE-backed companies automating internal workflows, and '
            'enterprise companies deploying AI agents for process automation. This is one of the '
            'hottest roles in AI as of 2026.'
        ),
        'career_path': (
            'AI Agent Development is one of the newest specializations, emerging in 2024-2025. '
            'Practitioners come from backend engineering, ML engineering, or LLM engineering backgrounds. '
            'Career progression is still forming but typically moves toward AI Architect, Head of AI '
            'Automation, or founding AI-agent startups.'
        ),
        'market_context': (
            'AI Agent Developer is the fastest-growing AI role in 2026. PE firms view agent-based '
            'automation as a major cost reduction lever for portfolio companies. Companies that can '
            'automate workflows with agents reduce headcount needs and improve margins, making this '
            'role directly tied to PE value creation thesis.'
        ),
    },
    'ai_solutions_architect': {
        'title': 'AI Solutions Architect',
        'full_title': 'AI Solutions Architect',
        'description': (
            'An AI Solutions Architect designs end-to-end AI systems that integrate with existing '
            'enterprise infrastructure. They evaluate AI technologies, design system architectures, '
            'manage technical requirements across teams, and ensure AI solutions meet performance, '
            'cost, and compliance requirements.'
        ),
        'day_in_life': (
            'A typical week includes designing system architecture for AI features, evaluating '
            'vendor AI solutions, writing technical design documents, meeting with engineering teams '
            'on integration requirements, reviewing infrastructure costs, advising leadership on '
            'AI technology strategy, and conducting proof-of-concept evaluations.'
        ),
        'skills': [
            'System design and architecture patterns',
            'Cloud architecture (AWS, GCP, Azure)',
            'AI/ML pipeline design and integration',
            'Cost modeling for AI workloads',
            'Security and compliance for AI systems',
            'Vendor evaluation and selection',
            'Technical documentation and communication',
            'Enterprise integration patterns (APIs, data lakes, ETL)',
        ],
        'compensation': {
            'entry': '$120K - $155K',
            'mid': '$160K - $210K',
            'senior': '$215K - $280K',
            'staff': '$280K - $350K',
        },
        'ideal_company': (
            'Enterprise companies deploying AI at scale, cloud providers with AI solution teams, '
            'AI consulting firms, and PE-backed companies needing to integrate AI into legacy systems. '
            'The role is critical when a company is making significant AI infrastructure investments '
            'and needs someone to own the technical architecture.'
        ),
        'career_path': (
            'AI Solutions Architects typically have 8+ years of software engineering or solutions '
            'architecture experience with recent AI/ML specialization. They often come from backend '
            'engineering, DevOps, or traditional solutions architecture roles. Career path leads to '
            'Principal Architect, VP Engineering (AI), or CTO at AI-focused companies.'
        ),
        'market_context': (
            'Demand for AI Solutions Architects is growing as enterprises move past AI experimentation '
            'into production deployment. PE-backed companies value this role during post-acquisition '
            'technology integration, where AI systems need to be rationalized across merged platforms. '
            'The role commands premiums due to the rare combination of architecture skills and AI depth.'
        ),
    },
    'data_engineer': {
        'title': 'Data Engineer',
        'full_title': 'Data Engineer',
        'description': (
            'A Data Engineer builds and maintains the data infrastructure that powers analytics and '
            'machine learning. They design data pipelines, manage data warehouses, ensure data quality, '
            'and create the foundation that data scientists and ML engineers depend on.'
        ),
        'day_in_life': (
            'A typical week includes building and maintaining ETL/ELT pipelines, debugging data quality '
            'issues, optimizing warehouse query performance, setting up data ingestion from new sources, '
            'collaborating with data scientists on feature pipeline requirements, monitoring pipeline '
            'health dashboards, and managing data governance and access controls.'
        ),
        'skills': [
            'SQL and data modeling (star schema, data vault)',
            'Python for data pipelines',
            'Data orchestration (Airflow, Dagster, Prefect)',
            'Cloud data warehouses (Snowflake, BigQuery, Redshift)',
            'Streaming data (Kafka, Flink, Spark Streaming)',
            'Data quality frameworks (Great Expectations, dbt tests)',
            'Infrastructure as code (Terraform)',
            'dbt (data build tool)',
        ],
        'compensation': {
            'entry': '$100K - $130K',
            'mid': '$140K - $180K',
            'senior': '$185K - $240K',
            'staff': '$240K - $310K',
        },
        'ideal_company': (
            'Any data-driven company: SaaS platforms generating user data, fintech companies with '
            'transaction data, healthcare companies with patient data, and e-commerce companies with '
            'behavioral data. PE-backed companies often hire data engineers early in the value creation '
            'plan to build the data foundation needed for analytics and AI initiatives.'
        ),
        'career_path': (
            'Data Engineers typically come from software engineering or database administration backgrounds. '
            'Career progression runs from Data Engineer to Senior Data Engineer to Staff Data Engineer '
            'or Analytics Engineering Manager. Many move into ML Engineering or Data Architecture roles '
            'as they gain experience with ML workloads.'
        ),
        'market_context': (
            'Data Engineering is the backbone role of the AI/ML ecosystem. Every ML project depends on '
            'clean, reliable data infrastructure. PE-backed companies invest heavily in data engineering '
            'because data quality directly determines whether AI investments succeed or fail. Demand '
            'remains strong and stable across all industries.'
        ),
    },
}

# Default for unknown role types
DEFAULT_ROLE = {
    'title': 'AI/ML Engineer',
    'full_title': 'AI/ML Engineer',
    'description': (
        'AI and ML engineering roles span a wide range of specializations, from building and training '
        'models to deploying them in production, designing data pipelines, and managing AI infrastructure. '
        'These roles require strong software engineering fundamentals combined with specialized knowledge '
        'of machine learning systems.'
    ),
    'day_in_life': (
        'AI/ML engineers typically split their time between building and improving models or AI systems, '
        'collaborating with product and data teams, monitoring production performance, and staying current '
        'with the fast-moving AI landscape. The specific work varies significantly by specialization.'
    ),
    'skills': [
        'Python and software engineering fundamentals',
        'Machine learning frameworks (PyTorch, TensorFlow)',
        'Cloud platforms (AWS, GCP, Azure)',
        'SQL and data processing',
        'LLM APIs and prompt engineering',
        'Docker and containerization',
        'Git and CI/CD workflows',
        'Data analysis and visualization',
    ],
    'compensation': {
        'entry': '$100K - $140K',
        'mid': '$145K - $195K',
        'senior': '$200K - $260K',
        'staff': '$260K - $340K',
    },
    'ideal_company': (
        'Companies building AI-powered products or integrating AI into existing platforms. Demand spans '
        'from early-stage startups to large enterprises, with PE-backed companies increasingly investing '
        'in AI talent as a value creation lever.'
    ),
    'career_path': (
        'AI/ML careers typically start with a strong foundation in software engineering or data science, '
        'followed by specialization into a specific area like MLOps, LLM engineering, or research. '
        'The field rewards both deep specialization and the ability to work across the full ML stack.'
    ),
    'market_context': (
        'AI/ML engineering roles are among the most in-demand and highest-compensated in tech. '
        'PE firms view AI talent as a strategic asset, driving hiring at portfolio companies. '
        'The field continues to evolve rapidly as new model capabilities create new role specializations.'
    ),
}


def detect_role_from_slug(slug):
    """Detect role_type from a job slug.

    Checks for known AI/ML role keywords in the slug and returns the matching
    role_type key, or 'other' if no match is found.
    """
    slug_lower = slug.lower()

    # Order matters: check more specific patterns first to avoid false matches
    role_patterns = [
        ('ai_agent_developer', ['ai-agent', 'agent-developer', 'agent-engineer', 'agentic']),
        ('ai_solutions_architect', ['solutions-architect', 'ai-architect', 'ml-architect']),
        ('ai_product_manager', ['ai-product-manager', 'ml-product-manager', 'ai-pm']),
        ('prompt_engineer', ['prompt-engineer', 'prompt-design']),
        ('llm_engineer', ['llm-engineer', 'llm-developer', 'large-language-model']),
        ('mlops_engineer', ['mlops', 'ml-ops', 'ml-infrastructure', 'ml-platform']),
        ('research_engineer', ['research-engineer', 'research-scientist', 'ai-research']),
        ('ml_engineer', ['ml-engineer', 'machine-learning-engineer', 'machine-learning']),
        ('data_scientist', ['data-scientist', 'data-science']),
        ('data_engineer', ['data-engineer', 'data-engineering', 'analytics-engineer']),
    ]

    for role_type, keywords in role_patterns:
        for kw in keywords:
            if kw in slug_lower:
                return role_type

    # Fallback: check for broad terms
    if 'prompt' in slug_lower and 'engineer' in slug_lower:
        return 'prompt_engineer'
    if 'llm' in slug_lower:
        return 'llm_engineer'
    if 'mlops' in slug_lower:
        return 'mlops_engineer'
    if 'machine-learning' in slug_lower or 'ml' in slug_lower:
        return 'ml_engineer'
    if 'data-scien' in slug_lower:
        return 'data_scientist'
    if 'data-engineer' in slug_lower:
        return 'data_engineer'
    if 'agent' in slug_lower:
        return 'ai_agent_developer'
    if 'research' in slug_lower and 'engineer' in slug_lower:
        return 'research_engineer'

    return 'other'


def get_role_data(role_type):
    """Get role data for a given role_type, falling back to default."""
    return ROLE_DATA.get(role_type, DEFAULT_ROLE)


def generate_enrichment_sections(role_type, title_display, company_display):
    """Generate all enrichment HTML sections for a stale job page.

    Args:
        role_type: Key from ROLE_DATA (e.g. 'ml_engineer', 'llm_engineer')
        title_display: The job title to show (e.g. 'ML Engineer')
        company_display: Company name to show (e.g. 'Acme Corp')

    Returns:
        dict with 'sections_html', 'faq_html', 'faq_schema', 'css'.
    """
    role = get_role_data(role_type)
    comp = role.get('compensation', DEFAULT_ROLE['compensation'])

    sections = []

    # 1. Role guide intro
    intro_paras = []
    if company_display and company_display not in ('This Company', 'Confidential', 'Unknown'):
        intro_paras.append(
            f"This {title_display} position at {company_display} has been filled. "
            f"Here's what you should know about {role['title']} roles in the current market."
        )
    else:
        intro_paras.append(
            f"This {title_display} position has been filled. "
            f"Here's what you should know about {role['title']} roles in the current market."
        )
    intro_paras.append(role['description'])

    sections.append(f'''
    <section class="enrichment-section">
        <h2>About {role['title']} Roles</h2>
        {''.join(f'<p>{p}</p>' for p in intro_paras)}
    </section>''')

    # 2. Day in the life
    sections.append(f'''
    <section class="enrichment-section">
        <h2>What the Work Looks Like</h2>
        <p>{role['day_in_life']}</p>
    </section>''')

    # 3. Salary benchmarks
    sections.append(f'''
    <section class="enrichment-section">
        <h2>{role['title']} Salary Benchmarks</h2>
        <p class="salary-note">Total compensation ranges including base salary, equity, and bonus. Ranges vary by location, company stage, and funding.</p>
        <div class="salary-grid">
            <div class="salary-item">
                <div class="salary-label">Entry Level</div>
                <div class="salary-value">{comp['entry']}</div>
            </div>
            <div class="salary-item">
                <div class="salary-label">Mid Level</div>
                <div class="salary-value">{comp['mid']}</div>
            </div>
            <div class="salary-item">
                <div class="salary-label">Senior</div>
                <div class="salary-value">{comp['senior']}</div>
            </div>
            <div class="salary-item">
                <div class="salary-label">Staff / Principal</div>
                <div class="salary-value">{comp['staff']}</div>
            </div>
        </div>
    </section>''')

    # 4. Skills
    skills = role.get('skills', DEFAULT_ROLE['skills'])
    skills_html = ''.join(f'<span class="skill-tag">{s}</span>' for s in skills)
    sections.append(f'''
    <section class="enrichment-section">
        <h2>Key Technical Skills</h2>
        <div class="skills-grid">{skills_html}</div>
    </section>''')

    # 5. Market context
    sections.append(f'''
    <section class="enrichment-section">
        <h2>Market Demand</h2>
        <p>{role.get('market_context', DEFAULT_ROLE['market_context'])}</p>
    </section>''')

    # 6. Career path
    sections.append(f'''
    <section class="enrichment-section">
        <h2>Career Path</h2>
        <p>{role.get('career_path', DEFAULT_ROLE['career_path'])}</p>
    </section>''')

    # 7. How to evaluate
    role_title_lower = role['title'].lower()
    sections.append(f'''
    <section class="enrichment-section">
        <h2>How to Evaluate a {role['title']}</h2>
        <p>When hiring a {role_title_lower}, prioritize candidates who have shipped production systems
        similar to what your company needs. AI/ML roles require hands-on technical depth that is
        difficult to assess through interviews alone. Ask for architecture walkthroughs of past
        projects and look for evidence of end-to-end ownership.</p>
        <p>Evaluate problem-solving approach over tool familiarity. The AI/ML landscape changes fast
        enough that specific framework experience matters less than the ability to learn new tools
        and adapt to evolving best practices. The best {role_title_lower}s can explain tradeoffs,
        not just implement solutions.</p>
        <p>For PE-backed companies, look for candidates who understand business constraints alongside
        technical excellence. The most valuable AI hires can connect model performance to business
        outcomes and make pragmatic tradeoffs between perfect and shipped.</p>
    </section>''')

    sections_html = '\n'.join(sections)

    # FAQ generation
    faqs = _generate_faqs(role, title_display, comp)
    faq_html = _render_faq_html(faqs)
    faq_schema = _render_faq_schema(faqs)

    return {
        'sections_html': sections_html,
        'faq_html': faq_html,
        'faq_schema': faq_schema,
        'css': ENRICHMENT_CSS,
    }


def _generate_faqs(role, title_display, compensation):
    """Generate FAQ pairs for a stale job page."""
    role_title = role['title']
    faqs = [
        {
            'q': f'What does a {role_title} do?',
            'a': role['description'],
        },
        {
            'q': f'How much does a {role_title} make?',
            'a': (
                f"Typical {role_title} total compensation ranges from {compensation['entry']} at "
                f"entry level to {compensation['staff']} at staff/principal level. Compensation varies "
                f"significantly based on location, company stage, equity component, and whether the "
                f"company is PE-backed, VC-funded, or public."
            ),
        },
        {
            'q': f'What skills does a {role_title} need?',
            'a': (
                f"Key skills for a {role_title} include: "
                + ', '.join(role.get('skills', DEFAULT_ROLE['skills'])[:6])
                + '. The specific skill mix depends on the company\'s tech stack and product requirements.'
            ),
        },
        {
            'q': f'What kind of company hires a {role_title}?',
            'a': role.get('ideal_company', DEFAULT_ROLE['ideal_company']),
        },
        {
            'q': f'What is the career path for a {role_title}?',
            'a': role.get('career_path', DEFAULT_ROLE['career_path']),
        },
    ]
    return faqs


def _render_faq_html(faqs):
    """Render FAQ section HTML."""
    if not faqs:
        return ''

    items = ''
    for faq in faqs:
        q = _escape(faq['q'])
        a = _escape(faq['a'])
        items += f'''
        <div class="faq-item">
            <h3 class="faq-question">{q}</h3>
            <p class="faq-answer">{a}</p>
        </div>'''

    return f'''
    <section class="enrichment-section faq-section">
        <h2>Frequently Asked Questions</h2>
        {items}
    </section>'''


def _render_faq_schema(faqs):
    """Render FAQ JSON-LD schema."""
    if not faqs:
        return ''

    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq['q'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq['a'],
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }

    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def _escape(text):
    """Escape HTML special characters."""
    if not text:
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


# CSS for enrichment sections - uses PE Collective dark teal + gold theme variables
ENRICHMENT_CSS = """
.enrichment-section {
    margin: 32px 0;
    padding: 0;
}
.enrichment-section h2 {
    font-size: 1.35rem;
    color: var(--text-primary, #ffffff);
    margin-bottom: 12px;
    font-weight: 600;
}
.enrichment-section p {
    color: var(--text-secondary, #a8c5cc);
    line-height: 1.7;
    font-size: 0.95rem;
    margin-bottom: 12px;
}
.salary-note {
    color: var(--text-muted, #6a8a94) !important;
    font-size: 0.85rem !important;
    margin-bottom: 16px !important;
}
.salary-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.salary-item {
    background: var(--bg-card, #132f38);
    border: 1px solid var(--border, rgba(255, 255, 255, 0.1));
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.salary-label {
    color: var(--text-muted, #6a8a94);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}
.salary-value {
    color: var(--gold, #e8a87c);
    font-size: 1.05rem;
    font-weight: 600;
}
.skills-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}
.skill-tag {
    background: var(--bg-card, #132f38);
    border: 1px solid var(--border, rgba(255, 255, 255, 0.1));
    color: var(--text-primary, #ffffff);
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 500;
}
.skill-tag:hover {
    border-color: var(--teal-accent, #3d8a9a);
    background: var(--bg-card-hover, #1a3d48);
}
.faq-section {
    margin-top: 40px;
    padding-top: 32px;
    border-top: 1px solid var(--border, rgba(255, 255, 255, 0.1));
}
.faq-item {
    margin-bottom: 24px;
}
.faq-question {
    color: var(--text-primary, #ffffff);
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 8px;
}
.faq-answer {
    color: var(--text-secondary, #a8c5cc);
    line-height: 1.7;
    font-size: 0.95rem;
}
@media (max-width: 768px) {
    .salary-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (max-width: 480px) {
    .salary-grid {
        grid-template-columns: 1fr;
    }
}
"""
