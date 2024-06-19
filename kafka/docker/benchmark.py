from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource
from confluent_kafka import KafkaException

# - Create topics -
broker = 'broker'
admin_client = AdminClient({'bootstrap.servers': broker})
topic_name = 'Benchmark_3000'

event_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1, config={
        'cleanup.policy': 'compact', # REF: https://kafka.apache.org/documentation.html#topicconfigs_cleanup.policy
        'retention.ms': 6000,
        # 'delete.retention.ms': 6000,
        'min.cleanable.dirty.ratio': 0.1,
        'segment.bytes': 500,
})

fs = admin_client.create_topics([
    event_topic,
])

for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print(f"Topic '{topic}' created successfully.")
    except Exception as e:
        print(f"Failed to create topic '{topic}': {e}")



# Produce 1b event
import json
import time
from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'broker'})

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

for i in range(3000):
    event_time = time.time()

    if i % 300 == 0:
        print(i, event_time)

    key = 'samekey'
    data = json.dumps({
        'group': 'stream_online_status_ABC',
        'event': 'stream.online',
        'user': 'user_A' if i % 2 else 'user_B',
        'payload': {
            'count': i,
            'ts': int(time.time()),
            'user': 'user_A' if i % 2 else 'user_B',
        },
    })

    p.produce(
        topic_name, 
        key=key, 
        value=data.encode('utf-8'), 
        headers={'h1': 'qwe'}, 
        callback=delivery_report,
    )

    print(i, event_time)
    p.flush()

# Consume with python client
import time
from confluent_kafka import Consumer

c = Consumer({
    'bootstrap.servers': 'broker',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
})

c.subscribe([topic_name])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print(f'Consumer error: {msg.error()}')
        continue

    print(f'Received message id:{msg.key()}: {msg.value().decode("utf-8")}')
    time.sleep(1)

c.close()


# Consume with ksq db (REST API)
## Create stream
set 'auto.offset.reset' = 'earliest';
CREATE STREAM event_stream_3000 (
    `group` VARCHAR,
    `event` VARCHAR,
    `payload` VARCHAR,
    `h1` BYTES HEADER('h1'),
    `channels` BYTES HEADER('channels')
) WITH (
    KAFKA_TOPIC='Benchmark_3000',
    VALUE_FORMAT='JSON'
);


## Read from stream and filter by field

## Read from stream and filter by json field
SELECT `group`, `event`, JSON_RECORDS(`payload`) AS payload_decoded, FROM_BYTES(`h1`, 'utf8') AS decoded
FROM event_stream_3000
WHERE CAST(EXTRACTJSONFIELD(`payload`, '$.count') AS INT) > 173500000
EMIT CHANGES;


# Create materialize stream for `private-user@USER_ID`
CREATE STREAM PRIVATE_USER__USER_ID
AS SELECT * FROM event_stream
WHERE 'PRIVATE_USER__USER_ID' IN EXTRACTJSONFIELD(FROM_BYTES(`channels`, 'utf8'), '$.channels')
WITH (
    KAFKA_TOPIC='PRIVATE_USER__USER_ID',
    VALUE_FORMAT='JSON',
    PARTITIONS=1
);
