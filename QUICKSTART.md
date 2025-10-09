# 🚀 Quick Start Guide - Kompletny Setup

## ⚡ Szybki start (1 minuta)

```bash
# 1. Clone repo (jeśli jeszcze nie)
git clone https://github.com/mandant10/programowanie-aplikacji.git
cd programowanie-aplikacji

# 2. Uruchom automatyczny setup
./setup.sh

# 3. Uruchom aplikację
dotnet run &

# 4. Test
./test_mcp_quick.sh
```

**Gotowe! 🎉** Aplikacja działa na `http://localhost:5022`

---

## 📋 Co zostało dodane?

### 1️⃣ Automatyzacja setupu środowiska
✅ **`.github/workflows/copilot-setup-steps.yml`**
- Wykrywa automatycznie typy projektów (.NET, Python, MCP)
- Setup dependencies w CI/CD
- Generuje setup scripts
- Multi-stage: detect → setup → verify

✅ **`setup.sh`** - Lokalny setup script
- Sprawdza .NET SDK i Python
- Instaluje dependencies
- Konfiguruje Git hooks
- Testy środowiska

**Użycie:**
```bash
./setup.sh
# lub w GitHub Actions: manual trigger
```

---

### 2️⃣ Dependabot - Auto-updates

✅ **`.github/dependabot.yml`**
- Auto-update dependencies:
  - NuGet (.NET packages)
  - pip (Python packages)
  - GitHub Actions
  - Docker base images
- Grouped updates (minor+patch razem)
- Weekly schedule
- Auto-reviewers

**Efekt:** Pull Requesty z updateami dependencies co tydzień

---

### 3️⃣ Multi-Agent Orchestration

✅ **`.github/agents.mmd`** - Diagram architektury
- Mermaid diagram orkiestracji
- Wizualizacja flow agentów
- Warstwy: User → Agents → MCP → API → Data

✅ **Implementacja agentów:**

**`agents/orchestrator.py`** - Main Orchestrator
```python
orchestrator = OrchestratorAgent()
result = await orchestrator.process_request("Pokaż top 5 wyników")
```

**`agents/game_agent.py`** - Game operations
- get_scores()
- submit_score()
- validate_score()

**`agents/data_agent.py`** - Analytics
- analyze()
- generate_report()
- parse_stats()

**`agents/mcp_agent.py`** - MCP management
- list_tools()
- list_resources()
- health_check()

**Użycie:**
```bash
# Activate venv
source venv/bin/activate

# Uruchom orchestrator
PYTHONPATH=. python3 agents/orchestrator.py

# Lub użyj w kodzie
from agents import OrchestratorAgent
orch = OrchestratorAgent()
await orch.process_request("your request")
```

---

## 🎯 Przykłady użycia

### 1. Automatyczny setup w CI/CD

```yaml
# GitHub Actions workflow
- name: Run automated setup
  uses: ./.github/workflows/copilot-setup-steps.yml
  with:
    setup_type: full
```

### 2. Lokalne środowisko

```bash
# Full setup
./setup.sh

# Tylko Python
source venv/bin/activate
pip install -r requirements.txt

# Tylko .NET
dotnet restore
dotnet build
```

### 3. Użycie agentów

```python
# Simple request
orchestrator = OrchestratorAgent()
result = await orchestrator.process_request("Pokaż top 5 easy")

# Complex multi-agent
scores = await orchestrator.agents['game'].get_scores(limit=10)
analysis = await orchestrator.agents['data'].analyze()
health = await orchestrator.agents['mcp'].health_check()

# Health check all agents
health = await orchestrator.health_check()
```

### 4. Dependabot updates

1. Dependabot tworzy PR z updatem
2. GitHub Actions automatycznie testuje
3. Jeśli testy przechodzą → merge lub review
4. Jeśli nie → investigate

---

## 📊 Architektura Multi-Agent

```
User Request
    ↓
Orchestrator (analiza intencji)
    ↓
┌─────────┬──────────┬──────────┐
│  Game   │   Data   │   MCP    │
│  Agent  │  Agent   │  Agent   │
└────┬────┴────┬─────┴────┬─────┘
     └──────┬──────────────┘
            ↓
      MCP Server (narzędzia i zasoby)
            ↓
      ASP.NET API (:5022)
            ↓
      In-Memory Data
```

**Zobacz diagram:** `.github/agents.mmd` (otwórz w VS Code z Mermaid extension)

---

## 🔧 Konfiguracja

### Agents config: `agents/config/agents.json`

```json
{
  "orchestrator": {
    "max_concurrent_agents": 5,
    "timeout_seconds": 30
  },
  "game_agent": {
    "mcp_server_path": "mcp_server_minesweeper.py",
    "validation_strict": true
  }
}
```

### Dependabot: `.github/dependabot.yml`

```yaml
updates:
  - package-ecosystem: "nuget"
    schedule:
      interval: "weekly"
    groups:
      dotnet-minor-patch:
        update-types: ["minor", "patch"]
```

---

## 🧪 Testowanie

### Test setupu:
```bash
./setup.sh
```

### Test agentów:
```bash
PYTHONPATH=. python3 agents/orchestrator.py
```

### Test MCP:
```bash
./test_mcp_quick.sh
```

### Test CI/CD (lokalnie z act):
```bash
act -j setup-dotnet
```

---

## 📚 Dokumentacja

| Plik | Opis |
|------|------|
| `.github/AGENTS_GUIDE.md` | Kompletny przewodnik agentów |
| `.github/ACTIONS_GUIDE.md` | GitHub Actions dokumentacja |
| `MCP_TESTING_GUIDE.md` | Testowanie MCP servera |
| `MCP_PROTOCOL_EXPLAINED.md` | Protokół MCP |
| `.github/copilot-instructions.md` | Instrukcje dla Copilot |

---

## 🎓 Best Practices

### Setup
✅ Uruchom `./setup.sh` przed każdym dev session  
✅ Używaj `venv` dla Python dependencies  
✅ Commituj tylko po `dotnet format`

### Agents
✅ Jeden agent = jedna odpowiedzialność  
✅ Zawsze używaj async/await  
✅ Loguj wszystkie actions (INFO level)  
✅ Graceful error handling

### CI/CD
✅ Dependabot updates → review przed merge  
✅ Testy muszą przechodzić przed deployment  
✅ Używaj semantic versioning dla tagów

---

## 🐛 Troubleshooting

### Problem: `setup.sh` fails
**Rozwiązanie:**
```bash
# Sprawdź dependencies
dotnet --version  # Powinno być >= 8.0
python3 --version # Powinno być >= 3.12

# Manual setup
dotnet restore MinesweeperAPI.csproj
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: Agents nie działają
**Rozwiązanie:**
```bash
# Sprawdź PYTHONPATH
export PYTHONPATH=/path/to/programowanie-aplikacji

# Sprawdź czy backend działa
curl http://localhost:5022/api/scores

# Sprawdź MCP dependencies
pip list | grep mcp
```

### Problem: Dependabot nie tworzy PRów
**Rozwiązanie:**
1. Settings → Code security → Dependabot
2. Enable Dependabot version updates
3. Check `.github/dependabot.yml` syntax

---

## 🚀 Deployment

### Staging:
```bash
# GitHub Actions - manual trigger
gh workflow run deploy.yml -f environment=staging

# Lokalnie
dotnet publish -c Release
docker build -t minesweeper-staging .
docker run -p 5022:5022 minesweeper-staging
```

### Production:
```bash
# Create release tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions auto-deploy
# Lub manual:
gh workflow run deploy.yml -f environment=production
```

---

## 📊 Monitoring

### Health checks:
```python
# All agents
health = await orchestrator.health_check()

# Specific agent
game_health = await game_agent.health_check()
```

### Metrics (to implement):
- Request latency
- Success rate per agent
- Error rates
- MCP call counts

---

## 🎉 Co dalej?

1. **Rozbuduj agenty:**
   - `monitor_agent.py` - monitoring aplikacji
   - `deploy_agent.py` - automatyczny deployment
   - `security_agent.py` - security scanning

2. **Dodaj UI dla agentów:**
   - Dashboard z live metrics
   - Agent control panel
   - Logs viewer

3. **LLM Integration:**
   - Użyj GPT/Claude do analizy intencji
   - Natural language → agent actions
   - Auto-generate reports

4. **Advanced orchestration:**
   - Agent workflows (DAGs)
   - Conditional execution
   - Retry policies per agent

---

## 📞 Support

- **Issues:** https://github.com/mandant10/programowanie-aplikacji/issues
- **Documentation:** `.github/*.md`
- **Tests:** `test_*.py`

---

**Powodzenia! 🚀**
