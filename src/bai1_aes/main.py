import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Kích thước khối đọc/ghi file (64 KB) để tối ưu RAM khi xử lý file hàng GB
CHUNK_SIZE = 64 * 1024  

class AESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Mã hoá & Giải mã AES - An toàn thông tin")
        self.root.geometry("620x580")
        
        self.key = None
        self.iv = None
        
        self.create_widgets()

    def create_widgets(self):
        # 1. Quản lý khoá AES
        key_frame = ttk.LabelFrame(self.root, text=" 1. Quản lý Khoá AES ")
        key_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(key_frame, text="1. Sinh khoá ngẫu nhiên", command=self.generate_key).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(key_frame, text="2. Lưu khoá ra file", command=self.save_key).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(key_frame, text="3. Import khoá từ file", command=self.load_key).grid(row=0, column=2, padx=5, pady=5)
        
        self.lbl_key_status = ttk.Label(key_frame, text="Trạng thái khoá: Chưa có khoá", foreground="red")
        self.lbl_key_status.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # 2. Mã hoá / Giải mã Văn bản
        text_frame = ttk.LabelFrame(self.root, text=" 2. Mã hoá / Giải mã Văn bản ")
        text_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(text_frame, text="Văn bản nhập vào:").pack(anchor="w", padx=5)
        self.txt_input = tk.Text(text_frame, height=3)
        self.txt_input.pack(fill="x", padx=5, pady=2)
        
        btn_box = ttk.Frame(text_frame)
        btn_box.pack(fill="x", pady=5)
        ttk.Button(btn_box, text="Mã hoá VB", command=self.encrypt_text).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Giải mã VB", command=self.decrypt_text).pack(side="left", padx=5)
        
        ttk.Label(text_frame, text="Kết quả:").pack(anchor="w", padx=5)
        self.txt_output = tk.Text(text_frame, height=3)
        self.txt_output.pack(fill="x", padx=5, pady=2)

        # 3. Mã hoá / Giải mã File & Kiểm thử File GB
        file_frame = ttk.LabelFrame(self.root, text=" 3. Xử lý File & Thử nghiệm File lớn (GB) ")
        file_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ttk.Button(file_frame, text="Mã hoá File", command=self.encrypt_file_action).pack(fill="x", padx=5, pady=3)
        ttk.Button(file_frame, text="Giải mã File", command=self.decrypt_file_action).pack(fill="x", padx=5, pady=3)
        ttk.Button(file_frame, text="So sánh Bytes (Compare Files)", command=self.compare_files_action).pack(fill="x", padx=5, pady=3)
        
        self.lbl_log = ttk.Label(file_frame, text="Log hệ thống & Thời gian thực thi sẽ hiển thị ở đây", foreground="blue", wraplength=580)
        self.lbl_log.pack(padx=5, pady=10)

    # --- LOGIC QUẢN LÝ KHOÁ ---
    def generate_key(self):
        self.key = os.urandom(32)  # AES-256 (32 bytes)
        self.iv = os.urandom(16)   # IV (16 bytes)
        self.lbl_key_status.config(text="Trạng thái khoá: Đã sinh khoá AES-256 thành công!", foreground="green")

    def save_key(self):
        if not self.key or not self.iv:
            messagebox.showwarning("Cảnh báo", "Vui lòng sinh khoá trước!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key files", "*.key")])
        if file_path:
            with open(file_path, "wb") as f:
                f.write(self.key + self.iv)
            messagebox.showinfo("Thành công", "Đã lưu khoá ra file thành công!")

    def load_key(self):
        file_path = filedialog.askopenfilename(filetypes=[("Key files", "*.key")])
        if file_path:
            with open(file_path, "rb") as f:
                data = f.read()
                if len(data) == 48:
                    self.key = data[:32]
                    self.iv = data[32:]
                    self.lbl_key_status.config(text="Trạng thái khoá: Đã import khoá từ file!", foreground="green")
                else:
                    messagebox.showerror("Lỗi", "File khoá không hợp lệ!")

    # --- LOGIC MÃ HOÁ/GIẢI MÃ VĂN BẢN ---
    def encrypt_text(self):
        if not self.key:
            messagebox.showwarning("Cảnh báo", "Chưa có khoá AES!")
            return
        plain_text = self.txt_input.get("1.0", tk.END).strip().encode('utf-8')
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plain_text) + padder.finalize()
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(padded_data) + encryptor.finalize()
        
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, cipher_text.hex())

    def decrypt_text(self):
        if not self.key:
            messagebox.showwarning("Cảnh báo", "Chưa có khoá AES!")
            return
        try:
            cipher_text = bytes.fromhex(self.txt_output.get("1.0", tk.END).strip())
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(cipher_text) + decryptor.finalize()
            
            unpadder = padding.PKCS7(128).unpadder()
            plain_text = unpadder.update(padded_data) + unpadder.finalize()
            
            self.txt_input.delete("1.0", tk.END)
            self.txt_input.insert(tk.END, plain_text.decode('utf-8'))
        except Exception as e:
            messagebox.showerror("Lỗi", "Giải mã thất bại! Chuỗi hoặc khoá không đúng.")

    # --- LOGIC XỬ LÝ FILE GB (STREAMING) ---
    def encrypt_file_action(self):
        if not self.key:
            messagebox.showwarning("Cảnh báo", "Chưa có khoá AES!")
            return
        in_file = filedialog.askopenfilename(title="Chọn file cần mã hoá")
        if not in_file: return
        out_file = filedialog.asksaveasfilename(title="Lưu file mã hoá")
        if not out_file: return

        start_time = time.perf_counter()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()

        with open(in_file, "rb") as f_in, open(out_file, "wb") as f_out:
            while chunk := f_in.read(CHUNK_SIZE):
                if len(chunk) < CHUNK_SIZE:
                    chunk = padder.update(chunk) + padder.finalize()
                    f_out.write(encryptor.update(chunk) + encryptor.finalize())
                    break
                else:
                    f_out.write(encryptor.update(chunk))

        elapsed_time = time.perf_counter() - start_time
        file_size_gb = os.path.getsize(in_file) / (1024**3)
        self.lbl_log.config(text=f"Mã hoá hoàn tất!\nDung lượng file: {file_size_gb:.2f} GB\nThời gian mã hoá: {elapsed_time:.2f} giây", foreground="green")

    def decrypt_file_action(self):
        if not self.key:
            messagebox.showwarning("Cảnh báo", "Chưa có khoá AES!")
            return
        in_file = filedialog.askopenfilename(title="Chọn file mã hoá")
        if not in_file: return
        out_file = filedialog.asksaveasfilename(title="Lưu file giải mã")
        if not out_file: return

        start_time = time.perf_counter()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()

        with open(in_file, "rb") as f_in, open(out_file, "wb") as f_out:
            buffer = b""
            while chunk := f_in.read(CHUNK_SIZE):
                decrypted_chunk = decryptor.update(chunk)
                buffer += decrypted_chunk
                if len(buffer) > CHUNK_SIZE:
                    f_out.write(buffer[:-CHUNK_SIZE])
                    buffer = buffer[-CHUNK_SIZE:]
            
            buffer += decryptor.finalize()
            unpadded_last_block = unpadder.update(buffer) + unpadder.finalize()
            f_out.write(unpadded_last_block)

        elapsed_time = time.perf_counter() - start_time
        file_size_gb = os.path.getsize(out_file) / (1024**3)
        self.lbl_log.config(text=f"Giải mã hoàn tất!\nDung lượng file: {file_size_gb:.2f} GB\nThời gian giải mã: {elapsed_time:.2f} giây", foreground="green")

    # --- SO SÁNH TỪNG BYTE CHÍNH XÁC ---
    def compare_files_action(self):
        f1 = filedialog.askopenfilename(title="Chọn file GỐC")
        if not f1: return
        f2 = filedialog.askopenfilename(title="Chọn file ĐÃ GIẢI MÃ")
        if not f2: return

        if os.path.getsize(f1) != os.path.getsize(f2):
            self.lbl_log.config(text="Kết quả So sánh: SAI KHÁC! (Kích thước 2 file không bằng nhau)", foreground="red")
            return

        match = True
        with open(f1, "rb") as file1, open(f2, "rb") as file2:
            while True:
                b1 = file1.read(CHUNK_SIZE)
                b2 = file2.read(CHUNK_SIZE)
                if b1 != b2:
                    match = False
                    break
                if not b1:
                    break

        if match:
            self.lbl_log.config(text="Kết quả So sánh Bytes: TRÙNG KHỚP 100%! File giải mã hoàn tất toàn vẹn.", foreground="green")
        else:
            self.lbl_log.config(text="Kết quả So sánh: SAI KHÁC! Dữ liệu byte không trùng khớp.", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = AESApp(root)
    root.mainloop()
