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
![1. Sinh & Xuất PEM](tài liệu/bai2/01-generate-export-pem.png)

## 2. Phân tích Cấu trúc Byte ASN.1 DER / PEM (View PEM)
- **Cấu trúc TLV (Tag-Length-Value):**
  - `0x30` (SEQUENCE): Bao bọc mảng chứa các thành phần khoá.
  - `0x02` (INTEGER): Lưu trữ các đại lượng toán học RSA.
- **Minh chứng:**
![2. View PEM Bytes](tài liệu/bai2/02-view-pem-bytes.png)

## 3. Import File PEM (Trích xuất thông số $n, e, d$)
- **Public Key:** Trích xuất $n$ (Modulus) và $e$ (Public Exponent, thường là 65537).
- **Private Key:** Trích xuất $n, e, d, p, q, dP, dQ, qInv$.
- **Minh chứng:**
![3. Import Keys](tài liệu/bai2/03-parse-keys.png)

## 4. Mã hoá & Giải mã Dữ liệu (Base64)
- **Mã hoá:** Mã hoá mảng byte dữ liệu $\le 190$ bytes (hoặc khoá AES 256-bit 32 bytes) bằng Public Key, xuất chuỗi mã hoá dạng Base64 ra file.
- **Giải mã:** Dùng Private Key giải mã dữ liệu Base64 và so sánh byte khớp 100% với ban đầu.
- **Minh chứng:**
![4. Encrypt Decrypt Data](tài liệu/bai2/04-encrypt-decrypt-data.png)

## 5. Đánh giá Tốc độ Mã hoá / Giải mã
- **Kết quả đo lường:**
  - **Mã hoá bằng Public Key ($e$ nhỏ):** Rất nhanh (phép tính số mũ nhỏ).
  - **Giải mã bằng Private Key ($d$ lớn):** Chậm hơn nhiều do phép tính số mũ kích thước 2048-bit lớn.
- **Minh chứng:**
![5. Benchmark Speed](tài liệu/bai2/05-benchmark-speed.png)

## 6. Sinh chuỗi băm SHA-256 & Hiệu ứng Avalanche (Tuyết lở)
- **Thử nghiệm:** Thay đổi chỉ 1 ký tự / 1 bit ở đầu vào, chuỗi băm 256-bit kết quả thay đổi hoàn toàn (không còn tương quan).
- **Minh chứng:**
![6. SHA256 Avalanche](tài liệu/bai2/06-sha256-avalanche.png)

## 7. Chữ ký số Ngẫu nhiên (Probabilistic Signature Scheme)
- **Đề xuất giải pháp:** Áp dụng chuẩn **RSA-PSS Padding** hoặc thêm **Random Salt** vào dữ liệu trước khi băm/ký.
- **Kết quả:** Cùng một dữ liệu và cùng một Private Key, mỗi lần bấm ký đều tạo ra một Chữ ký số hoàn toàn khác nhau nhưng tất cả đều xác minh (Verify) thành công.
- **Minh chứng:**
![7. Chữ ký số PSS](tài liệu/bai2/07-probabilistic-signature.png)
