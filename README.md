# tri-tue-nhan-tao

# Báo cáo Đồ án Cá nhân Trí tuệ Nhân tạo

## Đề tài: Giải bài toán 8-Puzzle bằng các thuật toán tìm kiếm

Giảng viên hướng dẫn: Cô Phan Thị Huyền Trang

Sinh viên thực hiện: Nguyễn Nguyên - 24110289

Ngày báo cáo: Tháng 06 năm 2026

## 1. Mục tiêu
Mục tiêu của dự án này là xây dựng một ứng dụng mô phỏng việc giải trò chơi 8-Puzzle bằng cách áp dụng và trực quan hóa hiệu quả của các thuật toán tìm kiếm khác nhau trong Trí tuệ Nhân tạo. Ứng dụng cung cấp giao diện đồ họa trực quan (PyQt5) để người dùng nhập trạng thái ban đầu và trạng thái đích, chọn thuật toán, xem quá trình giải từng bước, theo dõi biên tìm kiếm (frontier) / danh sách đã duyệt (explored), và so sánh hiệu suất giữa các thuật toán thông qua các chỉ số thống kê thời gian thực.

## 2. Nội dung
### 2.1. Các thuật toán Tìm kiếm không có thông tin (Uninformed Search)
**Khái niệm bài toán tìm kiếm và lời giải:**
Trong bối cảnh trò chơi 8-Puzzle, bài toán tìm kiếm được định nghĩa như sau:

- **Trạng thái (State):** Một cấu hình cụ thể của bảng 3x3, biểu diễn vị trí của 8 ô số (từ 1 đến 8) và ô trống (ký hiệu là 0). Ví dụ: `((1, 2, 3), (4, 0, 5), (6, 7, 8))`.
- **Hành động (Action):** Các di chuyển hợp lệ của ô trống: Lên (Up), Xuống (Down), Trái (Left), Phải (Right).
- **Môi trường (Environment):** Tập hợp tất cả các trạng thái có thể đạt được từ trạng thái ban đầu bằng cách áp dụng các hành động hợp lệ.
- **Trạng thái ban đầu (Initial State):** Cấu hình bắt đầu của bảng 8-Puzzle do người dùng tự nhập hoặc được tạo ngẫu nhiên.
- **Trạng thái đích (Goal State):** Cấu hình mong muốn của bảng 8-Puzzle (thường là các số được sắp xếp theo thứ tự từ 1 đến 8 và ô trống ở cuối hoặc ở giữa tùy cấu hình).
- **Chi phí bước đi (Step Cost):** Chi phí để thực hiện một hành động (thường mặc định là 1 cho mỗi bước di chuyển).
- **Lời giải (Solution):** Một chuỗi các hành động di chuyển từ trạng thái ban đầu dẫn đến trạng thái đích. Lời giải tối ưu là lời giải có tổng chi phí bước đi thấp nhất (tức chuỗi di chuyển ngắn nhất).

**Các thuật toán Tìm kiếm không có thông tin đã triển khai:**
Nhóm thuật toán này tìm kiếm lời giải mà không sử dụng bất kỳ thông tin bổ trợ nào về "độ gần" hay ước lượng khoảng cách từ trạng thái hiện tại đến trạng thái đích. Chúng duyệt không gian trạng thái một cách hệ thống dựa trên cấu trúc cây tìm kiếm. Các thuật toán được triển khai bao gồm:

- **BFS (Breadth-First Search):** Tìm kiếm theo chiều rộng.
- **DFS (Depth-First Search):** Tìm kiếm theo chiều sâu.
- **UCS (Uniform-Cost Search):** Tìm kiếm chi phí đồng nhất.
- **IDS (Iterative Deepening Search):** Tìm kiếm sâu dần.

**Ưu điểm, Nhược điểm và Hiệu suất:**

* **BFS (Breadth-First Search):**
  BFS khám phá không gian tìm kiếm theo từng lớp, mở rộng tất cả các node ở độ sâu $k$ trước khi chuyển sang độ sâu $k+1$.
  - *Cấu trúc dữ liệu:* Sử dụng hàng đợi **FIFO (First-In-First-Out)** qua `collections.deque` làm biên tìm kiếm (`frontier`).
  - *Ưu điểm:* Đảm bảo tính đầy đủ (completeness) và tính tối ưu (optimality) - luôn tìm ra lời giải ngắn nhất khi chi phí bước đi bằng nhau.
  - *Nhược điểm:* Yêu cầu lượng bộ nhớ rất lớn $O(b^d)$ để lưu trữ biên tìm kiếm và các trạng thái đã xét, dễ gây tràn bộ nhớ khi độ sâu lớn.

  **Hình ảnh minh họa quá trình chạy BFS:**
  
  <video src="https://github.com/user-attachments/assets/4699db84-3ad6-4cc1-9e07-efbf14314b29" controls muted style="max-width: 100%;"></video>




* **DFS (Depth-First Search):**
  DFS khám phá không gian tìm kiếm theo nhánh sâu nhất có thể trước khi thực hiện quay lui (backtracking).
  - *Cấu trúc dữ liệu:* Sử dụng ngăn xếp **LIFO (Last-In-First-Out)** qua danh sách Python (`pop()`).
  - *Ưu điểm:* Tiết kiệm bộ nhớ hơn BFS rất nhiều, độ phức tạp không gian chỉ là tuyến tính $O(b \cdot m)$ theo độ sâu.
  - *Nhược điểm:* Không đảm bảo tính đầy đủ trên không gian vô hạn (ứng dụng giới hạn tối đa 3000 bước để tránh lặp vô hạn) và không đảm bảo tối ưu (đường đi thường rất dài).

* **UCS (Uniform-Cost Search):**
  UCS mở rộng các nút dựa trên tổng chi phí từ trạng thái ban đầu đến trạng thái hiện tại.
  - *Cấu trúc dữ liệu:* Hàng đợi ưu tiên **Min-Heap** thông qua `heapq`.
  - *Đặc điểm trong mã nguồn:* Trong chương trình này, UCS được cấu hình đặc biệt sử dụng hàm Heuristic **Misplaced Tiles** làm độ ưu tiên để sắp xếp trong Min-Heap, hoạt động tương đương với **Greedy Best-First Search**.
  - *Ưu điểm:* Ưu tiên mở rộng trạng thái có ít ô sai lệch nhất trước để tiến nhanh đến đích.
  - *Nhược điểm:* Với cấu hình heuristic này, thuật toán không đảm bảo tính tối ưu (đường đi ngắn nhất).

* **IDS (Iterative Deepening Search):**
  IDS kết hợp ưu thế bộ nhớ của DFS và tính tối ưu của BFS bằng cách thực hiện tìm kiếm giới hạn độ sâu (DLS) lặp lại với giới hạn tăng dần từ 0, 1, 2...
  - *Cơ chế chống lặp:* Thực hiện kiểm tra chu trình trên nhánh hiện tại (`is_cycle = state in path[:-1]`).
  - *Ưu điểm:* Đầy đủ và tối ưu giống BFS, nhưng bộ nhớ cực thấp chỉ $O(b \cdot d)$.
  - *Nhược điểm:* Trùng lặp việc mở rộng các node ở độ sâu nông nhiều lần, tốn thời gian chạy hơn BFS một chút.

---

### 2.2. Các thuật toán Tìm kiếm có thông tin (Informed Search)
**Khái niệm bài toán tìm kiếm và lời giải:**
Tương tự tìm kiếm không có thông tin, nhưng nhóm thuật toán này sử dụng thêm hàm heuristic $h(n)$ để ước lượng chi phí còn lại từ trạng thái hiện tại đến đích. Hàm này định hướng tìm kiếm thông minh hơn. Dự án triển khai hai heuristic chính:
- **Heuristic Manhattan Distance:** Tổng khoảng cách di chuyển tối thiểu theo lưới của các ô số đến vị trí đích của chúng.
- **Heuristic Misplaced Tiles:** Số lượng ô nằm sai vị trí so với trạng thái đích.

**Các thuật toán Tìm kiếm có thông tin đã triển khai:**
- **A\* Search (A-Star):** Mở rộng node dựa trên tổng chi phí đánh giá $f(n) = g(n) + h(n)$ (trong đó $g(n)$ là chi phí thực tế từ trạng thái ban đầu, và $h(n)$ là ước lượng heuristic đến đích).
- **IDA\* Search (Iterative Deepening A\*):** Kết hợp A\* với cơ chế duyệt sâu dần dựa trên ngưỡng chi phí $f(n)$.

**Ưu điểm, Nhược điểm và Hiệu suất:**

* **A\* Search:**
  A\* đánh giá node bằng hàm $f(n) = g(n) + h(n)$ với $g(n)$ tính theo khoảng cách Manhattan và $h(n)$ theo misplaced tiles.
  - *Cấu trúc dữ liệu:* Hàng đợi ưu tiên **Min-Heap** (`heapq`).
  - *Ưu điểm:* Hoàn chỉnh và tối ưu (nếu heuristic chấp nhận được). Cực kỳ hiệu quả, duyệt ít node hơn rất nhiều so với BFS/UCS.
  - *Nhược điểm:* Yêu cầu bộ nhớ lớn để lưu trữ frontier và tập đã duyệt, có thể cạn kiệt tài nguyên trong các bài toán cực kỳ phức tạp.

* **IDA\* Search:**
  IDA\* duyệt DFS với giới hạn ngưỡng chi phí $f$. Khi một chu kỳ tìm kiếm kết thúc mà chưa gặp đích, ngưỡng mới sẽ là giá trị $f$ nhỏ nhất vượt quá ngưỡng cũ.
  - *Ưu điểm:* Đảm bảo tối ưu và đầy đủ giống A\* nhưng khắc phục triệt để điểm yếu bộ nhớ bằng cách chỉ lưu trữ nhánh duyệt hiện tại (độ phức tạp bộ nhớ tuyến tính $O(d)$).
  - *Nhược điểm:* Có thể lặp lại việc duyệt một số node ở các vòng lặp trước, tăng thời gian tính toán CPU.

---

### 2.3. Các thuật toán Tìm kiếm cục bộ (Local Search)
**Khái niệm bài toán tìm kiếm và lời giải:**
Tìm kiếm cục bộ chỉ hoạt động trên trạng thái hiện tại và các trạng thái lân cận của nó thay vì xây dựng cây tìm kiếm lớn. Lời giải thu được là trạng thái đích tìm thấy, đường đi là chuỗi các bước di chuyển cục bộ kế tiếp nhau. Hàm heuristic chính được sử dụng để đánh giá độ tốt của trạng thái là khoảng cách Manhattan.

**Các thuật toán Tìm kiếm cục bộ đã triển khai:**
- **Simple Hill Climbing:** Di chuyển đến trạng thái lân cận đầu tiên tốt hơn trạng thái hiện tại.
- **Steepest-Ascent Hill Climbing:** Đánh giá toàn bộ lân cận và di chuyển đến trạng thái tốt nhất.
- **Stochastic Hill Climbing:** Chọn ngẫu nhiên một trạng thái từ tập hợp các lân cận tốt hơn.
- **Random Restart Hill Climbing:** Khởi động lại thuật toán leo đồi từ một trạng thái ngẫu nhiên mới nếu bị kẹt ở cực trị cục bộ.
- **Local Beam Search (k = 4):** Duy trì và mở rộng song song tập hợp $k$ trạng thái tốt nhất.

**Ưu điểm, Nhược điểm và Hiệu suất:**

* **Simple Hill Climbing:**
  - *Ưu điểm:* Cực kỳ tiết kiệm bộ nhớ $O(1)$ và dễ cài đặt.
  - *Nhược điểm:* Rất dễ bị kẹt tại cực trị địa phương (local optimum) hoặc cao nguyên (plateau), nơi không có lân cận nào tốt hơn trạng thái hiện tại. Khi kẹt, giao diện hiển thị biểu tượng `⛰️`.

* **Steepest-Ascent Hill Climbing:**
  - *Ưu điểm:* Bộ nhớ tối ưu $O(1)$, tiếp cận đích nhanh hơn Simple Hill Climbing cục bộ vì luôn chọn hướng có độ dốc cao nhất.
  - *Nhược điểm:* Vẫn dễ bị kẹt tại cực trị địa phương/cao nguyên. Việc đánh giá toàn bộ lân cận tại mỗi bước tốn thời gian hơn Simple Hill Climbing.

* **Stochastic Hill Climbing:**
  - *Ưu điểm:* Bộ nhớ tối ưu $O(1)$, yếu tố ngẫu nhiên giúp có cơ hội vượt qua một số cao nguyên phẳng hoặc tránh rơi vào cùng một cực trị cố định.
  - *Nhược điểm:* Vẫn có tỷ lệ kẹt cao, không đảm bảo tìm thấy lời giải tối ưu. Các lần chạy khác nhau cho kết quả khác nhau.

* **Random Restart Hill Climbing:**
  - *Ưu điểm:* Độ tin cậy cực cao, gần như chắc chắn tìm thấy đích (xấp xỉ 100%) nhờ cơ chế tự động khởi động lại từ các trạng thái solvable ngẫu nhiên mới khi bị kẹt.
  - *Nhược điểm:* Đường đi không bắt nguồn từ trạng thái ban đầu mà là từ trạng thái random thành công cuối cùng đến đích. Các lần kẹt trước được ghi lại dưới dạng bước chuyển đổi `🔄 KHỞI ĐỘNG LẠI` trong lịch sử trực quan hóa.

* **Local Beam Search (k = 4):**
  Duy trì $k$ trạng thái. Ở mỗi bước, sinh ra tất cả lân cận của cả $k$ trạng thái này, sau đó chọn lại $k$ trạng thái tốt nhất.
  - *Ưu điểm:* Khám phá song song hiệu quả, chia sẻ thông tin giữa các nhánh để cắt tỉa các hướng đi xấu nhanh chóng. Ít bị kẹt hơn leo đồi thông thường và tiết kiệm bộ nhớ hơn A\*.
  - *Nhược điểm:* Không đảm bảo tối ưu, kết quả phụ thuộc vào tham số độ rộng chùm $k$.

---

## 3. Giao diện & Hướng dẫn khởi chạy

### 3.1. Giao diện ứng dụng
Ứng dụng được thiết kế trực quan sinh động bằng **PyQt5**:
- **Midnight Navy Theme:** Chủ đề giao diện tối hiện đại, tinh tế, giảm mỏi mắt và phân định rõ ràng các vùng chức năng.
- **Glow Gradients:** Các ô số trên bàn cờ có hiệu ứng chuyển màu và đổ bóng nổi 3D (Xanh Emerald cho ô đúng vị trí, Đỏ Crimson cho ô sai vị trí, và Indigo cho ô vừa di chuyển).
- **Metric Cards (Bảng Thống kê):** Cập nhật liên tục các thông số như Pop/Step, Cost ($f = g + h$), số trạng thái đã duyệt và kích thước biên tìm kiếm (Frontier Size).
- **Bàn cờ phụ (Frontier & Explored):** Hiển thị trực quan danh sách các trạng thái kề sắp duyệt và các trạng thái đã xét dưới dạng panel thu gọn ở góc phải.


### 3.2. Hướng dẫn khởi chạy nhanh

#### 1. Cài đặt thư viện cần thiết
Yêu cầu hệ thống đã cài đặt Python (phiên bản 3.6 trở lên) và thư viện PyQt5:
```bash
pip install PyQt5
```

#### 2. Khởi chạy ứng dụng
Mở terminal hoặc command prompt tại thư mục gốc `AI LAB` và chạy lệnh:
```bash
py ThuatToan/main.py
```

### 3.3. Hướng dẫn phím tắt & tương tác nhanh
- **Phím mũi tên Phải (`→`):** Tiến sang trạng thái kế tiếp trong lời giải.
- **Phím mũi tên Trái (`←`):** Quay lại trạng thái trước đó.
- **Phím cách (`Space`):** Bật/Tắt chế độ mô phỏng tự động (Auto Simulation).
- **Nút Copy Log:** Nhấp để sao chép nhanh toàn bộ lịch sử các bước giải thuật toán vào clipboard để phân tích hoặc báo cáo.

---

## 4. Kết luận
Dự án đã triển khai và trực quan hóa thành công 11 thuật toán tìm kiếm đa dạng bao gồm nhóm không có thông tin, có thông tin và tìm kiếm cục bộ để giải bài toán 8-Puzzle. Ứng dụng mang lại một công cụ giáo dục và học tập trực quan giúp:
- Nắm bắt sinh động cơ chế hoạt động thực tế từng bước của các giải thuật AI Search.
- So sánh các tham số hiệu suất định lượng (Pop/Step, chi phí đường đi, số node đã duyệt, kích thước frontier tối đa) để hiểu rõ sự cân bằng giữa thời gian thực thi và không gian bộ nhớ của từng nhóm thuật toán.
- Trực quan hóa các hiện tượng đặc thù của tìm kiếm cục bộ như kẹt cực trị địa phương (leo đồi) hay chùm trạng thái song song (beam search).

---

## 5. Link github

https://github.com/NguyenNguyen0210/tri-tue-nhan-tao
