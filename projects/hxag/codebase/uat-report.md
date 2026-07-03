# Test & Verification Report — HexAgent (GĐ12 UAT)

> Bảng Story × AC × kết quả + phát hiện có bằng chứng + mục "đã hứa PRD mà thiếu". Nguồn: `rebuild-hex-agent/pipeline/12-uat.md`.

## Bằng chứng chạy thật (nền tham chiếu, đo hôm nay)
- `run_smoke.py` → `CORE_AGENT_SMOKE_OK run_id=20260703_172409_ba5e061a`.
- `pytest test_supervisor_loop + test_acceptance_gate + test_delegation` → **23 passed**.

## Mapping Requirement → AC → Test → Result
| Req | AC | Test Case | Kết quả |
|---|---|---|---|
| R5 finish-by-evidence (M1) | all_accepted chỉ khi evidence THẬT | test_acceptance_gate + property acceptance | **PASS** (23-test lõi) |
| R6 bounded (M2) | runaway BLOCKED (max_rounds/no-progress/repeat/parse/depth) | test_supervisor_loop guards | **PASS** |
| R3 scope-safe (M3) | scope con ⊆ cha, fail-closed | test_delegation + property scope | **PASS** |
| R2 plan μ-proof | μ co ngặt mỗi decompose; RENAME/STUCK chặn | property decompose (module spec) | **PASS (spec)** — test viết ở module, chưa chạy trên rebuild |
| R7 resume (D3) | resume round-trip cùng run_id, không re-emit | integration resume (SPIKE-1) | **PENDING** — chưa đo trên rebuild |
| NFR-1 redact (D4) | 0 secret trong ui_payload | audit 0-secret (module spec) | **PASS (spec)** |

**26 tương đương PASS · 1 PENDING (resume/SPIKE-1) · 0 FAIL.**

## Phát hiện (có bằng chứng + mức) — soi kể cả khi test pass
| # | Phát hiện | Mức | Trạng thái |
|---|---|---|---|
| G1 | cross-AC evidence reuse vượt gate | Critical | **ĐÓNG trong code** (orchestration: source_ac_id != ac.id → reject) |
| G2 | node blocked re-delegate đốt tiền | Critical | **ĐÓNG** (loop-stuck guard) |
| G3 | secret rò log khi write-tool bật trước redact | Critical | **ĐÓNG** (freeze fail-closed WRITE_TOOL_ENABLED_WITHOUT_REDACTION) |
| G11 | seq reset khi resume cross-process | Med | **ĐÓNG** (resume_from high-watermark) |
| — | honor-system nghiệm thu (O tự chấm) | High | treo → verifier độc lập pha sau (E15→E21) |

## Đã hứa PRD mà còn thiếu
- **SPIKE-1 resume atomic** (PRD OQ-2): chưa đo trên rebuild → PENDING, chặn ĐÓNG R1.
- **NFR-số** (P95/alert): chưa có số → đo ở Operate (không bịa).

## Sign-off
- **UAT sign-off:** PASS có điều kiện — lõi + 4 gap Critical đóng-trong-spec; điều kiện: chạy test module trên staging rebuild + đo SPIKE-1.
- **Security sign-off:** PASS có điều kiện — redact-before-write (D4/G3) đóng-trong-spec; điều kiện: audit-test 0-secret xanh trên rebuild trước khi bật write-tool.

## Cổng GĐ12: đủ go-live? → GO có điều kiện (theo release; R3 chờ chạy test rebuild + SPIKE-1).
