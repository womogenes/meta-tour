console.info('Page (re)loaded');

import { startVideoRecording, stopVideoRecording } from './video.js';
import { socket } from './config.js';
import './upload.js';
import { $, genRanHex } from './utils.js';

window.startBtn = $('#start-button');
window.stopBtn = $('#stop-button');
const submitBtn = $('#submit-button');

let readings = 0;

let bearing = { alpha: NaN, beta: NaN, gamma: NaN };
let acceleration = { x: NaN, y: NaN, z: NaN };
let rotationRate = { alpha: NaN, beta: NaN, gamma: NaN };
let startTime;
let recordInfoInterval;
export let motionData = [];

const format = (value) => {
  return (Math.round(value * 100) / 100).toFixed(2).padStart(6, ' ');
};

const accelerationHandler = (event) => {
  const { x, y, z } = event.acceleration;
  const { alpha, beta, gamma } = event.rotationRate;
  acceleration = {
    x: x / 9.8,
    y: y / 9.8,
    z: z / 9.8,
  };
  rotationRate = { alpha, beta, gamma };

  $('#acceleration').innerText = `${format(x)}, ${format(y)}, ${format(z)}`;
  $('#rotation-rate').innerText = `${format(beta)}, ${format(gamma)}, ${format(
    alpha
  )}`;
};

const orientationHandler = (event) => {
  const { alpha, beta, gamma } = event;
  bearing = { alpha, beta, gamma };
  $('#orientation').innerText = `${format(beta)}, ${format(gamma)}, ${format(
    alpha
  )}`;
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

      recordInfoInterval = window.setInterval(recordInfo, 10);
    } else {
      $('.notification').style.display = 'block';
    }
  });
};

window.stopCapture = () => {
  stopBtn.disabled = true;
  submitBtn.disabled = false;

  window.clearInterval(recordInfoInterval);
  window.removeEventListener('devicemotion', accelerationHandler);
  window.removeEventListener('deviceorientation', orientationHandler);
  window.blob = stopVideoRecording();

  $('#data-form').style.display = 'block';
};

const recordInfo = () => {
  readings++;
  const time = Date.now() - startTime;

  if (!bearing.alpha) return;

  motionData.push([
    time,
    acceleration.x,
    acceleration.y,
    acceleration.z,
    rotationRate.beta,
    rotationRate.gamma,
    rotationRate.alpha,
    bearing.beta,
    bearing.gamma,
    bearing.alpha,
  ]);
  $('#readings').innerText = readings;
};

// Actually run stuff!
let dataAvailable = DeviceMotionEvent.requestPermission;
$('.notification').style.display = dataAvailable ? 'none' : 'block';
