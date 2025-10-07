var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseStaticFiles();

// Strona główna
app.MapGet("/", () => Results.Content(@"
<!DOCTYPE html>
<html>
<head>
    <title>Saper - Strona Główna</title>
    <style>
        :root {
            --bg-color: #f0f0f0;
            --text-color: #333;
            --button-bg: #4CAF50;
            --button-hover: #45a049;
            --card-bg: #fff;
            --border-color: #ddd;
        }
        
        [data-theme='dark'] {
            --bg-color: #1a1a1a;
            --text-color: #fff;
            --button-bg: #2196F3;
            --button-hover: #1976D2;
            --card-bg: #2d2d2d;
            --border-color: #555;
        }
        
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            background: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .container { max-width: 800px; margin: 0 auto; }
        
        .header { margin-bottom: 40px; }
        
        .title { 
            font-size: 3em; 
            margin: 0; 
            color: var(--text-color);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .theme-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--button-bg);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s ease;
        }
        
        .theme-toggle:hover {
            background: var(--button-hover);
        }
        
        .high-score-card {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .high-score-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: var(--text-color);
        }
        
        .score-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid var(--border-color);
        }
        
        .score-item:last-child {
            border-bottom: none;
        }
        
        .difficulty {
            font-weight: bold;
            color: var(--button-bg);
        }
        
        .play-button {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            border: none;
            padding: 20px 40px;
            font-size: 24px;
            border-radius: 50px;
            cursor: pointer;
            margin: 30px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .play-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }
        
        .instructions {
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 20px;
            margin: 30px 0;
            text-align: left;
        }
        
        .instructions h3 {
            text-align: center;
            color: var(--text-color);
        }
        
        .instructions ul {
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <button class='theme-toggle' onclick='toggleTheme()'>🌙</button>
    
    <div class='container'>
        <div class='header'>
            <h1 class='title'>🚩 SAPER 💣</h1>
            <p>Klasyczna gra logiczna - znajdź wszystkie miny!</p>
        </div>
        
        <div class='high-score-card'>
            <h2 class='high-score-title'>🏆 Najlepsze Wyniki</h2>
            <div class='score-item'>
                <span class='difficulty'>Łatwy (9x9)</span>
                <span id='easy-score'>Brak wyniku</span>
            </div>
            <div class='score-item'>
                <span class='difficulty'>Średni (16x16)</span>
                <span id='medium-score'>Brak wyniku</span>
            </div>
            <div class='score-item'>
                <span class='difficulty'>Trudny (16x30)</span>
                <span id='hard-score'>Brak wyniku</span>
            </div>
        </div>
        
        <a href='/game' class='play-button'>🎮 GRAJ TERAZ!</a>
        
        <div class='instructions'>
            <h3>📖 Jak grać?</h3>
            <ul>
                <li><strong>Lewy klik</strong> - odkryj pole</li>
                <li><strong>Prawy klik</strong> - postaw/usuń flagę</li>
                <li><strong>Cel:</strong> Odkryj wszystkie pola bez min</li>
                <li><strong>Liczby</strong> pokazują ile min jest w sąsiedztwie</li>
                <li><strong>Flagi</strong> pomagają oznaczyć podejrzane miny</li>
            </ul>
        </div>
    </div>
    
    <script>
        function toggleTheme() {
            const body = document.body;
            const button = document.querySelector('.theme-toggle');
            
            if (body.getAttribute('data-theme') === 'dark') {
                body.removeAttribute('data-theme');
                button.textContent = '🌙';
                localStorage.setItem('theme', 'light');
            } else {
                body.setAttribute('data-theme', 'dark');
                button.textContent = '☀️';
                localStorage.setItem('theme', 'dark');
            }
        }
        
        // Wczytaj zapisany motyw
        function loadTheme() {
            const savedTheme = localStorage.getItem('theme');
            const button = document.querySelector('.theme-toggle');
            
            if (savedTheme === 'dark') {
                document.body.setAttribute('data-theme', 'dark');
                button.textContent = '☀️';
            }
        }
        
        // Wczytaj najlepsze wyniki
        function loadHighScores() {
            const easyScore = localStorage.getItem('highscore-easy');
            const mediumScore = localStorage.getItem('highscore-medium');
            const hardScore = localStorage.getItem('highscore-hard');
            
            document.getElementById('easy-score').textContent = easyScore || 'Brak wyniku';
            document.getElementById('medium-score').textContent = mediumScore || 'Brak wyniku';
            document.getElementById('hard-score').textContent = hardScore || 'Brak wyniku';
        }
        
        // Inicjalizacja
        loadTheme();
        loadHighScores();
    </script>
</body>
</html>", "text/html"));

// Strona z grą
app.MapGet("/game", () => Results.Content(@"
<!DOCTYPE html>
<html>
<head>
    <title>Saper - Gra</title>
    <style>
        :root {
            --bg-color: #f0f0f0;
            --text-color: #333;
            --button-bg: #4CAF50;
            --button-hover: #45a049;
            --card-bg: #fff;
            --border-color: #ddd;
        }
        
        [data-theme='dark'] {
            --bg-color: #1a1a1a;
            --text-color: #fff;
            --button-bg: #2196F3;
            --button-hover: #1976D2;
            --card-bg: #2d2d2d;
            --border-color: #555;
        }
        
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            background: var(--bg-color);
            color: var(--text-color);
            transition: all 0.3s ease;
        }
        
        .theme-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            background: var(--button-bg);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s ease;
        }
        
        .theme-toggle:hover {
            background: var(--button-hover);
        }
        
        .home-link {
            position: absolute;
            top: 20px;
            left: 20px;
            background: var(--button-bg);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s ease;
            text-decoration: none;
        }
        
        .home-link:hover {
            background: var(--button-hover);
        }
        
        .game-container { margin: 20px auto; display: inline-block; }
        .stats { margin: 10px 0; font-size: 18px; }
        .game-board { border: 2px solid #333; display: inline-block; background: #c0c0c0; }
        .cell { width: 30px; height: 30px; border: 1px solid #999; display: inline-block; 
                text-align: center; line-height: 30px; cursor: pointer; background: #e0e0e0;
                font-weight: bold; font-size: 14px; }
        .cell:hover { background: #d0d0d0; }
        .cell.revealed { background: #f8f8f8; border: 1px inset #999; }
        .cell.mine { background: #ff4444; }
        .cell.flagged { background: #ffff44; }
        .row { height: 30px; white-space: nowrap; }
        .controls { margin: 20px 0; }
        button { padding: 10px 20px; font-size: 16px; cursor: pointer; 
                 background: var(--button-bg); color: white; border: none; border-radius: 5px; }
        button:hover { background: var(--button-hover); }
        select { padding: 10px; font-size: 16px; }
    </style>
</head>
<body>
    <button class='theme-toggle' onclick='toggleTheme()'>🌙</button>
    <a href='/' class='home-link'>🏠 Strona Główna</a>
    
    <h1>🚩 Saper 💣</h1>
    <div class='game-container'>
        <div class='stats'>
            <span>Miny: <span id='mines-count'>10</span></span>
            <span style='margin-left: 20px;'>Czas: <span id='time'>0</span>s</span>
        </div>
        <div class='controls'>
            <button onclick='newGame()'>Nowa Gra</button>
            <select id='difficulty' onchange='changeDifficulty()'>
                <option value='easy'>Łatwy (9x9, 10 min)</option>
                <option value='medium'>Średni (16x16, 40 min)</option>
                <option value='hard'>Trudny (16x30, 99 min)</option>
            </select>
        </div>
        <div id='game-board' class='game-board'></div>
        <div id='message' style='margin-top: 20px; font-size: 18px; font-weight: bold;'></div>
    </div>

    <script>
        let board = [];
        let revealed = [];
        let flagged = [];
        let rows = 9, cols = 9, mines = 10;
        let gameOver = false;
        let startTime = null;
        let timer = null;
        let currentDifficulty = 'easy';

        function toggleTheme() {
            const body = document.body;
            const button = document.querySelector('.theme-toggle');
            
            if (body.getAttribute('data-theme') === 'dark') {
                body.removeAttribute('data-theme');
                button.textContent = '🌙';
                localStorage.setItem('theme', 'light');
            } else {
                body.setAttribute('data-theme', 'dark');
                button.textContent = '☀️';
                localStorage.setItem('theme', 'dark');
            }
        }
        
        function loadTheme() {
            const savedTheme = localStorage.getItem('theme');
            const button = document.querySelector('.theme-toggle');
            
            if (savedTheme === 'dark') {
                document.body.setAttribute('data-theme', 'dark');
                button.textContent = '☀️';
            }
        }

        function initGame() {
            board = Array(rows).fill().map(() => Array(cols).fill(0));
            revealed = Array(rows).fill().map(() => Array(cols).fill(false));
            flagged = Array(rows).fill().map(() => Array(cols).fill(false));
            gameOver = false;
            startTime = null;
            clearInterval(timer);
            document.getElementById('time').textContent = '0';
            document.getElementById('mines-count').textContent = mines;
            document.getElementById('message').textContent = '';
            
            placeMines();
            calculateNumbers();
            renderBoard();
        }

        function placeMines() {
            let placed = 0;
            while (placed < mines) {
                let r = Math.floor(Math.random() * rows);
                let c = Math.floor(Math.random() * cols);
                if (board[r][c] !== -1) {
                    board[r][c] = -1;
                    placed++;
                }
            }
        }

        function calculateNumbers() {
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    if (board[r][c] === -1) continue;
                    let count = 0;
                    for (let dr = -1; dr <= 1; dr++) {
                        for (let dc = -1; dc <= 1; dc++) {
                            let nr = r + dr, nc = c + dc;
                            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && board[nr][nc] === -1) {
                                count++;
                            }
                        }
                    }
                    board[r][c] = count;
                }
            }
        }

        function renderBoard() {
            let boardDiv = document.getElementById('game-board');
            boardDiv.innerHTML = '';
            boardDiv.style.width = (cols * 32) + 'px';
            
            for (let r = 0; r < rows; r++) {
                let rowDiv = document.createElement('div');
                rowDiv.className = 'row';
                for (let c = 0; c < cols; c++) {
                    let cell = document.createElement('div');
                    cell.className = 'cell';
                    cell.onclick = () => revealCell(r, c);
                    cell.oncontextmenu = (e) => { e.preventDefault(); toggleFlag(r, c); };
                    
                    if (flagged[r][c]) {
                        cell.classList.add('flagged');
                        cell.textContent = '🚩';
                    } else if (revealed[r][c]) {
                        cell.classList.add('revealed');
                        if (board[r][c] === -1) {
                            cell.classList.add('mine');
                            cell.textContent = '💣';
                        } else if (board[r][c] > 0) {
                            cell.textContent = board[r][c];
                            cell.style.color = ['','blue','green','red','purple','maroon','turquoise','black','gray'][board[r][c]];
                        }
                    }
                    rowDiv.appendChild(cell);
                }
                boardDiv.appendChild(rowDiv);
            }
        }

        function revealCell(r, c) {
            if (gameOver || revealed[r][c] || flagged[r][c]) return;
            
            if (!startTime) {
                startTime = Date.now();
                timer = setInterval(() => {
                    document.getElementById('time').textContent = Math.floor((Date.now() - startTime) / 1000);
                }, 1000);
            }

            revealed[r][c] = true;

            if (board[r][c] === -1) {
                gameOver = true;
                clearInterval(timer);
                revealAllMines();
                document.getElementById('message').textContent = '💥 Przegrałeś! 💥';
                document.getElementById('message').style.color = 'red';
                return;
            }

            if (board[r][c] === 0) {
                for (let dr = -1; dr <= 1; dr++) {
                    for (let dc = -1; dc <= 1; dc++) {
                        let nr = r + dr, nc = c + dc;
                        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
                            revealCell(nr, nc);
                        }
                    }
                }
            }

            checkWin();
            renderBoard();
        }

        function toggleFlag(r, c) {
            if (gameOver || revealed[r][c]) return;
            flagged[r][c] = !flagged[r][c];
            
            let flagCount = 0;
            for (let i = 0; i < rows; i++) {
                for (let j = 0; j < cols; j++) {
                    if (flagged[i][j]) flagCount++;
                }
            }
            document.getElementById('mines-count').textContent = mines - flagCount;
            renderBoard();
        }

        function revealAllMines() {
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    if (board[r][c] === -1) {
                        revealed[r][c] = true;
                    }
                }
            }
        }

        function checkWin() {
            let revealedCount = 0;
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    if (revealed[r][c]) revealedCount++;
                }
            }
            
            if (revealedCount === rows * cols - mines) {
                gameOver = true;
                clearInterval(timer);
                const finalTime = Math.floor((Date.now() - startTime) / 1000);
                document.getElementById('message').textContent = '🎉 Wygrałeś! 🎉';
                document.getElementById('message').style.color = 'green';
                
                // Zapisz najlepszy wynik
                saveHighScore(currentDifficulty, finalTime);
            }
        }
        
        function saveHighScore(difficulty, time) {
            const key = `highscore-${difficulty}`;
            const currentBest = localStorage.getItem(key);
            
            if (!currentBest || time < parseInt(currentBest)) {
                localStorage.setItem(key, time.toString());
                setTimeout(() => {
                    alert(`🏆 Nowy rekord na poziomie ${difficulty.toUpperCase()}! Czas: ${time}s`);
                }, 500);
            }
        }

        function newGame() {
            initGame();
        }

        function changeDifficulty() {
            let difficulty = document.getElementById('difficulty').value;
            currentDifficulty = difficulty;
            switch(difficulty) {
                case 'easy':
                    rows = 9; cols = 9; mines = 10;
                    break;
                case 'medium':
                    rows = 16; cols = 16; mines = 40;
                    break;
                case 'hard':
                    rows = 16; cols = 30; mines = 99;
                    break;
            }
            initGame();
        }

        // Inicjalizacja
        loadTheme();
        initGame();
    </script>
</body>
</html>", "text/html"));

app.Run();
