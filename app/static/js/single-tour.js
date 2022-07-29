let socket = io();

console.info(socket);

socket.on('loaded', () => {
  window.location.reload();
});
