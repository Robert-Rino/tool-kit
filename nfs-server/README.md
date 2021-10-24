# NFS

Reference: https://medium.com/platformer-blog/nfs-persistent-volumes-with-kubernetes-a-case-study-ce1ed6e2c266

## Steps 

1. Create gce persistent disk
`gcloud compute disks create --size=200GB --zone=asia-east1-a gce-nfs-disk`

2. Create nfs deployment and service
- `kubectl apply -f 001_nfs.yml`
- `kubectl apply -f 002_nfs_server-service.yml`
- `kubectl apply -f 003_pv-pvc.yml`
3. To use nfs.
- `kubectl apply -f 004_pod.yml`