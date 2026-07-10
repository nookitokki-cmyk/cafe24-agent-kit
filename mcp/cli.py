#!/usr/bin/env python3
"""
백엔드 검증용 CLI — MCP 서버를 올리기 전, 함수가 잘 동작하는지 손으로 확인.

사용법 (mcp/ 에서 실행):

  [키트]
  python cli.py diagnose                    설치 진단 (smoke 5/9 기대치)
  python cli.py scaffold --mall {몰ID}      clients/{몰ID} scaffold
  python cli.py kit-version                 로컬 VERSION
  python cli.py kit-version --check-remote  GitHub Release 또는 VERSION URL 비교
  python cli.py kit-autoupdate              시작 시 자동 업데이트 체크 (12h 스로틀)
  python cli.py kit-autoupdate --apply      새 버전이면 조건부 자동 적용 (채널 감지)
  python cli.py kit-autoupdate --force      스로틀 무시하고 즉시 재확인
  python cli.py kit-update --source <path>  코드만 갱신 (config·clients 보존)
  python cli.py kit-update --from-github [--tag v2.2.0]  Release zip 자동 적용
  python cli.py kit-update --dry-run        갱신 대상 미리보기
  python cli.py skin-audit <local-skin-root> [--json-out path]
                                            로컬 스킨 read-only 안전 점검

  [API 백엔드]
  python cli.py status                       토큰 상태 확인
  python cli.py themes                       디자인(스킨) 목록
  python cli.py page <skin_no> <path>        스킨 파일 1건 읽기 (정본)
  python cli.py auth-url                     (refresh 만료 시) 재동의 주소 출력
  python cli.py code "<URL 또는 code>"        동의 후 code 를 토큰으로 교환
  python cli.py products [--limit N]         상품 목록
  python cli.py product <product_no>         상품 1건 조회
  python cli.py product-create --name ... --price ... [--json file]

  [SFTP 백엔드]
  python cli.py ls <원격경로> [깊이]           파일트리
  python cli.py cat <원격경로>                 파일 내용 (앞부분)
  python cli.py get <원격경로> <로컬경로>       다운로드
  python cli.py backup <원격경로>              백업본 만들기
  python cli.py put <로컬경로> <원격경로>       ★업로드 (사용자 컨펌 후에만)

  공통 옵션: --mall <mall_id>   (기본값 demo000)
"""
import json
import sys
from pathlib import Path

# Backends (auth/api/sftp) pull extra deps like paramiko. kit-* commands don't,
# so defer any ImportError — version/update/diagnose must work *before* the user
# runs `pip install -r requirements.txt` (e.g. /키트시작 Q0 auto-update check).
try:
    from auth.oauth import AuthError, TokenManager
    from backends.cafe24_api import Cafe24API, Cafe24ApiError
    from backends.cafe24_ftp import open_remote
    from backends.cafe24_sftp import SftpWriteDenied

    _BACKENDS_IMPORT_ERROR: Exception | None = None
except ImportError as _e:
    _BACKENDS_IMPORT_ERROR = _e
    TokenManager = Cafe24API = open_remote = None  # type: ignore[assignment,misc]

    class AuthError(Exception):  # type: ignore[no-redef]
        pass

    class Cafe24ApiError(Exception):  # type: ignore[no-redef]
        pass

    class SftpWriteDenied(Exception):  # type: ignore[no-redef]
        pass

from kit_tools import (
    diagnose_kit_setup,
    fetch_remote_version,
    kit_autoupdate,
    kit_update,
    kit_update_from_github,
    read_kit_version,
    scaffold_client,
)
from skin_analyzer import audit_skin

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _pop_mall(args: list[str]) -> str:
    """--mall 옵션을 찾아 빼내고 몰 아이디를 돌려준다."""
    if "--mall" in args:
        i = args.index("--mall")
        mall = args[i + 1]
        del args[i : i + 2]
        return mall
    return "demo000"


def _pop_flag(args: list[str], name: str) -> bool:
    if name in args:
        args.remove(name)
        return True
    return False


def _parse_kv_flags(args: list[str]) -> tuple[dict[str, str], list[str]]:
    """--key value 쌍을 dict로, 나머지 positional args 반환."""
    flags: dict[str, str] = {}
    rest: list[str] = []
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:].replace("-", "_")
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                flags[key] = "true"
                i += 1
            else:
                flags[key] = args[i + 1]
                i += 2
        else:
            rest.append(args[i])
            i += 1
    return flags, rest


def _load_product_payloads(flags: dict[str, str]) -> list[dict]:
    json_path = flags.get("json") or flags.get("file")
    if json_path:
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        if isinstance(data, dict) and "products" in data:
            return list(data["products"])
        if isinstance(data, list):
            return data
        raise ValueError("JSON 은 배열 또는 {\"products\": [...]} 형식이어야 합니다.")
    name = flags.get("name")
    price = flags.get("price")
    if not name or not price:
        raise ValueError(
            "단건 등록: --name 과 --price 필수. "
            "일괄 등록: --json products.json"
        )
    payload: dict = {"product_name": name, "price": price}
    for src, dst in (
        ("supply_price", "supply_price"),
        ("retail_price", "retail_price"),
        ("display", "display"),
        ("selling", "selling"),
        ("description", "description"),
    ):
        if src in flags:
            payload[dst] = flags[src]
    return [payload]


def _pop_opt(args: list[str], name: str) -> str | None:
    if name in args:
        i = args.index(name)
        if i + 1 >= len(args):
            return None
        val = args[i + 1]
        del args[i : i + 2]
        return val
    return None


def main():
    args = sys.argv[1:]
    mall = _pop_mall(args)
    dry_run = _pop_flag(args, "--dry-run")
    check_remote = _pop_flag(args, "--check-remote")
    overwrite = _pop_flag(args, "--overwrite")
    from_github = _pop_flag(args, "--from-github")
    apply_update = _pop_flag(args, "--apply")
    force = _pop_flag(args, "--force")
    github_tag = _pop_opt(args, "--tag") or "latest"
    cmd = args[0] if args else "status"

    # Backend commands need the optional deps; kit-* commands do not.
    backend_cmds = {
        "status", "themes", "page", "auth-url", "code",
        "products", "product", "product-create",
        "ls", "cat", "get", "backup", "put",
    }
    if cmd in backend_cmds and _BACKENDS_IMPORT_ERROR is not None:
        print(
            "ERROR: 백엔드 의존성이 없습니다 — `mcp/` 에서 "
            "`pip install -r requirements.txt` 후 다시 시도하세요.\n"
            f"  ({_BACKENDS_IMPORT_ERROR})",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        if cmd == "diagnose":
            print(json.dumps(diagnose_kit_setup(), ensure_ascii=False, indent=2))

        elif cmd == "scaffold":
            target = args[1] if len(args) > 1 else mall
            result = scaffold_client(target, overwrite=overwrite)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif cmd == "kit-version":
            local = read_kit_version()
            out = {"local": local}
            if check_remote:
                remote = fetch_remote_version()
                out["remote"] = remote
                if remote.get("available") and local.get("version"):
                    out["update_available"] = (
                        remote.get("version") != local.get("version")
                    )
            print(json.dumps(out, ensure_ascii=False, indent=2))

        elif cmd == "kit-autoupdate":
            result = kit_autoupdate(apply=apply_update, force=force)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif cmd == "kit-update":
            if from_github:
                result = kit_update_from_github(
                    tag=github_tag, dry_run=dry_run
                )
            else:
                source = None
                if "--source" in args:
                    i = args.index("--source")
                    source = Path(args[i + 1]).expanduser()
                result = kit_update(source=source, dry_run=dry_run)
            print(json.dumps(result, ensure_ascii=False, indent=2))

        elif cmd == "skin-audit":
            if len(args) < 2:
                print("사용법: python cli.py skin-audit <local-skin-root> [--json-out path]", file=sys.stderr)
                sys.exit(1)
            json_out = _pop_opt(args, "--json-out")
            report = audit_skin(Path(args[1]).expanduser())
            payload = report.to_jsonable()
            if json_out:
                out_path = Path(json_out).expanduser()
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"skin-audit 저장 완료: {out_path}")
            else:
                print(json.dumps(payload, ensure_ascii=False, indent=2))

        elif cmd == "status":
            api = Cafe24API(mall)
            print(json.dumps(api.auth_status(), ensure_ascii=False, indent=2))

        elif cmd == "themes":
            api = Cafe24API(mall)
            themes = api.list_themes()
            print(f"총 {len(themes)}개 디자인:")
            for th in themes:
                print(
                    f"  - skin_no={th['skin_no']} type={th['editor_type']} "
                    f"usage={th['usage_type']} name={th['skin_name']!r}"
                )

        elif cmd == "page":
            if len(args) < 3:
                print("사용법: python cli.py page <skin_no> <path>", file=sys.stderr)
                sys.exit(1)
            api = Cafe24API(mall)
            page = api.read_page(int(args[1]), args[2])
            source = page.get("source", "")
            print(f"path={page.get('path')!r} source={len(source)}자 (앞 300자):\n")
            print(source[:300])

        elif cmd == "auth-url":
            tm = TokenManager(mall)
            print("아래 주소를 브라우저 주소창에 붙여넣고 '허용'을 누르세요:\n")
            print(tm.auth_url())
            print(
                f"\n허용 후 주소창이 대략 이렇게 바뀝니다 (404 화면이어도 URL만 있으면 OK):"
            )
            print(f"  https://{mall}.cafe24.com/oauth-callback?code=...&state=...")
            print(f'\n  python cli.py code "복사한_URL_전체" --mall {mall}')

        elif cmd == "code":
            if len(args) < 2:
                print('사용법: python cli.py code "<URL 또는 code>"', file=sys.stderr)
                sys.exit(1)
            tm = TokenManager(mall)
            tok = tm.exchange_code(args[1])
            print(f"토큰 발급 완료 (access 만료: {tok.get('expires_at')})")

        elif cmd == "products":
            flags, _ = _parse_kv_flags(args[1:])
            limit = int(flags.get("limit", "20"))
            offset = int(flags.get("offset", "0"))
            api = Cafe24API(mall)
            products = api.list_products(limit=limit, offset=offset)
            print(f"총 {len(products)}건 (limit={limit}, offset={offset}):")
            for p in products:
                print(
                    f"  - no={p.get('product_no')} code={p.get('product_code')} "
                    f"name={p.get('product_name')!r} price={p.get('price')} "
                    f"display={p.get('display')} selling={p.get('selling')}"
                )

        elif cmd == "product":
            if len(args) < 2:
                print("사용법: python cli.py product <product_no>", file=sys.stderr)
                sys.exit(1)
            api = Cafe24API(mall)
            product = api.get_product(int(args[1]))
            print(json.dumps(product, ensure_ascii=False, indent=2))

        elif cmd == "product-create":
            flags, _ = _parse_kv_flags(args[1:])
            payloads = _load_product_payloads(flags)
            api = Cafe24API(mall)
            created = []
            for payload in payloads:
                product = api.create_product(payload)
                created.append(
                    {
                        "product_no": product.get("product_no"),
                        "product_code": product.get("product_code"),
                        "product_name": product.get("product_name"),
                        "price": product.get("price"),
                    }
                )
            print(json.dumps({"created": created, "count": len(created)}, ensure_ascii=False, indent=2))

        elif cmd == "ls":
            path = args[1] if len(args) > 1 else "/"
            depth = int(args[2]) if len(args) > 2 else 1
            with open_remote(mall) as s:
                items = s.list(path, depth)
            for it in items:
                indent = "  " * (it["path"].strip("/").count("/"))
                icon = "+" if it["type"] == "dir" else "-"
                size = f" ({it['size']:,}b)" if it["type"] == "file" else ""
                print(f"{indent}{icon} {it['path']}{size}")
            print(f"\n총 {len(items)}개 항목")

        elif cmd == "cat":
            if len(args) < 2:
                print("사용법: python cli.py cat <원격경로>", file=sys.stderr)
                sys.exit(1)
            with open_remote(mall) as s:
                text = s.read(args[1])
            print(f"{args[1]} — {len(text):,}자 (앞 500자):\n")
            print(text[:500])

        elif cmd == "get":
            if len(args) < 3:
                print("사용법: python cli.py get <원격경로> <로컬경로>", file=sys.stderr)
                sys.exit(1)
            with open_remote(mall) as s:
                r = s.download(args[1], args[2])
            print(f"다운로드: 받음 {r['files']}개 / 실패 {r['failed']}개 → {args[2]}")

        elif cmd == "backup":
            if len(args) < 2:
                print("사용법: python cli.py backup <원격경로>", file=sys.stderr)
                sys.exit(1)
            with open_remote(mall) as s:
                dest = s.backup(args[1])
            print(f"백업 완료: {dest}" if dest else "원격에 없는 경로 — 백업 생략(신규)")

        elif cmd == "put":
            if len(args) < 3:
                print("사용법: python cli.py put <로컬경로> <원격경로>", file=sys.stderr)
                sys.exit(1)
            with open_remote(mall) as s:
                r = s.upload(local_path=args[1], remote_path=args[2])
            print(
                f"업로드: {r['uploaded']}개 / 실패 {r['failed']}개"
                + (f"\n백업본: {r['backup']}" if r["backup"] else " (신규 — 백업 없음)")
            )

        else:
            print(__doc__)
            sys.exit(1)

    except (AuthError, Cafe24ApiError, SftpWriteDenied, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
