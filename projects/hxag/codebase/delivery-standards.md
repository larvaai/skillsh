# Delivery Standards + DoD — HexAgent (GĐ11 BUILD)

> Chuẩn giao hàng một lần cho mọi team. Nguồn: `rebuild-hex-agent/pipeline/11-delivery.md`.

## Standards
- **Repo/branch:** trunk + short-lived feature branch; 1 PR = 1 slice trỏ về story + AC.
- **Coding:** Python 3.11, UTF-8 no BOM, `@dataclass(frozen=True)` cho envelope, ports = `Protocol` (runtime_checkable), lazy LLM client.
- **CI/CD gates:** ruff + mypy + `pytest` (unit + Hypothesis property + audit-adversarial); smoke offline `run_smoke.py` phải OK.
- **Test pyramid:** unit (nhanh, offline) → property (invariant) → audit (đối kháng). Test skip nếu Qdrant unreachable (offline-first).
- **Secret:** redact tại biên; cấm log raw args khi write-tool bật (contract Observability).

## Definition of Done (DoD — biến 5 lời hứa thành cổng cứng kiểm-được)
| # | DoD | Test |
|---|---|---|
| D1 | Không call-site nào bypass `execute_tool` | audit-test grep 0 đường vòng |
| D2 | Scope child ⊆ parent | property-test (Hypothesis) fail-closed |
| D3 | Resume round-trip xanh cùng run_id (SPIKE-1) | integration resume test |
| D4 | 0 secret trong `ui_payload` (redact-before-write) | audit-test 0-secret + G3 freeze-gate |
| D5 | Worker không set verdict; evidence có provenance (G1) | property-test acceptance |

## PR Checklist
- [ ] Trỏ story + AC; [ ] test cho AC; [ ] không bypass execute_tool; [ ] scope khai tối thiểu; [ ] không log secret; [ ] events.jsonl sạch.

## Cổng GĐ11: đạt DoD/chuẩn đủ? → GO (DoD là cổng cứng cho mọi module build).
