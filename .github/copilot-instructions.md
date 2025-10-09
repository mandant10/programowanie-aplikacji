# Przykładowe instrukcje dla Copilot / asystenta kodu

Poniżej znajdziesz przykładowe, krótkie instrukcje, które możesz wkleić do narzędzia Copilot, asystenta AI lub do opisu PR/issue, by wymusić spójne zachowanie podczas generowania kodu.

Zasady ogólne
- Nie przesadzaj z zabezpieczeniami: implementuj rozsądne, minimalne kontrole poprawności i walidacji — nie dopisuj warstw zabezpieczeń, których nie wymaga zadanie.
- Unikaj nadmiernego skomplikowania i „over-engineering”. Preferuj prostotę i czytelność.
- Jeśli nie jesteś pewien wymagań lub konwencji, zapytaj najpierw — nie zgaduj.

Konwencje nazewnicze
- Zmienna i funkcje: camelCase (np. `playerScore`, `calculateReward`).
- Klasy i struktury: PascalCase (np. `GameService`, `PlayerProgress`).
- Stałe: UPPER_SNAKE_CASE lub PascalCase jeśli zgodne z konwencją projektu.
- Pliki: używaj konwencji projektu; w C# preferujemy PascalCase dla plików odpowiadających klasom.

Styl kodu
- Preferuj krótkie, dobrze nazwane funkcje (zazwyczaj < ~50 linii). Jeśli metoda rośnie — wyodrębnij część logiki.
- Jasne i krótkie komentarze tam, gdzie logika nie jest oczywista. Nie komentuj oczywistych rzeczy.
- Zwracaj uwagę na istniejące konwencje w repozytorium i stosuj je (np. użycie async/await, wzorce DI).

Testy i walidacja
- Dodaj testy jednostkowe dla kluczowej logiki — przynajmniej happy path i 1-2 edge case'y.
- Nie pisz testów integracyjnych, jeśli użytkownik nie poprosił o uruchomienie bazy lub środowiska zewnętrznego.

Commity i PR
- Twórz małe, logiczne commity z opisem w języku polskim lub angielskim (krótkie zdanie + 1 linia wyjaśnienia).
- W PR opisz krótko co zmieniono i dlaczego; nie wrzucaj niepotrzebnych refactorów w tym samym PR.

Bezpieczeństwo i dane wrażliwe
- Nie umieszczaj sekretów, kluczy API ani haseł w kodzie. Jeśli musisz zasugerować konfigurację, użyj placeholderów i opisz, gdzie dodać sekrety (np. `appsettings.Development.json` lub zmienne środowiskowe).

Restrykcyjne zmiany
- Nie zmieniaj globalnych konfiguracji lub zależności bez wyraźnej zgody (np. aktualizacja major dependency, zmiana target framework).

Inne wskazówki
- Jeśli dodajesz nowy endpoint lub API, dołącz przykład request/response (json) i minimalną walidację inputu.
- Jeśli proponujesz zmiany w architekturze lub wzorcach — podaj krótki przegląd alternatyw i uzasadnienie.

---
Możesz tę listę skrócić, rozbudować lub przetłumaczyć w zależności od potrzeb projektu. Jeśli chcesz, mogę dopracować wersję angielską lub bardziej szczegółową konfigurację (np. reguły ESLint/EditorConfig/formatowania).
