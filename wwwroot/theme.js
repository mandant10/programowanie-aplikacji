// Theme management functionality
function toggleTheme() {
  const body = document.body;
  const themeIcon = document.getElementById('theme-icon');
  
  if (body.classList.contains('dark-theme')) {
    body.classList.remove('dark-theme');
    themeIcon.textContent = '🌙';
    localStorage.setItem('theme', 'light');
  } else {
    body.classList.add('dark-theme');
    themeIcon.textContent = '☀️';
    localStorage.setItem('theme', 'dark');
  }
}

// Load saved theme on page load
function loadTheme() {
  const savedTheme = localStorage.getItem('theme');
  const body = document.body;
  const themeIcon = document.getElementById('theme-icon');
  
  if (savedTheme === 'dark') {
    body.classList.add('dark-theme');
    if (themeIcon) {
      themeIcon.textContent = '☀️';
    }
  } else {
    if (themeIcon) {
      themeIcon.textContent = '🌙';
    }
  }
}

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', loadTheme);
