(function () {
  function createVersionElement(current_version) {
    const versionElement = document.createElement('span');
    versionElement.classList.add('frankenstein-version')
    versionElement.textContent = `Frankenstein v${current_version}`;
    document.body.appendChild(versionElement);
  }

  function createUpdateModal(new_version) {
    const dialog = document.createElement('dialog');
    dialog.classList.add('frankenstein-update-dialog');
    dialog.innerHTML = `
      <h2>v${new_version} Available</h2>
      <p>A new version of Frankenstein is available. Click update to view the release notes (opens in browser).</p>
      <div>
        <button id="update-button">Update</button>
        <button id="cancel-update-button">Not now</button>
      </div>
    `;
    document.body.appendChild(dialog);

    const updateButton = dialog.querySelector('#update-button');
    updateButton.addEventListener('click', () => {
      window.pywebview.api.open_release_page();
      dialog.close();
    });

    const cancelButton = dialog.querySelector('#cancel-update-button');
    cancelButton.addEventListener('click', () => {
      dialog.close();
    });

    dialog.showModal();
  }

  if (window.pywebview && window.pywebview.api && window.pywebview.api.check_for_update) {
    window.pywebview.api.check_for_update().then(data => {
      createVersionElement(data.current_version)

      if (!data.new_version_available) { return; }

      createUpdateModal(data.new_version)
    });
  }
})();
