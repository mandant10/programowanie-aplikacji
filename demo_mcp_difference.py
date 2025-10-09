#!/usr/bin/env python3
"""
DEMONSTRACJA: Różnica między zwykłym API a MCP Server

Ten skrypt pokazuje DOKŁADNIE czym różni się korzystanie z MCP
od ręcznego kopiowania danych z API.
"""

import asyncio
import httpx
import time

API_BASE = "http://localhost:5022/api"

print("="*70)
print(" DEMONSTRACJA: Zwykły endpoint VS MCP Server")
print("="*70)

# ============================================================================
# SCENARIUSZ: "Sprawdź top 3 wyniki i dodaj nowy wynik dla gracza TestDemo"
# ============================================================================

print("\n" + "─"*70)
print("📋 ZADANIE: Sprawdź top 3 wyniki i dodaj nowy wynik 'TestDemo: 95s easy'")
print("─"*70)

# ============================================================================
# SPOSÓB 1: BEZ MCP (symulacja interakcji użytkownik-AI)
# ============================================================================

print("\n\n🔴 SPOSÓB 1: BEZ MCP (ręcznie)")
print("─"*70)

start_manual = time.time()

print("\n👤 TY: 'Pokaż mi top 3 wyniki'")
print("🤖 AI: 'Nie mam dostępu do API. Wykonaj: curl http://localhost:5022/api/scores?limit=3'")
print("\n👤 TY: *kopiujesz polecenie do terminala*")
print("   ⏳ Wykonuję curl...")

# Symulacja: użytkownik wykonuje curl
print("   $ curl http://localhost:5022/api/scores?limit=3")

async def manual_get_scores():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/scores?limit=3")
        return response.json()

scores = asyncio.run(manual_get_scores())
print(f"   Odpowiedź API (surowy JSON):")
for score in scores[:3]:
    print(f"   {score}")

print("\n👤 TY: *kopiujesz JSON i wklejasz do AI*")
print("   ⏳ Wklejam...")

print(f"\n🤖 AI: 'Widzę {len(scores)} wyników. Top 3:'")
for i, score in enumerate(scores[:3], 1):
    print(f"        {i}. {score['playerName']} - {score['timeSeconds']}s ({score['difficulty']})")

print("\n👤 TY: 'Teraz dodaj wynik TestDemo: 95s easy'")
print("🤖 AI: 'Wykonaj to polecenie:'")
print("       curl -X POST http://localhost:5022/api/scores \\")
print("            -H 'Content-Type: application/json' \\")
print("            -d '{\"playerName\":\"TestDemo\",\"difficulty\":\"easy\",\"timeSeconds\":95}'")

print("\n👤 TY: *kopiujesz polecenie i wykonujesz*")
print("   ⏳ Wykonuję POST...")

async def manual_submit_score():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/scores",
            json={"playerName": "TestDemo", "difficulty": "easy", "timeSeconds": 95}
        )
        return response.json()

result = asyncio.run(manual_submit_score())
print(f"   Odpowiedź API: {result}")

print("\n👤 TY: *kopiujesz wynik i wklejasz do AI*")
print("   ⏳ Wklejam...")

print("\n🤖 AI: '✅ Wynik został zapisany! ID: " + str(result.get('id', 'N/A')) + "'")

end_manual = time.time()
manual_time = end_manual - start_manual

print(f"\n⏱️  CZAS (bez MCP): {manual_time:.1f}s")
print(f"📊 LICZBA AKCJI: 4 kopie-wklej, 2 polecenia curl, 4 naciśnięcia ENTER")

# ============================================================================
# SPOSÓB 2: Z MCP (automatyczny)
# ============================================================================

print("\n\n" + "="*70)
print("🟢 SPOSÓB 2: Z MCP (automatycznie)")
print("─"*70)

start_mcp = time.time()

print("\n👤 TY: 'Pokaż mi top 3 wyniki i dodaj nowy wynik TestDemo: 95s easy'")
print("\n🤖 AI: *wywołuje narzędzia MCP automatycznie...*")

# Symulacja wywołania MCP tools
import sys
sys.path.insert(0, '/workspaces/programowanie-aplikacji')
from mcp_server_minesweeper import get_scores, submit_score

async def mcp_demo():
    print("   [MCP] Wywołuję get_scores(limit=3)...")
    scores_result = await get_scores(limit=3)
    
    print("   [MCP] Wywołuję submit_score('TestDemo2', 'easy', 95)...")
    submit_result = await submit_score("TestDemo2", "easy", 95)
    
    return scores_result, submit_result

scores_text, submit_text = asyncio.run(mcp_demo())

print("\n🤖 AI: 'Gotowe! Oto wyniki:\n")
print(scores_text)
print("\nI zapisałem nowy wynik:\n")
print(submit_text + "'")

end_mcp = time.time()
mcp_time = end_mcp - start_mcp

print(f"\n⏱️  CZAS (z MCP): {mcp_time:.1f}s")
print(f"📊 LICZBA AKCJI: 0 kopii-wklej, 0 poleceń curl, 1 prompt")

# ============================================================================
# PORÓWNANIE
# ============================================================================

print("\n\n" + "="*70)
print(" 📊 PORÓWNANIE EFEKTYWNOŚCI")
print("="*70)

print(f"\n{'Metryka':<30} {'Bez MCP':<20} {'Z MCP':<20}")
print("─"*70)
print(f"{'Czas wykonania':<30} {manual_time:.1f}s {' '*16} {mcp_time:.1f}s")
print(f"{'Kopie-wklej':<30} {'4':<20} {'0':<20}")
print(f"{'Polecenia curl':<30} {'2':<20} {'0':<20}")
print(f"{'Przełączenia kontekstu':<30} {'~6':<20} {'1':<20}")
print(f"{'Wysiłek użytkownika':<30} {'Wysoki ⚠️':<20} {'Niski ✅':<20}")
print(f"{'Ryzyko błędu':<30} {'Średnie':<20} {'Niskie':<20}")
print(f"{'Możliwość automatyzacji':<30} {'Nie ❌':<20} {'Tak ✅':<20}")

print("\n" + "="*70)
print(" 🎯 WNIOSKI")
print("="*70)

print("""
✅ Z MCP:
   - AI pracuje autonomicznie
   - Ty tylko kierujesz, AI wykonuje
   - Szybciej (mniej kroków)
   - Mniej podatne na błędy
   - Możliwość złożonych operacji (AI może wywołać 10 narzędzi po kolei)

❌ Bez MCP:
   - Ty jesteś "pośrednikiem" między AI a danymi
   - Każda operacja wymaga Twojej interwencji
   - Wolniejsze (dużo kopiowania)
   - Ryzyko literówek/błędów
   - Złożone operacje = żmudne

🎓 KLUCZOWA RÓŻNICA:
   MCP daje AI "ręce" do interakcji z Twoimi systemami.
   Bez MCP AI ma tylko "oczy" (widzi co mu pokażesz).
""")

print("="*70)
print(" Demo zakończone!")
print("="*70)
print("\n💡 Teraz rozumiesz czym jest MCP? To nie tylko 'endpoint jako tekst',")
print("   ale pełnoprawny interfejs pozwalający AI autonomicznie działać!")
