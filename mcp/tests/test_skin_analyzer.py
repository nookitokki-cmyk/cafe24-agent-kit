from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

MCP_DIR = Path(__file__).resolve().parents[1]
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))

from skin_analyzer import audit_skin, classify_reference, normalize_reference


class SkinAnalyzerTests(unittest.TestCase):
    def make_skin(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)

        (root / "_idio/js").mkdir(parents=True)
        (root / "_idio/inc").mkdir(parents=True)
        (root / "layout/basic").mkdir(parents=True)
        (root / "order").mkdir(parents=True)

        (root / "index.html").write_text(
            """
<!--@layout(/layout/basic/layout.html)-->
<!--@import(/_idio/inc/footer.html)-->
<!--@define(cmc_log)-->
<section module="product_listmain_1">
  <a href="/product/detail.html{$param}">{$product_name}</a>
</section>
""".strip(),
            encoding="utf-8",
        )
        (root / "_idio/js/setup.js").write_text(
            """
var IDIO = {};
IDIO['class-mshop'] = 'on';
IDIO['value-mshop-kor'] = '/index.html';
IDIO['href-f1'] = 'https://instagram.com/';
""".strip(),
            encoding="utf-8",
        )
        (root / "_idio/js/idio.js").write_text(
            """
if(keySplit[0]=='text'){}
if(keySplit[0]=='class'){}
if(keySplit[0]=='href'){}
""".strip(),
            encoding="utf-8",
        )
        (root / "_idio/inc/footer.html").write_text(
            """
<!--@js(/_idio/js/footer.js)-->
<div class="bt_mshop" module="Layout_multishopList">
  <button type="button"><span>{$current_language}</span></button>
  <ul module="Layout_multishopListitem">
    <li class="{$selected_class}"><a href="//{$shop_domain}/">{$locale_language}</a></li>
  </ul>
</div>
""".strip(),
            encoding="utf-8",
        )
        (root / "layout/basic/layout.html").write_text(
            """
<!doctype html>
<html><body>
<!--@contents-->
<div module="Layout_multishopShipping">
  <!--@css(/css/module/layout/multishopShipping.css)-->
  <!--@js(/js/module/layout/multishopShipping.js)-->
  <select module="Layout_multishopShippingCountrylist"><option>{$country_name}</option></select>
</div>
</body></html>
""".strip(),
            encoding="utf-8",
        )
        (root / "order/orderform.html").write_text(
            """
<!--@css(/css/module/order/ec_orderform/form_onetouch.css)-->
<!--@import(/order/ec_orderform/header.html)-->
<div module="Order_form">{$form.order_name}</div>
""".strip(),
            encoding="utf-8",
        )
        return root

    def test_normalize_reference_resolves_skin_absolute_and_relative_paths(self):
        cases = [
            (
                "absolute skin path",
                "/_idio/js/footer.js",
                "_idio/inc/footer.html",
                "_idio/js/footer.js",
            ),
            (
                "relative sibling path",
                "../js/footer.js",
                "_idio/inc/footer.html",
                "_idio/js/footer.js",
            ),
        ]

        for name, ref, current_rel, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(normalize_reference(ref, current_rel), expected)

    def test_classify_reference_treats_define_as_pseudo_edge_not_file_lookup(self):
        self.assertEqual(
            classify_reference("index.html", "@define", "cmc_log", False),
            "smartdesign_define_pseudo_not_file",
        )

    def test_classify_reference_protects_order_form_virtual_assets(self):
        cases = [
            "order/ec_orderform/header.html",
            "css/module/order/ec_orderform/form_onetouch.css",
            "js/module/order/ec_orderform/order.js",
        ]

        for target_norm in cases:
            with self.subTest(target_norm=target_norm):
                self.assertEqual(
                    classify_reference("order/orderform.html", "@import", target_norm, False),
                    "cafe24_order_ec_orderform_virtual_or_inaccessible",
                )


    def test_classify_reference_treats_cafe24_platform_assets_as_runtime_not_blockers(self):
        cases = [
            "layout/basic/css/common.css",
            "layout/basic/css/layout.css",
            "css/module/layout/multishopShipping.css",
            "js/module/layout/category.js",
            "js/module/layout/multishopShipping.js",
            "js/common.js",
            "layout/basic/js/basic.js",
            "board/report_popup.html",
            "board/image_popup.html",
        ]

        for target_norm in cases:
            with self.subTest(target_norm=target_norm):
                self.assertEqual(
                    classify_reference("layout/basic/layout.html", "@css", target_norm, False),
                    "cafe24_platform_runtime_asset_not_in_skin_snapshot",
                )


    def test_report_schema_matches_batch4_public_contract(self):
        data = audit_skin(self.make_skin()).to_jsonable()

        self.assertEqual(
            set(data["smartdesign_directives"][0]),
            {"source", "line", "kind", "target_raw", "target_norm"},
        )
        self.assertEqual(
            set(data["modules"][0]),
            {"source", "line", "module", "text"},
        )
        self.assertEqual(
            set(data["variables"][0]),
            {"source", "line", "variable", "text"},
        )
        self.assertEqual(
            set(data["idio_settings"][0]),
            {"source", "line", "key", "prefix", "element_key", "value", "target_found"},
        )
        self.assertEqual(
            set(data["reference_edges"][0]),
            {"source", "line", "edge_type", "target_raw", "target_norm", "exists_local", "category"},
        )
    def test_audit_skin_counts_core_smartdesign_constructs_and_classifies_edges(self):
        report = audit_skin(self.make_skin())
        data = report.to_jsonable()

        self.assertEqual(data["summary"]["smartdesign_directives"], 9)
        self.assertEqual(data["summary"]["module_occurrences"], 6)
        self.assertEqual(data["summary"]["variable_occurrences"], 8)

        expected_true_criteria = {
            "smartdesign_directives_found",
            "modules_found",
            "variables_found",
            "order_ec_orderform_protected",
            "smartdesign_define_not_treated_as_file",
            "multishop_module_source_of_truth",
            "idio_value_prefix_not_core_behavior",
            "missing_skin_owned_refs_reported",
        }
        for key in expected_true_criteria:
            with self.subTest(criteria=key):
                self.assertTrue(data["criteria"][key])

        modules = {module["module"] for module in data["modules"]}
        self.assertTrue(
            {"Layout_multishopList", "Layout_multishopListitem", "Layout_multishopShipping"}.issubset(modules)
        )

        edges_by_category = {}
        for edge in data["reference_edges"]:
            edges_by_category.setdefault(edge["category"], set()).add(edge["target_norm"])

        self.assertIn(
            "_idio/js/footer.js",
            edges_by_category["idio_referenced_script_missing_from_snapshot"],
        )
        self.assertIn(
            "order/ec_orderform/header.html",
            edges_by_category["cafe24_order_ec_orderform_virtual_or_inaccessible"],
        )
        self.assertIn(
            "css/module/order/ec_orderform/form_onetouch.css",
            edges_by_category["cafe24_order_ec_orderform_virtual_or_inaccessible"],
        )
        self.assertIn(
            "cmc_log",
            edges_by_category["smartdesign_define_pseudo_not_file"],
        )

    def test_report_payload_is_json_serializable_without_losing_semantic_content(self):
        report = audit_skin(self.make_skin())
        encoded = json.dumps(report.to_jsonable(), ensure_ascii=False, sort_keys=True)
        decoded = json.loads(encoded)

        self.assertIsInstance(decoded["root"], str)
        self.assertIn(
            "Layout_multishopList",
            {module["module"] for module in decoded["modules"]},
        )
        self.assertIn(
            "idio_referenced_script_missing_from_snapshot",
            {edge["category"] for edge in decoded["reference_edges"]},
        )


if __name__ == "__main__":
    unittest.main()
