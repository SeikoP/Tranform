# 📥📤 Hướng dẫn Import/Export Đa nguồn

## Tổng quan

Transform 3NF Premium Edition hỗ trợ import và export dữ liệu từ nhiều nguồn khác nhau, giúp bạn linh hoạt trong việc xử lý dữ liệu.

---

## 📥 Import Dữ liệu

### Các nguồn dữ liệu được hỗ trợ:

#### 1. **CSV Files** 📄
- Format phổ biến nhất
- Hỗ trợ nhiều encoding (UTF-8, Latin-1, etc.)
- Tự động phát hiện delimiter

**Cách sử dụng:**
1. Click "📥 Import Dữ liệu"
2. Chọn "📄 CSV File"
3. Browse và chọn file CSV

#### 2. **Excel Files** 📊
- Hỗ trợ .xlsx và .xls
- Có thể chọn sheet cụ thể
- Tự động đọc header

**Cách sử dụng:**
1. Click "📥 Import Dữ liệu"
2. Chọn "📊 Excel File"
3. Browse và chọn file Excel

#### 3. **JSON Files** 📋
- Hỗ trợ JSON array và object
- Tự động parse nested structures
- UTF-8 encoding

**Cách sử dụng:**
1. Click "📥 Import Dữ liệu"
2. Chọn "📋 JSON File"
3. Browse và chọn file JSON

#### 4. **SQLite Database** 🗄️
- Đọc trực tiếp từ .db hoặc .sqlite file
- Hỗ trợ custom SQL queries
- Không cần server

**Cách sử dụng:**
1. Click "📥 Import Dữ liệu"
2. Chọn "🗄️ SQLite Database"
3. Nhập tên bảng cần import
4. Browse và chọn database file

#### 5. **MySQL** 🐬
- Kết nối trực tiếp đến MySQL server
- Hỗ trợ authentication
- Real-time data access

**Yêu cầu:** Cài đặt `pymysql`
```bash
pip install pymysql
```

**Cách sử dụng:**
1. Click "📥 Import Dữ liệu"
2. Chọn "🐬 MySQL"
3. Nhập thông tin kết nối:
   - Host (VD: localhost hoặc IP address)
   - Username
   - Password
   - Database name
   - Table name
4. Click "Kết nối MySQL"

#### 6. **PostgreSQL** 🐘
- Kết nối trực tiếp đến PostgreSQL server
- Hỗ trợ advanced queries
- Enterprise-grade database

**Yêu cầu:** Cài đặt `psycopg2`
```bash
pip install psycopg2-binary
```

**Cách sử dụng:**
1. Click "📥 Import Dữ liệu"
2. Chọn "🐘 PostgreSQL"
3. Nhập thông tin kết nối tương tự MySQL
4. Click "Kết nối PostgreSQL"

---

## 📤 Export Dữ liệu

### Các định dạng export được hỗ trợ:

#### 1. **CSV Files** 📄
- Mỗi bảng → 1 file CSV riêng
- Dễ import vào Excel, Google Sheets
- Universal format

**Output:** `filename_TableName.csv`

#### 2. **Excel File** 📊
- Tất cả bảng trong 1 file Excel
- Mỗi bảng = 1 sheet
- Dễ xem và chỉnh sửa

**Output:** `filename.xlsx` với nhiều sheets

#### 3. **JSON Files** 📋
- Mỗi bảng → 1 file JSON
- Phù hợp cho APIs và web apps
- Human-readable format

**Output:** `filename_TableName.json`

#### 4. **SQL Script** 📜
- Tạo file .sql với:
  - CREATE TABLE statements
  - INSERT statements cho tất cả data
- Chạy được trên mọi SQL database
- Portable và version-controllable

**Output:** `filename.sql`

**Ví dụ nội dung:**
```sql
-- Table: Dim_Customer
DROP TABLE IF EXISTS Dim_Customer;
CREATE TABLE Dim_Customer (
    customer_id INTEGER,
    customer_name TEXT,
    email TEXT
);

INSERT INTO Dim_Customer VALUES (1, 'John Doe', 'john@example.com');
INSERT INTO Dim_Customer VALUES (2, 'Jane Smith', 'jane@example.com');
```

#### 5. **SQLite Database** 🗄️
- Tạo file .db với tất cả bảng
- Có thể query trực tiếp
- Không cần server setup
- Portable database file

**Output:** `filename.db`

---

## 🔧 Cài đặt Database Connectors (Tùy chọn)

### Cho MySQL:
```bash
pip install pymysql
```

### Cho PostgreSQL:
```bash
pip install psycopg2-binary
```

### Cho SQL Server:
```bash
pip install pyodbc
```

---

## 💡 Tips & Best Practices

### Import:
1. **Kiểm tra encoding**: Nếu CSV có ký tự đặc biệt, đảm bảo file dùng UTF-8
2. **Database connections**: Lưu connection strings để tái sử dụng
3. **Large files**: Với file >100MB, cân nhắc filter data trước khi import
4. **Security**: Không lưu passwords trong code, dùng environment variables

### Export:
1. **CSV**: Tốt nhất cho data analysis và import vào tools khác
2. **Excel**: Tốt nhất cho business users và presentations
3. **JSON**: Tốt nhất cho web applications và APIs
4. **SQL Script**: Tốt nhất cho version control và deployment
5. **SQLite**: Tốt nhất cho portable applications và testing

---

## 🚀 Workflow Ví dụ

### Scenario 1: Import từ MySQL, Export sang Excel
```
1. Click "📥 Import Dữ liệu"
2. Chọn MySQL, nhập credentials
3. Kết nối và load data
4. Phân tích và normalize (tab ERD)
5. Click "📤 Export Kết Quả"
6. Chọn "Excel File"
7. Nhập tên file và chọn folder
8. Done! File Excel với nhiều sheets được tạo
```

### Scenario 2: Import CSV, Export SQL Script
```
1. Click "📥 Import Dữ liệu"
2. Chọn CSV File
3. Load và phân tích data
4. Tạo ERD model (manual hoặc AI suggest)
5. Click "📤 Export Kết Quả"
6. Chọn "SQL Script"
7. File .sql được tạo, ready để deploy
```

---

## ⚠️ Troubleshooting

### "Module not found" error khi connect database:
- Cài đặt connector tương ứng (xem phần Cài đặt)

### "Connection refused" khi connect MySQL/PostgreSQL:
- Kiểm tra database server đang chạy
- Kiểm tra firewall settings
- Verify host và port

### "Permission denied" khi export:
- Chọn folder có quyền write
- Chạy app với quyền phù hợp

### CSV encoding issues:
- Mở file bằng text editor, check encoding
- Convert sang UTF-8 nếu cần

---

## 📞 Support

Nếu gặp vấn đề, check:
1. Console output cho error messages
2. Status bar ở bottom của app
3. File logs (nếu có)

---

**Transform 3NF Premium Edition v3.0**
*Making data normalization accessible and powerful* ✨
