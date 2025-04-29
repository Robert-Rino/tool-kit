# kafka kraft setup

REF: https://github.com/katyagorshkova/kafka-kraft/tree/main

# Start

## Pre request
```
docker compose up kafka-gen
```

Generate cluster id

```
CLUSTER_ID=$(/bin/kafka-storage random-uui)
```

Format configuration file
```
kafka-storage format --ignore-formatted -t $CLUSTER_ID -c /etc/kafka/kraft/broker.properties
kafka-storage format --ignore-formatted -t $CLUSTER_ID -c /etc/kafka/kraft/controller.properties
```


Check if configure get formatted

## Start cluster
```
docker compose up 
``` 
