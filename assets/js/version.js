(function () {
  function createAboutModal(current_version) {
    const dialog = document.createElement('dialog');
    dialog.classList.add('frankenstein-dialog');
    dialog.innerHTML = `
      <div class="dialog-center">
        <h2>Frankenstein v${current_version}</h2>
        <p>Unofficial cross-platform Google Play Books desktop client. Built by crxssed and contributors.</p>
        <div class="flex-container">
          <a href="https://github.com/crxssed7/play-books-frankenstein" target='_blank'>
            <svg class="simple-icon" role="img" height="24" width="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <title>GitHub</title>
              <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
            </svg>
          </a>
          <a href="https://crxssed.dev/" target='_blank'>
            <svg class="simple-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640" height="24" width="24">
              <title>Website</title>
              <path d="M415.9 344L225 344C227.9 408.5 242.2 467.9 262.5 511.4C273.9 535.9 286.2 553.2 297.6 563.8C308.8 574.3 316.5 576 320.5 576C324.5 576 332.2 574.3 343.4 563.8C354.8 553.2 367.1 535.8 378.5 511.4C398.8 467.9 413.1 408.5 416 344zM224.9 296L415.8 296C413 231.5 398.7 172.1 378.4 128.6C367 104.2 354.7 86.8 343.3 76.2C332.1 65.7 324.4 64 320.4 64C316.4 64 308.7 65.7 297.5 76.2C286.1 86.8 273.8 104.2 262.4 128.6C242.1 172.1 227.8 231.5 224.9 296zM176.9 296C180.4 210.4 202.5 130.9 234.8 78.7C142.7 111.3 74.9 195.2 65.5 296L176.9 296zM65.5 344C74.9 444.8 142.7 528.7 234.8 561.3C202.5 509.1 180.4 429.6 176.9 344L65.5 344zM463.9 344C460.4 429.6 438.3 509.1 406 561.3C498.1 528.6 565.9 444.8 575.3 344L463.9 344zM575.3 296C565.9 195.2 498.1 111.3 406 78.7C438.3 130.9 460.4 210.4 463.9 296L575.3 296z"/>
            </svg>
          </a>
        </div>
        <div class="flex-container">
          <button id="close-about-button" autofocus>Close</button>
        </div>
      </div>
    `;
    document.body.appendChild(dialog);

    window.pywebview.api.frankenstein_colour_logo().then(logo => {
      const logoElement = document.createElement('img');
      logoElement.src = logo;
      logoElement.height = 100;
      logoElement.alt = 'Frankenstein Logo';
      dialog.querySelector('.dialog-center').prepend(logoElement);
    })

    const closeButton = dialog.querySelector('#close-about-button');
    closeButton.addEventListener('click', () => {
      dialog.close();
    });

    dialog.showModal();
  }

  function createVersionElement(current_version) {
    const versionElement = document.createElement('span');
    versionElement.classList.add('frankenstein-version')
    versionElement.textContent = `Frankenstein v${current_version}`;
    versionElement.addEventListener('click', () => {
      createAboutModal(current_version)
    })
    document.body.appendChild(versionElement);
  }

  function createUpdateModal(new_version) {
    const dialog = document.createElement('dialog');
    dialog.classList.add('frankenstein-dialog');
    dialog.innerHTML = `
      <h2>v${new_version} Available</h2>
      <p>A new version of Frankenstein is available. Click update to view the release notes (opens in browser).</p>
      <div class="flex-container">
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
