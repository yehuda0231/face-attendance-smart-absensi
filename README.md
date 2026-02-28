# 🎓 Face Attendance - Smart Absensi Mahasiswa

Sistem absensi mahasiswa berbasis **Face Recognition** menggunakan Python dan OpenCV.  
Project ini dibuat sebagai implementasi Computer Vision dalam sistem presensi otomatis.

---

## 🚀 Features

✅ Real-time Face Detection  
✅ Face Recognition menggunakan LBPH Algorithm  
✅ Penyimpanan data absensi otomatis ke CSV  
✅ Training dataset wajah mahasiswa  
✅ Sistem berbasis kamera (webcam)

---

## 🧠 How It Works

1. Dataset wajah mahasiswa dikumpulkan
2. Model dilatih menggunakan algoritma **LBPH (Local Binary Pattern Histogram)**
3. Kamera mendeteksi wajah menggunakan **Haarcascade Classifier**
4. Sistem mengenali wajah
5. Data absensi dicatat ke file `Attendance.csv`

---

## 🛠️ Tech Stack

- Python 3.x
- OpenCV
- NumPy
- Pandas
- Haarcascade Classifier
- LBPH Face Recognizer

---

## 📂 Project Structure
```
face-attendance-smart-absensi/
│
├── datawajah/
│ └── isi file hasil foto
│
├── latihwajah/
│ └── training.xml
│
│── haarcascade_frontalface_default.xml
│── haarcascade_eye.xml
│
├── Attendance.csv
├── Face_Attendance.py
├── requirements.txt
├── README.md
└── .gitignore


---

## ⚙️ Installation & Usage

```bash
git clone https://github.com/yehuda0231/face-attendance-smart-absensi.git
cd face-attendance-smart-absensi
pip install -r requirements.txt
python Face_Attendance.py
