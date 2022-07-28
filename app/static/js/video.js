// Reference: https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Recording_a_media_element

import { socket } from './config.js';

let video = document.querySelector('#video-preview');

let constraints = {
  audio: false,
  video: {
    facingMode: 'user',
  },
};

let videoData = [];

navigator.mediaDevices.getUserMedia(constraints).then(function success(stream) {
  video.srcObject = stream;
  document.querySelector('#video-loader').remove();
  startBtn.disabled = false;
});

export const startVideoRecording = () => {
  return;

  let recorder = new MediaRecorder(video.srcObject);
  alert(recorder.getVideoTracks);
  let videoTrack = recorder.getVideoTracks()[0];
  alert('hi');

  recorder.start(120);

  return recorder;
};

export const stopVideoRecording = () => {
  return;

  video.srcObject.getTracks().forEach((track) => track.stop());
};
