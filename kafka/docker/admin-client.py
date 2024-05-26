from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException

# - Create topics -
broker = 'broker'
admin_client = AdminClient({'bootstrap.servers': broker})

event_topic = NewTopic('Event', num_partitions=3, replication_factor=1)
event_pull_request_topic = NewTopic('EventPullRequest', num_partitions=3, replication_factor=1, config={
    'cleanup.policy': 'compact' # REF: https://kafka.apache.org/documentation.html#topicconfigs_cleanup.policy
})

fs = admin_client.create_topics([
    event_topic,
    event_pull_request_topic,
])

for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print(f"Topic '{topic}' created successfully.")
    except Exception as e:
        print(f"Failed to create topic '{topic}': {e}")



# # - Delete topics -
# fs = admin_client.delete_topics(['Event'], operation_timeout=30)

# ## Check if the topic deletion was successful
# for topic, f in fs.items():
#     try:
#         f.result()  # The result itself is None
#         print(f"Topic '{topic}' deleted successfully.")
#     except Exception as e:
#         print(f"Failed to delete topic '{topic}': {e}")


# # - Delete consumer group and it's offset stored in broker. - 
# consumer_group_ids = ['mygroup']

# try:
#     fs = admin_client.delete_consumer_groups(consumer_group_ids)

#     # Wait for operation to complete
#     for topic_partition, f in fs.items():
#         try:
#             f.result()  # The result() call will raise an exception if the operation failed
#             print(f'Consumer groups {consumer_group_ids} deleted')
#         except KafkaException as e:
#             print(f"Failed to delete consumer groups {consumer_group_ids}: {e}")
# except Exception as e:
#     print(f"Failed to delete consumer groups {consumer_group_ids}: {e}")

