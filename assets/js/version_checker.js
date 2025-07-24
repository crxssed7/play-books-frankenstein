(function () {
  if (window.pywebview && window.pywebview.api && window.pywebview.api.get_app_version) {
    window.pywebview.api.get_app_version().then(version => {
      const versionElement = document.createElement('span');
      versionElement.classList.add('frankenstein-version')
      versionElement.textContent = `Frankenstein ${version}`;
      document.body.appendChild(versionElement);
    });
  }
})();
