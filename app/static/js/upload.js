const formEl = document.querySelector('#data-form');
document.querySelector('#tour-name').value = Date.now();

formEl.addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = new FormData(formEl);
  formData.append('video0', window.blob);

  let response = await fetch('/upload-data', {
    method: 'POST',
    body: formData,
  });

  window.location.replace(response.url);
});
