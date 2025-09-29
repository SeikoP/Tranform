
# Công cụ Chuẩn hóa Dữ liệu 3NF

## Giới thiệu

Đây là ứng dụng giao diện người dùng (GUI) sử dụng [Flet](https://flet.dev/) cho phép chuẩn hóa dữ liệu từ file CSV sang dạng 3NF (Third Normal Form). Ứng dụng hỗ trợ:
- Xem trước dữ liệu, phân tích đặc trưng cột (Dim/Fact).
- Thiết kế, chỉnh sửa, lưu và tải sơ đồ ERD (Entity-Relationship Diagram).
- Đề xuất tự động cấu trúc ERD dựa trên phân tích dữ liệu.
- Chuẩn hóa dữ liệu thành các bảng Dimension (`Dim_`) và Fact (`Fact_`).
- Xuất dữ liệu chuẩn hóa ra CSV, Excel hoặc script SQL.

## Cấu trúc thư mục

```
Tranform/
│   main.py                  # Chạy ứng dụng Flet
│   requirements.txt         # Thư viện phụ thuộc
│   README.md
│
├── assets/
│   └── normalization.ico    # Icon ứng dụng
│
├── ui/
│   ├── sidebar.py           # Thanh công cụ bên trái (mở file, xuất dữ liệu)
│   ├── data_preview.py      # Tab xem trước dữ liệu, gợi ý Dim/Fact
│   ├── erd_tab.py           # Tab thiết kế ERD, thao tác bảng/field
│   ├── erd_utils.py         # Tiện ích thao tác ERD (thêm/xóa trường, đề xuất, lưu/tải)
│   └── data/
│       └── erd.json         # File lưu cấu trúc ERD
│
└── utils/
	 ├── data_analysis.py     # Phân tích phụ thuộc, chuẩn hóa 3NF
	 ├── file_utils.py        # Đọc file, xuất dữ liệu, lưu/tải ERD
	 └── sql_generator.py     # Sinh script SQL từ ERD
```

## Yêu cầu cài đặt

- Python >= 3.8
- Thư viện: flet, pandas, numpy, scikit-learn, pyinstaller

Cài đặt nhanh:
```bash
pip install -r requirements.txt
```

## Hướng dẫn sử dụng

1. **Chạy ứng dụng:**
	```bash
	python main.py
	```
2. **Tải file CSV:** Nhấn "📂 Mở CSV" và chọn file dữ liệu.
3. **Xem trước dữ liệu:** Tab "Xem trước Dữ liệu" hiển thị thông tin tổng quan, gợi ý Dim/Fact.
4. **Thiết kế ERD:**
	- Thêm bảng (bắt đầu bằng Dim_ hoặc Fact_).
	- Thêm trường, chọn PK/FK, hoặc nhấn "🤖 Đề xuất ERD" để tự động sinh cấu trúc.
	- Lưu cấu trúc với "💾 Lưu cấu trúc", tải lại với "📂 Tải cấu trúc".
5. **Chuẩn hóa & Xuất dữ liệu:**
	- Nhấn "💾 Xuất Dữ liệu", chọn định dạng (CSV, Excel, Database Script).
	- Nếu chọn Database, có thể tạo script SQL với "Create DB Scripts".

## Một số lưu ý

- File ERD sẽ được lưu tại `ui/data/erd.json`.
- Script SQL sinh ra nằm trong thư mục `generated_scripts/`.
- Ứng dụng hỗ trợ xuất dữ liệu lớn (tối đa ~100MB/file CSV).

---

Nếu cần thêm ví dụ hoặc hướng dẫn chi tiết về từng chức năng, hãy yêu cầu!
