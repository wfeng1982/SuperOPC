"""Installation and setup guide."""

# SuperOPC Installation Guide

## 🚀 Quick Start (5 minutes)

### 1. Prerequisites

```bash
# Python 3.11+
python --version

# UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Chrome/Chromium (for browser automation)
which chromium-browser  # or google-chrome
```

### 2. Install SuperOPC

```bash
# Clone repository
git clone https://github.com/wfeng1982/SuperOPC.git
cd SuperOPC

# Install dependencies
uv sync

# Optional: Install Playwright browsers
uv run playwright install chromium
```

### 3. Configure

```bash
# Copy example config
cp .env.example .env

# Edit as needed
nano .env
```

### 4. Start SuperOPC

```bash
# Development mode
uv run python -m superopc.main

# Or with debug logging
DEBUG=true uv run python -m superopc.main
```

Server runs at: **http://localhost:8000**

Visit:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🐳 Docker Installation

### Prerequisites

- Docker & Docker Compose
- 4GB+ RAM
- 5GB+ disk space (for models)

### Quick Start

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f superopc

# Stop services
docker compose down
```

Services:
- SuperOPC API: http://localhost:8000
- Ollama: http://localhost:11434

### Download Models

```bash
# Pull Mistral model (for Ollama)
docker compose exec ollama ollama pull mistral

# Or other models
docker compose exec ollama ollama pull llama2
docker compose exec ollama ollama pull neural-chat
```

### Custom Configuration

```bash
# Edit docker-compose.yml
nano docker-compose.yml

# Rebuild and restart
docker compose up -d --build
```

---

## 🛠️ Configuration

### Environment Variables (.env)

```bash
# Application
APP_NAME=SuperOPC
DEBUG=false                    # Enable debug logging

# Server
HOST=127.0.0.1
PORT=8000

# Workspace
WORKSPACE_ROOT=~/.superopc    # Where to store data

# Browser
BROWSER_PORT=12321
BROWSER_WS_PORT=22321
HEADLESS=true                 # Run browser without UI

# Database
DB_URL=sqlite:///superopc.db  # Or: postgresql://user:pass@host/db

# Models
DEFAULT_MODEL_PROVIDER=ollama
DEFAULT_MODEL_NAME=mistral
OLLAMA_BASE_URL=http://localhost:11434

# Logging
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR

# Features
ENABLE_BROWSER_AUTOMATION=true
ENABLE_RAG=true
ENABLE_SCHEDULING=true
```

### Using Remote LLM Provider

```bash
# OpenAI
DEFAULT_MODEL_PROVIDER=openai
DEFAULT_MODEL_NAME=gpt-4
OPENAI_API_KEY=sk-...

# DeepSeek
DEFAULT_MODEL_PROVIDER=deepseek
DEFAULT_MODEL_NAME=deepseek-chat
DEEPSEEK_API_KEY=...

# Anthropic
DEFAULT_MODEL_PROVIDER=anthropic
DEFAULT_MODEL_NAME=claude-3-opus
ANTHROPIC_API_KEY=...
```

---

## ✅ Verify Installation

```bash
# Check health
curl http://localhost:8000/health

# Get API info
curl http://localhost:8000/

# List providers
curl http://localhost:8000/api/models/providers
```

---

## 📦 Development Setup

### Install Dev Dependencies

```bash
uv sync --all-extras  # Includes dev dependencies
```

### Run Tests

```bash
# All tests
uv run pytest tests/ -v

# Specific test
uv run pytest tests/test_sandbox.py -v

# With coverage
uv run pytest tests/ --cov=superopc
```

### Code Quality

```bash
# Format code
uv run black superopc/

# Check style
uv run ruff check superopc/

# Type checking
uv run mypy superopc/
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Change port in .env
PORT=8001

# Or kill process
lsof -i :8000
kill -9 <PID>
```

### Playwright Not Installed

```bash
# Install browsers
uv run playwright install chromium

# Or full install
uv run playwright install
```

### Ollama Connection Failed

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve  # or `docker compose up ollama`

# Update OLLAMA_BASE_URL in .env if remote
OLLAMA_BASE_URL=http://192.168.1.100:11434
```

### Database Lock Error

```bash
# SQLite can't run concurrently
# Use PostgreSQL for multi-process setup
DB_URL=postgresql://user:password@localhost/superopc
```

### Permission Denied on Workspace

```bash
# Fix workspace permissions
chmod -R 755 ~/.superopc
chown -R $USER:$USER ~/.superopc
```

---

## 📚 Next Steps

1. **Create your first agent:**
   ```bash
   curl -X POST http://localhost:8000/api/agents \
     -H "Content-Type: application/json" \
     -d '{
       "agent_id": "my_bot_1",
       "name": "My Bot",
       "model_provider": "ollama",
       "model_name": "mistral"
     }'
   ```

2. **Read the docs:**
   - [Architecture Guide](docs/architecture.md)
   - [Skill Development](docs/skill_development.md)
   - [API Reference](docs/api.md)

3. **Run examples:**
   ```bash
   uv run python examples/basic_example.py
   ```

4. **Join community:**
   - GitHub Issues: Report bugs
   - GitHub Discussions: Ask questions

---

## 🆘 Getting Help

- **Documentation**: https://github.com/wfeng1982/SuperOPC/tree/main/docs
- **Examples**: https://github.com/wfeng1982/SuperOPC/tree/main/examples
- **Issues**: https://github.com/wfeng1982/SuperOPC/issues
- **Discussions**: https://github.com/wfeng1982/SuperOPC/discussions

---

## 🎉 You're Ready!

Start automating your e-commerce operations with SuperOPC!
