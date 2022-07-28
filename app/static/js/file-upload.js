const fileInput = document.querySelector('input[type=file]');
const fileNameEl = document.querySelector('#filenames');

fileInput.onchange = () => {
  console.info('hello');
  const selectedFiles = [...fileInput.files];

  fileNameEl.innerHTML = '';
  for (const file of selectedFiles) {
    fileNameEl.innerHTML += `<li>${file.name}</li>`;
  }
};
