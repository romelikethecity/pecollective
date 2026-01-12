#!/usr/bin/env python3
"""
Enrich raw AI job data and prepare for page generation.

This script processes raw job scrape data and outputs:
1. data/jobs.json - For the live job board
2. data/ai_jobs_YYYYMMDD.csv - Weekly enriched data for page generators
3. data/market_intelligence.json - Skills/tools analysis for insights page
"""

import pandas as pd
import json
import re
import os
from datetime import datetime, date
import glob
from collections import Counter

# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = "data"

# Skills to extract from job descriptions
SKILL_KEYWORDS = {
    # LLM Frameworks
    "langchain": "LangChain",
    "llamaindex": "LlamaIndex",
    "llama index": "LlamaIndex",
    "semantic kernel": "Semantic Kernel",
    "haystack": "Haystack",
    "autogen": "AutoGen",
    "crewai": "CrewAI",
    "dspy": "DSPy",

    # LLM Providers / Models
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "claude": "Claude",
    "gpt-4": "GPT-4",
    "gpt-3": "GPT-3",
    "gpt4": "GPT-4",
    "llama": "Llama",
    "mistral": "Mistral",
    "gemini": "Gemini",
    "cohere": "Cohere",
    "hugging face": "Hugging Face",
    "huggingface": "Hugging Face",

    # Techniques
    "rag": "RAG",
    "retrieval augmented": "RAG",
    "fine-tuning": "Fine-tuning",
    "fine tuning": "Fine-tuning",
    "prompt engineering": "Prompt Engineering",
    "embeddings": "Embeddings",
    "vector search": "Vector Search",
    "rlhf": "RLHF",
    "chain of thought": "Chain of Thought",
    "multimodal": "Multimodal",
    "agentic": "AI Agents",
    "ai agent": "AI Agents",

    # Vector DBs
    "pinecone": "Pinecone",
    "weaviate": "Weaviate",
    "milvus": "Milvus",
    "qdrant": "Qdrant",
    "chroma": "Chroma",
    "pgvector": "pgvector",
    "faiss": "FAISS",

    # ML Frameworks
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "transformers": "Transformers",
    "jax": "JAX",
    "keras": "Keras",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",

    # Languages
    "python": "Python",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "rust": "Rust",
    "golang": "Go",
    " go ": "Go",

    # Infrastructure
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",
    "kubernetes": "Kubernetes",
    "docker": "Docker",
    "mlflow": "MLflow",
    "wandb": "Weights & Biases",
    "weights & biases": "Weights & Biases",
    "sagemaker": "SageMaker",
    "bedrock": "Bedrock",
    "vertex ai": "Vertex AI",
}

# Categories for grouping skills in insights
SKILL_CATEGORIES = {
    "LangChain": "LLM Frameworks",
    "LlamaIndex": "LLM Frameworks",
    "Semantic Kernel": "LLM Frameworks",
    "Haystack": "LLM Frameworks",
    "AutoGen": "LLM Frameworks",
    "CrewAI": "LLM Frameworks",
    "DSPy": "LLM Frameworks",
    "OpenAI": "LLM Providers",
    "Anthropic": "LLM Providers",
    "Claude": "LLM Providers",
    "GPT-4": "LLM Providers",
    "GPT-3": "LLM Providers",
    "Llama": "LLM Providers",
    "Mistral": "LLM Providers",
    "Gemini": "LLM Providers",
    "Cohere": "LLM Providers",
    "Hugging Face": "LLM Providers",
    "RAG": "Techniques",
    "Fine-tuning": "Techniques",
    "Prompt Engineering": "Techniques",
    "Embeddings": "Techniques",
    "Vector Search": "Techniques",
    "RLHF": "Techniques",
    "Chain of Thought": "Techniques",
    "Multimodal": "Techniques",
    "AI Agents": "Techniques",
    "Pinecone": "Vector Databases",
    "Weaviate": "Vector Databases",
    "Milvus": "Vector Databases",
    "Qdrant": "Vector Databases",
    "Chroma": "Vector Databases",
    "pgvector": "Vector Databases",
    "FAISS": "Vector Databases",
    "PyTorch": "ML Frameworks",
    "TensorFlow": "ML Frameworks",
    "Transformers": "ML Frameworks",
    "JAX": "ML Frameworks",
    "Keras": "ML Frameworks",
    "scikit-learn": "ML Frameworks",
    "Python": "Languages",
    "TypeScript": "Languages",
    "JavaScript": "Languages",
    "Rust": "Languages",
    "Go": "Languages",
    "AWS": "Cloud/Infrastructure",
    "Azure": "Cloud/Infrastructure",
    "GCP": "Cloud/Infrastructure",
    "Kubernetes": "Cloud/Infrastructure",
    "Docker": "Cloud/Infrastructure",
    "MLflow": "Cloud/Infrastructure",
    "Weights & Biases": "Cloud/Infrastructure",
    "SageMaker": "Cloud/Infrastructure",
    "Bedrock": "Cloud/Infrastructure",
    "Vertex AI": "Cloud/Infrastructure",
}

# Job categorization rules (first match wins)
CATEGORY_RULES = [
    ("prompt engineer", "Prompt Engineer"),
    ("ai agent", "AI Agent Developer"),
    ("agent developer", "AI Agent Developer"),
    ("rag engineer", "RAG Engineer"),
    ("llm engineer", "LLM Engineer"),
    ("llm developer", "LLM Engineer"),
    ("mlops", "MLOps Engineer"),
    ("ml ops", "MLOps Engineer"),
    ("ai safety", "AI Safety"),
    ("ai product manager", "AI Product Manager"),
    ("product manager ai", "AI Product Manager"),
    ("product manager ml", "AI Product Manager"),
    ("applied scientist", "Research Engineer"),
    ("research scientist", "Research Engineer"),
    ("research engineer", "Research Engineer"),
    ("nlp engineer", "AI/ML Engineer"),
    ("machine learning engineer", "AI/ML Engineer"),
    ("ml engineer", "AI/ML Engineer"),
    ("ai engineer", "AI/ML Engineer"),
    ("deep learning", "AI/ML Engineer"),
    ("generative ai", "AI/ML Engineer"),
    ("computer vision", "AI/ML Engineer"),
    ("data scientist", "Data Scientist"),
]

# Metro areas for location normalization
METRO_MAPPING = {
    "san francisco": "San Francisco",
    "sf": "San Francisco",
    "bay area": "San Francisco",
    "palo alto": "San Francisco",
    "menlo park": "San Francisco",
    "mountain view": "San Francisco",
    "sunnyvale": "San Francisco",
    "san jose": "San Francisco",
    "new york": "New York",
    "nyc": "New York",
    "manhattan": "New York",
    "brooklyn": "New York",
    "seattle": "Seattle",
    "austin": "Austin",
    "boston": "Boston",
    "los angeles": "Los Angeles",
    "la": "Los Angeles",
    "chicago": "Chicago",
    "denver": "Denver",
    "atlanta": "Atlanta",
    "remote": "Remote",
}


def extract_skills(text):
    """Extract skills from job description"""
    if not text or pd.isna(text):
        return []

    text_lower = str(text).lower()
    found_skills = set()

    for keyword, canonical in SKILL_KEYWORDS.items():
        if keyword in text_lower:
            found_skills.add(canonical)

    return sorted(list(found_skills))


def categorize_job(title):
    """Categorize job based on title"""
    if not title or pd.isna(title):
        return "Other AI Role"

    title_lower = str(title).lower()

    for keyword, category in CATEGORY_RULES:
        if keyword in title_lower:
            return category

    return "Other AI Role"


def determine_remote_type(row):
    """Determine if job is remote, hybrid, or onsite"""
    is_remote = row.get('is_remote', False)
    location = str(row.get('location', '')).lower()

    if is_remote or 'remote' in location:
        return 'remote'
    elif 'hybrid' in location:
        return 'hybrid'
    else:
        return 'onsite'


def determine_experience_level(title, description=''):
    """Determine experience level from title/description"""
    text = f"{title} {description}".lower()

    if any(word in text for word in ['senior', 'sr.', 'sr ', 'lead', 'principal', 'staff', 'head of', 'director']):
        return 'senior'
    elif any(word in text for word in ['junior', 'jr.', 'jr ', 'entry', 'associate', ' i ', ' ii ']):
        return 'entry'
    else:
        return 'mid'


def normalize_metro(location):
    """Normalize location to metro area"""
    if not location or pd.isna(location):
        return None

    location_lower = str(location).lower()

    for pattern, metro in METRO_MAPPING.items():
        if pattern in location_lower:
            return metro

    return None


def process_jobs(df):
    """Process raw job data into enriched format"""
    jobs = []

    for _, row in df.iterrows():
        # Skip if no title
        if pd.isna(row.get('title')):
            continue

        # Extract salary
        salary_min = None
        salary_max = None
        salary_type = 'annual'

        if pd.notna(row.get('min_amount')):
            try:
                salary_min = int(float(row['min_amount']))
            except:
                pass
        if pd.notna(row.get('max_amount')):
            try:
                salary_max = int(float(row['max_amount']))
            except:
                pass
        if pd.notna(row.get('interval')):
            interval = str(row['interval']).lower()
            if 'hour' in interval:
                salary_type = 'hourly'
                # Convert hourly to annual estimate for comparison
                if salary_min and salary_min < 500:
                    salary_min = int(salary_min * 2080)
                if salary_max and salary_max < 500:
                    salary_max = int(salary_max * 2080)

        # Build job object
        description = str(row.get('description', '')) if pd.notna(row.get('description')) else ''
        location = str(row.get('location', '')) if pd.notna(row.get('location')) else ''
        title = str(row.get('title', ''))

        job = {
            'job_id': str(row.get('id', ''))[:12] if pd.notna(row.get('id')) else '',
            'title': title,
            'company': str(row.get('company', '')) if pd.notna(row.get('company')) else 'Unknown',
            'location': location,
            'metro': normalize_metro(location),
            'remote_type': determine_remote_type(row),
            'is_remote': determine_remote_type(row) == 'remote',
            'salary_min': salary_min,
            'salary_max': salary_max,
            'min_amount': salary_min,  # Alias for compatibility
            'max_amount': salary_max,  # Alias for compatibility
            'salary_type': salary_type,
            'experience_level': determine_experience_level(title, description),
            'job_category': categorize_job(title),
            'skills_tags': extract_skills(description),
            'date_posted': str(row.get('date_posted', ''))[:10] if pd.notna(row.get('date_posted')) else None,
            'date_scraped': date.today().isoformat(),
            'source': str(row.get('site', 'indeed')),
            'source_url': str(row.get('job_url', row.get('job_url_direct', ''))) if pd.notna(row.get('job_url', row.get('job_url_direct'))) else '',
            'job_url_direct': str(row.get('job_url', row.get('job_url_direct', ''))) if pd.notna(row.get('job_url', row.get('job_url_direct'))) else '',
            'description': description,
            'description_snippet': description[:500] if description else '',
        }

        jobs.append(job)

    return jobs


def generate_market_intelligence(jobs):
    """Generate market intelligence data from jobs"""
    all_skills = []
    categories_count = Counter()
    experience_count = Counter()
    remote_count = Counter()
    metro_count = Counter()

    # Salary stats
    salaries = []

    for job in jobs:
        # Skills
        all_skills.extend(job.get('skills_tags', []))

        # Category
        categories_count[job.get('job_category', 'Other')] += 1

        # Experience
        experience_count[job.get('experience_level', 'mid')] += 1

        # Remote
        remote_count[job.get('remote_type', 'onsite')] += 1

        # Metro
        if job.get('metro'):
            metro_count[job['metro']] += 1

        # Salary
        if job.get('salary_max'):
            salaries.append(job['salary_max'])

    # Skill counts
    skill_counts = Counter(all_skills)

    # Group by category
    skills_by_category = {}
    for skill, count in skill_counts.items():
        category = SKILL_CATEGORIES.get(skill, 'Other')
        if category not in skills_by_category:
            skills_by_category[category] = {}
        skills_by_category[category][skill] = count

    # Calculate salary stats
    salary_stats = {}
    if salaries:
        salaries.sort()
        salary_stats = {
            'min': min(salaries),
            'max': max(salaries),
            'median': salaries[len(salaries)//2],
            'avg': sum(salaries) // len(salaries),
            'count_with_salary': len(salaries),
        }

    intel = {
        'date': date.today().isoformat(),
        'total_jobs': len(jobs),
        'skills': dict(skill_counts.most_common(50)),
        'skills_by_category': skills_by_category,
        'categories': dict(categories_count.most_common()),
        'experience_levels': dict(experience_count),
        'remote_breakdown': dict(remote_count),
        'top_metros': dict(metro_count.most_common(10)),
        'salary_stats': salary_stats,
    }

    return intel


def main():
    print("="*70)
    print("  PE COLLECTIVE - JOB ENRICHMENT")
    print("="*70)

    # Find raw job files
    raw_files = glob.glob(f"{DATA_DIR}/raw_ai_jobs_*.csv")
    if not raw_files:
        # Try loading from jobs.json if no raw files
        jobs_json = f"{DATA_DIR}/jobs.json"
        if os.path.exists(jobs_json):
            print(f"\n Loading from existing jobs.json")
            with open(jobs_json) as f:
                data = json.load(f)
            jobs = data.get('jobs', [])
            print(f" Jobs loaded: {len(jobs)}")
        else:
            print(" No raw job files or jobs.json found")
            print("   Run the AI jobs scraper first or add jobs.json to data/")
            exit(1)
    else:
        # Load most recent raw file
        latest_file = max(raw_files, key=os.path.getctime)
        print(f"\n Loading: {latest_file}")

        df = pd.read_csv(latest_file)
        print(f" Raw jobs loaded: {len(df)}")

        # Deduplicate
        url_col = 'job_url' if 'job_url' in df.columns else 'job_url_direct'
        df = df.drop_duplicates(subset=[url_col], keep='first')
        print(f" After deduplication: {len(df)}")

        # Process jobs
        jobs = process_jobs(df)
        print(f" Jobs processed: {len(jobs)}")

    # Print category breakdown
    categories = Counter(job['job_category'] for job in jobs)
    print("\n By category:")
    for cat, count in categories.most_common():
        print(f"   {cat}: {count}")

    # Remote breakdown
    remote = Counter(job['remote_type'] for job in jobs)
    print("\n Remote breakdown:")
    for rtype, count in remote.items():
        pct = (count / len(jobs) * 100) if jobs else 0
        print(f"   {rtype}: {count} ({pct:.1f}%)")

    # Salary stats
    salaries = [j['salary_max'] for j in jobs if j.get('salary_max')]
    if salaries:
        avg_sal = sum(salaries) // len(salaries)
        print(f"\n Salary data: {len(salaries)} jobs with salary")
        print(f"   Average max: ${avg_sal:,}")

    # Generate market intelligence
    intel = generate_market_intelligence(jobs)

    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Save jobs.json (for live job board)
    output_json = {
        'last_updated': date.today().isoformat(),
        'total_jobs': len(jobs),
        'jobs': jobs
    }
    with open(f'{DATA_DIR}/jobs.json', 'w') as f:
        json.dump(output_json, f, indent=2)
    print(f"\n Saved: {DATA_DIR}/jobs.json")

    # Save CSV for page generators
    csv_filename = f"{DATA_DIR}/ai_jobs_{date.today().strftime('%Y%m%d')}.csv"
    df_output = pd.DataFrame(jobs)

    # Convert skills_tags list to string for CSV
    df_output['skills_tags'] = df_output['skills_tags'].apply(lambda x: ','.join(x) if isinstance(x, list) else x)

    df_output.to_csv(csv_filename, index=False)
    print(f" Saved: {csv_filename}")

    # Save market intelligence
    with open(f'{DATA_DIR}/market_intelligence.json', 'w') as f:
        json.dump(intel, f, indent=2)
    print(f" Saved: {DATA_DIR}/market_intelligence.json")

    print(f"\n{'='*70}")
    print(" ENRICHMENT COMPLETE!")
    print(f"{'='*70}")
    print(f" Total jobs: {len(jobs)}")
    print(f" Jobs with salary: {len(salaries)}")
    print(f"\n Ready for page generation!")
    print("="*70)


if __name__ == "__main__":
    main()
