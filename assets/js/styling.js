(function () {
  function createAppIcon() {
    if (window.pywebview && window.pywebview.api && window.pywebview.api.assets.get_icon) {
      window.pywebview.api.assets.get_icon().then(icon => {
        let img = document.getElementById('frankenstein');
        if (img === null) {
          img = document.createElement('img');
          img.id = 'frankenstein'
        }
        img.classList.add("frankenstein-logo");
        img.src = icon;
        const element = document.getElementsByClassName("gb_md")[0];
        element.prepend(img);
      });
    }
  }

  function createThemeToggler(theme) {
    const emptyMoon = `<svg height="25" width="25" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="black" d="M144.7 98.7c-21 34.1-33.1 74.3-33.1 117.3c0 98 62.8 181.4 150.4 211.7c-12.4 2.8-25.3 4.3-38.6 4.3C126.6 432 48 353.3 48 256c0-68.9 39.4-128.4 96.8-157.3zm62.1-66C91.1 41.2 0 137.9 0 256C0 379.7 100 480 223.5 480c47.8 0 92-15 128.4-40.6c1.9-1.3 3.7-2.7 5.5-4c4.8-3.6 9.4-7.4 13.9-11.4c2.7-2.4 5.3-4.8 7.9-7.3c5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-3.7 .6-7.4 1.2-11.1 1.6c-5 .5-10.1 .9-15.3 1c-1.2 0-2.5 0-3.7 0l-.3 0c-96.8-.2-175.2-78.9-175.2-176c0-54.8 24.9-103.7 64.1-136c1-.9 2.1-1.7 3.2-2.6c4-3.2 8.2-6.2 12.5-9c3.1-2 6.3-4 9.6-5.8c6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-3.6-.3-7.1-.5-10.7-.6c-2.7-.1-5.5-.1-8.2-.1c-3.3 0-6.5 .1-9.8 .2c-2.3 .1-4.6 .2-6.9 .4z"/></svg>`
    const solidMoon = `<svg height="25" width="25" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path fill="white" d="M223.5 32C100 32 0 132.3 0 256S100 480 223.5 480c60.6 0 115.5-24.2 155.8-63.4c5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6c-96.9 0-175.5-78.8-175.5-176c0-65.8 36-123.1 89.3-153.3c6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"/></svg>`
    const moonElement = document.getElementsByClassName("gb_Te")[0]
    const moon = theme === "DARK" ? solidMoon : emptyMoon
    let element = document.getElementById('moon');
    if (element === null) {
      element = document.createElement('div');
      element.id = 'moon';
    }
    element.classList.add("moon");
    element.innerHTML = moon.trim();
    element.addEventListener("click", () => {
      const stored = localStorage?.getItem(key);
      theme = theme === "DARK" ? "LIGHT" : "DARK"
      const newMoon = theme === "DARK" ? solidMoon : emptyMoon
      if (stored) {
        const settings = JSON.parse(stored);
        settings.theme = theme
        localStorage?.setItem(key, JSON.stringify(settings));
      } else {
        localStorage?.setItem(key, JSON.stringify({ theme }));
      }
      element.innerHTML = newMoon.trim();
      document.body.dataset.theme = theme;
    })
    moonElement.prepend(element)
  }

  function getLocalStorageKey() {
    const scripts = document.querySelectorAll('script');

    for (const script of scripts) {
      const text = script.textContent;
      if (text.includes('books.library.bootstrap') || text.includes('reader.start')) {
        const matches = text.match(/"([a-zA-Z0-9_-]{20,})"/g);
        if (matches && matches.length > 0) {
          const potentialKey = matches.find((match) => match.length === 24) // 24 including quotation mark
          if (potentialKey === undefined) { continue; }
          const cleanKey = potentialKey.replace(/"/g, '');
          const fullKey = `gpb:${cleanKey}`;
          return fullKey;
        }
      }
    }
    return null
  }

  const key = getLocalStorageKey() ?? "gpb:";
  const stored = localStorage?.getItem(key);
  let theme = "DARK";
  if (stored) {
    const settings = JSON.parse(stored);
    if (settings.theme) {
      theme = settings.theme;
    }
  } else {
    localStorage?.setItem(key, JSON.stringify({ theme }));
  }
  document.body.dataset.theme = theme;

  if (window.location.href.includes("play.google.com/books/reader")) { return; }

  createAppIcon()
  createThemeToggler(theme);
})();
