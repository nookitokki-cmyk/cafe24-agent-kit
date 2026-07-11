# NK Esthe-style Easy Compatible Skin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the verified Cafe24 template into an Esthe/IDIO-style NK system with `inc` partials, `setup.html`, SmartDesignEasy metadata, NK CSS/JS layers, and distribution verification.

**Architecture:** Preserve the existing `_verified-template` safety baseline, then add an NK compatibility layer: `setup.html` feeds `NK_CONFIG`, `_nk/inc/common.html` loads tokens/assets/scripts, section partials carry both `nk-*` classes and `data-ez-*` metadata, and contract tests plus dist scripts guard forbidden Esthe namespaces. Do not copy Esthe source code or assets; reproduce the operating model with NK names and verified Cafe24 directives.

**Tech Stack:** Cafe24 SmartDesign HTML directives, SmartDesignEasy `data-ez-*` metadata, XHTML-compatible HTML, CSS custom properties, Vanilla JavaScript with safe jQuery fallback, Python `unittest`, Bash dist verification.

---

## File Structure and Responsibilities

### Create

- `agent-kit/clients/_verified-template/src/setup.html` — non-developer configuration surface exposing `window.NK_CONFIG`.
- `agent-kit/clients/_verified-template/src/ez/ez-module.html` — SmartDesignEasy module metadata contract.
- `agent-kit/clients/_verified-template/src/_nk/inc/common.html` — common loader for Pretendard, Phosphor, Swiper, NK CSS/JS, and `setup.html`.
- `agent-kit/clients/_verified-template/src/_nk/inc/main-hero.html` — Easy-compatible hero section.
- `agent-kit/clients/_verified-template/src/_nk/inc/product-list.html` — Easy-compatible product grid section.
- `agent-kit/clients/_verified-template/src/_nk/inc/product-slide.html` — Easy-compatible product slider section.
- `agent-kit/clients/_verified-template/src/_nk/inc/image-gallery.html` — Easy-compatible image gallery section.
- `agent-kit/clients/_verified-template/src/_nk/css/nk-ez.css` — Easy metadata/editor-safe presentation layer.
- `agent-kit/clients/_verified-template/src/_nk/css/nk-responsive.css` — 390/768/1440/1920 responsive contract layer.
- `agent-kit/clients/_verified-template/src/_nk/js/nk-config.js` — config defaults and safe config getter.
- `agent-kit/clients/_verified-template/src/_nk/js/nk-core.js` — config-driven visibility/link/text application.
- `agent-kit/clients/_verified-template/src/_nk/js/nk-slider.js` — Swiper bootstrapping for NK sections.
- `agent-kit/clients/_verified-template/src/_nk/js/nk-ez-adapter.js` — Easy metadata class synchronization without requiring Easy.
- `mcp/tests/test_verified_template_contract.py` — repo-level contract tests for the verified template.

### Modify

- `agent-kit/clients/_verified-template/src/layout/basic/layout.html` — import `/_nk/inc/common.html`; remove duplicate font/icon/CSS/JS lines that common now owns while preserving Cafe24 base CSS and body scope.
- `agent-kit/clients/_verified-template/src/layout/basic/main.html` — import `/_nk/inc/common.html`; replace inline main sections with `/_nk/inc/main-hero.html`, `product-list.html`, `product-slide.html`, and `image-gallery.html` imports.
- `agent-kit/clients/_verified-template/src/_nk/css/nk-tokens.css` — add missing Esthe-style flat NK tokens used by new files without changing existing token names.
- `agent-kit/clients/_verified-template/src/_nk/css/nk-main.css` — keep existing visual styles, add section styles for new partial class names if not covered.
- `agent-kit/clients/_verified-template/README.md` — update file count, folder map, and editing instructions for `setup.html` and Easy metadata.
- `scripts/build-dist-kit.sh` — add new required files to post-build sanity checks.
- `scripts/verify-kit.sh` — add verified-template checks for `setup.html`, `ez/ez-module.html`, Easy attributes, NK scripts, and forbidden Esthe namespaces.
- `mcp/tests/test_generate_skin.py` — extend fixture contract so `generate_skin` copy tests include Esthe-style/Easy files.
- `CHANGELOG.md` — add unreleased entry for NK Esthe-style Easy-compatible template.

### Do Not Modify

- `agent-kit/clients/_verified-template/src/order/ec_orderform/**` — protected order/payment surface remains excluded.
- Any live client folder under `agent-kit/clients/ecudemo*` — implementation targets `_verified-template` only.
- Esthe research snapshot under `.omc/research/**` — read-only reference only.

---

### Task 1: Add Failing Verified Template Contract Tests

**Files:**
- Create: `mcp/tests/test_verified_template_contract.py`

- [ ] **Step 1: Create the contract test file**

Write `mcp/tests/test_verified_template_contract.py` with this complete content:

```python
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "agent-kit" / "clients" / "_verified-template" / "src"


class VerifiedTemplateContractTests(unittest.TestCase):
    maxDiff = None

    def read_rel(self, rel: str) -> str:
        return (SRC / rel).read_text(encoding="utf-8")

    def test_esthe_style_easy_contract_files_exist(self):
        required = [
            "setup.html",
            "ez/ez-module.html",
            "_nk/inc/common.html",
            "_nk/inc/main-hero.html",
            "_nk/inc/product-list.html",
            "_nk/inc/product-slide.html",
            "_nk/inc/image-gallery.html",
            "_nk/css/nk-ez.css",
            "_nk/css/nk-responsive.css",
            "_nk/js/nk-config.js",
            "_nk/js/nk-core.js",
            "_nk/js/nk-slider.js",
            "_nk/js/nk-ez-adapter.js",
        ]
        missing = [rel for rel in required if not (SRC / rel).is_file()]
        self.assertEqual(missing, [])

    def test_easy_metadata_contract_is_present(self):
        ez = self.read_rel("ez/ez-module.html")
        for token in (
            "data-ez-module",
            "data-ez-layout",
            "data-ez-role",
            "data-ez-holder",
            "ez-prop",
            "ez-var",
            "ez-item",
        ):
            self.assertIn(token, ez)
        self.assertIn('data-ez-module="product-list/1"', ez)
        self.assertIn('data-ez-module="image-gallery/2"', ez)

    def test_nk_namespace_replaces_esthe_namespace(self):
        forbidden = (
            "_idio",
            "IDIO[",
            "--idio-",
            "Font Awesome",
            "fontawesome",
            "fa-regular",
            "fa-solid",
            "font-style: italic",
            "font-style: oblique",
        )
        offenders: list[str] = []
        for path in SRC.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                if token in text:
                    offenders.append(f"{path.relative_to(SRC).as_posix()} contains {token}")
        self.assertEqual(offenders, [])

    def test_common_loader_owns_config_and_assets(self):
        common = self.read_rel("_nk/inc/common.html")
        self.assertIn("Pretendard", common)
        self.assertIn("phosphor-icons", common)
        self.assertIn("swiper", common.lower())
        self.assertIn("<!--@import(/setup.html)-->", common)
        self.assertIn("<!--@css(/_nk/css/nk-ez.css)-->", common)
        self.assertIn("<!--@js(/_nk/js/nk-config.js)-->", common)
        self.assertIn("<!--@js(/_nk/js/nk-core.js)-->", common)

    def test_layouts_import_common_loader_once(self):
        layout = self.read_rel("layout/basic/layout.html")
        main = self.read_rel("layout/basic/main.html")
        self.assertEqual(layout.count("<!--@import(/_nk/inc/common.html)-->") , 1)
        self.assertEqual(main.count("<!--@import(/_nk/inc/common.html)-->") , 1)
        self.assertIn('class="nk-skin', layout)
        self.assertIn('class="nk-skin nk-main', main)

    def test_setup_exposes_documented_config_keys(self):
        setup = self.read_rel("setup.html")
        for key in (
            "window.NK_CONFIG",
            "showTopBanner",
            "showPopup",
            "showMainHero",
            "showNewProducts",
            "showBestProducts",
            "showImageGallery",
            "kakaoChannelUrl",
            "naverTalkUrl",
            "youtubeUrl",
            "escrowUrl",
        ):
            self.assertIn(key, setup)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new contract tests and verify they fail**

Run:

```bash
python -m unittest discover -s mcp/tests -p "test_verified_template_contract.py" -v
```

Expected: FAIL because `setup.html`, `ez/ez-module.html`, `_nk/inc/common.html`, and new NK JS/CSS files do not exist yet.

- [ ] **Step 3: Commit the failing contract test**

Run:

```bash
git add mcp/tests/test_verified_template_contract.py
git commit -m "test: add verified template easy contract"
```

---

### Task 2: Add `setup.html` and Common Loader

**Files:**
- Create: `agent-kit/clients/_verified-template/src/setup.html`
- Create: `agent-kit/clients/_verified-template/src/_nk/inc/common.html`
- Modify: `agent-kit/clients/_verified-template/src/layout/basic/layout.html`
- Modify: `agent-kit/clients/_verified-template/src/layout/basic/main.html`

- [ ] **Step 1: Create `setup.html`**

Write `agent-kit/clients/_verified-template/src/setup.html`:

```html
<script>
/*
  누끼토끼 카페24 스킨 설정 파일입니다.
  아래 true/false 또는 URL 값만 바꾸면 주요 영역을 켜고 끌 수 있습니다.
  CSS 클래스와 module="..." 속성은 수정하지 마세요.
*/
window.NK_CONFIG = {
  showTopBanner: true,
  showPopup: false,
  showMainHero: true,
  showNewProducts: true,
  showBestProducts: true,
  showCategoryTabs: true,
  showImageGallery: true,
  showVideo: false,
  showMap: false,
  showReview: true,
  showInstagram: false,
  kakaoChannelUrl: "",
  naverTalkUrl: "",
  youtubeUrl: "",
  escrowUrl: ""
};
</script>
```

- [ ] **Step 2: Create `_nk/inc/common.html`**

Write `agent-kit/clients/_verified-template/src/_nk/inc/common.html`:

```html
<!-- ============================================================
     NK 공통 로더
     - Pretendard, Phosphor Icons, Swiper, NK CSS/JS를 한 곳에서 로드합니다.
     - setup.html은 비개발자 설정 파일입니다.
     - 이 파일은 layout/basic/layout.html과 layout/basic/main.html에서 1회 import합니다.
     ============================================================ -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/regular/style.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/fill/style.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />

<!--@css(/_nk/css/nk-tokens.css)-->
<!--@css(/_nk/css/nk-cafe24-reset.css)-->
<!--@css(/_nk/css/nk-base.css)-->
<!--@css(/_nk/css/nk-components.css)-->
<!--@css(/_nk/css/nk-stock.css)-->
<!--@css(/_nk/css/nk-ez.css)-->
<!--@css(/_nk/css/nk-responsive.css)-->

<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
<!--@import(/setup.html)-->
<!--@js(/_nk/js/nk-config.js)-->
<!--@js(/_nk/js/nk-core.js)-->
<!--@js(/_nk/js/nk-slider.js)-->
<!--@js(/_nk/js/nk-ez-adapter.js)-->
```

- [ ] **Step 3: Update `layout/basic/layout.html` head loader**

In `agent-kit/clients/_verified-template/src/layout/basic/layout.html`, replace lines 27-40 with:

```html
    <!-- NK 공통 로더: Pretendard + Phosphor + 토큰 + reset + stock + Easy 호환 + setup.html -->
    <!--@import(/_nk/inc/common.html)-->
```

Keep lines 14-25 Cafe24 base CSS and lines 41-44 Cafe24 JS.

- [ ] **Step 4: Update `layout/basic/main.html` head loader**

In `agent-kit/clients/_verified-template/src/layout/basic/main.html`, replace lines 27-37 with:

```html
    <!-- NK 공통 로더: Pretendard + Phosphor + 토큰 + reset + Easy 호환 + setup.html -->
    <!--@import(/_nk/inc/common.html)-->
    <!--@css(/_nk/css/nk-main.css)--><!-- 메인 전용, body.nk-main 스코프 -->
```

Keep Cafe24 base CSS and Cafe24 JS imports.

- [ ] **Step 5: Run the common loader contract subset**

Run:

```bash
python -m unittest mcp.tests.test_verified_template_contract.VerifiedTemplateContractTests.test_common_loader_owns_config_and_assets mcp.tests.test_verified_template_contract.VerifiedTemplateContractTests.test_setup_exposes_documented_config_keys -v
```

Expected: PASS for these two tests.

- [ ] **Step 6: Commit setup and common loader**

Run:

```bash
git add agent-kit/clients/_verified-template/src/setup.html agent-kit/clients/_verified-template/src/_nk/inc/common.html agent-kit/clients/_verified-template/src/layout/basic/layout.html agent-kit/clients/_verified-template/src/layout/basic/main.html
git commit -m "feat: add nk setup and common loader"
```

---

### Task 3: Add SmartDesignEasy Module Contract

**Files:**
- Create: `agent-kit/clients/_verified-template/src/ez/ez-module.html`

- [ ] **Step 1: Create `ez/ez-module.html`**

Write `agent-kit/clients/_verified-template/src/ez/ez-module.html`:

```html
<section class="nk-section nk-main-product" data-ez-module="product-list/1" data-ez-layout="grid4">
    <ez-prop data-version="1.0.0">
        <ez-var data-prop="layout" data-namespace="ez.module.product-list.layout" data-type="array">
            <ez-item data-id="grid3" data-name="3단 상품 진열"></ez-item>
            <ez-item data-id="grid4" data-name="4단 상품 진열"></ez-item>
            <ez-item data-id="grid5" data-name="5단 상품 진열"></ez-item>
        </ez-var>
    </ez-prop>
    <div class="nk-section-heading" data-ez-role="ez-align" data-ez-align="left">
        <div class="nk-section-title" data-ez-role="title">New Product</div>
        <div class="nk-section-subtitle" data-ez-role="subtitle">새롭게 입고된 상품을 만나보세요</div>
    </div>
    <div data-ez-holder="product_listmain">
        <div module="product_listmain_1" class="ec-base-product nk-product-module">
            <!--
                $count = 8
                $basket_result = /product/add_basket.html
                $basket_option = /product/basket_option.html
            -->
            <ul class="nk-prd-grid" data-ez-role="layout ez-discount-tag">
                <!--@import(/product/list_product.html)-->
            </ul>
        </div>
    </div>
</section>

<section class="nk-section nk-image-gallery" data-ez-module="image-gallery/2" data-ez-role="style.background" data-ez-item-length="3">
    <ez-prop data-version="1.0.0">
        <ez-var data-prop="image" data-namespace="ez.module.image-gallery.image">
            <ez-item data-id="size" data-pc="720 720" data-mobile="720 720"></ez-item>
        </ez-var>
        <ez-var data-prop="display" data-namespace="ez.module.image-gallery.display">
            <ez-item data-id="item" data-max="10"></ez-item>
            <ez-item data-id="column" data-default="3" data-min="1" data-max="5"></ez-item>
        </ez-var>
        <ez-var data-prop="layout" data-namespace="ez.module.image-gallery.layout">
            <ez-item data-id="mobile" data-default="slide">
                <ez-item data-id="options" data-type="array">
                    <ez-item data-id="slide" data-name="슬라이드"></ez-item>
                    <ez-item data-id="more" data-name="더보기"></ez-item>
                    <ez-item data-id="none" data-name="사용안함"></ez-item>
                </ez-item>
            </ez-item>
        </ez-var>
    </ez-prop>
    <div class="nk-section-heading" data-ez-role="ez-align" data-ez-align="left">
        <div class="nk-section-title" data-ez-role="title">Lifestyle</div>
        <div class="nk-section-subtitle" data-ez-role="desc">브랜드 무드가 담긴 이미지를 소개합니다</div>
    </div>
    <ul class="nk-gallery-grid" data-ez-role="image-list ez-column" data-ez-column="3">
        <li class="nk-gallery-card" data-ez-role="image-item ez-align">
            <a data-ez-role="a" href="#none" target="_self">
                <picture>
                    <source srcset="/_nk/img/gallery-01.jpg" media="(min-width: 768px)" data-ez-role="img-pc" />
                    <img src="/_nk/img/gallery-01.jpg" alt="브랜드 갤러리 이미지 1" data-ez-role="img-mobile" loading="lazy" />
                </picture>
                <span class="nk-gallery-title" data-ez-role="title">Gallery One</span>
                <span class="nk-gallery-desc" data-ez-role="desc">자세히 보기</span>
            </a>
        </li>
    </ul>
</section>
```

- [ ] **Step 2: Run Easy metadata contract test**

Run:

```bash
python -m unittest mcp.tests.test_verified_template_contract.VerifiedTemplateContractTests.test_easy_metadata_contract_is_present -v
```

Expected: PASS.

- [ ] **Step 3: Commit Easy module contract**

Run:

```bash
git add agent-kit/clients/_verified-template/src/ez/ez-module.html
git commit -m "feat: add easy module metadata contract"
```

---

### Task 4: Split Main Sections Into Esthe-style Partials

**Files:**
- Create: `agent-kit/clients/_verified-template/src/_nk/inc/main-hero.html`
- Create: `agent-kit/clients/_verified-template/src/_nk/inc/product-list.html`
- Create: `agent-kit/clients/_verified-template/src/_nk/inc/product-slide.html`
- Create: `agent-kit/clients/_verified-template/src/_nk/inc/image-gallery.html`
- Modify: `agent-kit/clients/_verified-template/src/layout/basic/main.html`

- [ ] **Step 1: Create `main-hero.html`**

Write `agent-kit/clients/_verified-template/src/_nk/inc/main-hero.html`:

```html
<section class="nk-hero" aria-label="메인 비주얼" data-nk-config-show="showMainHero" data-ez-module="image/1" data-ez-role="style.background">
    <div class="nk-hero__copy" data-ez-role="ez-align" data-ez-align="center">
        <p class="nk-hero__wordmark" data-ez-role="title">YOUR BRAND</p><!-- 설치: 브랜드명으로 교체 -->
        <p class="nk-hero__tagline" data-ez-role="desc">Your tagline goes here.</p><!-- 설치: 태그라인으로 교체 -->
        <a class="nk-hero__link" href="#none" data-ez-role="a">Shop Now</a>
    </div>
</section>
```

- [ ] **Step 2: Create `product-list.html`**

Write `agent-kit/clients/_verified-template/src/_nk/inc/product-list.html`:

```html
<section class="nk-sec nk-sec--products" aria-labelledby="nkRecommendedTitle" data-nk-config-show="showBestProducts" data-ez-module="product-list/1" data-ez-layout="grid4">
    <ez-prop data-version="1.0.0">
        <ez-var data-prop="layout" data-namespace="ez.module.product-list.layout" data-type="array">
            <ez-item data-id="grid3" data-name="3단 상품 진열"></ez-item>
            <ez-item data-id="grid4" data-name="4단 상품 진열"></ez-item>
            <ez-item data-id="grid5" data-name="5단 상품 진열"></ez-item>
        </ez-var>
    </ez-prop>
    <div class="nk-listmain" module="product_listmain_1" data-ez-holder="product_listmain"><!--
        $count = 8
        $basket_result = /product/add_basket.html
        $basket_option = /product/basket_option.html
    -->
        <div class="nk-sec__head" data-ez-role="ez-align" data-ez-align="left">
            <h2 class="nk-sec__title" id="nkRecommendedTitle">
                <span class="nk-sec__en" data-ez-role="title">Recommended</span>
                <span class="nk-sec__kr" data-ez-role="subtitle">추천상품</span>
            </h2>
        </div>
        <ul class="nk-prd-grid" data-ez-role="layout ez-discount-tag">
            <li id="anchorBoxId_{$product_no}" class="nk-prd-card">
                <a href="{$link_product_detail}" name="anchorBoxName_{$product_no}" class="nk-prd-card__link">
                    <span class="nk-prd-card__thumb">
                        <img src="{$image_medium}" alt="{$seo_alt_tag}" class="nk-prd-card__img" loading="lazy" />
                    </span>
                    <span class="nk-prd-card__name">{$product_name}</span>
                </a>
                <ul module="product_ListItem" class="nk-prd-card__price-list">
                    <li class="nk-prd-card__price-item {$item_display|display}">
                        <span class="nk-prd-card__price-label {$item_title_display|display}">{$item_title}</span>
                        <span class="nk-prd-card__price-val">{$item_content}</span>
                    </li>
                    <li class="nk-prd-card__price-item {$item_display|display}">
                        <span class="nk-prd-card__price-label {$item_title_display|display}">{$item_title}</span>
                        <span class="nk-prd-card__price-val">{$item_content}</span>
                    </li>
                </ul>
            </li>
            <li id="anchorBoxId_{$product_no}" class="nk-prd-card">
                <a href="{$link_product_detail}" name="anchorBoxName_{$product_no}" class="nk-prd-card__link">
                    <span class="nk-prd-card__thumb">
                        <img src="{$image_medium}" alt="{$seo_alt_tag}" class="nk-prd-card__img" loading="lazy" />
                    </span>
                    <span class="nk-prd-card__name">{$product_name}</span>
                </a>
                <ul module="product_ListItem" class="nk-prd-card__price-list">
                    <li class="nk-prd-card__price-item {$item_display|display}">
                        <span class="nk-prd-card__price-label {$item_title_display|display}">{$item_title}</span>
                        <span class="nk-prd-card__price-val">{$item_content}</span>
                    </li>
                    <li class="nk-prd-card__price-item {$item_display|display}">
                        <span class="nk-prd-card__price-label {$item_title_display|display}">{$item_title}</span>
                        <span class="nk-prd-card__price-val">{$item_content}</span>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
</section>
```

- [ ] **Step 3: Create `product-slide.html`**

Write `agent-kit/clients/_verified-template/src/_nk/inc/product-slide.html`:

```html
<section class="nk-sec nk-sec--product-slide" aria-labelledby="nkNewArrivalsTitle" data-nk-config-show="showNewProducts" data-ez-module="product-list-slide/2" data-ez-layout="grid4_slide">
    <div class="nk-listmain nk-swiper" module="product_listmain_1" data-ez-holder="product_listmain"><!--
        $count = 8
        $basket_result = /product/add_basket.html
        $basket_option = /product/basket_option.html
    -->
        <div class="nk-sec__head" data-ez-role="ez-align" data-ez-align="left">
            <h2 class="nk-sec__title" id="nkNewArrivalsTitle">
                <span class="nk-sec__en" data-ez-role="title">New Arrivals</span>
                <span class="nk-sec__kr" data-ez-role="subtitle">신상품</span>
            </h2>
        </div>
        <div class="swiper nk-product-swiper" data-nk-swiper="product">
            <ul class="swiper-wrapper nk-prd-grid nk-prd-grid--slider" data-ez-role="layout ez-discount-tag">
                <li id="anchorBoxId_{$product_no}" class="swiper-slide nk-prd-card">
                    <a href="{$link_product_detail}" name="anchorBoxName_{$product_no}" class="nk-prd-card__link">
                        <span class="nk-prd-card__thumb">
                            <img src="{$image_medium}" alt="{$seo_alt_tag}" class="nk-prd-card__img" loading="lazy" />
                        </span>
                        <span class="nk-prd-card__name">{$product_name}</span>
                    </a>
                </li>
            </ul>
            <div class="swiper-pagination nk-product-swiper__pagination"></div>
        </div>
    </div>
</section>
```

- [ ] **Step 4: Create `image-gallery.html`**

Write `agent-kit/clients/_verified-template/src/_nk/inc/image-gallery.html`:

```html
<section class="nk-sec nk-image-gallery" data-nk-config-show="showImageGallery" data-ez-module="image-gallery/2" data-ez-role="style.background" data-ez-item-length="3">
    <div class="nk-sec__head" data-ez-role="ez-align" data-ez-align="left">
        <h2 class="nk-sec__title">
            <span class="nk-sec__en" data-ez-role="title">Lifestyle</span>
            <span class="nk-sec__kr" data-ez-role="desc">브랜드 무드가 담긴 이미지</span>
        </h2>
    </div>
    <ul class="nk-gallery-grid" data-ez-role="image-list ez-column" data-ez-column="3">
        <li class="nk-gallery-card" data-ez-role="image-item ez-align">
            <a href="#none" data-ez-role="a" target="_self">
                <span class="nk-gallery-card__media">
                    <img src="/_nk/img/gallery-01.jpg" alt="브랜드 갤러리 이미지 1" data-ez-role="img-mobile" loading="lazy" />
                </span>
                <span class="nk-gallery-card__title" data-ez-role="title">Gallery One</span>
                <span class="nk-gallery-card__desc" data-ez-role="desc">자세히 보기</span>
            </a>
        </li>
        <li class="nk-gallery-card" data-ez-role="image-item ez-align">
            <a href="#none" data-ez-role="a" target="_self">
                <span class="nk-gallery-card__media">
                    <img src="/_nk/img/gallery-02.jpg" alt="브랜드 갤러리 이미지 2" data-ez-role="img-mobile" loading="lazy" />
                </span>
                <span class="nk-gallery-card__title" data-ez-role="title">Gallery Two</span>
                <span class="nk-gallery-card__desc" data-ez-role="desc">자세히 보기</span>
            </a>
        </li>
        <li class="nk-gallery-card" data-ez-role="image-item ez-align">
            <a href="#none" data-ez-role="a" target="_self">
                <span class="nk-gallery-card__media">
                    <img src="/_nk/img/gallery-03.jpg" alt="브랜드 갤러리 이미지 3" data-ez-role="img-mobile" loading="lazy" />
                </span>
                <span class="nk-gallery-card__title" data-ez-role="title">Gallery Three</span>
                <span class="nk-gallery-card__desc" data-ez-role="desc">자세히 보기</span>
            </a>
        </li>
    </ul>
</section>
```

- [ ] **Step 5: Replace main inline sections with imports**

In `agent-kit/clients/_verified-template/src/layout/basic/main.html`, inside `<div id="contents">`, keep the existing explanatory comment shortened to this:

```html
            <!-- NK Esthe-style main sections: section bodies live in /_nk/inc for safe editing. -->
            <!--@import(/_nk/inc/main-hero.html)-->
            <!--@import(/_nk/inc/product-list.html)-->
            <!--@import(/_nk/inc/product-slide.html)-->
            <!--@import(/_nk/inc/image-gallery.html)-->
```

Remove the old inline hero/product/banner sections from `main.html` so each section has a single source of truth.

- [ ] **Step 6: Run partial file contract tests**

Run:

```bash
python -m unittest mcp.tests.test_verified_template_contract.VerifiedTemplateContractTests.test_esthe_style_easy_contract_files_exist -v
```

Expected: FAIL only if CSS/JS files from later tasks are not created. HTML partial paths should no longer be in the failure list.

- [ ] **Step 7: Commit section partials**

Run:

```bash
git add agent-kit/clients/_verified-template/src/_nk/inc/main-hero.html agent-kit/clients/_verified-template/src/_nk/inc/product-list.html agent-kit/clients/_verified-template/src/_nk/inc/product-slide.html agent-kit/clients/_verified-template/src/_nk/inc/image-gallery.html agent-kit/clients/_verified-template/src/layout/basic/main.html
git commit -m "feat: split verified main into nk partials"
```

---

### Task 5: Add NK Easy CSS and Responsive Layer

**Files:**
- Create: `agent-kit/clients/_verified-template/src/_nk/css/nk-ez.css`
- Create: `agent-kit/clients/_verified-template/src/_nk/css/nk-responsive.css`
- Modify: `agent-kit/clients/_verified-template/src/_nk/css/nk-tokens.css`
- Modify: `agent-kit/clients/_verified-template/src/_nk/css/nk-main.css`

- [ ] **Step 1: Append missing tokens to `nk-tokens.css`**

Append this block to `agent-kit/clients/_verified-template/src/_nk/css/nk-tokens.css`:

```css
/* NK Esthe-style compatibility tokens — 기존 토큰을 지우지 않고 보강합니다. */
:root {
  --nk-section-y: clamp(48px, 7vw, 120px);
  --nk-section-x: clamp(16px, 4vw, 80px);
  --nk-container-max: 1440px;
  --nk-container-wide: 1920px;
  --nk-radius-card: 18px;
  --nk-ease-standard: cubic-bezier(0.22, 1, 0.36, 1);
  --nk-motion-fast: 180ms;
  --nk-motion-base: 280ms;
}
```

- [ ] **Step 2: Create `nk-ez.css`**

Write `agent-kit/clients/_verified-template/src/_nk/css/nk-ez.css`:

```css
/* NK Easy compatibility layer. data-ez-*는 편집기 메타데이터이며 화면 필수 의존성이 아닙니다. */
.nk-skin [data-nk-hidden="true"] {
  display: none !important;
}

.nk-skin [data-ez-role="ez-align"][data-ez-align="center"] {
  text-align: center;
}

.nk-skin [data-ez-role="ez-align"][data-ez-align="right"] {
  text-align: right;
}

.nk-skin .nk-section-heading,
.nk-skin .nk-sec__head {
  margin: 0 auto 28px;
  max-width: var(--nk-container-max, 1440px);
  padding: 0 var(--nk-section-x, 24px);
}

.nk-skin .nk-section-title,
.nk-skin .nk-sec__en {
  display: block;
  color: var(--nk-font, #1a1a1a);
  font-family: var(--nk-font-display, var(--nk-font-body, "Pretendard", sans-serif));
  font-size: clamp(28px, 4vw, 56px);
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1.05;
}

.nk-skin .nk-section-subtitle,
.nk-skin .nk-sec__kr {
  display: block;
  margin-top: 8px;
  color: var(--nk-sub, #666666);
  font-size: clamp(14px, 1.4vw, 18px);
  line-height: 1.6;
}
```

- [ ] **Step 3: Create `nk-responsive.css`**

Write `agent-kit/clients/_verified-template/src/_nk/css/nk-responsive.css`:

```css
/* NK responsive contract: 390 / 768 / 1440 / 1920 기준. */
.nk-skin .nk-sec,
.nk-skin .nk-image-gallery {
  padding: var(--nk-section-y, 72px) var(--nk-section-x, 24px);
}

.nk-skin .nk-prd-grid,
.nk-skin .nk-gallery-grid {
  display: grid;
  gap: clamp(16px, 2vw, 32px);
  margin: 0 auto;
  max-width: var(--nk-container-max, 1440px);
  padding: 0;
  list-style: none;
}

.nk-skin .nk-prd-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.nk-skin .nk-gallery-grid {
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .nk-skin .nk-prd-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .nk-skin .nk-gallery-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (min-width: 1440px) {
  .nk-skin .nk-prd-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (min-width: 1920px) {
  .nk-skin .nk-prd-grid,
  .nk-skin .nk-gallery-grid,
  .nk-skin .nk-section-heading,
  .nk-skin .nk-sec__head {
    max-width: var(--nk-container-wide, 1920px);
  }
}
```

- [ ] **Step 4: Append section support to `nk-main.css`**

Append this block to `agent-kit/clients/_verified-template/src/_nk/css/nk-main.css`:

```css
/* NK Esthe-style partial support */
.nk-main .nk-hero__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  margin-top: 22px;
  padding: 0 24px;
  border: 1px solid currentColor;
  border-radius: 999px;
  color: inherit;
  text-decoration: none;
  transition: background-color var(--nk-motion-base, 280ms) var(--nk-ease-standard, ease), color var(--nk-motion-base, 280ms) var(--nk-ease-standard, ease);
}

.nk-main .nk-hero__link:hover {
  background-color: var(--nk-font, #1a1a1a);
  color: var(--nk-bg, #ffffff);
}

.nk-main .nk-gallery-card a {
  display: block;
  color: inherit;
  text-decoration: none;
}

.nk-main .nk-gallery-card__media {
  display: block;
  overflow: hidden;
  border-radius: var(--nk-radius-card, 18px);
  background: var(--nk-bg2, #f5f0e8);
  aspect-ratio: 1 / 1;
}

.nk-main .nk-gallery-card__media img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.nk-main .nk-gallery-card__title {
  display: block;
  margin-top: 14px;
  font-weight: 700;
}

.nk-main .nk-gallery-card__desc {
  display: block;
  margin-top: 4px;
  color: var(--nk-sub, #666666);
}
```

- [ ] **Step 5: Run namespace contract test**

Run:

```bash
python -m unittest mcp.tests.test_verified_template_contract.VerifiedTemplateContractTests.test_nk_namespace_replaces_esthe_namespace -v
```

Expected: PASS.

- [ ] **Step 6: Commit CSS layers**

Run:

```bash
git add agent-kit/clients/_verified-template/src/_nk/css/nk-tokens.css agent-kit/clients/_verified-template/src/_nk/css/nk-ez.css agent-kit/clients/_verified-template/src/_nk/css/nk-responsive.css agent-kit/clients/_verified-template/src/_nk/css/nk-main.css
git commit -m "feat: add nk easy css layers"
```

---

### Task 6: Add NK Config and Adapter JavaScript

**Files:**
- Create: `agent-kit/clients/_verified-template/src/_nk/js/nk-config.js`
- Create: `agent-kit/clients/_verified-template/src/_nk/js/nk-core.js`
- Create: `agent-kit/clients/_verified-template/src/_nk/js/nk-slider.js`
- Create: `agent-kit/clients/_verified-template/src/_nk/js/nk-ez-adapter.js`

- [ ] **Step 1: Create `nk-config.js`**

Write `agent-kit/clients/_verified-template/src/_nk/js/nk-config.js`:

```js
(function (window) {
  var defaults = {
    showTopBanner: true,
    showPopup: false,
    showMainHero: true,
    showNewProducts: true,
    showBestProducts: true,
    showCategoryTabs: true,
    showImageGallery: true,
    showVideo: false,
    showMap: false,
    showReview: true,
    showInstagram: false,
    kakaoChannelUrl: "",
    naverTalkUrl: "",
    youtubeUrl: "",
    escrowUrl: ""
  };

  var supplied = window.NK_CONFIG || {};
  var config = {};
  Object.keys(defaults).forEach(function (key) {
    config[key] = Object.prototype.hasOwnProperty.call(supplied, key) ? supplied[key] : defaults[key];
  });

  window.NK_CONFIG = config;
  window.NK = window.NK || {};
  window.NK.getConfig = function (key) {
    return Object.prototype.hasOwnProperty.call(config, key) ? config[key] : undefined;
  };
})(window);
```

- [ ] **Step 2: Create `nk-core.js`**

Write `agent-kit/clients/_verified-template/src/_nk/js/nk-core.js`:

```js
(function (window, document) {
  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function applyVisibility() {
    var getConfig = window.NK && window.NK.getConfig;
    if (!getConfig) return;

    document.querySelectorAll("[data-nk-config-show]").forEach(function (el) {
      var key = el.getAttribute("data-nk-config-show");
      if (getConfig(key) === false) {
        el.setAttribute("data-nk-hidden", "true");
      } else {
        el.removeAttribute("data-nk-hidden");
      }
    });
  }

  function applyLinks() {
    var getConfig = window.NK && window.NK.getConfig;
    if (!getConfig) return;

    document.querySelectorAll("[data-nk-config-href]").forEach(function (el) {
      var key = el.getAttribute("data-nk-config-href");
      var value = getConfig(key);
      if (typeof value === "string" && value.length > 0) {
        el.setAttribute("href", value);
      }
    });
  }

  onReady(function () {
    applyVisibility();
    applyLinks();
  });
})(window, document);
```

- [ ] **Step 3: Create `nk-slider.js`**

Write `agent-kit/clients/_verified-template/src/_nk/js/nk-slider.js`:

```js
(function (window, document) {
  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  onReady(function () {
    if (!window.Swiper) return;

    document.querySelectorAll('[data-nk-swiper="product"]').forEach(function (el) {
      if (el.swiper) return;
      new window.Swiper(el, {
        slidesPerView: 2,
        spaceBetween: 16,
        loop: false,
        pagination: {
          el: el.querySelector(".swiper-pagination"),
          clickable: true
        },
        breakpoints: {
          768: { slidesPerView: 3, spaceBetween: 20 },
          1440: { slidesPerView: 4, spaceBetween: 24 }
        }
      });
    });
  });
})(window, document);
```

- [ ] **Step 4: Create `nk-ez-adapter.js`**

Write `agent-kit/clients/_verified-template/src/_nk/js/nk-ez-adapter.js`:

```js
(function (document) {
  function onReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  onReady(function () {
    document.querySelectorAll("[data-ez-layout]").forEach(function (el) {
      var layout = el.getAttribute("data-ez-layout");
      if (layout && el.className.indexOf("nk-ez-layout-") === -1) {
        el.className += " nk-ez-layout-" + layout.replace(/\s+/g, "-");
      }
    });
  });
})(document);
```

- [ ] **Step 5: Run JS/common contract tests**

Run:

```bash
python -m unittest mcp.tests.test_verified_template_contract.VerifiedTemplateContractTests.test_esthe_style_easy_contract_files_exist mcp.tests.test_verified_template_contract.VerifiedTemplateContractTests.test_common_loader_owns_config_and_assets -v
```

Expected: PASS.

- [ ] **Step 6: Commit JS adapters**

Run:

```bash
git add agent-kit/clients/_verified-template/src/_nk/js/nk-config.js agent-kit/clients/_verified-template/src/_nk/js/nk-core.js agent-kit/clients/_verified-template/src/_nk/js/nk-slider.js agent-kit/clients/_verified-template/src/_nk/js/nk-ez-adapter.js
git commit -m "feat: add nk config and easy adapters"
```

---

### Task 7: Extend Generate Skin Fixture Coverage

**Files:**
- Modify: `mcp/tests/test_generate_skin.py`

- [ ] **Step 1: Update `_make_verified_src` fixture**

In `mcp/tests/test_generate_skin.py`, inside `_make_verified_src`, after the existing `nk.js` write block, add:

```python
        self._write(
            self.verified_src / "setup.html",
            "<script>window.NK_CONFIG = { showMainHero: true };</script>\n",
        )
        self._write(
            self.verified_src / "ez" / "ez-module.html",
            '<section data-ez-module="product-list/1" data-ez-layout="grid4"><ez-prop><ez-var><ez-item data-id="grid4"></ez-item></ez-var></ez-prop><div data-ez-role="title" data-ez-holder="product_listmain">Title</div></section>\n',
        )
        self._write(
            self.verified_src / "_nk" / "inc" / "common.html",
            "<!--@import(/setup.html)--><!--@css(/_nk/css/nk-ez.css)--><!--@js(/_nk/js/nk-config.js)--><!--@js(/_nk/js/nk-core.js)-->",
        )
        self._write(self.verified_src / "_nk" / "inc" / "main-hero.html", '<section class="nk-hero" data-ez-role="title"></section>\n')
        self._write(self.verified_src / "_nk" / "css" / "nk-ez.css", ".nk-skin [data-nk-hidden='true'] { display:none!important; }\n")
        self._write(self.verified_src / "_nk" / "js" / "nk-config.js", "window.NK_CONFIG = window.NK_CONFIG || {};\n")
        self._write(self.verified_src / "_nk" / "js" / "nk-core.js", "window.NK = window.NK || {};\n")
```

- [ ] **Step 2: Add copy preservation test**

Add this test method to `GenerateSkinTests`:

```python
    def test_generate_skin_preserves_easy_compatible_template_files(self):
        result = self._generate_skin("ecudemo123", with_design=False)
        src_dir = self._client_dir("ecudemo123") / "src"

        self.assertTrue((src_dir / "setup.html").is_file())
        self.assertTrue((src_dir / "ez" / "ez-module.html").is_file())
        self.assertTrue((src_dir / "_nk" / "inc" / "common.html").is_file())
        self.assertTrue((src_dir / "_nk" / "css" / "nk-ez.css").is_file())
        self.assertTrue((src_dir / "_nk" / "js" / "nk-config.js").is_file())
        self.assertTrue((src_dir / "_nk" / "js" / "nk-core.js").is_file())
        self.assertIn("data-ez-module", (src_dir / "ez" / "ez-module.html").read_text(encoding="utf-8"))
        self.assertIn("NK_CONFIG", (src_dir / "setup.html").read_text(encoding="utf-8"))
        self.assertEqual(result["files_copied"], len(self._relative_files(self.verified_src)))
```

- [ ] **Step 3: Run generate skin tests**

Run:

```bash
python -m unittest discover -s mcp/tests -p "test_generate_skin.py" -v
```

Expected: PASS.

- [ ] **Step 4: Commit generate skin test coverage**

Run:

```bash
git add mcp/tests/test_generate_skin.py
git commit -m "test: cover easy template skin generation"
```

---

### Task 8: Extend Build and Verify Guards

**Files:**
- Modify: `scripts/build-dist-kit.sh`
- Modify: `scripts/verify-kit.sh`

- [ ] **Step 1: Add required files to `build-dist-kit.sh`**

In `scripts/build-dist-kit.sh`, inside the `REQUIRED=(` block after the existing `_verified-template` required paths, add:

```bash
  "$OUT/agent-kit/clients/_verified-template/src/setup.html"
  "$OUT/agent-kit/clients/_verified-template/src/ez/ez-module.html"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/inc/common.html"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/inc/main-hero.html"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/inc/product-list.html"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/inc/product-slide.html"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/inc/image-gallery.html"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/css/nk-ez.css"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/css/nk-responsive.css"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/js/nk-config.js"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/js/nk-core.js"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/js/nk-slider.js"
  "$OUT/agent-kit/clients/_verified-template/src/_nk/js/nk-ez-adapter.js"
```

- [ ] **Step 2: Add post-build Easy contract checks to `build-dist-kit.sh`**

After the existing `_verified-template stock/legacy standard` checks and before the VERSION check, add:

```bash
VT_SETUP="$OUT/agent-kit/clients/_verified-template/src/setup.html"
VT_EZ="$OUT/agent-kit/clients/_verified-template/src/ez/ez-module.html"
VT_COMMON="$OUT/agent-kit/clients/_verified-template/src/_nk/inc/common.html"
if ! grep -q 'window.NK_CONFIG' "$VT_SETUP"; then
  echo "FAIL: _verified-template setup.html missing window.NK_CONFIG" >&2
  exit 1
fi
for token in 'data-ez-module' 'data-ez-role' 'data-ez-holder' 'ez-prop' 'ez-var' 'ez-item'; do
  if ! grep -q "$token" "$VT_EZ"; then
    echo "FAIL: _verified-template ez-module.html missing $token" >&2
    exit 1
  fi
done
if ! grep -q '<!--@import(/setup.html)-->' "$VT_COMMON"; then
  echo "FAIL: _verified-template common.html missing setup.html import" >&2
  exit 1
fi
if grep -rIqiE '_idio|IDIO\[|--idio-|Font Awesome|fontawesome|fa-regular|fa-solid|font-style:[[:space:]]*(italic|oblique)' "$OUT/agent-kit/clients/_verified-template/src"; then
  echo "FAIL: _verified-template contains forbidden Esthe/FontAwesome/italic tokens" >&2
  exit 1
fi
```

- [ ] **Step 3: Add verify-kit runtime checks**

In `scripts/verify-kit.sh`, after the existing `[9] 드리프트 가드` template checks and before `[10] skin_analyzer unit tests`, add:

```bash
# 9-6) NK Esthe-style Easy 호환 계약
if [[ -d "$VT/src" ]]; then
  VT_SETUP="$VT/src/setup.html"
  VT_EZ="$VT/src/ez/ez-module.html"
  VT_COMMON="$VT/src/_nk/inc/common.html"
  if [[ -f "$VT_SETUP" ]] && grep -q 'window.NK_CONFIG' "$VT_SETUP"; then
    ok "_verified-template setup.html NK_CONFIG 존재"
  else
    fail "_verified-template setup.html NK_CONFIG 없음"
  fi
  if [[ -f "$VT_COMMON" ]] && grep -q '<!--@import(/setup.html)-->' "$VT_COMMON"; then
    ok "_verified-template common.html setup import 존재"
  else
    fail "_verified-template common.html setup import 없음"
  fi
  if [[ -f "$VT_EZ" ]]; then
    EZ_MISSING=""
    for token in 'data-ez-module' 'data-ez-role' 'data-ez-holder' 'ez-prop' 'ez-var' 'ez-item'; do
      grep -q "$token" "$VT_EZ" || EZ_MISSING="$EZ_MISSING $token"
    done
    if [[ -z "$EZ_MISSING" ]]; then
      ok "_verified-template Easy 메타데이터 존재"
    else
      fail "_verified-template Easy 메타데이터 누락:$EZ_MISSING"
    fi
  else
    fail "_verified-template ez/ez-module.html 없음"
  fi
  FORBIDDEN_NK=$(grep -rIliE '_idio|IDIO\[|--idio-|Font Awesome|fontawesome|fa-regular|fa-solid|font-style:[[:space:]]*(italic|oblique)' "$VT/src" 2>/dev/null || true)
  if [[ -n "$FORBIDDEN_NK" ]]; then
    fail "_verified-template 금지 토큰 발견:"
    echo "$FORBIDDEN_NK" | while read -r f; do echo "     $f"; done
  else
    ok "_verified-template 금지 토큰 0건"
  fi
fi
```

- [ ] **Step 4: Run build and verify**

Run:

```bash
bash scripts/build-dist-kit.sh && bash scripts/verify-kit.sh
```

Expected: PASS, `OK: 모든 검증 통과 — 배포 준비 완료`.

- [ ] **Step 5: Commit build and verify guards**

Run:

```bash
git add scripts/build-dist-kit.sh scripts/verify-kit.sh
git commit -m "test: guard nk easy template distribution"
```

---

### Task 9: Update Non-developer Documentation

**Files:**
- Modify: `agent-kit/clients/_verified-template/README.md`
- Modify: `agent-kit/README.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update `_verified-template/README.md` file count and folder map**

In `agent-kit/clients/_verified-template/README.md`, replace the `## 1. 이게 뭔가요?` bullets with:

```markdown
- 카페24 **스마트디자인(HTML) 스킨**용 템플릿 — Esthe-style NK 구조를 적용한 검증 템플릿입니다.
- `src/setup.html`에서 주요 영역 on/off와 SNS/상담 링크를 수정합니다.
- `src/ez/ez-module.html`에는 SmartDesignEasy 편집기 호환용 `data-ez-*`, `ez-prop`, `ez-var`, `ez-item` 메타데이터가 포함됩니다.
- 실제 디자인 기준은 `nk-*` 클래스와 `src/_nk/css/*.css`가 담당합니다. Easy 속성은 편집기 인식용이며 화면 동작의 필수 조건이 아닙니다.
- 모든 색·폰트·치수는 `src/_nk/css/nk-tokens.css` 변수로 관리합니다.
```

Replace the folder map block with:

```markdown
src/
├── setup.html                  ← 비개발자 설정: 영역 on/off, SNS/상담 링크
├── ez/ez-module.html           ← SmartDesignEasy 호환 메타데이터
├── index.html                  ← 메인 라우팅 스텁
├── layout/basic/               ← 공용 레이아웃 · 메인 본체 · 팝업 레이아웃
├── product/                    ← 상품목록(list) · 상품검색(search) · 상품상세(detail)
├── member/                     ← 로그인(login) · 회원가입(join) · 가입완료 · 아이디/비밀번호 찾기
├── order/                      ← 장바구니(basket)
├── myshop/                     ← 마이쇼핑(index) · 관심상품(wish_list) · 마이쿠폰(coupon)
├── coupon/                     ← 쿠폰존(coupon_zone)
├── shopinfo/                   ← 회사소개(company) · 이용안내(guide)
├── board/                      ← 게시판 목록·읽기·쓰기
└── _nk/
    ├── inc/                    ← common/header/footer/main 섹션 조각
    ├── css/                    ← tokens/reset/base/components/easy/responsive/page CSS
    └── js/                     ← config/core/slider/easy adapter
```

- [ ] **Step 2: Add setup editing section**

After the brand token section, add:

```markdown
### 3-5. 영역 켜고 끄기 — `src/setup.html`

`setup.html`은 비개발자용 설정 파일입니다. 아래 값만 바꾸세요.

```html
showTopBanner: true,
showPopup: false,
showMainHero: true,
showNewProducts: true,
showBestProducts: true,
showImageGallery: true,
kakaoChannelUrl: "",
naverTalkUrl: "",
youtubeUrl: ""
```

- `true` = 보임
- `false` = 숨김
- URL 값은 따옴표 안에 붙여넣습니다.
- `module="..."`, `data-ez-*`, `ez-prop`, `ez-var`, `ez-item`은 지우지 마세요.
```

- [ ] **Step 3: Update `agent-kit/README.md` verified template description**

In `agent-kit/README.md`, update lines 112-124 section to mention:

```markdown
검증 템플릿은 Esthe-style NK 구조입니다. `setup.html`로 영역 on/off를 제어하고, `_nk/inc` 조각 파일로 메인 섹션을 나누며, `ez/ez-module.html`에 SmartDesignEasy 호환 메타데이터를 포함합니다. 실제 스타일과 동작은 `nk-*` 클래스, `_nk/css`, `_nk/js`가 담당합니다.
```

- [ ] **Step 4: Add changelog entry**

At the top of `CHANGELOG.md` under Unreleased, add:

```markdown
### Added
- Verified template now uses an NK Esthe-style Easy-compatible structure: `setup.html`, `_nk/inc/common.html`, section partials, `ez/ez-module.html`, NK config/core/slider/Easy adapter scripts, and dist guards for Easy metadata.

### Safety
- Added guards preventing `_idio`, `IDIO`, `--idio-*`, Font Awesome, and italic/oblique font-style from entering `_verified-template`.
```

- [ ] **Step 5: Commit documentation updates**

Run:

```bash
git add agent-kit/clients/_verified-template/README.md agent-kit/README.md CHANGELOG.md
git commit -m "docs: document nk easy template workflow"
```

---

### Task 10: Final Verification and Handoff

**Files:**
- No source edits unless verification fails.

- [ ] **Step 1: Run focused unit tests**

Run:

```bash
python -m unittest discover -s mcp/tests -p "test_verified_template_contract.py" -v
python -m unittest discover -s mcp/tests -p "test_generate_skin.py" -v
```

Expected: both PASS.

- [ ] **Step 2: Run full MCP tests**

Run:

```bash
python -m unittest discover -s mcp/tests -p "test*.py" -v
```

Expected: PASS.

- [ ] **Step 3: Run dist build and verify**

Run:

```bash
bash scripts/build-dist-kit.sh && bash scripts/verify-kit.sh
```

Expected: PASS, `OK: 모든 검증 통과 — 배포 준비 완료`.

- [ ] **Step 4: Run skin audit against verified template**

Run:

```bash
python mcp/cli.py skin-audit agent-kit/clients/_verified-template/src --json-out tmp/nk-easy-skin-audit.json
```

Expected: command exits 0 and writes `tmp/nk-easy-skin-audit.json`. Inspect JSON `blockers` should be empty.

- [ ] **Step 5: Commit verification-only fixes if needed**

If Step 1-4 reveal a defect, fix only the failing contract and commit with a message describing the exact failure. If all pass without edits, skip this commit step.

- [ ] **Step 6: Final handoff summary**

Report:

```text
구현 범위:
- setup.html
- _nk/inc/common.html
- _nk/inc 메인 섹션 partials
- ez/ez-module.html
- nk-ez.css / nk-responsive.css
- nk-config.js / nk-core.js / nk-slider.js / nk-ez-adapter.js
- build/verify/test guards

검증:
- test_verified_template_contract.py PASS
- test_generate_skin.py PASS
- full mcp/tests PASS
- build-dist-kit.sh + verify-kit.sh PASS
- skin-audit blockers 0
```

---

## Self-Review Notes

- Spec requirement `setup.html` is covered by Tasks 2, 7, 8, 9, 10.
- Spec requirement `ez/ez-module.html` and Easy metadata is covered by Tasks 3, 4, 7, 8, 10.
- Spec requirement `inc` partial structure is covered by Tasks 2 and 4.
- Spec requirement NK CSS/JS layers is covered by Tasks 5 and 6.
- Spec requirement forbidden Esthe namespace guard is covered by Tasks 1 and 8.
- Spec requirement docs update is covered by Task 9.
- Spec requirement verification is covered by Task 10.
- No implementation step targets live client folders.
