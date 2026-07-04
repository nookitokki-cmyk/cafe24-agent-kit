# 04. 실측 우선 (Measure First)

> **원칙:** 디자인 지시가 와도 **먼저 숫자를 모은다.** 「예쁘게」만으로는 작업하지 않는다.  
> 명령: `/요소측정` · 완료 후 `/디자인수정`

---

## 언제 쓰나

- 「헤더 바꿔줘」「여백 줄여줘」「폰트 고급스럽게」처럼 **말만 있는 요청**
- 레퍼런스 URL·Figma·스크린샷이 있을 때

---

## 흐름

```
사용자 지시
  → /요소측정 (질문 핑퐁)
  → 실측 시트 작성
  → 사용자 「예」
  → /디자인수정 또는 workflow 01/02
  → 업로드·?v=N·PC+모바일 스크린샷
```

---

## 실측 시트 템플릿

| 항목 | 값 |
|------|-----|
| 페이지 / URL | |
| skin_code | |
| 레퍼런스 | |
| 제목 font-family / size / weight | |
| 본문 font-family / size / line-height | |
| 섹션 padding (top/bottom px) | |
| 컨테이너 max-width | |
| 색상 primary / text / bg (hex) | |
| breakpoint (768 / 360) | |

---

## 에이전트 질문 예시 (그대로 써도 됨)

- 「**어떤 폰트**로 할까요? Pretendard 말고 지정이 있나요?」
- 「**여백을 px 숫자**로 알려주세요. 모르면 스크린샷에서 48px처럼 제안할게요.」
- 「**모바일 360px** 도 같은 기준인가요?」

---

## 파일 경로 (계정 유형별 — 실측 2026-06-19)

| 계정 | 편집 루트 예 | MCP/SFTP |
|------|-------------|----------|
| **일반 몰** (디자인 SFTP) | `/{skin_code}/…` (예: `/skin14/layout/…`) | `cafe24_sftp_*` |
| **파트너 샘플몰** (웹 FTP) | **`/sde_design/base/…`**, `/sde_design/mobile/…` | FTP 클라이언트. 루트에 `/{skin_code}` **없을 수 있음** |

파트너 몰은 API `list_themes` 없이 FTP list로 **실제 폴더**를 먼저 확인.

---

## MCP로 현재값 읽기 (일반 몰)

```text
cafe24_sftp_read path=/{skin_code}/_nk/css/common.css
```

또는 HTML에서 인라인이 아닌 **linked CSS** 확인.

---

## 완료 조건

실측 시트가 **사용자 승인**된 뒤에만 CSS/HTML 패치 시작.
