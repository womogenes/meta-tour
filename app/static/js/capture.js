console.info('Page (re)loaded');

import { startVideoRecording, stopVideoRecording } from './video.js';
import { socket } from './config.js';
import './upload.js';

window.startBtn = document.querySelector('#start-button');
window.stopBtn = document.querySelector('#stop-button');
const submitBtn = document.querySelector('#submit-button');

let readings = 0;

let bearing = { alpha: NaN, beta: NaN, gamma: NaN };
let acceleration = { x: NaN, y: NaN, z: NaN };
let startTime;
let sendInfoInterval;

const format = (value) => {
  return (Math.round(value * 100) / 100).toFixed(2).padStart(6, ' ');
};

const accelerationHandler = (event) => {
  const { x, y, z } = event.accelerationIncludingGravity;
  acceleration = {
    x: x / 9.8,
    y: y / 9.8,
    z: z / 9.8,
  };

  document.querySelector('#acceleration').innerText = `${format(x)}, ${format(
    y
  )}, ${format(z)}`;
};

const orientationHandler = (event) => {
  const { alpha, beta, gamma } = event;
  bearing = { alpha, beta, gamma };
  document.querySelector('#orientation').innerText = `${format(
    alpha
  )}, ${format(beta)}, ${format(gamma)}`;
};

window.startCapture = () => {
  if (!DeviceMotionEvent.requestPermission) {
    return;
  }

  DeviceMotionEvent.requestPermission().then(async (response) => {
    if (response == 'granted') {
      if (!startTime) {
        startTime = Date.now();
      }
      startBtn.disabled = true;
      stopBtn.disabled = false;
      window.addEventListener('devicemotion', accelerationHandler);
      window.addEventListener('deviceorientation', orientationHandler);

      startVideoRecording();

      // sendInfoInterval = window.setInterval(sendInfo, 10);
    } else {
      document.querySelector('.notification').style.display = 'block';
    }
  });
};

window.stopCapture = () => {
  stopBtn.disabled = true;
  startBtn.disabled = false;
  submitBtn.disabled = false;

  //window.clearInterval(sendInfoInterval);
  window.removeEventListener('devicemotion', accelerationHandler);
  window.removeEventListener('deviceorientation', orientationHandler);

  window.blob = stopVideoRecording();
};

const sendInfo = () => {
  readings++;
  const time = Date.now() - startTime;
  socket.emit('motion-reading', [
    time,
    bearing.alpha,
    bearing.beta,
    bearing.gamma,
    acceleration.x,
    acceleration.y,
    acceleration.z,
  ]);
  document.querySelector('#readings').innerText = readings;
};

// Actually run stuff!
let dataAvailable = DeviceMotionEvent.requestPermission;
document.querySelector('.notification').style.display = dataAvailable
  ? 'none'
  : 'block';
startBtn.disabled = !dataAvailable;
