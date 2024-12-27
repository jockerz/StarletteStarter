// Language
function setLang(language) {
  document.cookie = `language=${language}; samesite=lax; path=/`;
  for (const lang of ['en', 'id']) {
    elem = document.getElementById(`lang-${lang}`)
    lang === language ? elem.classList.add('active') : elem.classList.remove('active')
  }
}

// Theme
function setTheme(theme) {
  el_nav = document.getElementById('top-navbar')
  if (el_nav !== null) {
    el_nav.classList.remove('navbar-light')
    el_nav.classList.remove('navbar-dark')
  }

  theme_switch = document.getElementById('theme-switch')

  if (theme_switch !== null) {
    theme_switch.innerHTML = '';
  }

  if (theme === 'dark') {
    document.body.classList.add('dark-mode')
    if (el_nav !== null) {
      el_nav.classList.add('navbar-dark')
    }
    if (theme_switch !== null) {
      theme_switch.innerHTML = '<i class="fas fa-moon"></i>';
    }
  } else {
    document.body.classList.remove('dark-mode')
    if (el_nav !== null) {
      el_nav.classList.add('navbar-light')
    }
    if (theme_switch !== null) {
      theme_switch.innerHTML = '<i class="fas fa-sun"></i>';
    }
  }

  localStorage.setItem('theme', theme)
}

function initTheme() {
  const theme = localStorage.getItem('theme');
  if (theme !== undefined && theme !== null) {
    setTheme(theme)
  } else {
     const checkIsDarkSchemePreferred = () => window?.matchMedia?.('(prefers-color-scheme:dark)')?.matches ?? false;
     setTheme(checkIsDarkSchemePreferred ? 'dark' : 'light')
  }
}

function themeSwitch() {
  theme = localStorage.getItem('theme') || 'light';
  setTheme(theme === 'light' ? 'dark': 'light')
}