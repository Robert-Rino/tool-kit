# SOCKET.IO Quick start

Demonstrate how redis adaptor works with socket.io


## Run
```
docker compose up
```

`client.js`: Create socket to both `socketio-server-1` and `socketio-server-2`
`server.js`: Initialize socket.io server and send message on `joinRoom` if environment variable `SEND_MESSAGE` is `true`

You should see following output:
```sh
socketio-client    | Connected to server 2
socketio-client    | Connected to server 1
socketio-client    | Message received on server 1: Hello from Server
socketio-client    | Message received on server 2: Hello from Server
```
