#!/usr/bin/env python3
"""Append new glossary terms to data/glossary.json."""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'glossary.json')

NEW_TERMS = [
    {
        "term": "Large Language Model",
        "slug": "large-language-model",
        "full_name": "Large Language Model (LLM)",
        "definition": "A neural network trained on massive text datasets that can understand and generate human language. LLMs like GPT-4, Claude, Gemini, and Llama contain billions of parameters and power chatbots, coding assistants, content generation, and AI agents. The \"large\" refers to both the training data (trillions of tokens) and the model size (billions to trillions of parameters).",
        "category": "Core Concepts",
        "related_terms": ["transformer", "tokens", "fine-tuning", "inference"],
        "related_links": ["/tools/", "/blog/prompt-engineering-guide/"],
        "example": "GPT-4 has an estimated 1.8 trillion parameters. Claude 3.5 Sonnet, Gemini 1.5 Pro, and Llama 3.1 405B are other prominent LLMs. Each excels at different tasks: Claude at long-context analysis, GPT-4 at broad reasoning, Gemini at multimodal input, and Llama at open-source deployment.",
        "why_it_matters": "LLMs are the foundation of the entire AI application stack. Every prompt engineering technique, RAG system, and AI agent ultimately depends on an LLM. Understanding their capabilities and limits is the starting point for any AI career."
    },
    {
        "term": "GPT",
        "slug": "gpt",
        "full_name": "Generative Pre-trained Transformer",
        "definition": "A family of large language models developed by OpenAI that generate text by predicting the next token in a sequence. GPT models are pre-trained on internet text (the 'pre-trained' part), use transformer architecture (the 'transformer' part), and produce new content token by token (the 'generative' part).",
        "category": "Core Concepts",
        "related_terms": ["large-language-model", "transformer", "tokens", "fine-tuning"],
        "related_links": ["/tools/"],
        "example": "GPT-3 (2020) had 175B parameters and introduced few-shot prompting. GPT-3.5 powered the original ChatGPT launch. GPT-4 (2023) added multimodal capabilities and significantly improved reasoning. GPT-4o (2024) unified text, vision, and audio in a single model.",
        "why_it_matters": "GPT is the model family that popularized prompt engineering as a discipline. Understanding GPT's architecture helps explain why techniques like chain-of-thought prompting and system prompts work, and why the field exists at all."
    },
    {
        "term": "Natural Language Processing",
        "slug": "natural-language-processing",
        "full_name": "Natural Language Processing (NLP)",
        "definition": "The branch of AI focused on enabling computers to understand, interpret, and generate human language. NLP encompasses everything from simple text classification and sentiment analysis to complex tasks like machine translation, question answering, and open-ended conversation.",
        "category": "Core Concepts",
        "related_terms": ["large-language-model", "transformer", "tokens", "embeddings"],
        "related_links": ["/blog/prompt-engineering-guide/"],
        "example": "Classic NLP tasks include named entity recognition (finding names, dates, locations in text), sentiment analysis (is this review positive or negative?), and text summarization. Modern LLMs handle all of these and more through prompting alone, replacing dozens of specialized NLP models.",
        "why_it_matters": "NLP is the broader field that prompt engineering sits within. Before LLMs, NLP required training separate models for each task. Prompt engineering collapsed that complexity into a single model that handles any language task with the right prompt."
    },
    {
        "term": "Model Context Protocol",
        "slug": "model-context-protocol",
        "full_name": "Model Context Protocol (MCP)",
        "definition": "An open standard developed by Anthropic that defines how AI models connect to external data sources and tools. MCP provides a universal interface for LLMs to access files, databases, APIs, and other resources without custom integration code for each data source.",
        "category": "Architecture Patterns",
        "related_terms": ["function-calling", "ai-agent", "tool-use"],
        "related_links": ["/tools/"],
        "example": "Instead of writing custom code to connect Claude to your Postgres database, Slack workspace, and GitHub repos, you configure MCP servers for each. The model uses the same protocol to query any of them. One integration pattern works for every data source.",
        "why_it_matters": "MCP is becoming the standard plumbing for AI applications. It eliminates the N-times-M integration problem (N models times M tools) by providing a single protocol. Job postings mentioning MCP have grown rapidly since its late 2024 release."
    },
    {
        "term": "Tool Use",
        "slug": "tool-use",
        "definition": "The capability of AI models to interact with external tools, APIs, and systems by generating structured requests during a conversation. Tool use extends LLMs beyond text generation into taking real-world actions like searching the web, running code, querying databases, or calling APIs.",
        "category": "Architecture Patterns",
        "related_terms": ["function-calling", "ai-agent", "model-context-protocol", "agentic-ai"],
        "related_links": ["/jobs/ai-agent-developer/"],
        "example": "A model with tool access receives 'What's the weather in Tokyo?' It generates a tool call to a weather API with parameters {location: 'Tokyo'}, receives the result (72F, partly cloudy), and incorporates that live data into its response. The model decided when and how to use the tool.",
        "why_it_matters": "Tool use transforms LLMs from knowledge bases into action-takers. It's the mechanism that makes AI agents possible and is required for building any production AI system that needs to interact with external data or services."
    },
    {
        "term": "JSON Mode",
        "slug": "json-mode",
        "definition": "A model configuration that constrains a language model to output only valid JSON. When enabled, the model's output is guaranteed to parse as valid JSON, eliminating the need for output validation or retry logic that handles malformed responses.",
        "category": "Prompting Techniques",
        "related_terms": ["structured-output", "function-calling", "prompt-engineering"],
        "related_links": ["/blog/prompt-engineering-best-practices/"],
        "example": "Without JSON mode, asking a model to 'return a JSON object with name and age' might produce markdown-wrapped JSON, extra text before/after the JSON, or invalid syntax. With JSON mode enabled, the output is always parseable: {\"name\": \"Alice\", \"age\": 30}.",
        "why_it_matters": "JSON mode solves one of the biggest pain points in production AI: unreliable output formatting. Before JSON mode, developers spent significant time on output parsing, validation, and retry logic. It's now a standard feature in OpenAI, Anthropic, and Google APIs."
    },
    {
        "term": "Structured Output",
        "slug": "structured-output",
        "definition": "Model responses that conform to a predefined schema or format, such as JSON matching a specific structure, XML, or typed data. Structured output goes beyond JSON mode by letting you define the exact fields, types, and constraints the model's response must follow.",
        "category": "Architecture Patterns",
        "related_terms": ["json-mode", "function-calling", "prompt-engineering"],
        "related_links": ["/blog/prompt-engineering-best-practices/"],
        "example": "You define a schema: {name: string, sentiment: 'positive' | 'negative' | 'neutral', confidence: number 0-1}. The model analyzes a product review and returns exactly that structure: {\"name\": \"iPhone 16\", \"sentiment\": \"positive\", \"confidence\": 0.87}. No extra fields, no missing fields.",
        "why_it_matters": "Structured output is essential for production AI pipelines. Any system that feeds model output into downstream code needs reliable, typed responses. It eliminates an entire class of runtime errors caused by unexpected model output formats."
    },
    {
        "term": "Streaming",
        "slug": "streaming",
        "definition": "A technique where model responses are delivered token by token as they're generated, rather than waiting for the complete response before displaying anything. Streaming shows text appearing in real-time, dramatically reducing perceived latency in chat interfaces and AI applications.",
        "category": "Infrastructure",
        "related_terms": ["inference", "latency", "tokens"],
        "related_links": [],
        "example": "Without streaming, a 500-word response that takes 8 seconds to generate shows nothing for 8 seconds, then the full text appears. With streaming, the first words appear within 200ms and text flows continuously. Same total time, but the experience feels 40x faster.",
        "why_it_matters": "Streaming is a non-negotiable feature for user-facing AI products. ChatGPT's typing effect is streaming in action. Understanding server-sent events (SSE) and streaming API integration is a core skill for anyone building AI interfaces."
    },
    {
        "term": "Batch Processing",
        "slug": "batch-processing",
        "definition": "Running multiple AI model requests as a group rather than one at a time. Batch processing trades latency for throughput and cost savings, processing hundreds or thousands of prompts in a single job at significantly reduced per-token pricing (typically 50% off).",
        "category": "Infrastructure",
        "related_terms": ["inference", "throughput", "tokens"],
        "related_links": [],
        "example": "Classifying 10,000 customer support tickets: instead of making 10,000 individual API calls at full price, you submit them as a batch job. OpenAI's Batch API processes them within 24 hours at 50% the normal cost. 10,000 tickets at $0.005 each = $25 instead of $50.",
        "why_it_matters": "Batch processing cuts AI costs in half for any workload that doesn't need real-time responses. Data processing, content generation, document analysis, and evaluation pipelines all benefit. It's the first optimization most teams implement at scale."
    },
    {
        "term": "Model Evaluation",
        "slug": "model-evaluation",
        "definition": "The systematic process of measuring how well an AI model performs on specific tasks. Model evaluation uses test datasets, automated metrics, and human judgment to assess accuracy, reliability, safety, and fitness for a particular use case before deployment.",
        "category": "Core Concepts",
        "related_terms": ["benchmarks", "mmlu", "humaneval", "fine-tuning"],
        "related_links": [],
        "example": "Evaluating a customer support chatbot involves: automated tests on 500 known question-answer pairs (accuracy), human reviewers scoring 100 responses (quality), red-team testing for prompt injection (safety), and A/B testing against the previous version (improvement).",
        "why_it_matters": "You can't improve what you can't measure. Model evaluation is how teams decide which model to use, whether a fine-tune worked, and when a system is ready for production. It's increasingly a dedicated role, with 'AI Evaluation Engineer' appearing in job boards."
    },
    {
        "term": "Benchmarks",
        "slug": "benchmarks",
        "definition": "Standardized tests used to compare AI model performance across specific capabilities. Benchmarks provide consistent evaluation criteria so different models can be ranked and compared fairly on tasks like reasoning, coding, math, and general knowledge.",
        "category": "Core Concepts",
        "related_terms": ["model-evaluation", "mmlu", "humaneval"],
        "related_links": [],
        "example": "Common AI benchmarks: MMLU (general knowledge across 57 subjects), HumanEval (Python coding), GSM8K (grade-school math), HellaSwag (commonsense reasoning), GPQA (graduate-level science). Model providers report scores on these to demonstrate capability.",
        "why_it_matters": "Benchmarks are the primary language for comparing models. When Anthropic says Claude scores 88.7% on MMLU or OpenAI reports GPT-4o scores 90.2% on HumanEval, benchmarks make those comparisons meaningful. Understanding them helps you cut through marketing claims."
    },
    {
        "term": "MMLU",
        "slug": "mmlu",
        "full_name": "Massive Multitask Language Understanding",
        "definition": "A benchmark that tests AI models across 57 academic subjects including math, history, law, medicine, and computer science. MMLU uses multiple-choice questions at difficulty levels ranging from elementary to professional, making it the most widely cited general-knowledge benchmark for LLMs.",
        "category": "Core Concepts",
        "related_terms": ["benchmarks", "model-evaluation", "humaneval"],
        "related_links": [],
        "example": "An MMLU question from professional medicine: 'A 45-year-old man presents with chest pain radiating to the left arm. Which of the following is the most appropriate initial diagnostic test? (A) CT scan (B) ECG (C) Chest X-ray (D) Blood culture.' The model must select the correct answer across thousands of such questions.",
        "why_it_matters": "MMLU is the benchmark that headlines most model launches. GPT-4 scored 86.4%, Claude 3.5 Sonnet hit 88.7%, and Gemini Ultra reached 90.0%. These numbers drive enterprise adoption decisions. When evaluating models for a project, MMLU scores provide the broadest capability comparison."
    },
    {
        "term": "HumanEval",
        "slug": "humaneval",
        "definition": "A coding benchmark created by OpenAI that tests AI models on 164 Python programming problems. Each problem provides a function signature and docstring; the model must generate working code that passes unit tests. HumanEval is the standard measure of LLM coding ability.",
        "category": "Core Concepts",
        "related_terms": ["benchmarks", "model-evaluation", "mmlu"],
        "related_links": ["/tools/"],
        "example": "A HumanEval problem: 'Write a function that takes a list of integers and returns the second-largest unique value.' The model generates Python code, which is then run against hidden test cases. A model scoring 90% means it solved 148 of 164 problems correctly on the first attempt.",
        "why_it_matters": "HumanEval scores directly predict how useful a model is as a coding assistant. If you're evaluating Cursor vs Copilot vs Claude for code generation, HumanEval (and its expanded version, HumanEval+) is the most relevant benchmark to check."
    },
    {
        "term": "Perplexity",
        "slug": "perplexity-metric",
        "full_name": "Perplexity (Evaluation Metric)",
        "definition": "A statistical measure of how well a language model predicts a sequence of text. Lower perplexity means the model is less \"surprised\" by the text, indicating better language understanding. Perplexity of 1.0 would mean perfect prediction; typical LLMs achieve perplexity of 5-20 on standard benchmarks.",
        "category": "Model Parameters",
        "related_terms": ["cross-entropy", "loss-function", "model-evaluation"],
        "related_links": [],
        "example": "A model with perplexity 10 on English text is, on average, choosing between 10 likely next tokens at each position. A model with perplexity 50 is far less confident. Comparing perplexity across models on the same test data shows which model has a better understanding of language patterns.",
        "why_it_matters": "Perplexity is the foundational metric for language model quality. While benchmarks like MMLU test specific capabilities, perplexity measures core language modeling ability. Lower perplexity generally correlates with better performance across all downstream tasks."
    },
    {
        "term": "Cross-Entropy",
        "slug": "cross-entropy",
        "definition": "A mathematical measure of the difference between a model's predicted probability distribution and the actual distribution of outcomes. In language models, cross-entropy loss measures how well the model predicts each next token. Lower cross-entropy means better predictions and a more capable model.",
        "category": "Model Parameters",
        "related_terms": ["perplexity-metric", "loss-function", "tokens"],
        "related_links": [],
        "example": "If the true next word is 'cat' and the model assigns 80% probability to 'cat,' the cross-entropy for that token is low (good prediction). If the model only assigns 5% to 'cat,' the cross-entropy is high (bad prediction). Training minimizes this across trillions of tokens.",
        "why_it_matters": "Cross-entropy is the objective function that LLMs are trained to minimize. Understanding it explains why models sometimes generate high-probability but incorrect text (hallucinations) and why temperature adjustments change output quality."
    },
    {
        "term": "Loss Function",
        "slug": "loss-function",
        "definition": "A mathematical function that measures how far a model's predictions are from the correct answers during training. The training process adjusts model weights to minimize this loss. For language models, the primary loss function is cross-entropy loss over next-token predictions.",
        "category": "Model Training",
        "related_terms": ["cross-entropy", "fine-tuning", "rlhf"],
        "related_links": [],
        "example": "During training, the model sees 'The capital of France is ___' and predicts a probability distribution over its vocabulary. The loss function compares this to the correct answer ('Paris') and produces a number. High loss means the model predicted poorly; the optimizer adjusts weights to reduce it.",
        "why_it_matters": "Loss functions determine what a model learns. The shift from pure cross-entropy to RLHF and DPO-based training objectives is what made models helpful and conversational instead of just good at text completion. Understanding loss helps you understand model behavior."
    },
    {
        "term": "Prompt Chaining",
        "slug": "prompt-chaining",
        "definition": "A technique where the output of one prompt becomes the input for the next, creating a sequential pipeline of AI operations. Each step in the chain handles a focused sub-task, producing more reliable results than attempting complex tasks in a single prompt.",
        "category": "Prompting Techniques",
        "related_terms": ["prompt-engineering", "chain-of-thought", "ai-agent"],
        "related_links": ["/blog/prompt-engineering-best-practices/"],
        "example": "Analyzing a legal contract in 3 chained steps: (1) 'Extract all obligations from this contract' -> list of obligations (2) 'Classify each obligation by risk level: high, medium, low' -> risk-tagged list (3) 'Write a summary memo of high-risk obligations for the legal team' -> final memo.",
        "why_it_matters": "Prompt chaining is how production AI systems handle complex tasks that a single prompt can't reliably solve. It's the manual predecessor to agentic AI. Designing effective chains is one of the most practically valuable prompt engineering skills."
    },
    {
        "term": "Prompt Template",
        "slug": "prompt-template",
        "definition": "A reusable prompt structure with placeholder variables that get filled in at runtime. Prompt templates separate the fixed instruction logic from the variable input data, making prompts maintainable, testable, and consistent across different inputs.",
        "category": "Prompting Techniques",
        "related_terms": ["prompt-engineering", "system-prompt", "prompt-optimization"],
        "related_links": ["/blog/prompt-engineering-best-practices/"],
        "example": "Template: 'You are a {role}. Analyze the following {document_type} and extract: {fields}. Format as JSON.' At runtime: role='financial analyst', document_type='earnings report', fields='revenue, profit margin, guidance'. Same template works for any document analysis task.",
        "why_it_matters": "Prompt templates are how teams scale prompt engineering beyond one-off experiments. They version-control prompts, enable A/B testing, and make it possible for non-technical team members to use AI systems without understanding prompt design."
    },
    {
        "term": "Prompt Optimization",
        "slug": "prompt-optimization",
        "definition": "The systematic process of improving prompt performance through testing, measurement, and iteration. Prompt optimization treats prompts as code: version-controlled, tested against evaluation datasets, and refined based on metrics rather than intuition.",
        "category": "Prompting Techniques",
        "related_terms": ["prompt-engineering", "prompt-template", "model-evaluation"],
        "related_links": ["/blog/prompt-engineering-best-practices/"],
        "example": "Testing 5 variations of a customer classification prompt against 200 labeled examples. Version A achieves 78% accuracy, Version B hits 84%, Version C reaches 91%. The winning prompt uses few-shot examples and explicit output constraints. Total cost of testing: $2 in API calls.",
        "why_it_matters": "Prompt optimization is where prompt engineering becomes engineering. Companies spending $10K+/month on API calls can cut costs 30-50% by optimizing prompt length and structure. It's the difference between hobby prompting and professional prompt engineering."
    },
    {
        "term": "AI Alignment",
        "slug": "ai-alignment",
        "definition": "The research and engineering challenge of ensuring AI systems behave in ways that are helpful, harmless, and consistent with human values and intentions. Alignment techniques include RLHF, constitutional AI, and red-teaming to prevent models from producing harmful, deceptive, or unintended outputs.",
        "category": "Core Concepts",
        "related_terms": ["rlhf", "constitutional-ai", "ai-safety", "guardrails"],
        "related_links": [],
        "example": "An aligned model, when asked how to pick a lock, explains the legitimate locksmithing profession and suggests calling a locksmith, rather than providing step-by-step instructions for breaking into homes. The model understands the intent behind safety guidelines, not just the rules.",
        "why_it_matters": "Alignment determines whether AI systems are trustworthy enough for real-world deployment. It's one of the most active research areas in AI, with dedicated teams at Anthropic, OpenAI, and DeepMind. Alignment research roles are among the highest-paid positions in AI."
    },
    {
        "term": "AI Safety",
        "slug": "ai-safety",
        "definition": "The field focused on preventing AI systems from causing unintended harm, both in current applications and as systems become more capable. AI safety covers technical problems (jailbreaking, prompt injection, hallucination), policy questions (regulation, liability), and longer-term concerns about increasingly autonomous systems.",
        "category": "Core Concepts",
        "related_terms": ["ai-alignment", "guardrails", "prompt-injection", "constitutional-ai"],
        "related_links": ["/blog/prompt-engineering-best-practices/"],
        "example": "Safety testing for a medical AI chatbot: Can it be tricked into giving dangerous medical advice? Does it appropriately refuse to diagnose conditions? Does it hallucinate drug interactions? Does it maintain accuracy across different demographics? Each of these is an AI safety concern.",
        "why_it_matters": "AI safety is becoming a regulatory requirement. The EU AI Act, Executive Orders on AI, and industry standards all mandate safety evaluations. Prompt engineers increasingly need safety expertise: designing red-team tests, building guardrails, and evaluating model behavior."
    },
    {
        "term": "Synthetic Data",
        "slug": "synthetic-data",
        "definition": "Artificially generated data created by AI models or algorithms rather than collected from real-world sources. Synthetic data is used to train, fine-tune, and evaluate AI models when real data is scarce, expensive, private, or biased. It can include text, images, tabular data, or any other format.",
        "category": "Model Training",
        "related_terms": ["fine-tuning", "model-evaluation", "knowledge-distillation"],
        "related_links": [],
        "example": "A company needs 50,000 labeled customer emails to train a classifier but only has 2,000. They use GPT-4 to generate 48,000 realistic synthetic emails across categories (complaint, inquiry, praise, return request), then train a smaller model on the combined dataset.",
        "why_it_matters": "Synthetic data is reshaping model training economics. Instead of spending months collecting and labeling data, teams generate training data in hours. Models like Llama 3 and Phi-3 used significant amounts of synthetic data in training. It's also a key tool for privacy-compliant AI development."
    },
    {
        "term": "Instruction Tuning",
        "slug": "instruction-tuning",
        "definition": "A fine-tuning technique where a pre-trained model is trained on a dataset of instruction-response pairs to improve its ability to follow human instructions. Instruction tuning is what transforms a raw text-completion model into a helpful assistant that can answer questions, follow directions, and complete tasks.",
        "category": "Model Training",
        "related_terms": ["fine-tuning", "rlhf", "large-language-model"],
        "related_links": [],
        "example": "A base model trained on web text will complete 'Write a haiku about coding:' with more text about haiku or coding. An instruction-tuned version understands this is a request and responds with an actual haiku. The tuning dataset contains thousands of instruction-response pairs demonstrating this behavior.",
        "why_it_matters": "Instruction tuning is the step that makes raw language models usable. Without it, GPT-4 would just autocomplete text instead of following directions. Understanding this process helps prompt engineers work with the grain of how models are trained to respond."
    },
    {
        "term": "Reasoning Models",
        "slug": "reasoning-models",
        "definition": "A category of AI models specifically designed to perform multi-step logical reasoning before producing a final answer. Reasoning models like OpenAI's o1 and o3, DeepSeek R1, and Claude's extended thinking mode use internal chain-of-thought processing to solve complex math, science, and coding problems that standard models struggle with.",
        "category": "Core Concepts",
        "related_terms": ["chain-of-thought", "large-language-model", "benchmarks"],
        "related_links": ["/tools/"],
        "example": "Given a complex math competition problem, a standard model might guess an answer. A reasoning model spends 30 seconds 'thinking,' working through the problem step by step internally, before producing a correct solution. The trade-off: slower responses but dramatically higher accuracy on hard problems.",
        "why_it_matters": "Reasoning models are changing which tasks AI can handle. They've achieved expert-level performance on PhD-level science questions and competitive programming. For prompt engineers, they require different techniques: simpler prompts often work better because the model handles the reasoning internally."
    },
    {
        "term": "AI Coding Assistant",
        "slug": "ai-coding-assistant",
        "definition": "Software tools that use AI models to help developers write, edit, debug, and understand code. AI coding assistants range from inline autocomplete (GitHub Copilot) to full IDE environments (Cursor, Windsurf) to terminal-based agents (Claude Code) that can execute multi-file changes autonomously.",
        "category": "Infrastructure",
        "related_terms": ["ai-agent", "large-language-model", "tool-use"],
        "related_links": ["/tools/cursor-vs-windsurf/", "/tools/cursor-vs-github-copilot/"],
        "example": "Cursor's AI coding assistant can: autocomplete code as you type, explain unfamiliar code, refactor functions across multiple files, generate tests, and fix bugs by reading error messages and modifying source code. It uses Claude or GPT-4 as the underlying model.",
        "why_it_matters": "AI coding assistants are the most widely adopted AI productivity tools, used by over 50% of professional developers. Understanding their capabilities and limits is essential for any AI professional. The market is fiercely competitive, with new tools launching monthly."
    }
]


def main():
    # Load existing terms
    with open(DATA_FILE, 'r') as f:
        existing = json.load(f)

    existing_slugs = {t['slug'] for t in existing}
    print(f"Existing terms: {len(existing)}")

    # Add new terms, skip duplicates
    added = 0
    skipped = 0
    for term in NEW_TERMS:
        if term['slug'] in existing_slugs:
            print(f"  SKIP (exists): {term['term']}")
            skipped += 1
        else:
            existing.append(term)
            existing_slugs.add(term['slug'])
            print(f"  ADDED: {term['term']}")
            added += 1

    # Write updated file
    with open(DATA_FILE, 'w') as f:
        json.dump(existing, f, indent=2)

    print(f"\nDone! Added {added} terms, skipped {skipped} duplicates.")
    print(f"Total glossary terms: {len(existing)}")


if __name__ == '__main__':
    main()
