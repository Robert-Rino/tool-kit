import asyncio
import time

import nats
from nats.aio.errors import ErrTimeout
from nats.js.api import ConsumerConfig

# Test with publisher
# nats pub --count 0 --sleep 1000ms -s nats-server-1:4222 private.user.wh.events "WH Message {{Count}} @ {{TimeStamp}}"
# nats pub --count 0 --sleep 1500ms -s nats-server-2:4222 private.user.nino.events "Nino Message {{Count}} @ {{TimeStamp}}"

async def main():
    nc = await nats.connect("nats-server-1")

    # Create JetStream context.
    js = nc.jetstream()
        
    # Create a consumer
    sub = await js.pull_subscribe(
        'private.user.nino.*',
        stream="all-private-user",
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



