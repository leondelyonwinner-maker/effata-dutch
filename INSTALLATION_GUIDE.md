Perfect! Saya tulis ulang dengan detail lengkap untuk GitHub Anda: `leondelyonwinner-maker`

---

# **PANDUAN LENGKAP - Opsi 1: Path Pendek**

## **LANGKAH 1: Buat Folder di Path Pendek**

### 1.1 Buka PowerShell sebagai Administrator

1. Tekan tombol **Windows** di keyboard
2. Ketik: `PowerShell`
3. Klik kanan **"Windows PowerShell"** → pilih **"Run as administrator"**

![PowerShell Admin](https://i.imgur.com/example.png)

### 1.2 Buat Folder Proyek

Di PowerShell yang sudah terbuka, ketik:

```powershell
# Buat folder di C:\dev (bisa ganti D:\ atau E:\ jika ada)
mkdir C:\dev
cd C:\dev

# Cek folder sudah ada
ls
```

**Expected output:**
```
    Directory: C:\dev

Mode                 LastWriteTime         Length Name
----                 -----------           ------ ----
d-----         1/1/2025  10:00 AM                <DIR>
```

---

## **LANGKAH 2: Copy Files dari Claude Output ke Path Pendek**

### 2.1 Buka File Explorer

1. Tekan **Windows + E** untuk buka File Explorer
2. Navigate ke folder ini:
```
C:\Users\leona\Claude\Projects\Dutch Coach\effata-dutch
```

Atau copy-paste path ini di address bar File Explorer.

### 2.2 Copy Seluruh Folder

1. Di File Explorer, lihat folder `effata-dutch` (folder dengan icon folder biru)
2. Klik kanan pada `effata-dutch` folder → **Copy**

![Copy Folder](https://i.imgur.com/example.png)

### 2.3 Paste ke Path Baru

1. Di File Explorer, navigate ke: `C:\dev`
2. Klik kanan di area kosong → **Paste**
3. Tunggu sampai copy selesai (lihat progress bar)

**Result:**
```
C:\dev\effata-dutch\  ← Folder proyek siap
├── app\
├── scripts\
├── requirements.txt
├── render.yaml
├── README.md
└── ... (files lainnya)
```

---

## **LANGKAH 3: Setup Git Repository**

### 3.1 Masuk Folder Proyek

Di PowerShell yang masih terbuka, ketik:

```powershell
# Masuk ke folder effata-dutch
cd C:\dev\effata-dutch

# Verifikasi Anda di folder yang benar
pwd
# Expected: C:\dev\effata-dutch
```

### 3.2 Inisialisasi Git

Ketik di PowerShell:

```powershell
git init
```

**Expected output:**
```
Initialized empty Git repository in C:\dev\effata-dutch\.git/
```

### 3.3 Setup Git Config (Penting!)

```powershell
# Set nama dan email Anda (GitHub account)
git config user.name "leondelyonwinner-maker"
git config user.email "leogodservant@gmail.com"

# Verifikasi
git config --list | grep user
```

**Expected output:**
```
user.name=leondelyonwinner-maker
user.email=leogodservant@gmail.com
```

---

## **LANGKAH 4: Add Files & Initial Commit**

### 4.1 Add Semua Files

```powershell
git add .

# Verifikasi files yang akan di-commit
git status
```

**Expected output:**
```
On branch master

No commits yet

Changes to be committed:
  (use "rm --cached <file>..." to unstage)
        new file:   .env.example
        new file:   .gitignore
        new file:   README.md
        ... (40+ files)
```

### 4.2 Commit Pertama

```powershell
git commit -m "Initial commit: Effata Dutch coach app"
```

**Expected output:**
```
[master (root-commit) abc1234] Initial commit: Effata Dutch coach app
 41 files changed, 5000 insertions(+)
 create mode 100644 .env.example
 ... (list of files)
```

### 4.3 Rename Branch ke `main` (GitHub standard)

```powershell
git branch -M main

# Verifikasi
git branch
```

**Expected output:**
```
* main
```

---

## **LANGKAH 5: Buat Repository di GitHub**

### 5.1 Login GitHub

1. Buka browser, pergi ke: https://github.com/leondelyonwinner-maker
2. Klik tombol **"+"** di top-right → **"New repository"**

![New Repo](https://i.imgur.com/example.png)

### 5.2 Isi Form Repository

| Field | Value |
|-------|-------|
| **Repository name** | `effata-dutch` |
| **Description** | Personal Dutch language coach - FastAPI + DeepSeek + SMS-2 spaced repetition |
| **Public/Private** | Public (atau Private jika prefer) |
| **Initialize with README** | ❌ UNCHECK (karena sudah ada file) |
| **Add .gitignore** | ❌ UNCHECK (sudah ada) |
| **.gitignore template** | None |

### 5.3 Klik "Create repository"

Setelah create, Anda akan lihat halaman dengan git commands.

---

## **LANGKAH 6: Connect Local Repository ke GitHub**

### 6.1 Copy URL Repository

Di halaman GitHub yang baru saja dibuat, klik **"Code"** → copy URL HTTPS:

```
https://github.com/leondelyonwinner-maker/effata-dutch.git
```

### 6.2 Add Remote ke PowerShell

Kembali ke PowerShell, ketik:

```powershell
git remote add origin https://github.com/leondelyonwinner-maker/effata-dutch.git

# Verifikasi
git remote -v
```

**Expected output:**
```
origin  https://github.com/leondelyonwinner-maker/effata-dutch.git (fetch)
origin  https://github.com/leondelyonwinner-maker/effata-dutch.git (push)
```

---

## **LANGKAH 7: Push ke GitHub**

### 7.1 Authenticasi GitHub (First Time Only)

```powershell
git push -u origin main
```

Ini akan membuka popup browser untuk login GitHub. Ikuti langkah-langkahnya:

1. **Sign in** dengan username: `leondelyonwinner-maker`
2. **Authorize** Git Credential Manager
3. Kembali ke PowerShell - akan otomatis push

**Expected output:**
```
Enumerating objects: 41, done.
Counting objects: 100% (41/41), done.
Delta compression using up to 8 threads
Compressing objects: 100% (35/35), done.
Writing objects: 100% (41/41), 125.34 KiB | 2.50 MiB/s, done.
Total 41 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/leondelyonwinner-maker/effata-dutch.git
 * [new branch]      main -> main
Branch 'main' is set up to track remote tracking branch 'main' from 'origin'.
```

### 7.2 Verifikasi di GitHub

1. Refresh halaman GitHub Anda: https://github.com/leondelyonwinner-maker/effata-dutch
2. Lihat semua 41 files sudah ter-upload ✅

---

## **LANGKAH 8: Setup Environment Lokal**

### 8.1 Verify Folder Path

```powershell
# Pastikan masih di folder yang benar
cd C:\dev\effata-dutch
pwd
```

### 8.2 Buat Virtual Environment

```powershell
python -m venv .venv

# Activate venv
.venv\Scripts\Activate.ps1
```

**Expected output:**
```
(.venv) PS C:\dev\effata-dutch>
# Notice (.venv) di depan prompt
```

Jika error `Execution Policy`, jalankan:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
# Lalu ulangi: .venv\Scripts\Activate.ps1
```

### 8.3 Install Dependencies

```powershell
# Pastikan (.venv) aktif
pip install -r requirements.txt

# Tunggu sampai selesai (5-10 menit, tergantung internet)
```

**Expected output:**
```
Successfully installed fastapi-0.115.6 uvicorn-0.34.0 sqlalchemy-2.0.36 ... (40+ packages)
```

---

## **LANGKAH 9: Setup Environment Variables**

### 9.1 Copy .env.example ke .env

```powershell
# Masih di C:\dev\effata-dutch
copy .env.example .env
```

### 9.2 Generate Passcode Hash

```powershell
python -m app.cli hash-passcode "pilih-passcode-anda-misalnya-password123"

# Contoh output:
# $2b$12$K5XvXJ8N1mK7pL9qR4sT2eW5vJ0xK1mL2nO3pQ4sR5t6u7v8w9x0y
```

**COPY** hash yang keluar → simpan di clipboard

### 9.3 Edit File .env

```powershell
# Buka file .env dengan text editor
notepad .env
```

Di Notepad, ubah nilai ini:

```env
ENVIRONMENT=development

DATABASE_URL=sqlite+aiosqlite:///./effata_dutch.db

# PASTE hash yang di-copy dari step 9.2
APP_PASSCODE_HASH=$2b$12$K5XvXJ8N1mK7pL9qR4sT2eW5vJ0xK1mL2nO3pQ4sR5t6u7v8w9x0y

# Generate session secret baru
SESSION_SECRET_KEY=

# DeepSeek API key (daftar di https://api.deepseek.com)
DEEPSEEK_API_KEY=

DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

### 9.4 Generate SESSION_SECRET_KEY

Di PowerShell baru (buka tab baru), jalankan:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"

# Contoh output:
# aB_cD-eF_gH-iJ_kL-mN_oP-qR_sT-uV_wX-yZ0123456789
```

**COPY** output ini → Paste ke .env sebagai `SESSION_SECRET_KEY`

### 9.5 Dapatkan DeepSeek API Key

1. Buka: https://api.deepseek.com
2. Sign up atau login
3. Pergi ke **"API Keys"** atau **"Account Settings"**
4. Create new API key atau copy existing key
5. Paste ke `.env` sebagai `DEEPSEEK_API_KEY`

**File .env final Anda akan terlihat seperti:**
```env
ENVIRONMENT=development
DATABASE_URL=sqlite+aiosqlite:///./effata_dutch.db
APP_PASSCODE_HASH=$2b$12$K5XvXJ8N1mK7pL9qR4sT2eW5vJ0xK1mL2nO3pQ4sR5t6u7v8w9x0y
SESSION_SECRET_KEY=aB_cD-eF_gH-iJ_kL-mN_oP-qR_sT-uV_wX-yZ0123456789
DEEPSEEK_API_KEY=sk-1234567890abcdefghijklmnop
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

### 9.6 Save .env

Tekan **Ctrl+S** di Notepad → Close

---

## **LANGKAH 10: Load Seed Data**

Di PowerShell, pastikan (.venv) aktif, ketik:

```powershell
python -m app.seed
```

**Expected output:**
```
Seed complete: 10-week roadmap + Week 1 vocab/grammar/SRS cards loaded.
```

---

## **LANGKAH 11: Jalankan Aplikasi Lokal**

```powershell
uvicorn app.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

---

## **LANGKAH 12: Test di Browser**

1. Buka browser → **http://localhost:8000**
2. Login dengan **passcode** yang Anda set di Langkah 9.2
3. Test semua fitur:
   - ✅ Roadmap (lihat 10 weeks)
   - ✅ Vocabulary (Week 1 ada 6 kata)
   - ✅ Grammar (ada latihan de/het)
   - ✅ Conversation (chat dengan Coach Effata)
   - ✅ Pronunciation (test kata "huisje")
   - ✅ Review/Memory (lihat SRS cards)

Jika semua hijau ✅ - **Lokal setup BERHASIL!**

---

## **NEXT STEP: Deploy ke Render**

Setelah lokal berhasil, lanjut ke **TAHAP 2** (sudah saya jelaskan sebelumnya):
- Buat Render account
- Connect GitHub repo
- Deploy dengan render.yaml

---

**Sudah jelas semuanya? Mulai dari Langkah 1 dan kabari saya jika ada error!** 🚀