# kube-cleaner

![Version: 0.1.1](https://img.shields.io/badge/Version-0.1.1-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.1.1](https://img.shields.io/badge/AppVersion-0.1.1-informational?style=flat-square)

Kubernetes Operator for Kubernetes Pods cleanup. Powered by Kopf

## Installation

```sh
helm repo add kube-cleaner https://superwise-ai.github.io/kube-cleaner
helm repo update
helm install kube-cleaner kube-cleaner/kube-cleaner -n kube-cleaner --create-namespace
```

## Values

| Key                        | Type   | Default                                                  | Description                                                                                                            |
| -------------------------- | ------ | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| affinity                   | object | `{}`                                                     |                                                                                                                        |
| cleanupPolicies            | object | `{}`                                                     | Create cleanup policies using the chart                                                                                |
| env                        | list   | `[{"name":"KUBE_CLEANER_TIMER_INTERVAL","value":"300"}]` | Environment variables to inject                                                                                        |
| extraArgs                  | list   | `[]`                                                     | Additional command line arguments to pass                                                                              |
| fullnameOverride           | string | `""`                                                     |                                                                                                                        |
| image.pullPolicy           | string | `"IfNotPresent"`                                         |                                                                                                                        |
| image.repository           | string | `"ghcr.io/superwise-ai/kube-cleaner"`                    |                                                                                                                        |
| image.tag                  | string | `""`                                                     | Overrides the image tag whose default is the chart appVersion.                                                         |
| imagePullSecrets           | list   | `[]`                                                     |                                                                                                                        |
| nameOverride               | string | `""`                                                     |                                                                                                                        |
| nodeSelector               | object | `{}`                                                     |                                                                                                                        |
| podAnnotations             | object | `{}`                                                     |                                                                                                                        |
| podSecurityContext         | object | `{}`                                                     |                                                                                                                        |
| replicaCount               | int    | `1`                                                      |                                                                                                                        |
| resources                  | object | `{}`                                                     |                                                                                                                        |
| securityContext            | object | `{}`                                                     |                                                                                                                        |
| serviceAccount.annotations | object | `{}`                                                     | Annotations to add to the service account                                                                              |
| serviceAccount.create      | bool   | `true`                                                   | Specifies whether a service account should be created                                                                  |
| serviceAccount.name        | string | `""`                                                     | The name of the service account to use. If not set and create is true, a name is generated using the fullname template |
| tolerations                | list   | `[]`                                                     |                                                                                                                        |
| watchNamespace             | string | `""`                                                     | Namespace to watch. If not provided, the controller will watch all namespaces.                                         |

---

Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)
