# HPA

Doc: 
- https://cloud.google.com/kubernetes-engine/docs/how-to/horizontal-pod-autoscaling
- https://kubernetes.io/zh/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/


## CPU
### Generate Load
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"



## Memory
