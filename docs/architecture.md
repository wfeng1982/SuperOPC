# SuperOPC Architecture Guide

## 📋 System Overview

SuperOPC combines three core subsystems:

1. **Agent Sandbox System** - Physical isolation for multi-account management
2. **Browser Automation Engine** - Enterprise-grade web automation with anti-bot
3. **LLM Integration Layer** - Flexible model switching and orchestration

## 🏗️ Core Components

### Agent Sandbox Architecture

```
workspace/
├── agents/
│   ├── agent_id_1/
│   │   ├── state.db              # Isolated SQLite database
│   │   ├── skills/               # Agent-specific skills
│   │   ├── sandboxes/            # Execution directories
│   │   ├── memories/             # Agent memories & knowledge
│   │   └── logs/                 # Agent-specific logs
│   │
│   └── agent_id_2/
│       └── ... (same structure)
```

**Key Features:**
- Each agent has its own SQLite database (`state.db`)
- Isolated skills directory prevents cross-agent pollution
- Independent execution sandboxes
- Separate logging for audit trails

### Browser Automation Architecture

```
BrowserWorker (Daemon)
├── HTTP Server (:12321)
│   ├── Session Management
│   ├── Lock Management
│   ├── Action Execution
│   └── Snapshot API
│
└── Chrome Extension (MV3)
    ├── WebSocket Transport (:22321)
    ├── DOM Snapshot Engine
    ├── Anti-bot Simulation
    └── Page State Detection
```

**Anti-Bot Features:**
- Domain-level concurrency locking
- Natural delay simulation (Jitter)
- User-Agent rotation
- Rate limiting per domain
- Human-in-the-loop for CAPTCHA/Login

### LLM Provider Architecture

```
ModelProvider
├── Local Models (Ollama)
│   └── HTTP: localhost:11434
├── Remote Models (OpenAI)
│   └── HTTPS: api.openai.com
├── Remote Models (DeepSeek)
│   └── HTTPS: api.deepseek.com
└── Remote Models (Anthropic)
    └── HTTPS: api.anthropic.com
```

## 🔄 Request Flow

### Creating a Multi-Account Bot

```
1. User creates Agent A
   ↓
   AgentManager.create_agent("amazon_bot")
   ↓
   AgentSandbox initialized at workspace/agents/amazon_bot/
   ↓
   SQLite DB created at workspace/agents/amazon_bot/state.db
   ↓
   ✅ Agent A ready

2. User creates Agent B (completely isolated from A)
   ↓
   AgentManager.create_agent("ebay_bot")
   ↓
   AgentSandbox initialized at workspace/agents/ebay_bot/ (different)
   ↓
   SQLite DB created at workspace/agents/ebay_bot/state.db (different)
   ↓
   ✅ Agent B ready (zero cross-contamination)
```

### Browser Automation Flow

```
1. Agent executes search skill
   ↓
   BrowserManager.create_session("session_1", "amazon_bot")
   ↓
   Session locked to domain="amazon.com"

2. Search execution
   ↓
   Navigate to Amazon
   ↓
   Take DOM snapshot (quick/data/section/full/ax mode)
   ↓
   Extract data from snapshot (uses semantic keys, not CSS)
   ↓
   Detect page state (ok/login/captcha/blocked)

3. If CAPTCHA detected
   ↓
   Request human intervention
   ↓
   Wait for user to complete CAPTCHA
   ↓
   Resume automation

4. Release locks
   ↓
   Keep browser open for manual verification
   ↓
   ✅ Task complete
```

## 🎯 Data Flow Diagram

```
┌─────────────────┐
│   FastAPI       │
│   HTTP Server   │
└────────┬────────┘
         │
    ┌────┴────────────────┬──────────────┐
    │                     │              │
┌───▼────────┐    ┌──────▼──────┐  ┌───▼──────────┐
│ Agent       │    │ Browser     │  │ Model        │
│ Manager     │    │ Manager     │  │ Provider     │
└───┬────────┘    └──────┬──────┘  └───┬──────────┘
    │                     │              │
    │ creates isolates    │              │
    │                     │ manages      │
┌───▼─────────────┐    ┌──▼─────────┐   │
│ AgentSandbox    │    │ Browser     │   │
│ ├─ state.db     │    │ Sessions    │   │
│ ├─ skills/      │    │ ├─ Locking  │   │
│ ├─ data/        │    │ ├─ Snapshots│   │ queries
│ └─ logs/        │    │ └─ Anti-bot │   │
└────────────────┘    └─────────────┘   │
                                         │
                                    ┌────▼──────┐
                                    │ LLM APIs   │
                                    │ Ollama     │
                                    │ OpenAI     │
                                    │ DeepSeek   │
                                    └───────────┘
```

## 🔐 Security Model

### Isolation Levels

**Level 1: Database Isolation**
- Each agent has separate SQLite database
- No shared tables across agents
- Separate transaction contexts

**Level 2: Filesystem Isolation**
- Separate skill directories
- Separate execution sandboxes
- Separate memory/data storage

**Level 3: Process Isolation**
- Each agent can run in separate thread/process
- Environment variables scoped per agent
- Working directory isolated per agent

**Level 4: Network Isolation**
- Domain-level locking (one domain = one session at a time)
- Rate limiting per domain
- Separate browser profiles per agent

### Credential Management

```
Credentials Flow:
1. User provides credentials via API
2. Credentials encrypted with agent-specific key
3. Stored in agent sandbox database
4. Never written to logs
5. Auto-redacted in audit trails
```

## 📊 Database Schema

### Sessions Table
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    data JSON
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    skill TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    result JSON,
    error TEXT
);
```

### Browser Logs Table
```sql
CREATE TABLE browser_logs (
    id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    action TEXT NOT NULL,
    url TEXT,
    status TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP
);
```

## 🚀 Scaling Considerations

### Single Machine (MVP)
- All agents on one workspace
- SQLite for storage
- Local browser automation
- Single FastAPI instance

### Multi-Machine (Production)
- Distributed workspace (NFS/S3)
- PostgreSQL for shared data
- Remote browser nodes
- Load-balanced FastAPI (Nginx)
- Celery/RabbitMQ for task queue

### Cloud Deployment
- Agent sandboxes in containers
- Kubernetes orchestration
- Cloud storage (S3, GCS)
- Managed databases (RDS, CloudSQL)
- Serverless browser (Browserless, BrowserStack)

## 📈 Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Agent creation | <100ms | Just creates directories |
| Skill execution | 1-30s | Depends on website |
| DOM snapshot | 100-500ms | Varies by page complexity |
| Lock acquire | <10ms | In-memory operation |
| DB query | 1-10ms | SQLite on local SSD |

## 🔍 Monitoring & Debugging

### Logging
- Central logs in `workspace/logs/`
- Agent-specific logs in `workspace/agents/<id>/logs/`
- Structured JSONL format for easy parsing

### Metrics to Track
- Agent count & active sessions
- Task success/failure rates
- Average task duration
- Domain lock contention
- Model provider latency

### Debug Mode
- Enable with `DEBUG=true` in `.env`
- Captures detailed browser snapshots
- Keeps browser windows open
- Verbose logging

## 🔗 Extension Points

### Adding New Skills
1. Create skill in `superopc/skills/<category>/`
2. Inherit from `BaseSkill`
3. Implement `execute()` method
4. Register in agent config

### Adding New Providers
1. Create provider in `superopc/core/models/`
2. Implement `ModelProvider` interface
3. Add to `load_providers()` in manager
4. Test with sample models

### Custom Database Backends
1. Implement `StorageBackend` interface
2. Replace in `AgentSandbox.__init__()`
3. Support PostgreSQL, MongoDB, etc.
