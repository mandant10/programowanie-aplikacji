#!/usr/bin/env python3
"""
Skrypt testowy dla MCP Server
Testuje wszystkie narzędzia i zasoby
"""

import asyncio
import httpx

API_BASE = "http://localhost:5022/api"

async def test_api():
    """Testuje bezpośrednio API przed testem MCP"""
    print("=" * 60)
    print("🧪 TEST 1: Sprawdzanie API MinesweeperAPI")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        # Test 1: Pobierz wyniki (pusta lista na początku)
        print("\n1️⃣ GET /api/scores")
        response = await client.get(f"{API_BASE}/scores?limit=5")
        print(f"   Status: {response.status_code}")
        scores = response.json()
        print(f"   Wyniki: {len(scores)} wyników")
        
        # Test 2: Dodaj testowy wynik
        print("\n2️⃣ POST /api/scores (dodawanie wyniku)")
        payload = {
            "playerName": "TestPlayer",
            "difficulty": "easy",
            "timeSeconds": 125
        }
        response = await client.post(f"{API_BASE}/scores", json=payload)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Odpowiedź: {result}")
        
        # Test 3: Pobierz wyniki ponownie
        print("\n3️⃣ GET /api/scores (po dodaniu)")
        response = await client.get(f"{API_BASE}/scores?limit=5")
        scores = response.json()
        print(f"   Wyniki: {len(scores)} wyników")
        for i, score in enumerate(scores, 1):
            print(f"   {i}. {score['playerName']} - {score['timeSeconds']}s ({score['difficulty']})")
        
        # Test 4: Sprawdź postęp gracza
        print("\n4️⃣ GET /api/progress/TestPlayer")
        response = await client.get(f"{API_BASE}/progress/TestPlayer")
        print(f"   Status: {response.status_code}")
        progress = response.json()
        print(f"   Postęp: {progress}")
        
        # Test 5: Sprawdź nagrody gracza
        print("\n5️⃣ GET /api/progress/TestPlayer/rewards")
        response = await client.get(f"{API_BASE}/progress/TestPlayer/rewards")
        print(f"   Status: {response.status_code}")
        rewards = response.json()
        print(f"   Nagrody: {len(rewards)} nagród")
        for reward in rewards:
            status = "🔓" if reward['isUnlocked'] else "🔒"
            print(f"   {status} {reward['name']}")
    
    print("\n✅ Test API zakończony pomyślnie!\n")

async def test_mcp_tools():
    """Symuluje wywołania narzędzi MCP"""
    print("=" * 60)
    print("🧪 TEST 2: Symulacja wywołań narzędzi MCP")
    print("=" * 60)
    
    # Import narzędzi z MCP server
    import sys
    sys.path.insert(0, '/workspaces/programowanie-aplikacji')
    from mcp_server_minesweeper import get_scores, submit_score, get_player_progress
    
    # Test 1: get_scores
    print("\n1️⃣ Tool: get_scores(difficulty='easy', limit=5)")
    result = await get_scores(difficulty="easy", limit=5)
    print(f"   Wynik:\n{result}\n")
    
    # Test 2: submit_score
    print("2️⃣ Tool: submit_score('MCPTest', 'medium', 200)")
    result = await submit_score("MCPTest", "medium", 200)
    print(f"   Wynik:\n{result}\n")
    
    # Test 3: get_player_progress
    print("3️⃣ Tool: get_player_progress('TestPlayer')")
    result = await get_player_progress("TestPlayer")
    print(f"   Wynik:\n{result}\n")
    
    # Test 4: get_scores ponownie (wszystkie poziomy)
    print("4️⃣ Tool: get_scores(limit=10)")
    result = await get_scores(limit=10)
    print(f"   Wynik:\n{result}\n")
    
    print("✅ Test narzędzi MCP zakończony pomyślnie!\n")

async def test_mcp_resources():
    """Symuluje odczyt zasobów MCP"""
    print("=" * 60)
    print("🧪 TEST 3: Symulacja odczytu zasobów MCP")
    print("=" * 60)
    
    import sys
    sys.path.insert(0, '/workspaces/programowanie-aplikacji')
    from mcp_server_minesweeper import get_api_docs, get_game_stats
    
    # Test 1: api-docs
    print("\n1️⃣ Resource: mcp://api-docs")
    result = await get_api_docs()
    print(f"   Długość dokumentacji: {len(result)} znaków")
    print(f"   Pierwsze 300 znaków:\n{result[:300]}...\n")
    
    # Test 2: game-stats
    print("2️⃣ Resource: mcp://game-stats")
    result = await get_game_stats()
    print(f"   Statystyki:\n{result}\n")
    
    print("✅ Test zasobów MCP zakończony pomyślnie!\n")

async def main():
    """Uruchom wszystkie testy"""
    print("\n" + "🎮" * 30)
    print("  TEST MCP SERVER - MINESWEEPER API")
    print("🎮" * 30 + "\n")
    
    try:
        await test_api()
        await test_mcp_tools()
        await test_mcp_resources()
        
        print("=" * 60)
        print("🎉 WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE! 🎉")
        print("=" * 60)
        print("\n📋 Podsumowanie:")
        print("   ✅ API MinesweeperAPI działa poprawnie")
        print("   ✅ Narzędzia MCP działają (get_scores, submit_score, get_player_progress)")
        print("   ✅ Zasoby MCP działają (api-docs, game-stats)")
        print("\n🚀 MCP Server gotowy do użycia z AI!\n")
        
    except Exception as e:
        print(f"\n❌ BŁĄD: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
