"""Playwright browser integration."""

from typing import Optional, Dict, Any, List
import asyncio
from loguru import logger

try:
    from playwright.async_api import async_playwright, Browser, Page, BrowserContext
except ImportError:
    logger.warning("⚠️  Playwright not installed. Install with: pip install playwright")
    async_playwright = None


class PlaywrightBrowser:
    """Playwright browser controller."""
    
    def __init__(
        self,
        headless: bool = True,
        user_agent: Optional[str] = None
    ):
        """Initialize Playwright browser.
        
        Args:
            headless: Run in headless mode
            user_agent: Custom user agent
        """
        self.headless = headless
        self.user_agent = user_agent
        self.browser: Optional[Browser] = None
        self.contexts: Dict[str, BrowserContext] = {}
        self.pages: Dict[str, Page] = {}
        logger.info(f"🎬 Playwright initialized (headless={headless})")
    
    async def launch(self) -> bool:
        """Launch browser.
        
        Returns:
            True if successful
        """
        try:
            if not async_playwright:
                logger.error("❌ Playwright not installed")
                return False
            
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                ]
            )
            logger.info("✅ Browser launched")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to launch browser: {e}")
            return False
    
    async def create_context(
        self,
        context_id: str,
        viewport_size: Optional[tuple] = None
    ) -> bool:
        """Create new browser context.
        
        Args:
            context_id: Context identifier
            viewport_size: (width, height) or None for default
        
        Returns:
            True if successful
        """
        try:
            if not self.browser:
                logger.error("❌ Browser not launched")
                return False
            
            context = await self.browser.new_context(
                user_agent=self.user_agent,
                viewport=viewport_size and {"width": viewport_size[0], "height": viewport_size[1]}
            )
            
            self.contexts[context_id] = context
            logger.info(f"✅ Context created: {context_id}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to create context: {e}")
            return False
    
    async def create_page(
        self,
        page_id: str,
        context_id: str
    ) -> bool:
        """Create new page in context.
        
        Args:
            page_id: Page identifier
            context_id: Context to use
        
        Returns:
            True if successful
        """
        try:
            context = self.contexts.get(context_id)
            if not context:
                logger.error(f"❌ Context not found: {context_id}")
                return False
            
            page = await context.new_page()
            self.pages[page_id] = page
            logger.info(f"✅ Page created: {page_id}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to create page: {e}")
            return False
    
    async def goto(
        self,
        page_id: str,
        url: str,
        timeout_ms: int = 30000
    ) -> bool:
        """Navigate to URL.
        
        Args:
            page_id: Page identifier
            url: URL to navigate to
            timeout_ms: Timeout in milliseconds
        
        Returns:
            True if successful
        """
        try:
            page = self.pages.get(page_id)
            if not page:
                logger.error(f"❌ Page not found: {page_id}")
                return False
            
            await page.goto(url, timeout=timeout_ms)
            logger.info(f"✅ Navigated to: {url}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Navigation failed: {e}")
            return False
    
    async def click(
        self,
        page_id: str,
        selector: str
    ) -> bool:
        """Click element by selector.
        
        Args:
            page_id: Page identifier
            selector: CSS selector
        
        Returns:
            True if successful
        """
        try:
            page = self.pages.get(page_id)
            if not page:
                logger.error(f"❌ Page not found: {page_id}")
                return False
            
            await page.click(selector)
            logger.info(f"🖱️  Clicked: {selector}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Click failed: {e}")
            return False
    
    async def fill(
        self,
        page_id: str,
        selector: str,
        text: str
    ) -> bool:
        """Fill input element.
        
        Args:
            page_id: Page identifier
            selector: CSS selector
            text: Text to fill
        
        Returns:
            True if successful
        """
        try:
            page = self.pages.get(page_id)
            if not page:
                logger.error(f"❌ Page not found: {page_id}")
                return False
            
            await page.fill(selector, text)
            logger.info(f"✏️  Filled: {selector}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Fill failed: {e}")
            return False
    
    async def get_text(
        self,
        page_id: str,
        selector: str
    ) -> Optional[str]:
        """Get element text.
        
        Args:
            page_id: Page identifier
            selector: CSS selector
        
        Returns:
            Element text or None
        """
        try:
            page = self.pages.get(page_id)
            if not page:
                logger.error(f"❌ Page not found: {page_id}")
                return None
            
            text = await page.text_content(selector)
            return text
        
        except Exception as e:
            logger.error(f"❌ Failed to get text: {e}")
            return None
    
    async def evaluate(
        self,
        page_id: str,
        script: str
    ) -> Optional[Any]:
        """Evaluate JavaScript.
        
        Args:
            page_id: Page identifier
            script: JavaScript code
        
        Returns:
            Evaluation result
        """
        try:
            page = self.pages.get(page_id)
            if not page:
                logger.error(f"❌ Page not found: {page_id}")
                return None
            
            result = await page.evaluate(script)
            logger.debug(f"📝 JavaScript evaluated")
            return result
        
        except Exception as e:
            logger.error(f"❌ Evaluation failed: {e}")
            return None
    
    async def close_page(self, page_id: str) -> bool:
        """Close page.
        
        Args:
            page_id: Page identifier
        
        Returns:
            True if successful
        """
        try:
            page = self.pages.get(page_id)
            if page:
                await page.close()
                del self.pages[page_id]
                logger.info(f"✅ Page closed: {page_id}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to close page: {e}")
            return False
    
    async def close_context(self, context_id: str) -> bool:
        """Close context.
        
        Args:
            context_id: Context identifier
        
        Returns:
            True if successful
        """
        try:
            context = self.contexts.get(context_id)
            if context:
                await context.close()
                del self.contexts[context_id]
                logger.info(f"✅ Context closed: {context_id}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to close context: {e}")
            return False
    
    async def shutdown(self) -> bool:
        """Shutdown browser.
        
        Returns:
            True if successful
        """
        try:
            for page_id in list(self.pages.keys()):
                await self.close_page(page_id)
            
            for context_id in list(self.contexts.keys()):
                await self.close_context(context_id)
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            logger.info("✅ Browser shutdown")
            return True
        
        except Exception as e:
            logger.error(f"❌ Shutdown failed: {e}")
            return False