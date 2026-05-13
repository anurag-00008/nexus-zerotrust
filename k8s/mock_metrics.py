"""
NEXUS - Mock Kubernetes Metrics Simulator
Simulates real pod metrics from a Minikube/K3s cluster
"""

import random
import time
import math
from datetime import datetime

NAMESPACES = ["default", "monitoring", "app-prod", "database", "ingress-nginx"]

PODS = {
    "default": ["web-frontend-7d4f", "api-gateway-9b2c", "auth-service-3k1m"],
    "monitoring": ["prometheus-0", "grafana-7f9d", "alertmanager-0"],
    "app-prod": ["order-service-5x2p", "payment-svc-8q3r", "inventory-api-2m7n", "notification-worker-4j1k"],
    "database": ["postgres-primary-0", "redis-cache-6t8s", "mongodb-0"],
    "ingress-nginx": ["nginx-controller-1p9w"]
}

anomaly_pods = {}
_tick = 0

def generate_metrics():
    global _tick
    _tick += 1
    all_pods = []

    # Occasionally inject anomalies
    if _tick % 20 == 0:
        ns = random.choice(list(PODS.keys()))
        pod = random.choice(PODS[ns])
        anomaly_pods[pod] = random.choice(["cpu_spike", "memory_leak", "io_storm", "network_flood"])

    # Clear old anomalies
    if _tick % 60 == 0:
        anomaly_pods.clear()

    for ns, pods in PODS.items():
        for pod in pods:
            anomaly = anomaly_pods.get(pod)
            base_cpu = random.uniform(5, 30)
            base_mem = random.uniform(100, 400)
            base_disk = random.uniform(0.5, 5)
            base_net_in = random.uniform(10, 200)
            base_net_out = random.uniform(10, 150)
            base_pvc_ops = random.uniform(0, 20)

            if anomaly == "cpu_spike":
                base_cpu = random.uniform(85, 99)
            elif anomaly == "memory_leak":
                base_mem = random.uniform(900, 1024)
            elif anomaly == "io_storm":
                base_disk = random.uniform(80, 150)
                base_pvc_ops = random.uniform(200, 500)
            elif anomaly == "network_flood":
                base_net_in = random.uniform(900, 1500)
                base_net_out = random.uniform(700, 1200)

            # Add periodic waves for realism
            wave = math.sin(_tick * 0.1 + hash(pod) % 10) * 5

            all_pods.append({
                "pod": pod,
                "namespace": ns,
                "status": "Running" if not anomaly else random.choice(["Running", "Running", "CrashLoopBackOff"]),
                "cpu_percent": round(min(99, max(0, base_cpu + wave)), 2),
                "memory_mb": round(min(1024, max(10, base_mem + wave * 2)), 2),
                "disk_io_mbps": round(max(0, base_disk), 2),
                "network_in_kbps": round(max(0, base_net_in), 2),
                "network_out_kbps": round(max(0, base_net_out), 2),
                "pvc_ops_per_sec": round(max(0, base_pvc_ops), 2),
                "restarts": random.randint(0, 3) if anomaly else 0,
                "anomaly": anomaly,
                "timestamp": datetime.utcnow().isoformat()
            })

    return all_pods


def get_dependencies():
    """Static dependency graph between pods"""
    return [
        {"from": "web-frontend-7d4f", "to": "api-gateway-9b2c", "type": "HTTP"},
        {"from": "api-gateway-9b2c", "to": "auth-service-3k1m", "type": "gRPC"},
        {"from": "api-gateway-9b2c", "to": "order-service-5x2p", "type": "HTTP"},
        {"from": "api-gateway-9b2c", "to": "payment-svc-8q3r", "type": "HTTP"},
        {"from": "order-service-5x2p", "to": "postgres-primary-0", "type": "TCP"},
        {"from": "order-service-5x2p", "to": "redis-cache-6t8s", "type": "TCP"},
        {"from": "order-service-5x2p", "to": "inventory-api-2m7n", "type": "HTTP"},
        {"from": "payment-svc-8q3r", "to": "postgres-primary-0", "type": "TCP"},
        {"from": "inventory-api-2m7n", "to": "mongodb-0", "type": "TCP"},
        {"from": "notification-worker-4j1k", "to": "redis-cache-6t8s", "type": "TCP"},
        {"from": "prometheus-0", "to": "api-gateway-9b2c", "type": "Scrape"},
        {"from": "prometheus-0", "to": "order-service-5x2p", "type": "Scrape"},
        {"from": "grafana-7f9d", "to": "prometheus-0", "type": "Query"},
        {"from": "nginx-controller-1p9w", "to": "web-frontend-7d4f", "type": "Proxy"},
        {"from": "auth-service-3k1m", "to": "redis-cache-6t8s", "type": "TCP"},
    ]
