console.info(document.querySelector('#unprocessed'));

if (document.querySelector('#unprocessed') !== null) {
  window.setTimeout(() => {
    window.location.reload();
  }, 2000);
}
