// Reference: https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Recording_a_media_element

import { socket } from './config.js';

let video = document.querySelector('#video-preview');

let constraints = {
  audio: false,
  video: {
    facingMode: 'environment',
  },
};

export const videoData = [];

navigator.mediaDevices.getUserMedia(constraints).then(function success(stream) {
  video.srcObject = stream;
  document.querySelector('#video-loader').remove();
  window.startBtn.disabled = false;
});

export const startVideoRecording = () => {
  let recorder = new MediaRecorder(video.srcObject);
  recorder.ondataavailable = (event) => videoData.push(event.data);

  recorder.start(120);

  return recorder;
};

export const stopVideoRecording = () => {
  video.srcObject.getTracks().forEach((track) => track.stop());

  video.style.display = 'none';

  let recordedBlob = new Blob(videoData, { type: 'video/webm' });
  // return URL.createObjectURL(recordedBlob);
  return recordedBlob;
};
