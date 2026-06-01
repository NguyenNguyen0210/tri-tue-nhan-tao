# 🧩 8-Puzzle Solver & Visualizer

Đây là bài tập thực hành môn **Trí tuệ nhân tạo**.
* **Sinh viên thực hiện**: Nguyễn Nguyên
* **Mã số sinh viên**: 24110289
* **Giảng viên hướng dẫn**: Cô Phan Thị Huyền Trang

---

Ứng dụng trực quan hóa các thuật toán tìm kiếm trí tuệ nhân tạo (AI Search Algorithms) giải bài toán 8-Puzzle, được xây dựng trên ngôn ngữ **Python** và thư viện đồ họa **PyQt5**.

---

## 🚀 Hướng dẫn khởi chạy nhanh

### 1. Cài đặt thư viện cần thiết
Đảm bảo bạn đã cài đặt Python và thư viện PyQt5:
```bash
pip install PyQt5
```

### 2. Khởi chạy ứng dụng
Mở terminal tại thư mục gốc `AI LAB` và chạy lệnh:
```bash
py ThuatToan/main.py
```

---

## 📘 Chi tiết về các thuật toán giải 8-Puzzle

Ứng dụng hỗ trợ trực quan hóa 5 thuật toán tìm kiếm cốt lõi trong Trí tuệ nhân tạo. Dưới đây là phân tích chi tiết cơ chế hoạt động, cấu trúc dữ liệu và đặc điểm của từng thuật toán được triển khai trong chương trình:

### 1. BFS (Breadth-First Search - Tìm kiếm theo chiều rộng)
* **Cơ chế hoạt động**: BFS duyệt qua tất cả các trạng thái lân cận ở độ sâu hiện tại trước khi chuyển sang các trạng thái ở độ sâu tiếp theo. Thuật toán lan tỏa như làn sóng từ trạng thái bắt đầu.
* **Cấu trúc dữ liệu**: Sử dụng hàng đợi **FIFO (First-In-First-Out)** thông qua lớp `collections.deque` làm `frontier` (biên tìm kiếm).
* **Đặc điểm**:
  - **Tính hoàn chỉnh**: BFS chắc chắn tìm thấy lời giải nếu lời giải tồn tại.
  - **Tính tối ưu**: Đảm bảo tìm ra đường đi ngắn nhất (ít bước di chuyển nhất) vì nó duyệt theo từng cấp độ sâu tăng dần.
  - **Độ phức tạp**: Cả thời gian và bộ nhớ đều là $O(b^d)$ (với $b$ là hệ số nhánh - tối đa là 4 hướng di chuyển, và $d$ là độ sâu lời giải). Do lưu trữ toàn bộ biên duyệt, BFS dễ gây ngốn RAM đối với các bài toán có độ sâu lớn.

---

### 2. DFS (Depth-First Search - Tìm kiếm theo chiều sâu)
* **Cơ chế hoạt động**: DFS đi sâu nhất có thể dọc theo mỗi nhánh trạng thái trước khi quay lui (backtracking) để kiểm tra các nhánh khác.
* **Cấu trúc dữ liệu**: Sử dụng ngăn xếp **LIFO (Last-In-First-Out)** thông qua danh sách Python thông thường (gọi hàm `pop()` để lấy phần tử ở cuối).
* **Đặc điểm**:
  - **Tính hoàn chỉnh**: Không hoàn chỉnh trên không gian trạng thái vô hạn hoặc nếu gặp chu kỳ (tuy nhiên ứng dụng đã giới hạn 3000 bước duyệt tối đa).
  - **Tính tối ưu**: Không đảm bảo tối ưu. DFS thường tìm thấy những đường đi vòng vèo, dài hơn nhiều so với BFS.
  - **Độ phức tạp**: Tiết kiệm bộ nhớ hơn BFS với độ phức tạp không gian chỉ là $O(b \cdot m)$ (với $m$ là độ sâu tối đa của cây tìm kiếm).

---

### 3. UCS (Uniform Cost Search - Tìm kiếm chi phí đồng nhất)
* **Cơ chế hoạt động**: UCS mở rộng các nút có chi phí đường đi thấp nhất trước. Trong 8-puzzle thông thường, chi phí mỗi bước là 1 nên UCS nguyên bản sẽ tương đương BFS. 
* **Cấu trúc dữ liệu**: Hàng đợi ưu tiên **Min-Heap** thông qua thư viện `heapq` của Python.
* **Đặc điểm trong mã nguồn dự án**:
  - Trong chương trình này, UCS được cấu hình đặc biệt sử dụng hàm Heuristic **Misplaced Tiles** (số ô nằm sai vị trí so với trạng thái đích) làm độ ưu tiên để sắp xếp trong Min-Heap.
  - Do đó, thuật toán hoạt động tương đương với **Greedy Best-First Search (Tìm kiếm tham lam tốt nhất)**, ưu tiên mở rộng trạng thái nào có ít ô sai lệch nhất trước để nhanh chóng tiến tới đích.

---

### 4. IDS (Iterative Deepening Search - Tìm kiếm sâu dần)
* **Cơ chế hoạt động**: IDS kết hợp ưu thế tiết kiệm bộ nhớ của DFS và tính tối ưu của BFS. Thuật toán thực hiện lặp đi lặp lại việc tìm kiếm theo chiều sâu giới hạn (Depth-Limited Search) với giới hạn độ sâu (`limit`) tăng dần từ 0, 1, 2... cho đến khi tìm thấy đích.
* **Đặc điểm**:
  - **Tính hoàn chỉnh & Tối ưu**: Hoàn chỉnh và tối ưu tương tự BFS (vì độ sâu tăng dần từng bước).
  - **Bộ nhớ cực thấp**: Chỉ tốn $O(b \cdot d)$ bộ nhớ tại một thời điểm, giải quyết hoàn toàn điểm yếu tốn tài nguyên của BFS.
  - **Cơ chế chống trùng lặp**: IDS trong chương trình thực hiện kiểm tra chu trình trên nhánh hiện tại (`is_cycle = state in path[:-1]`). Nếu trạng thái đã có trên đường đi hiện tại, thuật toán sẽ bỏ qua trạng thái đó để ngăn chặn vòng lặp vô hạn.

---

### 5. Thuật toán A\* (A-Star Search)
* **Cơ chế hoạt động**: Thuật toán tìm kiếm heuristic phổ biến và hiệu quả nhất. A\* đánh giá các nút bằng cách kết hợp chi phí thực tế đã đi qua và chi phí ước lượng còn lại tới đích thông qua hàm:
  $$f(n) = g(n) + h(n)$$
  Trong đó:
  - **$g(n)$ (Chi phí thực tế)**: Được đo bằng khoảng cách **Manhattan** từ trạng thái hiện tại (tổng số ô di chuyển tối thiểu để đưa các ô số 1-8 về đúng vị trí đích).
  - **$h(n)$ (Ước lượng Heuristic)**: Tính bằng **Misplaced Tiles** (số ô số nằm sai vị trí so với đích).
* **Cấu trúc dữ liệu**: Hàng đợi ưu tiên **Min-Heap** (`heapq`).
* **Đặc điểm**:
  - **Tối ưu và Hoàn chỉnh**: Nhờ sử dụng Heuristic chấp nhận được (admissible), A\* đảm bảo tìm ra đường đi ngắn nhất với số bước duyệt ít hơn rất nhiều so với BFS hay UCS thông thường nhờ có định hướng thông minh.

---

### 6. Thuật toán IDA\* (Iterative Deepening A\* - Tìm kiếm A\* sâu dần)
* **Cơ chế hoạt động**: IDA\* kết hợp cơ chế giới hạn ngưỡng chi phí của thuật toán IDS với hàm đánh giá heuristic thông minh của A\*. 
  - Thay vì tăng giới hạn độ sâu từng cấp như IDS, IDA\* sử dụng ngưỡng cắt dựa trên giá trị hàm số $f(n) = g(n) + h(n)$ (với $g(n)$ là khoảng cách Manhattan và $h(n)$ là số ô sai vị trí `misplaced`).
  - Trong mỗi vòng lặp, thuật toán thực hiện tìm kiếm theo chiều sâu (DFS). Nếu gặp một nút có $f(n)$ vượt quá ngưỡng hiện tại (`f_limit`), nhánh đó sẽ bị cắt (`cutoff`).
  - Khi một vòng lặp tìm kiếm kết thúc mà không tìm thấy đích, ngưỡng giới hạn tiếp theo sẽ được cập nhật bằng giá trị $f(n)$ nhỏ nhất trong số các nút bị cắt nhánh mà vượt quá ngưỡng cũ.
* **Đặc điểm**:
  - **Tối ưu và Hoàn chỉnh**: Đảm bảo tìm ra lời giải tối ưu tương tự A\* (do ngưỡng $f$ tăng dần và hàm heuristic chấp nhận được).
  - **Tiết kiệm bộ nhớ**: Khắc phục hoàn toàn nhược điểm tiêu tốn bộ nhớ của A\* bằng cách chỉ lưu trữ nhánh tìm kiếm hiện tại trên ngăn xếp (độ phức tạp không gian chỉ là tuyến tính so với độ sâu đường đi).
  - **Cơ chế chống lặp**: Kiểm tra và loại bỏ chu kỳ trên nhánh tìm kiếm hiện tại tương tự DFS/IDS.

---

### 7. Thuật toán Simple Hill Climbing (Tìm kiếm leo đồi đơn giản)
* **Cơ chế hoạt động**: Là thuật toán tìm kiếm cục bộ (local search). Từ trạng thái hiện tại, thuật toán duyệt qua các trạng thái lân cận theo thứ tự và di chuyển ngay lập tức sang trạng thái lân cận đầu tiên tìm thấy có giá trị hàm heuristic tốt hơn (khoảng cách Manhattan nhỏ hơn).
* **Đặc điểm**:
  - **Không hoàn chỉnh**: Dễ bị kẹt tại các cực trị địa phương (local optimum) hoặc các cao nguyên (plateau/shoulder), nơi không có trạng thái lân cận nào tốt hơn trạng thái hiện tại, ngay cả khi chưa đạt tới đích. Khi bị kẹt, ứng dụng sẽ thông báo trạng thái dừng lại bằng biểu tượng kẹt `⛰️`.
  - **Không tối ưu**: Chỉ di chuyển theo độ dốc heuristic tốt hơn đầu tiên mà không có cái nhìn toàn cục, do đó đường đi tìm được (nếu có) có thể không phải là ngắn nhất.
  - **Cực kỳ tiết kiệm bộ nhớ**: Chỉ lưu trữ trạng thái hiện tại và đánh giá các lân cận của nó, không duy trì danh sách biên mở rộng (frontier) lớn như BFS hay A\*.

---

## 🎨 Giao diện & Các tính năng tương tác hỗ trợ

* **Midnight Navy Theme**: Giao diện tối hiện đại, hạn chế mỏi mắt, phân biệt rõ các vùng chức năng bằng độ tương phản màu sắc hợp lý.
* **Glow Gradients**: Các ô số trên bàn cờ có hiệu ứng chuyển màu và đổ bóng nổi 3D (Xanh Emerald cho ô đúng vị trí, Đỏ Crimson cho ô sai vị trí, và Indigo cho ô vừa di chuyển).
* **Bảng Thống kê (Metric Cards)**: Cập nhật chi tiết chỉ số Pop/Step, Cost ($f = g + h$), trạng thái đã duyệt và kích thước biên biên duyệt (Frontier).
* **Phím tắt điều hướng nhanh**:
  - Phím mũi tên phải `→` : Tiến sang bước tiếp theo.
  - Phím mũi tên trái `←` : Quay lại bước trước đó.
  - Phím cách `Space` : Bật/Tắt chế độ mô phỏng tự động (Auto).
* **Copy Log**: Nhấn nút `Copy Log` ở panel phải để sao chép nhanh toàn bộ lịch sử các bước duyệt thuật toán vào clipboard.
* **Bàn cờ phụ (Frontier & Explored)**: Các trạng thái biên kề duyệt tiếp theo và danh sách các trạng thái đã xét trước đó được thu gọn tiện lợi ở panel phải.
