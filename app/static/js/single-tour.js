// Refresh every minute if not processed
if (document.querySelector('#unprocessed') !== null) {
  window.setTimeout(() => {
    window.location.reload();
  }, 60 * 1000);
}

// View images with Viewer.js
const viewer = new window.Viewer(document.querySelector('.panorama'), {
  inline: false,
  title: 0,
  ready() {},
});
