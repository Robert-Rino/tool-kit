const io = require('socket.io-client');
const roomName = 'testRoom';

// Connect to the first Socket.IO server
const socket1 = io('http://socketio-server-1:3000', {
    auth: {
        token: 'valid_token' // Replace with the actual token
    }
});

// Connect to the second Socket.IO server
const socket2 = io('http://socketio-server-2:3000', {
    auth: {
        token: 'valid_token' // Replace with the actual token
    }
});

// Join the same room on both servers
socket1.on('connect', () => {
    console.log('Connected to server 1');

    socket1.emit('joinRoom', roomName, (response) => {
        if (response.status === 'ok') {
            console.log('Joined room on server 1');
        } else {
            console.error('Failed to join room on server 1:', response.message);
        }
    });

    socket1.on('message', (message) => {
        console.log('Message received on server 1:', message);
    });
});

socket2.on('connect', () => {
    console.log('Connected to server 2');

    socket2.emit('joinRoom', roomName, (response) => {
        if (response.status === 'ok') {
            console.log('Joined room on server 2');
        } else {
            console.error('Failed to join room on server 2:', response.message);
        }
    });

    socket2.on('message', (message) => {
        console.log('Message received on server 2:', message);
    });
});
