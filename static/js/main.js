// Theme switch
!function(e){"function"==typeof define&&define.amd?define(e):e()}((function(){"use strict";var e,t="tablerTheme",n=new Proxy(new URLSearchParams(window.location.search),{get:function(e,t){return e.get(t)}});if(n.theme)localStorage.setItem(t,n.theme),e=n.theme;else{var o=localStorage.getItem(t);e=o||"light"}document.body.classList.remove("theme-dark","theme-light"),document.body.classList.add("theme-".concat(e))}));
function setLang(language) {
    document.cookie = `language=${language}; samesite=lax; path=/`;
}