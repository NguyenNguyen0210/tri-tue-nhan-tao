# tri-tue-nhan-tao

# Báo cáo Đồ án Cá nhân Trí tuệ Nhân tạo

## Đề tài: Giải bài toán 8-Puzzle bằng các thuật toán tìm kiếm

Giảng viên hướng dẫn: Cô Phan Thị Huyền Trang

Sinh viên thực hiện: Nguyễn Nguyên - 24110289

Ngày báo cáo: Tháng 06 năm 2026

---

## 1. Mục tiêu
Mục tiêu của dự án này là xây dựng một ứng dụng mô phỏng việc giải trò chơi 8-Puzzle bằng cách áp dụng và trực quan hóa hiệu quả của **22 thuật toán tìm kiếm** thuộc **6 nhóm thuật toán chính** trong Trí tuệ Nhân tạo. Ứng dụng cung cấp giao diện đồ họa trực quan hiện đại (PyQt5) với bộ cấu hình thuật toán 2 tầng chuyên nghiệp, cho phép người dùng nhập trạng thái ban đầu và trạng thái đích, chọn thuật toán, xem quá trình giải từng bước, theo dõi biên tìm kiếm (frontier) / danh sách đã duyệt (explored), và so sánh hiệu suất giữa các thuật toán thông qua các chỉ số thống kê thời gian thực.

---

## 2. Nội dung

### Khái niệm bài toán tìm kiếm và lời giải trong 8-Puzzle
- **Trạng thái (State):** Một cấu hình cụ thể của bảng 3x3, biểu diễn vị trí của 8 ô số (từ 1 đến 8) và ô trống (ký hiệu là 0). Ví dụ: `((1, 2, 3), (4, 0, 5), (6, 7, 8))`.
- **Hành động (Action):** Các di chuyển hợp lệ của ô trống: Lên (Up), Xuống (Down), Trái (Left), Phải (Right).
- **Trạng thái ban đầu (Initial State):** Cấu hình bắt đầu của bảng 8-Puzzle do người dùng tự nhập hoặc tạo ngẫu nhiên.
- **Trạng thái đích (Goal State):** Cấu hình mong muốn của bảng 8-Puzzle (sắp xếp theo thứ tự từ 1 đến 8 và ô trống ở cuối).
- **Chi phí bước đi (Step Cost):** Chi phí để thực hiện một hành động di chuyển (mặc định là 1 cho mỗi nước đi).
- **Lời giải (Solution):** Một chuỗi các hành động di chuyển từ trạng thái ban đầu dẫn đến trạng thái đích.

---

### 2.1. Các thuật toán Tìm kiếm không có thông tin (Uninformed Search)
Nhóm thuật toán tìm kiếm lời giải mà không sử dụng bất kỳ thông tin bổ trợ nào về độ gần từ trạng thái hiện tại đến đích. Các thuật toán được triển khai bao gồm:

* **BFS (Breadth-First Search):**
  Tìm kiếm theo chiều rộng, mở rộng tất cả các node ở độ sâu $k$ trước khi chuyển sang độ sâu $k+1$.
  - *Cấu trúc dữ liệu:* Sử dụng hàng đợi **FIFO** qua `collections.deque` làm biên tìm kiếm (`frontier`).
  - *Ưu điểm:* Đảm bảo tính đầy đủ và tối ưu - luôn tìm ra lời giải ngắn nhất khi chi phí bước đi bằng nhau.
  - *Nhược điểm:* Yêu cầu lượng bộ nhớ rất lớn $O(b^d)$ để lưu trữ biên tìm kiếm và các trạng thái đã xét.

  **Video minh họa chạy BFS:**
  <video src="https://github.com/user-attachments/assets/66764516-7ab2-4b66-8deb-68655cc41cce" controls muted style="max-width: 100%;"></video>

* **DFS (Depth-First Search):**
  Tìm kiếm theo chiều sâu, khám phá theo nhánh sâu nhất có thể trước khi thực hiện quay lui.
  - *Cấu trúc dữ liệu:* Sử dụng ngăn xếp **LIFO** qua danh sách Python (`pop()`).
  - *Ưu điểm:* Tiết kiệm bộ nhớ hơn BFS rất nhiều, độ phức tạp không gian chỉ là tuyến tính $O(b \cdot m)$.
  - *Nhược điểm:* Không đảm bảo tính đầy đủ trên không gian vô hạn và không đảm bảo tối ưu.

  **Video minh họa chạy DFS:**
  <video src="https://github.com/user-attachments/assets/0709983d-785a-4fb1-959d-16fcf939126c" controls muted style="max-width: 100%;"></video>

* **UCS (Uniform-Cost Search):**
  Mở rộng các nút dựa trên tổng chi phí từ trạng thái ban đầu đến trạng thái hiện tại.
  - *Cấu trúc dữ liệu:* Hàng đợi ưu tiên **Min-Heap** thông qua `heapq`.
  - *Đặc điểm:* Ưu tiên mở rộng trạng thái có chi phí đường đi thực tế thấp nhất.
  - *Ưu điểm:* Tìm thấy lời giải tối ưu theo chi phí tích lũy.

  **Video minh họa chạy UCS:**
  <video src="https://github.com/user-attachments/assets/b2e41d93-ddfe-44ff-ba26-b1603a21d048" controls muted style="max-width: 100%;"></video>

* **IDS (Iterative Deepening Search):**
  Kết hợp ưu thế bộ nhớ của DFS và tính tối ưu của BFS bằng cách thực hiện tìm kiếm giới hạn độ sâu (DLS) lặp lại với giới hạn tăng dần từ 0, 1, 2...
  - *Ưu điểm:* Đầy đủ và tối ưu giống BFS, nhưng bộ nhớ cực thấp chỉ $O(b \cdot d)$.
  - *Nhược điểm:* Trùng lặp việc mở rộng các node ở độ sâu nông nhiều lần.

  **Video minh họa chạy IDS:**
  <video src="https://github.com/user-attachments/assets/f608c9c8-4eee-4963-b00d-a098d1045a16" controls muted style="max-width: 100%;"></video>

---

### 2.2. Các thuật toán Tìm kiếm có thông tin (Informed / Heuristic Search)
Nhóm thuật toán sử dụng thông tin bổ trợ qua hàm Heuristic $h(n)$ (Khoảng cách Manhattan hoặc Số ô sai vị trí Misplaced Tiles) để định hướng tìm kiếm thông minh hơn.

* **Greedy Best-First Search:**
  Đánh giá các nút chỉ dựa trên giá trị ước lượng heuristic $h(n)$ từ trạng thái hiện tại đến đích.
  - *Cấu trúc dữ liệu:* Hàng đợi ưu tiên **Min-Heap** (`heapq`) sắp xếp theo $h(n)$.
  - *Ưu điểm:* Thường tìm thấy lời giải rất nhanh trong thực tế.
  - *Nhược điểm:* Không đảm bảo tính tối ưu (đường đi thường dài hơn so với A*).

  **Video minh họa chạy Greedy Search:**
  <video src="https://github.com/user-attachments/assets/f0472c38-2efa-4128-9c3d-a2df0af295d5" controls muted style="max-width: 100%;"></video>

* **A\* Search:**
  A\* đánh giá node bằng hàm $f(n) = g(n) + h(n)$ với $g(n)$ chi phí thực tế và $h(n)$ ước lượng heuristic đến đích.
  - *Cấu trúc dữ liệu:* Hàng đợi ưu tiên **Min-Heap** (`heapq`).
  - *Ưu điểm:* Hoàn chỉnh và tối ưu. Cực kỳ hiệu quả, duyệt ít node hơn rất nhiều so với BFS/UCS.
  - *Nhược điểm:* Yêu cầu bộ nhớ lớn để lưu trữ frontier và tập đã duyệt.

  **Video minh họa chạy A\*:**
  <video src="https://github.com/user-attachments/assets/f3ab9497-6c77-4bef-b778-a6cf5ce657fb" controls muted style="max-width: 100%;"></video>

* **IDA\* Search:**
  IDA\* duyệt DFS với giới hạn ngưỡng chi phí $f$. Khi một chu kỳ tìm kiếm kết thúc mà chưa gặp đích, ngưỡng mới sẽ là giá trị $f$ nhỏ nhất vượt quá ngưỡng cũ.
  - *Ưu điểm:* Đảm bảo tối ưu và đầy đủ giống A\* nhưng khắc phục triệt để điểm yếu bộ nhớ (độ phức tạp bộ nhớ tuyến tính $O(d)$).
  - *Nhược điểm:* Có thể lặp lại việc duyệt một số node ở các vòng lặp trước.

  **Video minh họa chạy IDA\*:**
  <video src="https://github.com/user-attachments/assets/6aaea16b-120e-4647-88b2-b350a8e22ff6" controls muted style="max-width: 100%;"></video>

---

### 2.3. Các thuật toán Tìm kiếm cục bộ (Local Search)
Hoạt động trực tiếp trên trạng thái hiện tại và các trạng thái lân cận thay vì xây dựng toàn bộ cây tìm kiếm lớn.

* **Simple Hill Climbing:**
  - *Ưu điểm:* Cực kỳ tiết kiệm bộ nhớ $O(1)$ và dễ cài đặt.
  - *Nhược điểm:* Rất dễ bị kẹt tại cực trị địa phương (local optimum) hoặc cao nguyên (plateau).

  **Video minh họa chạy Simple Hill Climbing:**
  <video src="https://github.com/user-attachments/assets/ca697698-35a1-42ad-939b-37e992b00099" controls muted style="max-width: 100%;"></video>

* **Steepest-Ascent Hill Climbing:**
  - *Ưu điểm:* Bộ nhớ tối ưu $O(1)$, tiếp cận đích nhanh hơn Simple Hill Climbing cục bộ vì luôn chọn hướng có độ dốc cao nhất.
  - *Nhược điểm:* Vẫn dễ bị kẹt tại cực trị địa phương/cao nguyên.

  **Video minh họa chạy Steepest-Ascent Hill Climbing:**
  <video src="https://github.com/user-attachments/assets/22561d48-0e86-4650-9059-9d61e94d1387" controls muted style="max-width: 100%;"></video>

* **Stochastic Hill Climbing:**
  - *Ưu điểm:* Bộ nhớ tối ưu $O(1)$, yếu tố ngẫu nhiên giúp có cơ hội vượt qua một số cao nguyên phẳng.
  - *Nhược điểm:* Vẫn có tỷ lệ kẹt cao, không đảm bảo tìm thấy lời giải tối ưu.

  **Video minh họa chạy Stochastic Hill Climbing:**
  <video src="https://github.com/user-attachments/assets/0995f445-b538-4136-981f-69c32f0377ef" controls muted style="max-width: 100%;"></video>

* **Random Restart Hill Climbing:**
  - *Ưu điểm:* Độ tin cậy cực cao, gần như chắc chắn tìm thấy đích (xấp xỉ 100%) nhờ cơ chế tự động khởi động lại từ các trạng thái solvable ngẫu nhiên mới khi bị kẹt.
  - *Nhược điểm:* Đường đi không bắt nguồn từ trạng thái ban đầu mà là từ trạng thái random thành công cuối cùng đến đích.

  **Video minh họa chạy Random Restart Hill Climbing:**
  <video src="https://github.com/user-attachments/assets/b3c730f8-2633-476d-9f69-1c6e3aab7994" controls muted style="max-width: 100%;"></video>

* **Local Beam Search (k = 4):**
  Duy trì $k$ trạng thái. Ở mỗi bước, sinh ra tất cả lân cận của cả $k$ trạng thái này, sau đó chọn lại $k$ trạng thái tốt nhất.
  - *Ưu điểm:* Khám phá song song hiệu quả, chia sẻ thông tin giữa các nhánh để cắt tỉa các hướng đi xấu nhanh chóng.
  - *Nhược điểm:* Không đảm bảo tối ưu, kết quả phụ thuộc vào tham số độ rộng chùm $k$.

  **Video minh họa chạy Local Beam Search:**
  <video src="https://github.com/user-attachments/assets/6e0f1827-2e69-43bd-94dc-a8a3c72b2880" controls muted style="max-width: 100%;"></video>

* **Simulated Annealing:**
  Mô phỏng quá trình luyện kim, chấp nhận nước đi xấu hơn với một xác suất phụ thuộc vào nhiệt độ $T$ giảm dần theo thời gian để thoát khỏi cực trị địa phương.

---

### 2.4. Các thuật toán Tìm kiếm trong Môi trường Phức tạp (Complex Environments Search)
Giải quyết bài toán tìm kiếm khi môi trường không xác định hoàn toàn hoặc quan sát bị hạn chế.
- **Partial Observation Search:** Duyệt BFS trên không gian trạng thái giả định (Assumed Board) dựa trên các ô quan sát được và tự động lập lại kế hoạch (Replan) khi phát hiện sự sai lệch với thực tế.
- **Belief State Search:** Duyệt BFS trên tập hợp các trạng thái khả dĩ (Belief States) để tìm kiếm chuỗi hành động giải quyết đồng thời mọi thế giới có thể xảy ra.
- **AND-OR Graph Search:** Tìm kiếm kế hoạch dự phòng (Contingent Plan) dưới dạng cây AND-OR để ứng phó với tính không xác định của hành động.

---

### 2.5. Các thuật toán Thỏa mãn Ràng buộc (Constraint Satisfaction Problems - CSP)
Mô hình hóa bàn cờ dưới dạng các biến ràng buộc với miền giá trị và các điều kiện thỏa mãn.
- **Backtracking Search:** Tìm kiếm quay lui thử từng gán giá trị hợp lệ cho các biến, quay lui khi gặp mâu thuẫn.
- **Forward Checking Search:** Kết hợp Backtracking với việc kiểm tra và cắt tỉa sớm các giá trị trong miền của các biến chưa gán nếu vi phạm ràng buộc độ sâu.
- **AC-3 (Arc Consistency 3):** Duy trì tính nhất quán cung (arc consistency) trên các ràng buộc AllDiff để thu hẹp miền giá trị trước và trong quá trình tìm kiếm.
- **Min Conflict Search:** Thuật toán tìm kiếm cục bộ cho CSP, chọn biến bị xung đột nhiều nhất và di chuyển để tối thiểu hóa số lượng xung đột.

---

### 2.6. Các thuật toán Tìm kiếm trong Môi trường Đối kháng (Adversarial Search)
Tìm kiếm lời giải trong môi trường có sự tương tác giữa tác tử và đối thủ hoặc môi trường ngẫu nhiên.
- **Minimax Search:** Đánh giá cây trò chơi giữa tác tử MAX (tối đại hóa giá trị Utility $U(s) = -manhattan(s)$) và đối thủ MIN (tối thiểu hóa Utility của MAX).
- **Alpha-Beta Pruning:** Tối ưu hóa Minimax bằng cách cắt tỉa sớm các nhánh cây tìm kiếm không ảnh hưởng đến quyết định cuối cùng nhờ hai ngưỡng $\alpha$ và $\beta$.
- **Expectimax Search:** Đánh giá cây quyết định với các nút ngẫu nhiên (CHANCE nodes), tính toán giá trị kỳ vọng (Expected Utility) đại diện cho phản ứng ngẫu nhiên của môi trường.

---

## 3. Giao diện & Hướng dẫn khởi chạy

### 3.1. Giao diện ứng dụng
Ứng dụng được thiết kế trực quan sinh động bằng **PyQt5**:
- **Bộ Cấu hình Thuật toán 2 Tầng (Two-Tier Selector):** Thiết kế chuyên nghiệp gồm 2 QComboBox phân loại rõ ràng (Tầng 1: Nhóm thuật toán ➔ Tầng 2: Thuật toán chi tiết), khắc phục hoàn toàn tình trạng danh sách tràn màn hình.
- **Midnight Navy Theme:** Chủ đề giao diện tối hiện đại, giảm mỏi mắt và phân định rõ ràng các vùng chức năng.
- **Glow Gradients:** Các ô số trên bàn cờ có hiệu ứng chuyển màu nổi 3D (Emerald cho ô đúng vị trí, Crimson cho ô sai vị trí, và Indigo cho ô vừa di chuyển).
- **Metric Cards (Bảng Thống kê):** Cập nhật liên tục các thông số Pop/Step, Cost/Utility, Visited States, Frontier Size, Iteration và Depth Limit.
- **Panel Phụ (Frontier & Explored):** Hiển thị trực quan danh sách các trạng thái kề sắp duyệt và các trạng thái đã xét dưới dạng panel thu gọn ở góc phải.

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
- **Nút Reset / Submit:** Nhập lại trạng thái hoặc khởi tạo lại trình duyệt.

---

## 4. Kết luận
Dự án đã triển khai và trực quan hóa thành công **22 thuật toán tìm kiếm** đa dạng thuộc **6 nhóm lớn** để giải bài toán 8-Puzzle. Ứng dụng mang lại một công cụ giáo dục trực quan giúp:
- Nắm bắt sinh động cơ chế hoạt động thực tế từng bước của các giải thuật AI từ cơ bản đến nâng cao.
- So sánh các tham số hiệu suất định lượng (Pop/Step, chi phí đường đi, số node đã duyệt, kích thước frontier) để hiểu rõ sự cân bằng giữa thời gian thực thi và bộ nhớ.
- Trực quan hóa các hiện tượng đặc thù như cực trị địa phương (leo đồi), cắt tỉa cung (AC-3), cắt nhánh đối kháng (Alpha-Beta) và kỳ vọng môi trường (Expectimax).

---

## 5. Link GitHub

https://github.com/NguyenNguyen0210/tri-tue-nhan-tao
