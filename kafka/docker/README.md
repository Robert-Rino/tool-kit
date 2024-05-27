# Kafka and ksqlDB local
Ref: 
- https://ksqldb.io/quickstart.html
- [confluent-kafka github](https://github.com/confluentinc/confluent-kafka-python?tab=readme-ov-file)
- [confluent-kafka document](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html)
- [Apache Kafka config](https://kafka.apache.org/documentation.html#consumerconfigs)


## Bring up services
```sh
docker compose up 
```


## Create topics we need
```sh
docker compose exec python-client ipython
```

### Create topics we needs
Run code in `admin-client.py`
- Event (Srouce of truth)
- EventPullRequest (For ksqlDB pull request)
  - compact topic


## Setup ksql db
```sh
docker compose exec -it ksqldb-cli ksql http://ksqldb-server:8088
```

### Pull query
```sql
CREATE STREAM event_stream (
    `group` VARCHAR,
    `channels` ARRAY<VARCHAR>,
    `event` VARCHAR,
    `payload` VARCHAR
) WITH (
    KAFKA_TOPIC='Event',
    VALUE_FORMAT='JSON'
);
```

Create a table from the stream for pull queries
```sql
CREATE TABLE event_pull_query 
-- WITH (
--   -- Create this compact topic with admin client.
--   KAFKA_TOPIC='EventPullRequest',
--   VALUE_FORMAT='JSON',
--   PARTITIONS=3,
--   REPLICAS=1
-- )
AS SELECT
    `group`,
    LATEST_BY_OFFSET(`event`) AS latest_event,
    LATEST_BY_OFFSET(`payload`) AS latest_payload
FROM
    event_stream
GROUP BY
    `group`
EMIT CHANGES;
```

ksqlDB query:
```sql
SELECT * FROM event_pull_query WHERE `group` IN ('stream_online_status_ABC', 'user_online_status_ABC');
```

http query
```sh
curl -X POST http://localhost:8088/query \
     -H "Content-Type: application/vnd.ksql.v1+json; charset=utf-8" \
     -d '{
           "ksql": "SELECT * FROM event_pull_query WHERE `group` IN ('\''stream_online_status_ABC'\'', '\''user_online_status_ABC'\'');",
           "streamsProperties": {}
   
         }'
```

### Push query
Create a table for push queries
```sql
CREATE TABLE event_push_query AS
SELECT 
    `group`, 
    LATEST_BY_OFFSET(`event`) AS latest_event, 
    LATEST_BY_OFFSET(`payload`) AS latest_payload
FROM 
    event_stream
GROUP BY 
    `group`
EMIT CHANGES;
```

ksqldb query

```sql
SELECT * FROM event_push_query WHERE `group` IN ('stream_online_status_ABC', 'user_online_status_ABC') EMIT CHANGES;
```

http query
```sh
curl -X POST http://localhost:8088/query-stream \
     -H "Content-Type: application/vnd.ksql.v1+json; charset=utf-8" \
     -d '{
           "sql": "SELECT * FROM event_push_query WHERE `group` IN ('\''stream_online_status_ABC'\'', '\''user_online_status_ABC'\'') EMIT CHANGES;",
           "streamsProperties": {}
         }'
```


## Produce some event
run code in `producer-client.py`
- Create messages to `Event` topic

## Try query to ksqlDB with pull or push
