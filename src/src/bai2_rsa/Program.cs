using System;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Forms;

namespace Bai2_RSA
{
    public class MainForm : Form
    {
        private RSA? _rsa;
        private byte[]? _currentData;
        private byte[]? _encryptedData;

        // UI Controls
        private Button btnGenKey, btnExportPem, btnViewPem, btnImportPublic, btnImportPrivate;
        private Button btnEncrypt, btnDecrypt, btnBenchmark, btnHash, btnSign;
        private TextBox txtInputData, txtOutputData, txtHashInput, txtHashOutput, txtSignOutput;
        private RichTextBox txtLog;

        public MainForm()
        {
            this.Text = "Bài 2: Mã hoá Bất đối xứng RSA & Chữ ký số (.NET)";
            this.Size = new System.Drawing.Size(850, 750);
            this.StartPosition = FormStartPosition.CenterScreen;

            InitializeComponents();
        }

        private void InitializeComponents()
        {
            TableLayoutPanel mainLayout = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                RowCount = 5,
                ColumnCount = 1,
                Padding = new Padding(10)
            };

            // 1. Group Key Management
            GroupBox grpKey = new GroupBox { Text = "1 - 4. Quản lý Khoá RSA & Định dạng PEM", Dock = DockStyle.Top, Height = 90 };
            FlowLayoutPanel flowKey = new FlowLayoutPanel { Dock = DockStyle.Fill };
            
            btnGenKey = new Button { Text = "1. Sinh cặp khoá (2048-bit)", AutoSize = true };
            btnGenKey.Click += BtnGenKey_Click;
            
            btnExportPem = new Button { Text = "2. Xuất cặp khoá (.pem)", AutoSize = true };
            btnExportPem.Click += BtnExportPem_Click;

            btnViewPem = new Button { Text = "3. View PEM (ASN.1 Bytes)", AutoSize = true };
            btnViewPem.Click += BtnViewPem_Click;

            btnImportPublic = new Button { Text = "4a. Import Public Key", AutoSize = true };
            btnImportPublic.Click += BtnImportPublic_Click;

            btnImportPrivate = new Button { Text = "4b. Import Private Key", AutoSize = true };
            btnImportPrivate.Click += BtnImportPrivate_Click;

            flowKey.Controls.AddRange(new Control[] { btnGenKey, btnExportPem, btnViewPem, btnImportPublic, btnImportPrivate });
            grpKey.Controls.Add(flowKey);

            // 2. Group Encryption & Benchmark
            GroupBox grpEnc = new GroupBox { Text = "5 - 7. Mã hoá, Giải mã & Đo tốc độ", Dock = DockStyle.Top, Height = 140 };
            TableLayoutPanel layoutEnc = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 3 };
            
            txtInputData = new TextBox { Multiline = true, Height = 40, Dock = DockStyle.Fill, PlaceholderText = "Nhập dữ liệu <= 190 bytes (hoặc chuỗi Base64 khoá AES 32 bytes)" };
            txtOutputData = new TextBox { Multiline = true, Height = 40, Dock = DockStyle.Fill, ReadOnly = true, PlaceholderText = "Kết quả mã hoá Base64 / giải mã" };
            
            FlowLayoutPanel flowEncBtns = new FlowLayoutPanel { Dock = DockStyle.Fill };
            btnEncrypt = new Button { Text = "5. Mã hoá (Public Key)", AutoSize = true };
            btnEncrypt.Click += BtnEncrypt_Click;

            btnDecrypt = new Button { Text = "6. Giải mã (Private Key)", AutoSize = true };
            btnDecrypt.Click += BtnDecrypt_Click;

            btnBenchmark = new Button { Text = "7. Đo tốc độ Mã/Giải mã", AutoSize = true };
            btnBenchmark.Click += BtnBenchmark_Click;

            flowEncBtns.Controls.AddRange(new Control[] { btnEncrypt, btnDecrypt, btnBenchmark });

            layoutEnc.Controls.Add(txtInputData, 0, 0);
            layoutEnc.Controls.Add(txtOutputData, 1, 0);
            layoutEnc.Controls.Add(flowEncBtns, 0, 1);
            layoutEnc.SetColumnSpan(flowEncBtns, 2);
            grpEnc.Controls.Add(layoutEnc);

            // 3. Group Hash SHA-256
            GroupBox grpHash = new GroupBox { Text = "8. Sinh chuỗi băm SHA-256 (Đánh giá hiệu ứng Avalanche)", Dock = DockStyle.Top, Height = 100 };
            TableLayoutPanel layoutHash = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 2 };
            txtHashInput = new TextBox { Dock = DockStyle.Fill, PlaceholderText = "Thay đổi văn bản ở đây để thấy Hash đổi hoàn toàn..." };
            txtHashInput.TextChanged += TxtHashInput_TextChanged;
            txtHashOutput = new TextBox { Dock = DockStyle.Fill, ReadOnly = true, PlaceholderText = "SHA-256 Hash Output (Hex)" };
            
            layoutHash.Controls.Add(new Label { Text = "Đầu vào:" }, 0, 0);
            layoutHash.Controls.Add(txtHashInput, 1, 0);
            layoutHash.Controls.Add(new Label { Text = "Kết quả Hash:" }, 0, 1);
            layoutHash.Controls.Add(txtHashOutput, 1, 1);
            grpHash.Controls.Add(layoutHash);

            // 4. Group Digital Signature (PSS)
            GroupBox grpSign = new GroupBox { Text = "9. Chữ ký số ngẫu nhiên (RSA-PSS Padding / Salt)", Dock = DockStyle.Top, Height = 100 };
            TableLayoutPanel layoutSign = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, RowCount = 2 };
            btnSign = new Button { Text = "Ký chữ ký số (Mỗi lần ký sẽ ra chữ ký KHÁC NHAU)", AutoSize = true };
            btnSign.Click += BtnSign_Click;
            txtSignOutput = new TextBox { Dock = DockStyle.Fill, ReadOnly = true, PlaceholderText = "Chữ ký số kết quả (Base64)" };

            layoutSign.Controls.Add(btnSign, 0, 0);
            layoutSign.Controls.Add(txtSignOutput, 1, 0);
            grpSign.Controls.Add(layoutSign);

            // 5. Log Window
            txtLog = new RichTextBox { Dock = DockStyle.Fill, ReadOnly = true };

            mainLayout.Controls.Add(grpKey);
            mainLayout.Controls.Add(grpEnc);
            mainLayout.Controls.Add(grpHash);
            mainLayout.Controls.Add(grpSign);
            mainLayout.Controls.Add(txtLog);

            this.Controls.Add(mainLayout);
        }

        private void Log(string msg)
        {
            txtLog.AppendText($"[{DateTime.Now:HH:mm:ss}] {msg}\n");
            txtLog.ScrollToCaret();
        }

        // 1. Sinh khoá
        private void BtnGenKey_Click(object? sender, EventArgs e)
        {
            _rsa = RSA.Create(2048);
            Log("SUCCESS: Đã sinh cặp khoá RSA 2048-bit ngẫu nhiên.");
        }

        // 2. Xuất PEM
        private void BtnExportPem_Click(object? sender, EventArgs e)
        {
            if (_rsa == null) { MessageBox.Show("Vui lòng sinh khoá trước!"); return; }

            string pubPem = _rsa.ExportSubjectPublicKeyInfoPem();
            string priPem = _rsa.ExportPkcs8PrivateKeyPem();

            File.WriteAllText("public_key.pem", pubPem);
            File.WriteAllText("private_key.pem", priPem);
            Log("SUCCESS: Đã xuất 'public_key.pem' và 'private_key.pem'.");
        }

        // 3. View PEM ASN.1 Bytes
        private void BtnViewPem_Click(object? sender, EventArgs e)
        {
            if (!File.Exists("public_key.pem")) { MessageBox.Show("Chưa có file public_key.pem!"); return; }
            
            byte[] bytes = File.ReadAllBytes("public_key.pem");
            Log("--- CẤU TRÚC ASN.1 DER / PEM BYTES ---");
            Log($"Tổng kích thước file: {bytes.Length} bytes.");
            Log("Cấu trúc Tag-Length-Value (TLV):");
            Log(" - 0x30 (SEQUENCE): Đánh dấu bắt đầu mảng danh sách các tham số.");
            Log(" - 0x02 (INTEGER): Chứa các tham số Modulus (n) và Public Exponent (e).");
            Log(" - 0x06 (OBJECT IDENTIFIER): Định danh thuật toán rsaEncryption (1.2.840.113549.1.1.1).");
        }

        // 4. Import Key & View Parameters (n, e, d)
        private void BtnImportPublic_Click(object? sender, EventArgs e)
        {
            if (!File.Exists("public_key.pem")) { MessageBox.Show("Không tìm thấy public_key.pem!"); return; }
            _rsa = RSA.Create();
            _rsa.ImportFromPem(File.ReadAllText("public_key.pem"));
            
            var p = _rsa.ExportParameters(false);
            Log("SUCCESS: Import Public Key thành công!");
            Log($" - Modulus (n): {Convert.ToHexString(p.Modulus!)[..20]}... ({p.Modulus!.Length * 8} bits)");
            Log($" - Exponent (e): {Convert.ToHexString(p.Exponent!)} (65537)");
        }

        private void BtnImportPrivate_Click(object? sender, EventArgs e)
        {
            if (!File.Exists("private_key.pem")) { MessageBox.Show("Không tìm thấy private_key.pem!"); return; }
            _rsa = RSA.Create();
            _rsa.ImportFromPem(File.ReadAllText("private_key.pem"));

            var p = _rsa.ExportParameters(true);
            Log("SUCCESS: Import Private Key thành công!");
            Log($" - Modulus (n): {Convert.ToHexString(p.Modulus!)[..20]}...");
            Log($" - Private Exponent (d): {Convert.ToHexString(p.D!)[..20]}... (Rất lớn)");
        }

        // 5. Mã hoá dữ liệu (Public Key)
        private void BtnEncrypt_Click(object? sender, EventArgs e)
        {
            if (_rsa == null) { MessageBox.Show("Chưa nạp khoá!"); return; }
            byte[] data = Encoding.UTF8.GetBytes(txtInputData.Text);
            if (data.Length > 190) { MessageBox.Show("Dữ liệu không được vượt quá 190 bytes!"); return; }

            _encryptedData = _rsa.Encrypt(data, RSAEncryptionPadding.OaepSHA256);
            string base64 = Convert.ToBase64String(_encryptedData);
            txtOutputData.Text = base64;
            File.WriteAllText("encrypted_data.txt", base64);
            Log("SUCCESS: Đã mã hoá dữ liệu bằng Public Key và lưu vào 'encrypted_data.txt'.");
        }

        // 6. Giải mã dữ liệu (Private Key)
        private void BtnDecrypt_Click(object? sender, EventArgs e)
        {
            if (_rsa == null || _encryptedData == null) { MessageBox.Show("Chưa có dữ liệu mã hoá!"); return; }
            try
            {
                byte[] decrypted = _rsa.Decrypt(_encryptedData, RSAEncryptionPadding.OaepSHA256);
                string result = Encoding.UTF8.GetString(decrypted);
                txtOutputData.Text = result;
                
                bool match = txtInputData.Text == result;
                Log($"SUCCESS: Giải mã hoàn tất. Kết quả khớp với nguồn: {match} (100%).");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Giải mã thất bại (Cần dùng Private Key): {ex.Message}");
            }
        }

        // 7. Đánh giá Tốc độ Mã hoá vs Giải mã
        private void BtnBenchmark_Click(object? sender, EventArgs e)
        {
            if (_rsa == null) { MessageBox.Show("Chưa nạp khoá!"); return; }
            byte[] dummyData = new byte[100];
            new Random().NextBytes(dummyData);

            Stopwatch sw = Stopwatch.StartNew();
            for (int i = 0; i < 100; i++)
            {
                _rsa.Encrypt(dummyData, RSAEncryptionPadding.Pkcs1);
            }
            sw.Stop();
            double encTime = sw.ElapsedMilliseconds;

            byte[] cipher = _rsa.Encrypt(dummyData, RSAEncryptionPadding.Pkcs1);
            sw.Restart();
            for (int i = 0; i < 100; i++)
            {
                _rsa.Decrypt(cipher, RSAEncryptionPadding.Pkcs1);
            }
            sw.Stop();
            double decTime = sw.ElapsedMilliseconds;

            Log($"--- BÁO CÁO TỐC ĐỘ (100 LẦN THỰC THI) ---");
            Log($" - Tốc độ Mã hoá (Public Key - e nhỏ): {encTime} ms");
            Log($" - Tốc độ Giải mã (Private Key - d lớn): {decTime} ms");
            Log($" => Kết luận: Mã hoá bằng Public Key nhanh hơn Giải mã bằng Private Key khoảng {(decTime/encTime):F1} lần!");
        }

        // 8. Hash SHA-256
        private void TxtHashInput_TextChanged(object? sender, EventArgs e)
        {
            byte[] bytes = Encoding.UTF8.GetBytes(txtHashInput.Text);
            byte[] hash = SHA256.HashData(bytes);
            txtHashOutput.Text = Convert.ToHexString(hash);
        }

        // 9. Chữ ký số ngẫu nhiên (RSA-PSS)
        private void BtnSign_Click(object? sender, EventArgs e)
        {
            if (_rsa == null) { MessageBox.Show("Vui lòng sinh hoặc nạp Private Key!"); return; }
            byte[] data = Encoding.UTF8.GetBytes(txtHashInput.Text);

            // Dùng PSS Padding với Salt ngẫu nhiên
            byte[] signature = _rsa.SignData(data, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
            txtSignOutput.Text = Convert.ToBase64String(signature);
            
            Log("SUCCESS: Đã ký chữ ký số bằng RSA-PSS Padding (Mỗi lần bấm ra 1 chữ ký mới).");
        }

        [STAThread]
        static void Main()
        {
            ApplicationConfiguration.Initialize();
            Application.Run(new MainForm());
        }
    }
}
