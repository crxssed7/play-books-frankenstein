(function () {
  const originalOpen = XMLHttpRequest.prototype.open;
  const originalSend = XMLHttpRequest.prototype.send;
  const originalSetRequestHeader = XMLHttpRequest.prototype.setRequestHeader;

  XMLHttpRequest.prototype.open = function (method, url, async, user, password) {
    this._method = method;
    this._url = url;
    return originalOpen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.setRequestHeader = function (header, value) {
    this._headers = this._headers || {};
    this._headers[header] = value;
    return originalSetRequestHeader.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function (body) {
    if (this._url.includes('SyncDocumentPosition')) {
      const xhrData = {
        url: this._url,
        method: this._method,
        headers: this._headers || {},
        body: body
      };
      if (window.pywebview && window.pywebview.api && window.pywebview.api.session.update_progress_percentage) {
        window.pywebview.api.session.update_progress_percentage(xhrData);
      }
    }

    return originalSend.apply(this, arguments);
  };
})();
