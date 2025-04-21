# Soketi with NATS adaptor

## Setup tls secret
- Download cert files from certificate provider
```kubectl create secret tls nino.baby.tls --namespace=soketi \
    --cert=certificate.crt \
    --key=private.key
```


## Debug Nats
- `kubectl run -it nats-test --image=natsio/nats-box --restart=Never --rm -n soketi -- /bin/sh`

in shell

`nats request --reply-timeout=1000ms -s nats-0.nats.soketi.svc.cluster.local:4222 '$SYS.REQ.SERVER.PING.CONNZ' ''`
