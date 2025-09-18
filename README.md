# Finger Counter with OpenCV + MediaPipe

Hitung jumlah jari yang terangkat secara real-time menggunakan **OpenCV** dan **MediaPipe Hands**.  
Aplikasi ini:
- Mendeteksi tangan dari webcam
- Menggambar landmark & koneksi tangan
- Menghitung berapa jari yang “terangkat” berdasarkan sudut sendi
- Menampilkan status tiap jari (Jempol, Telunjuk, Tengah, Manis, Kelingking)

https://github.com/bobnolen

---

## Demo
Tekan `q` untuk keluar dari aplikasi. Jendela akan menampilkan:
- Kotak hijau dengan angka total jari terangkat
- Status tiap jari (Terangkat/Turun)
- Skeleton/landmark tangan

---

## Fitur Utama
- ✅ Deteksi hingga 2 tangan (configurable `max_num_hands`)
- ✅ Perhitungan sudut (radians → degrees) untuk klasifikasi jari
- ✅ Penentuan jempol secara khusus
- ✅ UI sederhana dengan overlay teks

---

## Persyaratan
- Python 3.8+
- Webcam/Camera
- Paket utama:
  - `opencv-python`
  - `mediapipe`
  - `numpy`

### Instalasi
```bash
# 1) Buat dan aktifkan virtual environment (opsional tapi direkomendasikan)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2) Install dependencies
pip install opencv-python mediapipe numpy
