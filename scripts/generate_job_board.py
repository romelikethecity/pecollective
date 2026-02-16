#!/usr/bin/env python3
"""
Generate the main job board listing page at /jobs/index.html
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

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from templates import (
        get_html_head, get_nav_html, get_footer_html, get_cta_box, get_breadcrumb_schema,
        slugify, format_salary, is_remote, BASE_URL, SITE_NAME
    )
except Exception as e:
    print(f"ERROR importing templates: {e}")
    traceback.print_exc()
    sys.exit(1)

DATA_DIR = 'data'
SITE_DIR = 'site'
JOBS_DIR = f'{SITE_DIR}/jobs'


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


def main():
    print("="*70)
    print("  PE COLLECTIVE - GENERATING JOB BOARD")
    print("="*70)

    os.makedirs(JOBS_DIR, exist_ok=True)

    # Load job data
    files = glob.glob(f"{DATA_DIR}/ai_jobs_*.csv")
    print(f"  Looking for CSV files in {DATA_DIR}/")
    print(f"  Found: {files}")

    if files:
        latest_file = max(files, key=os.path.getmtime)
        print(f"  Loading: {latest_file}")
        df = pd.read_csv(latest_file)
        print(f"\n Loaded {len(df)} jobs from {latest_file}")
        print(f"  Columns: {list(df.columns)}")
    elif os.path.exists(f"{DATA_DIR}/jobs.json"):
        with open(f"{DATA_DIR}/jobs.json") as f:
            data = json.load(f)
        df = pd.DataFrame(data.get('jobs', []))
        print(f"\n Loaded {len(df)} jobs from jobs.json")
    else:
        print(f" No job data found in {DATA_DIR}/")
        print(f"  Current directory: {os.getcwd()}")
        print(f"  Directory contents: {os.listdir('.')}")
        if os.path.exists(DATA_DIR):
            print(f"  Data dir contents: {os.listdir(DATA_DIR)}")
        sys.exit(1)

    # Calculate stats
    total_jobs = len(df)

    # Count remote jobs safely
    remote_jobs = 0
    if 'remote_type' in df.columns:
        remote_jobs = len(df[df['remote_type'].astype(str).str.contains('remote', case=False, na=False)])

    # Salary stats
    salary_col = 'salary_max' if 'salary_max' in df.columns else 'max_amount'
    salaries = df[salary_col].dropna() if salary_col in df.columns else pd.Series([])
    salaries = salaries[salaries > 0]
    avg_salary = int(salaries.mean() / 1000) if len(salaries) > 0 else 0

    # Category counts
    categories = df['job_category'].value_counts().head(6).to_dict() if 'job_category' in df.columns else {}

    # Generate job cards HTML
    job_cards_html = ""
    for idx, row in df.head(100).iterrows():
        company = escape_html(str(row.get('company', row.get('company_name', 'Unknown'))))
        title = escape_html(str(row.get('title', 'AI Role')))
        location = escape_html(str(row.get('location', ''))) if pd.notna(row.get('location')) else ''
        category = escape_html(str(row.get('job_category', ''))) if pd.notna(row.get('job_category')) else ''
        remote_status = is_remote(row)

        salary = format_salary(row.get('salary_min', row.get('min_amount')), row.get('salary_max', row.get('max_amount')))

        # Generate slug
        job_slug = f"{make_slug(row.get('company', row.get('company_name', '')))}-{make_slug(row.get('title', ''))}"
        hash_suffix = hashlib.md5(f"{row.get('company', row.get('company_name', ''))}{row.get('title','')}{row.get('location','')}".encode()).hexdigest()[:6]
        job_slug = f"{job_slug}-{hash_suffix}"

        job_cards_html += f'''
            <a href="/jobs/{job_slug}/" class="job-card">
                <div class="job-card__content">
                    <div class="job-card__company">{company}</div>
                    <div class="job-card__title">{title}</div>
                    <div class="job-card__meta">
                        {f'<span class="job-card__tag job-card__tag--salary">{salary}</span>' if salary else ''}
                        {f'<span class="job-card__tag job-card__tag--remote">Remote</span>' if remote_status else ''}
                        {f'<span class="job-card__tag">{location}</span>' if location and not remote_status else ''}
                        {f'<span class="job-card__tag">{category}</span>' if category else ''}
                    </div>
                </div>
            </a>
        '''

    # Category filter buttons
    category_filters = ""
    for cat, count in categories.items():
        cat_slug = make_slug(cat)
        category_filters += f'<a href="/jobs/{cat_slug}/" class="filter-btn">{escape_html(cat)} ({count})</a>\n'

    # Build ItemList schema for job listings
    import json as _json
    item_list_items = []
    for idx, row in df.head(50).iterrows():
        job_title = str(row.get('title', 'AI Role'))
        job_company = str(row.get('company', row.get('company_name', '')))
        job_slug_il = f"{make_slug(job_company)}-{make_slug(job_title)}"
        hash_il = hashlib.md5(f"{job_company}{job_title}{row.get('location','')}".encode()).hexdigest()[:6]
        job_slug_il = f"{job_slug_il}-{hash_il}"
        item_list_items.append({
            "@type": "ListItem",
            "position": len(item_list_items) + 1,
            "url": f"{BASE_URL}/jobs/{job_slug_il}/"
        })
    itemlist_schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "AI & ML Engineer Jobs",
        "numberOfItems": total_jobs,
        "itemListElement": item_list_items
    }
    itemlist_json = f'<script type="application/ld+json">\n{_json.dumps(itemlist_schema, indent=2)}\n</script>'

    # Page HTML
    job_board_breadcrumbs = get_breadcrumb_schema([("Home", "/"), ("AI Jobs", "/jobs/")])
    extra_head_content = job_board_breadcrumbs + '\n' + itemlist_json
    html = f'''{get_html_head(
        f"{total_jobs} AI & ML Engineer Jobs - ${avg_salary}K avg",
        f"Browse {total_jobs} AI engineer, ML engineer, and prompt engineer jobs. Average salary ${avg_salary}K. {remote_jobs} remote positions available. Updated weekly.",
        "jobs/",
        extra_head=extra_head_content
    )}
{get_nav_html('jobs')}

    <div class="page-header">
        <div class="container">
            <div class="page-label">AI Job Board</div>
            <h1>{total_jobs} AI & ML Jobs</h1>
            <p class="lead">Prompt Engineer, AI Engineer, ML Engineer, and more. Real salaries, no recruiter spin. Updated weekly.</p>

            <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-number">{total_jobs}</div>
                    <div class="stat-label">Open Roles</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">${avg_salary}K</div>
                    <div class="stat-label">Avg Salary</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{remote_jobs}</div>
                    <div class="stat-label">Remote</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{len(categories)}</div>
                    <div class="stat-label">Categories</div>
                </div>
            </div>
        </div>
    </div>

    <main>
        <div class="container">
            <div class="filters-section" style="margin-bottom: 32px;">
                <h3 style="margin-bottom: 16px; color: var(--text-secondary); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em;">Filter by Category</h3>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                    {category_filters}
                    <a href="/jobs/remote/" class="filter-btn">Remote ({remote_jobs})</a>
                </div>
            </div>

            <style>
                .filter-btn {{
                    display: inline-block;
                    padding: 8px 16px;
                    background: var(--bg-card);
                    border: 1px solid var(--border);
                    border-radius: 20px;
                    color: var(--text-secondary);
                    text-decoration: none;
                    font-size: 0.875rem;
                    transition: all 0.15s;
                }}
                .filter-btn:hover {{
                    border-color: var(--teal-light);
                    color: var(--text-primary);
                }}
                .jobs-grid {{
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                }}
            </style>

            <div class="jobs-grid">
                {job_cards_html}
            </div>

            {get_cta_box()}
        </div>
    </main>

{get_footer_html()}'''

    # Save
    with open(f'{JOBS_DIR}/index.html', 'w') as f:
        f.write(html)

    print(f"\n Generated job board with {total_jobs} jobs")
    print(f" Saved to {JOBS_DIR}/index.html")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
