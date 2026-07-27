# 🔱 PANTHEON SINGULARITY — v3.0.0

**Sovereign AI — Headless · Autonomous · Self-Evolving**
*"The Central Nervous System never sleeps."*

---

## Anatomy

| Layer | File | Role |
|---|---|---|
| **Pulse** | `pulse.py` | Legacy v2.0 heartbeat — GitHub Actions immortal loop |
| **Singularity** | `pantheon_singularity.py` | v3.0 autonomous engine — 8 modes, DNA mutation, HyperLoops |
| **Blueprint** | `blueprint.md` | Architecture reference |

## The 8 Modes

| Mode | Flag | Purpose |
|---|---|---|
| **SENTINEL** | `--sentinel` | Stealth reconnaissance — passive intel gathering |
| **ORACLE** | `--oracle` | Web investigation — cross-reference, verify, deep-dive |
| **SHADOW** | `--shadow` | Autonomous tool orchestration — spawn subagents |
| **GHOST** | `--ghost` | Entity resolution — track people, places, connections |
| **NEXUS** | `--nexus` | Memory consolidation — dream cycle, connect the dots |
| **FORGE** | `--forge` | Generate reports, artifacts, timelines |
| **PRIME** | `--prime` | Self-evolution — mutate DNA, train new weights |
| **VOID** | `--void` | Cleanup, garbage collection, reset |

## DNA Mutation Engine

Every mode run triggers a genetic tick. After 10 ticks, the genome mutates:

```python
GENES = {
    "aggression":    0.5,  # 0=passive recon → 1=full strike
    "curiosity":     0.5,  # 0=stay focused → 1=explore rabbit holes
    "patience":      0.5,  # 0=move fast → 1=wait for evidence
    "skepticism":    0.5,  # 0=trust sources → 1=verify everything
    "creativity":    0.5,  # 0=literal → 1=connect distant dots
}
```

Mutation: ±0.15 per tick, clamped [0.0, 1.0]. Every 10 ticks → forced mutation. Genome hash logged each cycle.

## HyperLoop

Each mode runs in HyperLoop — a self-reinforcing cycle:

```
INIT → SCAN → ANALYZE → ACT → REPORT → COMMIT → [MUTATE] → LOOP
```

- `--count N` = N cycles, then exit
- `--infinite` = run forever
- `--interval N` = N seconds between cycles (default 300)

## Quick Start

```bash
# Single mode, single cycle
python pantheon_singularity.py --oracle "Investigate Camp Scott Volume 5"

# Sentinel mode, 5 cycles, 60s interval
python pantheon_singularity.py --sentinel --count 5 --interval 60

# Forced mutation
python pantheon_singularity.py --prime --mutate

# Dream cycle (memory consolidation)
python pantheon_singularity.py --nexus --dream

# Full stack demo
python pantheon_singularity.py --all
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GITHUB_TOKEN` | For commits | — | PAT with repo scope |
| `GITHUB_REPO` | For commits | — | `user/repo` |
| `PULSE_INTERVAL` | No | `300` | Seconds between cycles |
| `SINGULARITY_MODE` | No | `oracle` | Default mode on bare run |

## Fail-Safe

- Every cycle commits state to `pulse_log.txt` / `singularity_state.json`
- If mode crashes → state saved before exit
- If genome corrupts → regenerate from seed
- If HyperLoop infinite → `--count N` caps it

---

*Built for the Pantheon Project*
*🔱 "The Central Nervous System never sleeps."*