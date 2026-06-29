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
Nhóm thuật toán tìm kiếm lời giải mà không sử dụng bất kỳ thông tin bổ trợ nào về độ gần từ trạng thái hiện tại đến đích.
- **BFS (Breadth-First Search):** Tìm kiếm theo chiều rộng (Queue FIFO). Luôn tìm ra lời giải tối ưu chuỗi nước đi ngắn nhất.
- **DFS (Depth-First Search):** Tìm kiếm theo chiều sâu (Stack LIFO). Tiết kiệm bộ nhớ nhưng không đảm bảo tính tối ưu.
- **UCS (Uniform-Cost Search):** Tìm kiếm chi phí đồng nhất dựa trên chi phí đường đi thực tế $g(n)$.
- **IDS (Iterative Deepening Search):** Kết hợp bộ nhớ ưu việt của DFS và tính tối ưu của BFS bằng cách lặp duyệt tăng dần độ sâu $d$.

---

### 2.2. Các thuật toán Tìm kiếm có thông tin (Informed / Heuristic Search)
Nhóm thuật toán sử dụng thông tin bổ trợ qua hàm Heuristic $h(n)$ (Khoảng cách Manhattan hoặc Số ô sai vị trí Misplaced Tiles) để định hướng tìm kiếm thông minh hơn.
- **Greedy Best-First Search:** Mở rộng trạng thái ưu tiên dựa trên giá trị heuristic $h(n)$ nhỏ nhất đến đích.
- **A\* Search (A-Star):** Mở rộng trạng thái dựa trên tổng chi phí đánh giá $f(n) = g(n) + h(n)$, đảm bảo tính đầy đủ và tối ưu.
- **IDA\* Search (Iterative Deepening A\*):** Kết hợp cơ chế DFS sâu dần với ngưỡng chi phí $f(n)$, khắc phục triệt để điểm yếu bộ nhớ của A\*.

---

### 2.3. Các thuật toán Tìm kiếm cục bộ (Local Search)
Hoạt động trực tiếp trên trạng thái hiện tại và các trạng thái lân cận thay vì xây dựng toàn bộ cây tìm kiếm.
- **Simple Hill Climbing:** Di chuyển tới trạng thái lân cận đầu tiên có Heuristic tốt hơn.
- **Steepest-Ascent Hill Climbing:** Đánh giá toàn bộ lân cận và chọn di chuyển tới trạng thái có Heuristic tốt nhất.
- **Stochastic Hill Climbing:** Chọn ngẫu nhiên một trong số các lân cận tốt hơn để di chuyển.
- **Random Restart Hill Climbing:** Tự động khởi động lại từ một trạng thái solvable ngẫu nhiên mới khi bị kẹt tại cực trị địa phương (local optimum).
- **Local Beam Search (k = 4):** Duy trì và mở rộng song song tập hợp $k=4$ trạng thái tốt nhất ở mỗi thế hệ.
- **Simulated Annealing:** Mô phỏng quá trình luyện kim, chấp nhận nước đi xấu hơn với một xác suất phụ thuộc vào nhiệt độ $T$ giảm dần theo thời gian để thoát khỏi cực trị địa phương.

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
