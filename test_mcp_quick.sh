#!/bin/bash
# Quick test MCP servera - sprawdza czy działa

echo "🚀 Test MCP Server dla MinesweeperAPI"
echo ""

# Sprawdź czy backend działa
echo "1️⃣  Sprawdzam backend .NET API..."
if curl -s http://localhost:5022/api/scores?limit=1 > /dev/null 2>&1; then
    echo "   ✅ Backend działa (http://localhost:5022)"
else
    echo "   ⚠️  Backend nie działa. Uruchom: dotnet run"
    echo ""
fi

# Sprawdź zależności Python
echo ""
echo "2️⃣  Sprawdzam zależności Python..."
if python3 -c "import mcp, httpx" 2>/dev/null; then
    echo "   ✅ mcp i httpx zainstalowane"
else
    echo "   ⚠️  Brak zależności. Uruchom: pip install mcp httpx"
    exit 1
fi

# Test MCP servera
echo ""
echo "3️⃣  Testuję MCP server..."
echo ""

python3 test_mcp_interactive.py

echo ""
echo "✅ Test zakończony!"
echo ""
echo "📖 Więcej info: cat MCP_TESTING_GUIDE.md"
