# Model Context Protocol (MCP) - Dokładny opis zawartości

## 🎯 Co to jest MCP Protocol

MCP to protokół komunikacji oparty na **JSON-RPC 2.0**, który umożliwia standaryzowaną wymianę informacji między AI a zewnętrznymi systemami.

## 📋 Struktura protokołu MCP

### 1. **Warstwa transportowa** (JSON-RPC 2.0)
```json
{
  "jsonrpc": "2.0",
  "id": "request_id",
  "method": "nazwa_metody",
  "params": { /* parametry */ }
}
```

### 2. **Wersjonowanie**
- Format: `YYYY-MM-DD` (np. `2025-06-18`)
- Negocjacja wersji podczas inicjalizacji
- Wsteczna kompatybilność

### 3. **Cykl życia połączenia**
```
Initialize → Tools/Resources Discovery → Method Calls → Shutdown
```

## 🔧 Główne komponenty protokołu

### **1. Tools (Narzędzia)**
Funkcje, które AI może wywoływać:

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_scores",
    "arguments": {
      "difficulty": "easy",
      "limit": 10
    }
  }
}
```

### **2. Resources (Zasoby)**  
Źródła danych, które AI może czytać:

```json
{
  "method": "resources/read",
  "params": {
    "uri": "file:///path/to/file.txt"
  }
}
```

### **3. Prompts (Szablony)**
Gotowe prompty z parametrami:

```json
{
  "method": "prompts/get", 
  "params": {
    "name": "analyze_code",
    "arguments": {
      "language": "csharp",
      "file_path": "/src/Controllers/ScoresController.cs"
    }
  }
}
```

### **4. Notifications (Powiadomienia)**
Asymetryczne aktualizacje:

```json
{
  "method": "notifications/resources/updated",
  "params": {
    "uri": "file:///database.db"
  }
}
```

## 📨 Wszystkie metody protokołu MCP

### **Lifecycle (Cykl życia)**
```
initialize          - Inicjalizacja połączenia
initialized         - Potwierdzenie inicjalizacji  
ping               - Test połączenia
shutdown           - Zamknięcie sesji
```

### **Tools (Narzędzia)**
```
tools/list         - Lista dostępnych narzędzi
tools/call         - Wywołanie narzędzia
```

### **Resources (Zasoby)**
```
resources/list     - Lista dostępnych zasobów
resources/read     - Odczyt zasobu
resources/subscribe - Subskrypcja zmian
resources/unsubscribe - Anulowanie subskrypcji
```

### **Prompts (Szablony)**
```
prompts/list       - Lista dostępnych promptów
prompts/get        - Pobranie promptu z parametrami
```

### **Logging (Logowanie)**
```
logging/setLevel   - Ustawienie poziomu logów
```

### **Notifications (Powiadomienia)**
```
notifications/initialized     - Serwer gotowy
notifications/progress       - Postęp długiej operacji
notifications/message        - Komunikat do użytkownika
notifications/resources/updated - Zasób się zmienił
notifications/tools/updated  - Narzędzia się zmieniły
notifications/prompts/updated - Prompty się zmieniły
```

## 🎮 Przykład dla Twojego MinesweeperAPI

Poprawię Twój serwer MCP, żeby pokazać pełną strukturę protokołu:

```python
#!/usr/bin/env python3
"""
Kompletny MCP Server dla MinesweeperAPI
Pokazuje wszystkie elementy protokołu MCP
"""

import asyncio
import json
import httpx
from mcp import McpServer
from mcp.types import (
    TextContent, Tool, Resource, Prompt,
    LoggingLevel, CallToolResult
)

app = McpServer("minesweeper-api")
API_BASE = "http://localhost:5022/api"

# === TOOLS (Narzędzia) ===
@app.tool()
async def get_scores(difficulty: str = None, limit: int = 10) -> list[TextContent]:
    """🏆 Pobierz najlepsze wyniki z gry Saper
    
    Args:
        difficulty: easy, medium, hard (opcjonalne)
        limit: maksymalna liczba wyników (1-100)
    """
    params = {"limit": min(limit, 100)}
    if difficulty in ["easy", "medium", "hard"]:
        params["difficulty"] = difficulty
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE}/scores", params=params)
            response.raise_for_status()
            scores = response.json()
            
            # Formatowanie wyników
            result = f"🏆 Top {len(scores)} wyników"
            if difficulty:
                result += f" ({difficulty})"
            result += ":\n\n"
            
            for i, score in enumerate(scores, 1):
                time_str = f"{score['timeSeconds']}s"
                result += f"{i}. {score['playerName']} - {time_str} ({score['difficulty']})\n"
                
            return [TextContent(type="text", text=result)]
            
        except httpx.RequestError as e:
            return [TextContent(type="text", text=f"❌ Błąd połączenia: {e}")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Błąd: {e}")]

@app.tool()
async def submit_score(player_name: str, difficulty: str, time_seconds: int) -> list[TextContent]:
    """📝 Wyślij nowy wynik do gry Saper
    
    Args:
        player_name: nazwa gracza (2-50 znaków)
        difficulty: easy, medium, hard
        time_seconds: czas gry w sekundach (1-9999)
    """
    # Walidacja
    if not (2 <= len(player_name) <= 50):
        return [TextContent(type="text", text="❌ Nazwa gracza: 2-50 znaków")]
    
    if difficulty not in ["easy", "medium", "hard"]:
        return [TextContent(type="text", text="❌ Poziom: easy, medium lub hard")]
        
    if not (1 <= time_seconds <= 9999):
        return [TextContent(type="text", text="❌ Czas: 1-9999 sekund")]
    
    payload = {
        "playerName": player_name,
        "difficulty": difficulty,
        "timeSeconds": time_seconds
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{API_BASE}/scores", json=payload)
            response.raise_for_status()
            result = response.json()
            
            return [TextContent(
                type="text",
                text=f"✅ Wynik zapisany!\n🎮 {player_name}: {time_seconds}s ({difficulty})\n📊 ID: {result.get('id', 'N/A')}"
            )]
            
        except httpx.HTTPStatusError as e:
            return [TextContent(type="text", text=f"❌ Błąd HTTP {e.response.status_code}: {e.response.text}")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Błąd: {e}")]

@app.tool()
async def get_player_progress(player_name: str) -> list[TextContent]:
    """🎯 Pobierz postęp gracza i odblokowane nagrody
    
    Args:
        player_name: nazwa gracza
    """
    if not (2 <= len(player_name) <= 50):
        return [TextContent(type="text", text="❌ Nazwa gracza: 2-50 znaków")]
    
    async with httpx.AsyncClient() as client:
        try:
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
            
            return [TextContent(type="text", text=result)]
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return [TextContent(type="text", text=f"❌ Gracz '{player_name}' nie został znaleziony")]
            return [TextContent(type="text", text=f"❌ Błąd HTTP {e.response.status_code}")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Błąd: {e}")]

# === RESOURCES (Zasoby) ===
@app.resource("api-docs")
async def get_api_docs() -> str:
    """📖 Dokumentacja API gry Saper"""
    return """# 🎮 MinesweeperAPI Documentation

## 🎯 Endpoints

### 🏆 Scores (Wyniki)
```
GET  /api/scores?difficulty={easy|medium|hard}&limit={1-100}
POST /api/scores
     Content-Type: application/json
     {
       "playerName": "string (2-50 chars)",
       "difficulty": "easy|medium|hard", 
       "timeSeconds": number (1-9999)
     }
```

### 🎯 Progress (Postęp)
```
GET /api/progress/{playerName}
GET /api/progress/{playerName}/rewards
```

## 🎮 Poziomy trudności

| Poziom | Rozmiar | Miny | Limit czasu |
|--------|---------|------|-------------|
| easy   | 9x9     | 10   | 10 min      |
| medium | 16x16   | 40   | 40 min      |
| hard   | 16x30   | 99   | 99 min      |

## 🏆 System nagród

- 🥉 **Brązowa tekstura**: Ukończ poziom łatwy
- 🥈 **Srebrna tekstura**: Ukończ poziom średni  
- 🥇 **Złota tekstura**: Ukończ poziom trudny

Aktywna tekstura to najwyższa odblokowana.

## 🔧 Przykłady użycia

### Pobranie top 5 wyników (wszystkie poziomy):
```bash
curl "http://localhost:5022/api/scores?limit=5"
```

### Zapisanie wyniku:
```bash
curl -X POST "http://localhost:5022/api/scores" \\
  -H "Content-Type: application/json" \\
  -d '{"playerName":"Jan","difficulty":"easy","timeSeconds":125}'
```

### Sprawdzenie postępu:
```bash
curl "http://localhost:5022/api/progress/Jan"
curl "http://localhost:5022/api/progress/Jan/rewards"
```
"""

@app.resource("game-stats")
async def get_game_stats() -> str:
    """📊 Statystyki gry w czasie rzeczywistym"""
    async with httpx.AsyncClient() as client:
        try:
            # Pobierz wszystkie wyniki
            response = await client.get(f"{API_BASE}/scores?limit=1000")
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

🎮 **Rozegranych gier**: {total_games}
👥 **Unikalnych graczy**: {unique_players}

📈 **Gry według poziomu**:
  🟢 Łatwy:  {easy_games} ({easy_games/total_games*100:.1f}%)
  🟡 Średni: {medium_games} ({medium_games/total_games*100:.1f}%)
  🔴 Trudny: {hard_games} ({hard_games/total_games*100:.1f}%)

🏆 **Najlepsze czasy**:
  🟢 Łatwy:  {best_easy}s
  🟡 Średni: {best_medium}s  
  🔴 Trudny: {best_hard}s

📊 **Średnia gier na gracza**: {total_games/unique_players:.1f}
"""
            return stats
            
        except Exception as e:
            return f"❌ Błąd pobierania statystyk: {e}"

# === PROMPTS (Szablony) ===
@app.prompt("analyze-player")
async def analyze_player_prompt(player_name: str) -> str:
    """🔍 Wygeneruj prompt do analizy gracza
    
    Args:
        player_name: nazwa gracza do analizy
    """
    return f"""Przeanalizuj gracza '{player_name}' w grze Saper:

1. 📊 Pobierz statystyki gracza: get_player_progress("{player_name}")
2. 🏆 Sprawdź wyniki gracza: get_scores() i znajdź wszystkie wyniki dla "{player_name}"
3. 📈 Oceń umiejętności:
   - Poziom ukończonych poziomów
   - Porównanie czasów z najlepszymi wynikami
   - Konsystencja gry (rozrzut czasów)
   - Progresja (poprawa z czasem)

4. 🎯 Zasugeruj:
   - Na jakim poziomie powinien grać dalej
   - Jak może poprawić swoje wyniki
   - Czy jest gotowy na wyższy poziom trudności

Przedstaw analizę w czytelnej formie z emotkami i konkretnymi radami."""

@app.prompt("game-report")
async def game_report_prompt(period: str = "today") -> str:
    """📋 Wygeneruj raport z gry
    
    Args:
        period: okres raportu (today, week, month, all)
    """
    return f"""Wygeneruj raport aktywności gry Saper za okres: {period}

1. 📊 Pobierz ogólne statystyki: get_game_stats()
2. 🏆 Pobierz najlepsze wyniki: get_scores(limit=20)
3. 🎯 Przeanalizuj trendy:
   - Którzy gracze są najaktywniejszi
   - Jakie poziomy trudności są najpopularniejsze
   - Czy czasy się poprawiają (trend)
   - Top 5 graczy każdego poziomu

4. 📈 Zasugeruj ulepszenia:
   - Czy potrzeba balansować poziomy trudności
   - Propozycje nowych funkcji
   - Motywacja dla graczy

Przedstaw raport w formie executive summary z kluczowymi wskaźnikami."""

# === MAIN ===
if __name__ == "__main__":
    print("🚀 Uruchamianie MCP Server dla MinesweeperAPI...")
    print(f"📡 API endpoint: {API_BASE}")
    print("🔧 Dostępne narzędzia: get_scores, submit_score, get_player_progress")
    print("📚 Dostępne zasoby: api-docs, game-stats")
    print("📝 Dostępne prompty: analyze-player, game-report")
    
    asyncio.run(app.run())
```

## 🔍 Komunikaty protokołu MCP w praktyce

### **Inicjalizacja**
```json
→ {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{"tools":{},"resources":{}}}}
← {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-06-18","capabilities":{"tools":{"listChanged":true},"resources":{"listChanged":true}}}}
```

### **Lista narzędzi**
```json
→ {"jsonrpc":"2.0","id":2,"method":"tools/list"}
← {"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"get_scores","description":"🏆 Pobierz najlepsze wyniki","inputSchema":{"type":"object","properties":{"difficulty":{"type":"string"},"limit":{"type":"integer"}}}}]}}
```

### **Wywołanie narzędzia**
```json
→ {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_scores","arguments":{"difficulty":"easy","limit":5}}}
← {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"🏆 Top 5 wyników (easy):\n\n1. Jan - 125s (easy)\n2. Anna - 130s (easy)"}]}}
```

### **Powiadomienie o zmianie**
```json
← {"jsonrpc":"2.0","method":"notifications/resources/updated","params":{"uri":"mcp://game-stats"}}
```

## 🎯 Podsumowanie zawartości MCP

**Protokół MCP zawiera**:
1. **Transport**: JSON-RPC 2.0 over stdin/stdout lub WebSocket
2. **Lifecycle**: initialize → discovery → calls → shutdown  
3. **Tools**: Funkcje wywołane przez AI (jak API calls)
4. **Resources**: Źródła danych do czytania (pliki, bazy danych)
5. **Prompts**: Gotowe szablony promptów z parametrami
6. **Notifications**: Powiadomienia o zmianach w czasie rzeczywistym
7. **Error handling**: Standardowe kody błędów JSON-RPC
8. **Security**: Kontrola uprawnień i sandboxing

To kompleksny system do bezpiecznego łączenia AI z zewnętrznymi systemami! 🚀