"""
Deployment: Kubernetes deployment patterns and Helm chart equivalents.
Demonstrates manifests, probes, resource limits, and rolling updates in Python dicts.
"""
from typing import Any

# ─────────────────────────────────────────────────────────
# Type alias for K8s manifest
# ─────────────────────────────────────────────────────────
Manifest = dict[str, Any]

# ─────────────────────────────────────────────────────────
# Manifest builders
# ─────────────────────────────────────────────────────────
def deployment(
    name: str,
    image: str,
    replicas: int = 2,
    port: int = 8000,
    env: dict | None = None,
    cpu_request: str = "100m",
    cpu_limit: str = "500m",
    mem_request: str = "128Mi",
    mem_limit: str = "512Mi",
    tag: str = "latest",
) -> Manifest:
    """Build a Kubernetes Deployment manifest."""
    env_list = [{"name": k, "value": v} for k, v in (env or {}).items()]
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": name,
            "labels": {"app": name},
        },
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "strategy": {
                "type": "RollingUpdate",
                "rollingUpdate": {"maxSurge": 1, "maxUnavailable": 0},
            },
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [{
                        "name": name,
                        "image": f"{image}:{tag}",
                        "ports": [{"containerPort": port}],
                        "env": env_list,
                        "resources": {
                            "requests": {"cpu": cpu_request, "memory": mem_request},
                            "limits":   {"cpu": cpu_limit,   "memory": mem_limit},
                        },
                        "livenessProbe": {
                            "httpGet": {"path": "/live", "port": port},
                            "initialDelaySeconds": 10,
                            "periodSeconds": 10,
                            "failureThreshold": 3,
                        },
                        "readinessProbe": {
                            "httpGet": {"path": "/ready", "port": port},
                            "initialDelaySeconds": 5,
                            "periodSeconds": 5,
                            "failureThreshold": 3,
                        },
                    }],
                    "terminationGracePeriodSeconds": 30,
                },
            },
        },
    }


def service(name: str, port: int = 8000, service_type: str = "ClusterIP") -> Manifest:
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name},
        "spec": {
            "type": service_type,
            "selector": {"app": name},
            "ports": [{"port": 80, "targetPort": port, "protocol": "TCP"}],
        },
    }


def ingress(name: str, host: str, service_name: str, port: int = 80) -> Manifest:
    return {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": name,
            "annotations": {
                "nginx.ingress.kubernetes.io/ssl-redirect": "true",
                "cert-manager.io/cluster-issuer": "letsencrypt-prod",
            },
        },
        "spec": {
            "tls": [{"hosts": [host], "secretName": f"{name}-tls"}],
            "rules": [{
                "host": host,
                "http": {"paths": [{
                    "path": "/",
                    "pathType": "Prefix",
                    "backend": {"service": {"name": service_name,
                                            "port": {"number": port}}},
                }]},
            }],
        },
    }


def configmap(name: str, data: dict) -> Manifest:
    return {"apiVersion": "v1", "kind": "ConfigMap",
            "metadata": {"name": name}, "data": data}


def secret(name: str, string_data: dict) -> Manifest:
    return {"apiVersion": "v1", "kind": "Secret", "type": "Opaque",
            "metadata": {"name": name}, "stringData": string_data}


def horizontal_pod_autoscaler(
    name: str, min_replicas: int = 2, max_replicas: int = 10,
    cpu_utilization: int = 70
) -> Manifest:
    return {
        "apiVersion": "autoscaling/v2",
        "kind": "HorizontalPodAutoscaler",
        "metadata": {"name": name},
        "spec": {
            "scaleTargetRef": {"apiVersion": "apps/v1", "kind": "Deployment", "name": name},
            "minReplicas": min_replicas,
            "maxReplicas": max_replicas,
            "metrics": [{
                "type": "Resource",
                "resource": {"name": "cpu",
                             "target": {"type": "Utilization",
                                        "averageUtilization": cpu_utilization}},
            }],
        },
    }


# ─────────────────────────────────────────────────────────
# YAML serializer
# ─────────────────────────────────────────────────────────
def to_yaml(obj: Any, indent: int = 0) -> str:
    """Simple YAML serializer (no dependency on PyYAML)."""
    lines = []
    pad = "  " * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.append(to_yaml(v, indent + 1))
            elif v is None:
                lines.append(f"{pad}{k}: null")
            elif isinstance(v, bool):
                lines.append(f"{pad}{k}: {'true' if v else 'false'}")
            else:
                lines.append(f"{pad}{k}: {v}")
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                first = True
                for k, v in item.items():
                    prefix = f"{pad}- " if first else f"{pad}  "
                    first = False
                    if isinstance(v, (dict, list)):
                        lines.append(f"{prefix}{k}:")
                        lines.append(to_yaml(v, indent + 2))
                    else:
                        lines.append(f"{prefix}{k}: {v}")
            else:
                lines.append(f"{pad}- {item}")
    return "\n".join(lines)


if __name__ == "__main__":
    import json

    app_name = "myapi"

    print("=== Deployment Manifest ===")
    deploy = deployment(
        name=app_name,
        image="registry.example.com/myapi",
        replicas=3,
        port=8000,
        env={"DB_HOST": "postgres", "REDIS_URL": "redis://redis:6379/0",
             "ENV": "production"},
        cpu_request="200m", cpu_limit="1000m",
        mem_request="256Mi", mem_limit="1Gi",
    )
    print(json.dumps(deploy, indent=2)[:600] + "\n...")

    print("\n=== Service ===")
    svc = service(app_name, port=8000)
    print(to_yaml(svc))

    print("\n=== Ingress ===")
    ing = ingress(f"{app_name}-ingress", "api.example.com", app_name)
    print(to_yaml(ing))

    print("\n=== HPA ===")
    hpa = horizontal_pod_autoscaler(app_name, min_replicas=2, max_replicas=20)
    print(to_yaml(hpa))

    print("\n=== ConfigMap ===")
    cm = configmap(f"{app_name}-config", {
        "LOG_LEVEL": "info",
        "WORKERS": "4",
        "MAX_CONNECTIONS": "100",
    })
    print(to_yaml(cm))

    print("\n=== Secret (never commit real secrets!) ===")
    sec = secret(f"{app_name}-secret", {
        "DB_PASSWORD": "REPLACE_ME",
        "SECRET_KEY": "REPLACE_ME",
    })
    print(to_yaml(sec))
