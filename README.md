# BananaScan - Banana Ripeness Classification

Aplikasi berbasis web untuk mengklasifikasikan tingkat kematangan buah pisang menggunakan deep learning. Proyek ini menggunakan arsitektur **ResNet18** (PyTorch) sebagai model klasifikasi di sisi backend dan **FastAPI** untuk menyajikan API prediksi, serta **Streamlit** sebagai antarmuka pengguna (frontend) yang interaktif dan responsif.

---

## 👥 Anggota Kelompok

- **Muhammad Faruqi** - (2308107010005)
- **Shaldi Shauqi** - (2308107010023)

---

## 📂 Struktur Proyek

- `/backend`: API server berbasis FastAPI yang memuat model PyTorch (`banana_ripeness_resnet18.pt`) dan memproses prediksi gambar pisang.
- `/frontend`: Dashboard Streamlit untuk mengunggah gambar dan melihat hasil klasifikasi tingkat kematangan pisang (Unripe, Ripe, Overripe, Rotten).
- `/model`: Menyimpan model weights terlatih (`banana_ripeness_resnet18.pt`).
- `/bvenv`: Virtual environment Python lokal.

---

## 🔗 Link Repository

- **GitHub Repository:** [https://github.com/Shqcod/BananaRipenessClassification](https://github.com/Shqcod/BananaRipenessClassification)

---

## 🚀 Instruksi Penerapan & Cara Menjalankan

### 1. Prasyarat (Prerequisites)

Python v3.10 ke atas

### 2. Instalasi Dependensi

Buat virtual environment

```bash
python -m venv bvenv
```

Aktifkan virtual environment Anda dan pasang dependensi yang diperlukan:

```bash
# Mengaktifkan virtual environment (Windows)
bvenv\Scripts\activate

# Menginstal dependensi di folder frontend
cd frontend
pip install -r requirements.txt

# Menginstall dependensi di folder backend
cd backend
pip install -r requirements.txt
```

### 3. Menjalankan Backend (FastAPI)

Buka terminal baru, aktifkan virtual environment, masuk ke direktori `backend`, dan jalankan server **uvicorn**:

```bash
cd backend
..\bvenv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Server backend akan berjalan di [http://127.0.0.1:8000](http://127.0.0.1:8000). Anda dapat mengakses dokumentasi API interaktif (Swagger UI) di [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 4. Menjalankan Frontend (Streamlit)

Buka terminal lainnya, aktifkan virtual environment, masuk ke direktori `frontend`, dan jalankan aplikasi **streamlit**:

```bash
cd frontend
..\bvenv\Scripts\python.exe -m streamlit run app.py
```

Aplikasi Streamlit secara otomatis akan terbuka di browser Anda pada alamat **[http://localhost:8501](http://localhost:8501)**.

---

## 🧪 Cara Menguji API

Untuk menguji apakah backend berjalan dan memberikan prediksi dengan benar, Anda dapat menggunakan script pengujian di folder scratch atau mengirimkan request POST secara manual ke endpoint `/predict` dengan form data berisi file gambar (key: `file`).
