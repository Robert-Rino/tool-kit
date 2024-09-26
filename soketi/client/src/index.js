const PusherJS = require('pusher-js');

let client = new PusherJS('app-key', {
    cluster: {
        hostname: '127.0.0.1',
        port: 6001,
    },
    wsHost: '127.0.0.1',
    wsPort: 6001,
    forceTLS: false,
    encrypted: true,
    disableStats: true,
    enabledTransports: ['ws', 'wss'],
});

client.subscribe('chat-room').bind('message', (message) => {
    alert(`${message.sender} says: ${message.content}`);
});
