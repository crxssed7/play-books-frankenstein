(function () {
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
})();
