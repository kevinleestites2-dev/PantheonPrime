#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════╗
║                 PANTHEON PRIME  v2.0.0                     ║
║        The Central Nervous System of the Pantheon          ║
║  Hybrid Sovereign Infrastructure — Cloud + Mobile Edge     ║
╠════════════════════════════════════════════════════════════╣
║  Pulse   → GitHub Actions (24/7 immortal loop)             ║
║  Muscle  → Red Magic (high-speed local inference)          ║
║  Nexus   → HTTP bridge between Pulse and Muscle            ║
║  Memory  → CrowdResearch + Evolving-Memory                 ║
║  DNA     → Self-evolving Qwen3-1.7B + LoRA stack           ║
╚════════════════════════════════════════════════════════════╝
"""

import asyncio
import hashlib
import json
import logging
import os
import subprocess
import sys
import tempfile
import time
import aiohttp
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Dict, List
from dataclasses import dataclass, field
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def _atomic_write(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(
        mode="w", dir=str(path.parent), prefix="." + path.name + ".",
        suffix=".tmp", delete=False,
    )
    try:
        json.dump(data, tmp, indent=2)
        tmp.flush(); os.fsync(tmp.fileno()); tmp.close()
        os.replace(tmp.name, str(path))
    except Exception:
        try: os.unlink(tmp.name)
        except Exception: pass
        raise


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


# ═══════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s][PULSE] %(message)s",
)
log = logging.getLogger("PANTHEON")


# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

CONFIG = {
    "name": "PantheonPrime",
    "version": "2.0.0",
    "author": "kevinleestites2-dev",
    "state_dir": Path(os.getenv("PANTHEON_STATE_DIR", "pantheon_state")),
    "nexus_url": os.getenv("NEXUS_URL", ""),
    "nexus_token": os.getenv("NEXUS_TOKEN", ""),
    "github_repo": os.getenv("GITHUB_REPO", ""),
    "github_token": os.getenv("GITHUB_TOKEN", ""),
    "pulse_interval": int(os.getenv("PULSE_INTERVAL", "300")),
    "dream_interval": int(os.getenv("DREAM_INTERVAL", "3600")),
    "max_retries": 3,
}

# ═══════════════════════════════════════════════════════════════
# SHARED SESSION
# ═══════════════════════════════════════════════════════════════

_SESSION: Optional[aiohttp.ClientSession] = None


async def _get_session() -> aiohttp.ClientSession:
    global _SESSION
    if _SESSION is None or _SESSION.closed:
        _SESSION = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
    return _SESSION


async def _close_session():
    global _SESSION
    if _SESSION and not _SESSION.closed:
        await _SESSION.close()
        _SESSION = None


# ═══════════════════════════════════════════════════════════════
# PULSE STATE
# ═══════════════════════════════════════════════════════════════

@dataclass
class PulseRecord:
    cycle: int
    timestamp: str
    nexus_online: bool
    muscle_online: bool
    primed_repos: list[str]
    memory_consolidated: bool
    dreams_run: int
    issues_opened: int
    errors: list[str]


class PulseState:
    def __init__(self, path: Path):
        self.path = path
        self._records: List[PulseRecord] = []
        self._primes: Dict[str, dict] = {}
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
                self._records = [PulseRecord(**r) for r in data.get("records", [])]
                self._primes = data.get("primes", {})
            except Exception:
                self._records = []
                self._primes = {}

    async def save(self):
        _atomic_write(self.path, {
            "records": [r.__dict__ for r in self._records[-50:]],
            "primes": self._primes,
        })

    async def append(self, record: PulseRecord):
        self._records.append(record)
        await self.save()

    async def register_prime(self, name: str, info: dict):
        self._primes[name] = {**info, "last_seen": _utcnow()}
        await self.save()

    def last_record(self) -> Optional[PulseRecord]:
        return self._records[-1] if self._records else None

    def prime_list(self) -> List[str]:
        return list(self._primes.keys())


STATE = PulseState(CONFIG["state_dir"] / "pulse_state.json")


# ═══════════════════════════════════════════════════════════════
# NEXUS — bridge to Red Magic / Muscle
# ═══════════════════════════════════════════════════════════════

class Nexus:
    """HTTP bridge between Pulse (cloud) and Muscle (mobile edge)."""

    def __init__(self):
        self.url = CONFIG["nexus_url"]
        self.token = CONFIG["nexus_token"]
        self.online = False

    async def ping(self) -> bool:
        """Check if Red Magic / Muscle is reachable."""
        if not self.url:
            return False
        try:
            session = await _get_session()
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            async with session.get(f"{self.url}/health", headers=headers) as resp:
                self.online = resp.status == 200
                return self.online
        except Exception:
            self.online = False
            return False

    async def infer(self, prompt: str, max_tokens: int = 256) -> Optional[str]:
        """Run inference on Muscle (Red Magic llama.cpp server)."""
        if not self.url:
            return None
        try:
            session = await _get_session()
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            async with session.post(
                f"{self.url}/completion",
                headers=headers,
                json={"prompt": prompt, "max_tokens": max_tokens},
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("content", "")
        except Exception as e:
            log.warning(f"[NEXUS] Inference failed: {e}")
        return None

    async def push_model(self, model_path: str) -> bool:
        """Push a new GGUF model to the Red Magic."""
        if not self.url:
            return False
        try:
            session = await _get_session()
            headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
            async with session.post(
                f"{self.url}/model/push",
                headers=headers,
                json={"path": model_path},
            ) as resp:
                return resp.status == 200
        except Exception:
            return False


NEXUS = Nexus()


# ═══════════════════════════════════════════════════════════════
# KNOWLEDGE STREAMS — CrowdResearch bridge
# ═══════════════════════════════════════════════════════════════

class KnowledgeStream:
    """Persistent log of traces from all primes — trades, bids, leads."""

    def __init__(self, path: Path):
        self.path = path
        self._entries: List[dict] = []
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                self._entries = json.loads(self.path.read_text())
            except Exception:
                self._entries = []

    async def record(self, prime: str, trace: dict):
        trace["prime"] = prime
        trace["ts"] = _utcnow()
        self._entries.append(trace)
        if len(self._entries) > 1000:
            self._entries = self._entries[-500:]
        await asyncio.to_thread(_atomic_write, self.path, self._entries)

    async def query(self, prime: str = None, n: int = 20) -> List[dict]:
        if prime:
            return [e for e in self._entries if e.get("prime") == prime][-n:]
        return self._entries[-n:]

    async def consolidate(self) -> str:
        """Distill recent traces into a memory summary."""
        if not self._entries[-20:]:
            return "No recent traces to consolidate."
        samples = json.dumps(self._entries[-10:], indent=2)[:2000]
        return f"Knowledge Stream: {len(self._entries)} total traces.\nRecent: {samples}"


STREAM = KnowledgeStream(CONFIG["state_dir"] / "knowledge_stream.json")


# ═══════════════════════════════════════════════════════════════
# GITHUB — self-committing
# ═══════════════════════════════════════════════════════════════

class GitHubPulse:
    def __init__(self):
        self.repo = CONFIG["github_repo"]
        self.token = CONFIG["github_token"]
        self.enabled = bool(self.repo and self.token)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _gh_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"token {self.token}",
                    "Accept": "application/vnd.github.v3+json",
                }
            )
        return self._session

    async def commit_state(self, message: str):
        if not self.enabled:
            return
        try:
            for cmd in [
                ["git", "add", "-A"],
                ["git", "commit", "-m", f"[PULSE] {message}"],
                ["git", "push"],
            ]:
                proc = await asyncio.create_subprocess_exec(
                    *cmd, stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if proc.returncode != 0:
                    log.warning(f"[GIT] {cmd[0]} failed: {stderr.decode()[:120]}")
                    return
            log.info(f"[GIT] Committed: {message[:60]}")
        except Exception as e:
            log.warning(f"[GIT] {e}")

    async def create_issue(self, title: str, body: str) -> Optional[int]:
        if not self.enabled:
            return None
        try:
            session = await self._gh_session()
            async with session.post(
                f"https://api.github.com/repos/{self.repo}/issues",
                json={"title": title, "body": body},
            ) as resp:
                if resp.status == 201:
                    data = await resp.json()
                    log.info(f"[GIT] Issue #{data['number']}: {title[:60]}")
                    return data["number"]
        except Exception as e:
            log.warning(f"[GIT] Issue failed: {e}")
        return None

    async def prime_heartbeat(self, prime_name: str, status: dict):
        """Receive heartbeat from a connected prime agent."""
        await STATE.register_prime(prime_name, status)
        log.info(f"[PULSE] Prime heartbeat: {prime_name} — {status.get('status', 'unknown')}")


GITHUB = GitHubPulse()


# ═══════════════════════════════════════════════════════════════
# DREAM CYCLE — Evolving-Memory consolidation
# ═══════════════════════════════════════════════════════════════

async def dream_cycle(cycle: int):
    """Consolidate knowledge streams, run introspection."""
    log.info(f"[DREAM] ⚡ Cycle {cycle} consolidation...")

    summary = await STREAM.consolidate()
    primes = STATE.prime_list()
    nexus_ok = await NEXUS.ping()

    dream = (
        f"# Dream Report — Cycle {cycle}\n\n"
        f"## Nexus Status\n"
        f"- Red Magic online: {nexus_ok}\n"
        f"- Connected primes: {len(primes)}\n"
        f"- Primes: {', '.join(primes) or 'none'}\n\n"
        f"## Knowledge Stream\n{summary}\n\n"
        f"---\nGenerated: {_utcnow()}\n"
    )

    dream_path = CONFIG["state_dir"] / "dreams" / f"dream_{cycle}.md"
    dream_path.parent.mkdir(parents=True, exist_ok=True)
    await asyncio.to_thread(dream_path.write_text, dream)

    log.info(f"[DREAM] Report saved: {dream_path.name}")


# ═══════════════════════════════════════════════════════════════
# PULSE — the main cycle
# ═══════════════════════════════════════════════════════════════

async def pulse_cycle(cycle: int) -> PulseRecord:
    """
    One full pulse cycle:
    1. Check Nexus link → Red Magic status
    2. Process knowledge streams
    3. Consolidate memory
    4. Check evolution queue
    5. Commit state to GitHub
    """
    errors: List[str] = []

    # 1. NEXUS — check Red Magic
    nexus_ok = await NEXUS.ping()
    if not nexus_ok:
        errors.append("Nexus offline — Red Magic unreachable")

    # 2. KNOWLEDGE — process traces
    primes = STATE.prime_list()

    # 3. MEMORY — consolidate
    memory_ok = True
    try:
        await STREAM.consolidate()
    except Exception as e:
        memory_ok = False
        errors.append(f"Memory consolidation failed: {e}")

    # 4. EVOLVE — check if any primes need attention
    issues_opened = 0
    for prime in primes:
        info = STATE._primes.get(prime, {})
        last_seen = info.get("last_seen", "")
        if last_seen:
            try:
                last_dt = datetime.fromisoformat(last_seen)
                if (datetime.now(timezone.utc) - last_dt).total_seconds() > 86400:
                    await GITHUB.create_issue(
                        f"[PULSE] {prime} appears offline",
                        f"{prime} hasn't checked in since {last_seen}.\n"
                        f"Cycle: {cycle}"
                    )
                    issues_opened += 1
            except Exception:
                pass

    record = PulseRecord(
        cycle=cycle,
        timestamp=_utcnow(),
        nexus_online=nexus_ok,
        muscle_online=nexus_ok,
        primed_repos=primes,
        memory_consolidated=memory_ok,
        dreams_run=0,
        issues_opened=issues_opened,
        errors=errors,
    )

    await STATE.append(record)

    # 5. GIT — commit state
    status_line = (
        f"Cycle {cycle} | Nexus: {'✅' if nexus_ok else '❌'} | "
        f"Primes: {len(primes)} | Issues: {issues_opened}"
    )
    await GITHUB.commit_state(status_line)

    return record


# ═══════════════════════════════════════════════════════════════
# STATUS — live system report
# ═══════════════════════════════════════════════════════════════

async def status_report() -> str:
    last = STATE.last_record()
    primes = STATE.prime_list()
    traces = await STREAM.query(n=1)
    last_trace = traces[0] if traces else None

    return (
        f"╔════════════════════════════════════════════╗\n"
        f"║        PANTHEON PRIME — STATUS             ║\n"
        f"╚════════════════════════════════════════════╝\n"
        f"Version:      {CONFIG['version']}\n"
        f"Nexus:        {'🟢 ONLINE' if (last and last.nexus_online) else '🔴 OFFLINE'}\n"
        f"Primes:       {len(primes)} connected\n"
        f"              {', '.join(primes) if primes else '(none)'}\n"
        f"Last cycle:   {last.cycle if last else 0}\n"
        f"Last trace:   {last_trace['ts'] if last_trace else 'never'}\n"
        f"Pulse beat:   every {CONFIG['pulse_interval']}s\n"
    )


# ═══════════════════════════════════════════════════════════════
# MAIN — The Eternal Pulse
# ═══════════════════════════════════════════════════════════════

async def main():
    log.info("╔════════════════════════════════════════════╗")
    log.info("║      PANTHEON PRIME — PULSE ONLINE         ║")
    log.info("║  The Central Nervous System of the Pantheon ║")
    log.info("╚════════════════════════════════════════════╝")
    log.info(f"Nexus URL: {CONFIG['nexus_url'] or 'not configured'}")
    log.info(f"GitHub:    {'ENABLED' if GITHUB.enabled else 'DISABLED'}")
    log.info(f"Pulse:     every {CONFIG['pulse_interval']}s")

    cycle = 0
    last_dream = time.time()

    while True:
        try:
            cycle += 1
            log.info(f"[PULSE] ⚡ Cycle {cycle} — {_utcnow()}")

            record = await pulse_cycle(cycle)
            status = "🟢" if not record.errors else "🟡"
            log.info(f"[PULSE] {status} Complete | Errors: {len(record.errors)}")

            for err in record.errors:
                log.warning(f"[PULSE]  ⚠ {err}")

            # Dream cycle
            if time.time() - last_dream > CONFIG["dream_interval"]:
                await dream_cycle(cycle)
                last_dream = time.time()

            # Status every 10 cycles
            if cycle % 10 == 0:
                log.info(await status_report())

            await asyncio.sleep(CONFIG["pulse_interval"])

        except KeyboardInterrupt:
            log.info("[PULSE] Shutdown — Pantheon Prime rests.")
            print(await status_report())
            break
        except Exception as e:
            log.error(f"[PULSE] Critical error: {e}")
            await GITHUB.create_issue(
                f"[PULSE] Cycle {cycle} failure",
                f"Error: {e}\nTime: {_utcnow()}"
            )
            await asyncio.sleep(30)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "status":
            async def _status():
                print(await status_report())
            asyncio.run(_status())

        elif cmd == "once":
            async def _once():
                record = await pulse_cycle(0)
                print(json.dumps(record.__dict__, indent=2))
            asyncio.run(_once())

        elif cmd == "dream":
            async def _dream():
                await dream_cycle(0)
            asyncio.run(_dream())

        elif cmd == "primes":
            async def _primes():
                primes = STATE.prime_list()
                if primes:
                    print(f"\n{len(primes)} connected primes:\n")
                    for p in primes:
                        info = STATE._primes.get(p, {})
                        print(f"  🔱 {p} — last seen: {info.get('last_seen', 'unknown')}")
                else:
                    print("No primes connected yet.")
            asyncio.run(_primes())

        sys.exit(0)

    asyncio.run(main())
