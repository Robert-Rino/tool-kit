from confluent_kafka import Consumer

c = Consumer({
    'bootstrap.servers': 'broker',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest',
    # 'enable.auto.commit': False,
})
topics = [
    'Event',
    # 'EventPullRequest',
]

c.subscribe(topics)

while True:
    msg = c.poll(5.0)

    if msg is None:
        continue
    if msg.error():
        print(f'Consumer error: {msg.error()}')
        continue

    print(f'Received message id:{msg.key()}: {msg.value().decode("utf-8")}')

c.close()
