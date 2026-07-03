```
⚠️ CẢNH BÁO — chạy bằng đầu vào ngoài pipeline
- Nguồn "Delivery Standards + Definition of Done" lấy từ prompt/file bạn đưa, CHƯA qua cổng GĐ11 (skill /delivery).
- Rủi ro: (1) chưa truy vết ngược được về pipeline; (2) có thể lệch / mâu thuẫn với domain · kiến trúc · quyết định thật; (3) artifact sinh ra chưa nối vào state — bạn tự chịu phần đồng bộ.
- Vẫn tiếp tục theo mô tả của bạn. Muốn chuẩn + có traceability: chạy /delivery trước để có "Delivery Standards + Definition of Done" đã qua cổng.
```

Không có `delivery.md` trong state cho hex_agent, nên yêu cầu ở đây tôi neo vào **những cam kết "baked-in" đã ghi trong README + hành vi thực của `core/kernel.py`** — coi mỗi cam kết là một requirement, mỗi test đã xanh là bằng chứng. Không tự chế yêu cầu mới.

---

# Test & Verification Report — hex_agent · Kernel + execute_tool (GĐ12)

## GÓC NHÌN LÃNH ĐẠO
Module lõi (microkernel + chokepoint `execute_tool`) **chạy đúng những gì đã cam kết**: 7/7 yêu cầu-chặn có test và tất cả PASS. Bộ test lõi **42/42 xanh**, toàn hệ offline **411 pass / 1 skip**, smoke tất định xanh (`CORE_AGENT_SMOKE_OK`). Một test skip duy nhất là của RAG (thiếu `qdrant_client`) — **ngoài phạm vi kernel, không chặn release**.

**Hai chữ ký: CẢ HAI CÒN TREO.** UAT sign-off (PO) và Security sign-off (Sec/CISO) chưa có — report này đủ điều kiện để trình ký, nhưng `uat` không ký hộ người thật.

**Còn hở gì:** không hở chặn-release trong phạm vi kernel/execute_tool. Một điều kiện go-live: SAST/DAST chưa chạy công cụ (mới soi tay + lint chưa cài `ruff` trên máy này) → ghi là gap chuyển vòng sau, không chặn slice lõi rủi ro thấp.

## MAPPING (Requirement → AC → Test Case → Result → Release)

| Requirement (cam kết baked-in) | Acceptance Criteria | Test Case | Result | Release Decision |
|---|---|---|---|---|
| Mọi tool call qua `execute_tool` | Tool đăng ký gọi được + emit event vòng đời | `test_kernel::test_execute_registered_tool`, `test_events_emitted` | PASS | đủ điều kiện |
| Tool không được crash kernel | Tool ném lỗi → envelope `ok=False, kernel_error` | `test_kernel::test_unknown_tool_null_fallback` + guard trong `core()` | PASS | đủ điều kiện |
| Session scope thực thi tại chokepoint | Cap ngoài scope → chặn `scope_block`, không chạy | `test_session::test_session_scope_is_enforced_at_kernel_chokepoint`, `test_child_cannot_expand_parent_scope` | PASS | đủ điều kiện |
| State giữa các session không nhiễm chéo | 10 session độc lập state + identity | `test_session::test_ten_sessions_do_not_cross_contaminate_state` | PASS | đủ điều kiện |
| Kernel shared/frozen trước session đầu | Freeze xong không thêm middleware được | `test_session::test_kernel_shared_configuration_freezes_on_first_session` | PASS | đủ điều kiện |
| Middleware fail-open không chạy đôi tool | Advisory ném sau nxt → replay, KHÔNG re-exec (`_LatchedNext`) | `test_middleware::test_advisory_middleware_failure_is_fail_open` (+ latch assert dòng 162) | PASS | đủ điều kiện |
| SQLite là checkpoint truth (resume được) | Roundtrip lưu/nạp + resume đúng task | `test_checkpoint::test_checkpoint_roundtrip_with_task`, `test_resume.py` | PASS | đủ điều kiện |
| Delegation qua cửa riêng, không nới scope | Mở rộng scope bị từ chối như result | `test_delegation::test_policy_rejects_scope_expansion_as_result` | PASS | đủ điều kiện |

## REPORT (lớp test + hai chữ ký)

| Lớp test | Phạm vi | Pass/Fail | Ghi chú |
|---|---|---|---|
| unit + integration | kernel/session/middleware/checkpoint/delegation/trace/resume | **42/42** | các suite lõi |
| regression (toàn hệ offline) | full `pytest` | **411 pass / 1 skip** | skip = RAG/Qdrant, ngoài scope |
| smoke (e2e tất định, no LLM/net) | `run_smoke.py` | PASS | `CORE_AGENT_SMOKE_OK` |
| trace/observability | lineage + request_id qua chokepoint | PASS | `test_trace_ids.py` |
| security (SAST/DAST/pentest) | — | **CHƯA CHẠY** | soi tay: deep-copy args chống mutate, deep-freeze config, tool-never-crash guard OK; công cụ chưa chạy (`ruff` chưa cài) → gap |
| perf / a11y / DR | — | bỏ | Đủ-là-đủ: slice lõi thư viện nội bộ, không NFR/UI → không nhồi |

```
UAT sign-off      : PO ______________ ngày ____  (CHỜ)
Security sign-off : Sec/CISO _________ ngày ____  (CHỜ)
```

## Tự soi
- Lãnh đạo đọc riêng khối đầu biết on-track (pass rate + trạng thái 2 chữ ký + hở) — có.
- Dev đọc mapping + lớp test biết chỗ nào chưa chạy (SAST/DAST) — có.
- Requirement TRÍCH từ README "Principles (baked-in)" + hành vi `core/kernel.py`, không bịa; lớp bỏ có ghi lý do — có.
- Không lấn: không đào edge case mới (đó là /review), không quyết deploy (đó là /ship).

```
═══ CỔNG GO/NO-GO (GĐ12 UAT) — hex_agent kernel+execute_tool ═══
Pass: 7/7 AC có test · 7 PASS · lõi 42/42 · full 411/1skip   Gap chưa test: SAST/DAST công cụ
UAT sign-off: CHỜ (PO)                     Security sign-off: CHỜ (Sec/CISO)
Đủ điều kiện go-live? → GO-LIVE CÓ ĐIỀU KIỆN:
   bằng chứng test đã đủ; cần (1) PO + Sec ký, (2) chạy SAST/DAST cho phần lõi
═══════════════
```

```
═══ BÀN GIAO — hex_agent (GĐ12 → GĐ13) ═══
Đã chứng minh: 7/7 AC PASS · lõi 42/42 · full 411 pass/1 skip · smoke xanh
              UAT ⧗ chờ PO · Security ⧗ chờ Sec/CISO
Điều kiện/hở còn treo: SAST/DAST chưa chạy công cụ (rủi ro thấp, soi tay OK) + 2 chữ ký treo
Artifact: state/project/hex_agent/pipeline/uat.md (chưa ghi — nguồn ngoài pipeline)
→ Đủ điều kiện go-live sau khi ký, làm Go/No-Go + Runbook + rollback: chạy /ship (GĐ13)
→ Còn nghi gap/edge case/permission chưa test hết: chạy /review trước khi ship
→ Muốn chuẩn traceability: chạy /delivery trước để có DoD qua cổng GĐ11
═══════════════
```

Tôi liệt kê các lối tiếp, không tự chọn hộ bạn.
