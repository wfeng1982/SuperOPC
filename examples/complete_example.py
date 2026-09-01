"""Comprehensive end-to-end example."""

import asyncio
from pathlib import Path
import json

from superopc.core.agent.manager import AgentManager
from superopc.core.browser.daemon import BrowserManager
from superopc.core.models.provider import ModelProvider
from superopc.core.executor import SkillExecutor
from superopc.core.task_manager import TaskManager
from superopc.core.rag import RAGManager
from superopc.scheduler.manager import TaskScheduler
from superopc.utils.logging import setup_logging


async def main():
    """Complete SuperOPC demonstration."""
    
    # Setup
    workspace = Path.home() / ".superopc_demo"
    workspace.mkdir(parents=True, exist_ok=True)
    
    setup_logging(workspace / "logs", level="INFO")
    
    print("\n" + "="*70)
    print(" 🚀 SuperOPC Complete System Demonstration")
    print("="*70)
    
    # ==================== PART 1: AGENT ISOLATION ====================
    print("\n📦 PART 1: Multi-Account Sandbox Isolation")
    print("-" * 70)
    
    agent_manager = AgentManager(workspace)
    
    # Create multiple isolated agents
    agents_config = [
        {
            "id": "amazon_us_1",
            "name": "Amazon US Account 1",
            "description": "Search and monitor US Amazon"
        },
        {
            "id": "amazon_us_2",
            "name": "Amazon US Account 2",
            "description": "Different US Amazon account"
        },
        {
            "id": "ebay_uk_1",
            "name": "eBay UK Account",
            "description": "Monitor eBay UK listings"
        },
    ]
    
    for config in agents_config:
        agent = agent_manager.create_agent(
            config["id"],
            {"name": config["name"], "description": config["description"]}
        )
        print(f"✅ Created: {config['name']}")
        print(f"   📍 Sandbox: {agent.sandbox_dir}")
        print(f"   🗄️ Database: {agent.db_path}")
    
    # ==================== PART 2: BROWSER AUTOMATION ====================
    print("\n🌐 PART 2: Browser Automation with Anti-Bot Protection")
    print("-" * 70)
    
    browser_manager = BrowserManager()
    
    # Create browser sessions
    session1 = await browser_manager.create_session(
        "search_amazon_001",
        "amazon_us_1"
    )
    print(f"✅ Browser session created: {session1.session_id}")
    
    # Demonstrate domain locking
    acquired = await session1.acquire_lock(
        ["amazon.com", "www.amazon.com"],
        "domain"
    )
    print(f"✅ Domain lock acquired: {acquired}")
    print(f"   🔐 Locked domains: {list(session1.locks.keys())}")
    
    # Release lock
    await session1.release_lock(close_browser=False)
    print(f"✅ Lock released (browser kept open for debugging)")
    
    # ==================== PART 3: LLM INTEGRATION ====================
    print("\n🤖 PART 3: Flexible LLM Provider Integration")
    print("-" * 70)
    
    model_provider = ModelProvider()
    
    # Show available providers
    print(f"📦 Available LLM Providers:")
    for provider_name, provider_info in model_provider.providers.items():
        models = provider_info["models"]
        print(f"   • {provider_name}: {models[:2]}... ({len(models)} models)")
    
    # Get specific provider info
    ollama_info = model_provider.get_provider_info("ollama")
    print(f"\n🔧 Ollama Configuration:")
    print(f"   Base URL: {ollama_info['base_url']}")
    print(f"   Type: {ollama_info['type']}")
    print(f"   Available models: {len(ollama_info['models'])}")
    
    # ==================== PART 4: SKILL EXECUTION ====================
    print("\n⚙️ PART 4: Skill Execution Engine")
    print("-" * 70)
    
    skill_executor = SkillExecutor(browser_manager, model_provider)
    
    # Load skill
    agent_sandbox = agent_manager.get_agent_sandbox("amazon_us_1")
    skill = await skill_executor._load_skill("amazon_automation", agent_sandbox)
    print(f"✅ Loaded skill: {skill.name} v{skill.version}")
    print(f"   📝 Description: {skill.description}")
    
    # Execute skill action (demo)
    print(f"\n🚀 Executing: amazon_automation.search_products")
    result = await skill.execute(
        "search_products",
        keyword="laptop",
        max_results=5
    )
    print(f"   Status: {'✅' if result['success'] else '❌'} {result.get('success', False)}")
    print(f"   Results: {result.get('results_count', 0)} products found")
    
    # ==================== PART 5: TASK MANAGEMENT ====================
    print("\n📋 PART 5: Task Management & Execution")
    print("-" * 70)
    
    task_manager = TaskManager()
    
    # Create tasks
    task1 = task_manager.create_task(
        agent_id="amazon_us_1",
        skill="amazon_automation",
        action="search_products",
        parameters={"keyword": "laptop", "max_results": 20}
    )
    print(f"✅ Task created: {task1.task_id}")
    print(f"   Agent: {task1.agent_id}")
    print(f"   Skill: {task1.skill}.{task1.action}")
    print(f"   Status: {task1.status.value}")
    
    # Simulate task execution
    task_manager.update_task_status(
        task1.task_id,
        task1.status.RUNNING
    )
    print(f"\n   Status updated: RUNNING")
    
    task_manager.update_task_status(
        task1.task_id,
        task1.status.COMPLETED,
        result={"products_found": 15, "success": True}
    )
    print(f"   Status updated: COMPLETED")
    print(f"   Result: {task1.result}")
    
    # ==================== PART 6: SCHEDULING ====================
    print("\n⏰ PART 6: Task Scheduling & Workflows")
    print("-" * 70)
    
    scheduler = TaskScheduler()
    
    # Schedule cron tasks
    scheduler.add_cron_task(
        task_id="daily_amazon_search",
        agent_id="amazon_us_1",
        skill="amazon_automation",
        action="search_products",
        cron_expression="0 9 * * *",
        parameters={"keyword": "laptop", "max_results": 50}
    )
    print(f"✅ Scheduled: daily_amazon_search")
    print(f"   When: Every day at 9:00 AM")
    
    scheduler.add_cron_task(
        task_id="weekly_price_monitor",
        agent_id="amazon_us_1",
        skill="amazon_automation",
        action="monitor_prices",
        cron_expression="0 10 * * MON",
        parameters={"product_ids": ["B001", "B002"], "alert_on_drop_percent": 10}
    )
    print(f"\n✅ Scheduled: weekly_price_monitor")
    print(f"   When: Every Monday at 10:00 AM")
    
    # Add workflow
    scheduler.add_workflow(
        workflow_id="daily_report",
        steps=[
            {"agent_id": "amazon_us_1", "skill": "amazon_automation", "action": "search_products"},
            {"agent_id": "amazon_us_1", "skill": "analysis", "action": "analyze_results"},
            {"agent_id": "marketing", "skill": "email", "action": "send_report"},
        ],
        cron_expression="0 9 * * *"
    )
    print(f"\n✅ Workflow scheduled: daily_report")
    print(f"   Steps: 3 (Search → Analyze → Email)")
    print(f"   When: Every day at 9:00 AM")
    
    # ==================== PART 7: RAG KNOWLEDGE BASE ====================
    print("\n📚 PART 7: RAG Knowledge Base Management")
    print("-" * 70)
    
    rag = RAGManager(workspace / "knowledge")
    
    # Simulate loading knowledge
    print(f"✅ RAG initialized at: {rag.knowledge_dir}")
    
    # In production, would load actual files
    rag.documents["amazon_rules.md"] = """# Amazon Listing Rules
    - Max 500 variations per product
    - Title max 200 characters
    - Pricing: $0.01 - $1,000,000
    """
    
    rag.documents["ebay_fees.txt"] = """eBay Seller Fees (2024)
    - Insertion: $0.30-$4.00
    - Final: 12.9% (capped at $750)
    """
    
    print(f"📝 Loaded documents: {len(rag.documents)}")
    
    # Query knowledge base
    results = await rag.query("Amazon listing rules", top_k=2)
    print(f"🔍 Query: 'Amazon listing rules'")
    print(f"   Found: {len(results)} results")
    
    # ==================== SUMMARY ====================
    print("\n" + "="*70)
    print(" ✅ SuperOPC Demonstration Complete")
    print("="*70)
    
    print("""
✨ Key Features Demonstrated:

1. 🏗️  Multi-Account Sandbox Isolation
   ✓ Each agent has isolated database
   ✓ Separate execution directories
   ✓ Zero cross-contamination

2. 🌐 Browser Automation with Anti-Bot
   ✓ Domain-level locking
   ✓ Session management
   ✓ Page state detection

3. 🤖 Flexible LLM Integration
   ✓ Multiple providers (Ollama, OpenAI, etc.)
   ✓ Easy model switching
   ✓ Unified API

4. ⚙️  Skill Execution Engine
   ✓ Dynamic skill loading
   ✓ Parameter validation
   ✓ Error handling

5. 📋 Task Management
   ✓ Task creation and tracking
   ✓ Status updates
   ✓ Result storage

6. ⏰ Scheduling & Workflows
   ✓ Cron-based scheduling
   ✓ Multi-step workflows
   ✓ Task dependency management

7. 📚 RAG Knowledge Base
   ✓ Document loading
   ✓ Knowledge queries
   ✓ Source traceability

🎯 Next Steps:
   1. Create your first agent
   2. Deploy a skill
   3. Schedule automated tasks
   4. Monitor results

📖 Documentation: https://github.com/wfeng1982/SuperOPC/tree/main/docs
🐛 Issues: https://github.com/wfeng1982/SuperOPC/issues
💬 Discussions: https://github.com/wfeng1982/SuperOPC/discussions
    """)
    
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())