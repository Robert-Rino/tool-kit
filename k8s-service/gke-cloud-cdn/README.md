# Enable gke cloud-cdn with BackendConfig

## Create tls cert
```sh
kubectl create secret tls nino.baby.tls \
    --cert=tls/certificate.crt \
    --key=tls/private.key
```
