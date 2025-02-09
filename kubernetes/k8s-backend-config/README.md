https://cloud.google.com/kubernetes-engine/docs/how-to/ingress-features#unique_backendconfig_per_service_port

```shell
kubectl apply -f pod-demo.yaml
kubectl apply -f service.yaml
kubectl apply -f backendconfig.yaml
kubectl apply -f ingress.yaml
```
