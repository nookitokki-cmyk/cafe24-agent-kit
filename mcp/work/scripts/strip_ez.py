#!/usr/bin/env python3
"""Remove SmartDesignEasy markup from Cafe24 skin HTML (WORK-GUIDE §15)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Files/dirs to skip even when scanning recursively (system EZ metadata)
SKIP_REL_PATHS = {
    "ez/ez-module.html",
    "ez/ez-settings.json",
    "smart-banner/init/ez-initialize.html",
}

EZ_PROP_BLOCK = re.compile(r"[ \t]*<ez-prop\b.*?</ez-prop>\s*\n?", re.DOTALL | re.IGNORECASE)
EZ_SCRIPT_PROP = re.compile(
    r"[ \t]*<script[^>]*type=\"text/ez-prop\".*?</script>\s*\n?",
    re.DOTALL | re.IGNORECASE,
)
DATA_EZ_ATTR = re.compile(r'\s+data-ez-[a-zA-Z-]+="[^"]*"')
DATA_EZ_BARE = re.compile(r'\s+data-ez="[^"]*"')
DATA_EZ_NOVAL = re.compile(r"\s+data-ez-[a-zA-Z-]+(?=[\s>/])")

# EZST runtime in layout/main (Phase C full)
EZ_FAVICON_BLOCK = re.compile(
    r"[ \t]*<!--ez-favicon\[-->.*?<!--ez-favicon\]-->\s*\n?",
    re.DOTALL,
)
EZST_INIT_SCRIPT = re.compile(
    r"[ \t]*<script>try\{window\.EZST=\{q:\[\],register:.*?</script>\s*\n?",
    re.DOTALL,
)
EZ_INIT_JS = re.compile(r"[ \t]*<!--@js\(/ez/init\.js\)-->\s*\n?", re.IGNORECASE)


def _count_ez(html: str) -> dict[str, int]:
    return {
        "data-ez-attrs": len(re.findall(r"data-ez-[a-zA-Z-]+", html)),
        "data-ez-bare": html.count('data-ez="'),
        "ez-prop-blocks": len(EZ_PROP_BLOCK.findall(html)),
        "ez-script-prop": len(EZ_SCRIPT_PROP.findall(html)),
        "ezst-init": len(EZST_INIT_SCRIPT.findall(html)),
        "ez-init-js": len(EZ_INIT_JS.findall(html)),
        "module=": html.count("module="),
    }


def strip_html(html: str, *, remove_runtime: bool = False) -> tuple[str, dict[str, int]]:
    before = _count_ez(html)
    out = html
    out = EZ_PROP_BLOCK.sub("", out)
    out = EZ_SCRIPT_PROP.sub("", out)
    out = DATA_EZ_ATTR.sub("", out)
    out = DATA_EZ_BARE.sub("", out)
    out = DATA_EZ_NOVAL.sub("", out)
    if remove_runtime:
        out = EZ_FAVICON_BLOCK.sub("", out)
        out = EZST_INIT_SCRIPT.sub("", out)
        out = EZ_INIT_JS.sub("", out)
    after = _count_ez(out)
    removed = {k: before[k] - after[k] for k in before}
    return out, removed


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    if rel in SKIP_REL_PATHS:
        return True
    return False


def process_file(path: Path, *, write: bool, remove_runtime: bool) -> dict | None:
    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    if "data-ez" not in original and "<ez-prop" not in original.lower():
        if not (remove_runtime and ("EZST" in original or "/ez/init.js" in original)):
            return None
    stripped, removed = strip_html(original, remove_runtime=remove_runtime)
    if stripped == original:
        return None
    stats = {"path": str(path), "removed": removed, "after": _count_ez(stripped)}
    if write:
        path.write_text(stripped, encoding="utf-8", newline="\n")
    return stats


def collect_html_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() == ".html" else []
    return sorted(p for p in target.rglob("*.html") if p.is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description="Strip data-ez-* and ez-prop from Cafe24 HTML")
    parser.add_argument("target", help="HTML file or skin directory")
    parser.add_argument("--write", action="store_true", help="Apply changes (default: preview)")
    parser.add_argument(
        "--remove-runtime",
        action="store_true",
        help="Also remove EZST init, ez-favicon, @js(/ez/init.js) from layout/main",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"ERROR: not found: {target}", file=sys.stderr)
        return 1

    root = target if target.is_dir() else target.parent
    files = collect_html_files(target)
    changed = []
    for fp in files:
        if target.is_dir() and should_skip(fp, root):
            continue
        rel = fp.relative_to(root).as_posix() if fp.is_relative_to(root) else fp.name
        remove_rt = args.remove_runtime and rel in {
            "layout/basic/layout.html",
            "layout/basic/main.html",
        }
        stats = process_file(fp, write=args.write, remove_runtime=remove_rt)
        if stats:
            changed.append(stats)

    mode = "WRITE" if args.write else "PREVIEW"
    print(f"[{mode}] {len(files)} html scanned, {len(changed)} would change")
    total_removed = {}
    for s in changed:
        rel = Path(s["path"]).name
        r = s["removed"]
        parts = [f"{k}:-{v}" for k, v in r.items() if v]
        print(f"  {rel}: {', '.join(parts) or 'runtime only'}")
        for k, v in r.items():
            total_removed[k] = total_removed.get(k, 0) + v
    if total_removed:
        print("TOTAL removed:", ", ".join(f"{k}={v}" for k, v in sorted(total_removed.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
