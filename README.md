# NEXUS — Neural EXploration & Understanding System

**Team:** **ZeroTrust**
**Hackathon:** ABB Accelerator 2026  
**Theme:** Theme 2 — Beyond Monitoring: AI Agents for Real-Time Pod Resource Discovery and Dependency Mapping

---

## 🧠 Project Overview

NEXUS is a multi-agent AI system that provides real-time visibility into containerized environments. It goes beyond traditional monitoring by using specialized AI agents to correlate resource behavior, detect anomalies, map inter-pod dependencies, and generate actionable NLP insights — all visible through a live, industrial-grade dashboard.

---

## 🏗️ Architecture

```
nexus/
├── backend/
│   ├── agents/
│   │   ├── cpu_agent.py          # CPU spike & throttle detection
│   │   ├── memory_agent.py       # Memory leak & OOM risk detection
│   │   ├── storage_agent.py      # PVC I/O & disk bottleneck analysis
│   │   └── network_agent.py      # Bandwidth flood & anomaly detection
│   ├── core/
│   │   └── orchestrator.py       # Multi-agent coordinator + NLP summary
│   ├── api/
│   │   └── main.py               # FastAPI server + WebSocket streaming
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── index.html                # Live real-time dashboard (single file)
├── k8s/
│   └── mock_metrics.py           # Minikube/K3s metrics simulator
├── docker-compose.yml
└── README.md
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **Multi-Agent AI** | 4 specialized agents (CPU, Memory, Storage, Network) run in parallel |
| **Real-Time WebSocket** | Dashboard updates every 3 seconds via WebSocket |
| **Dependency Graph** | Live SVG visualization of inter-pod communication |
| **Anomaly Injection** | Simulates CPU spikes, memory leaks, I/O storms, network floods |
| **NLP Insights** | Human-readable cluster health summaries and recommendations |
| **Sparkline Charts** | Historical trend charts for all 4 resource dimensions |
| **Alert System** | Severity-ranked alerts (CRITICAL / WARNING) per pod and namespace |

---

## 🚀 Quick Start

### Option 1: Run with Docker Compose (Recommended)

```bash
docker-compose up --build
```

Then open: [http://localhost:8000](http://localhost:8000)

---

### Option 2: Run Manually

**Step 1 — Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**Step 2 — Start the server**
```bash
cd backend
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Step 3 — Open the dashboard**

Navigate to: [http://localhost:8000](http://localhost:8000)

---

## 🧩 Multi-Agent System

### CPU Agent
- Tracks per-pod CPU history (rolling 30-sample window)
- Fires WARNING at >60%, CRITICAL at >85%
- Identifies top 5 CPU consumers

### Memory Agent
- Detects monotonic increase patterns (memory leaks)
- Fires WARNING at >600MB, CRITICAL at >900MB (OOM risk)
- Reports trend delta over observation window

### Storage Agent
- Monitors disk I/O and PVC operations per second
- Fires WARNING at >50 MB/s or >100 PVC ops/s
- Detects I/O storms (>100 MB/s)

### Network Agent
- Tracks bandwidth per pod (in + out)
- Detects sudden spikes (>3× average = flood alert)
- Reports top bandwidth consumers

---

## 📊 Dashboard Sections

1. **Header** — Live WebSocket status + timestamp
2. **Cluster Overview** — Total pods, healthy count, critical/warning counts
3. **Pod Explorer** — Sidebar list sorted by resource intensity, with anomaly flags
4. **Dependency Graph** — SVG visualization of pod-to-pod communication grouped by namespace, with pulsing anomaly indicators
5. **Sparklines** — 40-point rolling charts: CPU%, Memory MB, Disk MB/s, Network kbps
6. **Alerts Panel** — Real-time sorted alerts (CRITICAL first)
7. **Insights Panel** — AI-generated recommendations
8. **Agents Panel** — Per-agent status and findings

---

## 🔮 Simulated Anomalies

NEXUS automatically injects random anomalies to demonstrate detection:

| Anomaly | Trigger | Detection |
|---|---|---|
| `cpu_spike` | CPU → 85–99% | CPU Agent CRITICAL alert |
| `memory_leak` | RAM → 900–1024MB | Memory Agent CRITICAL + trend analysis |
| `io_storm` | Disk → 80–150 MB/s, PVC → 200–500 ops/s | Storage Agent CRITICAL |
| `network_flood` | Net → 900–1500 kbps in | Network Agent CRITICAL spike alert |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.11, FastAPI, WebSockets, Uvicorn
- **Frontend:** Vanilla HTML/CSS/JS (no build step required)
- **Simulation:** Custom Minikube-compatible metrics generator
- **Containerization:** Docker, Docker Compose
- **Fonts:** Space Mono, Syne (Google Fonts)

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serve dashboard frontend |
| `/api/health` | GET | System health check |
| `/api/snapshot` | GET | Single JSON snapshot of cluster state |
| `/ws` | WebSocket | Real-time streaming updates (3s interval) |

---

## 🏆 ABB Accelerator Alignment

| ABB Focus Area | NEXUS Coverage |
|---|---|
| Data and Artificial Intelligence | Multi-agent AI analysis framework |
| Advanced Automation | Auto-detection and alerting without manual rules |
| Cloud, Hosting, and Infrastructure | Kubernetes-native architecture |
| Internet of Things (IoT) | Edge-compatible (K3s / MicroK8s support) |
| Application and Business Process Monitoring | Full pod lifecycle and dependency monitoring |
| Operational Technology (OT) | Industrial-grade reliability and alerting |

---

## 👥 Team ByteForge

Built with 💙 for ABB Accelerator 2026.
