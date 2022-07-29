// Reference: https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Recording_a_media_element

import { socket } from './config.js';
import { formatBytes, $ } from './utils.js';

let video = $('#video-preview');

let constraints = {
  audio: false,
  video: {
    facingMode: 'environment',
  },
};

export const videoData = [];

navigator.mediaDevices.getUserMedia(constraints).then(function success(stream) {
  video.srcObject = stream;
  $('#video-loader').remove();
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

  let recordedBlob = new Blob(videoData, { type: 'video/webm' });
  video.style.display = 'none';
  $('#video-size').innerText = formatBytes(recordedBlob.size);

  // return URL.createObjectURL(recordedBlob);
  return recordedBlob;
};
