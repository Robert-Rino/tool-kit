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
# consumer.subscribe(topic=['my-topic'])
# Subscribe by pattern
consumer.subscribe(pattern=r'my-topic-([\d]+)')

consumer.topics() # sync metadata
consumer.seek_to_end() # set offset to end
offset_info : dict[TopicPartition, OffsetAndMetadata] = consumer._subscription.all_consumed_offsets()
# Get last offset and it's partition.
partition, offset_and_metadata = sorted(
    offset_info.items(),
    key=lambda info: info[1].offset,
    reverse=True
)[0]
# Seek to -1 message.
consumer.seek(
    partition,
    offset_and_metadata.offset - 1 ,
)



for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")

consumer.close()
