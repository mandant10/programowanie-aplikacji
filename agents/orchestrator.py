#!/usr/bin/env python3
"""
Main Orchestrator Agent - koordynuje wszystkie agenty
"""

import asyncio
from typing import Dict, List, Any, Optional
import json
import logging

# Importy agentów (będą stworzone)
from agents.game_agent import GameAgent
from agents.data_agent import DataAgent
from agents.mcp_agent import MCPAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """Główny orchestrator - koordynuje wszystkie agenty"""
    
    def __init__(self, config_path: str = "agents/config/agents.json"):
        self.config = self._load_config(config_path)
        self.agents = {
            'game': GameAgent(),
            'data': DataAgent(),
            'mcp': MCPAgent(),
        }
        logger.info("🎯 Orchestrator initialized with agents: %s", list(self.agents.keys()))
    
    def _load_config(self, path: str) -> Dict:
        """Załaduj konfigurację agentów"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Config not found, using defaults")
            return {
                "orchestrator": {
                    "max_concurrent_agents": 5,
                    "timeout": 30
                }
            }
    
    async def process_request(self, request: str) -> Dict[str, Any]:
        """
        Przetwarza request użytkownika i deleguje do odpowiednich agentów
        
        Args:
            request: Request od użytkownika (naturalny język)
            
        Returns:
            Wynik przetworzenia przez agenty
        """
        logger.info("📥 Processing request: %s", request)
        
        try:
            # Analiza intencji
            intent = self._analyze_intent(request)
            logger.info("🧠 Detected intent: %s", intent)
            
            # Routing do agentów
            if intent == 'get_scores':
                return await self._handle_get_scores(request)
                
            elif intent == 'submit_score':
                return await self._handle_submit_score(request)
                
            elif intent == 'analytics':
                return await self._handle_analytics(request)
                
            elif intent == 'complex':
                return await self._handle_complex(request)
                
            else:
                return {
                    "status": "error",
                    "error": "Unknown intent",
                    "suggestion": "Try: 'Pokaż wyniki' or 'Dodaj wynik Jan, easy, 120s'"
                }
                
        except Exception as e:
            logger.error("❌ Error processing request: %s", e)
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _analyze_intent(self, request: str) -> str:
        """
        Analizuje intencję użytkownika
        W produkcji można użyć LLM do lepszej analizy
        """
        request_lower = request.lower()
        
        # Keywords mapping
        if any(word in request_lower for word in ['wyniki', 'scores', 'top', 'ranking', 'najlepsi', 'pokaż']):
            return 'get_scores'
        
        if any(word in request_lower for word in ['dodaj', 'zapisz', 'submit', 'nowy wynik']):
            return 'submit_score'
        
        if any(word in request_lower for word in ['analiza', 'statystyki', 'raport', 'stats']):
            return 'analytics'
        
        if any(word in request_lower for word in ['wszystko', 'pełny', 'kompletny']):
            return 'complex'
        
        return 'unknown'
    
    async def _handle_get_scores(self, request: str) -> Dict:
        """Obsługa pobierania wyników"""
        # Ekstrakcja parametrów (uproszczone)
        difficulty = None
        if 'easy' in request.lower():
            difficulty = 'easy'
        elif 'medium' in request.lower():
            difficulty = 'medium'
        elif 'hard' in request.lower():
            difficulty = 'hard'
        
        # Limit
        limit = 10
        for word in request.split():
            if word.isdigit():
                limit = int(word)
                break
        
        # Deleguj do GameAgent
        result = await self.agents['game'].get_scores(difficulty, limit)
        return result
    
    async def _handle_submit_score(self, request: str) -> Dict:
        """Obsługa zapisywania wyniku"""
        # Parsowanie (uproszczone - w produkcji użyj LLM)
        # Format: "Dodaj wynik Jan, easy, 120"
        parts = request.split(',')
        
        if len(parts) < 3:
            return {
                "status": "error",
                "error": "Invalid format. Use: 'Dodaj wynik [name], [difficulty], [time]'"
            }
        
        player_name = parts[0].split()[-1].strip()
        difficulty = parts[1].strip()
        time_seconds = int(''.join(filter(str.isdigit, parts[2])))
        
        # Walidacja
        if not await self.agents['game'].validate_score(time_seconds, difficulty):
            return {
                "status": "error",
                "error": "Invalid score - time too low for difficulty"
            }
        
        # Zapisz
        result = await self.agents['game'].submit_score(player_name, difficulty, time_seconds)
        return result
    
    async def _handle_analytics(self, request: str) -> Dict:
        """Obsługa analiz"""
        result = await self.agents['data'].analyze()
        return result
    
    async def _handle_complex(self, request: str) -> Dict:
        """Obsługa złożonych requestów - wiele agentów równolegle"""
        logger.info("🔄 Running multi-agent collaboration")
        
        # Uruchom równolegle
        tasks = [
            self.agents['game'].get_scores(limit=5),
            self.agents['data'].analyze(),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "status": "success",
            "scores": results[0] if not isinstance(results[0], Exception) else str(results[0]),
            "analytics": results[1] if not isinstance(results[1], Exception) else str(results[1])
        }
    
    async def health_check(self) -> Dict:
        """Sprawdź status wszystkich agentów"""
        health = {}
        
        for name, agent in self.agents.items():
            try:
                # Każdy agent powinien mieć health_check()
                if hasattr(agent, 'health_check'):
                    health[name] = await agent.health_check()
                else:
                    health[name] = {"status": "unknown"}
            except Exception as e:
                health[name] = {"status": "error", "error": str(e)}
        
        return {
            "status": "ok" if all(h.get("status") != "error" for h in health.values()) else "degraded",
            "agents": health
        }


async def main():
    """Demo użycia orchestratora"""
    orchestrator = OrchestratorAgent()
    
    print("🤖 Orchestrator Agent Demo\n")
    
    # Test 1: Pobierz wyniki
    print("=" * 60)
    print("Test 1: Pobierz wyniki")
    result = await orchestrator.process_request("Pokaż top 5 wyników easy")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Test 2: Analiza
    print("\n" + "=" * 60)
    print("Test 2: Analiza statystyk")
    result = await orchestrator.process_request("Pokaż statystyki")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Test 3: Health check
    print("\n" + "=" * 60)
    print("Test 3: Health check")
    health = await orchestrator.health_check()
    print(json.dumps(health, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
