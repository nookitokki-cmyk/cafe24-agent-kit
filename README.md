> ✅ **단일 기준(THE ONE) · v2.4.0 · 2026-06-21** — 이 폴더(`C:\dev\cafe24-agent-kit`)가 유일한 진짜 키트입니다. 다른 사본은 `_archive` 보관소(사용 금지). 현재 상태는 [`_dev/meta/__지금상태_STATUS.md`](_dev/meta/__지금상태_STATUS.md) 참고.

# cafe24-agent-kit

카페24 **두뇌(agent-kit)** + **손발(mcp)** 단일 기준 저장소. (이 README는 30초 오리엔테이션용입니다.)

> 🆕 **v2.4.0 (2026-06-21)** — cafe24 skill 대폭 확장 (45개 신규 파일): 모듈 레시피북·페이지 템플릿·스니펫·Design Token·Brand Profile·원클릭 자동화 명령. 일부 자료는 🧪 **실험적** 표시 — 실 클라이언트 검증 후 안정화 예정. **안정 자료**(✅: troubleshooting, variables, recipes, module-browser)부터 도입 권장. 상세 → [`CHANGELOG.md`](CHANGELOG.md) v2.4.0 / [`agent-kit/README.md`](agent-kit/README.md) "🆕 v2.4.0 신규 자료" 섹션.

## ▶ 시작은 여기부터

**[`agent-kit/README.md`](agent-kit/README.md) — 단일 진입점.** 명령표·폴더맵·온보딩 순서가 모두 여기 있습니다.

1. 이 폴더를 Cursor에서 연다  
2. **[`agent-kit/README.md`](agent-kit/README.md)** 를 펼친다 (명령어·폴더맵·다음 단계)

> 명령어 표는 중복을 막기 위해 [`agent-kit/README.md`](agent-kit/README.md)에 한 곳으로 모았습니다.

## 검증

```bash
bash agent-kit/connect/scripts/verify-kit.sh    # 구조·문서 29항목
bash agent-kit/connect/scripts/verify-live.sh   # 운영 MCP smoke 5/5 (토큰 필요)
```

## 문서

- 공식 대조: `agent-kit/brain/docs/OFFICIAL-AUDIT.md`
- API 튜토리얼: `agent-kit/connect/MCP-OAUTH-GUIDE.md`
- 복제 기록: `_dev/meta/MANIFEST.txt`
