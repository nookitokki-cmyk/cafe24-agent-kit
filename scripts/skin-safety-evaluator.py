#!/usr/bin/env python3
"""Evaluate Cafe24 SmartDesign template safety criteria.

This script is intentionally dependency-free so it can run on a learner's
machine with only Python installed. It scans a shipped template source tree and
prints a JSON report that matches the deep-interview skin-safety criteria.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Pattern


CRITERIA_KEYS = (
    "smartdesign_directives_preserved",
    "cafe24_variables_preserved",
    "modules_preserved",
    "xans_ecbase_preserved",
    "order_payment_pg_excluded",
    "backup_and_rollback_defined",
    "brand_traces_removed",
    "local_smartdesign_assets_exist",
    "non_developer_safe",
)

TEXT_EXTENSIONS = {
    ".css",
    ".html",
    ".htm",
    ".js",
    ".json",
    ".md",
    ".svg",
    ".txt",
    ".xml",
}

SMARTDESIGN_DIRECTIVE_RE = re.compile(
    r"<!--\s*@(?:layout|contents|import|css|js)\b[^>]*-->", re.IGNORECASE
)
LOCAL_RESOURCE_DIRECTIVE_RE = re.compile(
    r"<!--\s*@(?P<kind>layout|import|css|js)\((?P<path>[^)]+)\)\s*-->",
    re.IGNORECASE,
)
CAFE24_VARIABLE_RE = re.compile(r"\{\$[A-Za-z0-9_.]+(?:\|[^}]*)?\}")
MODULE_RE = re.compile(r"\bmodule\s*=\s*([\"'])[^\"']+\1", re.IGNORECASE)
XANS_ECBASE_RE = re.compile(r"\b(?:xans-[A-Za-z0-9_-]+|ec-base-[A-Za-z0-9_-]+)\b")

BRAND_TRACE_PATTERNS: tuple[tuple[str, Pattern[str]], ...] = (
    ("MURMUR", re.compile(r"MURMUR", re.IGNORECASE)),
    ("ecudemo", re.compile(r"ecudemo", re.IGNORECASE)),
    ("401788", re.compile(r"401788")),
    ("402307", re.compile(r"402307")),
    ("ref-401788", re.compile(r"ref-401788", re.IGNORECASE)),
    ("mcp/backups", re.compile(r"mcp[\\/]+backups", re.IGNORECASE)),
    ("03_references", re.compile(r"03_references", re.IGNORECASE)),
    ("reference-intake", re.compile(r"reference-intake", re.IGNORECASE)),
    ("sftp_", re.compile(r"sftp_", re.IGNORECASE)),
    ("cafe24_config_", re.compile(r"cafe24_config_", re.IGNORECASE)),
    ("higgsfield", re.compile(r"higgsfield", re.IGNORECASE)),
    ("test1111", re.compile(r"test1111", re.IGNORECASE)),
    ("#cc785c", re.compile(r"#cc785c", re.IGNORECASE)),
    ("#a9583e", re.compile(r"#a9583e", re.IGNORECASE)),
    ("#181715", re.compile(r"#181715", re.IGNORECASE)),
)

BACKUP_RE = re.compile(r"\bbackup\b|백업", re.IGNORECASE)
ROLLBACK_RE = re.compile(r"\brollback\b|\brestore\b|\brevert\b|롤백|복구|원복|되돌리", re.IGNORECASE)
NON_DEVELOPER_RE = re.compile(
    r"비개발자|초보자?|수강생|초급|처음\s*(?:사용자|하는|시작|설치)|붙여\s*넣|복사해서",
    re.IGNORECASE,
)
SAFETY_EXPLANATION_RE = re.compile(r"안전|주의|금지|실패|정상|확인|되돌리|복구|롤백", re.IGNORECASE)

C_GROUP_PATH_PATTERNS: tuple[tuple[str, Pattern[str]], ...] = (
    (
        "order/orderform.html",
        re.compile(r"(?:^|/)order/orderform\.html$", re.IGNORECASE),
    ),
    (
        "order/order_result.html",
        re.compile(r"(?:^|/)order/order_result\.html$", re.IGNORECASE),
    ),
    (
        "order/pg_success.html",
        re.compile(r"(?:^|/)order/pg_success\.html$", re.IGNORECASE),
    ),
    (
        "order/gift_select.html",
        re.compile(r"(?:^|/)order/gift_select\.html$", re.IGNORECASE),
    ),
    (
        "myshop/order/*",
        re.compile(r"(?:^|/)myshop/order(?:/|$)", re.IGNORECASE),
    ),
    (
        "payment paths",
        re.compile(r"(?:^|/)(?:payment|payments)(?:/|$|[-_.])", re.IGNORECASE),
    ),
    (
        "PG transaction pages",
        re.compile(r"(?:^|/)(?:pg|pg_|pg-)[^/]*\.html$", re.IGNORECASE),
    ),
)


@dataclass(frozen=True)
class ScannedFile:
    path: Path
    rel: str
    text: str


@dataclass(frozen=True)
class MatchSample:
    file: str
    line: int
    text: str

    def to_json(self) -> dict[str, object]:
        return {"file": self.file, "line": self.line, "text": self.text}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_template_root() -> Path:
    return repo_root() / "agent-kit" / "clients" / "_verified-template" / "src"


def resolve_scan_root(path_arg: str | None) -> Path:
    if not path_arg:
        return default_template_root()

    raw = Path(path_arg)
    if raw.is_absolute():
        return raw

    cwd_candidate = (Path.cwd() / raw).resolve()
    if cwd_candidate.exists():
        return cwd_candidate

    return (repo_root() / raw).resolve()


def iter_text_files(root: Path) -> Iterable[ScannedFile]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if b"\x00" in raw:
            continue
        text = raw.decode("utf-8", errors="replace")
        yield ScannedFile(path=path, rel=path.relative_to(root).as_posix(), text=text)


def first_samples(
    files: Iterable[ScannedFile],
    pattern: Pattern[str],
    limit: int = 5,
) -> tuple[int, list[MatchSample]]:
    count = 0
    samples: list[MatchSample] = []
    for scanned in files:
        for line_number, line in enumerate(scanned.text.splitlines(), start=1):
            matches = list(pattern.finditer(line))
            if not matches:
                continue
            count += len(matches)
            if len(samples) < limit:
                samples.append(
                    MatchSample(
                        file=scanned.rel,
                        line=line_number,
                        text=line.strip()[:220],
                    )
                )
    return count, samples


def path_matches(files: Iterable[ScannedFile], patterns: tuple[tuple[str, Pattern[str]], ...]) -> list[dict[str, str]]:
    matches: list[dict[str, str]] = []
    for scanned in files:
        for label, pattern in patterns:
            if pattern.search(scanned.rel):
                matches.append({"file": scanned.rel, "pattern": label})
                break
    return matches


def trace_matches(files: Iterable[ScannedFile]) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for scanned in files:
        for line_number, line in enumerate(scanned.text.splitlines(), start=1):
            for label, pattern in BRAND_TRACE_PATTERNS:
                if pattern.search(line):
                    matches.append(
                        {
                            "file": scanned.rel,
                            "line": line_number,
                            "trace": label,
                            "text": line.strip()[:220],
                        }
                    )
    return matches


def files_with_both_markers(
    files: Iterable[ScannedFile],
    first_pattern: Pattern[str],
    second_pattern: Pattern[str],
    first_label: str,
    second_label: str,
    limit: int = 10,
) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for scanned in files:
        first_sample: MatchSample | None = None
        second_sample: MatchSample | None = None
        for line_number, line in enumerate(scanned.text.splitlines(), start=1):
            if first_sample is None and first_pattern.search(line):
                first_sample = MatchSample(scanned.rel, line_number, line.strip()[:220])
            if second_sample is None and second_pattern.search(line):
                second_sample = MatchSample(scanned.rel, line_number, line.strip()[:220])
            if first_sample and second_sample:
                matches.append(
                    {
                        "file": scanned.rel,
                        f"{first_label}_sample": first_sample.to_json(),
                        f"{second_label}_sample": second_sample.to_json(),
                    }
                )
                break
        if len(matches) >= limit:
            break
    return matches


def sample_json(samples: list[MatchSample]) -> list[dict[str, object]]:
    return [sample.to_json() for sample in samples]


def missing_local_resources(files: Iterable[ScannedFile], scan_root: Path) -> list[dict[str, object]]:
    missing: list[dict[str, object]] = []
    for scanned in files:
        for line_number, line in enumerate(scanned.text.splitlines(), start=1):
            for match in LOCAL_RESOURCE_DIRECTIVE_RE.finditer(line):
                raw_path = match.group("path").strip()
                if "://" in raw_path or raw_path.startswith("//"):
                    continue
                kind = match.group("kind").lower()
                normalized = raw_path.split("?", 1)[0].split("#", 1)[0].lstrip("/")
                if not normalized:
                    continue
                is_template_owned = normalized.startswith("_nk/") or kind == "layout"
                if not is_template_owned:
                    continue
                expected = scan_root / normalized
                if not expected.exists():
                    missing.append(
                        {
                            "file": scanned.rel,
                            "line": line_number,
                            "kind": kind,
                            "path": raw_path,
                            "expected": expected.relative_to(scan_root).as_posix(),
                            "text": line.strip()[:220],
                        }
                    )
    return missing


def evaluate(scan_root: Path) -> dict[str, object]:
    if not scan_root.exists():
        criteria = {key: False for key in CRITERIA_KEYS}
        return {
            "pass": False,
            "score": 0,
            "criteria": criteria,
            "blockers": [f"scan root not found: {scan_root}"],
            "evidence": [],
        }

    if not scan_root.is_dir():
        criteria = {key: False for key in CRITERIA_KEYS}
        return {
            "pass": False,
            "score": 0,
            "criteria": criteria,
            "blockers": [f"scan root is not a directory: {scan_root}"],
            "evidence": [],
        }

    files = list(iter_text_files(scan_root))
    guidance_root = scan_root.parent if scan_root.name == "src" else scan_root
    guidance_files = list(iter_text_files(guidance_root))
    criteria: dict[str, bool] = {}
    evidence: list[dict[str, object]] = []
    blockers: list[str] = []

    directive_count, directive_samples = first_samples(files, SMARTDESIGN_DIRECTIVE_RE)
    criteria["smartdesign_directives_preserved"] = directive_count > 0
    evidence.append(
        {
            "criterion": "smartdesign_directives_preserved",
            "pass": criteria["smartdesign_directives_preserved"],
            "details": f"found {directive_count} Cafe24 SmartDesign directive(s)",
            "samples": sample_json(directive_samples),
        }
    )
    if directive_count == 0:
        blockers.append("SmartDesign directives such as <!--@layout-->, <!--@import-->, <!--@css-->, or <!--@js--> were not found.")

    missing_resources = missing_local_resources(files, scan_root)
    criteria["local_smartdesign_assets_exist"] = len(missing_resources) == 0
    evidence.append(
        {
            "criterion": "local_smartdesign_assets_exist",
            "pass": criteria["local_smartdesign_assets_exist"],
            "details": "all local @layout/@import/@css/@js resources exist"
            if not missing_resources
            else f"found {len(missing_resources)} missing local SmartDesign resource(s)",
            "matches": missing_resources[:20],
        }
    )
    if missing_resources:
        blockers.append("Local SmartDesign resources referenced by @layout/@import/@css/@js must exist in the template.")

    variable_count, variable_samples = first_samples(files, CAFE24_VARIABLE_RE)
    criteria["cafe24_variables_preserved"] = variable_count > 0
    evidence.append(
        {
            "criterion": "cafe24_variables_preserved",
            "pass": criteria["cafe24_variables_preserved"],
            "details": f"found {variable_count} Cafe24 variable token(s)",
            "samples": sample_json(variable_samples),
        }
    )
    if variable_count == 0:
        blockers.append("Cafe24 variable tokens like {$mall_name} were not found.")

    module_count, module_samples = first_samples(files, MODULE_RE)
    criteria["modules_preserved"] = module_count > 0
    evidence.append(
        {
            "criterion": "modules_preserved",
            "pass": criteria["modules_preserved"],
            "details": f"found {module_count} module=\"...\" binding(s)",
            "samples": sample_json(module_samples),
        }
    )
    if module_count == 0:
        blockers.append("Cafe24 module bindings like module=\"product_listnormal\" were not found.")

    xans_count, xans_samples = first_samples(files, XANS_ECBASE_RE)
    criteria["xans_ecbase_preserved"] = xans_count > 0
    evidence.append(
        {
            "criterion": "xans_ecbase_preserved",
            "pass": criteria["xans_ecbase_preserved"],
            "details": f"found {xans_count} xans-* / ec-base-* token(s)",
            "samples": sample_json(xans_samples),
        }
    )
    if xans_count == 0:
        blockers.append("Cafe24 xans-* or ec-base-* structural hooks were not found.")

    c_group_matches = path_matches(files, C_GROUP_PATH_PATTERNS)
    criteria["order_payment_pg_excluded"] = len(c_group_matches) == 0
    evidence.append(
        {
            "criterion": "order_payment_pg_excluded",
            "pass": criteria["order_payment_pg_excluded"],
            "details": "no C-group order/payment/PG file paths found" if not c_group_matches else f"found {len(c_group_matches)} C-group path(s)",
            "matches": c_group_matches[:20],
        }
    )
    if c_group_matches:
        blockers.append("C-group order/payment/PG files are present and must stay out of the starter template.")

    backup_count, backup_samples = first_samples(guidance_files, BACKUP_RE)
    rollback_count, rollback_samples = first_samples(guidance_files, ROLLBACK_RE)
    backup_definition_files = files_with_both_markers(
        guidance_files,
        BACKUP_RE,
        ROLLBACK_RE,
        "backup",
        "rollback",
    )
    criteria["backup_and_rollback_defined"] = bool(backup_definition_files)
    evidence.append(
        {
            "criterion": "backup_and_rollback_defined",
            "pass": criteria["backup_and_rollback_defined"],
            "details": (
                f"found {backup_count} backup marker(s), {rollback_count} rollback/restore marker(s), "
                f"and {len(backup_definition_files)} file(s) containing both"
            ),
            "backup_samples": sample_json(backup_samples),
            "rollback_samples": sample_json(rollback_samples),
            "definition_files": backup_definition_files,
        }
    )
    if not backup_definition_files:
        blockers.append("Backup and rollback guidance must be defined together, not as unrelated incidental comments.")

    brand_matches = trace_matches(files)
    criteria["brand_traces_removed"] = len(brand_matches) == 0
    evidence.append(
        {
            "criterion": "brand_traces_removed",
            "pass": criteria["brand_traces_removed"],
            "details": "no blocked brand/client traces found" if not brand_matches else f"found {len(brand_matches)} blocked brand/client trace(s)",
            "matches": brand_matches[:20],
        }
    )
    if brand_matches:
        blockers.append("Brand/client traces are present: MURMUR, ecudemo, 401788, mcp/backups, 03_references, or reference-intake.")

    non_developer_count, non_developer_samples = first_samples(guidance_files, NON_DEVELOPER_RE)
    safety_count, safety_samples = first_samples(guidance_files, SAFETY_EXPLANATION_RE)
    non_developer_definition_files = files_with_both_markers(
        guidance_files,
        NON_DEVELOPER_RE,
        SAFETY_EXPLANATION_RE,
        "non_developer",
        "safety",
    )
    criteria["non_developer_safe"] = bool(non_developer_definition_files)
    evidence.append(
        {
            "criterion": "non_developer_safe",
            "pass": criteria["non_developer_safe"],
            "details": (
                f"found {non_developer_count} explicit beginner/non-developer marker(s), "
                f"{safety_count} safety explanation marker(s), and "
                f"{len(non_developer_definition_files)} file(s) containing both"
            ),
            "non_developer_samples": sample_json(non_developer_samples),
            "safety_samples": sample_json(safety_samples),
            "definition_files": non_developer_definition_files,
        }
    )
    if not non_developer_definition_files:
        blockers.append("The shipped template needs explicit beginner/non-developer safety guidance, not only developer-facing code comments.")

    passed_count = sum(1 for key in CRITERIA_KEYS if criteria.get(key))
    return {
        "pass": passed_count == len(CRITERIA_KEYS),
        "score": passed_count,
        "criteria": {key: criteria.get(key, False) for key in CRITERIA_KEYS},
        "blockers": blockers,
        "evidence": evidence,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate _verified-template/src against Cafe24 skin-safety criteria."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Optional template src path. Defaults to agent-kit/clients/_verified-template/src relative to the repo root.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    scan_root = resolve_scan_root(args.path).resolve()
    report = evaluate(scan_root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
