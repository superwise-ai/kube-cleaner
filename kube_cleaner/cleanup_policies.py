##################################
# Modules
##################################
import logging
import os
from datetime import datetime, timedelta

import kopf
from kubernetes import client, config

##################################
# Clients
##################################
# Load Kubernetes config
config.load_config()
core_v1 = client.CoreV1Api()

##################################
# Environment Variables
##################################
timer_interval = int(os.getenv("KUBE_CLEANER_TIMER_INTERVAL", 300))

##################################
# Functions
##################################
# Convert time string to seconds
def convert_to_seconds(s):
    UNITS = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days", "w": "weeks"}
    count = int(s[:-1])
    unit = UNITS[s[-1]]
    td = timedelta(**{unit: count})
    return td.seconds + 60 * 60 * 24 * td.days


# Get pod last transition time for a condition reason
def get_pod_last_transition_time(pod, reason):
    for condition in pod.status.conditions:
        if condition.reason == reason:
            return condition.last_transition_time


# Clean pod according to the defined rule
def clean_pod_by_rule(pod, rule):
    # Get the pod condition reason
    if pod.status.phase == "Failed":
        reason = "PodFailed"
    elif pod.status.phase == "Succeeded":
        reason = "PodCompleted"

    # Get the pod last transition time
    last_transition_time = get_pod_last_transition_time(pod, reason)

    # Define the time delta for the pod cleanup
    delta = timedelta(seconds=convert_to_seconds(rule[pod.status.phase.lower()]))

    # Remove the pod if older than the defined time
    if datetime.now().timestamp() >= (last_transition_time + delta).timestamp():
        try:
            core_v1.delete_namespaced_pod(pod.metadata.name, pod.metadata.namespace)
            logging.info(f'Pod {pod.metadata.namespace}/{pod.metadata.name} with phase "{pod.status.phase}" deleted.')
        except Exception as e:
            logging.error(f"Failed to delete pod {pod.metadata.namespace}/{pod.metadata.name}: {e.reason}")


# Cleanup pods according to the rules that are defined in the policy
def cleanup(body):
    namespace = body["metadata"]["namespace"] if "namespace" in body["metadata"] else None
    rules = body["spec"]["rules"]
    for rule in rules:
        label_selector = (
            ",".join(f"{key}={value}" for key, value in rule["labelSelector"].items())
            if "labelSelector" in rule
            else None
        )
        if namespace:
            pods = core_v1.list_namespaced_pod(namespace=namespace, label_selector=label_selector)
        else:
            pods = core_v1.list_pod_for_all_namespaces(label_selector=label_selector)
        if pods.items:
            for pod in pods.items:
                if (rule["failed"] and pod.status.phase == "Failed") or (
                    rule["succeeded"] and pod.status.phase == "Succeeded"
                ):
                    clean_pod_by_rule(pod, rule)


##################################
# Custom Resources
##################################
@kopf.timer(kind="CleanupPolicy", group="dev.superwise.ai", interval=timer_interval)
def clean_namespaced_pods(body, **kwargs):
    cleanup(body)


@kopf.timer(kind="ClusterCleanupPolicy", group="dev.superwise.ai", interval=timer_interval)
def clean_pods(body, **kwargs):
    cleanup(body)
