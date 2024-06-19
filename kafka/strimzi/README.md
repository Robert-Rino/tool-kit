# Up kafka cluster with STRIMZI

[Quici start](https://strimzi.io/quickstarts/)

- Bring up different producer

```sh
kubectl -n kafka run kafka-producer-1 -ti --image=quay.io/strimzi/kafka:0.41.0-kafka-3.7.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic-1

kubectl -n kafka run kafka-producer-2 -ti --image=quay.io/strimzi/kafka:0.41.0-kafka-3.7.0 --rm=true --restart=Never -- bin/kafka-console-producer.sh --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic-2
```

# Run you python client
- Run container in cluster

```sh
kubectl -n kafka run kafka-debug -ti --image=python:3.12.3-alpine3.18 --rm=true --restart=Never -- sh
```

- Install depandency

```sh
pip install ipython kafka
```

- solve `ModuleNotFoundError: No module named 'kafka.vendor.six.moves'`

```sh
apk add git
pip install git+https://github.com/dpkp/kafka-python.git
```

- past code in `consumer.py` to ipython.
