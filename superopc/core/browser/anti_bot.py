"""Anti-bot protection strategies."""

import asyncio
import random
import time
from typing import List
from loguru import logger


class AntiBotStrategy:
    """Anti-bot detection and evasion strategies."""
    
    # User agents from real browsers
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    ]
    
    def __init__(
        self,
        min_delay_ms: int = 500,
        max_delay_ms: int = 3000,
        jitter_factor: float = 0.2
    ):
        """Initialize anti-bot strategy.
        
        Args:
            min_delay_ms: Minimum delay in milliseconds
            max_delay_ms: Maximum delay in milliseconds
            jitter_factor: Jitter factor (0-1)
        """
        self.min_delay = min_delay_ms / 1000
        self.max_delay = max_delay_ms / 1000
        self.jitter_factor = jitter_factor
        
        # Track domain access
        self.domain_requests: dict = {}
        self.domain_timestamps: dict = {}
    
    async def add_human_like_delay(
        self,
        action_type: str = "click"
    ) -> None:
        """Add human-like delay between actions.
        
        Args:
            action_type: Type of action (click, type, scroll, hover)
        """
        # Different delays for different actions
        if action_type == "type":
            # Typing is slower - 50-200ms per character
            delay = random.uniform(0.05, 0.2)
        elif action_type == "scroll":
            # Scrolling is medium speed
            delay = random.uniform(0.3, 1.0)
        elif action_type == "hover":
            # Hovering is fast
            delay = random.uniform(0.1, 0.5)
        else:  # click, default
            # Clicking is medium speed
            delay = random.uniform(self.min_delay, self.max_delay)
        
        # Add jitter (randomness)
        jitter = random.uniform(-self.jitter_factor, self.jitter_factor)
        final_delay = delay * (1 + jitter)
        
        logger.debug(f"⏳ Delay: {final_delay:.2f}s ({action_type})")
        await asyncio.sleep(final_delay)
    
    async def rotate_user_agent(self) -> str:
        """Get random user agent.
        
        Returns:
            Random user agent string
        """
        ua = random.choice(self.USER_AGENTS)
        logger.debug(f"🔄 Rotated user agent")
        return ua
    
    async def check_rate_limit(
        self,
        domain: str,
        max_requests_per_hour: int = 30
    ) -> bool:
        """Check if domain rate limit exceeded.
        
        Args:
            domain: Domain name
            max_requests_per_hour: Max requests allowed per hour
        
        Returns:
            True if within limit, False if exceeded
        """
        current_time = time.time()
        hour_ago = current_time - 3600
        
        if domain not in self.domain_timestamps:
            self.domain_timestamps[domain] = []
        
        # Remove old timestamps
        self.domain_timestamps[domain] = [
            ts for ts in self.domain_timestamps[domain]
            if ts > hour_ago
        ]
        
        # Check limit
        if len(self.domain_timestamps[domain]) >= max_requests_per_hour:
            logger.warning(f"⚠️  Rate limit exceeded for {domain}")
            return False
        
        # Record this request
        self.domain_timestamps[domain].append(current_time)
        logger.debug(f"✅ Rate limit OK for {domain} ({len(self.domain_timestamps[domain])}/{max_requests_per_hour})")
        return True
    
    async def add_random_mouse_movement(self) -> None:
        """Simulate random mouse movement."""
        # Small random movements
        await asyncio.sleep(random.uniform(0.1, 0.5))
        logger.debug("🖱️  Random mouse movement")
    
    async def add_scroll_pause(self) -> None:
        """Add pause after scrolling like human would."""
        await asyncio.sleep(random.uniform(0.5, 2.0))
        logger.debug("📜 Scroll pause")
    
    def get_realistic_viewport_size(self) -> tuple:
        """Get realistic browser viewport size.
        
        Returns:
            (width, height) tuple
        """
        # Common desktop viewport sizes
        viewports = [
            (1920, 1080),
            (1366, 768),
            (1440, 900),
            (1280, 720),
            (1024, 768),
        ]
        return random.choice(viewports)
    
    def get_realistic_headers(self) -> dict:
        """Get realistic HTTP headers.
        
        Returns:
            Dictionary of headers
        """
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }