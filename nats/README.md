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
```
nats pub --count 0 --sleep 1000ms -s nats-server-1:4222 private.user.wh "WH Message {{Count}} @ {{TimeStamp}}"
nats pub --count 0 --sleep 1500ms -s nats-server-2:4222 private.user.nino "Nino Message {{Count}} @ {{TimeStamp}}"

nats sub -s nats-server-1:4222 "private.user.>"
nats sub -s nats-server-1:4222 private.user.*


nats pub --count 0 --sleep 1000ms -s nats-server-1:4222 private.user.wh.stream. "WH stream abc {{Count}} @ {{TimeStamp}}"
nats pub --count 0 --sleep 1000ms -s nats-server-1:4222 private.user.wh.toy.abc. "WH toy abc {{Count}} @ {{TimeStamp}}"
nats pub --count 0 --sleep 1000ms -s nats-server-1:4222 private.user.wh.toy.qwe. "WH toy qwe {{Count}} @ {{TimeStamp}}"
nats pub --count 0 --sleep 1000ms -s nats-server-1:4222 private.user.nino.stream. "Nino stream abc {{Count}} @ {{TimeStamp}}"
nats pub --count 0 --sleep 1500ms -s nats-server-1:4222 private.user.nino.toy.nnn "Nino toy nnn Message {{Count}} @ {{TimeStamp}}"

nats sub -s nats-server-1:4222 private.user.>

nats sub -s nats-server-1:4222 private.user.*.stream

nats sub -s nats-server-1:4222 private.user.*.toy.*

nats sub -s nats-server-1:4222 private.*.wh.>
```

# Config
## Cluster
REF: https://docs.nats.io/running-a-nats-service/configuration/clustering/jetstream_clustering#raft


# Examples
https://natsbyexample.com/



