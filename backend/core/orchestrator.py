"""
NEXUS Multi-Agent Orchestrator
Coordinates all agents, merges insights, generates NLP summaries
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.cpu_agent import CPUAgent
from agents.memory_agent import MemoryAgent
from agents.storage_agent import StorageAgent
from agents.network_agent import NetworkAgent
from k8s.mock_metrics import generate_metrics, get_dependencies
from datetime import datetime

class NexusOrchestrator:
    def __init__(self):
        self.cpu_agent = CPUAgent()
        self.memory_agent = MemoryAgent()
        self.storage_agent = StorageAgent()
        self.network_agent = NetworkAgent()
        self.alert_history = []

    def run_cycle(self) -> dict:
        pods = generate_metrics()
        deps = get_dependencies()

        cpu_result = self.cpu_agent.analyze(pods)
        mem_result = self.memory_agent.analyze(pods)
        storage_result = self.storage_agent.analyze(pods)
        net_result = self.network_agent.analyze(pods)

        all_alerts = (
            cpu_result["alerts"] +
            mem_result["alerts"] +
            storage_result["alerts"] +
            net_result["alerts"]
        )

        # Deduplicate by pod+type
        seen = set()
        unique_alerts = []
        for a in all_alerts:
            key = f"{a['pod']}_{a['type']}_{a['severity']}"
            if key not in seen:
                seen.add(key)
                unique_alerts.append(a)

        self.alert_history.extend(unique_alerts)
        if len(self.alert_history) > 100:
            self.alert_history = self.alert_history[-100:]

        all_insights = (
            cpu_result["insights"] +
            mem_result["insights"] +
            storage_result["insights"] +
            net_result["insights"]
        )

        # NLP summary
        critical_count = sum(1 for a in unique_alerts if a["severity"] == "CRITICAL")
        warning_count = sum(1 for a in unique_alerts if a["severity"] == "WARNING")

        if critical_count > 0:
            summary = f"🔴 {critical_count} critical issue(s) detected across your cluster. Immediate action required."
        elif warning_count > 0:
            summary = f"🟡 {warning_count} warning(s) active. Monitor closely and consider scaling."
        else:
            summary = "🟢 All systems nominal. No anomalies detected across monitored pods."

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "pods": pods,
            "dependencies": deps,
            "agents": {
                "cpu": cpu_result,
                "memory": mem_result,
                "storage": storage_result,
                "network": net_result
            },
            "alerts": unique_alerts,
            "insights": all_insights,
            "summary": summary,
            "stats": {
                "total_pods": len(pods),
                "critical_alerts": critical_count,
                "warning_alerts": warning_count,
                "healthy_pods": len([p for p in pods if not p.get("anomaly")])
            }
        }
