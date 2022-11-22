# kube-cleaner

[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![](https://github.com/superwise-ai/kube-cleaner/workflows/Release%20Charts/badge.svg?branch=main)](https://github.com/superwise-ai/kube-cleaner/actions)
[![](https://github.com/superwise-ai/kube-cleaner/workflows/Build/badge.svg?branch=main)](https://github.com/superwise-ai/kube-cleaner/actions)

Kubernetes operator that performs a customized cleanup of completed or failed pods.  
The operator is working with Kubernetes custom resource definitions that defines the cleanup policies.  
Powered by [Kopf](https://github.com/nolar/kopf).

# Custom resources

## `CleanupPolicy` and `ClusterCleanupPolicy`

The basic Kubernetes CR that is required for `kube-cleaner` is `CleanupPolicy`.  
Each policy can define one or more cleanup rules. For each rule, the following parameters are supported:

- `succeeded`: Clean succeeded pods after a certain time. The format is `1s`, `1m`, `1h`, `1d`, etc.  
  If not provided, the cleanup will not include pods with this status.
- `failed`: Clean failed pods. The concept and format is the same as `succeeded`.
- `labelSelector`: Apply the rules above only to pods matching these labels, if provided.

`ClusterCleanupPolicy` is using the same logic but it is a cluster-wide resource.  
If created, the cleanup will include all pods in the cluster (all namespaces).  
This CR requires more permissions so the `watchNamespace` parameter in the Helm chart should not be provided for it to work (by default, the operator is watching all namespaces).

Detailed examples can be found in the [examples](examples) directory.

The CRDs can be installed using the following command:

```sh
kubectl apply -f charts/kube-cleaner/crds
```

# Helm chart

A Helm chart for deploying `kube-cleaner` is available for installation.  
The docs are available in the chart [README](charts/kube-cleaner/README.md).

# Docker image

The Docker image is available at: `ghcr.io/superwise-ai/kube-cleaner:latest`

# Local development

```sh
kopf run kube_cleaner/cleanup_policies.py -v
```
