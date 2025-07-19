function showHardcoverResults(results, googleId) {
  let container = document.getElementById("matcher");
  if (!container) {
    container = document.createElement("div");
    container.id = "matcher";
    document.body.appendChild(container);
  }

  const header = document.createElement('div');
  header.classList.add('hc-header')
  container.appendChild(header);

  const strong = document.createElement('strong');
  strong.textContent = 'Hardcover Results';
  header.appendChild(strong);

  const close = document.createElement('div');
  close.textContent = '×';
  close.classList.add('close-button');
  close.onclick = () => {
    container.remove();
  };
  header.appendChild(close);

  results.forEach(book => {
    const resultDiv = document.createElement('div');
    resultDiv.classList.add('result')

    const img = document.createElement('img');
    img.src = book.image.url ?? "https://img.hardcover.app/enlarge?url=https://assets.hardcover.app/static/covers/cover6.webp&width=180&height=270&type=webp";
    img.style.width = '50px';
    img.style.height = 'auto';
    img.style.marginRight = '10px';
    resultDiv.appendChild(img);

    const inner = document.createElement('div');
    inner.style.display = 'flex';
    inner.style.flexDirection = 'column';
    inner.style.gap = '5px';
    resultDiv.appendChild(inner);

    const title = document.createElement('span');
    title.textContent = book.title;
    title.style.fontWeight = 'bold';
    title.style.marginRight = '5px';
    inner.appendChild(title);

    const authors = document.createElement('small');
    authors.textContent = book.author;
    authors.style.marginRight = '5px';
    inner.appendChild(authors);

    resultDiv.onclick = () => {
      window.pywebview.api.save_match(googleId, book.id).then(() => {
        container.remove();
      });
    };
    container.appendChild(resultDiv);
  });
}

(function () {
  if (!window.pywebview || !window.pywebview.api) {
    return;
  }

  const extractGoogleIDFromURL = () => {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
  };

  const title = document.title.replace(" - Google Play Books", "")
  const googleID = extractGoogleIDFromURL();
  window.pywebview.api.get_match_from_google_id(googleID).then(match => {
    if (match === null) {
      window.pywebview.api.search_hardcover(title).then(results => {
        if (results.length > 0) {
          showHardcoverResults(results, googleID);
        }
      });
    } else {
      window.pywebview.api.set_current_book(match, googleID)
    }
  });
})();
