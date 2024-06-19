from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata

# Replace with your Kafka broker address
KAFKA_BROKER = "my-cluster-kafka-bootstrap:9092"

consumer = KafkaConsumer(
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='latest',  # Set offset reset strategy (earliest, latest, etc.)
    enable_auto_commit=False,
    metadata_max_age_ms=5000, # Time period refresh metadata.
)

# Subscribe topic names
consumer.subscribe(pattern='my-topic-2')
consumer.topics() # sync metadata

# Not working
consumer.seek_to_end() # set offset to end
consumer.poll(timeout_ms=1000, update_offsets=False) # Get {}

# Working
consumer.position(TopicPartition(topic='my-topic-2', partition=0))
consumer.seek(TopicPartition(topic='my-topic-2', partition=0), offset=11)
consumer.poll(timeout_ms=1000, update_offsets=False) # Get last message

consumer.close()
