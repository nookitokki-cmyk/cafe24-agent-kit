# 카페24 에이전트 키트

> **비코더가 Cursor / Claude Code로 카페24 스킨 작업을 자동화하는 키트.**
> 코드 몰라도, 채팅 명령으로 카페24 디자인을 수정·배포합니다.

**처음 오면 이 문서(README)부터 시작하세요.** 설치·심화는 아래를 상황별로 참고합니다.

- **이 문서(`README.md`)** = 처음 오면 여기부터 (길잡이)
- **[`설치-안내.md`](설치-안내.md)** = 설치·연결이 막힐 때
- **`PURPOSE.md`** = 설계 원칙 (개발자용 — 개발 레포에만 있고 배포본엔 미포함)

## 🚀 시작 (3단계)

1. **받기** — GitHub Release에서 `cafe24-agent-kit*.zip` 다운로드 → 압축 해제 (또는 `git clone`)
2. **열기** — 그 폴더를 **Cursor 또는 Claude Code**로 열기
3. **채팅에 `/키트시작`** — 설치·연결을 하나씩 안내합니다 (준비물: Python 3.10+, 내 몰 ID)

→ 설치가 막히면: [`설치-안내.md`](설치-안내.md) (수동 설치·트러블슈팅)

## 📂 다음은 어디로?

| 하려는 것 | 가는 곳 |
|---|---|
| 키트가 뭔지·명령·폴더맵 | [`agent-kit/README.md`](agent-kit/README.md) — **키트 본체 지도** |
| 처음부터 차근차근 | [`agent-kit/00_시작하기/`](agent-kit/00_시작하기/) — 온보딩 순서 |
| 카페24 연결(토큰) | 채팅 `/API발급` |
| 효율 프롬프트 60선 | [`agent-kit/00_시작하기/프롬프트-마스터.md`](agent-kit/00_시작하기/프롬프트-마스터.md) |
| 작업하다 막힘 | [`agent-kit/02_막혔을때/F-상황-인덱스.md`](agent-kit/02_막혔을때/F-상황-인덱스.md) |
| 배포 전 스킨 안전 점검 | [`agent-kit/01_작업하기/workflows/10-production-skin-safety.md`](agent-kit/01_작업하기/workflows/10-production-skin-safety.md) |

## 🔧 구조 (한눈에)

| 폴더 | 내용 |
|---|---|
| `agent-kit/` | 키트 본체 — 가이드·스킬·두뇌 (배포 대상) |
| `mcp/` | 카페24 연결 손발 (MCP 서버) |
| `scripts/` · `dist/` | 빌드 도구·배포 산출물 (개발 레포 전용 — 배포본 미포함) |
| `_dev/` | 개발용 (배포 제외) |


> **v2.13.0 업데이트:** `python mcp/cli.py skin-audit <local-skin-root>`로 로컬 Cafe24 SmartDesign 스킨을 read-only 점검합니다. SmartDesign directive, `module="..."`, `{$...}` 변수, 보호 영역(`/order/ec_orderform/**`), 누락 reference를 분류해 SFTP 업로드 전 위험을 먼저 보여줍니다. 업로드·삭제·원격 변경은 하지 않습니다.
>
> **v2.12.0 업데이트:** 앞으로 `/새클라이언트` 온보딩과 토대정리 기준 CSS는 `nk-tokens.css` → `nk-cafe24-reset.css` → `nk-base.css` → `nk-stock.css` 4종을 표준으로 안내합니다. 단, `nk-stock.css`는 `layout` include와 `body.nk-skin` 스코프가 함께 있을 때 스톡/legacy 페이지에 적용됩니다.

## ✅ 검증

```bash
bash agent-kit/connect/scripts/verify-kit.sh    # 소스 구조·문서 점검
```

---

> 변경 이력: [`CHANGELOG.md`](CHANGELOG.md)  ·  (목적·구조 원칙은 개발 레포의 `PURPOSE.md` 참고 — 배포본 미포함)
