"""
몰별 설정 로더.

- 몰마다 cafe24_config_{mall_id}.py 파일을 이 폴더에 두면 자동으로 읽는다.
- 배포본: `cafe24_config.example.py` 복사 후 편집.
- 모노레po 전용: api-poc/ 경로 fallback (개발 트리에만 존재할 수 있음).
"""
import importlib.util
import os

# 이 파일(config/__init__.py)이 있는 폴더의 절대 경로
HERE = os.path.dirname(os.path.abspath(__file__))
# mcp/ 폴더의 부모 = web/cafe24/
CAFE24_ROOT = os.path.dirname(os.path.dirname(HERE))
# 기존 PoC 설정 파일 위치 (demo000 용)
POC_CONFIG = os.path.join(CAFE24_ROOT, "api-poc", "cafe24_config.py")
# 모노레po(cafe24-agent-workspace)만 clone 한 경우 OneDrive 개발 트리 fallback
ONEDRIVE_POC_CONFIG = os.path.join(
    os.path.expanduser("~"),
    "OneDrive", "문서", "개발", "web", "cafe24", "api-poc", "cafe24_config.py",
)


def _load_py(path: str):
    """파이썬 파일 하나를 모듈로 읽어서 돌려주는 도우미."""
    spec = importlib.util.spec_from_file_location("cafe24_mall_config", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_mall_config(mall_id: str = "demo000"):
    """몰 아이디를 받아 해당 몰의 설정 모듈을 돌려준다.

    찾는 순서:
      1) mcp/config/cafe24_config_{mall_id}.py
      2) {CAFE24_ROOT}/api-poc/cafe24_config.py
      3) OneDrive 개발 트리 api-poc (모노레po 단독 시)
    """
    per_mall = os.path.join(HERE, f"cafe24_config_{mall_id}.py")
    if os.path.exists(per_mall):
        return _load_py(per_mall)

    if os.path.exists(POC_CONFIG):
        cfg = _load_py(POC_CONFIG)
        if getattr(cfg, "MALL_ID", "") == mall_id:
            return cfg

    onedrive_poc = ONEDRIVE_POC_CONFIG
    if os.path.exists(onedrive_poc):
        cfg = _load_py(onedrive_poc)
        if getattr(cfg, "MALL_ID", "") == mall_id:
            return cfg

    raise FileNotFoundError(
        f"몰 '{mall_id}' 설정을 찾을 수 없습니다. "
        f"mcp/config/cafe24_config_{mall_id}.py 를 만들어 주세요. "
        f"(서식: mcp/config/cafe24_config.example.py)"
    )


def token_file_path(mall_id: str) -> str:
    """몰별 토큰 저장 파일 경로 (git 제외 대상)."""
    return os.path.join(HERE, f"{mall_id}.token.json")


# ── SFTP 설정 ──────────────────────────────────────────────

import json  # noqa: E402

# demo000 SFTP 접속정보가 이미 들어있는 기존 파일 (VS Code SFTP 확장용)
_KNOWN_SFTP_SOURCES = {
    "demo000": os.path.join(
        CAFE24_ROOT, "clients", "template-02", ".vscode", "sftp.json"
    ),
}

# demo000 쓰기 허용 슬롯 (2026-06-10 재개설 후 대표님 확정)
# /skin14=_nk 신규 템플릿, /mobile=모바일 스킨. /skin2(IDIO원본)·/skin15(베이직)·/base 보호
_DEFAULT_WRITE_ALLOWED = {
    "demo000": ["/skin14", "/mobile"],
}


def sftp_config_path(mall_id: str) -> str:
    """몰별 SFTP 설정 파일 경로 (git 제외 대상)."""
    return os.path.join(HERE, f"sftp_{mall_id}.json")


def load_sftp_config(mall_id: str = "demo000") -> dict:
    """몰의 SFTP 접속정보를 돌려준다.

    형식: {host, port, username, password, write_allowed: [...]}
    - write_allowed: 업로드(쓰기)가 허용되는 원격 최상위 폴더 목록.
      여기 없는 경로로의 업로드는 무조건 거부된다.

    찾는 순서:
      1) mcp/config/sftp_{mall_id}.json  (전용 설정)
      2) 알려진 기존 위치(예: template-02/.vscode/sftp.json)에서 자동 이전
    """
    path = sftp_config_path(mall_id)
    if not os.path.exists(path):
        _migrate_sftp_config(mall_id, path)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"몰 '{mall_id}' SFTP 설정이 없습니다. {path} 를 만들어 주세요. "
            '(형식: {"host","port","username","password","write_allowed"})'
        )
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    # write_allowed 가 없으면 빈 목록 = 모든 쓰기 거부 (안전 기본값)
    cfg.setdefault("write_allowed", [])
    return cfg


def _migrate_sftp_config(mall_id: str, dest: str):
    """기존 VS Code sftp.json 에서 접속정보만 뽑아 전용 설정으로 이전."""
    src = _KNOWN_SFTP_SOURCES.get(mall_id)
    if not src or not os.path.exists(src):
        return
    try:
        with open(src, encoding="utf-8") as f:
            old = json.load(f)
    except (OSError, json.JSONDecodeError):
        return
    cfg = {
        "host": old["host"],
        "port": int(old.get("port", 22)),
        "username": old["username"],
        "password": old["password"],
        "write_allowed": _DEFAULT_WRITE_ALLOWED.get(mall_id, []),
    }
    tmp = dest + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.replace(tmp, dest)
