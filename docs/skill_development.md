# Skill Development Guide

## 📚 Overview

Skills are reusable automation modules that agents execute. Each skill can:
- Access browser automation
- Query LLM models
- Store data in agent sandbox
- Interact with external APIs

## 🏗️ Skill Architecture

```python
from superopc.skills.base import BaseSkill
from superopc.core.browser import BrowserManager
from superopc.core.models import ModelProvider

class MySkill(BaseSkill):
    """My custom skill."""
    
    name = "my_skill"
    description = "Description of what this skill does"
    version = "1.0.0"
    
    def __init__(
        self,
        browser_manager: BrowserManager,
        model_provider: ModelProvider,
        sandbox
    ):
        self.browser = browser_manager
        self.models = model_provider
        self.sandbox = sandbox
    
    async def execute(self, action: str, **params):
        """Execute skill action."""
        if action == "my_action":
            return await self.my_action(**params)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def my_action(self, **params):
        """Implementation of my_action."""
        pass
```

## 🎯 Creating E-commerce Skills

### Amazon Search Skill

```python
from superopc.skills.base import BaseSkill
import time
import random

class AmazonSearchSkill(BaseSkill):
    name = "amazon_search"
    description = "Search products on Amazon"
    
    async def execute(self, action: str, **params):
        if action == "search":
            return await self.search_products(**params)
        elif action == "get_details":
            return await self.get_product_details(**params)
    
    async def search_products(self, keyword: str, max_results: int = 20):
        """Search for products on Amazon."""
        
        # Create session
        session = await self.browser.create_session(
            session_id=f"amazon_search_{int(time.time())}",
            agent_id=self.sandbox.agent_id
        )
        
        try:
            # Acquire domain lock
            await session.acquire_lock(["amazon.com"])
            
            # Navigate to Amazon
            await session.goto("https://amazon.com")
            
            # Detect page state
            state = await session.detect_page_state()
            if state["state"] != "ok":
                if state["state"] == "captcha":
                    await session.request_help(
                        "Complete Amazon CAPTCHA",
                        "Please solve the CAPTCHA",
                        timeout_ms=300000
                    )
                else:
                    return {"error": state["state"]}
            
            # Take snapshot to find search box
            snapshot = await session.snapshot(mode="quick")
            search_box = next(
                (item for item in snapshot["items"]
                 if item.get("semantic_key") == "search.input"),
                None
            )
            
            if not search_box:
                return {"error": "Search box not found"}
            
            # Type keyword with anti-bot delay
            await session.fill(search_box["handle"], keyword)
            await asyncio.sleep(random.uniform(0.5, 1.5))  # Natural delay
            
            # Click search button
            snapshot = await session.snapshot(mode="quick")
            search_btn = next(
                (item for item in snapshot["items"]
                 if item.get("semantic_key") == "search.submit"),
                None
            )
            
            if search_btn:
                await session.click(search_btn["handle"])
            
            # Wait for results
            await asyncio.sleep(2)
            
            # Get product data
            snapshot = await session.snapshot(mode="data")
            
            products = []
            for item in snapshot["items"][:max_results]:
                product = {
                    "title": item.get("text", ""),
                    "price": item.get("price", ""),
                    "rating": item.get("rating", ""),
                    "reviews": item.get("review_count", ""),
                    "url": item.get("url", ""),
                    "handle": item.get("handle")
                }
                products.append(product)
            
            # Store results in sandbox
            conn = self.sandbox.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO search_results (keyword, results_json, created_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (keyword, json.dumps(products)))
            conn.commit()
            conn.close()
            
            return {"success": True, "products": products}
        
        finally:
            await session.release_lock(close_browser=False)
    
    async def get_product_details(self, product_url: str):
        """Get detailed product information."""
        session = await self.browser.create_session(
            session_id=f"amazon_detail_{int(time.time())}",
            agent_id=self.sandbox.agent_id
        )
        
        try:
            await session.acquire_lock(["amazon.com"])
            await session.goto(product_url)
            
            state = await session.detect_page_state()
            if state["state"] != "ok":
                return {"error": state["state"]}
            
            snapshot = await session.snapshot(mode="full")
            
            details = {
                "title": self._extract_by_semantic(snapshot, "product.title"),
                "price": self._extract_by_semantic(snapshot, "product.price"),
                "rating": self._extract_by_semantic(snapshot, "product.rating"),
                "reviews": self._extract_by_semantic(snapshot, "product.reviews"),
                "description": self._extract_by_semantic(snapshot, "product.description"),
                "availability": self._extract_by_semantic(snapshot, "product.availability"),
            }
            
            return {"success": True, "details": details}
        
        finally:
            await session.release_lock()
    
    def _extract_by_semantic(self, snapshot, semantic_key):
        """Extract data by semantic key."""
        for item in snapshot["items"]:
            if item.get("semantic_key") == semantic_key:
                return item.get("text") or item.get("value")
        return None
```

## 🧠 Using LLM in Skills

```python
class AnalysisSkill(BaseSkill):
    name = "analysis"
    
    async def execute(self, action: str, **params):
        if action == "analyze_products":
            return await self.analyze_products(**params)
    
    async def analyze_products(self, products: list):
        """Use LLM to analyze products."""
        
        # Prepare context
        product_list = "\n".join([
            f"- {p['title']}: ${p['price']} (Rating: {p['rating']}/5)"
            for p in products
        ])
        
        messages = [
            {
                "role": "system",
                "content": "You are a product analyst. Analyze products and provide insights."
            },
            {
                "role": "user",
                "content": f"Analyze these products:\n{product_list}\n\nIdentify the best deals."
            }
        ]
        
        # Query LLM
        response = await self.models.chat(
            provider="ollama",
            model="mistral",
            messages=messages,
            temperature=0.7
        )
        
        return {"analysis": response}
```

## 📦 Skill Directory Structure

```
superopc/skills/
├── base.py                    # BaseSkill class
├── ecommerce/
│   ├── __init__.py
│   ├── amazon.py             # Amazon skill
│   ├── ebay.py               # eBay skill
│   └── shopify.py            # Shopify skill
├── marketing/
│   ├── __init__.py
│   ├── social_media.py       # Social media posting
│   ├── email.py              # Email campaigns
│   └── analytics.py          # Analytics tracking
└── utils/
    ├── __init__.py
    ├── extractors.py         # Data extraction utilities
    └── validators.py         # Data validation
```

## 🧪 Testing Skills

```python
import pytest

@pytest.mark.asyncio
async def test_amazon_search():
    """Test Amazon search skill."""
    
    # Setup
    manager = AgentManager(Path("/tmp/test"))
    sandbox = manager.create_agent("test_agent", {})
    
    browser = BrowserManager()
    models = ModelProvider()
    
    skill = AmazonSearchSkill(browser, models, sandbox)
    
    # Execute
    result = await skill.execute(
        "search",
        keyword="laptop",
        max_results=10
    )
    
    # Assert
    assert result["success"] is True
    assert len(result["products"]) > 0
    assert "title" in result["products"][0]
```

## 🔌 Registering Skills

```python
# In agent config
config = {
    "agent_id": "amazon_bot",
    "name": "Amazon Bot",
    "skills": [
        {
            "name": "amazon_search",
            "module": "superopc.skills.ecommerce.amazon",
            "class": "AmazonSearchSkill",
            "config": {}
        },
        {
            "name": "analysis",
            "module": "superopc.skills.analysis",
            "class": "AnalysisSkill",
            "config": {"model": "mistral"}
        }
    ]
}
```

## 📖 Skill Template

```python
from superopc.skills.base import BaseSkill
from typing import Dict, Any

class MySkill(BaseSkill):
    """Template for new skills."""
    
    name = "my_skill"
    description = "What this skill does"
    version = "1.0.0"
    
    async def execute(self, action: str, **params) -> Dict[str, Any]:
        """Main execution method."""
        if action == "action1":
            return await self.action1(**params)
        elif action == "action2":
            return await self.action2(**params)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def action1(self, **params) -> Dict[str, Any]:
        """Action 1 implementation."""
        try:
            # Your logic here
            return {"success": True, "data": {}}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def action2(self, **params) -> Dict[str, Any]:
        """Action 2 implementation."""
        pass
```

## ✅ Best Practices

1. **Always acquire locks before browser automation**
2. **Always check page state before continuing**
3. **Use semantic keys, not CSS selectors**
4. **Add anti-bot delays between actions**
5. **Request human help for edge cases (CAPTCHA, login)**
6. **Store results in agent sandbox database**
7. **Log all actions for audit trail**
8. **Handle timeouts and network errors gracefully**
9. **Test skills thoroughly before deployment**
10. **Document skill actions and parameters**
