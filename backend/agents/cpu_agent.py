"""
NEXUS CPU Agent
Analyzes CPU patterns, detects spikes, identifies throttling
"""

from typing import List, Dict

class CPUAgent:
    def __init__(self):
        self.history: Dict[str, List[float]] = {}
        self.thresholds = {"warning": 60, "critical": 85}

    def analyze(self, pods: List[Dict]) -> Dict:
        alerts = []
        insights = []
        top_consumers = []

        for pod in pods:
            name = pod["pod"]
            cpu = pod["cpu_percent"]

            if name not in self.history:
                self.history[name] = []
            self.history[name].append(cpu)
            if len(self.history[name]) > 30:
                self.history[name].pop(0)

            avg = sum(self.history[name]) / len(self.history[name])
            top_consumers.append({"pod": name, "namespace": pod["namespace"], "cpu": cpu, "avg": round(avg, 2)})

            if cpu >= self.thresholds["critical"]:
                alerts.append({
                    "severity": "CRITICAL",
                    "pod": name,
                    "namespace": pod["namespace"],
                    "message": f"CPU at {cpu}% — immediate throttling risk",
                    "type": "cpu"
                })
            elif cpu >= self.thresholds["warning"]:
                alerts.append({
                    "severity": "WARNING",
                    "pod": name,
                    "namespace": pod["namespace"],
                    "message": f"CPU elevated at {cpu}%",
                    "type": "cpu"
                })

        top_consumers.sort(key=lambda x: x["cpu"], reverse=True)

        if top_consumers:
            top = top_consumers[0]
            insights.append(f"Highest CPU consumer: {top['pod']} in {top['namespace']} at {top['cpu']}%")
            if top["cpu"] > 80:
                insights.append(f"Recommend horizontal scaling or resource limit review for {top['pod']}")

        return {
            "agent": "CPU",
            "alerts": alerts,
            "insights": insights,
            "top_consumers": top_consumers[:5]
        }
