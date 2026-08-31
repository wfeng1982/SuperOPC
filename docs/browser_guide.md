# Browser Automation Guide

## 🌐 Overview

SuperOPC's browser automation system provides:
- Enterprise-grade DOM manipulation
- Anti-bot protection built-in
- Smart page state detection
- Human-in-the-loop for edge cases

## 🚀 Quick Start

### Create Browser Session

```python
from superopc.core.browser import BrowserManager

manager = BrowserManager()
session = await manager.create_session(
    session_id="search_001",
    agent_id="amazon_bot_1"
)
```

### Acquire Domain Lock

```python
# Prevent concurrent access to same domain
await session.acquire_lock(
    domains=["amazon.com"],
    concurrency_policy="domain"
)
```

### Navigate & Snapshot

```python
# Navigate to page
await session.goto("https://amazon.com/s?k=laptop")

# Take DOM snapshot (multiple modes available)
snapshot = await session.snapshot(mode="data")  # Emphasize data elements

# Extract data from snapshot
for item in snapshot["items"]:
    product = {
        "title": item["text"],
        "price": item["price"],
        "handle": item["handle"]  # Use handle, not CSS selector!
    }
```

### Detect Page State

```python
state = await session.detect_page_state()

if state["state"] == "captcha":
    # Request human intervention
    await session.request_help(
        title="CAPTCHA Required",
        prompt="Please complete the CAPTCHA",
        timeout_ms=300000
    )
elif state["state"] == "login":
    # Handle login
    pass
elif state["state"] == "blocked":
    # IP is blocked, rotate proxy
    pass
else:
    # Continue automation
    pass
```

### Release Locks

```python
# Release locks (but keep browser open)
await session.release_lock(close_browser=False)

# Or close browser entirely
await session.release_lock(close_browser=True)
```

## 📸 DOM Snapshot Modes

### 1. Quick Mode (Default)
Fast snapshot of visible controls.
```python
snapshot = await session.snapshot(mode="quick")
# Returns: input boxes, buttons, dialogs, links
# Time: ~100ms
```

### 2. Data Mode
Emphasize data elements (tables, cards, lists).
```python
snapshot = await session.snapshot(mode="data")
# Returns: product cards, table rows, list items
# Time: ~200ms
# Perfect for: E-commerce, data extraction
```

### 3. Section Mode
Snapshot specific section by CSS selector.
```python
snapshot = await session.snapshot(
    mode="section",
    selector=".search-results"
)
# Returns: Elements within selector
# Time: ~150ms
```

### 4. Full Mode
Deep scan of entire page.
```python
snapshot = await session.snapshot(mode="full")
# Returns: All visible and rendered elements
# Time: ~500ms
# Perfect for: Complex sites, detailed analysis
```

### 5. Accessibility (AX) Mode
Use accessibility tree for better semantic understanding.
```python
snapshot = await session.snapshot(mode="ax")
# Returns: Elements with ARIA roles and names
# Time: ~300ms
# Perfect for: Modern React/Vue apps, accessible sites
```

## 🔒 Anti-Bot Protection

### 1. Domain Locking
```python
# Only one session can access domain at a time
await session.acquire_lock(["amazon.com"], "domain")

# Prevents:
# - Multiple concurrent requests from same IP
# - Being identified as bot farm
# - Account lockouts
```

### 2. Natural Delays
```python
# Automatic jitter between actions
await anti_bot.add_human_like_delay("click")  # 0.5-3 seconds
await anti_bot.add_human_like_delay("type")   # 1-2 seconds per char

# Simulates real user thinking/reaction time
```

### 3. User-Agent Rotation
```python
user_agent = await anti_bot.rotate_user_agent()
# Randomly picks from real browser user agents
# Prevents detection as bot
```

### 4. Rate Limiting
```python
await anti_bot.check_rate_limit(
    domain="amazon.com",
    requests_per_hour=30  # Conservative limit
)

# Raises exception if rate exceeded
```

### 5. Human-in-the-Loop
```python
if state["state"] == "captcha":
    # DON'T try to solve automatically
    # Instead request human help
    await session.request_help(
        title="Please complete CAPTCHA",
        prompt="A CAPTCHA has appeared. Please solve it in your browser.",
        timeout_ms=300000  # 5 minutes
    )
    # Resume after human solves it
```

## 🎯 Best Practices

### ✅ DO

1. **Use semantic keys instead of CSS selectors**
   ```python
   # GOOD
   await session.click(semantic_key="search.submit")
   
   # BAD - breaks when CSS changes
   await session.click(selector="div.css-1a2b3c > button")
   ```

2. **Check page state before actions**
   ```python
   state = await session.detect_page_state()
   if state["state"] != "ok":
       await session.request_help(...)
   ```

3. **Use domain locking**
   ```python
   await session.acquire_lock(["example.com"])
   try:
       # Do work
       pass
   finally:
       await session.release_lock()
   ```

4. **Add human-like delays**
   ```python
   await session.fill(selector, text)
   await anti_bot.add_human_like_delay("type")
   await session.click(button)
   ```

### ❌ DON'T

1. **Don't hardcode CSS selectors**
   - Sites change CSS all the time
   - Use semantic keys or text matching

2. **Don't retry aggressively on CAPTCHA**
   - You'll get permanently blocked
   - Request human help instead

3. **Don't access same domain concurrently**
   - Use domain locking
   - Prevents IP detection

4. **Don't skip delays**
   - Delays are essential for avoiding bans
   - Add jitter to make them unpredictable

5. **Don't log sensitive data**
   - Passwords, cookies, tokens are auto-redacted
   - Never print full responses

## 🛠️ Action Reference

```python
# Navigation
await session.goto("https://example.com")
await session.go_back()
await session.go_forward()
await session.reload()

# Input
await session.fill(selector, text)
await session.click(selector)
await session.hover(selector)
await session.press("Enter")

# Waiting
await session.wait_for_selector(".element")
await session.wait_for_timeout(2000)  # 2 seconds

# Extraction
text = await session.get_text(selector)
value = await session.get_attribute(selector, "href")
html = await session.get_html()
title = await session.get_title()
url = await session.get_url()

# Execution
result = await session.evaluate("document.title")
```

## 📊 Performance Tips

1. **Use quick snapshots for controls, data for extraction**
   - Quick: 100ms, good for buttons/inputs
   - Data: 200ms, good for product cards
   - Full: 500ms, only when necessary

2. **Keep browser session alive**
   - Create once, reuse for multiple tasks
   - Reduces overhead

3. **Batch domain access**
   - Process all tasks for domain in one session
   - Minimize lock contention

4. **Use headless mode**
   - 20-30% faster than headed mode
   - Set `HEADLESS=true` in `.env`

## 🐛 Debugging

### Enable Debug Mode
```bash
DEBUG=true uv run python -m superopc.main
```

### Keep Browser Open
```python
await session.release_lock(close_browser=False)
# Browser stays open for manual inspection
```

### Check Logs
```bash
cat ~/.superopc/logs/superopc.log
cat ~/.superopc/agents/agent_id/logs/*.log
```

### Inspect Snapshots
```python
import json
snapshot = await session.snapshot(mode="data")
print(json.dumps(snapshot, indent=2))
```

## 🔗 Related Docs
- [Architecture Guide](architecture.md)
- [Skill Development](skill_development.md)
- [API Reference](api.md)
