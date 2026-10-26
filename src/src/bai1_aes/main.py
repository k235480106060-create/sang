import os
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class AESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Mã hoá & Giải mã AES - An toàn thông tin")
        self.root.geometry("750x650")
        
        self.key = None
        self.iv = None
        
        self.setup_ui()

    def setup_ui(self):
        # 1. Quản lý Khoá
        frame_key = ttk.LabelFrame(self.root, text="1. Quản lý Khoá AES-256 (CBC Mode)", padding=10)
        frame_key.pack(fill="x", padx=10, pady=5)
        
        btn_gen_key = ttk.Button(frame_key, text="1. Sinh khoá ngẫu nhiên", command=self.generate_key)
        btn_gen_key.pack(side="left", padx=5)
        
        btn_save_key = ttk.Button(frame_key, text="2. Lưu khoá ra file", command=self.save_key)
        btn_save_key.pack(side="left", padx=5)
        
        btn_load_key = ttk.Button(frame_key, text="3. Import khoá từ file", command=self.load_key)
        btn_load_key.pack(side="left", padx=5)
        
        self.lbl_key_status = ttk.Label(frame_key, text="Trạng thái khoá: Chưa khởi tạo", foreground="red")
        self.lbl_key_status.pack(side="left", padx=10)

        # 2. Mã hoá Văn bản
        frame_text = ttk.LabelFrame(self.root, text="2. Mã hoá & Giải mã Văn bản", padding=10)
        frame_text.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_text, text="Văn bản đầu vào:").grid(row=0, column=0, sticky="w")
        self.txt_input = tk.Text(frame_text, height=3, width=60)
        self.txt_input.grid(row=1, column=0, columnspan=2, pady=5)
        
        btn_enc_text = ttk.Button(frame_text, text="Mã hoá Văn bản", command=self.encrypt_text)
        btn_enc_text.grid(row=2, column=0, sticky="w", pady=5)
        
        btn_dec_text = ttk.Button(frame_text, text="Giải mã Văn bản", command=self.decrypt_text)
        btn_dec_text.grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Label(frame_text, text="Kết quả (Hex / Plaintext):").grid(row=3, column=0, sticky="w")
        self.txt_output = tk.Text(frame_text, height=3, width=60)
        self.txt_output.grid(row=4, column=0, columnspan=2, pady=5)

        # 3. Xử lý File lớn & So sánh Bytes
        frame_file = ttk.LabelFrame(self.root, text="3. Xử lý File & Thử nghiệm File lớn (GB)", padding=10)
        frame_file.pack(fill="x", padx=10, pady=5)
        
        btn_enc_file = ttk.Button(frame_file, text="Mã hoá File", command=self.encrypt_file)
        btn_enc_file.pack(fill="x", pady=2)
        
        btn_dec_file = ttk.Button(frame_file, text="Giải mã File", command=self.decrypt_file)
        btn_dec_file.pack(fill="x", pady=2)
        
        btn_cmp_file = ttk.Button(frame_file, text="So sánh Bytes (Compare Files)", command=self.compare_files)
        btn_cmp_file.pack(fill="x", pady=2)

        self.lbl_compare_res = ttk.Label(frame_file, text="", font=("Arial", 10, "bold"))
        self.lbl_compare_res.pack(pady=5)

        # 4. Nhật ký Log
        frame_log = ttk.LabelFrame(self.root, text="Nhật ký hoạt động (Log)", padding=10)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.txt_log = tk.Text(frame_log, height=6)
        self.txt_log.pack(fill="both", expand=True)

    def log(self, msg):
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)

    def generate_key(self):
        self.key = os.urandom(32)  # AES-256
        self.iv = os.urandom(16)   # IV 16 bytes cho CBC
        self.lbl_key_status.config(text="Trạng thái khoá: Đã sinh khoá ngẫu nhiên!", foreground="green")
        self.log("[OK] Đã sinh khoá AES-256 và IV mới.")

    def save_key(self):
        if not self.key or not self.iv:
            messagebox.showerror("Lỗi", "Vui lòng sinh khoá hoặc import khoá trước!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key files", "*.key")])
        if path:
            with open(path, "wb") as f:
                f.write(self.key + self.iv)
            self.log(f"[OK] Đã lưu khoá và IV vào tệp: {path}")

    def load_key(self):
        path = filedialog.askopenfilename(filetypes=[("Key files", "*.key"), ("All files", "*.*")])
        if path:
            try:
                with open(path, "rb") as f:
                    data = f.read()
                    if len(data) == 48: # 32 bytes Key + 16 bytes IV
                        self.key = data[:32]
                        self.iv = data[32:]
                        self.lbl_key_status.config(text="Trạng thái khoá: Đã nạp khoá từ file thành công!", foreground="green")
                        self.log(f"[OK] Đã nạp khoá từ tệp: {path}")
                    else:
                        messagebox.showerror("Lỗi", "Tệp khoá không đúng kích thước (cần 48 bytes)!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file khoá: {e}")

    def encrypt_text(self):
        if not self.key or not self.iv:
            messagebox.showerror("Lỗi", "Chưa có khoá AES!")
            return
        text = self.txt_input.get("1.0", tk.END).strip().encode('utf-8')
        if not text:
            return
        
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(text) + padder.finalize()
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, ct.hex())
        self.log("[OK] Đã mã hoá văn bản thành công.")

    def decrypt_text(self):
        if not self.key or not self.iv:
            messagebox.showerror("Lỗi", "Chưa có khoá AES!")
            return
        hex_data = self.txt_output.get("1.0", tk.END).strip()
        if not hex_data:
            return
        try:
            ct = bytes.fromhex(hex_data)
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
            decryptor = cipher.decryptor()
            pt_padded = decryptor.update(ct) + decryptor.finalize()
            
            unpadder = padding.PKCS7(128).unpadder()
            pt = unpadder.update(pt_padded) + unpadder.finalize()
            
            self.txt_input.delete("1.0", tk.END)
            self.txt_input.insert(tk.END, pt.decode('utf-8'))
            self.log("[OK] Đã giải mã văn bản thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Giải mã thất bại: {e}")

    def encrypt_file(self):
        if not self.key or not self.iv:
            messagebox.showerror("Lỗi", "Chưa có khoá AES!")
            return
        in_path = filedialog.askopenfilename(title="Chọn file mã hoá")
        if not in_path:
            return
        out_path = filedialog.asksaveasfilename(title="Lưu file đã mã hoá")
        if not out_path:
            return

        start_time = time.perf_counter()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        
        file_size = os.path.getsize(in_path)
        
        with open(in_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
            while chunk := f_in.read(64 * 1024):
                if len(chunk) == 64 * 1024:
                    f_out.write(encryptor.update(chunk))
                else:
                    padded_chunk = padder.update(chunk) + padder.finalize()
                    f_out.write(encryptor.update(padded_chunk))
            f_out.write(encryptor.finalize())
            
        elapsed = time.perf_counter() - start_time
        size_gb = file_size / (1024**3)
        self.log(f"[THÀNH CÔNG] Mã hoá file ({size_gb:.2f} GB) trong {elapsed:.2f} giây.")
        messagebox.showinfo("Thành công", f"Mã hoá file hoàn tất trong {elapsed:.2f}s!")

    def decrypt_file(self):
        if not self.key or not self.iv:
            messagebox.showerror("Lỗi", "Chưa có khoá AES!")
            return
        in_path = filedialog.askopenfilename(title="Chọn file cần giải mã")
        if not in_path:
            return
        out_path = filedialog.asksaveasfilename(title="Lưu file sau giải mã")
        if not out_path:
            return

        start_time = time.perf_counter()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        
        file_size = os.path.getsize(in_path)
        
        with open(in_path, 'rb') as f_in, open(out_path, 'wb') as f_out:
            buffer = b""
            while chunk := f_in.read(64 * 1024):
                decrypted_chunk = decryptor.update(chunk)
                buffer += decrypted_chunk
                if len(buffer) > 64 * 1024:
                    f_out.write(buffer[:-64*1024])
                    buffer = buffer[-64*1024:]
            
            decrypted_chunk = decryptor.finalize()
            buffer += decrypted_chunk
            unpadded_last = unpadder.update(buffer) + unpadder.finalize()
            f_out.write(unpadded_last)

        elapsed = time.perf_counter() - start_time
        size_gb = file_size / (1024**3)
        self.log(f"[THÀNH CÔNG] Giải mã file ({size_gb:.2f} GB) trong {elapsed:.2f} giây.")
        messagebox.showinfo("Thành công", f"Giải mã file hoàn tất trong {elapsed:.2f}s!")

    def compare_files(self):
        f1 = filedialog.askopenfilename(title="Chọn File GỐC")
        if not f1:
            return
        f2 = filedialog.askopenfilename(title="Chọn File ĐÃ GIẢI MÃ")
        if not f2:
            return

        if os.path.getsize(f1) != os.path.getsize(f2):
            self.lbl_compare_res.config(text="Kết quả So sánh: SAI KHÁC! (Kích thước 2 file không bằng nhau)", foreground="red")
            return

        match = True
        with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
            while True:
                b1 = fp1.read(64 * 1024)
                b2 = fp2.read(64 * 1024)
                if b1 != b2:
                    match = False
                    break
                if not b1:
                    break

        if match:
            self.lbl_compare_res.config(text="Kết quả So sánh Bytes: TRÙNG KHỚP 100%! File giải mã hoàn tất toàn vẹn.", foreground="green")
            self.log("[OK] So sánh Bytes: Hai file trùng khớp hoàn toàn (100%).")
        else:
            self.lbl_compare_res.config(text="Kết quả So sánh Bytes: SAI KHÁC! Dữ liệu bị thay đổi.", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = AESApp(root)
    root.mainloop()
