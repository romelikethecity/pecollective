#!/usr/bin/env python3
"""Append new comparison pages to data/comparisons.json."""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'comparisons.json')

NEW_COMPARISONS = [
    {
        "slug": "pinecone-vs-weaviate",
        "tool_a": {
            "name": "Pinecone",
            "icon": "🌲",
            "url": "https://www.pinecone.io",
            "cta_text": "Try Pinecone Free",
            "price_free": "Starter (free tier)",
            "price_individual": "Serverless: usage-based",
            "price_business": "Standard: from $50/mo",
            "price_enterprise": "Enterprise: from $500/mo"
        },
        "tool_b": {
            "name": "Weaviate",
            "icon": "🔷",
            "url": "https://weaviate.io",
            "cta_text": "Try Weaviate Free",
            "price_free": "Free sandbox cluster",
            "price_individual": "Self-hosted (open source)",
            "price_business": "Cloud: ~$0.095/1M dims",
            "price_enterprise": "Custom pricing"
        },
        "title": "Pinecone vs Weaviate: Which Vector Database Should You Choose?",
        "h1": "Which Vector Database Should You Use?",
        "meta_description": "Pinecone vs Weaviate: Compare pricing, performance, and features of the two leading vector databases for RAG and AI applications in 2026.",
        "og_description": "Pinecone or Weaviate? We compare the two most popular vector databases for building RAG systems and AI search.",
        "subtitle": "A practical comparison for building RAG systems and AI search applications",
        "verdict_a": "You want a fully managed, serverless vector database with zero infrastructure overhead. Pinecone handles scaling, indexing, and operations so you can focus on your application logic.",
        "verdict_b": "You want an open-source vector database with hybrid search capabilities, self-hosting options, and transparent pricing. Weaviate gives you full control over your data and deployment.",
        "features": [
            {"feature": "Deployment Model", "a": "Fully managed (serverless)", "b": "Cloud managed or self-hosted", "winner": "tie"},
            {"feature": "Open Source", "a": "No (proprietary)", "b": "Yes (BSD-3)", "winner": "b", "b_check": True},
            {"feature": "Hybrid Search", "a": "Vector only", "b": "Vector + keyword combined", "winner": "b", "b_check": True},
            {"feature": "Setup Complexity", "a": "Minutes (API key only)", "b": "Minutes (cloud) or hours (self-hosted)", "winner": "a"},
            {"feature": "Scaling", "a": "Automatic (serverless)", "b": "Manual or managed", "winner": "a"},
            {"feature": "Filtering", "a": "Metadata filtering", "b": "Advanced filtering + GraphQL", "winner": "b"},
            {"feature": "Data Privacy", "a": "Cloud only", "b": "Self-host option", "winner": "b"},
            {"feature": "Multi-tenancy", "a": "Namespace-based", "b": "Native multi-tenancy", "winner": "b", "b_check": True},
            {"feature": "Free Tier", "a": "~1M vectors", "b": "Sandbox cluster", "winner": "tie"}
        ],
        "deep_dive": [
            {
                "heading": "Pinecone Wins: Simplicity and Scale",
                "icon": "🌲",
                "paragraphs": [
                    "Pinecone's serverless model is its strongest selling point. You create an index, send vectors, and query them. No clusters to manage, no nodes to scale, no YAML configs to debug at 2 AM. For teams that want to build RAG applications without becoming database administrators, Pinecone removes the entire infrastructure layer.",
                    "Scaling is automatic and invisible. Whether you're storing 10,000 vectors or 10 million, Pinecone handles the infrastructure. You pay for what you use (read units, write units, storage) and never think about capacity planning.",
                    "The developer experience is also more polished. Pinecone's SDKs, documentation, and quickstart guides are consistently praised. If you've never worked with vector databases before, Pinecone has the shortest path from zero to working RAG system."
                ]
            },
            {
                "heading": "Weaviate Wins: Flexibility and Hybrid Search",
                "icon": "🔷",
                "paragraphs": [
                    "Weaviate's hybrid search is a genuine differentiator. Instead of choosing between keyword search and vector search, Weaviate combines both in a single query. This matters because pure vector search sometimes misses exact matches (product SKUs, error codes, proper nouns) that keyword search catches instantly.",
                    "Being open source gives you options that Pinecone can't match. You can self-host on your own infrastructure for data sovereignty, run it locally during development, inspect the source code, and avoid vendor lock-in entirely. For regulated industries (healthcare, finance, government), the self-hosting option is often a hard requirement.",
                    "Native multi-tenancy is another Weaviate advantage. If you're building a SaaS product where each customer needs isolated data, Weaviate handles this at the database level rather than requiring application-level workarounds. At scale, this simplifies architecture significantly."
                ]
            }
        ],
        "use_cases_a": [
            "Teams that want zero infrastructure management",
            "Rapid prototyping of RAG applications",
            "Serverless architectures",
            "Startups that need to move fast",
            "Applications where vector search alone is sufficient",
            "Projects prioritizing developer experience"
        ],
        "use_cases_b": [
            "Applications requiring hybrid (vector + keyword) search",
            "Regulated industries needing self-hosted deployment",
            "Multi-tenant SaaS platforms",
            "Teams that want open-source flexibility",
            "Cost-sensitive deployments at scale",
            "Projects requiring advanced filtering and GraphQL"
        ],
        "recommendation_sections": [
            {
                "audience": "For AI Engineers Building RAG",
                "text": "Start with Pinecone if you want the fastest path to a working system. The serverless model means you can have a RAG pipeline running in an afternoon. Switch to Weaviate if you need hybrid search, self-hosting, or hit Pinecone's pricing limits at scale."
            },
            {
                "audience": "For Enterprise Teams",
                "text": "Weaviate's self-hosting option and open-source license make compliance conversations easier. If your security team has concerns about sending data to a third-party managed service, Weaviate on your own infrastructure removes that objection entirely."
            },
            {
                "audience": "The Bottom Line",
                "text": "Pinecone for speed and simplicity. Weaviate for flexibility and control. Both are production-ready and power thousands of AI applications. If hybrid search matters to your use case, Weaviate wins. If you want the simplest possible setup, Pinecone wins."
            }
        ],
        "faqs": [
            {
                "question": "Is Pinecone better than Weaviate?",
                "answer": "It depends on your priorities. Pinecone is simpler to set up and manage with its fully serverless model. Weaviate offers more flexibility with hybrid search, self-hosting, and open-source access. For pure vector search with minimal ops, choose Pinecone. For hybrid search or self-hosted needs, choose Weaviate."
            },
            {
                "question": "Can I migrate from Pinecone to Weaviate or vice versa?",
                "answer": "Yes, but it requires re-indexing your vectors. Export your vectors and metadata from one system and import into the other. The embeddings themselves are model-dependent, not database-dependent, so they transfer directly. Plan for a few hours of migration work for most datasets."
            },
            {
                "question": "Which vector database is cheaper?",
                "answer": "At small scale, both have free tiers. At medium scale, Weaviate's self-hosted option is cheapest (just your compute costs). At large scale, Pinecone's serverless pricing can add up with high query volumes. Run cost estimates with your expected traffic before committing."
            },
            {
                "question": "Do I need a vector database for RAG?",
                "answer": "For production RAG systems, yes. While you can prototype with in-memory vectors or SQLite extensions, a purpose-built vector database handles indexing, scaling, filtering, and concurrent queries. Both Pinecone and Weaviate are designed for exactly this use case."
            }
        ]
    },
    {
        "slug": "claude-vs-chatgpt-coding",
        "tool_a": {
            "name": "Claude",
            "icon": "🟠",
            "url": "https://claude.ai",
            "cta_text": "Try Claude Free",
            "price_free": "Free tier available",
            "price_individual": "Pro: $20/month",
            "price_business": "Team: $25/user/month",
            "price_enterprise": "Custom pricing"
        },
        "tool_b": {
            "name": "ChatGPT",
            "icon": "🟢",
            "url": "https://chat.openai.com",
            "cta_text": "Try ChatGPT Free",
            "price_free": "Free tier (GPT-4o mini)",
            "price_individual": "Plus: $20/month",
            "price_business": "Team: $25/user/month",
            "price_enterprise": "Custom pricing"
        },
        "title": "Claude vs ChatGPT for Coding: Which AI Is Better for Developers?",
        "h1": "Which AI Assistant Is Better for Coding?",
        "meta_description": "Claude vs ChatGPT for coding: Compare Anthropic's Claude and OpenAI's ChatGPT on code generation, debugging, refactoring, and real-world development tasks in 2026.",
        "og_description": "Claude or ChatGPT for coding? We compare both AI assistants on code generation, debugging, and developer workflows.",
        "subtitle": "A developer-focused comparison of the two leading AI assistants for code",
        "verdict_a": "You want an AI that excels at understanding large codebases, following complex instructions precisely, and producing clean, well-structured code. Claude's extended context window and instruction-following are best-in-class for serious development work.",
        "verdict_b": "You want the broadest AI ecosystem with plugins, custom GPTs, web browsing, DALL-E integration, and a massive community of shared prompts and workflows. ChatGPT's versatility extends beyond coding into a general-purpose productivity tool.",
        "features": [
            {"feature": "Code Generation Quality", "a": "Excellent (top SWE-bench)", "b": "Excellent (GPT-4o)", "winner": "a"},
            {"feature": "Context Window", "a": "200K tokens", "b": "128K tokens", "winner": "a", "a_check": True},
            {"feature": "Instruction Following", "a": "Very precise", "b": "Good, sometimes verbose", "winner": "a"},
            {"feature": "Debugging", "a": "Strong", "b": "Strong", "winner": "tie"},
            {"feature": "Code Explanation", "a": "Thorough and clear", "b": "Thorough with examples", "winner": "tie"},
            {"feature": "Reasoning (Hard Problems)", "a": "Extended thinking mode", "b": "o1/o3 reasoning models", "winner": "tie"},
            {"feature": "Web Browsing", "a": "Limited", "b": "Full browsing + plugins", "winner": "b", "b_check": True},
            {"feature": "IDE Integration", "a": "Claude Code (terminal)", "b": "Codex agent, ChatGPT plugins", "winner": "tie"},
            {"feature": "API for Custom Tools", "a": "Anthropic API", "b": "OpenAI API", "winner": "tie"}
        ],
        "deep_dive": [
            {
                "heading": "Claude Wins: Code Quality and Instruction Following",
                "icon": "🟠",
                "paragraphs": [
                    "Claude consistently produces cleaner, more idiomatic code. In SWE-bench evaluations (resolving real GitHub issues), Claude models have set the high-water mark. The code it generates tends to be more concise, better structured, and more closely aligned with what you actually asked for.",
                    "The 200K token context window is a significant practical advantage. You can paste an entire codebase into a conversation and Claude will reference specific files, understand cross-file dependencies, and suggest changes that account for the broader system architecture. ChatGPT's 128K window is large but hits limits sooner with real codebases.",
                    "Instruction following is where Claude pulls ahead most noticeably. Tell Claude to 'only modify the authentication middleware, don't touch the routing layer' and it follows that constraint. ChatGPT is more likely to helpfully suggest additional changes you didn't ask for, which can be frustrating when you need precise, scoped modifications."
                ]
            },
            {
                "heading": "ChatGPT Wins: Ecosystem and Versatility",
                "icon": "🟢",
                "paragraphs": [
                    "ChatGPT's ecosystem is unmatched. Custom GPTs, plugins, web browsing, DALL-E for generating architecture diagrams, and a community that shares thousands of coding-specific GPTs. If you want a single tool that handles coding, research, image generation, and data analysis, ChatGPT covers more ground.",
                    "The o1 and o3 reasoning models are genuinely powerful for hard algorithmic problems. When you need to solve a complex dynamic programming challenge or debug a subtle concurrency issue, the reasoning models take extra time to think through the problem step by step. Both Claude and ChatGPT offer reasoning modes, but OpenAI's have been available longer with more refinement.",
                    "Web browsing integration means ChatGPT can look up current documentation, check package versions, and reference Stack Overflow answers during your conversation. Claude's web access is more limited, which sometimes means you need to paste documentation into the conversation yourself."
                ]
            }
        ],
        "use_cases_a": [
            "Large codebase refactoring and analysis",
            "Precise, instruction-following code generation",
            "Working with files that exceed 128K tokens",
            "System prompt engineering and testing",
            "Production code review and audit",
            "Teams prioritizing code quality over speed"
        ],
        "use_cases_b": [
            "Full-stack development with research needs",
            "Quick prototyping with web lookups",
            "Algorithm and competitive programming problems",
            "Multi-modal workflows (code + diagrams)",
            "Teams already in the OpenAI ecosystem",
            "Projects needing plugin integrations"
        ],
        "recommendation_sections": [
            {
                "audience": "For Professional Developers",
                "text": "Claude is the better coding assistant for most professional work. The instruction following, code quality, and large context window make it superior for real-world development tasks: refactoring, debugging production code, and working across large codebases."
            },
            {
                "audience": "For AI/ML Engineers",
                "text": "Use both. Claude for writing and reviewing code. ChatGPT for research, exploring new libraries, and working through complex algorithmic problems with o1 reasoning. They complement each other well."
            },
            {
                "audience": "The Bottom Line",
                "text": "Claude produces better code. ChatGPT is a better general-purpose tool. If coding is your primary use case, Claude wins. If you need one subscription for everything (coding, writing, research, images), ChatGPT's breadth is hard to beat."
            }
        ],
        "faqs": [
            {
                "question": "Is Claude better than ChatGPT for coding?",
                "answer": "For code generation quality and instruction following, Claude leads based on SWE-bench and similar evaluations. ChatGPT offers a broader feature set with web browsing, plugins, and reasoning models. For pure coding tasks, Claude is the better choice for most developers."
            },
            {
                "question": "Can I use both Claude and ChatGPT?",
                "answer": "Yes, and many developers do. A common workflow: use Claude for code generation and review (it follows instructions more precisely), and ChatGPT for research, documentation lookups, and brainstorming. Both offer free tiers."
            },
            {
                "question": "Which is cheaper for API usage?",
                "answer": "Pricing is comparable. Claude Sonnet and GPT-4o are in the same range ($3-5/million input tokens). Claude offers prompt caching for up to 90% savings on repeated context. OpenAI offers batch processing at 50% off. The cheapest option depends on your usage pattern."
            },
            {
                "question": "Which AI handles longer code files better?",
                "answer": "Claude, with its 200K token context window (roughly 150,000 words). GPT-4 Turbo supports 128K tokens. For analyzing entire codebases or very long files, Claude can process about 50% more content in a single conversation."
            }
        ]
    },
    {
        "slug": "copilot-vs-codewhisperer",
        "tool_a": {
            "name": "GitHub Copilot",
            "icon": "🤖",
            "url": "https://github.com/features/copilot",
            "cta_text": "Get Copilot Free",
            "price_free": "Free tier available",
            "price_individual": "Pro: $10/month",
            "price_business": "Business: $19/user/month",
            "price_enterprise": "Enterprise: $39/user/month"
        },
        "tool_b": {
            "name": "Amazon Q Developer",
            "icon": "🔶",
            "url": "https://aws.amazon.com/q/developer/",
            "cta_text": "Try Q Developer Free",
            "price_free": "Free (50 agentic chats/mo)",
            "price_individual": "Pro: $19/user/month",
            "price_business": "$19/user/month",
            "price_enterprise": "Included with AWS"
        },
        "title": "GitHub Copilot vs Amazon Q Developer: Which AI Coding Assistant Wins?",
        "h1": "Which AI Coding Assistant Should You Use?",
        "meta_description": "GitHub Copilot vs Amazon Q Developer (formerly CodeWhisperer): Compare features, pricing, and real-world coding performance for developers in 2026.",
        "og_description": "GitHub Copilot or Amazon Q Developer? We compare the two biggest AI coding assistants on autocomplete, chat, pricing, and enterprise features.",
        "subtitle": "Comparing the two enterprise-grade AI coding assistants (Amazon Q Developer was formerly CodeWhisperer)",
        "verdict_a": "You want the most widely adopted AI coding assistant with the best autocomplete, a massive extension ecosystem, and deep GitHub integration. Copilot is the industry default for a reason.",
        "verdict_b": "You're building on AWS and want an AI assistant that understands your cloud infrastructure. Amazon Q Developer goes beyond code completion into infrastructure management, security scanning, and AWS-native workflows.",
        "features": [
            {"feature": "Code Autocomplete", "a": "Best in class", "b": "Good", "winner": "a", "a_check": True},
            {"feature": "AI Chat", "a": "Copilot Chat (in IDE)", "b": "Q Developer Chat", "winner": "a"},
            {"feature": "Agentic Coding", "a": "Coding agent mode", "b": "Agentic interactions", "winner": "a"},
            {"feature": "Language Support", "a": "Broad (all major languages)", "b": "Broad + AWS SDKs", "winner": "tie"},
            {"feature": "IDE Support", "a": "VS Code, JetBrains, Neovim", "b": "VS Code, JetBrains, CLI", "winner": "tie"},
            {"feature": "Security Scanning", "a": "Basic", "b": "Built-in vulnerability scanning", "winner": "b", "b_check": True},
            {"feature": "Cloud Integration", "a": "GitHub-native", "b": "AWS-native (deep)", "winner": "tie"},
            {"feature": "Code Transformation", "a": "Limited", "b": "Java upgrades, .NET porting", "winner": "b", "b_check": True},
            {"feature": "IP Indemnity", "a": "Business/Enterprise", "b": "Pro tier", "winner": "b"}
        ],
        "deep_dive": [
            {
                "heading": "GitHub Copilot Wins: Autocomplete and Ecosystem",
                "icon": "🤖",
                "paragraphs": [
                    "Copilot's inline code suggestions are the benchmark that every competitor tries to match. The autocomplete is faster, more context-aware, and more consistently useful than Amazon Q Developer's suggestions. When you're in flow and want code to materialize as you type, Copilot is still the tool to beat.",
                    "The GitHub integration creates a workflow that nothing else replicates. Copilot can reference your repositories, understand your commit history, and generate PR descriptions that actually reflect the changes. For teams already on GitHub (which is most teams), this integration eliminates friction.",
                    "Model flexibility matters too. Copilot Pro+ gives you access to multiple AI models including Claude and GPT-4o, letting you pick the best model for each task. Amazon Q Developer is tied to Amazon's own models, with less visibility into what's running under the hood."
                ]
            },
            {
                "heading": "Amazon Q Developer Wins: AWS and Enterprise Security",
                "icon": "🔶",
                "paragraphs": [
                    "If your infrastructure runs on AWS, Q Developer understands it in a way that Copilot can't. It can analyze your CloudFormation templates, suggest IAM policy changes, troubleshoot Lambda functions, and navigate AWS service configurations. This isn't just code completion; it's infrastructure intelligence.",
                    "Code transformation is a unique feature. Q Developer can automatically upgrade Java 8 applications to Java 17, or port .NET Framework applications to cross-platform .NET. For enterprises maintaining legacy codebases, this alone can justify the cost by saving months of manual migration work.",
                    "The security scanning is also more thorough. Q Developer scans for vulnerabilities against a comprehensive database and suggests fixes inline. Copilot has some security features, but Q Developer treats security as a first-class feature rather than an add-on."
                ]
            }
        ],
        "use_cases_a": [
            "Day-to-day code writing and autocomplete",
            "GitHub-centric development workflows",
            "Teams wanting the broadest language support",
            "Open-source development",
            "Developers who want model choice",
            "Quick prototyping and boilerplate generation"
        ],
        "use_cases_b": [
            "AWS-heavy development teams",
            "Legacy code migration (Java, .NET upgrades)",
            "Security-first development workflows",
            "Cloud infrastructure management",
            "Enterprises with AWS Enterprise agreements",
            "Teams needing IP indemnity at lower cost"
        ],
        "recommendation_sections": [
            {
                "audience": "For Individual Developers",
                "text": "GitHub Copilot Pro at $10/month is the clear winner for most developers. Better autocomplete, broader ecosystem, and the free tier lets you try before buying. Choose Q Developer only if you spend most of your time in AWS services."
            },
            {
                "audience": "For Enterprise Teams",
                "text": "The choice depends on your stack. GitHub-centric teams should use Copilot Enterprise. AWS-centric teams get more value from Q Developer, especially with its code transformation and security scanning features. Some enterprises use both."
            },
            {
                "audience": "The Bottom Line",
                "text": "Copilot is the better general-purpose coding assistant. Q Developer is the better AWS companion. If you write code that runs on AWS, Q Developer adds value that Copilot can't. For everything else, Copilot's autocomplete quality and ecosystem make it the default choice."
            }
        ],
        "faqs": [
            {
                "question": "Is GitHub Copilot better than Amazon Q Developer?",
                "answer": "For general-purpose code completion and everyday development, yes. Copilot has better autocomplete and a larger ecosystem. Amazon Q Developer is better for AWS-specific development, legacy code migration, and security scanning. Your primary use case should drive the choice."
            },
            {
                "question": "What happened to Amazon CodeWhisperer?",
                "answer": "Amazon rebranded CodeWhisperer to Amazon Q Developer in April 2024. Q Developer expanded beyond code completion to include agentic chat, code transformation, security scanning, and AWS infrastructure management. Existing CodeWhisperer users were migrated automatically."
            },
            {
                "question": "Can I use both Copilot and Amazon Q Developer?",
                "answer": "Yes. They can run in the same IDE (both support VS Code and JetBrains). Some developers use Copilot for code completion and Q Developer for AWS-specific tasks and security scanning. There's no technical conflict between them."
            },
            {
                "question": "Which offers a better free tier?",
                "answer": "Both offer free tiers. Copilot Free provides limited completions and chat. Q Developer Free includes 50 agentic chat interactions per month and 1,000 lines of code transformation. For code completion, Copilot's free tier is more useful. For AWS-specific help, Q Developer's free tier offers more."
            }
        ]
    }
]


def main():
    with open(DATA_FILE, 'r') as f:
        existing = json.load(f)

    existing_slugs = {c['slug'] for c in existing}
    print(f"Existing comparisons: {len(existing)}")

    added = 0
    for comp in NEW_COMPARISONS:
        if comp['slug'] in existing_slugs:
            print(f"  SKIP (exists): {comp['slug']}")
        else:
            existing.append(comp)
            existing_slugs.add(comp['slug'])
            print(f"  ADDED: {comp['slug']}")
            added += 1

    with open(DATA_FILE, 'w') as f:
        json.dump(existing, f, indent=2)

    print(f"\nDone! Added {added} comparisons. Total: {len(existing)}")


if __name__ == '__main__':
    main()
