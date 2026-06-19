#!/usr/bin/env python3
"""
카페24 스마트디자인 MCP 서버 — 설계서 §4 도구 8종 (stdio)

에이전트(클로드)가 카페24 몰에 직접 손을 뻗는 "손발".
  - API 백엔드  : 디자인 목록·정본 읽기·인증 진단 (읽기 전용)
  - SFTP 백엔드 : 파일트리·읽기·다운로드·백업·업로드★

실행:  python server.py          (stdio — .mcp.json 에서 이 명령으로 등록)
검증:  python smoke_test.py      (도구 목록 + 실제 호출 왕복 확인)

안전 구조:
  - 업로드는 write_allowed 화이트리스트(config/sftp_{mall}.json) 밖이면 무조건 거부
  - 업로드 전 원본 자동 백업 (mcp/backups/)
  - 에이전트는 업로드 호출 전 반드시 사용자 확인 (누끼토끼 절대룰)
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Annotated, Optional
from urllib.request import urlopen

from pydantic import Field

from mcp.server.fastmcp import FastMCP

from auth.oauth import AuthError, TokenManager
from backends.cafe24_api import Cafe24API, Cafe24ApiError
from backends.cafe24_ftp import open_remote
from backends.cafe24_sftp import SftpWriteDenied

from kit_tools import (
    ONBOARDING_COMMANDS,
    diagnose_kit_setup,
    read_kit_version,
    scaffold_client,
)

mcp = FastMCP("cafe24_mcp")

# 자주 쓰는 파라미터 타입 (몰 아이디 — 기본 demo000)
MallId = Annotated[str, Field(description="카페24 몰 아이디 (기본: demo000)")]


def _err(e: Exception) -> str:
    """모든 도구가 같은 형식으로 오류를 알려준다 (에이전트가 다음 행동을 알 수 있게)."""
    if isinstance(e, AuthError):
        return f"Error(인증): {e}"
    if isinstance(e, Cafe24ApiError):
        msg = str(e)
        if "422" in msg:
            return (
                f"Error(API): {msg}\n"
                "힌트: API pages 는 HTML 페이지만 읽을 수 있습니다. "
                "CSS/JS/이미지 등 에셋은 cafe24_sftp_read 를 사용하세요."
            )
        return f"Error(API): {msg}"
    if isinstance(e, SftpWriteDenied):
        return f"Error(쓰기보호): {e}"
    if isinstance(e, FileNotFoundError):
        return f"Error(없음): {e}"
    return f"Error({type(e).__name__}): {e}"


def _json(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


KIT_ROOT = Path(
    os.environ.get(
        "CAFE24_KIT_ROOT",
        Path(__file__).resolve().parent.parent / "agent-kit",
    )
)

WORKFLOWS = [
    ("01-quick-fix", 3),
    ("02-skin-build-standard", 6),
    ("03-reference-renewal", 8),
    ("04-measure-first", None),
    ("05-reference-intake", 5),
    ("06-verify-loop", None),
    ("07-ez-on-legacy-setup", None),
    ("08-ez-three-step-pingpong", 3),
]

F_QUICK = ["F27", "F28", "F33", "F34", "F35", "F36"]

WORK_ROOT = Path(
    os.environ.get(
        "CAFE24_WORK_ROOT",
        Path(__file__).resolve().parent.parent / "work",
    )
)
SCRIPTS_DIR = WORK_ROOT / "scripts"

# check name → score script (ecudemo393674→400786 하드코딩 스크립트)
PREFLIGHT_CHECKS: dict[str, str] = {
    "header": "ref393674-score-header.py",
    "mobile_full": "ref393674-score-mobile-full.py",
    "plp": "ref393674-score-plp.py",
    "pdp": "ref393674-score-pdp.py",
    "basket": "ref393674-score-basket.py",
    "member": "ref393674-score-member.py",
    "board": "ref393674-score-board.py",
    "page": "ref393674-score-page.py",
    "paginate": "ref393674-score-paginate.py",
}

PILOT_MALL = "ecudemo400786"

MCP_CONFIG_DIR = Path(__file__).resolve().parent / "config"
OAUTH_GUIDE = "connect/MCP-OAUTH-GUIDE.md"
OAUTH_BEGINNER = "connect/OAUTH-BEGINNER-5MIN.md"


def _malls_missing_token() -> list[str]:
    """cafe24_config_*.py 가 있는 몰 중 .token.json 이 없는 ID 목록."""
    missing: list[str] = []
    for cfg in sorted(MCP_CONFIG_DIR.glob("cafe24_config_*.py")):
        mall_id = cfg.stem.removeprefix("cafe24_config_")
        if TokenManager(mall_id).status().get("token") == "없음":
            missing.append(mall_id)
    return missing


# ════════════════════════════════════════════════════════════
# agent-kit 부트스트랩 — HYBRID-ARCHITECTURE-DRAFT Phase 1
# ════════════════════════════════════════════════════════════

@mcp.tool(
    name="get_kit_guides",
    annotations={
        "title": "카페24 agent-kit 가이드",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def get_kit_guides(
    workflow_id: Annotated[
        Optional[str],
        Field(
            description="선택: 01-quick-fix, 06-verify-loop 등. 생략 시 README+전체 목록."
        ),
    ] = None,
    symptom_f_code: Annotated[
        Optional[str],
        Field(
            description="선택: F27, F28 등 증상 코드 — F-index에서 관련 문서만 필터."
        ),
    ] = None,
) -> str:
    """카페24 agent-kit 워크플로우·F-index·다음에 읽을 문서 경로를 반환합니다.

    작업 시작 시 가장 먼저 호출하세요. CAFE24_KIT_ROOT 미설정 시
    server.py 기준 ../agent-kit 경로를 사용합니다.
    """
    if not KIT_ROOT.is_dir():
        return _json(
            {
                "error": "CAFE24_KIT_ROOT not found",
                "hint": "set CAFE24_KIT_ROOT env or clone agent-kit",
                "attempted": str(KIT_ROOT),
            }
        )

    out = {
        "kit_root": str(KIT_ROOT),
        "kit_version": read_kit_version(),
        "changelog_path": str(
            KIT_ROOT.parent / "CHANGELOG.md"
            if (KIT_ROOT.parent / "CHANGELOG.md").is_file()
            else KIT_ROOT / "CHANGELOG.md"
        ),
        "onboarding_commands": ONBOARDING_COMMANDS,
        "mcp_registration_guide": str(
            KIT_ROOT / "00_시작하기/05b-MCP-등록.md"
        ),
        "constitution": str(KIT_ROOT / "CLAUDE.md"),
        "f_index": str(KIT_ROOT / "02_막혔을때/F-상황-인덱스.md"),
        "workflows_readme": str(KIT_ROOT / "01_작업하기/workflows/README.md"),
        "workflows": [
            {
                "id": wid,
                "path": str(KIT_ROOT / "01_작업하기/workflows" / f"{wid}.md"),
                "steps": steps,
            }
            for wid, steps in WORKFLOWS
        ],
        "f_quick": F_QUICK,
        "slash_command": str(
            KIT_ROOT / ".claude/commands/카페24-워크플로우.md"
        ),
        "next_read": [
            str(KIT_ROOT / "01_작업하기/workflows/08-ez-three-step-pingpong.md"),
            str(KIT_ROOT / "01_작업하기/workflows/07-ez-on-legacy-setup.md"),
            str(KIT_ROOT / "02_막혔을때/F-상황-인덱스.md"),
        ],
        "next_read_hint": "실행: 08-ez-three-step-pingpong · 배경·판정·0-C/0-D: 07-ez-on-legacy-setup",
        "oauth_onboarding": [
            str(KIT_ROOT / OAUTH_BEGINNER),
            str(KIT_ROOT / "00_시작하기/05-MCP-연결-개요.md"),
            str(KIT_ROOT / OAUTH_GUIDE),
        ],
    }

    if workflow_id:
        p = KIT_ROOT / "01_작업하기/workflows" / f"{workflow_id}.md"
        out["focused_workflow"] = str(p) if p.exists() else None
        if out["focused_workflow"]:
            out["next_read"] = [out["focused_workflow"], out["f_index"]]

    if symptom_f_code:
        code = symptom_f_code.strip().upper()
        if not code.startswith("F"):
            code = f"F{code}"
        out["f_code_hint"] = (
            f"Read F-index section {code} in 02_막혔을때/F-상황-인덱스.md"
        )
        pitfalls = KIT_ROOT / "02_막혔을때/common-pitfalls.md"
        out["f_code_docs"] = {
            "f_index": out["f_index"],
            "common_pitfalls": str(pitfalls),
            "brain": str(KIT_ROOT / "brain/docs/CAFE24-SMARTDESIGN-AGENT.md"),
        }

    missing_tokens = _malls_missing_token()
    if missing_tokens:
        oauth_docs = [
            str(KIT_ROOT / OAUTH_BEGINNER),
            str(KIT_ROOT / OAUTH_GUIDE),
        ]
        out["oauth_needed"] = {
            "malls_without_token": missing_tokens,
            "hint": "python cli.py auth-url --mall {몰ID} → 브라우저 허용 → code 교환",
        }
        out["next_read"] = oauth_docs + out["next_read"]
        out["next_read_hint"] = (
            f"OAuth 미완료 ({', '.join(missing_tokens)}) — "
            f"{OAUTH_BEGINNER} 먼저 · 그다음 {out['next_read_hint']}"
        )

    return _json(out)


@mcp.tool(
    name="diagnose_kit_setup",
    annotations={
        "title": "키트 설치 진단",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def diagnose_kit_setup_tool() -> str:
    """pip·import server·MCP JSON·config·토큰·smoke 기대치(5/9)를 구조화해 반환합니다."""
    try:
        return _json(diagnose_kit_setup())
    except Exception as e:
        return _json({"error": str(e)})


@mcp.tool(
    name="scaffold_client",
    annotations={
        "title": "새 클라이언트 폴더 생성",
        "readOnlyHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
def scaffold_client_tool(
    mall_id: MallId,
    overwrite: Annotated[
        bool,
        Field(description="True면 기존 clients/{mall_id} scaffold만 덮어씀"),
    ] = False,
) -> str:
    """clients/_template → clients/{mall_id} 복사 및 cafe24_config_{mall} 힌트 생성."""
    try:
        return _json(scaffold_client(mall_id, overwrite=overwrite))
    except (ValueError, FileNotFoundError, FileExistsError) as e:
        return _json({"error": str(e)})
    except Exception as e:
        return _err(e)


def _parse_score_stdout(stdout: str) -> dict:
    """Score script stdout → dict. trailing non-JSON tolerated."""
    text = stdout.strip()
    if not text:
        return {"error": "empty stdout", "total_score": 0, "pass": False}
    decoder = json.JSONDecoder()
    try:
        obj, _ = decoder.raw_decode(text)
        return obj
    except json.JSONDecodeError:
        start = text.find("{")
        if start < 0:
            return {"error": "no JSON in stdout", "raw": text[:500]}
        obj, _ = decoder.raw_decode(text[start:])
        return obj


def _extract_fails(data: dict, limit: int = 5) -> list[dict]:
    """Flatten FAIL checks from score script JSON (single or multi-report)."""
    fails: list[dict] = []

    def collect(checks: list):
        for c in checks:
            if c.get("pts", 0) < c.get("max_pts", 1):
                fails.append(
                    {
                        "id": c.get("id"),
                        "label": c.get("label"),
                        "pts": c.get("pts"),
                        "max_pts": c.get("max_pts"),
                        "note": c.get("note", ""),
                    }
                )

    if "checks" in data:
        collect(data["checks"])
    for report in data.get("reports", []):
        collect(report.get("checks", []))
    return fails[:limit]


def _score_from_data(data: dict) -> int | None:
    score = data.get("total_score")
    if score is not None:
        return score
    if "reports" in data:
        scores = [r.get("score", 0) for r in data["reports"]]
        maxes = [r.get("max", 100) for r in data["reports"]]
        if sum(maxes):
            return round(sum(scores) / sum(maxes) * 100)
    return None


F34_MOBILE_WEB_MESSAGE = (
    "CAFE24.MOBILE_WEB=true — MCP cannot change admin settings (F34). "
    "Ask user to set 쇼핑몰 설정 → 사이트 설정 → 쇼핑몰 환경 설정 → 모바일 탭 → "
    "「모바일 전용 디자인 사용설정」→「사용안함」, then re-verify "
    "CAFE24.MOBILE_WEB=false in page source."
)


def _derive_f_codes(check: str, data: dict, fails: list[dict], pass_ok: bool) -> list[str]:
    """Map score failures to F-index codes for agent guidance."""
    if pass_ok:
        return []

    f_codes: list[str] = []
    if check == "mobile_full":
        fail_ids = {f.get("id") for f in fails}
        mobile_web = data.get("mobile_web") or {}
        mw_failed = (
            "MW1" in fail_ids
            or mobile_web.get("main") is True
            or any(
                "MOBILE_WEB" in (f.get("label") or "")
                or "MOBILE_WEB" in (f.get("note") or "")
                for f in fails
            )
        )
        if mw_failed:
            f_codes.append("F34")
        if "C1" in fail_ids:
            f_codes.append("F27")
    return f_codes


def _mall_id_metadata(mall_id: str) -> dict:
    """Document mall_id passed to score scripts via CLI/env."""
    return {
        "mall_id": mall_id,
        "pilot_mall": PILOT_MALL,
        "mall_id_applied_to_scripts": True,
        "mall_id_note": (
            f"Score scripts target {mall_id}.cafe24.com via --mall-id / CAFE24_MALL_ID; "
            "reference defaults to ecudemo393674 (CAFE24_REF_MALL / --ref-mall)."
        ),
    }


def _run_score_script(
    script: Path,
    mall_id: str,
    timeout: int = 180,
) -> tuple[subprocess.CompletedProcess[str] | None, dict | None, str | None]:
    """Run one score script; return (proc, parsed_json, error_message)."""
    env = {**os.environ, "CAFE24_MALL_ID": mall_id, "CAFE24_TGT_MALL": mall_id}
    cmd = [sys.executable, str(script), "--mall-id", mall_id]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=str(SCRIPTS_DIR),
            env=env,
        )
    except subprocess.TimeoutExpired:
        return None, None, f"score script timeout ({timeout}s)"
    except Exception as e:
        return None, None, str(e)

    data = _parse_score_stdout(proc.stdout or "")
    if "error" in data and proc.returncode != 0 and not proc.stdout:
        return proc, data, data.get("error", "script failed")
    return proc, data, None


def _build_check_result(
    check: str,
    mall_id: str,
    script: Path,
    proc: subprocess.CompletedProcess[str],
    data: dict,
) -> dict:
    score = _score_from_data(data)
    pass_ok = score == 100 if score is not None else bool(data.get("pass"))
    fails = _extract_fails(data)
    f_codes = _derive_f_codes(check, data, fails, pass_ok)

    out: dict = {
        "check": check,
        "script": str(script),
        "total_score": score,
        "pass": pass_ok,
        "exit_code": proc.returncode,
        "fails": fails,
        "f_codes": f_codes,
    }
    if f_codes:
        out["f_code_hint"] = "Read F-index for " + ", ".join(f_codes)
    if check == "mobile_full" and "F34" in f_codes:
        out["f34_message"] = F34_MOBILE_WEB_MESSAGE
    if proc.returncode != 0 and not pass_ok:
        out["stderr_tail"] = (proc.stderr or "")[-300:]
    if check == "mobile_full" and "mobile_web" in data:
        out["mobile_web"] = data["mobile_web"]
    return out


def _run_single_preflight(
    check: str,
    mall_id: str,
    script_path: Optional[str] = None,
) -> dict:
    """Run one preflight check; return result dict (not JSON string)."""
    script_name = PREFLIGHT_CHECKS.get(check)
    if not script_name and not script_path:
        return {
            "error": f"unknown check: {check}",
            "valid_checks": sorted(PREFLIGHT_CHECKS) + ["all"],
            "check": check,
        }

    script = Path(script_path) if script_path else SCRIPTS_DIR / script_name
    if not script.is_file():
        return {
            "error": "score script not found",
            "script": str(script),
            "check": check,
            "hint": "install playwright: pip install playwright && playwright install chromium",
        }

    proc, data, run_err = _run_score_script(script, mall_id)
    if run_err or proc is None or data is None:
        out = {
            "error": run_err or "script failed",
            "check": check,
            **_mall_id_metadata(mall_id),
        }
        if proc is not None:
            out["stderr"] = (proc.stderr or "")[:500]
        out["total_score"] = 0
        out["pass"] = False
        out["fails"] = []
        out["f_codes"] = []
        return out

    return {**_mall_id_metadata(mall_id), **_build_check_result(check, mall_id, script, proc, data)}


@mcp.tool(
    name="run_preflight",
    annotations={
        "title": "카페24 verify-loop preflight (score 스크립트)",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def run_preflight(
    check: Annotated[
        str,
        Field(
            description=(
                "채점 종류: header, mobile_full, plp, pdp, basket, member, "
                "board, page, paginate, all (9종 일괄)"
            )
        ),
    ] = "header",
    mall_id: Annotated[
        str,
        Field(description="대상 몰 ID (--mall-id / CAFE24_MALL_ID, 기본 ecudemo400786)"),
    ] = PILOT_MALL,
    script_path: Annotated[
        Optional[str],
        Field(description="선택: score 스크립트 절대경로 오버라이드"),
    ] = None,
) -> str:
    """verify-loop Phase 0/0.5용 — work/scripts/ref*-score-*.py 를 subprocess로 실행.

    check=all 이면 9종을 순차 실행하고 total_passed·checks별 점수를 집계합니다.
    반환: total_score, pass (100만 true), fails, f_codes. mobile_full MOBILE_WEB 실패 시 F34 안내.
    """
    valid_checks = sorted(PREFLIGHT_CHECKS) + ["all"]

    if check == "all":
        if script_path:
            return _json(
                {
                    "error": "script_path override not supported for check=all",
                    "valid_checks": valid_checks,
                }
            )

        checks_out: dict[str, dict] = {}
        errors: list[dict] = []
        all_f_codes: list[str] = []
        total_passed = 0

        for chk in PREFLIGHT_CHECKS:
            one = _run_single_preflight(chk, mall_id)
            if "error" in one and one.get("total_score") is None:
                errors.append({"check": chk, "error": one["error"]})
                checks_out[chk] = {
                    "total_score": 0,
                    "pass": False,
                    "fails": [],
                    "f_codes": [],
                    "error": one["error"],
                }
                continue

            checks_out[chk] = {
                "total_score": one.get("total_score"),
                "pass": one.get("pass"),
                "fails": one.get("fails", []),
                "f_codes": one.get("f_codes", []),
                "exit_code": one.get("exit_code"),
            }
            if one.get("f34_message"):
                checks_out[chk]["f34_message"] = one["f34_message"]
            if one.get("mobile_web"):
                checks_out[chk]["mobile_web"] = one["mobile_web"]
            for code in one.get("f_codes", []):
                if code not in all_f_codes:
                    all_f_codes.append(code)
            if one.get("pass"):
                total_passed += 1

        total_checks = len(PREFLIGHT_CHECKS)
        batch_out = {
            "check": "all",
            **_mall_id_metadata(mall_id),
            "total_checks": total_checks,
            "total_passed": total_passed,
            "pass": total_passed == total_checks,
            "checks": checks_out,
            "f_codes": all_f_codes,
        }
        if all_f_codes:
            batch_out["f_code_hint"] = "Read F-index for " + ", ".join(all_f_codes)
        if "F34" in all_f_codes:
            batch_out["f34_message"] = F34_MOBILE_WEB_MESSAGE
        if errors:
            batch_out["errors"] = errors
        return _json(batch_out)

    out = _run_single_preflight(check, mall_id, script_path)
    if "valid_checks" not in out and "error" in out:
        out["valid_checks"] = valid_checks
    return _json(out)


# ════════════════════════════════════════════════════════════
# API 백엔드 (읽기·메타) — 설계서 §4-1
# ════════════════════════════════════════════════════════════

@mcp.tool(
    name="cafe24_list_themes",
    annotations={
        "title": "카페24 디자인(스킨) 목록",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def cafe24_list_themes(mall_id: MallId = "demo000") -> str:
    """카페24 몰의 디자인(스킨) 목록과 메타데이터를 조회한다.

    반환 필드:
      - skin_no: API 호출(cafe24_read_page)에 쓰는 번호
      - skin_code: SFTP 폴더명과 같다고 알려진 실무 규칙 (예: 'skin14' → /skin14) ⚠️ OFFICIAL-AUDIT §E-2a
      - editor_type: 'H'=HTML 스마트디자인 ✅ / 'E'=Easy ✅ / D,W,C 도 존재 — HTML SFTP 연결은 공식 미확인
      - skin_name / usage_type

    skin_code 로 API(skin_no)와 SFTP 경로를 연결. 작업 시작 시 항상 이 도구로 확정.
    """
    try:
        return _json(Cafe24API(mall_id).list_themes())
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="cafe24_read_page",
    annotations={
        "title": "카페24 스킨 페이지 정본 읽기 (API)",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def cafe24_read_page(
    skin_no: Annotated[int, Field(description="cafe24_list_themes 가 알려주는 스킨 번호", ge=1)],
    path: Annotated[str, Field(description="스킨 루트 기준 경로 (예: /layout/basic/layout.html)")],
    mall_id: MallId = "demo000",
) -> str:
    """스킨의 HTML 페이지 1건을 카페24 보관 정본으로 읽는다 (Admin API).

    주의:
      - HTML 페이지만 읽힌다. CSS/JS/이미지 등 에셋은 422 오류
        → 에셋은 cafe24_sftp_read 사용.
      - API 호출 제한(40건)이 있어 대량 읽기엔 cafe24_sftp_download 가 낫다.

    반환: {"path", "source", ...} JSON. source 가 파일 전체 소스.
    """
    try:
        return _json(Cafe24API(mall_id).read_page(skin_no, path))
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="cafe24_auth_status",
    annotations={
        "title": "카페24 API 토큰 상태 진단",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def cafe24_auth_status(mall_id: MallId = "demo000") -> str:
    """OAuth 토큰의 유효시간·scope 를 진단한다 (비밀값 미포함).

    access_token(2시간)은 만료 시 자동 갱신되므로 보통 신경 쓸 필요 없다.
    refresh_token(2주)까지 만료된 경우에만 사용자 재동의가 필요하다
    (web/cafe24/mcp/ 에서 `python cli.py auth-url` 안내).
    """
    try:
        return _json(Cafe24API(mall_id).auth_status())
    except Exception as e:
        return _err(e)


# ════════════════════════════════════════════════════════════
# SFTP 백엔드 (탐색·대량·쓰기) — 설계서 §4-2
# ════════════════════════════════════════════════════════════

@mcp.tool(
    name="cafe24_sftp_list",
    annotations={
        "title": "카페24 SFTP 파일트리",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def cafe24_sftp_list(
    remote_path: Annotated[str, Field(description="원격 경로 (예: /skin14, /skin14/_nk/css)")] = "/",
    depth: Annotated[int, Field(description="탐색 깊이 (1=바로 아래만)", ge=1, le=5)] = 1,
    mall_id: MallId = "demo000",
) -> str:
    """SFTP 로 원격 폴더의 파일트리를 조회한다 (API 엔 없는 기능).

    반환: [{"path", "type": "file"|"dir", "size", "mtime"}, ...] JSON.
    깊이가 클수록 느려지므로 넓게 1~2로 훑고 필요한 곳만 더 들어갈 것.
    """
    try:
        with open_remote(mall_id) as s:
            return _json(s.list(remote_path, depth))
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="cafe24_sftp_read",
    annotations={
        "title": "카페24 SFTP 파일 읽기",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def cafe24_sftp_read(
    remote_path: Annotated[str, Field(description="원격 파일 경로 (예: /skin14/_nk/css/tokens.css)")],
    mall_id: MallId = "demo000",
) -> str:
    """SFTP 로 원격 텍스트 파일 1건의 내용을 읽는다.

    CSS/JS 등 에셋 읽기는 이 도구가 정답 (API read_page 는 HTML 만 가능).
    5MB 초과 파일은 거부된다 → cafe24_sftp_download 사용.
    """
    try:
        with open_remote(mall_id) as s:
            return s.read(remote_path)
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="cafe24_sftp_download",
    annotations={
        "title": "카페24 SFTP 다운로드",
        "readOnlyHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def cafe24_sftp_download(
    remote_path: Annotated[str, Field(description="원격 파일/폴더 경로 (폴더면 재귀 미러)")],
    local_path: Annotated[str, Field(description="저장할 로컬 경로 (절대 경로 권장)")],
    mall_id: MallId = "demo000",
) -> str:
    """원격 파일/폴더를 로컬로 내려받는다 (폴더는 하위까지 재귀).

    대량 읽기·초기 동기화는 API 대신 이 도구를 쓴다 (호출 제한 없음).
    반환: {"files": 받은 개수, "failed": 실패 개수}
    """
    try:
        with open_remote(mall_id) as s:
            return _json(s.download(remote_path, local_path))
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="cafe24_sftp_backup",
    annotations={
        "title": "카페24 SFTP 백업 (쓰기 전)",
        "readOnlyHint": True,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
def cafe24_sftp_backup(
    remote_path: Annotated[str, Field(description="백업할 원격 파일/폴더 경로")],
    mall_id: MallId = "demo000",
) -> str:
    """원격 파일/폴더를 로컬 mcp/backups/{몰}/{시각}/ 아래로 백업한다.

    cafe24_sftp_upload 가 기본으로 자동 호출하지만,
    큰 작업 전에 폴더 단위로 미리 백업해 둘 때 직접 쓸 수 있다.
    반환: 백업본 로컬 절대 경로 (원격에 없는 경로면 그 사실을 알려줌).
    """
    try:
        with open_remote(mall_id) as s:
            dest = s.backup(remote_path)
        return dest if dest else f"원격에 없는 경로라 백업할 원본이 없습니다: {remote_path} (신규 파일이면 정상)"
    except Exception as e:
        return _err(e)


@mcp.tool(
    name="cafe24_sftp_upload",
    annotations={
        "title": "카페24 SFTP 업로드 ★운영 반영",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
def cafe24_sftp_upload(
    remote_path: Annotated[str, Field(description="업로드할 원격 경로 (write_allowed 안이어야 함)")],
    local_path: Annotated[Optional[str], Field(description="올릴 로컬 파일/폴더 경로 (content 와 둘 중 하나)")] = None,
    content: Annotated[Optional[str], Field(description="파일 내용 문자열을 바로 업로드 (local_path 와 둘 중 하나)")] = None,
    auto_backup: Annotated[bool, Field(description="덮어쓰기 전 원본 자동 백업 (기본 켜짐, 끄지 말 것)")] = True,
    mall_id: MallId = "demo000",
) -> str:
    """★운영 서버 반영 — 로컬 파일/폴더 또는 문자열을 원격에 업로드한다.

    반드시 지킬 것:
      1) 이 도구를 호출하기 전에 사용자에게 "업로드해도 될까요?" 확인을 받을 것
         (누끼토끼 절대룰 — 운영 반영 전 컨펌).
      2) write_allowed 화이트리스트(config/sftp_{mall}.json) 밖 경로는
         코드가 무조건 거부한다 (demo000: /skin14, /mobile 만 허용).
      3) auto_backup 은 끄지 말 것 — 사고 시 mcp/backups/ 의 백업본으로 복구.

    업로드 후에는 라이브 화면(?v=타임스탬프 캐시 우회)을 PC+모바일로 검증할 것.
    반환: {"uploaded": 개수, "failed": 개수, "backup": 백업경로|null}
    """
    try:
        if not local_path and content is None:
            return "Error(입력): local_path 또는 content 중 하나는 필요합니다."
        with open_remote(mall_id) as s:
            return _json(
                s.upload(
                    local_path=local_path,
                    remote_path=remote_path,
                    content=content,
                    auto_backup=auto_backup,
                )
            )
    except Exception as e:
        return _err(e)


if __name__ == "__main__":
    # stdio 모드로 실행 — Claude Code / Cursor 가 이 프로세스와 표준입출력으로 대화
    mcp.run()
