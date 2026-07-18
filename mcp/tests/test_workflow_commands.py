from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MCP_DIR = Path(__file__).resolve().parents[1]
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))

import kit_tools


class WorkflowCommandTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.kit_root = self.root / "agent-kit"
        self.clients_dir = self.kit_root / "clients"
        self.clients_dir.mkdir(parents=True)
        patcher = mock.patch.object(kit_tools, "KIT_ROOT", self.kit_root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _run_cli(self, *args: str):
        env = os.environ.copy()
        env.update({"CAFE24_KIT_ROOT": str(self.kit_root), "PYTHONIOENCODING": "utf-8"})
        return subprocess.run(
            [sys.executable, "cli.py", *args],
            cwd=MCP_DIR,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def _workflow(self, mall_id: str, *, client: str, updated: str, current: str, next_action: str) -> None:
        self._write(
            self.clients_dir / mall_id / ".workflow.md",
            f"""# 워크플로우 진행 상태

## 메타
- 클라: {client}
- 작업: {mall_id} 카페24 작업
- 워크플로우: skin-build-standard
- 마지막 업데이트: {updated}

## 진행 단계

| 단계 | 상태 | 시작 | 완료 | 산출물 |
|---|---|---|---|---|
| ① 분석 | ✅ 완료 | 10:00 | 10:10 | 04_design/analysis.md |
| ② 세팅 | {current} | 10:10 | - | src/_nk/css/nk-tokens.css |
| ③ 검증 | ⏳ 대기 | - | - | - |

## 다음 액션

- {next_action}
""",
        )

    def test_build_workspace_index_scans_workflow_files_without_touching_sources(self):
        self._workflow(
            "ecudemo111",
            client="모던세라믹",
            updated="2026-07-11T10:00:00+09:00",
            current="🔄 진행 중",
            next_action="/토대정리 후 /검증",
        )
        self._workflow(
            "ecudemo222",
            client="슬로우에이징스",
            updated="2026-07-10T18:00:00+09:00",
            current="❌ 실패",
            next_action="/검증 재실행",
        )
        self._write(self.clients_dir / "_template" / ".workflow.md", "# ignore template\n")
        self._workflow(
            ".hidden",
            client="숨김폴더",
            updated="2026-07-11T11:00:00+09:00",
            current="🔄 진행 중",
            next_action="숨김 폴더는 제외",
        )
        before = (self.clients_dir / "ecudemo111" / ".workflow.md").read_text(encoding="utf-8")

        payload = kit_tools.build_workspace_index(write=True)

        self.assertEqual(payload["source_of_truth"], ".workflow.md")
        self.assertTrue(payload["derived"])
        self.assertEqual([w["mall_id"] for w in payload["workspaces"]], ["ecudemo111", "ecudemo222"])
        self.assertEqual(payload["workspaces"][0]["client_name"], "모던세라믹")
        self.assertEqual(payload["workspaces"][0]["current_status"], "🔄 진행 중")
        self.assertEqual(payload["workspaces"][0]["next_action"], "/토대정리 후 /검증")
        self.assertTrue((self.clients_dir / ".workspace-index.json").is_file())
        self.assertEqual((self.clients_dir / "ecudemo111" / ".workflow.md").read_text(encoding="utf-8"), before)

    def test_build_workspace_index_reconstructs_minimal_status_when_workflow_missing(self):
        self._write(self.clients_dir / "ecudemo333" / "src" / "index.html", "<!--@layout(/layout/basic/layout.html)-->")
        self._write(self.clients_dir / "ecudemo333" / "04_design" / "blank-slate-rebuild-queue.md", "queue")

        payload = kit_tools.build_workspace_index(write=False)

        self.assertEqual(payload["workspaces"][0]["mall_id"], "ecudemo333")
        self.assertEqual(payload["workspaces"][0]["current_status"], "스킨 생성됨")
        self.assertEqual(payload["workspaces"][0]["next_action"], "/접속세팅 또는 /토대정리")
        self.assertFalse((self.clients_dir / ".workspace-index.json").exists())

    def test_prepare_upload_blocks_when_skin_audit_has_blockers(self):
        self._write(self.clients_dir / "ecudemo444" / "src" / "index.html", "broken")
        audit_payload = {"blockers": ["missing SmartDesign directive"], "warnings": []}

        result = kit_tools.prepare_upload_plan("ecudemo444", audit_payload=audit_payload, remote_root="/skin1")

        self.assertFalse(result["upload_allowed"])
        self.assertEqual(result["status"], "blocked")
        self.assertIn("skin-audit", result["reason"])
        self.assertFalse((self.clients_dir / "ecudemo444" / "upload-manifest.json").exists())

    def test_prepare_upload_blocks_when_skin_audit_criteria_failed(self):
        self._write(self.clients_dir / "ecudemo445" / "src" / "index.html", "broken")
        audit_payload = {"blockers": [], "criteria": {"c_group_excluded": False}}

        result = kit_tools.prepare_upload_plan("ecudemo445", audit_payload=audit_payload, remote_root="/skin1")

        self.assertFalse(result["upload_allowed"])
        self.assertEqual(result["status"], "blocked")
        self.assertFalse((self.clients_dir / "ecudemo445" / "upload-manifest.json").exists())

    def test_prepare_upload_writes_manifest_but_never_approves_or_uploads(self):
        self._write(self.clients_dir / "ecudemo555" / "src" / "index.html", "ok")
        self._write(self.clients_dir / "ecudemo555" / "src" / "_nk" / "css" / "nk-base.css", "css")
        self._write(self.clients_dir / "ecudemo555" / "src" / "order" / "ec_orderform" / "index.html", "protected")
        audit_payload = {"blockers": [], "warnings": []}

        result = kit_tools.prepare_upload_plan("ecudemo555", audit_payload=audit_payload, remote_root="/skin1")

        self.assertTrue(result["upload_allowed"])
        self.assertEqual(result["status"], "ready_for_approval")
        self.assertTrue(result["requires_approval"])
        self.assertFalse(result["approved"])
        self.assertFalse(result["will_upload_now"])
        self.assertEqual(
            result["files"],
            [
                {"local": "src/_nk/css/nk-base.css", "remote": "/skin1/_nk/css/nk-base.css", "backup_required": True},
                {"local": "src/index.html", "remote": "/skin1/index.html", "backup_required": True},
            ],
        )
        manifest = json.loads((self.clients_dir / "ecudemo555" / "upload-manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["approved"])
        self.assertEqual(manifest["files"], result["files"])


    def test_cli_workspace_list_outputs_json_and_writes_derived_index(self):
        self._workflow(
            "ecudemo666",
            client="목록테스트",
            updated="2026-07-11T12:00:00+09:00",
            current="🔄 진행 중",
            next_action="/검증",
        )

        completed = self._run_cli("workspace-list")

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["source_of_truth"], ".workflow.md")
        self.assertTrue(payload["derived"])
        self.assertEqual(payload["workspaces"][0]["mall_id"], "ecudemo666")
        self.assertTrue((self.clients_dir / ".workspace-index.json").is_file())

    def test_cli_upload_prepare_requires_explicit_non_demo_mall(self):
        completed = self._run_cli("upload-prepare", "--remote-root", "/skin1")

        self.assertEqual(completed.returncode, 1)
        self.assertIn("--mall", completed.stderr)
        self.assertIn("demo000", completed.stderr)


if __name__ == "__main__":
    unittest.main()
