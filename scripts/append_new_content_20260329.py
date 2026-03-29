#!/usr/bin/env python3
"""Append 6 new comparisons and 6 new glossary terms - 2026-03-29 batch."""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COMP_FILE = os.path.join(SCRIPT_DIR, '..', 'data', 'comparisons.json')
GLOSS_FILE = os.path.join(SCRIPT_DIR, '..', 'data', 'glossary.json')

NEW_COMPARISONS = [
    {
        "slug": "claude-code-vs-cursor",
        "date_updated": "March 2026",
        "tool_a": {
            "name": "Claude Code",
            "icon": "🟠",
            "url": "https://docs.anthropic.com/en/docs/claude-code",
            "cta_text": "Try Claude Code",
            "price_free": "Included with Claude Pro ($20/mo)",
            "price_individual": "$20/mo (Claude Pro)",
            "price_business": "$25/user/mo (Team)",
            "price_enterprise": "Custom pricing"
        },
        "tool_b": {
            "name": "Cursor",
            "icon": "⚡",
            "url": "https://www.cursor.com",
            "cta_text": "Get Cursor Free",
            "price_free": "Limited free tier",
            "price_individual": "$20/month",
            "price_business": "$40/month",
            "price_enterprise": "Contact sales"
        },
        "title": "Claude Code vs Cursor (2026): Terminal Agent vs AI IDE",
        "h1": "Terminal Agent or AI-Powered IDE?",
        "meta_description": "Claude Code vs Cursor compared: terminal-first agentic coding vs visual AI IDE. Features, pricing, and which fits your development workflow in 2026.",
        "og_description": "Claude Code or Cursor? We compare Anthropic's terminal agent with the leading AI code editor on real-world coding tasks.",
        "subtitle": "Two fundamentally different approaches to AI-assisted development",
        "verdict_a": "You prefer working in the terminal, want an agent that can autonomously execute multi-step coding tasks, and value deep integration with your existing CLI workflow. Claude Code excels at large refactors and codebase-wide changes.",
        "verdict_b": "You want a visual IDE experience with inline completions, chat in the sidebar, and a familiar VS Code interface. Cursor is better for line-by-line coding, real-time autocomplete, and developers who think visually.",
        "features": [
            {"feature": "Interface", "a": "Terminal / CLI", "b": "VS Code fork (GUI)", "winner": "tie"},
            {"feature": "Autocomplete", "a": "No inline autocomplete", "b": "Best-in-class autocomplete", "winner": "b", "b_check": True},
            {"feature": "Agentic Coding", "a": "Full autonomous agent", "b": "Composer agent mode", "winner": "a", "a_check": True},
            {"feature": "Multi-file Edits", "a": "Excellent (reads/writes directly)", "b": "Good (Composer mode)", "winner": "a"},
            {"feature": "Codebase Understanding", "a": "Reads entire repo on demand", "b": "Indexed codebase search", "winner": "tie"},
            {"feature": "Shell Access", "a": "Native (runs commands)", "b": "Built-in terminal", "winner": "a"},
            {"feature": "Model Choice", "a": "Claude models only", "b": "Claude, GPT-4, Gemini", "winner": "b", "b_check": True},
            {"feature": "Git Integration", "a": "Direct git commands", "b": "GUI git + AI commits", "winner": "tie"},
            {"feature": "Learning Curve", "a": "Steeper (terminal-native)", "b": "Lower (familiar IDE)", "winner": "b"}
        ],
        "deep_dive": [
            {
                "heading": "Claude Code Wins: Autonomous Agents and Large Refactors",
                "icon": "🟠",
                "paragraphs": [
                    "Claude Code operates as a true coding agent. Give it a task like 'refactor the authentication module to use JWT instead of session cookies' and it will read the relevant files, plan the changes, write the code, run the tests, and fix failures. You supervise rather than micromanage. For experienced developers who can describe what they want precisely, this workflow is significantly faster than editing files one at a time.",
                    "The terminal-native approach means Claude Code plugs into your existing workflow. It runs in the same environment where you run your tests, your build tools, and your deployment scripts. There is no context switching between an IDE and a terminal. If you already live in tmux or iTerm, Claude Code feels like a natural extension of your workflow.",
                    "For codebase-wide changes, Claude Code has a structural advantage. It can grep across thousands of files, read dependency graphs, and make coordinated changes across dozens of files in a single operation. Cursor's Composer mode handles multi-file edits too, but Claude Code's ability to execute shell commands and verify results mid-task gives it an edge on complex refactors."
                ]
            },
            {
                "heading": "Cursor Wins: Visual Editing and Autocomplete",
                "icon": "⚡",
                "paragraphs": [
                    "Cursor's inline autocomplete is the feature most developers cite as their primary reason for using it. As you type, Cursor suggests the next few lines based on your codebase context, open files, and recent edits. This real-time suggestion loop accelerates line-by-line coding in a way that a terminal agent simply cannot replicate.",
                    "The visual diff interface matters more than it sounds. When Cursor proposes changes, you see a color-coded diff overlay directly in your editor. You can accept individual hunks, reject others, and manually adjust before committing. Claude Code shows diffs in the terminal, which works but requires more cognitive effort to review large changesets.",
                    "Model flexibility is another Cursor advantage. You can switch between Claude, GPT-4.1, and Gemini depending on the task. Some models handle certain languages or frameworks better than others. Claude Code is locked to Anthropic's models, which are excellent but give you no fallback when a particular task would benefit from a different model."
                ]
            }
        ],
        "use_cases_a": [
            "Large-scale codebase refactoring",
            "Developers who live in the terminal",
            "Automated multi-step coding tasks",
            "CI/CD pipeline modifications",
            "Developers who want an agent, not an assistant",
            "Complex cross-file dependency changes"
        ],
        "use_cases_b": [
            "Day-to-day code writing with autocomplete",
            "Developers who prefer a visual IDE",
            "Quick prototyping with inline suggestions",
            "Teams that need model flexibility",
            "Developers transitioning from VS Code",
            "Visual code review and diff management"
        ],
        "recommendation_sections": [
            {
                "audience": "For Senior Developers",
                "text": "Claude Code is the better tool if you can precisely describe what you want. Its agentic workflow handles complex multi-file tasks faster than any IDE-based approach. The tradeoff is zero autocomplete and a terminal-only interface."
            },
            {
                "audience": "For Teams and Onboarding",
                "text": "Cursor is easier to adopt across a team. The VS Code interface is familiar, the autocomplete is immediately useful, and the learning curve is shallow. Claude Code requires more terminal proficiency and a different mental model of AI-assisted coding."
            },
            {
                "audience": "The Bottom Line",
                "text": "Use both. Claude Code for large refactors and autonomous coding tasks. Cursor for everyday line-by-line development. They solve different problems and many developers run both depending on the task at hand."
            }
        ],
        "migration": {
            "what_transfers": [
                "Your code and git history (both use your local filesystem)",
                "Terminal workflows (Claude Code is additive, not replacement)",
                "API keys and environment variables"
            ],
            "what_needs_reconfiguration": [
                "Cursor settings and keybindings don't apply to Claude Code",
                "Cursor's codebase index is separate from Claude Code's file reading",
                "Custom Cursor rules need to be translated to Claude Code's CLAUDE.md format"
            ],
            "time_estimate": "No migration needed. Both tools work on the same codebase simultaneously. You can use Cursor as your IDE and Claude Code in a separate terminal window."
        },
        "faqs": [
            {
                "question": "Can I use Claude Code and Cursor at the same time?",
                "answer": "Yes. Many developers use Cursor as their IDE for autocomplete and visual editing, and run Claude Code in a separate terminal for larger autonomous tasks. Both read and write to the same filesystem. Just be careful about concurrent edits to the same file."
            },
            {
                "question": "Is Claude Code free?",
                "answer": "Claude Code requires a Claude Pro subscription ($20/month) or a Team/Enterprise plan. There is no standalone free tier for Claude Code. Cursor offers a limited free tier with restricted completions and chat messages."
            },
            {
                "question": "Which is better for beginners?",
                "answer": "Cursor. Its VS Code interface is familiar, autocomplete works immediately, and the chat sidebar provides guidance as you code. Claude Code assumes terminal proficiency and requires you to describe tasks clearly in natural language, which takes practice."
            },
            {
                "question": "Does Claude Code have autocomplete?",
                "answer": "No. Claude Code is a terminal-based agent, not an IDE. It does not provide inline code suggestions as you type. For autocomplete, you need an IDE-based tool like Cursor, GitHub Copilot, or Windsurf."
            }
        ],
        "internal_links": [
            {"url": "/tools/cursor-vs-windsurf/", "text": "Cursor vs Windsurf"},
            {"url": "/tools/cursor-vs-copilot/", "text": "Cursor vs GitHub Copilot"},
            {"url": "/tools/cursor-vs-claude-code/", "text": "Cursor vs Claude Code (alternative view)"},
            {"url": "/glossary/ai-coding-assistant/", "text": "What is an AI Coding Assistant?"}
        ]
    },
    {
        "slug": "copilot-vs-codeium",
        "date_updated": "March 2026",
        "tool_a": {
            "name": "GitHub Copilot",
            "icon": "🤖",
            "url": "https://github.com/features/copilot",
            "cta_text": "Get Copilot",
            "price_free": "Free tier (limited)",
            "price_individual": "Pro: $10/month",
            "price_business": "Business: $19/user/month",
            "price_enterprise": "Enterprise: $39/user/month"
        },
        "tool_b": {
            "name": "Codeium (Windsurf)",
            "icon": "🌊",
            "url": "https://codeium.com",
            "cta_text": "Try Codeium Free",
            "price_free": "Free forever (individuals)",
            "price_individual": "Free (unlimited completions)",
            "price_business": "Teams: $15/user/month",
            "price_enterprise": "Enterprise: custom pricing"
        },
        "title": "GitHub Copilot vs Codeium (2026): AI Code Completion Compared",
        "h1": "Which AI Code Completion Tool Should You Use?",
        "meta_description": "GitHub Copilot vs Codeium: Compare code completion quality, pricing, IDE support, and features. Codeium is free for individuals. Full 2026 analysis.",
        "og_description": "Copilot or Codeium? We compare the two most popular AI code completion tools on quality, speed, and pricing.",
        "subtitle": "The industry standard vs the free alternative for AI-powered code completion",
        "verdict_a": "You want the most accurate and context-aware code completions backed by OpenAI and GitHub's ecosystem. Copilot's quality leads the market, and it integrates deeply with GitHub workflows, PR reviews, and documentation.",
        "verdict_b": "You want a genuinely free code completion tool with no usage caps for individual developers. Codeium (now also powering Windsurf IDE) delivers solid completions across 70+ languages and over 40 IDE integrations without costing anything.",
        "features": [
            {"feature": "Completion Quality", "a": "Best in class", "b": "Very good", "winner": "a", "a_check": True},
            {"feature": "Free Tier", "a": "Limited (2K completions/mo)", "b": "Unlimited for individuals", "winner": "b", "b_check": True},
            {"feature": "IDE Support", "a": "VS Code, JetBrains, Neovim", "b": "40+ IDEs including Vim, Emacs", "winner": "b", "b_check": True},
            {"feature": "AI Chat", "a": "Copilot Chat (strong)", "b": "Codeium Chat", "winner": "a"},
            {"feature": "GitHub Integration", "a": "Deep (PRs, issues, actions)", "b": "Basic", "winner": "a", "a_check": True},
            {"feature": "Speed", "a": "Fast", "b": "Very fast", "winner": "b"},
            {"feature": "Privacy Options", "a": "Enterprise only", "b": "Local model option", "winner": "b"},
            {"feature": "Model Choice", "a": "Multiple (Claude, GPT)", "b": "Proprietary models", "winner": "a"},
            {"feature": "Code Search", "a": "Copilot Workspace", "b": "Codeium Search", "winner": "tie"}
        ],
        "deep_dive": [
            {
                "heading": "Copilot Wins: Quality and Ecosystem",
                "icon": "🤖",
                "paragraphs": [
                    "Copilot's completion quality remains the benchmark. It consistently suggests more contextually accurate code, handles edge cases better, and produces fewer suggestions you need to dismiss. This quality difference compounds over a full day of coding. Even a 10% better acceptance rate translates to dozens of fewer rejected suggestions and less cognitive interruption.",
                    "The GitHub ecosystem integration is Copilot's moat. Copilot understands your repository, references open issues when suggesting fixes, generates PR descriptions, and reviews code in pull requests. If your team lives on GitHub, Copilot extends naturally across your entire development lifecycle, not just the editor.",
                    "Model selection in Copilot Pro+ gives you access to Claude Sonnet, GPT-4.1, and other models. Different models perform better on different languages and tasks. Codeium uses proprietary models that you cannot swap or configure."
                ]
            },
            {
                "heading": "Codeium Wins: Pricing and Accessibility",
                "icon": "🌊",
                "paragraphs": [
                    "Codeium's free tier is genuinely unlimited for individual developers. No completion caps, no feature restrictions, no trial countdown. For students, open-source contributors, and developers at companies without tool budgets, this removes the biggest barrier to AI-assisted coding entirely.",
                    "IDE breadth is a real differentiator. Codeium supports over 40 editors including Vim, Emacs, Eclipse, and even web-based IDEs that Copilot does not support. If you use anything outside VS Code or JetBrains, Codeium may be your only option for AI code completion.",
                    "Codeium also offers a local model option for privacy-sensitive environments. Organizations that cannot send code to external servers can run Codeium's models on their own infrastructure. Copilot requires sending code to GitHub's servers (with enterprise privacy controls, but still external)."
                ]
            }
        ],
        "use_cases_a": [
            "Professional developers wanting best completion quality",
            "GitHub-centric development teams",
            "Enterprise organizations needing IP indemnity",
            "Teams wanting model choice (Claude, GPT)",
            "Developers using Copilot Workspace for planning",
            "PR review and documentation generation"
        ],
        "use_cases_b": [
            "Individual developers wanting free AI completions",
            "Students and open-source contributors",
            "Developers using non-standard IDEs (Vim, Emacs)",
            "Organizations needing local/on-premise deployment",
            "Budget-conscious teams getting started with AI tools",
            "Developers wanting fast completions with low latency"
        ],
        "recommendation_sections": [
            {
                "audience": "For Individual Developers",
                "text": "Start with Codeium. It is free with no limits. If you find the completion quality lacking after a few weeks, upgrade to Copilot Pro at $10/month. Many developers find Codeium's quality good enough and never switch."
            },
            {
                "audience": "For Teams and Enterprises",
                "text": "Copilot Business ($19/user/month) is the safer enterprise choice with IP indemnity, admin controls, and GitHub integration. Codeium Teams ($15/user/month) costs less but lacks the GitHub workflow integration."
            },
            {
                "audience": "The Bottom Line",
                "text": "Copilot is better. Codeium is free. If budget is not a factor, Copilot wins on quality and ecosystem. If budget matters, Codeium delivers 80-90% of the value at zero cost for individuals."
            }
        ],
        "faqs": [
            {
                "question": "Is Codeium really free?",
                "answer": "Yes. Codeium offers unlimited code completions and chat for individual developers at no cost. The free tier has no expiration or usage caps. Team features (admin controls, analytics, custom models) require a paid plan starting at $15/user/month."
            },
            {
                "question": "Is Codeium the same as Windsurf?",
                "answer": "Codeium is the company behind both the Codeium code completion extension and Windsurf, a standalone AI IDE. Codeium is the completion engine that works in any IDE. Windsurf is a full VS Code-fork IDE that bundles Codeium's AI features with additional agent capabilities."
            },
            {
                "question": "Which has better code completion quality?",
                "answer": "GitHub Copilot has a slight quality edge, particularly in complex multi-line completions and context-aware suggestions. The gap has narrowed over time. For most daily coding tasks, both tools provide useful suggestions. The difference is most noticeable in less common languages and frameworks."
            },
            {
                "question": "Can I use Codeium in Vim or Emacs?",
                "answer": "Yes. Codeium supports over 40 IDEs and editors including Vim, Neovim, Emacs, Eclipse, and several web-based editors. This is one of the broadest IDE support offerings among AI code completion tools."
            }
        ],
        "internal_links": [
            {"url": "/tools/cursor-vs-copilot/", "text": "Cursor vs GitHub Copilot"},
            {"url": "/tools/cursor-vs-windsurf/", "text": "Cursor vs Windsurf"},
            {"url": "/tools/copilot-vs-codewhisperer/", "text": "Copilot vs Amazon Q Developer"},
            {"url": "/glossary/ai-coding-assistant/", "text": "What is an AI Coding Assistant?"}
        ]
    },
    {
        "slug": "openai-api-vs-anthropic-api-pricing",
        "date_updated": "March 2026",
        "tool_a": {
            "name": "OpenAI API",
            "icon": "🟢",
            "url": "https://platform.openai.com",
            "cta_text": "Get OpenAI API Key",
            "price_free": "Free credits for new accounts",
            "price_individual": "GPT-4o: $2.50/$10 per 1M tokens",
            "price_business": "GPT-4.1: $2/$8 per 1M tokens",
            "price_enterprise": "Volume discounts available"
        },
        "tool_b": {
            "name": "Anthropic API",
            "icon": "🟠",
            "url": "https://console.anthropic.com",
            "cta_text": "Get Anthropic API Key",
            "price_free": "Free credits for new accounts",
            "price_individual": "Sonnet: $3/$15 per 1M tokens",
            "price_business": "Opus: $15/$75 per 1M tokens",
            "price_enterprise": "Volume discounts available"
        },
        "title": "OpenAI API vs Anthropic API Pricing (2026): Cost Breakdown",
        "h1": "Which AI API Gives You Better Value?",
        "meta_description": "OpenAI API vs Anthropic API pricing compared: GPT-4o vs Claude Sonnet costs per token, batch pricing, caching, and real-world cost optimization strategies for 2026.",
        "og_description": "Compare OpenAI and Anthropic API pricing: per-token costs, batch discounts, prompt caching, and total cost of ownership.",
        "subtitle": "A detailed pricing comparison for developers and teams building AI applications",
        "verdict_a": "You want the broadest model lineup with competitive pricing, 50% batch discounts, and the largest ecosystem of tools, libraries, and community support. OpenAI's GPT-4.1 offers strong quality at lower per-token rates than Claude Sonnet.",
        "verdict_b": "You want the best instruction-following model for production applications, with prompt caching that saves up to 90% on repeated context. Anthropic's Claude Sonnet leads on code quality and complex task execution despite slightly higher base pricing.",
        "features": [
            {"feature": "Flagship Model Cost (Input)", "a": "GPT-4o: $2.50/1M tokens", "b": "Sonnet 3.5: $3/1M tokens", "winner": "a"},
            {"feature": "Flagship Model Cost (Output)", "a": "GPT-4o: $10/1M tokens", "b": "Sonnet 3.5: $15/1M tokens", "winner": "a"},
            {"feature": "Batch Processing Discount", "a": "50% off", "b": "50% off", "winner": "tie"},
            {"feature": "Prompt Caching", "a": "Automatic (limited)", "b": "Up to 90% savings", "winner": "b", "b_check": True},
            {"feature": "Budget Model (Input)", "a": "GPT-4o-mini: $0.15/1M", "b": "Haiku: $0.25/1M", "winner": "a", "a_check": True},
            {"feature": "Reasoning Models", "a": "o3-mini: $1.10/$4.40", "b": "Extended thinking (Sonnet)", "winner": "a"},
            {"feature": "Context Window", "a": "128K tokens", "b": "200K tokens", "winner": "b", "b_check": True},
            {"feature": "Rate Limits (default)", "a": "Generous (tier-based)", "b": "Moderate (tier-based)", "winner": "a"},
            {"feature": "Free Credits", "a": "$5-$100 for new users", "b": "$5 for new users", "winner": "a"}
        ],
        "deep_dive": [
            {
                "heading": "OpenAI Wins: Raw Per-Token Pricing",
                "icon": "🟢",
                "paragraphs": [
                    "On a pure per-token basis, OpenAI is cheaper across most model tiers. GPT-4o at $2.50/$10 per million tokens undercuts Claude Sonnet's $3/$15. GPT-4o-mini at $0.15/$0.60 is significantly cheaper than Haiku at $0.25/$1.25. For high-volume applications where every fraction of a cent matters, OpenAI's base pricing is lower.",
                    "The model lineup gives you more price-performance options. GPT-4.1-mini and GPT-4.1-nano offer stepping stones between full GPT-4.1 and GPT-4o-mini. This lets you fine-tune your cost by picking exactly the right model tier for each task in your pipeline.",
                    "OpenAI's batch processing is mature and well-documented. Submit jobs via the Batch API, get results within 24 hours, pay 50% less. For workloads like data classification, content generation, and bulk analysis, this halves your costs with minimal code changes."
                ]
            },
            {
                "heading": "Anthropic Wins: Prompt Caching and Total Cost",
                "icon": "🟠",
                "paragraphs": [
                    "Prompt caching changes the math completely. If your application sends the same system prompt, RAG context, or few-shot examples repeatedly, Anthropic caches that content and charges 90% less for cached tokens on subsequent requests. For a RAG application with a 10K-token system prompt, caching saves $2.70 per million cached input tokens.",
                    "Total cost of ownership often favors Anthropic despite higher base pricing. Claude's superior instruction following means fewer retries, less output parsing failure, and shorter prompts needed to get the right result. If Claude completes a task in one call where GPT-4o needs two attempts, the effective cost per successful task is lower with Claude.",
                    "The 200K context window also reduces costs indirectly. Instead of complex chunking and retrieval pipelines to work within 128K tokens, you can often pass more context directly. This can eliminate the need for a vector database and retrieval layer entirely for smaller knowledge bases, saving infrastructure costs."
                ]
            }
        ],
        "use_cases_a": [
            "High-volume text processing at lowest per-token cost",
            "Applications needing the cheapest budget model",
            "Batch workloads (50% discount on async processing)",
            "Teams needing broad model selection",
            "Applications requiring high rate limits",
            "Prototyping with generous free credits"
        ],
        "use_cases_b": [
            "Applications with repetitive context (RAG, chatbots)",
            "Tasks requiring precise instruction following",
            "Long-context applications (150K+ tokens)",
            "Production systems where retry rate matters",
            "Code generation and analysis pipelines",
            "Applications benefiting from prompt caching"
        ],
        "recommendation_sections": [
            {
                "audience": "For Startups and Prototyping",
                "text": "Start with OpenAI. The free credits are more generous, the ecosystem has more tutorials, and GPT-4o-mini is the cheapest capable model available. Switch to Anthropic if you need better instruction following or your costs are dominated by repeated context (where caching saves 90%)."
            },
            {
                "audience": "For Production Applications",
                "text": "Run cost estimates with both APIs using your actual prompts. If you send the same system prompt or context repeatedly, Anthropic's caching can make it 30-50% cheaper despite higher base pricing. If your workload is diverse with little prompt reuse, OpenAI's lower base rates win."
            },
            {
                "audience": "The Bottom Line",
                "text": "OpenAI is cheaper per token. Anthropic is often cheaper per task. The right choice depends on your usage pattern. Many production systems use both: OpenAI for high-volume simple tasks and Anthropic for complex tasks requiring precision."
            }
        ],
        "faqs": [
            {
                "question": "Which API is cheaper, OpenAI or Anthropic?",
                "answer": "OpenAI has lower per-token base pricing. However, Anthropic's prompt caching (up to 90% savings on repeated context) can make it cheaper for applications with repetitive prompts. Calculate based on your specific usage pattern rather than comparing base rates alone."
            },
            {
                "question": "What is prompt caching and how much does it save?",
                "answer": "Prompt caching stores frequently sent content (system prompts, few-shot examples, RAG context) so you only pay full price on the first request. Anthropic caches input tokens at 90% off on cache hits. For a chatbot sending the same 5K-token system prompt with every message, this saves roughly $2.70 per million cached input tokens."
            },
            {
                "question": "Can I use both OpenAI and Anthropic APIs?",
                "answer": "Yes, and many production applications do. A common pattern: use GPT-4o-mini for simple classification and routing, then Claude Sonnet for complex reasoning tasks. Libraries like LiteLLM and LangChain make it easy to switch between providers with minimal code changes."
            },
            {
                "question": "Which API has better rate limits?",
                "answer": "OpenAI generally offers higher default rate limits, especially at lower spending tiers. Both providers increase limits as your usage grows. For burst workloads, OpenAI is more forgiving. For sustained high-throughput, both offer enterprise rate limit increases on request."
            }
        ],
        "internal_links": [
            {"url": "/tools/openai-api-vs-anthropic-api/", "text": "OpenAI vs Anthropic API (Full Comparison)"},
            {"url": "/tools/openai-vs-gemini-api/", "text": "OpenAI vs Gemini API"},
            {"url": "/glossary/tokens/", "text": "What are Tokens?"},
            {"url": "/glossary/prompt-caching/", "text": "What is Prompt Caching?"}
        ]
    },
    {
        "slug": "langsmith-vs-weights-and-biases",
        "date_updated": "March 2026",
        "tool_a": {
            "name": "LangSmith",
            "icon": "🦜",
            "url": "https://smith.langchain.com",
            "cta_text": "Try LangSmith Free",
            "price_free": "Free (5K traces/mo)",
            "price_individual": "Plus: $39/seat/mo",
            "price_business": "Startup: ~1M traces/mo",
            "price_enterprise": "Custom pricing"
        },
        "tool_b": {
            "name": "Weights & Biases",
            "icon": "📊",
            "url": "https://wandb.ai",
            "cta_text": "Try W&B Free",
            "price_free": "Free (personal projects)",
            "price_individual": "Free for individuals",
            "price_business": "Teams: $50/seat/mo",
            "price_enterprise": "Custom pricing"
        },
        "title": "LangSmith vs Weights & Biases (2026): LLM Observability Compared",
        "h1": "Which LLM Observability Platform Should You Use?",
        "meta_description": "LangSmith vs Weights & Biases for LLM observability: Compare tracing, evaluation, prompt management, and pricing for AI application monitoring in 2026.",
        "og_description": "LangSmith or Weights & Biases? We compare the two leading platforms for LLM tracing, evaluation, and monitoring.",
        "subtitle": "Comparing the two leading platforms for monitoring and evaluating AI applications",
        "verdict_a": "You are building LLM applications with LangChain and need deep tracing, prompt versioning, and evaluation tools designed specifically for LLM pipelines. LangSmith was built for the LLM application stack from day one.",
        "verdict_b": "You need a comprehensive ML platform that handles experiment tracking, model training, dataset management, and LLM monitoring under one roof. W&B Weave extends an established ML platform into LLM observability.",
        "features": [
            {"feature": "LLM Trace Logging", "a": "Purpose-built for LLM chains", "b": "W&B Weave (newer)", "winner": "a", "a_check": True},
            {"feature": "Prompt Management", "a": "Built-in prompt hub", "b": "Artifact-based tracking", "winner": "a"},
            {"feature": "Evaluation Framework", "a": "LangSmith Evaluators", "b": "W&B Evaluate", "winner": "tie"},
            {"feature": "Experiment Tracking", "a": "LLM-focused", "b": "Full ML experiment tracking", "winner": "b", "b_check": True},
            {"feature": "Dataset Management", "a": "Good (test datasets)", "b": "Excellent (W&B Artifacts)", "winner": "b"},
            {"feature": "Model Training Monitoring", "a": "Not supported", "b": "Core feature", "winner": "b", "b_check": True},
            {"feature": "LangChain Integration", "a": "Native (automatic tracing)", "b": "Manual integration", "winner": "a", "a_check": True},
            {"feature": "Framework Agnostic", "a": "Best with LangChain", "b": "Works with any framework", "winner": "b"},
            {"feature": "Community and Docs", "a": "Growing rapidly", "b": "Large, established", "winner": "b"}
        ],
        "deep_dive": [
            {
                "heading": "LangSmith Wins: LLM-Native Observability",
                "icon": "🦜",
                "paragraphs": [
                    "LangSmith was designed specifically for LLM application debugging. Every feature assumes you are building with language models: trace visualization shows each step in a chain, token counts and costs are tracked per-call, and the UI lets you replay any trace with different prompts. This focus means zero configuration for LangChain users and minimal setup for other frameworks.",
                    "The prompt management hub is a standout feature. Store prompt versions, compare performance across versions, and roll back to a previous version without redeploying your application. For teams iterating on prompts daily, this workflow saves significant time compared to managing prompts in code.",
                    "Evaluation in LangSmith is built around LLM-specific metrics: faithfulness, relevance, hallucination detection, and custom rubrics scored by judge LLMs. You define test datasets, run evaluations, and compare results across prompt versions or model changes. The entire loop (edit prompt, evaluate, compare, ship) lives in one platform."
                ]
            },
            {
                "heading": "W&B Wins: Full ML Platform and Flexibility",
                "icon": "📊",
                "paragraphs": [
                    "Weights & Biases is a mature ML platform trusted by 95% of Fortune 500 companies. If your team trains models (fine-tuning, RLHF, custom classifiers), W&B handles experiment tracking, hyperparameter sweeps, and model registry alongside LLM monitoring. LangSmith only covers the LLM application layer.",
                    "W&B Artifacts provides robust dataset versioning that goes beyond LangSmith's test datasets. Track training data lineage, version evaluation datasets, and maintain reproducible experiment pipelines. For teams that care about data provenance and reproducibility, W&B's data management is significantly more mature.",
                    "Framework flexibility matters if you do not use LangChain. W&B Weave works equally well with LlamaIndex, custom Python code, or any other framework. LangSmith works outside LangChain, but the experience is noticeably better within the LangChain ecosystem. If your stack is diverse, W&B adapts more naturally."
                ]
            }
        ],
        "use_cases_a": [
            "LangChain-based LLM applications",
            "Teams focused purely on LLM app development",
            "Rapid prompt iteration and A/B testing",
            "LLM pipeline debugging and tracing",
            "Teams that need prompt version management",
            "Production monitoring of LLM chains"
        ],
        "use_cases_b": [
            "Teams doing model training AND LLM apps",
            "Organizations already using W&B for ML",
            "Multi-framework AI development",
            "Research teams needing experiment tracking",
            "Teams requiring robust dataset versioning",
            "Enterprise ML platforms (Fortune 500)"
        ],
        "recommendation_sections": [
            {
                "audience": "For LLM Application Developers",
                "text": "If you build with LangChain, start with LangSmith. The native integration means automatic tracing with zero code changes. The prompt hub and evaluation tools are designed for exactly your workflow."
            },
            {
                "audience": "For ML/AI Teams",
                "text": "If your team trains models (fine-tuning, classifiers, custom models) in addition to building LLM applications, W&B covers both under one platform. LangSmith only addresses the LLM application layer."
            },
            {
                "audience": "The Bottom Line",
                "text": "LangSmith is the better LLM-specific observability tool. W&B is the better overall ML platform. Choose based on whether your work is purely LLM applications (LangSmith) or spans the full ML lifecycle (W&B)."
            }
        ],
        "faqs": [
            {
                "question": "Do I need LangChain to use LangSmith?",
                "answer": "No. LangSmith works with any LLM framework via its Python and TypeScript SDKs. However, LangChain users get automatic tracing with no additional code. Other frameworks require manual instrumentation, which adds setup time."
            },
            {
                "question": "Can W&B Weave replace LangSmith?",
                "answer": "For basic LLM tracing and evaluation, yes. W&B Weave covers the core observability use cases. LangSmith has deeper features for prompt management and LLM-specific debugging. If you already use W&B for ML experiment tracking, Weave may be sufficient and avoids adding another tool."
            },
            {
                "question": "Which is cheaper for a small team?",
                "answer": "LangSmith offers 5,000 free traces per month. W&B is free for personal projects with unlimited experiments. For a small team (3-5 people), LangSmith Plus at $39/seat/month is comparable to W&B Teams at $50/seat/month. Both offer startup programs with discounted pricing."
            },
            {
                "question": "What about alternatives like Arize, Langfuse, or Helicone?",
                "answer": "Arize Phoenix is a strong open-source alternative. Langfuse offers open-source LLM tracing. Helicone focuses on API gateway and cost tracking. LangSmith and W&B are the most comprehensive options, but open-source alternatives work well for teams wanting self-hosted solutions."
            }
        ],
        "internal_links": [
            {"url": "/tools/langchain-vs-llamaindex/", "text": "LangChain vs LlamaIndex"},
            {"url": "/tools/langchain-vs-crewai/", "text": "LangChain vs CrewAI"},
            {"url": "/glossary/rag/", "text": "What is RAG?"},
            {"url": "/glossary/model-evaluation/", "text": "What is Model Evaluation?"}
        ]
    },
    {
        "slug": "perplexity-vs-chatgpt-research",
        "date_updated": "March 2026",
        "tool_a": {
            "name": "Perplexity",
            "icon": "🔍",
            "url": "https://www.perplexity.ai",
            "cta_text": "Try Perplexity Free",
            "price_free": "Free (limited Pro searches)",
            "price_individual": "Pro: $20/month",
            "price_business": "Enterprise: $40/user/month",
            "price_enterprise": "Custom pricing"
        },
        "tool_b": {
            "name": "ChatGPT",
            "icon": "🟢",
            "url": "https://chat.openai.com",
            "cta_text": "Try ChatGPT Free",
            "price_free": "Free (GPT-4o mini)",
            "price_individual": "Plus: $20/month",
            "price_business": "Team: $25/user/month",
            "price_enterprise": "Custom pricing"
        },
        "title": "Perplexity vs ChatGPT for Research (2026): Which Is Better?",
        "h1": "Which AI Is Better for Research?",
        "meta_description": "Perplexity vs ChatGPT for research: Compare source citations, accuracy, search capabilities, and which AI gives you more reliable answers in 2026.",
        "og_description": "Perplexity or ChatGPT for research? We compare both AI tools on citation quality, accuracy, and real-world research tasks.",
        "subtitle": "An answer engine vs a general-purpose AI for research and fact-finding tasks",
        "verdict_a": "You want an AI that searches the web in real-time and cites every claim with a numbered source. Perplexity is built for research: it finds information, summarizes it, and shows you exactly where it came from so you can verify.",
        "verdict_b": "You want a general-purpose AI that can research, analyze, write, code, and create in a single conversation. ChatGPT's web browsing is one feature among many, and its reasoning models excel at synthesizing complex topics.",
        "features": [
            {"feature": "Source Citations", "a": "Every answer, inline numbered", "b": "Occasional, not consistent", "winner": "a", "a_check": True},
            {"feature": "Real-time Web Search", "a": "Every query (core feature)", "b": "When model decides to search", "winner": "a", "a_check": True},
            {"feature": "Search Depth", "a": "Deep (reads multiple pages)", "b": "Surface (snippets)", "winner": "a"},
            {"feature": "Follow-up Research", "a": "Suggested follow-ups", "b": "Conversational follow-ups", "winner": "tie"},
            {"feature": "Analysis and Synthesis", "a": "Good summaries", "b": "Excellent deep analysis", "winner": "b", "b_check": True},
            {"feature": "Writing from Research", "a": "Basic", "b": "Full writing assistant", "winner": "b", "b_check": True},
            {"feature": "Academic Sources", "a": "Academic search mode", "b": "No dedicated academic mode", "winner": "a"},
            {"feature": "File Upload", "a": "PDF analysis", "b": "Any file type analysis", "winner": "b"},
            {"feature": "Speed", "a": "Fast (search + answer)", "b": "Variable (depends on task)", "winner": "a"}
        ],
        "deep_dive": [
            {
                "heading": "Perplexity Wins: Citations and Verifiability",
                "icon": "🔍",
                "paragraphs": [
                    "Perplexity's core advantage is that every answer comes with numbered source citations. Each claim maps to a specific URL you can click and verify. This is not optional or inconsistent. It is the fundamental design of the product. For any research task where accuracy and verifiability matter, this citation model is transformative.",
                    "The search depth goes beyond what ChatGPT's browsing provides. Perplexity reads full pages, cross-references multiple sources, and synthesizes information from 5-10 web results. ChatGPT's web browsing often pulls from snippets and may not read full articles. When you need comprehensive coverage of a topic, Perplexity's search pipeline produces more thorough results.",
                    "Academic search mode is purpose-built for scholarly research. It prioritizes peer-reviewed papers, academic databases, and institutional sources. For literature reviews, market research, and technical due diligence, this focused search mode saves significant time compared to filtering through general web results."
                ]
            },
            {
                "heading": "ChatGPT Wins: Analysis and Versatility",
                "icon": "🟢",
                "paragraphs": [
                    "ChatGPT is a better thinker than searcher. When you need to analyze a complex topic, compare multiple perspectives, or synthesize information into a framework, ChatGPT's reasoning capabilities produce deeper insights. Perplexity excels at finding and summarizing information. ChatGPT excels at analyzing and reasoning about it.",
                    "The ability to transition from research into action is a major ChatGPT advantage. Research a topic, then ask ChatGPT to write a report, create a presentation outline, draft an email, or build a spreadsheet formula based on the findings. Perplexity's scope stops at answering questions. ChatGPT can take the next step.",
                    "ChatGPT's reasoning models (o3) handle complex analytical questions that Perplexity cannot. Questions like 'What would happen to the housing market if interest rates dropped 2% while immigration increased 30%?' require multi-step reasoning, not web search. ChatGPT can model scenarios and reason through implications in ways Perplexity is not designed for."
                ]
            }
        ],
        "use_cases_a": [
            "Fact-checking and source verification",
            "Market research with citation needs",
            "Academic literature reviews",
            "Competitive intelligence gathering",
            "Replacing Google for question-based searches",
            "Research tasks where trust and verifiability matter"
        ],
        "use_cases_b": [
            "Deep analysis requiring multi-step reasoning",
            "Research that leads directly into writing",
            "Complex scenario modeling and forecasting",
            "Multi-modal research (text, images, files)",
            "Research combined with coding or data analysis",
            "General productivity beyond just search"
        ],
        "recommendation_sections": [
            {
                "audience": "For Researchers and Analysts",
                "text": "Use Perplexity as your primary research tool. Its citation model and search depth are purpose-built for finding accurate, verifiable information. Then use ChatGPT to analyze and synthesize what you found into deliverables."
            },
            {
                "audience": "For Knowledge Workers",
                "text": "ChatGPT is the better all-in-one tool. Research, analyze, write, and create in a single conversation. Perplexity is a better search engine, but ChatGPT is a better work companion."
            },
            {
                "audience": "The Bottom Line",
                "text": "Perplexity is the better research tool. ChatGPT is the better thinking tool. Use Perplexity when you need to find and verify information. Use ChatGPT when you need to analyze, reason, and create from information."
            }
        ],
        "faqs": [
            {
                "question": "Is Perplexity more accurate than ChatGPT?",
                "answer": "For factual questions, Perplexity is more reliable because it searches the web in real-time and cites sources. ChatGPT relies on training data (potentially outdated) unless it decides to browse. Perplexity does not hallucinate less, but its citations let you verify claims quickly."
            },
            {
                "question": "Should I cancel ChatGPT Plus if I get Perplexity Pro?",
                "answer": "Only if your primary use case is research and question-answering. ChatGPT covers far more ground: coding, writing, image generation, data analysis, and reasoning. Perplexity is focused on search and answers. Many users subscribe to both at $20/month each."
            },
            {
                "question": "Can Perplexity replace Google?",
                "answer": "For question-based searches, yes. Perplexity provides direct answers with sources instead of a list of blue links. For navigational searches (finding a specific website) or shopping, Google is still better. Perplexity is best thought of as a research companion, not a full Google replacement."
            },
            {
                "question": "Does ChatGPT cite its sources?",
                "answer": "Sometimes. When ChatGPT browses the web, it may include links. But citation is inconsistent and not the default behavior. Perplexity cites every answer by design with inline numbered references. If source verification matters, Perplexity is the clear choice."
            }
        ],
        "internal_links": [
            {"url": "/tools/claude-vs-chatgpt-coding/", "text": "Claude vs ChatGPT for Coding"},
            {"url": "/tools/claude-vs-gemini/", "text": "Claude vs Gemini"},
            {"url": "/glossary/hallucination/", "text": "What is AI Hallucination?"},
            {"url": "/glossary/grounding/", "text": "What is Grounding?"}
        ]
    },
    {
        "slug": "huggingface-vs-replicate",
        "date_updated": "March 2026",
        "tool_a": {
            "name": "Hugging Face",
            "icon": "🤗",
            "url": "https://huggingface.co",
            "cta_text": "Explore Hugging Face",
            "price_free": "Free (Inference API limited)",
            "price_individual": "Pro: $9/month",
            "price_business": "Inference Endpoints: usage-based",
            "price_enterprise": "Enterprise Hub: custom pricing"
        },
        "tool_b": {
            "name": "Replicate",
            "icon": "🔁",
            "url": "https://replicate.com",
            "cta_text": "Try Replicate Free",
            "price_free": "Free credits on signup",
            "price_individual": "Pay per second of compute",
            "price_business": "Volume discounts available",
            "price_enterprise": "Custom pricing"
        },
        "title": "Hugging Face vs Replicate (2026): Model Hosting Compared",
        "h1": "Which Platform Should You Use for Running AI Models?",
        "meta_description": "Hugging Face vs Replicate: Compare model hosting, inference APIs, pricing, and community. Which platform is better for deploying open-source AI models in 2026?",
        "og_description": "Hugging Face or Replicate? We compare the two leading platforms for hosting and running open-source AI models.",
        "subtitle": "The AI model hub vs the simple inference platform for running open-source models",
        "verdict_a": "You want the largest collection of open-source models, a thriving community, and flexible deployment options from free inference to dedicated endpoints. Hugging Face is the GitHub of AI models with 800K+ models available.",
        "verdict_b": "You want the simplest way to run AI models via API without managing infrastructure. Replicate wraps models in a clean API with one-line deployment and pay-per-second pricing. No Docker, no GPU management, no configuration.",
        "features": [
            {"feature": "Model Library", "a": "800K+ models", "b": "Curated (thousands)", "winner": "a", "a_check": True},
            {"feature": "Ease of Deployment", "a": "Moderate (Endpoints)", "b": "Very simple (one command)", "winner": "b", "b_check": True},
            {"feature": "Custom Model Hosting", "a": "Full control (Endpoints)", "b": "Cog container format", "winner": "a"},
            {"feature": "Free Inference", "a": "Limited free API", "b": "Free credits only", "winner": "a"},
            {"feature": "Pricing Model", "a": "Per-hour (Endpoints)", "b": "Per-second of compute", "winner": "b"},
            {"feature": "Community", "a": "Massive (datasets, spaces)", "b": "Growing", "winner": "a", "a_check": True},
            {"feature": "Image Generation", "a": "Supported (Diffusion)", "b": "Strong (Flux, SDXL)", "winner": "tie"},
            {"feature": "Fine-tuning Support", "a": "AutoTrain, custom", "b": "Training API (select models)", "winner": "a"},
            {"feature": "Documentation", "a": "Extensive", "b": "Clean and focused", "winner": "tie"}
        ],
        "deep_dive": [
            {
                "heading": "Hugging Face Wins: Model Selection and Community",
                "icon": "🤗",
                "paragraphs": [
                    "Hugging Face hosts over 800,000 models. If a model exists in the open-source world, it is on Hugging Face. This includes every variant of Llama, Mistral, Stable Diffusion, Whisper, and thousands of fine-tuned models for specific tasks. Replicate curates a smaller collection, which means you may not find the exact model variant you need.",
                    "The community layer is what makes Hugging Face more than a model registry. Spaces let you deploy interactive demos. Datasets provide training data alongside models. Discussion forums under each model share usage tips and known issues. This ecosystem means you rarely start from scratch when working with a new model.",
                    "For teams that need fine-tuning, Hugging Face offers AutoTrain (no-code fine-tuning) and direct integration with the Transformers library. You can fine-tune a model, push it to the Hub, and deploy it to an Inference Endpoint in a single workflow. Replicate's training support is more limited."
                ]
            },
            {
                "heading": "Replicate Wins: Simplicity and Pay-Per-Second Pricing",
                "icon": "🔁",
                "paragraphs": [
                    "Replicate's API is remarkably simple. Pick a model, send input, get output. No endpoint configuration, no GPU selection, no scaling policies. For developers who want to add AI model inference to an application without becoming infrastructure engineers, Replicate removes nearly all the friction.",
                    "Pay-per-second pricing means you pay nothing when your model is idle. Hugging Face Inference Endpoints charge per hour, even when no requests come in. For applications with variable traffic (internal tools, side projects, batch jobs), Replicate's pricing model avoids the waste of paying for idle GPUs.",
                    "Replicate's cold start optimization has improved significantly. Models spin up faster than Hugging Face Endpoints with serverless configuration. For latency-sensitive applications, Replicate offers dedicated hardware, but even the default serverless inference is responsive enough for most use cases."
                ]
            }
        ],
        "use_cases_a": [
            "Teams needing access to any open-source model",
            "Organizations building fine-tuned model pipelines",
            "Research teams sharing and discovering models",
            "Projects needing datasets alongside models",
            "Companies wanting dedicated GPU endpoints",
            "MLOps teams with existing Hugging Face workflows"
        ],
        "use_cases_b": [
            "Developers wanting the simplest model API",
            "Applications with variable/low traffic",
            "Quick prototyping without infrastructure setup",
            "Image and video generation applications",
            "Teams without ML infrastructure expertise",
            "Projects needing pay-per-use pricing"
        ],
        "recommendation_sections": [
            {
                "audience": "For Application Developers",
                "text": "Start with Replicate if you want the fastest path to a working integration. Its API is simpler, pricing is more predictable for variable workloads, and you avoid infrastructure decisions entirely. Move to Hugging Face Endpoints when you need custom models or higher throughput."
            },
            {
                "audience": "For ML/AI Teams",
                "text": "Hugging Face is the better platform for teams that train, fine-tune, and deploy models as a core part of their work. The model hub, dataset registry, and Endpoints create an integrated workflow that Replicate's simpler approach cannot match."
            },
            {
                "audience": "The Bottom Line",
                "text": "Replicate for simplicity. Hugging Face for depth. If you just need to call a model API, Replicate wins. If you need the full model lifecycle (find, fine-tune, evaluate, deploy), Hugging Face wins."
            }
        ],
        "faqs": [
            {
                "question": "Is Hugging Face free to use?",
                "answer": "Hugging Face Hub (browsing models, datasets, spaces) is free. The free Inference API has rate limits. Dedicated Inference Endpoints start at approximately $0.06/hour for CPU and $0.60/hour for GPU. Pro accounts ($9/month) get higher rate limits on the free API."
            },
            {
                "question": "How does Replicate pricing work?",
                "answer": "Replicate charges per second of compute time. Prices vary by hardware: CPU models cost fractions of a cent per second, GPU models range from $0.000225/sec (T4) to $0.003525/sec (A100 80GB). You only pay while the model processes your request. No idle charges."
            },
            {
                "question": "Can I deploy my own custom model on Replicate?",
                "answer": "Yes. Replicate uses the Cog packaging format to containerize models. You define your model's setup and prediction functions in a Python file, build a Cog container, and push it to Replicate. The process takes 30-60 minutes for a first deployment."
            },
            {
                "question": "Which is better for image generation?",
                "answer": "Both support popular image models (Stable Diffusion, Flux). Replicate has a slightly better experience for image generation with optimized cold starts and a clean API for image outputs. Hugging Face offers more model variants and fine-tuned checkpoints."
            }
        ],
        "internal_links": [
            {"url": "/tools/pinecone-vs-weaviate/", "text": "Pinecone vs Weaviate"},
            {"url": "/glossary/inference/", "text": "What is Inference?"},
            {"url": "/glossary/fine-tuning/", "text": "What is Fine-Tuning?"},
            {"url": "/glossary/quantization/", "text": "What is Quantization?"}
        ]
    }
]

NEW_GLOSSARY_TERMS = [
    {
        "term": "Retrieval Augmented Generation",
        "slug": "retrieval-augmented-generation",
        "full_name": "Retrieval Augmented Generation (RAG)",
        "definition": "An architecture pattern that enhances language model responses by first retrieving relevant documents from an external knowledge base, then passing those documents as context to the model for answer generation. RAG grounds model outputs in real, verifiable data rather than relying solely on trained knowledge.",
        "category": "Architecture Patterns",
        "related_terms": ["rag", "vector-database", "embeddings", "semantic-search"],
        "related_links": [
            "/glossary/rag/",
            "/tools/pinecone-vs-weaviate/",
            "/glossary/vector-database/",
            "/glossary/embeddings/"
        ],
        "example": "A legal research tool receives the question 'What are the filing requirements for a 10-K?' The RAG system searches a database of SEC filings and legal documents, retrieves the 5 most relevant passages, and passes them to Claude alongside the question. The model generates an answer citing specific SEC rules, grounded in the retrieved documents rather than its training data.",
        "why_it_matters": "RAG is the dominant architecture for production AI applications that need factual accuracy. It solves the hallucination problem by giving models access to verified, up-to-date information. Nearly every enterprise AI chatbot, knowledge base, and research tool uses some form of RAG.",
        "in_depth": "A RAG pipeline has three core stages: indexing, retrieval, and generation.\n\nDuring indexing, your documents are split into chunks (by paragraph, section, or semantic boundary), converted into vector embeddings, and stored in a vector database like Pinecone or Weaviate. This is a one-time process that runs when documents change.\n\nAt query time, the user's question is converted into the same embedding format and compared against stored vectors using similarity search. The top 3-10 most relevant chunks are retrieved.\n\nFinally, the retrieved chunks are inserted into the LLM's prompt alongside the original question. The model generates a response grounded in the provided context, reducing hallucination and enabling citation.\n\nAdvanced RAG patterns include hybrid search (combining vector and keyword matching), re-ranking (using a second model to improve retrieval quality), and multi-hop RAG (iterative retrieval for complex questions that span multiple documents).",
        "common_mistakes": [
            {
                "mistake": "Using fixed-size token chunks without considering document structure",
                "correction": "Chunk by semantic boundaries (headings, paragraphs, logical sections). Use overlapping windows to prevent splitting critical information across chunks."
            },
            {
                "mistake": "Skipping evaluation of retrieval quality independently from generation quality",
                "correction": "Measure retrieval precision and recall separately. A perfect LLM cannot fix poor retrieval. If the relevant document is not retrieved, the answer will be wrong."
            },
            {
                "mistake": "Indexing entire documents without metadata filtering",
                "correction": "Add metadata (date, source, category, author) to chunks so retrieval can be filtered. This dramatically improves relevance for multi-topic knowledge bases."
            }
        ],
        "career_relevance": "RAG engineering is the most in-demand AI architecture skill in 2026. Companies building AI products need engineers who can design chunking strategies, optimize retrieval pipelines, and evaluate RAG system quality. RAG-specific roles pay $150K-$250K at the senior level.",
        "faqs": [
            {
                "question": "What is the difference between RAG and fine-tuning?",
                "answer": "RAG adds external knowledge at query time without changing the model. Fine-tuning changes the model's weights to encode knowledge permanently. RAG is better for frequently changing data (knowledge bases, documentation). Fine-tuning is better for teaching the model new behaviors or domain-specific language."
            },
            {
                "question": "Do I need a vector database for RAG?",
                "answer": "For production systems, yes. Vector databases (Pinecone, Weaviate, Chroma) handle indexing, similarity search, and metadata filtering at scale. For prototypes with small document sets, you can use in-memory vectors, but this does not scale beyond a few thousand documents."
            }
        ]
    },
    {
        "term": "Function Calling in LLMs",
        "slug": "function-calling-llms",
        "full_name": "Function Calling in Large Language Models",
        "definition": "A capability that allows language models to generate structured JSON output that maps to predefined function signatures, enabling the model to interact with external tools, APIs, and databases. Instead of generating free-form text, the model outputs a function name and arguments that application code can execute.",
        "category": "Architecture Patterns",
        "related_terms": ["function-calling", "tool-use", "ai-agent", "model-context-protocol", "structured-output"],
        "related_links": [
            "/glossary/function-calling/",
            "/glossary/tool-use/",
            "/glossary/ai-agent/",
            "/glossary/model-context-protocol/"
        ],
        "example": "You define a function get_weather(city: str, unit: str). When a user asks 'What is the weather in Paris?', the model does not hallucinate a weather report. Instead, it outputs: {\"function\": \"get_weather\", \"arguments\": {\"city\": \"Paris\", \"unit\": \"celsius\"}}. Your application executes the actual API call and returns real weather data to the model for its response.",
        "why_it_matters": "Function calling transforms LLMs from text generators into action-taking agents. It is the technical foundation for AI assistants that can book flights, query databases, send emails, and interact with any system that has an API. Without function calling, AI agents would not exist.",
        "in_depth": "Function calling works through a structured protocol between your application and the model.\n\nFirst, you define available functions as JSON schemas (name, description, parameters with types). These schemas are sent to the model alongside the user's message.\n\nThe model then decides whether to respond with text or call a function. If a function call is appropriate, it outputs the function name and arguments as structured JSON. Your application parses this JSON, executes the real function, and sends the result back to the model.\n\nThe model can chain multiple function calls in a single conversation turn, enabling complex workflows like: search for flights, filter by price, then book the cheapest option.\n\nOpenAI, Anthropic, and Google all support function calling (Anthropic calls it 'tool use'). The implementations differ slightly but the core concept is the same: the model generates structured output that maps to real code execution.",
        "common_mistakes": [
            {
                "mistake": "Writing vague function descriptions that confuse the model about when to use each function",
                "correction": "Write clear, specific descriptions with usage examples. Describe not just what the function does, but when the model should choose it over alternatives."
            },
            {
                "mistake": "Not handling cases where the model calls the wrong function or provides invalid arguments",
                "correction": "Always validate function arguments before execution. Implement fallback logic for incorrect function calls. The model will occasionally make mistakes."
            },
            {
                "mistake": "Defining too many functions in a single request, which increases latency and confusion",
                "correction": "Keep function sets focused. Use 5-15 functions maximum per request. Group related functions and only expose the relevant set based on conversation context."
            }
        ],
        "career_relevance": "Function calling is a required skill for AI agent developers and AI engineers. Every production AI assistant (customer support bots, coding agents, data analysts) relies on function calling to interact with external systems. Understanding this pattern is essential for building anything beyond a simple chatbot.",
        "faqs": [
            {
                "question": "What is the difference between function calling and tool use?",
                "answer": "They refer to the same concept. OpenAI uses 'function calling,' Anthropic uses 'tool use,' and Google uses 'function declarations.' The underlying mechanism is identical: the model generates structured output that maps to executable code."
            },
            {
                "question": "Can function calling replace traditional API integrations?",
                "answer": "Function calling does not replace APIs. It adds an AI layer on top. The model decides which API to call and with what parameters, but your application still makes the actual API requests. Function calling is the decision layer, not the execution layer."
            }
        ]
    },
    {
        "term": "AI Agent",
        "slug": "what-is-ai-agent",
        "full_name": "AI Agent (Autonomous Agent)",
        "definition": "An AI system that can independently plan, execute, and iterate on tasks by combining language model reasoning with tool use, memory, and feedback loops. Unlike a chatbot that responds to one prompt at a time, an AI agent pursues a goal autonomously, deciding which actions to take, executing them, evaluating results, and adjusting its approach.",
        "category": "Core Concepts",
        "related_terms": ["ai-agent", "agentic-ai", "function-calling", "tool-use", "model-context-protocol"],
        "related_links": [
            "/glossary/ai-agent/",
            "/glossary/agentic-ai/",
            "/glossary/tool-use/",
            "/glossary/function-calling/"
        ],
        "example": "You tell a coding agent: 'Add user authentication to this Flask app.' The agent reads the codebase, identifies the relevant files, plans the implementation (routes, database schema, middleware), writes the code across multiple files, runs the test suite, identifies a failing test, debugs the issue, fixes it, and re-runs tests until they all pass. You supervise rather than dictate each step.",
        "why_it_matters": "AI agents represent the next evolution of AI applications. While chatbots answer questions, agents complete tasks. The shift from 'AI that talks' to 'AI that does' is driving massive investment from every major AI company. Agent-related job postings grew over 300% in 2025.",
        "in_depth": "An AI agent operates through a loop: observe, think, act, evaluate.\n\nIn the observe phase, the agent gathers information about its current state. It might read files, check database values, or process user input.\n\nIn the think phase, the language model reasons about what to do next. This is where chain-of-thought prompting and planning happen. The model considers available tools, prior results, and the overall goal.\n\nIn the act phase, the agent executes a tool call: running code, calling an API, writing a file, or searching the web. Function calling is the mechanism that enables this.\n\nIn the evaluate phase, the agent assesses the result. Did the action succeed? Is the goal met? Should the approach change? This feedback loop continues until the task is complete or the agent determines it cannot proceed.\n\nModern agent frameworks include LangGraph, CrewAI, and AutoGen. Each provides different abstractions for building multi-step, tool-using AI systems.",
        "common_mistakes": [
            {
                "mistake": "Giving agents too much autonomy without human checkpoints",
                "correction": "Implement approval gates for high-impact actions (sending emails, modifying production data, making purchases). Start with human-in-the-loop and relax as you build trust."
            },
            {
                "mistake": "Building agents that cannot recover from failures",
                "correction": "Design agents with explicit error handling and retry logic. The model should recognize when an action failed and try an alternative approach rather than repeating the same failing action."
            },
            {
                "mistake": "Using agents for tasks that a simple prompt chain would handle",
                "correction": "Agents add complexity and cost. If a task has a predictable 3-step workflow, use prompt chaining instead. Reserve agents for tasks where the steps depend on intermediate results."
            }
        ],
        "career_relevance": "AI agent development is one of the fastest-growing roles in tech. Companies need engineers who can design agent architectures, implement tool integrations, build evaluation frameworks, and manage the reliability challenges of autonomous systems. Salaries for senior agent developers range from $180K-$300K.",
        "faqs": [
            {
                "question": "What is the difference between a chatbot and an AI agent?",
                "answer": "A chatbot responds to individual messages. An AI agent pursues goals autonomously across multiple steps. A chatbot answers 'How do I deploy to AWS?' An agent actually deploys your code to AWS, handling configuration, testing, and troubleshooting along the way."
            },
            {
                "question": "Are AI agents reliable enough for production?",
                "answer": "For well-defined tasks with good guardrails, yes. Coding agents, customer support agents, and data analysis agents are in production at major companies. For open-ended tasks with high stakes, they still need human oversight. Reliability improves as models improve."
            }
        ]
    },
    {
        "term": "Chain of Thought Prompting",
        "slug": "what-is-chain-of-thought",
        "full_name": "Chain of Thought (CoT) Prompting",
        "definition": "A prompting technique that instructs the language model to show its reasoning process step by step before reaching a final answer. By generating intermediate reasoning steps, the model produces significantly more accurate results on math, logic, coding, and multi-step reasoning tasks.",
        "category": "Prompting Techniques",
        "related_terms": ["chain-of-thought", "prompt-engineering", "reasoning-models", "few-shot-prompting"],
        "related_links": [
            "/glossary/chain-of-thought/",
            "/glossary/prompt-engineering/",
            "/glossary/reasoning-models/",
            "/blog/prompt-engineering-best-practices/"
        ],
        "example": "Without CoT: 'A store has 45 apples. They sell 12 and receive 30. How many?' Model might answer incorrectly.\n\nWith CoT: 'Think step by step. A store has 45 apples. They sell 12 and receive 30. How many?'\nModel: 'Starting: 45 apples. After selling 12: 45 - 12 = 33. After receiving 30: 33 + 30 = 63. Answer: 63 apples.'",
        "why_it_matters": "Chain of thought prompting improves accuracy by 20-40% on reasoning tasks according to research from Google. It is one of the most impactful prompt engineering techniques and forms the basis of modern reasoning models like o1 and o3. Understanding when and how to use CoT is a core prompt engineering skill.",
        "in_depth": "Chain of thought works because language models process text sequentially. Each generated token serves as additional context for the next token. When the model writes out intermediate steps, each step provides context that improves the accuracy of subsequent steps.\n\nThere are several CoT variants with different applications:\n\nZero-shot CoT: Simply add 'Let's think step by step' to your prompt. This triggers step-by-step reasoning without examples. It is the simplest approach and works surprisingly well on most reasoning tasks.\n\nFew-shot CoT: Provide 2-3 example problems with worked-out solutions before your actual question. The examples teach the model the expected reasoning format. This produces more reliable output than zero-shot CoT.\n\nSelf-consistency: Generate multiple CoT reasoning paths for the same question, then take a majority vote on the final answer. If 4 out of 5 reasoning paths arrive at the same answer, that answer is likely correct.\n\nTree of Thought: Explore multiple reasoning branches at each step, evaluate which branches look most promising, and follow the best path. This is slower and more expensive but handles complex problems where the first approach may be a dead end.",
        "common_mistakes": [
            {
                "mistake": "Using chain of thought for simple factual lookups where it adds unnecessary cost and latency",
                "correction": "Reserve CoT for multi-step reasoning: math, logic, code debugging, multi-part analysis. For simple questions like 'What is the capital of France?' direct prompting is faster and cheaper."
            },
            {
                "mistake": "Providing chain of thought examples with flawed reasoning steps",
                "correction": "Double-check the logic in your few-shot examples. Models learn from your examples, including your mistakes. One error in a CoT example can systematically bias all subsequent answers."
            },
            {
                "mistake": "Assuming CoT always helps with smaller models",
                "correction": "Research shows CoT provides the biggest gains with larger models (70B+ parameters). Smaller models sometimes perform worse with CoT because they struggle to maintain coherent multi-step reasoning. Test before committing."
            }
        ],
        "career_relevance": "Chain of thought is the most widely applicable prompt engineering technique. It appears in nearly every prompt engineering interview and is a requirement for building reliable AI applications that handle reasoning tasks. Mastering CoT variants is a baseline expectation for prompt engineer roles.",
        "faqs": [
            {
                "question": "Does chain of thought cost more?",
                "answer": "Yes. CoT prompts generate more output tokens (the reasoning steps), which increases cost. However, the accuracy improvement often reduces the need for retries, which can offset the higher per-call cost. For critical tasks, the accuracy gain is usually worth the extra tokens."
            },
            {
                "question": "How is CoT different from reasoning models like o1?",
                "answer": "Traditional CoT is a prompting technique that you apply manually. Reasoning models like o1 and o3 perform chain of thought internally as part of their architecture. You do not need to ask o1 to 'think step by step' because it already does. Traditional CoT is for standard models; reasoning models have it built in."
            }
        ]
    },
    {
        "term": "Model Distillation",
        "slug": "model-distillation",
        "full_name": "Model Distillation (Knowledge Distillation)",
        "definition": "A training technique where a smaller 'student' model learns to replicate the behavior of a larger 'teacher' model. The student model is trained on the teacher's outputs rather than raw data, capturing the larger model's knowledge in a more compact, faster, and cheaper form factor.",
        "category": "Model Training",
        "related_terms": ["knowledge-distillation", "fine-tuning", "quantization", "inference"],
        "related_links": [
            "/glossary/knowledge-distillation/",
            "/glossary/fine-tuning/",
            "/glossary/quantization/",
            "/glossary/inference/"
        ],
        "example": "A company uses GPT-4 to classify 100,000 customer support tickets into 15 categories with 95% accuracy. They then fine-tune a small open-source model (Llama 8B) on GPT-4's classifications. The distilled model achieves 92% accuracy at 1/100th the inference cost and 10x the speed, suitable for real-time classification.",
        "why_it_matters": "Distillation is how companies move from expensive prototype to affordable production. Most AI applications prototype with a large model (GPT-4, Claude Opus) then distill into a smaller, faster model for deployment. This pattern reduces inference costs by 90-99% while retaining most of the quality.",
        "in_depth": "Distillation works on a simple insight: the probability distributions generated by a large model contain richer information than raw labels alone.\n\nWhen GPT-4 classifies a support ticket as 'billing issue,' it also assigns lower probabilities to related categories like 'account access' and 'payment failure.' These soft probability distributions, called 'soft labels' or 'dark knowledge,' capture nuanced relationships between categories that binary labels miss.\n\nThe distillation process involves three steps:\n\nFirst, generate training data using the teacher model. Run your inputs through GPT-4 or Claude Opus and collect both the outputs and (if available) the probability distributions.\n\nSecond, train the student model on this data. The student learns to mimic the teacher's behavior, including the subtle probability patterns, not just the final answers.\n\nThird, evaluate the student against a held-out test set. The quality gap between teacher and student is called the 'distillation gap.' A well-executed distillation achieves 85-95% of the teacher's quality.\n\nCommon distillation targets include moving from GPT-4 to GPT-4o-mini, from Claude Opus to a fine-tuned Haiku, or from any large model to an open-source model you can self-host.",
        "common_mistakes": [
            {
                "mistake": "Distilling on too little data, producing a student that memorizes examples rather than learning patterns",
                "correction": "Use at least 10,000-50,000 examples for distillation. More data produces better students. Quality matters too: ensure the teacher's outputs are diverse and representative."
            },
            {
                "mistake": "Comparing the student model to human performance rather than to the teacher model",
                "correction": "The student's ceiling is the teacher's performance. If GPT-4 achieves 93% accuracy on your task, a distilled model achieving 90% is excellent. Expecting it to exceed the teacher is unrealistic."
            },
            {
                "mistake": "Ignoring the tradeoff between model size and quality for your latency requirements",
                "correction": "Benchmark multiple student sizes. Sometimes a 3B model at 88% accuracy with 50ms latency beats a 7B model at 91% accuracy with 120ms latency. Let your application's latency budget guide the choice."
            }
        ],
        "career_relevance": "Distillation is a core MLOps and AI engineering skill. Companies hiring AI engineers expect candidates to understand when and how to distill large models into production-ready smaller models. It is the bridge between prototyping with expensive APIs and deploying cost-effective AI at scale.",
        "faqs": [
            {
                "question": "What is the difference between distillation and fine-tuning?",
                "answer": "Fine-tuning trains a model on task-specific data (human-labeled examples). Distillation trains a smaller model on a larger model's outputs. Distillation is a form of fine-tuning, but the training data comes from a model rather than from humans. You can combine both: fine-tune with human data, then distill."
            },
            {
                "question": "Is it legal to distill from commercial APIs like GPT-4?",
                "answer": "This depends on the provider's terms of service. As of 2026, OpenAI's terms restrict using API outputs to train competing models. Anthropic has similar restrictions. Always check current terms before distilling. Using outputs to train models for your own internal use is generally permitted."
            }
        ]
    },
    {
        "term": "RLHF",
        "slug": "what-is-rlhf",
        "full_name": "Reinforcement Learning from Human Feedback",
        "definition": "A training technique that improves language models by incorporating human preferences into the learning process. Humans rank model outputs from best to worst, a reward model learns these preferences, and then reinforcement learning adjusts the base model to generate outputs that align with what humans prefer.",
        "category": "Model Training",
        "related_terms": ["rlhf", "dpo", "fine-tuning", "ai-alignment", "instruction-tuning"],
        "related_links": [
            "/glossary/rlhf/",
            "/glossary/dpo/",
            "/glossary/fine-tuning/",
            "/glossary/ai-alignment/"
        ],
        "example": "A model generates two responses to 'Explain quantum computing.' Response A is technically accurate but dense and jargon-heavy. Response B is accurate and written clearly for a general audience. A human annotator ranks B above A. Thousands of such comparisons train a reward model, which then guides the base model to produce more responses like B.",
        "why_it_matters": "RLHF is the technique that transformed raw text-completion models into the helpful AI assistants we use today. ChatGPT, Claude, and Gemini all use RLHF (or its variants) to produce responses that are helpful, harmless, and honest. Without RLHF, language models would generate text that is statistically likely but not necessarily useful or safe.",
        "in_depth": "RLHF has three distinct stages:\n\nStage 1: Supervised Fine-Tuning (SFT). The base model is fine-tuned on a dataset of high-quality instruction-response pairs. This teaches the model to follow instructions rather than just complete text. The result is a model that can answer questions but without consistent quality or safety.\n\nStage 2: Reward Model Training. Human annotators compare pairs of model outputs and select which response is better. These preference pairs train a separate reward model that scores any model output on a quality scale. The reward model learns patterns like 'clear explanations score higher than jargon' and 'polite refusals score higher than harmful content.'\n\nStage 3: Reinforcement Learning. The SFT model generates responses, the reward model scores them, and Proximal Policy Optimization (PPO) adjusts the model's weights to maximize the reward score. Over millions of iterations, the model learns to produce responses that score highly according to human preferences.\n\nAlternatives to RLHF have emerged, notably Direct Preference Optimization (DPO), which skips the reward model entirely and optimizes preferences directly. DPO is simpler to implement but RLHF remains the most proven approach for flagship models.",
        "common_mistakes": [
            {
                "mistake": "Confusing RLHF with basic fine-tuning",
                "correction": "Fine-tuning teaches a model what to say. RLHF teaches a model how humans prefer it to say things. Fine-tuning uses labeled examples. RLHF uses human preference rankings over paired outputs."
            },
            {
                "mistake": "Assuming RLHF makes models factually accurate",
                "correction": "RLHF optimizes for human preference, not factual accuracy. A model can learn to produce confident, well-written, but factually wrong answers if annotators prefer confident tone. Grounding and RAG address accuracy separately."
            },
            {
                "mistake": "Thinking RLHF is a one-time training step",
                "correction": "Leading AI labs run RLHF continuously as they discover new failure modes and as user expectations evolve. It is an ongoing process of alignment, not a single training phase."
            }
        ],
        "career_relevance": "RLHF knowledge is essential for anyone working in AI alignment, model training, or AI safety. While few practitioners implement RLHF from scratch, understanding the process helps prompt engineers and AI product managers work with model behavior, predict failure modes, and design better evaluation criteria.",
        "faqs": [
            {
                "question": "What is the difference between RLHF and DPO?",
                "answer": "RLHF uses a three-stage process: SFT, reward model training, and reinforcement learning. DPO (Direct Preference Optimization) simplifies this to two stages by skipping the reward model and optimizing preferences directly. DPO is simpler and cheaper to implement. RLHF is more established and used by OpenAI and Anthropic for their flagship models."
            },
            {
                "question": "How many human annotators does RLHF require?",
                "answer": "Large-scale RLHF at companies like OpenAI and Anthropic uses hundreds to thousands of annotators. Smaller teams can use RLHF with as few as 5-10 annotators for domain-specific applications. The quality and consistency of annotations matters more than the quantity of annotators."
            }
        ]
    }
]


def main():
    # Append comparisons
    with open(COMP_FILE, 'r') as f:
        comparisons = json.load(f)

    existing_comp_slugs = {c['slug'] for c in comparisons}
    print(f"Existing comparisons: {len(comparisons)}")

    comp_added = 0
    for comp in NEW_COMPARISONS:
        if comp['slug'] in existing_comp_slugs:
            print(f"  SKIP (exists): {comp['slug']}")
        else:
            comparisons.append(comp)
            existing_comp_slugs.add(comp['slug'])
            print(f"  ADDED: {comp['slug']}")
            comp_added += 1

    with open(COMP_FILE, 'w') as f:
        json.dump(comparisons, f, indent=2)

    print(f"\nComparisons: Added {comp_added}. Total: {len(comparisons)}")

    # Append glossary terms
    with open(GLOSS_FILE, 'r') as f:
        glossary = json.load(f)

    existing_gloss_slugs = {t['slug'] for t in glossary}
    print(f"\nExisting glossary terms: {len(glossary)}")

    gloss_added = 0
    for term in NEW_GLOSSARY_TERMS:
        if term['slug'] in existing_gloss_slugs:
            print(f"  SKIP (exists): {term['slug']}")
        else:
            glossary.append(term)
            existing_gloss_slugs.add(term['slug'])
            print(f"  ADDED: {term['term']}")
            gloss_added += 1

    with open(GLOSS_FILE, 'w') as f:
        json.dump(glossary, f, indent=2)

    print(f"\nGlossary: Added {gloss_added}. Total: {len(glossary)}")
    print(f"\nTotal new pages: {comp_added + gloss_added}")


if __name__ == '__main__':
    main()
