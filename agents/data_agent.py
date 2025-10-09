#!/usr/bin/env python3
"""
Data Agent - analiza danych i statystyk
"""

import asyncio
from typing import Dict
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class DataAgent:
    """Agent do analizy danych i generowania raportów"""
    
    def __init__(self):
        self.mcp_server = StdioServerParameters(
            command="python3",
            args=["mcp_server_minesweeper.py"]
        )
        logger.info("📊 DataAgent initialized")
    
    async def analyze(self) -> Dict:
        """Przeanalizuj statystyki gry"""
        logger.info("🔍 Analyzing game statistics")
        
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Pobierz statystyki
                    stats = await session.read_resource("mcp://game-stats")
                    
                    # Parsuj statystyki
                    parsed = self._parse_stats(stats.contents[0].text)
                    
                    return {
                        "status": "success",
                        "agent": "data",
                        "raw_stats": stats.contents[0].text,
                        "parsed": parsed
                    }
        except Exception as e:
            logger.error("❌ Error analyzing stats: %s", e)
            return {
                "status": "error",
                "agent": "data",
                "error": str(e)
            }
    
    def _parse_stats(self, stats_text: str) -> Dict:
        """Parsuj tekst statystyk na strukturę JSON"""
        lines = stats_text.split('\n')
        
        parsed = {
            "total_games": 0,
            "unique_players": 0,
            "distribution": {},
            "best_times": {}
        }
        
        for line in lines:
            # Parsowanie (uproszczone regex można ulepszyć)
            if "Rozegranych gier:" in line:
                try:
                    parsed["total_games"] = int(line.split(':')[1].strip())
                except:
                    pass
            
            elif "Unikalnych graczy:" in line:
                try:
                    parsed["unique_players"] = int(line.split(':')[1].strip())
                except:
                    pass
            
            elif "Łatwy:" in line and "s" in line:
                try:
                    time_str = line.split(':')[-1].strip().replace('s', '')
                    parsed["best_times"]["easy"] = int(time_str)
                except:
                    pass
            
            elif "Średni:" in line and "s" in line:
                try:
                    time_str = line.split(':')[-1].strip().replace('s', '')
                    parsed["best_times"]["medium"] = int(time_str)
                except:
                    pass
            
            elif "Trudny:" in line and "s" in line:
                try:
                    time_str = line.split(':')[-1].strip().replace('s', '')
                    parsed["best_times"]["hard"] = int(time_str)
                except:
                    pass
        
        return parsed
    
    async def generate_report(self, period: str = "week") -> Dict:
        """
        Generuj raport za okres
        
        Args:
            period: day, week, month, all
        """
        logger.info("📝 Generating report for period: %s", period)
        
        stats = await self.analyze()
        
        if stats["status"] != "success":
            return stats
        
        parsed = stats["parsed"]
        
        # Oblicz metryki
        avg_games_per_player = (
            parsed["total_games"] / max(parsed["unique_players"], 1)
        )
        
        report = f"""
📊 Raport za okres: {period}

🎮 **Podstawowe statystyki:**
- Rozegranych gier: {parsed['total_games']}
- Unikalnych graczy: {parsed['unique_players']}
- Średnia gier/gracz: {avg_games_per_player:.1f}

🏆 **Najlepsze czasy:**
- 🟢 Łatwy: {parsed['best_times'].get('easy', 'N/A')}s
- 🟡 Średni: {parsed['best_times'].get('medium', 'N/A')}s
- 🔴 Trudny: {parsed['best_times'].get('hard', 'N/A')}s

📈 **Wnioski:**
- Aktywność graczy: {'wysoka' if avg_games_per_player > 3 else 'średnia' if avg_games_per_player > 1 else 'niska'}
- Najpopularniejszy poziom: (do implementacji)
"""
        
        return {
            "status": "success",
            "agent": "data",
            "period": period,
            "report": report,
            "metrics": {
                "total_games": parsed["total_games"],
                "unique_players": parsed["unique_players"],
                "avg_games_per_player": avg_games_per_player,
                "best_times": parsed["best_times"]
            }
        }
    
    async def compare_players(self, player1: str, player2: str) -> Dict:
        """Porównaj dwóch graczy (do implementacji)"""
        logger.info("⚖️  Comparing players: %s vs %s", player1, player2)
        
        # TODO: Implement player comparison
        return {
            "status": "not_implemented",
            "agent": "data",
            "message": "Player comparison coming soon"
        }
    
    async def health_check(self) -> Dict:
        """Sprawdź czy resources są dostępne"""
        try:
            async with stdio_client(self.mcp_server) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    resources = await session.list_resources()
                    
                    return {
                        "status": "ok",
                        "resources_count": len(resources.resources)
                    }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
