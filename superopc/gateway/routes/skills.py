"""Skill management endpoints."""

from fastapi import APIRouter, HTTPException, Request
from loguru import logger

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("/available")
async def list_available_skills():
    """List available skills."""
    skills = {
        "amazon_automation": {
            "name": "amazon_automation",
            "description": "Automate Amazon product search and data extraction",
            "version": "1.0.0",
            "actions": [
                "search_products",
                "get_details",
                "monitor_prices"
            ]
        },
        # More skills can be added here
    }
    return {"skills": skills}


@router.get("/{skill_name}")
async def get_skill_info(skill_name: str):
    """Get skill information."""
    # In production, would load from registry
    skill_info = {
        "amazon_automation": {
            "name": "amazon_automation",
            "description": "Automate Amazon product search and data extraction",
            "version": "1.0.0",
            "actions": [
                {
                    "name": "search_products",
                    "description": "Search for products on Amazon",
                    "parameters": {
                        "keyword": {"type": "string", "required": True},
                        "max_results": {"type": "integer", "required": False, "default": 20},
                        "filters": {"type": "object", "required": False}
                    }
                },
                {
                    "name": "get_details",
                    "description": "Get detailed product information",
                    "parameters": {
                        "product_url": {"type": "string", "required": True}
                    }
                },
                {
                    "name": "monitor_prices",
                    "description": "Monitor product prices and alert on drops",
                    "parameters": {
                        "product_ids": {"type": "array", "required": True},
                        "alert_on_drop_percent": {"type": "number", "required": False, "default": 10}
                    }
                }
            ]
        }
    }
    
    if skill_name not in skill_info:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return skill_info[skill_name]