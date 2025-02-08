# Questions
If update Deployment with image tag that doesn't exist, k8s will try to create pod but encounter `ErrImagePull`. 
In this scenario if HPA trying to scale, which version will HPA uses to scale pods ?

# Answer
HPA will scale both version by half, if target is 10 it will scale 5 old version and 5 new version.

# Flow
1. Apply normal deployment.yaml 與 hpa.yaml.
2. After pod create，update deployment into bad image ，beore hpa scales pod.
3. Wait for hpa scales pods we can monitor it scales both good and bad version of deployment.


