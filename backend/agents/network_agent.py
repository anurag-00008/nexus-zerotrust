"""
NEXUS Network Agent
Detects unusual traffic patterns, bandwidth floods, inter-pod network issues
"""
from typing import List, Dict

class NetworkAgent:
    def __init__(self):
        self.history: Dict[str, List] = {}

    def analyze(self, pods: List[Dict]) -> Dict:
        alerts = []
        insights = []
        bandwidth_hogs = []

        for pod in pods:
            name = pod["pod"]
            net_in = pod["network_in_kbps"]
            net_out = pod["network_out_kbps"]
            total = net_in + net_out

            if name not in self.history:
                self.history[name] = []
            self.history[name].append(total)
            if len(self.history[name]) > 20:
                self.history[name].pop(0)

            avg = sum(self.history[name]) / len(self.history[name])

            if total > 500:
                bandwidth_hogs.append({
                    "pod": name,
                    "namespace": pod["namespace"],
                    "net_in_kbps": net_in,
                    "net_out_kbps": net_out,
                    "total_kbps": total
                })

            # Detect sudden spike vs average
            if len(self.history[name]) >= 5 and avg > 0 and total > avg * 3:
                alerts.append({
                    "severity": "CRITICAL",
                    "pod": name,
                    "namespace": pod["namespace"],
                    "message": f"Network spike: {round(total)}kbps (3x avg). Possible flood or DDoS reflection.",
                    "type": "network"
                })
            elif total > 800:
                alerts.append({
                    "severity": "WARNING",
                    "pod": name,
                    "namespace": pod["namespace"],
                    "message": f"High bandwidth usage: {round(total)}kbps",
                    "type": "network"
                })

        if bandwidth_hogs:
            top = sorted(bandwidth_hogs, key=lambda x: x["total_kbps"], reverse=True)[0]
            insights.append(f"Top network consumer: {top['pod']} at {round(top['total_kbps'])}kbps total")

        return {
            "agent": "Network",
            "alerts": alerts,
            "insights": insights,
            "bandwidth_hogs": bandwidth_hogs
        }
