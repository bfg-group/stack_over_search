// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:8081');

// Connection opened
socket.addEventListener('open', function (event) {
    console.log('Start listening...');
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
    document.getElementById("ws_msg").innerHTML = event.data;
});
