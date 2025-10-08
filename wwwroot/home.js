const API_BASE = '/api';

// Pobierz nazwę gracza z localStorage
function getPlayerName() {
  return localStorage.getItem('playerName') || 'Gracz';
}

// Zapisz nazwę gracza
function savePlayerName() {
  const input = document.getElementById('playerName');
  const name = input.value.trim();
  if (name && name.length <= 50) {
    localStorage.setItem('playerName', name);
    showPlayerGreeting(name);
    loadRewards();
  }
}

// Pokaż powitanie
function showPlayerGreeting(name) {
  document.getElementById('playerGreeting').textContent = `Witaj, ${name}!`;
}

// Załaduj wyniki
async function loadScores(difficulty = 'all') {
  const scoresDiv = document.getElementById('scores');
  scoresDiv.innerHTML = 'Ładowanie...';
  
  // Aktualizuj aktywną zakładkę
  document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
  event?.target?.classList.add('active');
  
  try {
    const url = difficulty === 'all' 
      ? `${API_BASE}/scores?limit=10`
      : `${API_BASE}/scores?difficulty=${difficulty}&limit=10`;
    
    const response = await fetch(url);
    const scores = await response.json();
    
    if (scores.length === 0) {
      scoresDiv.innerHTML = '<p style="color: #999; text-align: center;">Brak wyników</p>';
      return;
    }
    
    scoresDiv.innerHTML = scores.map((score, index) => `
      <div class="score-item ${score.difficulty}">
        <span class="score-name">${index + 1}. ${score.playerName}</span>
        <span class="score-time">${formatTime(score.timeSeconds)} • ${getDifficultyName(score.difficulty)}</span>
      </div>
    `).join('');
  } catch (error) {
    console.error('Błąd ładowania wyników:', error);
    scoresDiv.innerHTML = '<p style="color: #f44; text-align: center;">Błąd ładowania wyników</p>';
  }
}

// Załaduj nagrody
async function loadRewards() {
  const playerName = getPlayerName();
  const rewardsDiv = document.getElementById('rewards-track');
  const currentTextureSpan = document.getElementById('current-texture');
  
  try {
    const [rewardsResponse, progressResponse] = await Promise.all([
      fetch(`${API_BASE}/progress/${playerName}/rewards`),
      fetch(`${API_BASE}/progress/${playerName}`)
    ]);
    
    const rewards = await rewardsResponse.json();
    const progress = await progressResponse.json();
    
    currentTextureSpan.textContent = getTextureName(progress.currentTexture);
    
    rewardsDiv.innerHTML = rewards.map(reward => `
      <div class="reward ${reward.texture} ${reward.isUnlocked ? 'unlocked' : ''}">
        <div class="reward-icon">${reward.isUnlocked ? '✓' : '🔒'}</div>
        <div class="reward-name">${reward.name}</div>
      </div>
    `).join('');
  } catch (error) {
    console.error('Błąd ładowania nagród:', error);
    rewardsDiv.innerHTML = '<p style="color: #f44;">Błąd ładowania</p>';
  }
}

// Pomocnicze funkcje
function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function getDifficultyName(difficulty) {
  const names = {
    easy: 'Łatwy',
    medium: 'Średni',
    hard: 'Trudny'
  };
  return names[difficulty] || difficulty;
}

function getTextureName(texture) {
  const names = {
    default: 'Domyślna',
    bronze: 'Brązowa',
    silver: 'Srebrna',
    gold: 'Złota'
  };
  return names[texture] || texture;
}

// Inicjalizacja strony
window.addEventListener('DOMContentLoaded', () => {
  const playerName = getPlayerName();
  document.getElementById('playerName').value = playerName;
  showPlayerGreeting(playerName);
  loadScores('all');
  loadRewards();
});
