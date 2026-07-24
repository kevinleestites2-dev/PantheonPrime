# 🔱 PantheonPrime

**The Central Nervous System of the Pantheon. v2.0.0**

PantheonPrime is a Hybrid Sovereign Infrastructure — the immortal heart that keeps every Pantheon agent alive, connected, and evolving. It bridges persistent cloud orchestration (GitHub Actions) with high-performance mobile edge inference (Red Magic).

## 🏛️ Hybrid Architecture

| Layer | Where | Role |
|---|---|---|
| **Pulse** | GitHub Actions | 24/7 immortal loop — state, evolution, fallback |
| **Muscle** | Red Magic phone | High-speed local inference via llama.cpp |
| **Nexus** | HTTP bridge | Connects Pulse ↔ Muscle |
| **Memory** | Evolving-Memory + CrowdResearch | Knowledge streams from all primes |
| **DNA** | Qwen3-1.7B + LoRA | Self-evolving model stack |

## The Pulse Cycle

Every pulse cycle (configurable, default every 5 minutes):

```
1. NEXUS   → Check Red Magic health
2. MEMORY  → Process knowledge streams from all primes
3. CONSOLIDATE → Distill traces into memory
4. EVOLVE  → Check if any primes need attention (offline >24h = auto-issue)
5. COMMIT  → Push state to GitHub
```

## The 13 Pieces

1. `llama.cpp` — Runtime engine
2. `Qwen3-1.7B` — Brain model
3. `LoRA Adapter` — DNA imprint
4. `TinyVector` — Memory store
5. `MoE Router` — Routing brain
6. `Inference Server` — API layer
7. `GGUF Quantizer` — Compression
8. `Evolving-Memory` — Sleep/dream cycle
9. `AutoResearch-Mini` — Trainer
10. `A-Evolve` — Evolution engine
11. `AdaptiveHarness` — Adaptive evolution
12. `CrowdResearch` — Shared knowledge
13. `Game Space` — Sustained performance

## Quick Start

```bash
# Clone
git clone https://github.com/kevinleestites2-dev/PantheonPrime.git
cd PantheonPrime

# Install
pip install aiohttp

# Set environment
export GITHUB_REPO=your-username/your-repo
export GITHUB_TOKEN=your_token
export NEXUS_URL=http://your-red-magic:8080    # optional
export PULSE_INTERVAL=300                       # seconds

# Run the eternal pulse
python pulse.py

# Or single cycle
python pulse.py once

# Status report
python pulse.py status

# List connected primes
python pulse.py primes

# Trigger dream consolidation
python pulse.py dream
```

## GitHub Actions

The `.github/workflows/pulse.yml` workflow runs every 6 hours as backup. It:
1. Runs `pulse.py`
2. Commits state + dreams back to the repo
3. Self-restarts via workflow dispatch

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GITHUB_REPO` | For auto-commit | — | `user/repo` |
| `GITHUB_TOKEN` | For auto-commit | — | PAT with repo scope |
| `NEXUS_URL` | For muscle | — | Red Magic inference server |
| `NEXUS_TOKEN` | Optional | — | Auth for Nexus |
| `PULSE_INTERVAL` | No | `300` | Seconds between cycles |
| `DREAM_INTERVAL` | No | `3600` | Seconds between dream consolidations |

## Fail-Safe Protocol

- If Red Magic is offline → Pulse handles everything via cloud fallback
- If Pulse hits job limit → Self-restart via Actions API
- State is NEVER stored only in RAM — every cycle commits to GitHub

---

*Built for the Pantheon Project*  
*"The Central Nervous System never sleeps."* 🔱
