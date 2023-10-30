# Make docker image
```shell
docker pull nginx
export PREFIX=nginx
export TAG=$PREFIX-$(date +%s)
export IMAGE="asia-east1-docker.pkg.dev/$PROJECT_ID/pop-stats/pop-stats:$TAG"
docker tag nginx $IMAGE
gcloud auth configure-docker us-central1-docker.pkg.dev
docker push $IMAGE
```

# Demo app
## Build demo app
`DOCKER_DEFAULT_PLATFORM=linux/amd64 docker build -t a901002666/debug-nginx .`

## Use default debug message
`docker run --name nginx-debug --rm -p 8080:80 --env DEBUG_MESSAGE='Nino Message' a901002666/debug-nginx`

## Call debug route
`http :8080/debug`


# Cloud deploy
## Apply cloud deploy config
```shell
gcloud deploy apply --file=clouddeploy-demo.yaml --region=us-central1 --project=swag-nino-chang
```

## Create release
```shell
gcloud deploy releases create test-release-001 \
  --project=swag-nino-chang \
  --region=us-central1 \
  --delivery-pipeline=my-gke-demo-app-1 \
  --images my-app-image=us-central1-docker.pkg.dev/swag-nino-chang/nginx/nginx:release-1
```

## Create release 
```shell
gcloud deploy releases create test-release-010 \
  --project=swag-nino-chang \
  --region=us-central1 \
  --delivery-pipeline=my-canary-demo-app-1 \
  --images=my-app-image=a901002666/debug-nginx
```

## Approve rollout
```shell
gcloud deploy rollouts approve test-release-010-to-cluster-production-0001 \
  --project=swag-nino-chang \
  --region=us-central1 \
  --delivery-pipeline=my-canary-demo-app-1 \
  --release=test-release-010
```

## Promote rollout to staging (canary)
```shell
gcloud deploy rollouts advance test-release-010-to-cluster-production-0001 \
  --project=swag-nino-chang \
  --region=us-central1 \
  --delivery-pipeline=my-canary-demo-app-1 \
  --release=test-release-010
```
