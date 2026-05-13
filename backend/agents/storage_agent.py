"""
NEXUS Storage Agent
Monitors PVC I/O, disk usage, storage bottlenecks
"""
from typing import List, Dict

class StorageAgent:
    def __init__(self):
        self.history: Dict[str, List] = {}

    def analyze(self, pods: List[Dict]) -> Dict:
        alerts = []
        insights = []
        hot_pods = []

        for pod in pods:
            name = pod["pod"]
            disk = pod["disk_io_mbps"]
            pvc = pod["pvc_ops_per_sec"]

            if name not in self.history:
                self.history[name] = []
            self.history[name].append({"disk": disk, "pvc": pvc})
            if len(self.history[name]) > 20:
                self.history[name].pop(0)

            if disk > 50 or pvc > 100:
                hot_pods.append({"pod": name, "namespace": pod["namespace"], "disk_io": disk, "pvc_ops": pvc})
                alerts.append({
                    "severity": "WARNING",
                    "pod": name,
                    "namespace": pod["namespace"],
                    "message": f"High I/O: {disk} MB/s disk, {pvc} PVC ops/s",
                    "type": "storage"
                })
            if disk > 100:
                alerts.append({
                    "severity": "CRITICAL",
                    "pod": name,
                    "namespace": pod["namespace"],
                    "message": f"I/O storm detected — {disk} MB/s exceeds safe threshold",
                    "type": "storage"
                })

        if hot_pods:
            insights.append(f"{len(hot_pods)} pod(s) showing elevated I/O. Consider SSD-backed PVCs or read caching.")

        return {
            "agent": "Storage",
            "alerts": alerts,
            "insights": insights,
            "hot_pods": hot_pods
        }
