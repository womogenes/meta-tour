import { motionData } from './capture.js';
import { $, genRanHex } from './utils.js';

const formEl = document.querySelector('#data-form');

formEl.addEventListener('submit', async (e) => {
  $('#submit-button').classList.add('is-loading');
  e.preventDefault();

  const formData = new FormData(formEl);
  formData.append('video0', window.blob);
  formData.append('readings', JSON.stringify(motionData));

  let response = await fetch('/upload-data', {
    method: 'POST',
    body: formData,
  });

  window.location.replace(response.url);
});
