# KEDA
REF: https://keda.sh/docs/2.18/deploy/#yaml

## Installation

#### Including admission webhooks
kubectl apply --server-side -f https://github.com/kedacore/keda/releases/download/v2.18.3/keda-2.18.3.yaml
#### Without admission webhooks
kubectl apply --server-side -f https://github.com/kedacore/keda/releases/download/v2.18.3/keda-2.18.3-core.yaml