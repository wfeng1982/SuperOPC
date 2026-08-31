# SuperOPC 🚀

**SuperOPC** - Open-source AI Agent Platform for E-commerce & Marketing Automation

Combining the best of **VaneWorker** (enterprise-grade browser automation, strict sandbox isolation) with **ARGO** (flexible LLM integration, knowledge management), designed specifically for cross-border e-commerce and marketing automation.

## 🎯 Core Vision

SuperOPC is designed for **Personal Companies & SMBs** who need:
- ✅ Multi-account management (Amazon, eBay, Shopify, etc.) with strict data isolation
- ✅ Anti-bot detection & human-like behavior (防封控)
- ✅ Flexible AI model switching (local Ollama, OpenAI, DeepSeek, etc.)
- ✅ RAG-powered knowledge bases for business rules
- ✅ Scheduled workflows and multi-agent orchestration
- ✅ 100% local deployment, zero cloud dependency

## 🏗️ Architecture

```
SuperOPC/
├── core/                          # Core engine
│   ├── agent/                     # Agent runtime & lifecycle
│   ├── browser/                   # Browser automation daemon
│   ├── models/                    # LLM provider management
│   └── rag/                       # Knowledge base system
│
├── skills/                        # Pre-built skill modules
│   ├── ecommerce/                 # Amazon, eBay, Shopify
│   └── marketing/                 # Social media, email, analytics
│
├── gateway/                       # FastAPI HTTP/WebSocket server
├── scheduler/                     # Cron job management
├── storage/                       # Database & file isolation
├── ui/                            # Web dashboard + CLI
└── tests/                         # Comprehensive test suite
```

## 🌟 Key Features

### 1. **Physical Sandbox Isolation** (from VaneWorker)
- Each agent runs in isolated sandbox: `storage/agents/<agent-id>/`
- Independent SQLite databases per agent
- Separate skills, memories, and execution directories
- Zero cross-contamination between accounts

### 2. **Enterprise-Grade Browser Automation** (from VaneWorker)
- Chrome MV3 extension-based architecture
- 5-mode DOM snapshot system (quick/data/section/full/ax)
- Domain-level concurrency locking (prevent IP detection)
- Automatic CAPTCHA/login detection with human-in-the-loop
- Anti-bot rules: natural delays, user-agent rotation, rate limiting
- Structured action tracing with automatic redaction

### 3. **Flexible LLM Integration** (from ARGO)
- Support for local models: Ollama, Mistral, Llama
- Remote models: OpenAI, DeepSeek, Anthropic Claude
- One-command model downloads
- Seamless model switching mid-conversation
- OpenAI-compatible API

### 4. **Knowledge Management** (from ARGO)
- Local RAG knowledge bases
- Multiple input formats: files, folders, websites
- Dynamic folder synchronization
- Agentic RAG with intelligent decomposition
- Answer traceability to source

### 5. **Multi-Agent Orchestration** (from VaneWorker)
- Cron-based task scheduling
- Parallel & serial workflow execution
- Structured task logging
- Automatic retry with exponential backoff
- Human-in-the-loop for complex decisions

### 6. **Built-in Local API Gateway**
- FastAPI HTTP server
- WebSocket support for real-time updates
- OpenAI-compatible `/v1` endpoints
- Comprehensive REST API for agent management

## 📦 Quick Start

### Prerequisites
- Python 3.11+
- UV package manager
- Chrome/Chromium browser
- 4GB+ RAM (for model inference)

### Installation

```bash
# Clone repository
git clone https://github.com/wfeng1982/SuperOPC.git
cd SuperOPC

# Install dependencies
uv sync

# Start SuperOPC
uv run python -m superopc.main
```

## 📡 HTTP API

### Create Agent

```bash
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "amazon_us_1",
    "name": "Amazon US Bot",
    "model_provider": "ollama",
    "model_name": "mistral"
  }'
```

### Execute Skill

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "amazon_us_1",
    "skill": "amazon_search",
    "action": "search_products",
    "parameters": {"keyword": "laptop"}
  }'
```

## 📝 License

Apache License 2.0

## 🙌 Acknowledgments

- Inspired by [VaneWorker](https://github.com/huawolf/VaneWorker)
- Inspired by [ARGO](https://github.com/xark-argo/argo)
- Built on [Hermes Agent](https://github.com/NousResearch/hermes-agent)
