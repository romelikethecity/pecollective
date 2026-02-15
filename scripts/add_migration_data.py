#!/usr/bin/env python3
"""Add migration guidance and date_updated to all comparisons."""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'comparisons.json')

MIGRATION_DATA = {
    "cursor-vs-windsurf": {
        "date_updated": "February 15, 2026",
        "migration": {
            "what_transfers": [
                "VS Code extensions (both are VS Code forks, most extensions work in either)",
                "Keyboard shortcuts and keybindings (same base editor)",
                "Workspace settings and project configurations",
                "Git integration and terminal workflows"
            ],
            "what_needs_reconfiguration": [
                "AI chat history and saved conversations (not portable)",
                "Custom AI rules and prompt configurations (different formats)",
                "Subscription and billing (separate accounts)",
                "Codebase indexing (needs to re-index your project)"
            ],
            "time_estimate": "About 30 minutes. Install the new editor, open your project, let it index, and reconfigure your AI preferences. Your code, git history, and extensions carry over immediately."
        }
    },
    "langchain-vs-llamaindex": {
        "date_updated": "February 15, 2026",
        "migration": {
            "what_transfers": [
                "Your data sources and documents (both use standard file formats)",
                "Embedding vectors (model-dependent, not framework-dependent)",
                "Vector database connections (both support Pinecone, Weaviate, Chroma, etc.)",
                "LLM API keys and model configurations"
            ],
            "what_needs_reconfiguration": [
                "Chain/pipeline logic (completely different APIs and abstractions)",
                "Agent configurations (LangGraph vs LlamaIndex agents)",
                "Retrieval strategies (different chunking, indexing, and query approaches)",
                "Observability setup (LangSmith vs LlamaCloud monitoring)"
            ],
            "time_estimate": "1-3 days for a typical RAG application. The data pipeline stays the same, but you'll rewrite the orchestration layer. Budget extra time if migrating complex agent workflows."
        }
    },
    "pinecone-vs-weaviate": {
        "date_updated": "February 15, 2026",
        "migration": {
            "what_transfers": [
                "Embedding vectors (export from one, import to the other)",
                "Metadata and filtering logic (both support metadata-based filtering)",
                "Embedding model configuration (vectors are model-dependent, not DB-dependent)",
                "Application-level query logic (search patterns are similar)"
            ],
            "what_needs_reconfiguration": [
                "Client SDK code (different APIs: Pinecone SDK vs Weaviate client)",
                "Index/collection configuration (namespaces vs classes/collections)",
                "Query syntax (REST/gRPC vs GraphQL)",
                "Deployment infrastructure (serverless vs self-hosted considerations)"
            ],
            "time_estimate": "A few hours for re-indexing plus 1-2 days for client code changes. The vectors themselves transfer directly. Plan for re-indexing time proportional to your dataset size."
        }
    },
    "claude-vs-chatgpt-coding": {
        "date_updated": "February 15, 2026",
        "migration": {
            "what_transfers": [
                "Prompt templates and system prompts (both use similar formats)",
                "API integration patterns (both offer REST APIs with comparable structures)",
                "General workflow patterns (chat-based coding, paste-and-ask, etc.)",
                "Conversation strategies (chain-of-thought, few-shot examples work in both)"
            ],
            "what_needs_reconfiguration": [
                "API client code (different SDKs: anthropic vs openai packages)",
                "Function/tool calling syntax (different JSON schema formats)",
                "Rate limiting and error handling (different thresholds and error codes)",
                "Streaming response parsers (slightly different SSE formats)",
                "Token counting (different tokenizers, so budget estimates change)"
            ],
            "time_estimate": "2-4 hours for API client swaps. 1-2 days to tune prompts for optimal results on the new model, since each model responds differently to the same instructions."
        }
    },
    "copilot-vs-codewhisperer": {
        "date_updated": "February 15, 2026",
        "migration": {
            "what_transfers": [
                "IDE setup (both support VS Code and JetBrains)",
                "Your codebase and project configuration",
                "Git workflow and version control setup",
                "General coding habits and AI interaction patterns"
            ],
            "what_needs_reconfiguration": [
                "Extension/plugin installation (uninstall one, install the other)",
                "Authentication (GitHub account vs AWS account)",
                "AI behavior preferences and custom instructions",
                "Code review and security scanning workflows (different feature sets)",
                "Team/organization settings (different admin consoles)"
            ],
            "time_estimate": "Under 30 minutes. Uninstall the old extension, install the new one, authenticate, and start coding. The learning curve is the bigger time investment: 1-2 weeks to get comfortable with the new tool's strengths."
        }
    }
}

def main():
    with open(DATA_FILE, 'r') as f:
        comparisons = json.load(f)

    updated = 0
    for comp in comparisons:
        slug = comp['slug']
        if slug in MIGRATION_DATA:
            data = MIGRATION_DATA[slug]
            comp['date_updated'] = data['date_updated']
            comp['migration'] = data['migration']
            updated += 1
            print(f"  Updated: {slug}")

    with open(DATA_FILE, 'w') as f:
        json.dump(comparisons, f, indent=2, ensure_ascii=False)

    print(f"\nUpdated {updated} comparisons with migration guidance and dates")

if __name__ == '__main__':
    main()
