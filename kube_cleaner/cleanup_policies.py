##################################
# Modules
##################################
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Text

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
def convert_to_seconds(s: Text):
    """Convert time string to seconds"""
    UNITS = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days", "w": "weeks"}
    count = int(s[:-1])
    unit = UNITS[s[-1]]
    td = timedelta(**{unit: count})
    return td.seconds + 60 * 60 * 24 * td.days


def get_pod_last_transition_time(pod: client.V1Pod, reason: Text):
    """Get pod last transition time for a condition reason"""
    for condition in pod.status.conditions:
        if condition.reason == reason:
            return condition.last_transition_time
    return False


def get_label_selector(rule: Dict):
    """Get the label selector from the rule"""
    label_selector = (
        ",".join(f"{key}={value}" for key, value in rule["labelSelector"].items()) if "labelSelector" in rule else None
    )
    return label_selector


def cleanup_pods_by_rule(rule: Dict, policy_kind: Text, policy_name: Text, namespace=None, label_selector=None):
    """Cleanup pods by a rule defined in the policy"""
    if namespace:
        pods = core_v1.list_namespaced_pod(namespace=namespace, label_selector=label_selector)
    else:
        pods = core_v1.list_pod_for_all_namespaces(label_selector=label_selector)
    if pods.items:
        for pod in pods.items:
            if ("failed" in rule and rule["failed"] and pod.status.phase == "Failed") or (
                "succeeded" in rule and rule["succeeded"] and pod.status.phase == "Succeeded"
            ):
                # Define the policy identifier for the log message
                policy = f"{namespace}/{policy_kind}/{policy_name}" if namespace else f"{policy_kind}/{policy_name}"
                # Get the pod condition reason
                if pod.status.phase == "Failed":
                    reason = "PodFailed"
                elif pod.status.phase == "Succeeded":
                    reason = "PodCompleted"
                # Get the rule time
                rule_time = rule[pod.status.phase.lower()]
                # Get the pod last transition time
                last_transition_time = get_pod_last_transition_time(pod, reason)
                # If the pod last_transition_time is not empty
                if last_transition_time:
                    # Define the time delta for the pod cleanup
                    delta = timedelta(seconds=convert_to_seconds(rule_time))
                    # Remove the pod if older than the defined time
                    if datetime.now().timestamp() >= (last_transition_time + delta).timestamp():
                        try:
                            core_v1.delete_namespaced_pod(pod.metadata.name, pod.metadata.namespace)
                            logging.info(
                                f'{policy} - pod {pod.metadata.namespace}/{pod.metadata.name} with phase "{pod.status.phase}" deleted (older than {rule_time}).'
                            )
                        except Exception as e:
                            logging.error(
                                f"Failed to delete pod {pod.metadata.namespace}/{pod.metadata.name}: {e.reason}"
                            )


def cleanup(body: Dict):
    """Cleanup resources according to the rules that are defined in the policy"""
    namespace = body["metadata"]["namespace"] if "namespace" in body["metadata"] else None
    rules = body["spec"]["rules"]
    for resource_type in rules:
        for rule in rules[resource_type]:
            label_selector = get_label_selector(rule)
            if resource_type == "pods":
                cleanup_pods_by_rule(
                    rule, body["kind"], body["metadata"]["name"], namespace=namespace, label_selector=label_selector
                )


##################################
# Custom Resources
##################################
@kopf.timer(kind="CleanupPolicy", group="dev.superwise.ai", interval=timer_interval)
@kopf.timer(kind="ClusterCleanupPolicy", group="dev.superwise.ai", interval=timer_interval)
def run_cleanup(body, **kwargs):
    cleanup(body)
