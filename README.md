# FlowerShop - Website Bán Hoa Tươi

## 1. Mục tiêu dự án
Dự án nhằm xây dựng một ứng dụng web bán hoa tươi hoàn chỉnh, cho phép người dùng xem sản phẩm, quản lý giỏ hàng, đặt hàng và quản trị viên quản lý toàn bộ hệ thống.

## 2. Kiến trúc & Công nghệ
- **Ngôn ngữ**: Python 3.x
- **Framework**: Django 6.0.1
- **Cơ sở dữ liệu**: SQLite (Mặc định) - có thể chuyển sang PostgreSQL/MySQL
- **Frontend**: Bootstrap 5, Font Awesome 6, Chart.js
- **Xử lý hình ảnh**: Pillow
- **Form handling**: Django Crispy Forms (với Bootstrap 5 pack)

## 3. Các tính năng chính
- **Xác thực & Phân quyền**: Đăng ký, đăng nhập, quản lý hồ sơ người dùng.
- **Quản lý Sản phẩm**: CRUD danh mục và sản phẩm, tìm kiếm, lọc theo danh mục, sắp xếp theo giá và ngày tạo.
- **Nghiệp vụ Đặt hàng**: Giỏ hàng (session-based), quy trình thanh toán, theo dõi lịch sử đơn hàng và trạng thái đơn hàng.
- **Quản trị & Thống kê**: Dashboard dành cho admin với biểu đồ thống kê doanh thu, trạng thái đơn hàng và sản phẩm bán chạy.
- **Trợ lý chat (AI cục bộ)**: Ollama + Llama 3.2; Django nhận tin nhắn tại `/chatbot/` và gọi API Ollama trên máy (không dùng Gemini/API cloud).
- **An toàn dữ liệu**: Kiểm tra định dạng và kích thước tệp tải lên, bảo vệ CSRF, phân quyền truy cập theo vai trò.

## 4. Hướng dẫn cài đặt & Chạy
### Yêu cầu:
- Python 3.10+
- pip (trình quản lý gói của Python)

### Các bước cài đặt:
1. Giải nén hoặc clone mã nguồn.
2. Cài đặt các thư viện cần thiết (khuyến nghị dùng file cố định phiên bản):
   ```bash
   pip install -r requirements.txt
   ```
   Hoặc cài thủ công: `pip install django pillow django-crispy-forms crispy-bootstrap5 python-dotenv`
3.4. Chạy migration để khởi tạo cơ sở dữ liệu:
   ```bash
   python manage.py migrate
   ```
5. Chatbot dùng **Ollama** (Llama 3.2 chạy cục bộ):
   - Cài [Ollama](https://ollama.com/), mở terminal và chạy: `ollama pull llama3.2`
   - Đảm bảo Ollama đang chạy (mặc định lắng nghe `http://127.0.0.1:11434`).
   - Tuỳ chọn trong `.env`:
   ```env
   OLLAMA_BASE_URL=http://127.0.0.1:11434
   OLLAMA_MODEL=llama3.2
   ```
6. Nạp dữ liệu mẫu (Sample Data):
   ```bash
   python manage.py seed
   ```
5. Chạy server phát triển (Cổng 800):
   ```bash
   python manage.py runserver 800
   ```
6. Truy cập ứng dụng tại: `http://127.0.0.1:800/`

## 5. Tài khoản mẫu
- **Admin**: 
  - Tài khoản: `admin`
  - Mật khẩu: `admin123`
- **Khách hàng mẫu**:
  - Tài khoản: `user`
  - Mật khẩu: `user123`

## 6. Cấu trúc thư mục chính
- `flower_shop/`: Cấu hình dự án (settings, urls, wsgi).
- `shop/`: Ứng dụng chính (models, views, forms, urls, signals, management).
- `templates/`: Giao diện HTML của toàn bộ website.
- `static/`: Chứa các tệp CSS, JS, hình ảnh tĩnh.
- `media/`: Chứa các tệp hình ảnh tải lên (sản phẩm, avatar).
