# NATS

# Run repository

## Run cluster
```sh
docker compose up
```

## Publish message with nats
```sh
docker compose exec nats-server-1 sh
nats pub --count 0 --sleep 1000ms -s nats-server-1:4222 private.user.wh "WH Message {{Count}} @ {{TimeStamp}}"
```

## Try Jetstream
```sh
docker compose exec nats-python-client sh
python jetstream-basic.py
```

# Test scripts
```sh
// Publish events to subjects
nats pub --count 0 --sleep 1000ms -s nats-server-1:4222 private.user.wh "WH Message {{Count}} @ {{TimeStamp}}"
nats pub --count 0 --sleep 1500ms -s nats-server-2:4222 private.user.nino "Nino Message {{Count}} @ {{TimeStamp}}"

// Subscribe to wildcard subject
nats sub -s nats-server-1:4222 "private.user.>"
nats sub -s nats-server-1:4222 private.user.*


// Create Jetstream 
nats stream add --subjects=private.user.*.events  -s nats-server-1 all-private-user 

// Get Jetstreams
nats stream ls  -s nats-server-1

// Publish events with same message id, test deduplication
nats pub --count 0 --sleep 5000ms -H Nats-Msg-Id:1 -s nats-server-2:4222 private.user.nino.events "Nino Message {{Count}} @ {{TimeStamp}}"
```

# Config
## Cluster
REF: https://docs.nats.io/running-a-nats-service/configuration/clustering/jetstream_clustering#raft


# Examples
https://natsbyexample.com/

