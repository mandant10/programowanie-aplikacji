const API_BASE = '/api';

// Konfiguracja poziomów trudności
const DIFFICULTY_CONFIG = {
  easy: { rows: 9, cols: 9, mines: 10, name: 'Łatwy' },
  medium: { rows: 16, cols: 16, mines: 40, name: 'Średni' },
  hard: { rows: 16, cols: 30, mines: 99, name: 'Trudny' }
};

// Stan gry
let gameState = {
  difficulty: 'easy',
  config: null,
  board: [],
  revealed: [],
  flags: [],
  gameOver: false,
  gameWon: false,
  startTime: null,
  timerInterval: null,
  elapsedSeconds: 0
};

// Inicjalizacja gry
function initGame() {
  // Pobierz poziom trudności z URL
  const urlParams = new URLSearchParams(window.location.search);
  gameState.difficulty = urlParams.get('mode') || 'easy';
  gameState.config = DIFFICULTY_CONFIG[gameState.difficulty];
  
  // Aktualizuj UI
  document.getElementById('difficulty-name').textContent = gameState.config.name;
  document.getElementById('mines-count').textContent = gameState.config.mines;
  
  // Reset stanu
  gameState.gameOver = false;
  gameState.gameWon = false;
  gameState.startTime = null;
  gameState.elapsedSeconds = 0;
  gameState.flags = [];
  
  // Zatrzymaj timer
  if (gameState.timerInterval) {
    clearInterval(gameState.timerInterval);
    gameState.timerInterval = null;
  }
  
  // Wygeneruj planszę
  generateBoard();
  renderBoard();
  updateFlagsCount();
  updateTimer();
  hideMessage();
}

// Generuj planszę z minami
function generateBoard() {
  const { rows, cols, mines } = gameState.config;
  
  // Inicjalizuj pustą planszę
  gameState.board = Array(rows).fill(0).map(() => Array(cols).fill(0));
  gameState.revealed = Array(rows).fill(0).map(() => Array(cols).fill(false));
  
  // Losowo rozmieść miny
  let minesPlaced = 0;
  while (minesPlaced < mines) {
    const row = Math.floor(Math.random() * rows);
    const col = Math.floor(Math.random() * cols);
    
    if (gameState.board[row][col] !== -1) {
      gameState.board[row][col] = -1; // -1 oznacza minę
      minesPlaced++;
      
      // Zaktualizuj liczby w sąsiednich polach
      updateAdjacentCells(row, col);
    }
  }
}

// Zaktualizuj liczby w sąsiednich polach
function updateAdjacentCells(row, col) {
  const { rows, cols } = gameState.config;
  
  for (let dr = -1; dr <= 1; dr++) {
    for (let dc = -1; dc <= 1; dc++) {
      if (dr === 0 && dc === 0) continue;
      
      const newRow = row + dr;
      const newCol = col + dc;
      
      if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols) {
        if (gameState.board[newRow][newCol] !== -1) {
          gameState.board[newRow][newCol]++;
        }
      }
    }
  }
}

// Renderuj planszę
function renderBoard() {
  const { rows, cols } = gameState.config;
  const boardDiv = document.getElementById('game-board');
  
  boardDiv.style.gridTemplateColumns = `repeat(${cols}, 30px)`;
  boardDiv.innerHTML = '';
  
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.dataset.row = row;
      cell.dataset.col = col;
      
      // Event listenery
      cell.addEventListener('click', () => revealCell(row, col));
      cell.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        toggleFlag(row, col);
      });
      
      updateCellDisplay(cell, row, col);
      boardDiv.appendChild(cell);
    }
  }
}

// Aktualizuj wyświetlanie komórki
function updateCellDisplay(cell, row, col) {
  const isRevealed = gameState.revealed[row][col];
  const hasFlag = gameState.flags.some(f => f.row === row && f.col === col);
  const value = gameState.board[row][col];
  
  cell.className = 'cell';
  
  if (hasFlag) {
    cell.classList.add('flag');
    cell.textContent = '🚩';
  } else if (isRevealed) {
    cell.classList.add('revealed');
    
    if (value === -1) {
      cell.classList.add('mine');
      cell.textContent = '💣';
    } else if (value > 0) {
      cell.textContent = value;
      cell.classList.add(`number-${value}`);
    }
  } else {
    cell.textContent = '';
  }
}

// Odkryj komórkę
function revealCell(row, col) {
  if (gameState.gameOver || gameState.gameWon) return;
  if (gameState.revealed[row][col]) return;
  if (gameState.flags.some(f => f.row === row && f.col === col)) return;
  
  // Rozpocznij timer przy pierwszym kliknięciu
  if (!gameState.startTime) {
    startTimer();
  }
  
  gameState.revealed[row][col] = true;
  const value = gameState.board[row][col];
  
  // Trafiłeś na minę
  if (value === -1) {
    gameOver(false);
    return;
  }
  
  // Jeśli pole jest puste (0), odkryj sąsiednie
  if (value === 0) {
    revealAdjacentCells(row, col);
  }
  
  // Odśwież planszę
  renderBoard();
  
  // Sprawdź warunek wygranej
  checkWinCondition();
}

// Odkryj sąsiednie pola (dla pustych pól)
function revealAdjacentCells(row, col) {
  const { rows, cols } = gameState.config;
  
  for (let dr = -1; dr <= 1; dr++) {
    for (let dc = -1; dc <= 1; dc++) {
      if (dr === 0 && dc === 0) continue;
      
      const newRow = row + dr;
      const newCol = col + dc;
      
      if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols) {
        if (!gameState.revealed[newRow][newCol] && 
            !gameState.flags.some(f => f.row === newRow && f.col === newCol)) {
          revealCell(newRow, newCol);
        }
      }
    }
  }
}

// Przełącz flagę
function toggleFlag(row, col) {
  if (gameState.gameOver || gameState.gameWon) return;
  if (gameState.revealed[row][col]) return;
  
  const flagIndex = gameState.flags.findIndex(f => f.row === row && f.col === col);
  
  if (flagIndex >= 0) {
    gameState.flags.splice(flagIndex, 1);
  } else {
    if (gameState.flags.length < gameState.config.mines) {
      gameState.flags.push({ row, col });
    }
  }
  
  renderBoard();
  updateFlagsCount();
}

// Sprawdź warunek wygranej
function checkWinCondition() {
  const { rows, cols, mines } = gameState.config;
  let revealedCount = 0;
  
  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      if (gameState.revealed[row][col]) {
        revealedCount++;
      }
    }
  }
  
  // Wygrana: odkryto wszystkie pola oprócz min
  if (revealedCount === (rows * cols - mines)) {
    gameOver(true);
  }
}

// Zakończ grę
async function gameOver(won) {
  gameState.gameOver = !won;
  gameState.gameWon = won;
  
  // Zatrzymaj timer
  if (gameState.timerInterval) {
    clearInterval(gameState.timerInterval);
  }
  
  // Odkryj wszystkie miny
  if (!won) {
    const { rows, cols } = gameState.config;
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        if (gameState.board[row][col] === -1) {
          gameState.revealed[row][col] = true;
        }
      }
    }
    renderBoard();
    showMessage('💥 Przegrałeś! Trafiłeś na minę.', 'error');
  } else {
    showMessage('🎉 Gratulacje! Wygrałeś!', 'success');
    
    // Zapisz wynik
    await saveScore();
  }
}

// Zapisz wynik do API
async function saveScore() {
  const playerName = localStorage.getItem('playerName') || 'Gracz';
  
  try {
    const response = await fetch(`${API_BASE}/scores`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        playerName: playerName,
        difficulty: gameState.difficulty,
        timeSeconds: gameState.elapsedSeconds
      })
    });
    
    if (response.ok) {
      const score = await response.json();
      showMessage(`🎉 Gratulacje! Czas: ${formatTime(gameState.elapsedSeconds)} • Wynik zapisany!`, 'success');
    }
  } catch (error) {
    console.error('Błąd zapisu wyniku:', error);
  }
}

// Timer
function startTimer() {
  gameState.startTime = Date.now();
  gameState.timerInterval = setInterval(() => {
    gameState.elapsedSeconds = Math.floor((Date.now() - gameState.startTime) / 1000);
    updateTimer();
  }, 1000);
}

function updateTimer() {
  document.getElementById('timer').textContent = formatTime(gameState.elapsedSeconds);
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Aktualizuj licznik flag
function updateFlagsCount() {
  document.getElementById('flags-count').textContent = gameState.flags.length;
}

// Pokaż wiadomość
function showMessage(text, type) {
  const messageDiv = document.getElementById('game-message');
  messageDiv.textContent = text;
  messageDiv.className = `game-message ${type}`;
  messageDiv.style.display = 'block';
}

function hideMessage() {
  const messageDiv = document.getElementById('game-message');
  messageDiv.style.display = 'none';
}

// Inicjalizuj grę przy załadowaniu strony
window.addEventListener('DOMContentLoaded', initGame);
