#!/usr/bin/env python3
"""
백엔드 검증용 CLI — MCP 서버를 올리기 전, 함수가 잘 동작하는지 손으로 확인.

사용법 (mcp/ 에서 실행):

  [키트]
  python cli.py diagnose                    설치 진단 (smoke 5/9 기대치)
  python cli.py scaffold --mall {몰ID}      clients/{몰ID} scaffold
  python cli.py kit-version                 로컬 VERSION
  python cli.py kit-version --check-remote  GitHub Release 또는 VERSION URL 비교
  python cli.py kit-update --source <path>  코드만 갱신 (config·clients 보존)
  python cli.py kit-update --from-github [--tag v2.2.0]  Release zip 자동 적용
  python cli.py kit-update --dry-run        갱신 대상 미리보기

  [API 백엔드]
  python cli.py status                       토큰 상태 확인
  python cli.py themes                       디자인(스킨) 목록
  python cli.py page <skin_no> <path>        스킨 파일 1건 읽기 (정본)
  python cli.py auth-url                     (refresh 만료 시) 재동의 주소 출력
  python cli.py code "<URL 또는 code>"        동의 후 code 를 토큰으로 교환

  [SFTP 백엔드]
  python cli.py ls <원격경로> [깊이]           파일트리
  python cli.py cat <원격경로>                 파일 내용 (앞부분)
  python cli.py get <원격경로> <로컬경로>       다운로드
  python cli.py backup <원격경로>              백업본 만들기
  python cli.py put <로컬경로> <원격경로>       ★업로드 (사용자 컨펌 후에만)

  공통 옵션: --mall <mall_id>   (기본값 paransky97)
"""
import json
import sys
from pathlib import Path

from auth.oauth import AuthError, TokenManager
from backends.cafe24_api import Cafe24API, Cafe24ApiError
from backends.cafe24_sftp import Cafe24SFTP, SftpWriteDenied
from kit_tools import (
    diagnose_kit_setup,
    fetch_remote_version,
    kit_update,
    kit_update_from_github,
    read_kit_version,
    scaffold_client,
)

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
    return "paransky97"


def _pop_flag(args: list[str], name: str) -> bool:
    if name in args:
        args.remove(name)
        return True
    return False


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
    github_tag = _pop_opt(args, "--tag") or "latest"
    cmd = args[0] if args else "status"

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

        elif cmd == "ls":
            path = args[1] if len(args) > 1 else "/"
            depth = int(args[2]) if len(args) > 2 else 1
            with Cafe24SFTP(mall) as s:
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
            with Cafe24SFTP(mall) as s:
                text = s.read(args[1])
            print(f"{args[1]} — {len(text):,}자 (앞 500자):\n")
            print(text[:500])

        elif cmd == "get":
            if len(args) < 3:
                print("사용법: python cli.py get <원격경로> <로컬경로>", file=sys.stderr)
                sys.exit(1)
            with Cafe24SFTP(mall) as s:
                r = s.download(args[1], args[2])
            print(f"다운로드: 받음 {r['files']}개 / 실패 {r['failed']}개 → {args[2]}")

        elif cmd == "backup":
            if len(args) < 2:
                print("사용법: python cli.py backup <원격경로>", file=sys.stderr)
                sys.exit(1)
            with Cafe24SFTP(mall) as s:
                dest = s.backup(args[1])
            print(f"백업 완료: {dest}" if dest else "원격에 없는 경로 — 백업 생략(신규)")

        elif cmd == "put":
            if len(args) < 3:
                print("사용법: python cli.py put <로컬경로> <원격경로>", file=sys.stderr)
                sys.exit(1)
            with Cafe24SFTP(mall) as s:
                r = s.upload(local_path=args[1], remote_path=args[2])
            print(
                f"업로드: {r['uploaded']}개 / 실패 {r['failed']}개"
                + (f"\n백업본: {r['backup']}" if r["backup"] else " (신규 — 백업 없음)")
            )

        else:
            print(__doc__)
            sys.exit(1)

    except (AuthError, Cafe24ApiError, SftpWriteDenied) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
