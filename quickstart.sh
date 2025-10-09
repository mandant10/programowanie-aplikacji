#!/bin/bash
# 🚀 Quick Start - MCP Server dla MinesweeperAPI

echo "🎮 MCP Server Quick Start"
echo "=========================="
echo ""

# 1. Sprawdź zależności
echo "1️⃣ Sprawdzanie zależności..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 nie znaleziony"
    exit 1
fi

if ! command -v dotnet &> /dev/null; then
    echo "❌ .NET SDK nie znaleziony"
    exit 1
fi

echo "✅ Python3: $(python3 --version)"
echo "✅ .NET: $(dotnet --version)"
echo ""

# 2. Instaluj pakiety Python
echo "2️⃣ Instalowanie pakietów Python..."
pip install -q mcp httpx
echo "✅ Pakiety zainstalowane"
echo ""

# 3. Uruchom API
echo "3️⃣ Uruchamianie MinesweeperAPI..."
dotnet run --project MinesweeperAPI.csproj --urls="http://localhost:5022" > /dev/null 2>&1 &
API_PID=$!
echo "✅ API uruchomione (PID: $API_PID)"
sleep 3
echo ""

# 4. Test API
echo "4️⃣ Testowanie API..."
if curl -s http://localhost:5022/api/scores?limit=1 > /dev/null; then
    echo "✅ API odpowiada na localhost:5022"
else
    echo "❌ API nie odpowiada"
    kill $API_PID
    exit 1
fi
echo ""

# 5. Dodaj przykładowe dane
echo "5️⃣ Dodawanie przykładowych danych..."
curl -s -X POST http://localhost:5022/api/scores \
  -H "Content-Type: application/json" \
  -d '{"playerName":"QuickStart","difficulty":"easy","timeSeconds":100}' > /dev/null
echo "✅ Przykładowy wynik dodany"
echo ""

# 6. Test MCP narzędzi
echo "6️⃣ Testowanie MCP narzędzi..."
python3 << 'EOF'
import asyncio
import sys
sys.path.insert(0, '.')
from mcp_server_minesweeper import get_scores, get_game_stats

async def test():
    result = await get_scores(limit=3)
    print("✅ get_scores działa:")
    print(result)

asyncio.run(test())
EOF
echo ""

# 7. Informacje końcowe
echo "=========================="
echo "🎉 GOTOWE!"
echo ""
echo "📋 Co dalej:"
echo ""
echo "▶️  Uruchom MCP Server:"
echo "    python3 mcp_server_minesweeper.py"
echo ""
echo "▶️  Przetestuj wszystko:"
echo "    python3 test_mcp.py"
echo ""
echo "▶️  Zobacz wyniki testów:"
echo "    cat MCP_TEST_RESULTS.md"
echo ""
echo "▶️  Zatrzymaj API:"
echo "    kill $API_PID"
echo ""
echo "🌐 API działa na: http://localhost:5022"
echo "📖 Dokumentacja: MCP_PROTOCOL_EXPLAINED.md"
echo ""
