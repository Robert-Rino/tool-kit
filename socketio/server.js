const { createClient } = require("redis");
const { Server } = require("socket.io");
const { createAdapter } = require("@socket.io/redis-adapter");

(async () => {
    const pubClient = createClient({ url: "redis://redis:6379" });
    const subClient = pubClient.duplicate();

    await Promise.all([
        pubClient.connect(),
        subClient.connect()
    ]);

    const io = new Server({
        adapter: createAdapter(pubClient, subClient)
    });

    io.listen(3000);

    io.on('connection', (socket) => {
        console.log('A user connected');

        socket.on('joinRoom', (room) => {
            socket.join(room);
            console.log(`Socket ${socket.id} joined room ${room}`);
    
            if (process.env.SEND_MESSAGE === 'true') {
                setTimeout(() => {
                    io.to(room).emit('message', 'Hello from Server');
                }, 2000);
            }

        });

        // socket.on('leaveRoom', (room) => {
        //     socket.leave(room);
        //     console.log(`Socket ${socket.id} left room ${room}`);
        // });

    });

    console.log('Server listening on port 3000');
})();
