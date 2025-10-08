# 🎮 Gra Saper - ASP.NET Core + JavaScript

Klasyczna gra Saper z trzema poziomami trudności, zapisywaniem rekordów czasowych i systemem nagród odblokowującym nowe tekstury liczb.

## ✨ Funkcjonalności

### Główne wymagania:
- ✅ **Panel gry** - Klasyczna gra Saper w 3 trybach:
  - **Łatwy**: 9x9, 10 min
  - **Średni**: 16x16, 40 min  
  - **Trudny**: 16x30, 99 min
  
- ✅ **Rekordy czasowe** - Wszystkie wyniki zapisywane w bazie (in-memory)
  
- ✅ **Oś nagród** - System odblokowywania tekstur:
  - **Brązowa tekstura** - za ukończenie poziomu łatwego
  - **Srebrna tekstura** - za ukończenie poziomu średniego
  - **Złota tekstura** - za ukończenie poziomu trudnego
  - Aktywna jest tekstura z najwyższego ukończonego poziomu
  
- ✅ **Strona główna** - Wyświetla:
  - Najlepsze wyniki (ogólne i per poziom)
  - Oś nagród z postępem gracza
  - Przyciski do rozpoczęcia gry

## 🏗️ Architektura

### Backend (C# / ASP.NET Core 8.0)
```
/Controllers
  ├── ScoresController.cs      # API dla wyników (GET, POST)
  └── ProgressController.cs    # API dla postępu i nagród
  
/Models
  ├── GameScore.cs             # Model wyniku gry
  ├── PlayerProgress.cs        # Model postępu gracza
  └── Reward.cs                # Model nagrody
  
/Services
  └── GameService.cs           # Logika biznesowa (in-memory storage)
```

### Frontend (HTML + CSS + JavaScript)
```
/wwwroot
  ├── index.html               # Strona główna
  ├── game.html                # Panel gry
  ├── styles.css               # Style globalne
  ├── home.js                  # Logika strony głównej
  └── game.js                  # Logika gry Saper
```

## 🚀 Uruchomienie

### Wymagania
- .NET 8.0 SDK
- Przeglądarka internetowa

### Krok po kroku

1. **Sklonuj/pobierz projekt**
```bash
git clone <repo-url>
cd programowanie-aplikacji
```

2. **Przywróć zależności i zbuduj**
```bash
dotnet restore
dotnet build MinesweeperAPI.csproj
```

3. **Uruchom aplikację**
```bash
dotnet run --project MinesweeperAPI.csproj
```

4. **Otwórz w przeglądarce**
```
http://localhost:5022
```

Aplikacja automatycznie:
- Uruchomi backend API
- Udostępni pliki statyczne (frontend)
- Przekieruje `/` na `index.html`

## 📡 API Endpoints

### Wyniki gry

**POST** `/api/scores` - Zapisz nowy wynik
```json
{
  "playerName": "Gracz",
  "difficulty": "easy",
  "timeSeconds": 125
}
```

**GET** `/api/scores?difficulty=medium&limit=10` - Pobierz top wyniki
- `difficulty` (opcjonalne): "easy", "medium", "hard"
- `limit` (opcjonalne): liczba wyników (1-100, domyślnie 10)

### Postęp gracza

**GET** `/api/progress/{playerName}` - Pobierz postęp gracza
```json
{
  "id": 1,
  "playerName": "Gracz",
  "easyCompleted": true,
  "mediumCompleted": false,
  "hardCompleted": false,
  "currentTexture": "bronze"
}
```

**GET** `/api/progress/{playerName}/rewards` - Pobierz nagrody gracza
```json
[
  {
    "name": "Brązowa tekstura",
    "texture": "bronze",
    "requiredDifficulty": "easy",
    "isUnlocked": true
  }
]
```

## 🎮 Jak grać

1. **Wpisz swoje imię** na stronie głównej
2. **Wybierz poziom trudności** (Łatwy / Średni / Trudny)
3. **Kliknij pole** - odkryj komórkę
4. **Prawy przycisk myszy** - postaw flagę
5. **Cel**: Odkryj wszystkie pola bez min

### Zasady:
- Liczby wskazują ile min jest wokół danego pola
- Flagi pomagają oznaczyć podejrzane pola
- Trafienie na minę = przegrana
- Odkrycie wszystkich bezpiecznych pól = wygrana

## 🏆 System nagród

Nagrody są odblokowywane po pierwszym ukończeniu danego poziomu:

| Poziom | Nagroda | Tekstura |
|--------|---------|----------|
| Łatwy | 🥉 Brązowa | Bronze gradient |
| Średni | 🥈 Srebrna | Silver gradient |
| Trudny | 🥇 Złota | Gold gradient |

Aktywna tekstura to ta z **najwyższego ukończonego poziomu**.

## 🛠️ Technologie

- **Backend**: ASP.NET Core 8.0, C#
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Storage**: In-memory (ConcurrentBag, ConcurrentDictionary)
- **API**: RESTful, JSON
- **Dokumentacja API**: Swagger/OpenAPI (dostępna w `/swagger`)

## 📁 Struktura projektu

```
programowanie-aplikacji/
├── Controllers/              # Kontrolery API
├── Models/                   # Modele danych
├── Services/                 # Logika biznesowa
├── Properties/               # Konfiguracja launchSettings
├── wwwroot/                  # Pliki statyczne (frontend)
│   ├── index.html
│   ├── game.html
│   ├── styles.css
│   ├── home.js
│   └── game.js
├── Program.cs                # Konfiguracja aplikacji
├── appsettings.json          # Ustawienia aplikacji
├── MinesweeperAPI.csproj     # Plik projektu
├── programowanie-aplikacji.sln
└── README.md                 # Ten plik
```

## 🔧 Rozwój

### Dodanie nowej funkcjonalności:

1. **Backend** - dodaj endpoint w `Controllers/`
2. **Model** - utwórz/zaktualizuj model w `Models/`
3. **Serwis** - rozszerz logikę w `Services/GameService.cs`
4. **Frontend** - dodaj wywołanie API w `wwwroot/*.js`

### Debugowanie:

- **Backend logs**: w konsoli terminala
- **Frontend logs**: F12 → Console w przeglądarce
- **API docs**: `/swagger` w przeglądarce

## 📝 TODO (potencjalne rozszerzenia)

- [ ] Persystencja danych (SQL Server, SQLite)
- [ ] Autentykacja użytkowników (ASP.NET Identity)
- [ ] Multiplayer / ranking globalny
- [ ] Więcej tekstur i customizacji
- [ ] Tryb "endless" z dynamiczną trudnością
- [ ] Statystyki (% wygranych, średni czas, itp.)
- [ ] Motywy kolorystyczne (dark mode)
- [ ] PWA (offline support)

## 📄 Licencja

Projekt edukacyjny.

## 👤 Autor

Stworzone jako projekt aplikacji webowej ASP.NET Core.

---

**Miłej zabawy!** 💣🚩
