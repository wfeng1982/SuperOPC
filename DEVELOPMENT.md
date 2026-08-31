# SuperOPC Development Guide

## 🏗️ Project Structure

SuperOPC is organized into modular components:

```
superopc/
├── core/                  # Core systems
│   ├── agent/            # Agent sandbox isolation
│   ├── browser/          # Browser automation
│   ├── models/           # LLM integration
│   └── rag/              # Knowledge bases
├── skills/               # Automation skills
│   ├── ecommerce/
│   ├── marketing/
│   └── base.py           # Skill interface
├── gateway/              # HTTP API
├── scheduler/            # Task scheduling
├── utils/                # Utilities
└── config.py             # Configuration
```

## 🚀 Getting Started

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/wfeng1982/SuperOPC.git
cd SuperOPC

# Install UV (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Start development server
uv run python -m superopc.main
```

Server runs at: `http://localhost:8000`

### Using Docker

```bash
# Build image
docker build -t superopc:latest .

# Run with Docker Compose
docker compose up -d

# View logs
docker compose logs -f superopc
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/

# Run specific test file
uv run pytest tests/test_sandbox.py -v

# Run with coverage
uv run pytest tests/ --cov=superopc --cov-report=html
```

## 📝 Code Style

```bash
# Format code
uv run black superopc/

# Check style
uv run ruff check superopc/

# Type checking
uv run mypy superopc/
```

## 🔧 Development Workflow

### Adding a New Skill

1. Create skill file: `superopc/skills/category/my_skill.py`
2. Inherit from `BaseSkill`
3. Implement `execute()` method
4. Add tests in `tests/test_my_skill.py`
5. Update `__init__.py`

### Adding a New API Endpoint

1. Create route file: `superopc/gateway/routes/my_route.py`
2. Define FastAPI router
3. Add to `superopc/gateway/app.py`
4. Document in `docs/api.md`

### Adding a New Core Module

1. Create module: `superopc/core/my_module/`
2. Implement module logic
3. Add to `superopc/core/__init__.py`
4. Create tests: `tests/test_my_module.py`
5. Document in `docs/architecture.md`

## 🐛 Debugging

### Enable Debug Mode

```bash
DEBUG=true uv run python -m superopc.main
```

### View Logs

```bash
# All logs
tail -f ~/.superopc/logs/superopc.log

# Error logs only
tail -f ~/.superopc/logs/errors.log

# Agent-specific logs
tail -f ~/.superopc/agents/agent_id/logs/*.log
```

### Interactive Development

```bash
# Start Python REPL
uv run ipython

# Import and test
from superopc.core.agent.manager import AgentManager
from pathlib import Path

manager = AgentManager(Path("/tmp/test"))
agent = manager.create_agent("test", {})
print(agent.get_info())
```

## 📚 Documentation

- [Architecture Guide](docs/architecture.md)
- [Browser Automation](docs/browser_guide.md)
- [Skill Development](docs/skill_development.md)
- [API Reference](docs/api.md)

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and test
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature/my-feature`
6. Create Pull Request

## 📋 Development Checklist

Before submitting PR:
- [ ] Code passes `ruff check`
- [ ] Code formatted with `black`
- [ ] Type checking passes with `mypy`
- [ ] All tests pass with `pytest`
- [ ] Documentation updated
- [ ] No hardcoded credentials
- [ ] Logs use `logger` instead of `print`

## 🎯 Current Development Focus

**Phase 1 (MVP - Current):**
- ✅ Agent sandbox isolation
- ✅ Basic browser automation
- ✅ HTTP API gateway
- ✅ Task scheduling
- 🔄 Amazon skill
- 🔄 Documentation

**Phase 2 (Next):**
- [ ] Chrome MV3 extension
- [ ] Full DOM snapshot system
- [ ] WebSocket support
- [ ] RAG implementation
- [ ] eBay, Shopify skills
- [ ] CLI interface

**Phase 3 (Future):**
- [ ] Web dashboard
- [ ] Multi-node deployment
- [ ] Advanced analytics
- [ ] Plugin system

## 🐛 Known Issues

- None currently (project is in early development)

## 📞 Support

- GitHub Issues: Report bugs
- GitHub Discussions: Ask questions
- Documentation: Read guides

## 📄 License

Apache 2.0 - See LICENSE file
