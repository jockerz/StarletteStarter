function setLang(language) {
    document.cookie = `language=${language}; samesite=lax; path=/`;
}

document.addEventListener("DOMContentLoaded", function () {
  var themeConfig = {
    theme: "light",
    "theme-base": "gray",
    /*
    "theme-font": "sans-serif",
    "theme-primary": "blue",
    "theme-radius": "1",
    */
  };

  var url = new URL(window.location);
  /*
  var setTheme = document.documentElement.getAttribute('data-bs-theme');
  var argTheme = url.searchParams.get('theme');
  */

  var checkItems = function () {

    for (var key in themeConfig) {
      var value = url.searchParams.get(key) || window.localStorage["tabler-" + key] || themeConfig[key];
      if (!!value) {
        document.documentElement.setAttribute("data-bs-" + key, value);
        window.localStorage.setItem("tabler-" + key, value);
        url.searchParams.delete(key);
      }
    }
    // window.history.pushState({}, "", url);
  };

  checkItems();
})