import asyncio
import time

import nats
from nats.errors import TimeoutError
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
from nats.js.api import DeliverPolicy, AckPolicy, StreamConfig


async def main():
    nc = await nats.connect("nats-server-1")

    # Create JetStream context.
    js = nc.jetstream()

    # Persist messages on different subjects
    # REF: 
    # https://nats-io.github.io/nats.py/modules.html#jetstream
    # https://github.com/nats-io/nats.py/blob/4c854e6ded4d2cd58b0b9e87945210a2c989fd4d/nats/js/api.py#L267
    # - stream name can not contain '.', '*', '>'
    # - stream subjects can't overlap like `private.user.nino` and `private.user.>` can't exists at the same time.

    await js.add_stream(name="private-user-nino", subjects=["private.user.nino"])
    # await js.add_stream(name="all-private-user", subjects=["private.user.>"])
    await js.add_stream(name="all-private-user", subjects=["private.user.*.*"])
    await js.add_stream(name="all-private-user-something-stream", subjects=["private.user.*.stream"])
    await js.add_stream(name="private.user.*.toy.*", subjects=["private.user.*.toy.*"])
    await js.add_stream(name="private.*.wh.>", subjects=["private.*.wh.>"])

    # Publish from stream
    for i in range(0, 10):
        ack = await js.publish("private.user.nino", f"hello world: {i}".encode())
        print(ack)
        
    # Create a consumer
    sub = await js.pull_subscribe(
        'private.user.nino',
        stream="private-user-nino",
        durable="durable-consumer",
    )

    # Consume messages
    while True:
        try:
            msgs = await sub.fetch(10)
            for msg in msgs:
                print(f"Received message: {msg.data.decode()}")
                await msg.ack()
        except ErrTimeout:
            print("No messages available")

    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())



