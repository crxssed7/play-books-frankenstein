(function () {
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
  document.body.dataset.gpbkey = key;
})();
