# C · Do/Don't theo mức

## editSummary
Sửa vào bảng "Mức hiểu" của explain/SKILL.md (BƯỚC 2, hướng C). Dưới mỗi mức L0–L4 thêm ĐÚNG MỘT dòng "Do/Don't" nêu rõ được nói / cấm nói loại thuật ngữ nào — mục tiêu chặn model lỡ thả tên hàm/file/số dòng dưới ngưỡng mức cho phép (nhắm tiêu chí 1 Mức, tiêu chí xương sống). Sửa tối thiểu: chỉ chèn 5 dòng, không đụng thang zoom, luật neo, hay các bước. Output đóng vai bản ĐÃ SỬA ở fixture L3/overview: neo mọi thuật ngữ vào bước luồng trước khi gọi tên, được nhắc tên module + entrypoint (orchestrator.run) + cửa đã neo (execute_tool), nhưng KHÔNG số dòng / chữ ký hàm / tên biến / chi tiết middleware — đúng dòng Do/Don't của L3.

## changedSections
Chèn thêm một dòng "Do/Don't" (bắt đầu bằng "  Do/Don't:") ngay dưới phần mô tả của mỗi mức L0–L4 trong khối "## Mức hiểu — quyết DỪNG Ở TẦNG ZOOM NÀO". Bản sau chèn:

L0 locate    — Chưa biết code nằm ở đâu
  Dừng ở: Zoom 0–1. Ngôn ngữ đời thường, không thuật ngữ, không tên code.
  Do/Don't: được nói tên miền nghiệp vụ ("trợ lý tự chạy", "giao việc con"). CẤM mọi tên code, tên file, tên module, tên hàm.
  Gợi ý: "Bạn muốn hiểu app này làm gì, hay muốn biết mình nên đọc file nào trước?"

L1 scout     — Biết file liên quan, chưa hiểu logic
  Dừng ở: Zoom 1. Thuật ngữ nghiệp vụ, tên tính năng. Không nhắc code.
  Do/Don't: được nói tên TÍNH NĂNG ("delegation", "observability") như khái niệm nghiệp vụ. CẤM tên hàm/file/class và tên định danh code (vd `execute_tool`, `kernel.py`).
  Gợi ý: "Bạn muốn tôi giải thích nghiệp vụ, hay muốn biết tính năng nào quan trọng nhất?"

L2 map       — Hiểu nghiệp vụ, chưa hiểu code flow
  Dừng ở: Zoom 2 (bản đồ luồng). Neo entrypoint + luồng chính; tên module chỉ như gợi ý.
  Do/Don't: được nhắc ENTRYPOINT + tên cửa/chokepoint đã neo trong luồng. CẤM số dòng, chữ ký hàm, tên biến, chi tiết middleware/codec.
  Gợi ý: "Bạn muốn đi qua luồng chạy từng bước, hay có một luồng cụ thể bạn muốn xem trước?"

L3 flow      — Hiểu entrypoint và happy path
  Dừng ở: Zoom 2 kỹ + chạm Zoom 3. Trách nhiệm từng module/class, data flow cơ bản.
             Mỗi thuật ngữ code neo vào bước trong luồng trước khi gọi tên.
  Do/Don't: được nói tên MODULE/THƯ MỤC + entrypoint + tên chokepoint đã neo (vd `execute_tool`). CẤM số dòng, chữ ký hàm đầy đủ, tên biến nội bộ, chi tiết middleware/codec.
  Gợi ý: "Bạn muốn tôi giải thích trách nhiệm từng phần, hay có module nào bạn đang thắc mắc?"

L4 structure — Hiểu responsibility từng phần ✓ Ngưỡng làm việc được
  Dừng ở: Zoom 3 đầy đủ. Trả lời thẳng vào câu hỏi, không giải thích từ đầu. Xem như đồng nghiệp.
  Do/Don't: được nói tên hàm + chữ ký + trích code khi cần (level ≥ L4). Vẫn CẤM trích số dòng vô ích khi không load-bearing.
  Gợi ý: "Bạn đang cần thêm tính năng, sửa bug, hay muốn hiểu lý do thiết kế của một phần?"

## output (nguyên văn)
Bạn đang ở L3 (hiểu entrypoint + happy path), nên mình đi kỹ luồng chạy rồi chạm nhẹ vào các module. Theo dòng Do/Don't của L3 mình mới thêm: mình sẽ gọi tên thư mục, entrypoint, và đúng những "cái cửa" sau khi đã chỉ chỗ nó đứng trong luồng — không quăng số dòng hay chữ ký hàm.

Nói một câu: đây là một cái khung để chạy "trợ lý AI tự làm việc" — nhận một việc, tự nghĩ, tự gọi công cụ, tự giao bớt cho trợ lý con, rồi trả kết quả — mà không để nó chạy loạn.

Vấn đề nó giải, cho ai: khi một agent được tự gọi LLM và tự đụng vào file/terminal, hai thứ dễ vỡ là AN TOÀN (nó làm gì ngoài ý muốn?) và KHÔI PHỤC (chạy nửa chừng chết thì sao?). Người hưởng lợi là dev dựng hệ multi-agent: họ cần một chỗ để nhìn, chặn, và tua lại mọi hành động. Ý tưởng cốt lõi: bắt MỌI hành động đi qua đúng một cánh cửa, và ghi trạng thái xuống một nguồn sự thật bền — nhờ vậy mọi thứ đều quan sát được, chặn được, tua lại được.

Luồng "bạn ở đây" — một việc chạy từ vào tới ra (đây là bản đồ để định vị mọi thứ sau đó):

1. Ai đó gọi facade công khai để bắt đầu — entrypoint là `run()`/`resume()` trong `orchestrator/loop.py`. Đây là cửa vào ổn định, dùng cái này.
2. Facade nạp một đồ thị điều phối đã biên dịch (một substrate LangGraph duy nhất). Đồ thị chỉ lo thứ tự các bước; phần lõi không dính vào framework đó.
3. Một node "guard" chặn trước mỗi bước: hết ngân sách bước thì cho fail luôn, còn không thì cho agent nghĩ tiếp.
4. Node "agent" gọi LLM để lấy ĐÚNG MỘT hành động kế tiếp. Điểm mấu chốt: LLM ở đây cũng chỉ là một "công cụ" (`llm.chat`), không có đường tắt — nó đi qua cùng cánh cửa như mọi công cụ khác.
5. Tuỳ hành động, đồ thị rẽ sang chạy một công cụ (đọc/ghi file, chạy lệnh), hoặc GIAO VIỆC cho một agent con, hoặc kết thúc.
6. Bước 4 và 5 — cái cửa duy nhất mọi lời gọi LLM và công cụ phải chui qua — code gọi là `AgentKernel.execute_tool` (trong `core/`). Trước khi chạy, nó phát sự kiện "đã yêu cầu", kiểm tra công cụ này có nằm trong phạm vi được phép của phiên không, rồi mới chạy và phát "đã xong / thất bại". Đây chính là chỗ để quan sát và chặn — trả lời cho phần "an toàn" ở trên.
7. Riêng việc GIAO VIỆC cho agent con đi một cửa RIÊNG, cố ý tách khỏi cửa trên — nên trong đồ thị có hẳn một node `delegate` riêng, không dính vào kernel.
8. Sau mỗi bước, trạng thái được ghi xuống một file SQLite trong `var/agent_runs/<run_id>/`. Đây là nguồn sự thật để `resume()` tua lại đúng chỗ khi chạy dở — trả lời cho phần "khôi phục".

Điểm danh các phần (mỗi cái là một chỗ trong luồng trên):

- `orchestrator/` — cửa vào ở bước 1 (`run`/`resume`) và chỗ mở SQLite ở bước 8. File `checkpoint.json` chỉ là bản chiếu cho UI xem, không phải nguồn tua lại — nguồn tua lại là SQLite.
- `graph/` — cái đồ thị điều phối ở bước 2–5: các node (guard/agent/tool/delegate/finish) và runtime biên dịch chúng. Mọi hành động bên ngoài ở đây vẫn phải chui qua cửa `execute_tool`.
- `core/` — cái microkernel: chính là cánh cửa duy nhất ở bước 6 (`execute_tool`), cộng registry (tên công cụ → chỗ chạy nó), state và session của một lần chạy. Phần này cố ý KHÔNG biết gì về LangGraph.
- `delegation/` — cái cửa riêng ở bước 7: một manager tuần tự lo policy (giới hạn độ sâu, ngân sách, và phạm vi quyền của con không vượt cha), tạo phiên con, ghi tiến độ.
- `discipline/` — mấy cái "phanh" dùng chung ở bước 3–5: ngân sách vòng lặp, cổng đọc JSON hành động của model, và finish gate (chặn "xong" nếu đã đổi code mà chưa validate).
- Vòng ngoài của cửa `execute_tool` còn có lớp an toàn (`safety/` — nhốt đường dẫn trong workspace) và các lớp cross-cutting (`middleware/` — như deny-list, đo thời gian) và ghi nhật ký (`observability/`) — tất cả bám vào đúng cánh cửa ở bước 6 để quan sát/chặn tập trung.

Tóm lại giá trị: nhờ dồn mọi hành động vào một cửa (cộng cửa giao-việc tách riêng) và một nguồn checkpoint bền, hệ này giữ được ba thứ dev cần ở một khung multi-agent — nhìn được, chặn được, tua lại được.

Bạn đang ở L3 rồi — bước tiếp tự nhiên: bạn muốn mình đi sâu trách nhiệm của một phần cụ thể (vd bên trong cửa `execute_tool`, hay cửa delegation), hay có module nào bạn đang thắc mắc trước?
