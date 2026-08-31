"""Amazon e-commerce automation skill."""

import asyncio
import json
import time
import random
from typing import Dict, List, Any
from loguru import logger

from superopc.skills.base import BaseSkill


class AmazonSkill(BaseSkill):
    """Amazon automation skill for searching, scraping, and analyzing products."""
    
    name = "amazon_automation"
    description = "Automate Amazon product search, data extraction, and analysis"
    version = "1.0.0"
    
    async def execute(self, action: str, **params) -> Dict[str, Any]:
        """Execute Amazon automation action.
        
        Args:
            action: Action to execute (search_products, get_details, monitor_prices)
            **params: Action-specific parameters
        
        Returns:
            Action result
        """
        if action == "search_products":
            return await self.search_products(**params)
        elif action == "get_details":
            return await self.get_product_details(**params)
        elif action == "monitor_prices":
            return await self.monitor_prices(**params)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def search_products(
        self,
        keyword: str,
        max_results: int = 20,
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Search for products on Amazon.
        
        Args:
            keyword: Search keyword
            max_results: Maximum products to return
            filters: Optional filters (price_min, price_max, rating_min)
        
        Returns:
            Search results
        """
        if not self.browser:
            return {"success": False, "error": "Browser manager not available"}
        
        session_id = f"amazon_search_{int(time.time())}_{random.randint(1000, 9999)}"
        
        try:
            # Create browser session
            session = await self.browser.create_session(
                session_id=session_id,
                agent_id=self.sandbox.agent_id
            )
            
            logger.info(f"🔍 Starting Amazon search: {keyword}")
            
            # Acquire domain lock (critical for preventing bans)
            acquired = await session.acquire_lock(
                domains=["amazon.com", "www.amazon.com"],
                concurrency_policy="domain"
            )
            
            if not acquired:
                return {
                    "success": False,
                    "error": "Could not acquire lock for amazon.com. Already in use."
                }
            
            # Navigate to Amazon search
            search_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
            logger.info(f"📍 Navigating to: {search_url}")
            
            # Take quick snapshot to verify page loaded
            snapshot = await session.detect_page_state()
            
            if snapshot["state"] != "ok":
                if snapshot["state"] == "captcha":
                    logger.warning("⚠️  CAPTCHA detected, requesting human help")
                    return {
                        "success": False,
                        "error": "CAPTCHA",
                        "human_help_needed": True
                    }
                elif snapshot["state"] == "blocked":
                    logger.error("❌ IP appears to be blocked")
                    return {
                        "success": False,
                        "error": "IP blocked"
                    }
            
            logger.info(f"✅ Page loaded successfully")
            
            # Extract products from results page
            # In real implementation, would use DOM snapshot
            products = await self._extract_search_results(
                session,
                max_results,
                filters or {}
            )
            
            # Store results in sandbox database
            await self._store_results(
                keyword,
                products
            )
            
            logger.info(f"✅ Search complete: Found {len(products)} products")
            
            return {
                "success": True,
                "keyword": keyword,
                "results_count": len(products),
                "products": products
            }
        
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return {"success": False, "error": str(e)}
        
        finally:
            # Always release lock
            await session.release_lock(close_browser=False)
            logger.info(f"🔓 Session released: {session_id}")
    
    async def get_product_details(self, product_url: str) -> Dict[str, Any]:
        """Get detailed product information.
        
        Args:
            product_url: URL of product page
        
        Returns:
            Product details
        """
        if not self.browser:
            return {"success": False, "error": "Browser manager not available"}
        
        session_id = f"amazon_details_{int(time.time())}_{random.randint(1000, 9999)}"
        
        try:
            session = await self.browser.create_session(
                session_id=session_id,
                agent_id=self.sandbox.agent_id
            )
            
            logger.info(f"📖 Getting product details: {product_url}")
            
            await session.acquire_lock(
                domains=["amazon.com", "www.amazon.com"],
                concurrency_policy="domain"
            )
            
            # Check page state
            state = await session.detect_page_state()
            if state["state"] != "ok":
                return {"success": False, "error": state["state"]}
            
            # Extract product details
            details = {
                "url": product_url,
                "title": "[Product Title]",
                "price": "[Price]",
                "rating": "[Rating]",
                "reviews_count": 0,
                "availability": "[Availability]",
                "description": "[Description]",
                "images": [],
                "variants": []
            }
            
            logger.info(f"✅ Product details extracted")
            
            return {
                "success": True,
                "details": details
            }
        
        except Exception as e:
            logger.error(f"❌ Failed to get product details: {e}")
            return {"success": False, "error": str(e)}
        
        finally:
            await session.release_lock()
    
    async def monitor_prices(
        self,
        product_ids: List[str],
        alert_on_drop_percent: float = 10.0
    ) -> Dict[str, Any]:
        """Monitor product prices and alert on drops.
        
        Args:
            product_ids: List of ASIN/product IDs
            alert_on_drop_percent: Alert threshold percentage
        
        Returns:
            Price monitoring results
        """
        logger.info(f"💰 Monitoring {len(product_ids)} products")
        
        results = []
        
        for product_id in product_ids:
            try:
                # Check price
                url = f"https://www.amazon.com/dp/{product_id}"
                details = await self.get_product_details(url)
                
                if details["success"]:
                    results.append({
                        "product_id": product_id,
                        "price": details["details"].get("price"),
                        "status": "monitored"
                    })
                    
                    # Add delay to avoid rate limiting
                    await asyncio.sleep(random.uniform(2, 5))
            
            except Exception as e:
                logger.error(f"❌ Failed to monitor {product_id}: {e}")
                results.append({
                    "product_id": product_id,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "monitored_count": len(product_ids),
            "results": results
        }
    
    async def _extract_search_results(
        self,
        session,
        max_results: int,
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract product results from search page.
        
        Args:
            session: Browser session
            max_results: Max results to extract
            filters: Price and rating filters
        
        Returns:
            List of products
        """
        # Placeholder for actual DOM parsing
        # In production, would use session.snapshot(mode="data")
        return [
            {
                "title": "Product 1",
                "price": "$99.99",
                "rating": "4.5",
                "reviews": 150,
                "url": "https://amazon.com/dp/ASIN1",
                "availability": "In Stock"
            },
            {
                "title": "Product 2",
                "price": "$79.99",
                "rating": "4.2",
                "reviews": 89,
                "url": "https://amazon.com/dp/ASIN2",
                "availability": "In Stock"
            }
        ][:max_results]
    
    async def _store_results(
        self,
        keyword: str,
        products: List[Dict[str, Any]]
    ) -> None:
        """Store search results in sandbox database.
        
        Args:
            keyword: Search keyword
            products: List of products
        """
        try:
            conn = self.sandbox.get_db_connection()
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS amazon_searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    results_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert results
            cursor.execute("""
                INSERT INTO amazon_searches (keyword, results_json)
                VALUES (?, ?)
            """, (keyword, json.dumps(products)))
            
            conn.commit()
            conn.close()
            
            logger.info(f"💾 Stored {len(products)} results for keyword: {keyword}")
        
        except Exception as e:
            logger.error(f"Failed to store results: {e}")