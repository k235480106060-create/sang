# BÀI TẬP MÔN AN TOÀN VÀ BẢO MẬT THÔNG TIN

**1**. Thông tin sinh viên

**Sinh viên thực hiện:** Nguyễn Văn Sang  

**Mã sinh viên:** K235480106060   

**Lớp:** K59.KTP.K01  

**Khoa:** Điện tử  


bài 1: Mã hoá AES : Mã hoá đối xứng (mã hoá, giải mã cùng dùng 1 khoá)

### 1. Sinh khoá AES
- **Mô tả:** Ứng dụng khởi tạo khoá AES 256-bit (32 bytes) ngẫu nhiên và vector khởi tạo IV (16 bytes) phục vụ cho chế độ mã hoá CBC.
- **Minh chứng:**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/28b3f3ea-3e79-49e2-806d-b775b5f3a8ec" />


---

### 2. Lưu khoá ra file
- **Mô tả:** Cho phép xuất khoá AES và IV hiện tại ra file định dạng `.key` để lưu trữ an toàn.
- **Minh chứng:**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/aba09dec-08ae-48cd-a13e-b4bc046c65b6" />


---

### 3. Import khoá từ file
- **Mô tả:** Đọc và nạp lại khoá AES / IV từ file `.key` đã lưu trước đó vào ứng dụng để tiến hành giải mã dữ liệu.
- **Minh chứng:**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b9c8fede-b007-441d-877d-4465196f1af4" />


---

### 4. Mã hoá 1 đoạn văn bản -> Kết quả mã hoá ra màn hình
- **Mô tả:** Nhập chuỗi văn bản bất kỳ, ứng dụng thực hiện mã hoá AES-256 CBC và hiển thị chuỗi Ciphertext dạng Hex ngay trên màn hình.
- **Minh chứng:**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/18cef628-0101-4d58-9a76-2b1b00686512" />


---

### 5. Mã hoá 1 file -> Lưu vào 1 file (Thử nghiệm File lớn GB)
- **Mô tả:** Áp dụng kỹ thuật xử lý luồng (Stream processing) theo từng chunk 64KB để mã hoá và giải mã các file dung lượng lớn (hàng GB) mà không gây tràn bộ nhớ RAM.
- **Tính thời gian thực thi:** Đo chính xác thời gian xử lý bằng `time.perf_counter()`.
- **Minh chứng:**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1546e56e-3937-44e0-9847-fdb0fddfdb3f" />


---

### 6. Compare theo Bytes (Kiểm tra tính toàn vẹn)
- **Mô tả:** Đọc và so sánh từng byte giữa file nguồn ban đầu và file sau khi giải mã để chứng minh dữ liệu được phục hồi nguyên vẹn 100%.
- **Minh chứng:**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/973b9296-ef44-4584-a90b-6ab1b8cfa6e8" />


---

