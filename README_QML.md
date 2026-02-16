# Tranform 3NF - QML Edition

Dự án đã được refactor toàn bộ từ Flet sang **PySide6 (QML)** để đạt được tính tương tác cao hơn và giao diện mượt mà hơn.

## Kiến trúc mới
- **`main.py`**: Khởi chạy ứng dụng Qt, cung cấp context cho QML.
- **`bridge.py`**: Chứa logic xử lý trung gian (load dữ liệu, phân tích 3NF, quản lý trạng thái).
- **`qml/`**: Chứa toàn bộ giao diện người dùng định dạng QML.
  - `Main.qml`: Khung layout chính.
  - `Sidebar.qml`: Thanh điều hướng.
  - `DataPreview.qml`: Xem trước dữ liệu và thống kê.
  - `ErdTab.qml`: Thiết kế mô hình ERD.
  - `TableCard.qml`: Thành phần hiển thị bảng trong ERD.

## Cách chạy
1. Cài đặt môi trường ảo (đã thực hiện).
2. Chạy ứng dụng:
   ```bash
   .\venv\Scripts\python main.py
   ```

## Các tính năng đã chuyển đổi
- Tải file CSV và hiển thị bảng dữ liệu (15 dòng đầu).
- Thống kê tự động (Số bản ghi, cột, gợi ý Dim/Fact).
- Đề xuất mô hình ERD chuẩn 3NF tự động.
- Tạo bảng và thêm trường thủ công trong mô hình ERD.
- Giao diện hiện đại (Deep Slate theme) với hiệu ứng hover và scroll mượt mà.
