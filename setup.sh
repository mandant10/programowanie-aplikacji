#!/bin/bash
# Auto-generated setup script for MinesweeperAPI
# Supports: Linux, macOS, Windows (Git Bash/WSL)

set -e

echo "🚀 MinesweeperAPI - Automatyczny Setup"
echo "======================================"
echo ""

# Kolory
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funkcje pomocnicze
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_step() {
    echo -e "${YELLOW}📦 $1${NC}"
}

# 1. Sprawdź .NET
print_step "Sprawdzam .NET SDK..."
if command -v dotnet &> /dev/null; then
    DOTNET_VERSION=$(dotnet --version)
    print_success ".NET SDK: $DOTNET_VERSION"
else
    print_error ".NET SDK nie znalezione!"
    echo "Zainstaluj z: https://dotnet.microsoft.com/download"
    exit 1
fi

# 2. Sprawdź Python
print_step "Sprawdzam Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "$PYTHON_VERSION"
else
    print_error "Python3 nie znaleziony!"
    exit 1
fi

# 3. Setup .NET
echo ""
print_step "Setup .NET dependencies..."

# Find .csproj or .sln file
if [ -f "MinesweeperAPI.csproj" ]; then
    PROJECT_FILE="MinesweeperAPI.csproj"
elif [ -f "programowanie-aplikacji.sln" ]; then
    PROJECT_FILE="programowanie-aplikacji.sln"
else
    PROJECT_FILE=$(find . -maxdepth 1 -name "*.csproj" -o -name "*.sln" | head -n 1)
fi

if [ -z "$PROJECT_FILE" ]; then
    print_warning "No .csproj or .sln found, skipping .NET setup"
else
    dotnet restore "$PROJECT_FILE"
    print_success "Restore complete"
    
    dotnet build "$PROJECT_FILE" --configuration Release
    print_success "Build complete"
fi

# 4. Setup Python
echo ""
print_step "Setup Python environment..."

# Virtual environment
if [ ! -d "venv" ]; then
    print_step "Tworzę virtual environment..."
    python3 -m venv venv
    print_success "venv created"
else
    print_success "venv exists"
fi

# Activate venv
source venv/bin/activate || . venv/Scripts/activate 2>/dev/null

# Upgrade pip
print_step "Upgrading pip..."
pip install --upgrade pip -q
print_success "pip upgraded"

# Install dependencies
print_step "Instaluję dependencies..."
pip install -r requirements.txt -q
print_success "Dependencies installed"

# 5. Setup Git hooks (optional)
echo ""
print_step "Setup Git hooks..."
if [ -d ".git" ]; then
    # Pre-commit hook
    cat > .git/hooks/pre-commit << 'EOFHOOK'
#!/bin/bash
# Auto-format before commit
if command -v dotnet &> /dev/null; then
    dotnet format --verify-no-changes --verbosity quiet || dotnet format
fi
EOFHOOK
    chmod +x .git/hooks/pre-commit
    print_success "Git hooks configured"
else
    print_warning "Not a git repository, skipping hooks"
fi

# 6. Test setup
echo ""
print_step "Testuje setup..."

# Test .NET build
if dotnet build --configuration Release --no-restore > /dev/null 2>&1; then
    print_success ".NET build OK"
else
    print_warning ".NET build failed"
fi

# Test Python imports
if python3 -c "import mcp, httpx" 2>/dev/null; then
    print_success "Python dependencies OK"
else
    print_warning "Python dependencies issue"
fi

# 7. Summary
echo ""
echo "======================================"
echo -e "${GREEN}✅ Setup zakończony!${NC}"
echo "======================================"
echo ""
echo "📋 Następne kroki:"
echo ""
echo "  1. Uruchom backend API:"
echo "     ${YELLOW}dotnet run${NC}"
echo ""
echo "  2. Uruchom MCP server (w nowym terminalu):"
echo "     ${YELLOW}source venv/bin/activate${NC}  # Linux/macOS"
echo "     ${YELLOW}venv\\Scripts\\activate${NC}      # Windows"
echo "     ${YELLOW}python3 mcp_server_minesweeper.py${NC}"
echo ""
echo "  3. Testy:"
echo "     ${YELLOW}./test_mcp_quick.sh${NC}"
echo ""
echo "  4. Agents (opcjonalne):"
echo "     ${YELLOW}python3 agents/orchestrator.py${NC}"
echo ""
echo "📖 Dokumentacja:"
echo "   - API: http://localhost:5022/swagger"
echo "   - MCP Guide: cat MCP_TESTING_GUIDE.md"
echo "   - Agents: cat .github/AGENTS_GUIDE.md"
echo ""
print_success "Gotowe do użycia! 🎉"
