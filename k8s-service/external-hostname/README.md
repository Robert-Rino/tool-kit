# ExternalName

Assume we have a running mongodb on host `mongo.nino.run:27017` which is outside of cluster
we want to let pod in cluster connect to this external db through `mongo-external` service.

mongodb
username: `admin`
password: `password`

# Flows
1. kubectl apply -f service.yaml
2. pod in cluster can access external db through `mongo-external.default.svc.cluster.local`
3. ExternalName doesn't support port remap.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongo-express-express
  labels:
    app: mongo-express
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mongo-express
  template:
    metadata:
      labels:
        app: mongo-express
    spec:
      containers:
      - name: mongo-express
        image: mongo-express
        ports:
        - name: mongo-express
          containerPort: 8081
        env:
        - name: ME_CONFIG_OPTIONS_EDITORTHEME
          value: ambiance
        - name: ME_CONFIG_MONGODB_URL
          value: mongodb://admin:password@mongo-external.default.svc.cluster.local:27017

```


REF: https://kubernetes.io/docs/concepts/services-networking/service/#services-without-selectors
