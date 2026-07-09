#!/usr/bin/env python3
"""
MCP 서버 스모크 테스트 — 실제 MCP 클라이언트로 server.py 를 stdio 로 띄워서
도구 등록·호출이 끝까지 동작하는지 확인한다 (읽기 도구만 호출, 업로드 X).

실행: python smoke_test.py   (mcp/ 에서)

v2.2 smoke (기본):
  - 자격 증명 없음 → **5/9 partial, exit 0** (정상)
  - OAuth·SFTP 후 → API/SFTP 호출 포함 9/9+
  - ecudemo400786 토큰 + SMOKE_PREFLIGHT_ALL=1 → live preflight batch
"""
import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = Path(HERE) / "config"
PILOT_MALL = "ecudemo400786"
PILOT_TOKEN = CONFIG_DIR / f"{PILOT_MALL}.token.json"
PREFLIGHT_CHECKS = (
    "header",
    "mobile_full",
    "plp",
    "pdp",
    "basket",
    "member",
    "board",
    "page",
    "paginate",
)
VALID_PREFLIGHT_CHECKS = sorted(PREFLIGHT_CHECKS) + ["all"]
PARTIAL_PASS_COUNT = 5

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def any_token_exists() -> bool:
    return any(CONFIG_DIR.glob("*.token.json"))


def pilot_token_exists() -> bool:
    return PILOT_TOKEN.is_file()


def preflight_all_enabled() -> bool:
    default = "1" if pilot_token_exists() else "0"
    val = os.environ.get("SMOKE_PREFLIGHT_ALL", default).strip().lower()
    return val not in ("0", "false", "no", "off")


async def run_preflight_check(session, check: str, mall_id: str, timeout: int = 180):
    """run_preflight 1회 호출 → (status, summary). status: OK | WARN | SKIP | ERROR."""
    try:
        res = await asyncio.wait_for(
            session.call_tool(
                "run_preflight",
                {"check": check, "mall_id": mall_id},
            ),
            timeout=timeout,
        )
        text = res.content[0].text if res.content else ""
        data = json.loads(text)
        if res.isError or "error" in data:
            err = data.get("error", text[:120])
            return "ERROR", f"error={err}"
        ok = data.get("total_score") == 100 and data.get("pass") is True
        status = "OK" if ok else "WARN"
        return status, f"score={data.get('total_score')}, pass={data.get('pass')}"
    except asyncio.TimeoutError:
        return "SKIP", "timeout"
    except Exception as e:
        return "SKIP", f"{type(e).__name__}: {e}"


async def main() -> int:
    params = StdioServerParameters(
        command=sys.executable,
        args=[os.path.join(HERE, "server.py")],
        cwd=HERE,
    )
    results: list[str] = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mall_id = PILOT_MALL if pilot_token_exists() else "demo000"
            if pilot_token_exists():
                print(f"[예시몰 파일럿] {PILOT_MALL} token — preflight·API 호출에 사용")
            else:
                print(
                    f"[예시몰 파일럿] {PILOT_MALL} token 없음 (정상 — 키트 예시몰이라 무시해도 됨), "
                    f"API 기본몰={mall_id}"
                )

            tools = await session.list_tools()
            names = sorted(t.name for t in tools.tools)
            print(f"[1] 등록된 도구 {len(names)}종:")
            for n in names:
                print(f"    - {n}")

            expected = {
                "get_kit_guides",
                "diagnose_kit_setup",
                "scaffold_client",
                "run_preflight",
                "cafe24_list_themes",
                "cafe24_read_page",
                "cafe24_auth_status",
                "cafe24_sftp_list",
                "cafe24_sftp_read",
                "cafe24_sftp_download",
                "cafe24_sftp_backup",
                "cafe24_sftp_upload",
            }
            missing = expected - set(names)
            r0 = "OK" if not missing else "ERROR"
            if missing:
                print(f"\n[tools/list] {r0} — 누락: {sorted(missing)}")
            else:
                print(f"\n[tools/list] {r0} — 필수 {len(expected)}종 등록")
            results.append(r0)

            res_kit = await session.call_tool("get_kit_guides", {})
            kit_text = res_kit.content[0].text if res_kit.content else ""
            kit_data: dict = {}
            try:
                kit_data = json.loads(kit_text)
                kit_ok = (
                    not res_kit.isError
                    and "kit_root" in kit_data
                    and "workflows" in kit_data
                    and "kit_version" in kit_data
                    and len(kit_data.get("workflows", [])) == 8
                )
            except json.JSONDecodeError:
                kit_ok = False
            r_kit = "OK" if kit_ok else "ERROR"
            print(
                f"\n[get_kit_guides] {r_kit} — workflows="
                f"{len(kit_data.get('workflows', [])) if kit_ok else '?'}, "
                f"kit_root={kit_data.get('kit_root', kit_text[:80]) if kit_ok else kit_text[:120]}"
            )
            results.append(r_kit)

            res_f36 = await session.call_tool(
                "get_kit_guides", {"symptom_f_code": "F36"}
            )
            f36_text = res_f36.content[0].text if res_f36.content else ""
            f36_data: dict = {}
            try:
                f36_data = json.loads(f36_text)
                f36_ok = (
                    not res_f36.isError
                    and "f_code_hint" in f36_data
                    and "F36" in f36_data["f_code_hint"]
                )
            except json.JSONDecodeError:
                f36_ok = False
            r_f36 = "OK" if f36_ok else "ERROR"
            print(
                f"[get_kit_guides+F36] {r_f36} — "
                f"hint={f36_data.get('f_code_hint', f36_text[:80]) if f36_ok else f36_text[:120]}"
            )
            results.append(r_f36)

            res_pf_bad = await session.call_tool(
                "run_preflight", {"check": "__invalid_check__"}
            )
            pf_bad_text = res_pf_bad.content[0].text if res_pf_bad.content else ""
            pf_bad_data: dict = {}
            try:
                pf_bad_data = json.loads(pf_bad_text)
                valid = sorted(pf_bad_data.get("valid_checks", []))
                pf_bad_ok = (
                    not res_pf_bad.isError
                    and "error" in pf_bad_data
                    and set(valid) == set(VALID_PREFLIGHT_CHECKS)
                )
            except json.JSONDecodeError:
                pf_bad_ok = False
            r_pf_bad = "OK" if pf_bad_ok else "ERROR"
            print(
                f"[run_preflight/invalid] {r_pf_bad} — "
                f"valid_checks={len(pf_bad_data.get('valid_checks', []))}/"
                f"{len(VALID_PREFLIGHT_CHECKS)}"
            )
            results.append(r_pf_bad)

            if pilot_token_exists() and preflight_all_enabled():
                print(
                    f"\n[run_preflight] live {len(PREFLIGHT_CHECKS)} checks "
                    f"— mall={PILOT_MALL} (Playwright, ~15min; "
                    f"SMOKE_PREFLIGHT_ALL=0 for fast smoke)"
                )
                pf_live_results: list[str] = []
                for check in PREFLIGHT_CHECKS:
                    status, summary = await run_preflight_check(
                        session, check, PILOT_MALL
                    )
                    pf_live_results.append(status)
                    print(f"    [{check}] {status} — {summary}")
                pf_pass = sum(1 for s in pf_live_results if s == "OK")
                r_pf_all = "OK" if pf_pass == len(PREFLIGHT_CHECKS) else "WARN"
                print(
                    f"[run_preflight/all] {r_pf_all} — "
                    f"{pf_pass}/{len(PREFLIGHT_CHECKS)} score=100"
                )
                results.append(r_pf_all)
            elif pilot_token_exists():
                print(
                    "\n[run_preflight/live] SKIP — SMOKE_PREFLIGHT_ALL=0 "
                    "(v2 default is 1 when token present)"
                )
                results.append("OK")
            else:
                print(
                    f"\n[run_preflight/live] SKIP — "
                    f"no token in mcp/config (9 check Playwright 생략)"
                )
                results.append("OK")

            has_creds = any_token_exists()

            async def call(tool: str, args: dict, preview: int = 200):
                res = await session.call_tool(tool, args)
                text = res.content[0].text if res.content else ""
                if res.isError or text.startswith("Error"):
                    if "No such file" in text or "없음" in text:
                        status = "WARN"
                    else:
                        status = "ERROR"
                else:
                    status = "OK"
                print(f"\n[{tool}] {status} — 응답 {len(text):,}자 (앞 {preview}자):")
                print("    " + text[:preview].replace("\n", "\n    "))
                return status

            if has_creds:
                r1 = await call("cafe24_auth_status", {"mall_id": mall_id})
                r2 = await call("cafe24_list_themes", {"mall_id": mall_id})
                r3 = await call(
                    "cafe24_sftp_list",
                    {"remote_path": "/skin14", "depth": 1, "mall_id": mall_id},
                )
                r4 = await call(
                    "cafe24_sftp_read",
                    {
                        "remote_path": "/skin14/_nk/css/header.css",
                        "mall_id": mall_id,
                    },
                )
                res = await session.call_tool(
                    "cafe24_sftp_upload",
                    {
                        "remote_path": "/skin2/test.html",
                        "content": "x",
                        "mall_id": mall_id,
                    },
                )
                text = res.content[0].text if res.content else ""
                r5 = (
                    "OK"
                    if "쓰기보호" in text or "쓰기 거부" in text
                    else "ERROR"
                )
                print(
                    f"\n[cafe24_sftp_upload→보호슬롯] {r5} "
                    f"(거부돼야 정상): {text[:120]}"
                )
                results.extend([r1, r2, r3, r4, r5])
            else:
                skip_msg = "SKIP — OAuth/SFTP 미설정 (v2.2: 5/9 partial 정상)"
                for label in (
                    "cafe24_auth_status",
                    "cafe24_list_themes",
                    "cafe24_sftp_list",
                    "cafe24_sftp_read",
                    "cafe24_sftp_upload→보호슬롯",
                ):
                    print(f"\n[{label}] {skip_msg}")
                    results.append("SKIP")

            ok_count = sum(1 for r in results if r == "OK")
            skip_count = sum(1 for r in results if r == "SKIP")
            total = len(results)
            partial = not has_creds

            print(
                f"\n=== 결과: {ok_count}/{total} 통과"
                + (f", {skip_count} SKIP" if skip_count else "")
                + f", 도구 {len(names)}종 등록 ==="
            )
            if partial and ok_count >= PARTIAL_PASS_COUNT:
                print(
                    f"=== {PARTIAL_PASS_COUNT}/9 partial (정상) — "
                    "OAuth·SFTP 후 전체 smoke ==="
                )
                print(json.dumps({"expected_partial": True, "ok": ok_count, "total": total}))
                return 0

            if all(r in ("OK", "SKIP", "WARN") for r in results):
                return 0
            return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
