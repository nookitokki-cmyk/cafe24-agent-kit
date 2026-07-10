from __future__ import annotations

import json
import posixpath
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

SMARTDESIGN_DEFINE_PSEUDO = "smartdesign_define_pseudo_not_file"
CAFE24_ORDER_VIRTUAL = "cafe24_order_ec_orderform_virtual_or_inaccessible"
IDIO_MISSING_SCRIPT = "idio_referenced_script_missing_from_snapshot"
LEGACY_ROOT_SETUP_ALIAS = "legacy_root_setup_alias_missing"
CAFE24_PLATFORM_RUNTIME = "cafe24_platform_runtime_asset_not_in_skin_snapshot"
LAYOUT_INTRO_MISSING = "layout_intro_missing_from_snapshot"
MODULE_CSS_MISSING = "module_css_missing_from_snapshot"
LOCAL_REFERENCE_OK = "local_reference_ok"
OTHER_MISSING_LOCAL = "other_missing_local_reference"
EXTERNAL_REFERENCE = "external_or_absolute_platform_reference"

CRITERIA_KEYS = (
    "smartdesign_directives_found",
    "modules_found",
    "variables_found",
    "order_ec_orderform_protected",
    "smartdesign_define_not_treated_as_file",
    "multishop_module_source_of_truth",
    "idio_value_prefix_not_core_behavior",
    "missing_skin_owned_refs_reported",
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
    r"<!--\s*@([a-zA-Z_][\w-]*)(?:\((.*?)\))?\s*-->", re.IGNORECASE
)
MODULE_RE = re.compile(r"\bmodule\s*=\s*['\"]([^'\"]+)['\"]", re.IGNORECASE)
CAFE24_VARIABLE_RE = re.compile(r"\{\$[^}]+\}")
SCRIPT_SRC_RE = re.compile(
    r"<script\b[^>]*\bsrc\s*=\s*['\"]([^'\"]+)['\"][^>]*>", re.IGNORECASE
)
LINK_CSS_RE = re.compile(
    r"<link\b[^>]*\brel\s*=\s*['\"]stylesheet['\"][^>]*\bhref\s*=\s*['\"]([^'\"]+)['\"][^>]*>"
    r"|<link\b[^>]*\bhref\s*=\s*['\"]([^'\"]+)['\"][^>]*\brel\s*=\s*['\"]stylesheet['\"][^>]*>",
    re.IGNORECASE,
)
IDIO_KEY_RE = re.compile(r"IDIO\s*\[\s*(['\"])(.*?)\1\s*\]\s*=\s*(['\"])(.*?)\3\s*;")
IDIO_LOADER_PREFIX_RE = re.compile(r"keySplit\s*\[\s*0\s*\]\s*==\s*['\"]([^'\"]+)['\"]")


@dataclass(frozen=True)
class SkinFile:
    path: Path
    rel: str
    text: str
    encoding: str


@dataclass(frozen=True)
class SmartDesignDirective:
    source: str
    line: int
    kind: str
    target_raw: str
    target_norm: str


@dataclass(frozen=True)
class ModuleBinding:
    source: str
    line: int
    module: str
    text: str


@dataclass(frozen=True)
class Cafe24Variable:
    source: str
    line: int
    variable: str
    text: str


@dataclass(frozen=True)
class ReferenceEdge:
    source: str
    line: int
    edge_type: str
    target_raw: str
    target_norm: str
    exists_local: bool | None
    category: str


@dataclass(frozen=True)
class IdioSetting:
    source: str
    line: int
    key: str
    prefix: str
    element_key: str
    value: str
    target_found: bool


@dataclass(frozen=True)
class SkinAuditReport:
    root: str
    files_total: int
    text_files_total: int
    smartdesign_directives: list[SmartDesignDirective]
    modules: list[ModuleBinding]
    variables: list[Cafe24Variable]
    reference_edges: list[ReferenceEdge]
    idio_settings: list[IdioSetting]
    criteria: dict[str, bool]
    blockers: list[str]
    warnings: list[str]
    summary: dict[str, Any]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_jsonable(), ensure_ascii=False, indent=2)


def audit_skin(root: Path | str) -> SkinAuditReport:
    """Analyze a local Cafe24 SmartDesign skin root without modifying files."""
    root_path = Path(root).expanduser().resolve()
    blockers: list[str] = []
    warnings: list[str] = []

    if not root_path.exists():
        blockers.append(f"skin root not found: {root_path}")
        return _report(root_path, [], [], [], [], [], [], blockers, warnings, 0, 0)
    if not root_path.is_dir():
        blockers.append(f"skin root is not a directory: {root_path}")
        return _report(root_path, [], [], [], [], [], [], blockers, warnings, 0, 0)

    all_files = [path for path in root_path.rglob("*") if path.is_file()]
    skin_files = _read_skin_files(root_path, warnings)
    target_index = _build_target_index(skin_files)

    directives: list[SmartDesignDirective] = []
    modules: list[ModuleBinding] = []
    variables: list[Cafe24Variable] = []
    reference_edges: list[ReferenceEdge] = []
    raw_idio_settings: list[tuple[str, int, str, str, str, str]] = []
    idio_loader_prefixes: list[str] = []

    for skin_file in skin_files:
        line_starts = _line_starts(skin_file.text)
        lines = skin_file.text.splitlines()

        for match in SMARTDESIGN_DIRECTIVE_RE.finditer(skin_file.text):
            kind = f"@{match.group(1)}".lower()
            target_raw = (match.group(2) or "").strip()
            target_norm = normalize_reference(target_raw, skin_file.rel) if target_raw else ""
            line = _line_for(match.start(), line_starts)
            directives.append(SmartDesignDirective(skin_file.rel, line, kind, target_raw, target_norm))
            if kind in {"@layout", "@import", "@css", "@js", "@define"}:
                reference_edges.append(_make_edge(root_path, skin_file.rel, line, kind, target_raw))

        for match in MODULE_RE.finditer(skin_file.text):
            line = _line_for(match.start(), line_starts)
            modules.append(ModuleBinding(skin_file.rel, line, match.group(1), _line_text(lines, line)))

        for match in CAFE24_VARIABLE_RE.finditer(skin_file.text):
            line = _line_for(match.start(), line_starts)
            variables.append(Cafe24Variable(skin_file.rel, line, match.group(0), _line_text(lines, line)))

        for match in SCRIPT_SRC_RE.finditer(skin_file.text):
            target = match.group(1).strip()
            reference_edges.append(_make_edge(root_path, skin_file.rel, _line_for(match.start(), line_starts), "script_src", target))

        for match in LINK_CSS_RE.finditer(skin_file.text):
            target = (match.group(1) or match.group(2) or "").strip()
            reference_edges.append(_make_edge(root_path, skin_file.rel, _line_for(match.start(), line_starts), "link_css", target))

        for match in IDIO_KEY_RE.finditer(skin_file.text):
            key = match.group(2)
            value = match.group(4)
            prefix, element_key = _split_idio_key(key)
            raw_idio_settings.append((skin_file.rel, _line_for(match.start(), line_starts), key, prefix, element_key, value))

        for match in IDIO_LOADER_PREFIX_RE.finditer(skin_file.text):
            prefix = match.group(1)
            if prefix not in idio_loader_prefixes:
                idio_loader_prefixes.append(prefix)

    idio_settings = [
        IdioSetting(source, line, key, prefix, element_key, value, element_key in target_index)
        for source, line, key, prefix, element_key, value in raw_idio_settings
    ]

    _add_blockers(reference_edges, blockers)
    return _report(
        root_path,
        directives,
        modules,
        variables,
        reference_edges,
        idio_settings,
        idio_loader_prefixes,
        blockers,
        warnings,
        len(all_files),
        len(skin_files),
    )


def classify_reference(source: str, edge_type: str, target_norm: str, exists_local: bool | None) -> str:
    """Return the v2.13 reference category for a local or pseudo edge."""
    if edge_type == "@define":
        return SMARTDESIGN_DEFINE_PSEUDO
    if (
        "order/ec_orderform" in target_norm
        or "css/module/order/ec_orderform" in target_norm
        or "js/module/order/ec_orderform" in target_norm
    ):
        return CAFE24_ORDER_VIRTUAL
    if target_norm in {"_idio/js/footer.js", "_idio/js/bnrArea1.js"}:
        return IDIO_MISSING_SCRIPT if exists_local is False else LOCAL_REFERENCE_OK
    if target_norm == "setup.js":
        return LEGACY_ROOT_SETUP_ALIAS if exists_local is False else LOCAL_REFERENCE_OK
    if _is_cafe24_platform_runtime_asset(target_norm):
        return CAFE24_PLATFORM_RUNTIME
    if target_norm == "layout/intro/layout.html":
        return LAYOUT_INTRO_MISSING if exists_local is False else LOCAL_REFERENCE_OK
    if target_norm == "css/module/product/listrecommend.css":
        return MODULE_CSS_MISSING if exists_local is False else LOCAL_REFERENCE_OK
    if target_norm.startswith(("http://", "https://", "//", "data:", "#")):
        return EXTERNAL_REFERENCE
    if exists_local is True:
        return LOCAL_REFERENCE_OK
    return OTHER_MISSING_LOCAL



def _is_cafe24_platform_runtime_asset(target_norm: str) -> bool:
    if target_norm.startswith(("css/module/", "js/module/", "layout/basic/css/")):
        return True
    if target_norm in {"ec-js/common.js", "js/common.js", "layout/basic/js/basic.js"}:
        return True
    return target_norm in {"board/report_popup.html", "board/image_popup.html"}

def normalize_reference(ref: str, current_rel: str) -> str:
    """Normalize local SmartDesign reference paths without resolving outside the scan root."""
    cleaned = ref.strip().strip("'\"")
    if not cleaned:
        return ""
    if cleaned.startswith(("http://", "https://", "//", "data:", "#")):
        return cleaned

    cleaned = cleaned.split("#", 1)[0].split("?", 1)[0]
    cleaned = cleaned.replace("\\", "/")

    if cleaned.startswith("/"):
        candidate = cleaned.lstrip("/")
    else:
        base = posixpath.dirname(current_rel.replace("\\", "/"))
        candidate = posixpath.join(base, cleaned) if base else cleaned

    normalized = posixpath.normpath(candidate).lstrip("/")
    if normalized == ".":
        return ""
    while normalized.startswith("../"):
        normalized = normalized[3:]
    return normalized


def _read_skin_files(root_path: Path, warnings: list[str]) -> list[SkinFile]:
    files: list[SkinFile] = []
    for path in _iter_text_files(root_path):
        rel = _rel(path, root_path)
        try:
            text = path.read_text(encoding="utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            text = path.read_text(encoding="cp949", errors="replace")
            encoding = "cp949"
            warnings.append(f"decoded with cp949 fallback: {rel}")
        except OSError as exc:
            warnings.append(f"could not read {rel}: {exc}")
            continue
        files.append(SkinFile(path, rel, text, encoding))
    return files


def _build_target_index(skin_files: Iterable[SkinFile]) -> set[str]:
    targets: set[str] = set()
    for skin_file in skin_files:
        for match in re.finditer(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", skin_file.text, re.IGNORECASE):
            targets.add(match.group(1))
        for match in re.finditer(r"\bclass\s*=\s*['\"]([^'\"]+)['\"]", skin_file.text, re.IGNORECASE):
            targets.update(part for part in re.split(r"\s+", match.group(1).strip()) if part)
    return targets


def _report(
    root_path: Path,
    directives: list[SmartDesignDirective],
    modules: list[ModuleBinding],
    variables: list[Cafe24Variable],
    reference_edges: list[ReferenceEdge],
    idio_settings: list[IdioSetting],
    idio_loader_prefixes: list[str],
    blockers: list[str],
    warnings: list[str],
    files_total: int,
    text_files_total: int,
) -> SkinAuditReport:
    define_edges = [edge for edge in reference_edges if edge.edge_type == "@define"]
    order_edges = [edge for edge in reference_edges if "order/ec_orderform" in edge.target_norm]
    idio_missing_edges = [
        edge
        for edge in reference_edges
        if edge.target_norm in {"_idio/js/footer.js", "_idio/js/bnrArea1.js"}
        and edge.exists_local is False
    ]
    criteria = {
        "smartdesign_directives_found": len(directives) > 0,
        "modules_found": len(modules) > 0,
        "variables_found": len(variables) > 0,
        "order_ec_orderform_protected": all(edge.category == CAFE24_ORDER_VIRTUAL for edge in order_edges),
        "smartdesign_define_not_treated_as_file": all(edge.category == SMARTDESIGN_DEFINE_PSEUDO for edge in define_edges),
        "multishop_module_source_of_truth": any(
            module.module in {"Layout_multishopList", "Layout_multishopListitem", "Layout_multishopShipping"}
            for module in modules
        ),
        "idio_value_prefix_not_core_behavior": "value" not in idio_loader_prefixes,
        "missing_skin_owned_refs_reported": all(edge.category == IDIO_MISSING_SCRIPT for edge in idio_missing_edges),
    }
    summary = {
        "smartdesign_directives": len(directives),
        "module_occurrences": len(modules),
        "variable_occurrences": len(variables),
        "reference_edges": len(reference_edges),
        "idio_settings": len(idio_settings),
        "idio_loader_prefixes": len(idio_loader_prefixes),
        "blockers": len(blockers),
        "warnings": len(warnings),
    }
    return SkinAuditReport(
        root=str(root_path),
        files_total=files_total,
        text_files_total=text_files_total,
        smartdesign_directives=directives,
        modules=modules,
        variables=variables,
        reference_edges=reference_edges,
        idio_settings=idio_settings,
        criteria={key: criteria.get(key, False) for key in CRITERIA_KEYS},
        blockers=blockers,
        warnings=warnings,
        summary=summary,
    )


def _make_edge(root: Path, source: str, line: int, edge_type: str, target_raw: str) -> ReferenceEdge:
    target_norm = normalize_reference(target_raw, source)
    exists_local = _exists_local(root, target_norm)
    category = classify_reference(source, edge_type, target_norm, exists_local)
    return ReferenceEdge(source, line, edge_type, target_raw, target_norm, exists_local, category)


def _exists_local(root: Path, target_norm: str) -> bool | None:
    if not target_norm or target_norm.startswith(("http://", "https://", "//", "data:", "#")):
        return None
    try:
        candidate = (root / target_norm).resolve()
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate.exists()


def _add_blockers(reference_edges: list[ReferenceEdge], blockers: list[str]) -> None:
    for edge in reference_edges:
        if edge.category in {IDIO_MISSING_SCRIPT, OTHER_MISSING_LOCAL, LEGACY_ROOT_SETUP_ALIAS, LAYOUT_INTRO_MISSING, MODULE_CSS_MISSING}:
            blockers.append(f"missing local reference: {edge.source}:{edge.line} -> {edge.target_norm} ({edge.category})")


def _iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for match in re.finditer("\n", text):
        starts.append(match.end())
    return starts


def _line_for(offset: int, starts: list[int]) -> int:
    line = 1
    for idx, start in enumerate(starts, start=1):
        if start > offset:
            break
        line = idx
    return line


def _line_text(lines: list[str], line: int) -> str:
    if line <= 0 or line > len(lines):
        return ""
    return lines[line - 1].strip()


def _split_idio_key(key: str) -> tuple[str, str]:
    if "-" not in key:
        return key, ""
    prefix, element_key = key.split("-", 1)
    return prefix, element_key
