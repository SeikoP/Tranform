Data Normalization Tool (3NF)
Giới thiệu
Đây là một ứng dụng giao diện người dùng (GUI) được xây dựng bằng Flet, cho phép người dùng chuẩn hóa dữ liệu từ file CSV sang dạng 3NF (Third Normal Form). Ứng dụng hỗ trợ:

Tạo sơ đồ ERD (Entity-Relationship Diagram) dựa trên dữ liệu đầu vào.
Chuẩn hóa dữ liệu thành các bảng Dimension (Dim_) và Fact (Fact_).
Xuất dữ liệu đã chuẩn hóa thành file CSV, Excel hoặc script SQL để tạo cơ sở dữ liệu.
Ứng dụng phù hợp cho các nhà phân tích dữ liệu, kỹ sư dữ liệu hoặc bất kỳ ai cần xử lý dữ liệu thô thành dạng chuẩn hóa để phân tích hoặc lưu trữ.

Tính năng
Nhập dữ liệu: Tải file CSV để phân tích.
Thiết kế ERD: Thêm, chỉnh sửa, xóa bảng và trường, với hỗ trợ khóa chính (Primary Key) và khóa ngoại (Foreign Key).
Đề xuất tự động: Tự động gợi ý cấu trúc ERD dựa trên phân tích dữ liệu (Dimension/Fact).
Chuẩn hóa 3NF: Chuyển đổi dữ liệu thành các bảng chuẩn hóa theo dạng 3NF.
Xuất dữ liệu: Lưu kết quả dưới dạng CSV, Excel hoặc script SQL.
Yêu cầu
Phần mềm
Python 3.8 hoặc cao hơn.
Trình duyệt (nếu chạy Flet dưới dạng ứng dụng web).
Thư viện Python
flet: Giao diện người dùng.
pandas: Xử lý dữ liệu.
Các thư viện khác (xem requirements.txt).
