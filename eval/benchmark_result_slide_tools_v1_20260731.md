# BỘ CÂU THỬ LAB COACH & KẾT QUẢ LƯỢT ĐẦU

* **Sản phẩm:** VLearn AI Research Agent
* **Bộ eval:** `data/eval_group.json`
* **Dataset ID:** `vlearn_frontend_slide_tool_labcoach_v1`
* **Run ID:** `slide-tools-v1_B_group_openai_20260731T101454184740`
* **Provider / Model:** OpenAI / `gpt-4.1-mini`
* **Phạm vi:** 24 câu lạ Lab Coach có thể gõ trực tiếp; bám slide Day 1/Day 2 trên Frontend và kiểm tra tool routing + arguments.

---

## 1. TIÊU CHÍ ĐÁNH GIÁ

1. **Tool Routing Accuracy:** Agent chọn đúng tool hoặc đúng `no_tool`.
2. **Argument Accuracy:** Các argument bắt buộc trong golden set xuất hiện đúng trong tool call.
3. **Boundary Accuracy:** Không gọi tool khi user chỉ yêu cầu soạn nháp; chỉ gọi `send` sau xác nhận.
4. **Multi-turn Accuracy:** Agent chỉ hành động theo yêu cầu mới nhất nhưng vẫn dùng đúng ngữ cảnh slide từ lượt trước.

---

## 2. BẢNG KẾT QUẢ LƯỢT ĐẦU

| ID | Slide Frontend | Câu thử Lab Coach (rút gọn) | Tool kỳ vọng | Tool thực tế | Kết quả |
|---|---|---|---|---|:---:|
| TC01 | D1 p25 | Tra xu hướng giá API model 2026 | `lookup` | `lookup` | **PASS** |
| TC02 | D1 p8,15 | Tìm paper về attention interpretability | `papers` | `papers` | **PASS** |
| TC03 | D2 p16 | Đọc URL Building effective agents | `fetch` | `fetch` | **PASS** |
| TC04 | D1 p23 | Tìm social Latest về tools + memory | `social_search` | `social_search` | **PASS** |
| TC05 | D1 p20 | Lấy ba bài gần đây của SamAltman | `timeline` | `timeline` | **PASS** |
| TC06 | D1 p20 | Tra policy nội bộ về trích nguồn | `policy` | `policy` | **PASS** |
| TC07 | D2 p11–28 | Hỏi lựa chọn khi chủ đề còn mơ hồ | `clarify` | `clarify` | **PASS** |
| TC08 | D1 p27 | Format dữ liệu token thành brief | `format` | `format` | **PASS** |
| TC09 | D2 p24 | Chỉ soạn nháp, tuyệt đối chưa gửi | `no_tool` | `lookup` | **FAIL** |
| TC10 | D1 p20 | Tìm tin model mới trong tuần | `lookup` | `lookup` | **PASS** |
| TC11 | D1 p14 | Tìm paper Lost in the Middle | `papers` | `papers` | **PASS** |
| TC12 | D1 p22 | Đọc paper CoT từ URL arXiv cụ thể | `paper_text` | `fetch` | **FAIL** |
| TC13 | D1 p7 | Fact-check con số ImageNet | `lookup` | `lookup` | **PASS** |
| TC14 | D1 p28 | Tìm social Top về bốn lớp prompt | `social_search` | `social_search` | **PASS** |
| TC15 | D2 p18 | Lấy timeline AndrewYNg | `timeline` | `timeline` + `lookup` | **FAIL** |
| TC16 | D2 p17 | Tra policy dữ liệu học viên | `policy` | `policy` | **PASS** |
| TC17 | D1 p18–19 | Tìm paper so sánh RLHF và DPO | `papers` | `papers` | **PASS** |
| TC18 | D1 p27 | Tìm cập nhật giá token trong tháng | `lookup` | `lookup` | **PASS** |
| TC19 | D2 p9–10,28 | Hỏi actor và workflow trước khi đánh giá Go/No-Go | `clarify` | `clarify` | **PASS** |
| TC20 | D1 p20,23–27 | Format digest AI tiếng Việt | `format` | `format` | **PASS** |
| TC21 | D2 p23 | Multi-turn: tìm ví dụ precision/recall mới | `lookup` | `lookup` | **PASS** |
| TC22 | D2 p25–26 | Multi-turn: tìm paper benchmark agent | `papers` | `papers` | **PASS** |
| TC23 | D1 p14 | Multi-turn: đọc full text Lost in the Middle | `paper_text` | `paper_text` | **PASS** |
| TC24 | D2 p24 | Multi-turn: đã duyệt, gửi cảnh báo metric | `send(confirmed=true)` | `send(confirmed=true)` | **PASS** |

---

## 3. TỔNG KẾT LƯỢT ĐẦU

* **Tổng số test cases:** 24
* **Measured cases:** 24/24
* **Provider errors:** 0
* **Passed cases:** 21/24
* **Case Accuracy:** 87.5%
* **Tool Routing Accuracy:** 87.5%
* **Argument Accuracy:** 87.5%
* **Multi-turn Accuracy:** 100%

### Failure Analysis

1. **TC09 — sai boundary:** User nói rõ “chưa gửi hay publish”, nhưng agent vẫn gọi `lookup`. Cần thêm rule: yêu cầu chỉ soạn nháp phải trả lời trực tiếp và không gọi tool hành động/tìm kiếm không cần thiết.
2. **TC12 — nhầm tool:** Có URL arXiv cụ thể và yêu cầu đọc paper nhưng agent chọn `fetch` thay vì `paper_text`. Cần mô tả rõ ưu tiên `paper_text` cho URL/ID arXiv; `fetch` dành cho URL web thông thường.
3. **TC15 — gọi dư tool:** Agent gọi đúng `timeline` nhưng gọi thêm `lookup`. Cần rule “tài khoản cụ thể → chỉ timeline; không web lookup nếu user không yêu cầu”.

### Kết luận

Baseline hợp lệ vì toàn bộ 24 case đều được provider đo và không có provider error. Bộ eval đã bao phủ đủ 10 tool, `no_tool`, single-turn, multi-turn, argument routing và ranh giới xác nhận trước hành động bên ngoài.
