import json
from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'broker'})
topic = 'Event'
events = [
    {
        'group': 'stream_online_status_ABC',
        'chanels': ['private-user@ABC', 'pricate-stream@ABC'],
        'event': 'stream.online',
        'payload': {
            'ts': 123,
        },
    },

    #
    {
        'group': 'stream_online_status_ABC',
        'chanels': ['private-user@ABC', 'pricate-stream@ABC'],
        'event': 'stream.offline',
        'payload': {
            'ts': 456,
        },
    },

    #
    {
        'group': 'stream_online_status_QWE',
        'chanels': ['private-user@QWE', 'private-stream@QWE'],
        'event': 'stream.online',
        'payload': {
            'ts': 345,
        },
    },

    #
    {
        'group': 'user_online_status_ABC',
        'chanels': ['private-user@ABC'],
        'event': 'user.online',
        'payload': {
            'balance': 100,
        }
    },
]

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

for event in events:
    p.poll(0)
    key = event['group']
    data = json.dumps({
        'group': event['group'],
        'event': event['event'],
        'payload': event['payload']
    })

    p.produce(topic, key=key, value=data.encode('utf-8'), callback=delivery_report)

p.flush()
