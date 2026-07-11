from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

MCP_DIR = Path(__file__).resolve().parents[1]
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))

import kit_tools


class GenerateSkinTests(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.kit_root = self.root / "agent-kit"
        self.clients_dir = self.kit_root / "clients"
        self.template_client = self.clients_dir / "_template"
        self.verified_src = self.clients_dir / "_verified-template" / "src"
        self.config_dir = self.root / "mcp-config"
        self.greenfield_templates = self.root / "greenfield-templates"

        self._make_scaffold_template()
        self._make_verified_src()
        self._make_greenfield_templates()
        self.config_dir.mkdir(parents=True)
        self._write(
            self.config_dir / "cafe24_config.example.py",
            "MALL_ID = 'your_mall_id'\nCLIENT_ID = ''\nCLIENT_SECRET = ''\n",
        )

        patchers = [
            mock.patch.object(kit_tools, "KIT_ROOT", self.kit_root),
            mock.patch.object(kit_tools, "TEMPLATE_CLIENT", self.template_client),
            mock.patch.object(kit_tools, "CONFIG_DIR", self.config_dir),
            mock.patch.object(
                kit_tools,
                "VERIFIED_TEMPLATE_SRC",
                self.verified_src,
                create=True,
            ),
            mock.patch.object(
                kit_tools,
                "GREENFIELD_TEMPLATES_DIR",
                self.greenfield_templates,
                create=True,
            ),
        ]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)

    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _make_scaffold_template(self) -> None:
        self._write(
            self.template_client / "CLAUDE.md",
            "# {클라이언트명}\n{프로젝트명}\n{YYYY-MM-DD}\n{https://...cafe24.com/skin-skinN}\n",
        )
        self._write(
            self.template_client / "01_요청사항" / "initial.md",
            "# 요청 원문\n",
        )
        self._write(self.template_client / "05_work-log.md", "scaffold log\n")

    def _make_verified_src(self) -> None:
        self._write(
            self.verified_src / "index.html",
            "<!--@layout(/layout/basic/layout.html)--><!-- verified index -->\n",
        )
        self._write(
            self.verified_src / "layout" / "basic" / "layout.html",
            "<!doctype html><html><body><!--@contents--></body></html>\n",
        )
        self._write(
            self.verified_src / "_nk" / "css" / "nk-tokens.css",
            ":root { --nk-theme-color: #111111; }\n",
        )
        self._write(
            self.verified_src / "_nk" / "js" / "nk.js",
            "window.NK = window.NK || {};\n",
        )

    def _make_greenfield_templates(self) -> None:
        self._write(
            self.greenfield_templates / "blank-slate-rebuild-queue.md",
            "mall={몰ID}\ndate={YYYY-MM-DD}\nkeep={$product_no}\n",
        )
        self._write(
            self.greenfield_templates / "wave4-page-queue.md",
            "wave4 for {몰ID}; keep {slug}\n",
        )
        self._write(
            self.greenfield_templates / "rerun-audit-spec.md",
            "rerun {YYYY-MM-DD} for {몰ID}; keep {N}\n",
        )
        self._write(
            self.greenfield_templates / "audit-overrides.example.json",
            '{"allowedMissing": [], "mall": "{몰ID}"}\n',
        )

    def _relative_files(self, root: Path) -> list[str]:
        return sorted(
            str(path.relative_to(root)).replace(os.sep, "/")
            for path in root.rglob("*")
            if path.is_file()
        )

    def _generate_skin(self, mall_id: str, **kwargs):
        generate_skin = getattr(kit_tools, "generate_skin", None)
        if generate_skin is None:
            self.fail("kit_tools.generate_skin is not implemented")
        kwargs.setdefault("templates_dir", self.greenfield_templates)
        return generate_skin(mall_id, **kwargs)

    def _client_dir(self, mall_id: str) -> Path:
        return self.clients_dir / mall_id

    def test_generate_skin_rejects_invalid_mall_id_before_creating_client(self):
        cases = [
            ("too short", "ab"),
            ("dot separator", "bad.mall"),
        ]
        for name, mall_id in cases:
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as cm:
                    self._generate_skin(mall_id)
                self.assertIn("몰 ID", str(cm.exception))
                normalized = mall_id.strip().lower()
                self.assertFalse((self.clients_dir / normalized).exists())
                self.assertFalse((self.config_dir / f"cafe24_config_{normalized}.py").exists())

    def test_generate_skin_without_design_creates_only_src_even_if_templates_are_missing(self):
        missing_templates = self.root / "missing-greenfield-templates"

        result = self._generate_skin("ecudemo123", with_design=False, templates_dir=missing_templates)
        client_dir = self._client_dir("ecudemo123")

        self.assertEqual(self._relative_files(client_dir / "src"), self._relative_files(self.verified_src))
        self.assertFalse((client_dir / "04_design").exists())
        self.assertFalse(missing_templates.exists())
        self.assertFalse(result["with_design"])
        self.assertIsNone(result["templates_dir"])
        self.assertEqual(result["design_artifacts_written"], [])
        self.assertEqual(result["design_artifacts_skipped"], [])

    def test_missing_design_templates_raise_with_no_design_guidance_before_writes(self):
        missing_templates = self.root / "missing-greenfield-templates"

        with self.assertRaises(FileNotFoundError) as cm:
            self._generate_skin("ecudemo123", templates_dir=missing_templates)

        self.assertIn("--no-design", str(cm.exception))
        self.assertFalse(self._client_dir("ecudemo123").exists())
        self.assertFalse((self.config_dir / "cafe24_config_ecudemo123.py").exists())


    def test_generate_skin_copies_verified_src_and_seeds_only_four_design_templates(self):
        result = self._generate_skin("ecudemo123")
        client_dir = self._client_dir("ecudemo123")
        src_dir = client_dir / "src"
        design_dir = client_dir / "04_design"

        self.assertEqual(self._relative_files(src_dir), self._relative_files(self.verified_src))
        self.assertEqual(
            (src_dir / "_nk" / "css" / "nk-tokens.css").read_text(encoding="utf-8"),
            (self.verified_src / "_nk" / "css" / "nk-tokens.css").read_text(encoding="utf-8"),
        )
        self.assertEqual(
            self._relative_files(design_dir),
            [
                "audit-overrides.json",
                "blank-slate-rebuild-queue.md",
                "rerun-audit-spec.md",
                "wave4-page-queue.md",
            ],
        )
        self.assertFalse((design_dir / "design.md").exists())
        self.assertFalse((design_dir / "css-module-inventory.md").exists())
        self.assertFalse((design_dir / "shots").exists())
        self.assertEqual(result["mall_id"], "ecudemo123")
        self.assertEqual(result["files_copied"], len(self._relative_files(self.verified_src)))
        self.assertTrue(result["client_bootstrapped"])
        self.assertEqual(
            sorted(result["design_artifacts_written"]),
            [
                "04_design/audit-overrides.json",
                "04_design/blank-slate-rebuild-queue.md",
                "04_design/rerun-audit-spec.md",
                "04_design/wave4-page-queue.md",
            ],
        )

    def test_design_template_seeding_replaces_only_mall_and_date_placeholders(self):
        self._generate_skin("ecudemo123")
        design_dir = self._client_dir("ecudemo123") / "04_design"
        today = date.today().isoformat()

        blank = (design_dir / "blank-slate-rebuild-queue.md").read_text(encoding="utf-8")
        rerun = (design_dir / "rerun-audit-spec.md").read_text(encoding="utf-8")
        wave4 = (design_dir / "wave4-page-queue.md").read_text(encoding="utf-8")
        overrides = json.loads((design_dir / "audit-overrides.json").read_text(encoding="utf-8"))

        self.assertIn("mall=ecudemo123", blank)
        self.assertIn(f"date={today}", blank)
        self.assertIn("keep={$product_no}", blank)
        self.assertIn(f"rerun {today} for ecudemo123", rerun)
        self.assertIn("keep {N}", rerun)
        self.assertIn("keep {slug}", wave4)
        self.assertEqual(overrides, {"allowedMissing": [], "mall": "{몰ID}"})

    def test_existing_src_without_overwrite_raises_and_preserves_everything(self):
        client_dir = self._client_dir("ecudemo123")
        self._write(client_dir / "src" / "custom.html", "user custom src\n")
        self._write(client_dir / "05_work-log.md", "user log\n")

        with self.assertRaises(FileExistsError):
            self._generate_skin("ecudemo123")

        self.assertEqual((client_dir / "src" / "custom.html").read_text(encoding="utf-8"), "user custom src\n")
        self.assertEqual((client_dir / "05_work-log.md").read_text(encoding="utf-8"), "user log\n")
        self.assertFalse((client_dir / "04_design").exists())
        self.assertFalse((client_dir / "backups").exists())

    def test_overwrite_moves_existing_src_to_backup_before_replacing_it(self):
        client_dir = self._client_dir("ecudemo123")
        self._write(client_dir / "src" / "custom.html", "old src\n")
        self._write(client_dir / "04_design" / "design.md", "human-authored design\n")
        self._write(client_dir / "04_design" / "wave4-page-queue.md", "user queue\n")

        result = self._generate_skin("ecudemo123", overwrite=True)
        backup_dir = Path(result["backup_dir"])

        self.assertTrue(backup_dir.is_dir())
        self.assertEqual((backup_dir / "src" / "custom.html").read_text(encoding="utf-8"), "old src\n")
        self.assertFalse((client_dir / "src" / "custom.html").exists())
        self.assertEqual(self._relative_files(client_dir / "src"), self._relative_files(self.verified_src))
        self.assertEqual(
            (client_dir / "04_design" / "design.md").read_text(encoding="utf-8"),
            "human-authored design\n",
        )
        self.assertEqual(
            (client_dir / "04_design" / "wave4-page-queue.md").read_text(encoding="utf-8"),
            "user queue\n",
        )
        self.assertIn("04_design/wave4-page-queue.md", result["design_artifacts_skipped"])
        self.assertTrue(str(backup_dir).startswith(str(client_dir / "backups")))

    def test_existing_client_without_design_folder_gets_design_seed_without_scaffold(self):
        client_dir = self._client_dir("ecudemo123")
        self._write(client_dir / "05_work-log.md", "existing client notes\n")

        result = self._generate_skin("ecudemo123")

        self.assertFalse(result["client_bootstrapped"])
        self.assertEqual((client_dir / "05_work-log.md").read_text(encoding="utf-8"), "existing client notes\n")
        self.assertEqual(
            self._relative_files(client_dir / "04_design"),
            [
                "audit-overrides.json",
                "blank-slate-rebuild-queue.md",
                "rerun-audit-spec.md",
                "wave4-page-queue.md",
            ],
        )
        self.assertEqual(self._relative_files(client_dir / "src"), self._relative_files(self.verified_src))

    def test_dry_run_reports_plan_without_creating_client_config_or_design_files(self):
        result = self._generate_skin("ecudemo123", dry_run=True)

        self.assertFalse(self._client_dir("ecudemo123").exists())
        self.assertFalse((self.config_dir / "cafe24_config_ecudemo123.py").exists())
        self.assertTrue(result["dry_run"])
        self.assertTrue(result["would_bootstrap"])
        self.assertEqual(result["planned_files"], len(self._relative_files(self.verified_src)))
        self.assertFalse(result["src_exists"])
        self.assertFalse(result["would_overwrite"])
        self.assertEqual(
            sorted(result["design_artifacts_to_seed"]),
            [
                "04_design/audit-overrides.json",
                "04_design/blank-slate-rebuild-queue.md",
                "04_design/rerun-audit-spec.md",
                "04_design/wave4-page-queue.md",
            ],
        )

    def _run_cli(self, *args: str, env_overrides: dict[str, str] | None = None):
        env = os.environ.copy()
        env.update(
            {
                "CAFE24_KIT_ROOT": str(self.kit_root),
                "CAFE24_GREENFIELD_TEMPLATES": str(self.greenfield_templates),
                "PYTHONIOENCODING": "utf-8",
            }
        )
        if env_overrides:
            env.update(env_overrides)
        return subprocess.run(
            [sys.executable, "cli.py", *args],
            cwd=MCP_DIR,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_cli_skin_generate_dry_run_requires_explicit_non_demo_mall(self):
        cases = [
            ("missing --mall", ["skin-generate", "--dry-run"]),
            ("demo mall", ["skin-generate", "--mall", "demo000", "--dry-run"]),
        ]
        for name, args in cases:
            with self.subTest(name=name):
                completed = self._run_cli(*args)
                self.assertEqual(completed.returncode, 1)
                self.assertIn("--mall", completed.stderr)
                self.assertIn("demo000", completed.stderr)
                self.assertFalse((self.clients_dir / "demo000").exists())

    def test_cli_skin_generate_dry_run_outputs_json_plan_and_performs_no_writes(self):
        completed = self._run_cli("skin-generate", "--mall", "ecudemo123", "--dry-run")

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["mall_id"], "ecudemo123")
        self.assertTrue(payload["dry_run"])
        self.assertEqual(payload["planned_files"], len(self._relative_files(self.verified_src)))
        self.assertFalse(self._client_dir("ecudemo123").exists())

    def test_cli_skin_generate_no_design_creates_src_without_design_seed_or_template_lookup(self):
        mall_id = "ecudemo124"
        self._client_dir(mall_id).mkdir(parents=True)
        missing_templates = self.root / "missing-greenfield-templates"

        completed = self._run_cli(
            "skin-generate",
            "--mall",
            mall_id,
            "--no-design",
            env_overrides={"CAFE24_GREENFIELD_TEMPLATES": str(missing_templates)},
        )

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        payload = json.loads(completed.stdout)
        client_dir = self._client_dir(mall_id)
        self.assertEqual(payload["mall_id"], mall_id)
        self.assertFalse(payload["dry_run"])
        self.assertFalse(payload["with_design"])
        self.assertIsNone(payload["templates_dir"])
        self.assertEqual(payload["design_artifacts_written"], [])
        self.assertEqual(payload["design_artifacts_skipped"], [])
        self.assertEqual(self._relative_files(client_dir / "src"), self._relative_files(self.verified_src))
        self.assertFalse((client_dir / "04_design").exists())
        self.assertFalse(missing_templates.exists())

    def test_cli_skin_generate_real_run_creates_src_in_isolated_kit_root_and_returns_json(self):
        mall_id = "ecudemo125"
        self._client_dir(mall_id).mkdir(parents=True)

        completed = self._run_cli("skin-generate", "--mall", mall_id)

        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
        payload = json.loads(completed.stdout)
        client_dir = self._client_dir(mall_id)
        self.assertEqual(payload["mall_id"], mall_id)
        self.assertFalse(payload["dry_run"])
        self.assertEqual(Path(payload["skin_dir"]), client_dir / "src")
        self.assertEqual(payload["files_copied"], len(self._relative_files(self.verified_src)))
        self.assertEqual(self._relative_files(client_dir / "src"), self._relative_files(self.verified_src))
        self.assertEqual(
            sorted(payload["design_artifacts_written"]),
            [
                "04_design/audit-overrides.json",
                "04_design/blank-slate-rebuild-queue.md",
                "04_design/rerun-audit-spec.md",
                "04_design/wave4-page-queue.md",
            ],
        )


if __name__ == "__main__":
    unittest.main()
