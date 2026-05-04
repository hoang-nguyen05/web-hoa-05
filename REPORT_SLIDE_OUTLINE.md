# Đề cương Báo cáo hết môn (30 trang) - Website FlowerShop

## 1. Mở đầu (2-3 trang)
- Lý do chọn đề tài: Sự phát triển của thương mại điện tử trong ngành hoa tươi.
- Mục tiêu dự án: Xây dựng website bán hoa hoàn chỉnh, chuyên nghiệp.
- Phạm vi dự án: Quản lý sản phẩm, đơn hàng, khách hàng, thống kê.

## 2. Phân tích bài toán & Yêu cầu (4-5 trang)
- Quy trình nghiệp vụ: Từ chọn hoa, vào giỏ hàng đến thanh toán và giao nhận.
- Các vai trò người dùng: Guest, Member, Admin.
- Yêu cầu chức năng: CRUD, Tìm kiếm/Lọc, Xác thực, Đặt hàng, Thống kê.
- Yêu cầu phi chức năng: Hiệu năng, bảo mật, giao diện thân thiện (UX/UI).

## 3. Thiết kế hệ thống (6-8 trang)
- Kiến trúc hệ thống: Mô hình MVT (Model-View-Template) của Django.
- Thiết kế CSDL:
  - Sơ đồ quan hệ thực thể (ERD).
  - Chi tiết các bảng: `User`, `Profile`, `Category`, `Product`, `Order`, `OrderItem`.
- Sơ đồ phân rã chức năng (BFD).
- Sơ đồ luồng dữ liệu (DFD).

## 4. Công nghệ & Công cụ (3-4 trang)
- Tại sao chọn Python & Django?
- Frontend: Bootstrap 5, Chart.js.
- Công cụ phát triển: IDE (Visual Studio Code/PyCharm), Git.

## 5. Triển khai & Kết quả (8-10 trang)
- Hình ảnh giao diện chính: Trang chủ, Danh sách sản phẩm, Giỏ hàng, Thanh toán.
- Giao diện Admin: Dashboard thống kê, Quản lý đơn hàng.
- Mô tả các luồng nghiệp vụ chính bằng code snippet quan trọng.

## 6. Kiểm thử (Testing) (2-3 trang)
- Kịch bản kiểm thử (Test cases): Đăng ký, Đăng nhập, Đặt hàng, Phân quyền.
- Kết quả kiểm thử thực tế.

## 7. Kết luận & Hướng phát triển (1-2 trang)
- Những gì đã đạt được.
- Hạn chế của hệ thống hiện tại.
- Hướng phát triển: Thanh toán trực tuyến (Momo/VNPay), Gợi ý hoa thông minh (AI), App di động.

---

# Đề cương Slide trình bày (10-15 trang) - Demo Website FlowerShop

1. **Trang tiêu đề**: Tên dự án, Thành viên thực hiện, GV hướng dẫn.
2. **Đặt vấn đề**: Tại sao cần website bán hoa?
3. **Mục tiêu & Phạm vi**: Các tính năng cốt lõi.
4. **Công nghệ sử dụng**: Python, Django, Bootstrap, SQLite.
5. **Sơ đồ ERD (CSDL)**: 6 bảng dữ liệu chính.
6. **Demo Chức năng 1**: Đăng ký, Đăng nhập & Profile.
7. **Demo Chức năng 2**: Tìm kiếm, Lọc & CRUD Sản phẩm.
8. **Demo Chức năng 3 (Nghiệp vụ)**: Quy trình Đặt hàng & Thanh toán.
9. **Demo Chức năng 4 (Quản trị)**: Dashboard Thống kê & Báo cáo.
10. **Bảo mật & Xử lý an toàn**: Tải lên ảnh, CSRF, Phân quyền.
11. **Kết quả đạt được**: Tổng quan hệ thống chạy ổn định.
12. **Hướng phát triển tương lai**: Các tính năng mở rộng.
13. **Kết luận & Cảm ơn**: Hỏi đáp (Q&A).
