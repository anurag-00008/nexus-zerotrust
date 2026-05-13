"""
NEXUS Memory Agent
Detects memory leaks, OOM risks, and consumption trends
"""

from typing import List, Dict

class MemoryAgent:
    def __init__(self):
        self.history: Dict[str, List[float]] = {}
        self.thresholds = {"warning": 600, "critical": 900}  # MB

    def analyze(self, pods: List[Dict]) -> Dict:
        alerts = []
        insights = []
        leak_suspects = []

        for pod in pods:
            name = pod["pod"]
            mem = pod["memory_mb"]

            if name not in self.history:
                self.history[name] = []
            self.history[name].append(mem)
            if len(self.history[name]) > 30:
                self.history[name].pop(0)

            # Detect monotonic increase (memory leak pattern)
            hist = self.history[name]
            if len(hist) >= 5:
                trend = hist[-1] - hist[0]
                if trend > 100 and all(hist[i] <= hist[i+1] for i in range(len(hist)-3, len(hist)-1)):
                    leak_suspects.append({
                        "pod": name,
                        "namespace": pod["namespace"],
                        "trend_mb": round(trend, 2),
                        "current_mb": mem
                    })
                    alerts.append({
                        "severity": "WARNING",
                        "pod": name,
                        "namespace": pod["namespace"],
                        "message": f"Possible memory leak — +{round(trend,1)}MB trend detected",
                        "type": "memory"
                    })

            if mem >= self.thresholds["critical"]:
                alerts.append({
                    "severity": "CRITICAL",
                    "pod": name,
                    "namespace": pod["namespace"],
                    "message": f"Memory at {mem}MB — OOM kill imminent",
                    "type": "memory"
                })
            elif mem >= self.thresholds["warning"]:
                alerts.append({
                    "severity": "WARNING",
                    "pod": name,
                    "namespace": pod["namespace"],
                    "message": f"Memory usage high at {mem}MB",
                    "type": "memory"
                })

        insights = []
        if leak_suspects:
            suspects = ", ".join(s["pod"] for s in leak_suspects[:3])
            insights.append(f"Memory leak pattern detected in: {suspects}")
            insights.append("Recommend heap profiling and reviewing object lifecycle management")

        return {
            "agent": "Memory",
            "alerts": alerts,
            "insights": insights,
            "leak_suspects": leak_suspects
        }
