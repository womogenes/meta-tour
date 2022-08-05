import { $, $$ } from './utils.js';

// Refresh every minute if not processed
if ($('#unprocessed') !== null) {
  window.setTimeout(() => {
    window.location.reload();
  }, 60 * 1000);
}

// View images with Viewer.js
const panoDivs = [...document.getElementById('panoramas-container').children];
let panoIDs = panoDivs.map((el) => el.id);
let started = {};

for (let div of panoDivs) {
  let viewerContainer = div.children[1];
  let imgEl = div.children[0];

  const setup = () => {
    // viewerContainer.children[0].style.backgroundImage = `url('${imgEl.src}')`;

    let imgWidth = imgEl.naturalWidth;
    let imgHeight = imgEl.naturalHeight;

    new window.PhotoSphereViewer.Viewer({
      container: viewerContainer.children[1],
      panorama: imgEl.src,
      loadingImg: 'media/favicon.svg',
      panoData: {
        fullWidth: imgWidth,
        fullHeight: imgWidth / 2,
        croppedWidth: imgWidth,
        croppedHeight: imgHeight,
        croppedX: 0,
        croppedY: (imgWidth / 2 - imgHeight) / 2,
      },
    });
  };

  imgEl.addEventListener('click', () => {
    viewerContainer.style.display = 'flex';
    if (started[div.id]) return;
    started[div.id] = true;

    viewerContainer.children[2].addEventListener('click', () => {
      viewerContainer.style.display = 'none';
    });

    if (imgEl.complete) {
      setup();
    } else {
      imgEl.onload = setup;
    }
  });
}
