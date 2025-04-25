import ws from 'k6/ws';
import http from 'k6/http';
import { check } from 'k6';

// Environment variables
const CLIENT_COUNT = __ENV.CLIENT_COUNT || '100';
const PUSHER_CHANNELS = (__ENV.PUSHER_CHANNELS || '').split(' ');
const PUSHER_WH_HOST = __ENV.PUSHER_WH_HOST;
const PUSHER_APP_KEY = __ENV.PUSHER_APP_KEY;
const PUSHER_AUTHORIZATION_ENDPOINT = __ENV.PUSHER_AUTHORIZATION_ENDPOINT;


export const options = {
  vus: parseInt(CLIENT_COUNT),
  duration: '300s',
};

function subscribeToChannels(socket, socketId) {
    console.log('subscribing to channels', PUSHER_CHANNELS);
    PUSHER_CHANNELS.forEach(async (channel) => {
      const authResponse = http.post(PUSHER_AUTHORIZATION_ENDPOINT, {
        channel_name: channel,
        socket_id: socketId,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      check(authResponse, {
        'Auth request successful': (r) => r.status === 200,
      });

      const authData = authResponse.json();

      // Step 3: Subscribe to channel with auth token
      socket.send(JSON.stringify({
        event: 'pusher:subscribe',
        data: {
            channel: channel,
            auth: authData.auth,
            channel_data: authData.channel_data,
        },
      }));
  });
}

function handleMessageEvent(message, socket) {
  message = JSON.parse(message);
  
  switch (message.event) {
    case 'pusher:connection_established':
      subscribeToChannels(socket, JSON.parse(message.data).socket_id);
      break;
  }
}


export default function () {
  const url = `${PUSHER_WH_HOST}/app/${PUSHER_APP_KEY}`;
//   const url = `ws://echo.websocket.org`
  const params = { 
    tags: { my_tag: 'hello' },
  };

  const response = ws.connect(url, params, function (socket) {
    console.log('connection initialized');
    
    socket.on('open', function open() {
      console.log('connected');

      socket.setInterval(function timeout() {
        socket.send(JSON.stringify({
            event: 'pusher:pong',
            data: {},
        }));
        console.log('Pinging every 30sec (setInterval test)');
      }, 30000);
    });


    socket.on('pusher:pong', function () {
        console.log('pusher:pong received');
      });

    socket.on('message', function (message) {
      console.log(`Received message: ${message}`);
      handleMessageEvent(message, socket);
    });

    socket.on('close', function () {
      console.log('disconnected');
    });

    socket.on('error', function (e) {
      if (e.error() != 'websocket: close sent') {
        console.log('An unexpected error occured: ', e.error());
      }
    });

    // Pusher events

    socket.on('activity', function () {
      console.log('activity');
    });

  });

  check(response, { 
    'status is 101': (r) => r && r.status === 101,

  });

}
