"""Example: Creating multi-account Amazon bot."""

import asyncio
from pathlib import Path

from superopc.core.agent.manager import AgentManager
from superopc.core.browser.daemon import BrowserManager
from superopc.core.models.provider import ModelProvider
from superopc.skills.ecommerce.amazon import AmazonSkill


async def example_multi_account_bot():
    """Example: Create and manage multiple Amazon accounts."""
    
    # Setup
    workspace = Path.home() / ".superopc_example"
    agent_manager = AgentManager(workspace)
    browser_manager = BrowserManager()
    model_provider = ModelProvider()
    
    print("\n" + "="*60)
    print("SuperOPC Multi-Account Bot Example")
    print("="*60)
    
    # Create isolated agents for different accounts
    print("\n📱 Creating isolated agents...\n")
    
    accounts = [
        {"id": "amazon_us_account_1", "name": "Amazon US - Account A"},
        {"id": "amazon_us_account_2", "name": "Amazon US - Account B"},
        {"id": "amazon_uk_account_1", "name": "Amazon UK - Account 1"},
    ]
    
    for account in accounts:
        agent = agent_manager.create_agent(
            account["id"],
            {
                "name": account["name"],
                "model_provider": "ollama",
                "model_name": "mistral",
                "skills": ["amazon_search", "amazon_details"]
            }
        )
        print(f"✅ Created: {account['name']}")
        print(f"   Location: {agent.sandbox_dir}")
        print(f"   Database: {agent.db_path}")
        print()
    
    # Create skills for agents
    print("\n🛠️  Creating skill instances...\n")
    
    skills = {}
    for account in accounts:
        agent_id = account["id"]
        sandbox = agent_manager.get_agent_sandbox(agent_id)
        skill = AmazonSkill(
            browser_manager=browser_manager,
            model_provider=model_provider,
            sandbox=sandbox
        )
        skills[agent_id] = skill
        print(f"✅ {agent_id}: Amazon skill ready")
    
    # Demonstrate isolated execution
    print("\n🚀 Demonstrating isolated skill execution...\n")
    
    # Each agent searches independently without data leakage
    for i, account in enumerate(accounts[:2]):
        agent_id = account["id"]
        skill = skills[agent_id]
        
        print(f"\n📍 Agent: {account['name']}")
        print(f"   Executing: search_products(keyword='laptop', max_results=5)")
        
        result = await skill.execute(
            action="search_products",
            keyword="gaming laptop",
            max_results=5
        )
        
        if result["success"]:
            print(f"   ✅ Found {result['results_count']} products")
        else:
            print(f"   ⚠️  {result.get('error', 'Unknown error')}")
    
    # Show isolation benefits
    print("\n" + "="*60)
    print("Isolation Benefits Demonstrated")
    print("="*60)
    print("""
✅ Data Isolation:
   - Each agent has separate SQLite database
   - No data leakage between accounts
   - Independent search history

✅ Process Isolation:
   - Each agent has separate sandboxes directory
   - Separate execution environments
   - Independent browser sessions

✅ Security:
   - Domain-level locking prevents concurrent access
   - Natural delays prevent bot detection
   - Human-in-the-loop for verification

✅ Scalability:
   - Add unlimited accounts
   - Each account operates independently
   - Zero interference between agents
    """)
    
    # List all agents
    print("\n📋 All created agents:\n")
    for agent_id, config in agent_manager.list_agents().items():
        info = agent_manager.get_agent_info(agent_id)
        print(f"  • {agent_id}")
        print(f"    Name: {config.get('name')}")
        print(f"    Sandbox: {info['sandbox']['sandbox_dir']}")
    
    print("\n" + "="*60)
    print("Example completed successfully!")
    print("="*60 + "\n")


async def example_scheduled_tasks():
    """Example: Scheduled tasks and workflows."""
    
    from superopc.scheduler.manager import TaskScheduler
    
    print("\n" + "="*60)
    print("SuperOPC Scheduled Tasks Example")
    print("="*60 + "\n")
    
    scheduler = TaskScheduler()
    
    # Add daily task
    print("📅 Adding scheduled tasks...\n")
    
    scheduler.add_cron_task(
        task_id="daily_amazon_search",
        agent_id="amazon_us_account_1",
        skill="amazon_search",
        action="search_products",
        cron_expression="0 9 * * *",  # Every day at 9 AM
        parameters={
            "keyword": "laptop",
            "max_results": 20
        }
    )
    print("✅ Scheduled: daily_amazon_search (every day at 9 AM)")
    
    scheduler.add_cron_task(
        task_id="weekly_price_monitor",
        agent_id="amazon_us_account_1",
        skill="amazon_monitor",
        action="monitor_prices",
        cron_expression="0 10 * * MON",  # Every Monday at 10 AM
        parameters={
            "product_ids": ["B001", "B002", "B003"],
            "alert_on_drop_percent": 10
        }
    )
    print("✅ Scheduled: weekly_price_monitor (every Monday at 10 AM)")
    
    # Add workflow
    print("\n🔄 Adding multi-step workflow...\n")
    
    scheduler.add_workflow(
        workflow_id="daily_report_workflow",
        steps=[
            {
                "agent_id": "amazon_us_account_1",
                "skill": "amazon_search",
                "action": "search_products",
                "params": {"keyword": "electronics"}
            },
            {
                "agent_id": "amazon_us_account_1",
                "skill": "analysis",
                "action": "analyze_products",
                "depends_on": "step_1"
            },
            {
                "agent_id": "marketing_agent",
                "skill": "email",
                "action": "send_report",
                "depends_on": "step_2"
            }
        ],
        cron_expression="0 9 * * *"
    )
    print("✅ Workflow scheduled: daily_report_workflow")
    print("   Step 1: Search products")
    print("   Step 2: Analyze products")
    print("   Step 3: Send email report")
    
    # Show scheduled tasks
    print("\n📋 All scheduled tasks:\n")
    for task_id, task in scheduler.list_tasks().items():
        print(f"  • {task_id}")
        print(f"    Agent: {task['agent_id']}")
        print(f"    Schedule: {task['cron']}")
        print(f"    Status: {task['status']}")
    
    print("\n" + "="*60)
    print("Scheduling example completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Run examples
    asyncio.run(example_multi_account_bot())
    asyncio.run(example_scheduled_tasks())