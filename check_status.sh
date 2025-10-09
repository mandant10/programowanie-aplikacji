#!/bin/bash
# Quick status check - sprawdź co działa

echo "🔍 Status aplikacji MinesweeperAPI"
echo "=================================="
echo ""

# 1. .NET API
echo "1️⃣  ASP.NET API (port 5022):"
if curl -s http://localhost:5022/api/scores?limit=1 > /dev/null 2>&1; then
    echo "   ✅ Działa - http://localhost:5022"
    echo "   📊 Scores count: $(curl -s http://localhost:5022/api/scores | jq '. | length')"
else
    echo "   ❌ Nie działa"
    echo "   💡 Uruchom: dotnet run"
fi

echo ""

# 2. MCP Server
echo "2️⃣  MCP Server:"
MCP_PID=$(pgrep -f "mcp_server_minesweeper.py" | head -1)
if [ -n "$MCP_PID" ]; then
    echo "   ⚠️  Proces istnieje (PID: $MCP_PID) ale może być zatrzymany"
    echo "   💡 MCP server działa przez stdin/stdout - nie uruchamiaj w tle!"
    echo "   💡 Użyj: python3 test_mcp_interactive.py (zamiast uruchamiać serwer)"
else
    echo "   ℹ️  Nie uruchomiony (to OK - MCP uruchamia się on-demand)"
fi

echo ""

# 3. Processes
echo "3️⃣  Aktywne procesy:"
ps aux | grep -E "(dotnet run|Minesweeper)" | grep -v grep | head -3

echo ""

# 4. Ports
echo "4️⃣  Zajęte porty:"
lsof -i :5022 2>/dev/null | grep LISTEN || echo "   Port 5022 wolny"

echo ""
echo "=================================="
echo "✅ Status check complete"
echo ""
echo "💡 Użycie:"
echo "   - Test MCP: ./test_mcp_quick.sh"
echo "   - Agenty: PYTHONPATH=. python3 agents/orchestrator.py"
echo "   - UI: http://localhost:5022/index.html"
