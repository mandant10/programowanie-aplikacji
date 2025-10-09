#!/usr/bin/env python3
"""
Interactive Agent Demo - pełne testy wszystkich agentów
"""

import asyncio
import json
from agents import OrchestratorAgent

async def test_game_agent():
    """Test GameAgent - operacje na grze"""
    print("=" * 70)
    print("🎮 TEST 1: GameAgent - Operacje na grze")
    print("=" * 70)
    
    orch = OrchestratorAgent()
    game_agent = orch.agents['game']
    
    # 1. Pobierz wyniki
    print("\n📊 1.1 Pobierz top 3 wyniki (easy):")
    result = await game_agent.get_scores(difficulty="easy", limit=3)
    print(result['data'])
    
    # 2. Walidacja wyniku
    print("\n✅ 1.2 Waliduj wynik (120s, easy):")
    is_valid = await game_agent.validate_score(120, "easy")
    print(f"Wynik 120s dla 'easy' jest {'✅ poprawny' if is_valid else '❌ niepoprawny'}")
    
    print("\n❌ 1.3 Waliduj podejrzany wynik (5s, easy - za szybko!):")
    is_valid = await game_agent.validate_score(5, "easy")
    print(f"Wynik 5s dla 'easy' jest {'✅ poprawny' if is_valid else '❌ niepoprawny (za szybko!)'}")
    
    # 3. Zapisz wynik
    print("\n💾 1.4 Zapisz nowy wynik (AgentTest, medium, 180s):")
    result = await game_agent.submit_score("AgentTest", "medium", 180)
    print(result['message'])
    
    # 4. Postęp gracza
    print("\n🎯 1.5 Sprawdź postęp gracza 'TestDemo2':")
    result = await game_agent.get_player_progress("TestDemo2")
    print(result['data'])
    
    # 5. Health check
    print("\n🏥 1.6 Health check GameAgent:")
    health = await game_agent.health_check()
    print(f"Status: {health['status']}, Tools: {health.get('tools_count', 'N/A')}")

async def test_data_agent():
    """Test DataAgent - analityka"""
    print("\n\n" + "=" * 70)
    print("📊 TEST 2: DataAgent - Analityka i raporty")
    print("=" * 70)
    
    orch = OrchestratorAgent()
    data_agent = orch.agents['data']
    
    # 1. Analiza statystyk
    print("\n📈 2.1 Analiza statystyk gry:")
    result = await data_agent.analyze()
    print("\nSurowe statystyki (pierwsze 300 znaków):")
    print(result['raw_stats'][:300] + "...")
    
    print("\n📊 Sparsowane dane:")
    print(json.dumps(result['parsed'], indent=2, ensure_ascii=False))
    
    # 2. Generuj raport
    print("\n📝 2.2 Raport tygodniowy:")
    result = await data_agent.generate_report("week")
    print(result['report'])
    
    print("\n📈 Metryki:")
    print(json.dumps(result['metrics'], indent=2, ensure_ascii=False))
    
    # 3. Health check
    print("\n🏥 2.3 Health check DataAgent:")
    health = await data_agent.health_check()
    print(f"Status: {health['status']}, Resources: {health.get('resources_count', 'N/A')}")

async def test_mcp_agent():
    """Test MCPAgent - zarządzanie MCP"""
    print("\n\n" + "=" * 70)
    print("🔧 TEST 3: MCPAgent - Zarządzanie MCP")
    print("=" * 70)
    
    orch = OrchestratorAgent()
    mcp_agent = orch.agents['mcp']
    
    # 1. Lista narzędzi
    print("\n🛠️  3.1 Lista dostępnych narzędzi MCP:")
    result = await mcp_agent.list_tools()
    for i, tool in enumerate(result['tools'], 1):
        print(f"\n  {i}. {tool['name']}")
        print(f"     {tool['description']}")
    
    # 2. Lista zasobów
    print("\n\n📚 3.2 Lista dostępnych zasobów MCP:")
    result = await mcp_agent.list_resources()
    for i, resource in enumerate(result['resources'], 1):
        print(f"\n  {i}. {resource['uri']}")
        print(f"     {resource['name']}")
    
    # 3. Info o serwerze
    print("\n\n📡 3.3 Informacje o serwerze MCP:")
    result = await mcp_agent.get_server_info()
    info = result['server_info']
    print(f"  Protocol version: {info['protocol_version']}")
    print(f"  Tools: {info['tools_count']}")
    print(f"  Resources: {info['resources_count']}")
    print(f"  Capabilities: {str(info['capabilities'])}")

async def test_orchestrator():
    """Test Orchestrator - inteligentne przetwarzanie"""
    print("\n\n" + "=" * 70)
    print("🎯 TEST 4: Orchestrator - Natural Language Processing")
    print("=" * 70)
    
    orch = OrchestratorAgent()
    
    # Przykładowe requesty
    requests = [
        "Pokaż top 5 wyników",
        "Pokaż top 3 easy",
        "Pokaż statystyki",
        "Analiza gry",
        "Wszystko - pełny raport"
    ]
    
    for i, req in enumerate(requests, 1):
        print(f"\n📥 4.{i} Request: '{req}'")
        result = await orch.process_request(req)
        
        # Pokaż tylko status i pierwsze 150 znaków
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Agent: {result.get('agent', 'orchestrator')}")
        
        if 'data' in result:
            data_preview = str(result['data'])[:150]
            print(f"   Data: {data_preview}...")
        elif 'scores' in result:
            print(f"   Scores: {str(result['scores'])[:100]}...")
            print(f"   Analytics: {str(result['analytics'])[:100]}...")

async def test_health_check_all():
    """Test Health Check wszystkich agentów"""
    print("\n\n" + "=" * 70)
    print("🏥 TEST 5: Health Check - Wszystkie agenty")
    print("=" * 70)
    
    orch = OrchestratorAgent()
    
    print("\n🔍 Sprawdzam status wszystkich agentów...\n")
    health = await orch.health_check()
    
    print(f"Overall Status: {'✅ OK' if health['status'] == 'ok' else '⚠️  DEGRADED'}\n")
    
    for agent_name, agent_health in health['agents'].items():
        status_icon = "✅" if agent_health['status'] == 'ok' else "❌"
        print(f"{status_icon} {agent_name:15} - {agent_health['status']}")
        
        # Dodatkowe info
        if 'tools_count' in agent_health:
            print(f"   └─ Tools: {agent_health['tools_count']}")
        if 'resources_count' in agent_health:
            print(f"   └─ Resources: {agent_health['resources_count']}")
        if 'protocol_version' in agent_health:
            print(f"   └─ Protocol: {agent_health['protocol_version']}")

async def test_parallel_execution():
    """Test równoległego wykonania wielu agentów"""
    print("\n\n" + "=" * 70)
    print("⚡ TEST 6: Równoległe wykonanie (Performance)")
    print("=" * 70)
    
    orch = OrchestratorAgent()
    
    print("\n🚀 Uruchamiam 3 agenty równolegle...\n")
    
    import time
    start = time.time()
    
    # Równoległe wywołania
    tasks = [
        orch.agents['game'].get_scores(limit=5),
        orch.agents['data'].analyze(),
        orch.agents['mcp'].list_tools(),
    ]
    
    results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start
    
    print(f"✅ Zakończono w {elapsed:.2f}s")
    print(f"\n📊 Wyniki:")
    print(f"  1. GameAgent: {results[0]['status']}")
    print(f"  2. DataAgent: {results[1]['status']}")
    print(f"  3. MCPAgent: {results[2]['status']} ({results[2]['count']} tools)")

async def main():
    """Uruchom wszystkie testy"""
    print("\n")
    print("🤖" * 35)
    print("     INTERACTIVE AGENT DEMO - Kompleksowe testy")
    print("🤖" * 35)
    print("\n")
    
    try:
        await test_game_agent()
        await test_data_agent()
        await test_mcp_agent()
        await test_orchestrator()
        await test_health_check_all()
        await test_parallel_execution()
        
        print("\n\n" + "=" * 70)
        print("✅ WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE!")
        print("=" * 70)
        print("\n💡 Co dalej?")
        print("  - Sprawdź kod w: agents/")
        print("  - Dokumentacja: .github/AGENTS_GUIDE.md")
        print("  - Użyj agentów w swoim kodzie!")
        print("\n")
        
    except Exception as e:
        print(f"\n\n❌ BŁĄD: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
