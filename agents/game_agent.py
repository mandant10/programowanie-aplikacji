#!/usr/bin/env python3
"""
Game Agent - zarządza operacjami gry przez MCP
"""

import asyncio
from typing import Dict, Optional
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class GameAgent:
    """Agent do operacji związanych z grą Saper"""
    
    def __init__(self):
        self.mcp_server = StdioServerParameters(
            command="python3",
            args=["mcp_server_minesweeper.py"]
        )
        logger.info("🎮 GameAgent initialized")
    
    async def get_scores(self, difficulty: Optional[str] = None, limit: int = 10) -> Dict:
        """
        Pobierz wyniki gry
        
        Args:
            difficulty: easy, medium, hard (opcjonalne)
            limit: maksymalna liczba wyników
        """
        logger.info("📊 Getting scores: difficulty=%s, limit=%d", difficulty, limit)
        
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    result = await session.call_tool(
                        "get_scores",
                        arguments={
                            "difficulty": difficulty or "",
                            "limit": limit
                        }
                    )
                    
                    return {
                        "status": "success",
                        "agent": "game",
                        "data": result.content[0].text
                    }
        except Exception as e:
            logger.error("❌ Error getting scores: %s", e)
            return {
                "status": "error",
                "agent": "game",
                "error": str(e)
            }
    
    async def submit_score(self, player_name: str, difficulty: str, time_seconds: int) -> Dict:
        """
        Zapisz wynik gry
        
        Args:
            player_name: Nazwa gracza
            difficulty: easy, medium, hard
            time_seconds: Czas w sekundach
        """
        logger.info("💾 Submitting score: %s, %s, %ds", player_name, difficulty, time_seconds)
        
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    result = await session.call_tool(
                        "submit_score",
                        arguments={
                            "player_name": player_name,
                            "difficulty": difficulty,
                            "time_seconds": time_seconds
                        }
                    )
                    
                    return {
                        "status": "success",
                        "agent": "game",
                        "message": result.content[0].text
                    }
        except Exception as e:
            logger.error("❌ Error submitting score: %s", e)
            return {
                "status": "error",
                "agent": "game",
                "error": str(e)
            }
    
    async def get_player_progress(self, player_name: str) -> Dict:
        """Pobierz postęp gracza"""
        logger.info("🎯 Getting progress for: %s", player_name)
        
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    result = await session.call_tool(
                        "get_player_progress",
                        arguments={"player_name": player_name}
                    )
                    
                    return {
                        "status": "success",
                        "agent": "game",
                        "data": result.content[0].text
                    }
        except Exception as e:
            logger.error("❌ Error getting progress: %s", e)
            return {
                "status": "error",
                "agent": "game",
                "error": str(e)
            }
    
    async def validate_score(self, time_seconds: int, difficulty: str) -> bool:
        """
        Waliduj czy wynik jest realistyczny
        
        Returns:
            True jeśli wynik jest OK, False jeśli podejrzany
        """
        # Minimalne czasy dla poziomów (antyoszustwo)
        min_times = {
            "easy": 10,
            "medium": 30,
            "hard": 60
        }
        
        max_times = {
            "easy": 600,    # 10 minut
            "medium": 2400,  # 40 minut
            "hard": 5940     # 99 minut
        }
        
        min_time = min_times.get(difficulty, 0)
        max_time = max_times.get(difficulty, 10000)
        
        is_valid = min_time <= time_seconds <= max_time
        
        if not is_valid:
            logger.warning("⚠️  Suspicious score: %ds for %s (min:%d, max:%d)", 
                         time_seconds, difficulty, min_time, max_time)
        
        return is_valid
    
    async def health_check(self) -> Dict:
        """Sprawdź czy MCP server działa"""
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    
                    return {
                        "status": "ok",
                        "tools_count": len(tools.tools)
                    }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
