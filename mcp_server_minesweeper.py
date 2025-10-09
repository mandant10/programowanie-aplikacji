#!/usr/bin/env python3
"""
MCP Server dla MinesweeperAPI
Udostępnia narzędzia do zarządzania grą Saper przez API
"""

import json
import httpx
from mcp.server import FastMCP

# Inicjalizacja FastMCP server
mcp = FastMCP("minesweeper-api")

# Konfiguracja API
API_BASE = "http://localhost:5022/api"

@mcp.tool()
async def get_scores(difficulty: str = "", limit: int = 10) -> str:
    """🏆 Pobierz najlepsze wyniki z gry Saper
    
    Args:
        difficulty: Poziom trudności (easy, medium, hard) - opcjonalne
        limit: Maksymalna liczba wyników (1-100)
    
    Returns:
        Sformatowana lista najlepszych wyników
    """
    try:
        params = {"limit": min(limit, 100)}
        if difficulty and difficulty in ["easy", "medium", "hard"]:
            params["difficulty"] = difficulty
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE}/scores", params=params)
            response.raise_for_status()
            scores = response.json()
            
            if not scores:
                return "📊 Brak wyników - nikt jeszcze nie zagrał!"
            
            # Formatowanie wyników
            result = f"🏆 Top {len(scores)} wyników"
            if difficulty:
                result += f" ({difficulty})"
            result += ":\n\n"
            
            for i, score in enumerate(scores, 1):
                time_str = f"{score['timeSeconds']}s"
                result += f"{i}. {score['playerName']} - {time_str} ({score['difficulty']})\n"
                
            return result
            
    except httpx.RequestError as e:
        return f"❌ Błąd połączenia z API: {e}"
    except Exception as e:
        return f"❌ Błąd: {e}"

@mcp.tool()
async def submit_score(player_name: str, difficulty: str, time_seconds: int) -> str:
    """📝 Wyślij nowy wynik do gry Saper
    
    Args:
        player_name: Nazwa gracza (2-50 znaków)
        difficulty: Poziom trudności (easy, medium, hard)
        time_seconds: Czas gry w sekundach (1-9999)
    
    Returns:
        Potwierdzenie zapisu lub błąd
    """
    try:
        # Walidacja
        if not (2 <= len(player_name) <= 50):
            return "❌ Nazwa gracza musi mieć 2-50 znaków"
        
        if difficulty not in ["easy", "medium", "hard"]:
            return "❌ Poziom musi być: easy, medium lub hard"
            
        if not (1 <= time_seconds <= 9999):
            return "❌ Czas musi być w zakresie 1-9999 sekund"
        
        payload = {
            "playerName": player_name,
            "difficulty": difficulty,
            "timeSeconds": time_seconds
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_BASE}/scores", json=payload)
            response.raise_for_status()
            result = response.json()
            
            return f"✅ Wynik zapisany!\n🎮 {player_name}: {time_seconds}s ({difficulty})\n📊 ID: {result.get('id', 'N/A')}"
            
    except httpx.HTTPStatusError as e:
        return f"❌ Błąd HTTP {e.response.status_code}: {e.response.text}"
    except Exception as e:
        return f"❌ Błąd: {e}"

@mcp.tool()
async def get_player_progress(player_name: str) -> str:
    """🎯 Pobierz postęp gracza i odblokowane nagrody
    
    Args:
        player_name: Nazwa gracza
    
    Returns:
        Szczegółowy postęp gracza i status nagród
    """
    try:
        if not (2 <= len(player_name) <= 50):
            return "❌ Nazwa gracza musi mieć 2-50 znaków"
        
        async with httpx.AsyncClient() as client:
            # Postęp gracza
            progress_response = await client.get(f"{API_BASE}/progress/{player_name}")
            progress_response.raise_for_status()
            progress = progress_response.json()
            
            # Nagrody gracza
            rewards_response = await client.get(f"{API_BASE}/progress/{player_name}/rewards")
            rewards_response.raise_for_status()
            rewards = rewards_response.json()
            
            # Formatowanie odpowiedzi
            result = f"🎯 Postęp gracza: {player_name}\n\n"
            result += f"📈 Ukończone poziomy:\n"
            result += f"  🟢 Łatwy: {'✅' if progress.get('easyCompleted') else '❌'}\n"
            result += f"  🟡 Średni: {'✅' if progress.get('mediumCompleted') else '❌'}\n"
            result += f"  🔴 Trudny: {'✅' if progress.get('hardCompleted') else '❌'}\n\n"
            
            result += f"🎨 Aktualna tekstura: {progress.get('currentTexture', 'brak')}\n\n"
            
            result += f"🏆 Odblokowane nagrody:\n"
            for reward in rewards:
                status = "🔓" if reward.get('isUnlocked') else "🔒"
                result += f"  {status} {reward.get('name', 'Nieznana')}\n"
            
            return result
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"❌ Gracz '{player_name}' nie został znaleziony"
        return f"❌ Błąd HTTP {e.response.status_code}"
    except Exception as e:
        return f"❌ Błąd: {e}"

@mcp.resource("mcp://api-docs")
async def get_api_docs() -> str:
    """📖 Dokumentacja API gry Saper"""
    return """# 🎮 MinesweeperAPI Documentation

## 🎯 Endpoints

### 🏆 Scores (Wyniki)
GET  /api/scores?difficulty={easy|medium|hard}&limit={1-100}
POST /api/scores
     Content-Type: application/json
     {
       "playerName": "string (2-50 chars)",
       "difficulty": "easy|medium|hard", 
       "timeSeconds": number (1-9999)
     }

### 🎯 Progress (Postęp)
GET /api/progress/{playerName}
GET /api/progress/{playerName}/rewards

## 🎮 Poziomy trudności

| Poziom | Rozmiar | Miny | Limit czasu |
|--------|---------|------|-------------|
| easy   | 9x9     | 10   | 10 min      |
| medium | 16x16   | 40   | 40 min      |
| hard   | 16x30   | 99   | 99 min      |

## 🏆 System nagród

- 🥉 Brązowa tekstura: Ukończ poziom łatwy
- 🥈 Srebrna tekstura: Ukończ poziom średni  
- 🥇 Złota tekstura: Ukończ poziom trudny

Aktywna tekstura to najwyższa odblokowana.
"""

@mcp.resource("mcp://game-stats")
async def get_game_stats() -> str:
    """📊 Statystyki gry w czasie rzeczywistym"""
    try:
        async with httpx.AsyncClient() as client:
            # Pobierz wszystkie wyniki (max 100 - limit API)
            response = await client.get(f"{API_BASE}/scores?limit=100")
            response.raise_for_status()
            scores = response.json()
            
            if not scores:
                return "📊 Brak danych - nie ma jeszcze żadnych wyników"
            
            # Analiza statystyk
            total_games = len(scores)
            easy_games = len([s for s in scores if s['difficulty'] == 'easy'])
            medium_games = len([s for s in scores if s['difficulty'] == 'medium'])
            hard_games = len([s for s in scores if s['difficulty'] == 'hard'])
            
            unique_players = len(set(s['playerName'] for s in scores))
            
            # Najlepsze czasy
            best_easy = min([s['timeSeconds'] for s in scores if s['difficulty'] == 'easy'], default=0)
            best_medium = min([s['timeSeconds'] for s in scores if s['difficulty'] == 'medium'], default=0)
            best_hard = min([s['timeSeconds'] for s in scores if s['difficulty'] == 'hard'], default=0)
            
            stats = f"""📊 Statystyki gry Saper

🎮 Rozegranych gier: {total_games}
👥 Unikalnych graczy: {unique_players}

📈 Gry według poziomu:
  🟢 Łatwy:  {easy_games} ({easy_games/total_games*100:.1f}%)
  🟡 Średni: {medium_games} ({medium_games/total_games*100:.1f}%)
  🔴 Trudny: {hard_games} ({hard_games/total_games*100:.1f}%)

🏆 Najlepsze czasy:
  🟢 Łatwy:  {best_easy}s
  🟡 Średni: {best_medium}s  
  🔴 Trudny: {best_hard}s

📊 Średnia gier na gracza: {total_games/unique_players:.1f}
"""
            return stats
            
    except Exception as e:
        return f"❌ Błąd pobierania statystyk: {e}"

if __name__ == "__main__":
    print("🚀 MCP Server dla MinesweeperAPI")
    print(f"📡 API endpoint: {API_BASE}")
    print("🔧 Uruchamiam serwer...")
    mcp.run()