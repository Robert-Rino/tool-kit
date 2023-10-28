# Make docker image

docker pull nginx
export PREFIX=nginx
export TAG=$PREFIX-$(date +%s)
export IMAGE="asia-east1-docker.pkg.dev/$PROJECT_ID/pop-stats/pop-stats:$TAG"
docker tag nginx $IMAGE
gcloud auth configure-docker us-central1-docker.pkg.dev
docker push $IMAGE


# Create release
gcloud deploy releases create test-release-001 \
  --project=swag-nino-chang \
  --region=us-central1 \
  --delivery-pipeline=my-gke-demo-app-1 \
  --images my-app-image=us-central1-docker.pkg.dev/swag-nino-chang/nginx/nginx:release-1


# Run demo app
## Use default debug message
`docker run --name nginx-debug --rm -p 8080:80 --env DEBUG_MESSAGE='Nino Message' a901002666/debug-nginx`

## Call debug route
`http :8080/debug`

