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

# BÀI 2: MÃ HOÁ BẤT ĐỐI XỨNG RSA & CHỮ KÝ SỐ (.NET C#)

## 1. Sinh cặp khoá RSA & Xuất định dạng PEM
- **Mô tả:** Khởi tạo cặp khoá RSA 2048-bit và xuất ra file định dạng `.pem` (PKCS#1 / PKCS#8).
- **Minh chứng:**
<img width="1920" height="1021" alt="image" src="https://github.com/user-attachments/assets/7273a358-ef26-40c4-adb2-beb711b6331c" />


## 2. Phân tích Cấu trúc Byte ASN.1 DER / PEM (View PEM)
- **Cấu trúc TLV (Tag-Length-Value):**
  - `0x30` (SEQUENCE): Bao bọc mảng chứa các thành phần khoá.
  - `0x02` (INTEGER): Lưu trữ các đại lượng toán học RSA.
- **Minh chứng:**
<img width="1920" height="1021" alt="image" src="https://github.com/user-attachments/assets/98e60a2d-135a-4652-a5c7-d4c53c6f2c6c" />


## 3. Import File PEM (Trích xuất thông số $n, e, d$)
- **Public Key:** Trích xuất $n$ (Modulus) và $e$ (Public Exponent, thường là 65537).
- **Private Key:** Trích xuất $n, e, d, p, q, dP, dQ, qInv$.
- **Minh chứng:**
<img width="1920" height="1016" alt="image" src="https://github.com/user-attachments/assets/81b30afb-b968-4d24-bf61-4289c3a9432c" />


## 4. Mã hoá & Giải mã Dữ liệu (Base64)
- **Mã hoá:** Mã hoá mảng byte dữ liệu $\le 190$ bytes (hoặc khoá AES 256-bit 32 bytes) bằng Public Key, xuất chuỗi mã hoá dạng Base64 ra file.
- **Giải mã:** Dùng Private Key giải mã dữ liệu Base64 và so sánh byte khớp 100% với ban đầu.
- **Minh chứng:**
<img width="1920" height="1026" alt="image" src="https://github.com/user-attachments/assets/cf31b530-a672-40fc-ba86-21731ff4d66b" />


## 5. Đánh giá Tốc độ Mã hoá / Giải mã
- **Kết quả đo lường:**
  - **Mã hoá bằng Public Key ($e$ nhỏ):** Rất nhanh (phép tính số mũ nhỏ).
  - **Giải mã bằng Private Key ($d$ lớn):** Chậm hơn nhiều do phép tính số mũ kích thước 2048-bit lớn.
- **Minh chứng:**
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/cfdaa925-7275-43b0-9605-282dee62ead5" />


## 6. Sinh chuỗi băm SHA-256 & Hiệu ứng Avalanche (Tuyết lở)
- **Thử nghiệm:** Thay đổi chỉ 1 ký tự / 1 bit ở đầu vào, chuỗi băm 256-bit kết quả thay đổi hoàn toàn (không còn tương quan).
- **Minh chứng:**
<img width="1920" height="1026" alt="image" src="https://github.com/user-attachments/assets/803d8128-373b-4bde-9f02-f241fc21721f" />


## 7. Chữ ký số Ngẫu nhiên (Probabilistic Signature Scheme)
- **Đề xuất giải pháp:** Áp dụng chuẩn **RSA-PSS Padding** hoặc thêm **Random Salt** vào dữ liệu trước khi băm/ký.
- **Kết quả:** Cùng một dữ liệu và cùng một Private Key, mỗi lần bấm ký đều tạo ra một Chữ ký số hoàn toàn khác nhau nhưng tất cả đều xác minh (Verify) thành công.
- **Minh chứng:**
<img width="1920" height="1021" alt="image" src="https://github.com/user-attachments/assets/ad670011-e0f6-4933-8f2e-e22731eeb6f8" />
<img width="1920" height="1017" alt="image" src="https://github.com/user-attachments/assets/101a488b-908a-478f-bb9d-e0521725313b" />

