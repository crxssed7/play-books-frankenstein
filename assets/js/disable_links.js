(function () {
  function disablePlayStoreLinks(root = document) {
    const links = root.querySelectorAll('a[href*="play.google.com/store"]');
    links.forEach(link => {
      link.href = 'javascript:void(0)';
      link.style.pointerEvents = 'none';
    });

    const bookLinks = root.querySelectorAll('a[href*="/store/books"]');
    bookLinks.forEach(link => {
      link.href = 'javascript:void(0)';
      link.style.pointerEvents = 'none';
    });
  }

  disablePlayStoreLinks();

  const observer = new MutationObserver(mutations => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        if (node.nodeType === 1) { // ELEMENT_NODE
          disablePlayStoreLinks(node);
        }
      }
    }
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
})();
