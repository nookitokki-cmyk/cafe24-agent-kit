"""Kit scaffold, diagnose, version, and update helpers (dist + monorepo)."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MCP_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = MCP_DIR.parent
KIT_ROOT = Path(
    os.environ.get("CAFE24_KIT_ROOT", WORKSPACE_ROOT / "agent-kit")
)
CONFIG_DIR = MCP_DIR / "config"
# Throttle cache for start-time auto-update check (gitignored — local state only)
AUTOUPDATE_CACHE = CONFIG_DIR / ".autoupdate_check.json"
TEMPLATE_CLIENT = KIT_ROOT / "clients" / "_template"
VERSION_FILE = WORKSPACE_ROOT / "VERSION"
CHANGELOG_FILE = WORKSPACE_ROOT / "CHANGELOG.md"

DEFAULT_GITHUB_REPO = os.environ.get(
    "CAFE24_KIT_GITHUB_REPO",
    "nookitokki-cmyk/cafe24-agent-kit",
)

# Optional: raw URL to latest VERSION file (line 1 = vX.Y.Z) for kit-version --check-remote
RELEASE_VERSION_URL = os.environ.get(
    "CAFE24_KIT_RELEASE_URL",
    "",
)

ONBOARDING_COMMANDS = [
    "/키트시작",
    "/새클라이언트",
    "/MCP연결",
    "/API발급",
    "/접속세팅",
]


def read_kit_version() -> dict[str, str]:
    """Read VERSION file from workspace root or dist bundle."""
    vf = VERSION_FILE
    if not vf.is_file():
        vf = KIT_ROOT.parent / "VERSION"
    if not vf.is_file():
        return {"version": "unknown", "date": "", "path": str(vf)}
    lines = vf.read_text(encoding="utf-8").strip().splitlines()
    return {
        "version": lines[0].strip() if lines else "unknown",
        "date": lines[1].strip() if len(lines) > 1 else "",
        "path": str(vf),
    }


def fetch_remote_version(url: str = RELEASE_VERSION_URL) -> dict[str, Any]:
    """Compare local VERSION via raw URL or GitHub Releases API."""
    if url:
        try:
            with urlopen(url, timeout=15) as resp:
                text = resp.read().decode("utf-8", errors="replace")
            lines = text.strip().splitlines()
            return {
                "available": True,
                "source": "url",
                "version": lines[0].strip() if lines else "unknown",
                "date": lines[1].strip() if len(lines) > 1 else "",
                "url": url,
            }
        except (URLError, OSError, TimeoutError) as e:
            return {"available": False, "error": str(e), "url": url}

    repo = DEFAULT_GITHUB_REPO.strip()
    if repo:
        try:
            rel = fetch_github_release(repo=repo, tag="latest")
            return {
                "available": True,
                "source": "github",
                "version": rel.get("tag_name", "unknown"),
                "date": (rel.get("published_at") or "")[:10],
                "repo": repo,
                "html_url": rel.get("html_url"),
            }
        except (URLError, OSError, TimeoutError, ValueError, HTTPError) as e:
            return {
                "available": False,
                "source": "github",
                "error": str(e),
                "repo": repo,
                "hint": "Set CAFE24_KIT_RELEASE_URL or check CAFE24_KIT_GITHUB_REPO",
            }

    return {
        "available": False,
        "hint": "Set CAFE24_KIT_GITHUB_REPO or CAFE24_KIT_RELEASE_URL",
    }


def _github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "cafe24-agent-kit",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        try:
            import subprocess

            r = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if r.returncode == 0:
                token = r.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _github_json(url: str) -> dict[str, Any]:
    req = Request(url, headers=_github_headers())
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:300]
        raise ValueError(f"GitHub API {e.code}: {body}") from e


def _github_download_asset(asset_api_url: str, dest: Path) -> None:
    """Download release asset (private repos need API URL + octet-stream)."""
    headers = _github_headers()
    headers["Accept"] = "application/octet-stream"
    req = Request(asset_api_url, headers=headers)
    with urlopen(req, timeout=180) as resp, open(dest, "wb") as out:
        shutil.copyfileobj(resp, out)


def fetch_github_release(
    repo: str = DEFAULT_GITHUB_REPO,
    tag: str = "latest",
) -> dict[str, Any]:
    """Return release metadata + zip asset URL (cafe24-agent-kit*.zip)."""
    if not repo or "/" not in repo:
        raise ValueError("CAFE24_KIT_GITHUB_REPO must be owner/repo")

    if tag == "latest":
        api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    else:
        api_url = f"https://api.github.com/repos/{repo}/releases/tags/{tag}"

    data = _github_json(api_url)
    assets = data.get("assets") or []
    zip_asset = None
    for asset in assets:
        name = asset.get("name", "")
        if name.startswith("cafe24-agent-kit") and name.endswith(".zip"):
            zip_asset = asset
            break
    if not zip_asset:
        raise ValueError(
            f"No cafe24-agent-kit*.zip asset in release {data.get('tag_name')}"
        )

    return {
        "repo": repo,
        "tag_name": data.get("tag_name"),
        "name": data.get("name"),
        "published_at": data.get("published_at"),
        "html_url": data.get("html_url"),
        "zip_name": zip_asset.get("name"),
        "zip_url": zip_asset.get("browser_download_url"),
        "zip_api_url": zip_asset.get("url"),
        "zip_size": zip_asset.get("size"),
    }


def _extract_kit_zip(zip_path: Path) -> Path:
    """Extract release zip; return kit root (cafe24-agent-kit/)."""
    extract_dir = zip_path.parent / "extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    for candidate in (
        extract_dir / "cafe24-agent-kit",
        extract_dir,
    ):
        if (candidate / "VERSION").is_file() and (candidate / "mcp" / "server.py").is_file():
            return candidate

    for p in extract_dir.rglob("server.py"):
        if p.parent.name == "mcp" and (p.parent.parent / "VERSION").is_file():
            return p.parent.parent

    raise FileNotFoundError(f"Invalid kit zip layout under {extract_dir}")


def kit_update_from_github(
    tag: str = "latest",
    *,
    repo: str = DEFAULT_GITHUB_REPO,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Download GitHub Release zip and apply kit_update (config preserved)."""
    rel = fetch_github_release(repo=repo, tag=tag)
    if dry_run:
        return {
            "dry_run": True,
            "release": rel,
            "would_update_paths": UPDATE_PATHS,
            "preserved": ["mcp/config/*", "agent-kit/clients/{your_mall}/"],
        }

    tmp_zip = Path(tempfile.mkdtemp()) / rel["zip_name"]
    try:
        api_url = rel.get("zip_api_url") or rel.get("zip_url")
        _github_download_asset(api_url, tmp_zip)
        kit_root = _extract_kit_zip(tmp_zip)
        result = kit_update(source=kit_root, dry_run=False)
        result["release"] = {
            "tag_name": rel.get("tag_name"),
            "zip_name": rel.get("zip_name"),
            "html_url": rel.get("html_url"),
        }
        return result
    finally:
        if tmp_zip.parent.exists():
            shutil.rmtree(tmp_zip.parent, ignore_errors=True)


def detect_install_channel() -> str:
    """Best-effort guess of how this kit was installed: git | npm | release.

    Override with env CAFE24_KIT_CHANNEL. A channel-aware updater lets the same
    start-time check serve git clones, GitHub Release zips, and future npm users.
    """
    override = os.environ.get("CAFE24_KIT_CHANNEL", "").strip().lower()
    if override in {"git", "npm", "release"}:
        return override
    if (WORKSPACE_ROOT / ".git").exists():
        return "git"
    if "node_modules" in WORKSPACE_ROOT.parts:
        return "npm"
    return "release"


def _channel_update_command(channel: str) -> str:
    return {
        "git": "git pull --ff-only",
        "npm": "npm update -g cafe24-agent-kit",
        "release": "python cli.py kit-update --from-github",
    }.get(channel, "python cli.py kit-update --from-github")


def _git_is_clean() -> bool:
    """True only if the workspace git tree has no uncommitted changes."""
    try:
        import subprocess

        r = subprocess.run(
            ["git", "-C", str(WORKSPACE_ROOT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=15, check=False,
        )
        return r.returncode == 0 and not r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return False


def _git_pull_ff() -> dict[str, Any]:
    import subprocess

    try:
        r = subprocess.run(
            ["git", "-C", str(WORKSPACE_ROOT), "pull", "--ff-only"],
            capture_output=True, text=True, timeout=120, check=False,
        )
        return {
            "ok": r.returncode == 0,
            "output": (r.stdout + r.stderr).strip()[:500],
        }
    except (OSError, subprocess.SubprocessError) as e:
        return {"ok": False, "output": str(e)}


def _load_autoupdate_cache() -> dict[str, Any]:
    try:
        return json.loads(AUTOUPDATE_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_autoupdate_cache(data: dict[str, Any]) -> None:
    try:
        AUTOUPDATE_CACHE.parent.mkdir(parents=True, exist_ok=True)
        AUTOUPDATE_CACHE.write_text(
            json.dumps(data, ensure_ascii=False), encoding="utf-8"
        )
    except OSError:
        pass


def kit_autoupdate(
    *, apply: bool = False, force: bool = False, throttle_hours: float = 12.0
) -> dict[str, Any]:
    """Start-time update check: compare local vs remote VERSION, channel-aware.

    - Throttled: skips the network call if checked within ``throttle_hours``
      (so running it on every start is cheap). ``force=True`` bypasses it.
    - Offline-safe: a failed remote lookup never raises — startup proceeds.
    - ``apply=True`` performs a *conditional* auto-update: GitHub-Release and
      git (clean tree) channels self-apply; otherwise the command is returned
      for the user to run. config/* and clients/{mall} are always preserved.
    """
    local = read_kit_version()
    channel = detect_install_channel()
    now = datetime.now(timezone.utc)
    cache = _load_autoupdate_cache()

    if not force and cache.get("last_check"):
        try:
            last = datetime.fromisoformat(cache["last_check"])
            if (now - last).total_seconds() < throttle_hours * 3600:
                return {
                    "checked": False,
                    "throttled": True,
                    "channel": channel,
                    "local": local,
                    "throttle_hours": throttle_hours,
                    "cached_remote_version": cache.get("remote_version"),
                }
        except ValueError:
            pass

    remote = fetch_remote_version()
    cache.update(
        {"last_check": now.isoformat(), "remote_version": remote.get("version")}
    )
    _save_autoupdate_cache(cache)

    if not remote.get("available"):
        return {
            "checked": True,
            "channel": channel,
            "local": local,
            "remote": remote,
            "update_available": False,
            "note": "원격 버전 확인 실패(오프라인일 수 있음) — 무시하고 진행",
        }

    update_available = bool(
        local.get("version")
        and remote.get("version")
        and remote["version"] != local["version"]
    )
    result: dict[str, Any] = {
        "checked": True,
        "channel": channel,
        "local": local,
        "remote": remote,
        "update_available": update_available,
        "recommended_command": _channel_update_command(channel),
    }
    if not update_available or not apply:
        return result

    # Conditional auto-apply (best-effort; never crashes startup)
    if channel == "release":
        try:
            result["applied"] = kit_update_from_github(tag="latest", dry_run=False)
            result["apply_status"] = "updated"
        except (
            URLError, HTTPError, OSError, TimeoutError, ValueError,
            zipfile.BadZipFile, FileNotFoundError,
        ) as e:
            result["apply_status"] = "failed"
            result["apply_error"] = str(e)
    elif channel == "git":
        if _git_is_clean():
            pull = _git_pull_ff()
            result["applied"] = pull
            result["apply_status"] = "updated" if pull["ok"] else "failed"
        else:
            result["apply_status"] = "manual"
            result["note"] = "로컬 변경이 있어 자동 pull 보류 — 직접 git pull 하세요"
    else:  # npm
        result["apply_status"] = "manual"
        result["note"] = "npm 채널은 수동 업데이트 명령을 실행하세요"
    return result


def _safe_mall_id(mall_id: str) -> str:
    mid = mall_id.strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{2,31}", mid):
        raise ValueError(
            "몰 ID는 영소문자·숫자·_- 만 3~32자 (예: myshop001)"
        )
    return mid


def scaffold_client(mall_id: str, *, overwrite: bool = False) -> dict[str, Any]:
    """Copy clients/_template → clients/{mall_id}; hint config copy."""
    mid = _safe_mall_id(mall_id)
    if not TEMPLATE_CLIENT.is_dir():
        raise FileNotFoundError(f"Template missing: {TEMPLATE_CLIENT}")

    dest = KIT_ROOT / "clients" / mid
    if dest.exists() and not overwrite:
        raise FileExistsError(
            f"Already exists: {dest} (use overwrite=True to replace scaffold only)"
        )

    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(
        TEMPLATE_CLIENT,
        dest,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )

    # Replace placeholders in key files
    today = date.today().isoformat()
    claude = dest / "CLAUDE.md"
    if claude.is_file():
        text = claude.read_text(encoding="utf-8")
        text = text.replace("{클라이언트명}", mid)
        text = text.replace("{프로젝트명}", f"{mid} 카페24 작업")
        text = text.replace("{이름/회사명}", mid)
        text = text.replace("{YYYY-MM-DD}", today)
        text = text.replace(
            "{https://...cafe24.com/skin-skinN}",
            f"https://{mid}.cafe24.com/",
        )
        text = text.replace("{/skinN}", "(미확정 — themes API 후 갱신)")
        claude.write_text(text, encoding="utf-8")

    wf_example = dest / ".workflow.md.example"
    wf = dest / ".workflow.md"
    if wf_example.is_file():
        wf_text = wf_example.read_text(encoding="utf-8")
        wf_text = wf_text.replace("musatax", mid)
        wf.write_text(wf_text, encoding="utf-8")

    initial = dest / "01_요청사항" / "initial.md"
    if initial.is_file():
        init_text = initial.read_text(encoding="utf-8")
        if "요청 원문" in init_text and mid not in init_text:
            init_text += f"\n\n## 몰 ID\n- `{mid}` — scaffold {today}\n"
        initial.write_text(init_text, encoding="utf-8")

    config_example = CONFIG_DIR / "cafe24_config.example.py"
    config_dest = CONFIG_DIR / f"cafe24_config_{mid}.py"
    config_created = False
    if config_example.is_file() and not config_dest.exists():
        cfg = config_example.read_text(encoding="utf-8")
        cfg = cfg.replace("your_mall_id", mid)
        config_dest.write_text(cfg, encoding="utf-8")
        config_created = True

    return {
        "mall_id": mid,
        "client_dir": str(dest),
        "workflow_file": str(wf) if wf.is_file() else None,
        "config_file": str(config_dest) if config_dest.exists() else None,
        "config_created": config_created,
        "next_commands": ["/MCP연결", "/API발급", "/접속세팅"],
        "hint": "cafe24_config_{mall}.py 에 CLIENT_ID/SECRET 입력 후 /API발급",
    }


def diagnose_kit_setup() -> dict[str, Any]:
    """Structured setup diagnostic for dist recipients."""
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str = "", **extra):
        checks.append({"name": name, "ok": ok, "detail": detail, **extra})

    ver = read_kit_version()
    add("kit_version", ver["version"] != "unknown", ver.get("version", ""))

    for pkg in ("auth", "backends"):
        p = MCP_DIR / pkg
        add(f"mcp_{pkg}", p.is_dir() and (p / "__init__.py").is_file(), str(p))

    add("config_init", (CONFIG_DIR / "__init__.py").is_file(), str(CONFIG_DIR))

    example_cfg = CONFIG_DIR / "cafe24_config.example.py"
    add("config_example", example_cfg.is_file(), str(example_cfg))

    mall_configs = sorted(
        p.name for p in CONFIG_DIR.glob("cafe24_config_*.py")
        if p.name != "cafe24_config.example.py"
    )
    add(
        "mall_config",
        len(mall_configs) > 0,
        f"{len(mall_configs)} file(s)",
        malls=mall_configs,
    )

    tokens = sorted(CONFIG_DIR.glob("*.token.json"))
    add("oauth_token", len(tokens) > 0, f"{len(tokens)} token(s)")

    sftp_jsons = sorted(CONFIG_DIR.glob("sftp_*.json"))
    add("sftp_config", len(sftp_jsons) > 0, f"{len(sftp_jsons)} file(s)")

    mcp_json = WORKSPACE_ROOT / ".cursor" / "mcp.json"
    mcp_example = WORKSPACE_ROOT / ".cursor" / "mcp.json.example"
    add(
        "cursor_mcp_json",
        mcp_json.is_file(),
        str(mcp_json) if mcp_json.is_file() else f"copy from {mcp_example}",
    )

    try:
        import server  # noqa: F401

        add("import_server", True, "python -c 'import server' OK")
    except Exception as e:
        add("import_server", False, str(e))

    # Expected smoke without credentials
    expected_smoke = "5/9" if not tokens else "9/9+ with SMOKE_PREFLIGHT_ALL=1"
    all_core = all(
        c["ok"]
        for c in checks
        if c["name"] in ("mcp_auth", "mcp_backends", "config_init", "import_server")
    )

    return {
        "kit_version": ver,
        "checks": checks,
        "core_ready": all_core,
        "expected_smoke_without_credentials": expected_smoke,
        "onboarding_commands": ONBOARDING_COMMANDS,
        "changelog_path": str(CHANGELOG_FILE) if CHANGELOG_FILE.is_file() else None,
        "next_steps": _next_steps(checks, tokens),
    }


def _next_steps(checks: list[dict], tokens: list[Path]) -> list[str]:
    steps: list[str] = []
    by_name = {c["name"]: c for c in checks}
    if not by_name.get("import_server", {}).get("ok"):
        steps.append("cd mcp && pip install -r requirements.txt")
    if not by_name.get("cursor_mcp_json", {}).get("ok"):
        steps.append("Copy .cursor/mcp.json.example → .cursor/mcp.json")
    if not by_name.get("mall_config", {}).get("ok"):
        steps.append("/새클라이언트 또는 cafe24_config.example.py 복사")
    if not tokens:
        steps.append("/API발급 — OAuth 토큰 발급")
    if not steps:
        steps.append("MCP get_kit_guides · run_preflight(check='header')")
    return steps


# Paths updated by kit-update (never touch user secrets or client trees)
UPDATE_PATHS = [
    ".claude",
    "agent-kit/commands",
    "agent-kit/00_시작하기",
    "agent-kit/01_작업하기",
    "agent-kit/02_막혔을때",
    "agent-kit/brain",
    "agent-kit/connect",
    "agent-kit/CLAUDE.md",
    "agent-kit/README.md",
    "mcp/auth",
    "mcp/backends",
    "mcp/work/scripts/strip_ez.py",
    "mcp/server.py",
    "mcp/cli.py",
    "mcp/smoke_test.py",
    "mcp/kit_tools.py",
    "mcp/requirements.txt",
    "mcp/README.md",
    "work/scripts",
    ".cursor/mcp.json.example",
    "README.md",
    "AGENTS.md",
    "VERSION",
    "CHANGELOG.md",
]


def kit_update(source: Path | None = None, dry_run: bool = False) -> dict[str, Any]:
    """Copy kit code from source tree; preserve mcp/config and clients/."""
    src_env = os.environ.get("CAFE24_KIT_UPDATE_SOURCE", "").strip()
    src_root = source or (Path(src_env).expanduser() if src_env else None)
    if not src_root or not src_root.is_dir():
        raise FileNotFoundError(
            "Set CAFE24_KIT_UPDATE_SOURCE to a newer kit root (or pass source=)"
        )
    if src_root.resolve() == WORKSPACE_ROOT.resolve():
        raise ValueError(
            "kit_update source cannot be the workspace root (self-update)"
        )

    updated: list[str] = []
    skipped: list[str] = []

    for rel in UPDATE_PATHS:
        s = src_root / rel
        d = WORKSPACE_ROOT / rel
        if not s.exists():
            skipped.append(f"missing at source: {rel}")
            continue
        if dry_run:
            updated.append(rel)
            continue
        if s.is_dir():
            if d.exists():
                shutil.rmtree(d)
            shutil.copytree(
                s,
                d,
                ignore=shutil.ignore_patterns(
                    "__pycache__", "*.pyc", ".git", "nookitokki002"
                ),
            )
        else:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
        updated.append(rel)

    # agent-kit/clients: only refresh _template + _verified-template + reference workflows
    for rel in (
        "agent-kit/clients/_template",
        "agent-kit/clients/_verified-template",
        "agent-kit/clients/demo000/.workflow.md",
        "agent-kit/clients/ecudemo400786/.workflow.md",
    ):
        s = src_root / rel
        d = WORKSPACE_ROOT / rel
        if not s.exists():
            continue
        if dry_run:
            updated.append(rel)
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.is_dir():
            if d.exists():
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
        updated.append(rel)

    return {
        "source": str(src_root),
        "target": str(WORKSPACE_ROOT),
        "dry_run": dry_run,
        "updated": updated,
        "skipped": skipped,
        "preserved": ["mcp/config/*", "agent-kit/clients/{your_mall}/"],
    }
