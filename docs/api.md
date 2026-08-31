# API Reference

## Overview

SuperOPC provides a RESTful API for all operations. Base URL: `http://localhost:8000`

## 📋 Agent Endpoints

### Create Agent

**POST** `/api/agents`

```json
{
  "agent_id": "amazon_us_1",
  "name": "Amazon US Bot",
  "model_provider": "ollama",
  "model_name": "mistral",
  "skills": ["amazon_search", "amazon_details"]
}
```

**Response:**
```json
{
  "agent_id": "amazon_us_1",
  "status": "created",
  "sandbox": {
    "agent_id": "amazon_us_1",
    "sandbox_dir": "/home/user/.superopc/agents/amazon_us_1",
    "db_path": "/home/user/.superopc/agents/amazon_us_1/state.db",
    "skills_dir": "/home/user/.superopc/agents/amazon_us_1/skills",
    "data_dir": "/home/user/.superopc/agents/amazon_us_1/data"
  }
}
```

### Get Agent

**GET** `/api/agents/{agent_id}`

**Response:**
```json
{
  "id": "amazon_us_1",
  "config": {
    "name": "Amazon US Bot",
    "model_provider": "ollama",
    "skills": [...]
  },
  "sandbox": {...}
}
```

### List Agents

**GET** `/api/agents`

**Response:**
```json
{
  "agents": {
    "amazon_us_1": {...},
    "ebay_uk_1": {...}
  }
}
```

### Delete Agent

**DELETE** `/api/agents/{agent_id}`

**Response:**
```json
{
  "status": "deleted",
  "agent_id": "amazon_us_1"
}
```

## 🌐 Browser Endpoints

### Create Session

**POST** `/api/browser/sessions`

```json
{
  "session_id": "search_001",
  "agent_id": "amazon_us_1"
}
```

**Response:**
```json
{
  "session_id": "search_001",
  "status": "created"
}
```

### List Sessions

**GET** `/api/browser/sessions`

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "search_001",
      "agent_id": "amazon_us_1",
      "state": "initialized",
      "created_at": "2026-08-31T07:28:00",
      "locked_domains": ["amazon.com"]
    }
  ]
}
```

### Acquire Lock

**POST** `/api/browser/sessions/{session_id}/lock`

```json
{
  "domains": ["amazon.com"],
  "concurrency_policy": "domain"
}
```

**Response:**
```json
{
  "session_id": "search_001",
  "acquired": true,
  "domains": ["amazon.com"]
}
```

### Release Lock

**POST** `/api/browser/sessions/{session_id}/unlock`

**Query Parameters:**
- `close_browser` (bool, default: false) - Whether to close browser

**Response:**
```json
{
  "session_id": "search_001",
  "status": "unlocked"
}
```

### Close Session

**DELETE** `/api/browser/sessions/{session_id}`

**Response:**
```json
{
  "status": "closed",
  "session_id": "search_001"
}
```

## 🤖 Model Endpoints

### List Providers

**GET** `/api/models/providers`

**Response:**
```json
{
  "providers": ["ollama", "openai", "deepseek", "anthropic"]
}
```

### List Models

**GET** `/api/models/providers/{provider}/models`

**Response:**
```json
{
  "provider": "ollama",
  "models": ["mistral", "llama2", "neural-chat"]
}
```

## 🏥 Health Endpoints

### Health Check

**GET** `/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-08-31T07:28:00"
}
```

### Root

**GET** `/`

**Response:**
```json
{
  "name": "SuperOPC",
  "version": "0.1.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

## 📊 Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Agent not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## 🔗 WebSocket Endpoints

WebSocket support for real-time updates coming in Phase 2.

## 📚 SDK Examples

### Python SDK

```python
import httpx
import asyncio

class SuperOPCClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def create_agent(self, agent_id: str, config: dict):
        response = await self.client.post(
            f"{self.base_url}/api/agents",
            json={**config, "agent_id": agent_id}
        )
        return response.json()
    
    async def create_session(self, session_id: str, agent_id: str):
        response = await self.client.post(
            f"{self.base_url}/api/browser/sessions",
            json={"session_id": session_id, "agent_id": agent_id}
        )
        return response.json()

# Usage
async def main():
    client = SuperOPCClient()
    
    # Create agent
    agent = await client.create_agent(
        "amazon_us_1",
        {"name": "Amazon Bot", "model_provider": "ollama"}
    )
    print(agent)
    
    # Create session
    session = await client.create_session("search_001", "amazon_us_1")
    print(session)

asyncio.run(main())
```

### cURL Examples

```bash
# Create agent
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "amazon_us_1",
    "name": "Amazon Bot",
    "model_provider": "ollama"
  }'

# List agents
curl http://localhost:8000/api/agents

# Create session
curl -X POST http://localhost:8000/api/browser/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "search_001",
    "agent_id": "amazon_us_1"
  }'

# Acquire lock
curl -X POST http://localhost:8000/api/browser/sessions/search_001/lock \
  -H "Content-Type: application/json" \
  -d '{
    "domains": ["amazon.com"],
    "concurrency_policy": "domain"
  }'
```
