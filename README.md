# kube-cleaner

[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![](https://github.com/superwise-ai/kube-cleaner/workflows/Release%20Charts/badge.svg?branch=main)](https://github.com/superwise-ai/kube-cleaner/actions)
[![](https://github.com/superwise-ai/kube-cleaner/workflows/Build/badge.svg?branch=main)](https://github.com/superwise-ai/kube-cleaner/actions)

Kubernetes operator that performs a customized cleanup of completed or failed pods.  
The operator is working with Kubernetes custom resource definitions that defines the cleanup policies.  
Powered by [Kopf](https://github.com/nolar/kopf).

# Custom resources

The following Kubernetes CRs are available:

- `CleanupPolicy` - a namespaced resource that can define one or more cleanup rules. All rules in this policy are scoped to the namespace.
- `ClusterCleanupPolicy` - a cluster scope resources that can define one or more cleanup roles that will apply for the entire cluster (all namespaces).  
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
