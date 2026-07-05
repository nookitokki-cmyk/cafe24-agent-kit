# Wave4 그룹 오케스트레이션 (기술 보조)

> **페이지당 1 에이전트**가 1차. 이 문서는 **파일 충돌 방지·FTP 직렬·4-tier 게이트**용.

클라이언트 정본: `clients/{몰}/.omc/specs/wave4-orchestration-plan.md` · `04_design/wave4-group-matrix.md`

## 그룹 ↔ 페이지 타입

| Group | 타입 | 하위 에이전트 배치 단위 |
|-------|------|------------------------|
| G1 | 메인 | `/` + header/footer inc |
| G2 | PLP | list · search · recent |
| G3 | PDP | detail + submodule URL |
| G4 | auth-order | login · basket |
| G5 | board | 28+ URL (타입별 또는 URL별 brief) |
| G6 | myshop · member · etc | 21+8+7 URL |
| G7 | popup · fragment | popup 45+ |
| G8 | Final | ultraqa · status 193행 |

## Single writer (충돌 방지)

| 파일 | 독점 그룹 |
|------|-----------|
| `nk-pdp.css` | G3 |
| `nk-member.css` | G4 → G6 member |
| `nk-header.html` · `main.html` | G1 PASS 전 타입 금지 |
| `nk-tokens.css` | G0 승인 후 1 writer |

## 페이지 에이전트와의 관계

- **page-agent-orchestration.md**: 무엇을·누가·언제 (Human gate · brief · module 계약)
- **본 문서 + wave4-orchestration-plan**: 어떤 파일을 동시에 못 만지는지 (mutex)
