# 📘 SoalBot – Ubah Materi Jadi Soal Otomatis

**SoalBot** adalah aplikasi AI berbasis Streamlit yang membantu mahasiswa dan pengajar mengubah file materi kuliah (.pdf) menjadi soal pilihan ganda dan esai secara otomatis. Aplikasi ini menggabungkan teknologi LLM (Large Language Model), klasifikasi tingkat kesluitan (Neural Network), dan clustering topic (K-Means).

👉 **Coba langsung di web:** [https://soalbot.streamlit.app/](https://soalbot.streamlit.app/)

---

## 🚀 Fitur Unggulan

- 🔍 Ekstraksi teks dari file PDF
- 🧠 Deteksi tingkat kesulitan kalimat (Easy, Medium, Hard)
- 🗂️ Clustering topik materi (K-Means)
- 📝 Pembuatan soal otomatis (HOTS):
  - Soal **pilihan ganda** (berformat A–D)
  - Soal **esai** berbobot analitis
- 📄 Ringkasan otomatis dari file materi
- ✅ Evaluasi jawaban PG
- 💾 Unduh PDF ringkasan

---

## 📂 Struktur Direktori

```
soal-bot/
├── app.py
├── requirements.txt
├── README.md
├── backend/
│   ├── extract.py
│   ├── sentence_utils.py
│   ├── difficulty_classifier.py
│   ├── topic_cluster.py
│   └── question_generator.py
├── model/
│   ├── difficulty_model_dl.h5
│   ├── label_encoder.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── kmeans_topic.pkl
│   └── kalimat_difficulty_100.xlsx
└── train/
    └── train_difficulty_model.py
    └── train_topic_cluster.py

```

---

## ⚙️ Jalankan Lokal

### 1. Clone repo
```bash
git clone https://github.com/username/soal-bot.git
cd soal-bot
```

### 2. Install dependensi
```bash
pip install -r requirements.txt
```
Jika error di spaCy, tambahkan model bahasa:
```bash
python -m spacy download en_core_web_sm
```

### 3. Jalankan app
```bash
streamlit run app.py
```

---

## ☁️ Deploy ke Streamlit Cloud

### 1. Isi `requirements.txt`:
```
streamlit==1.33.0
requests
fpdf
spacy==3.7.2
scikit-learn
pandas
numpy
joblib
```

### 2. Tambahkan secrets:
Masuk ke `Settings > Secrets` dan isi:
```toml
OPENROUTER_API_KEY = "sk-or-..."
```

### 3. Download spaCy model jika perlu:
Tambahkan baris ke `app.py` jika model belum tersedia:
```python
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
```

---

## 🤖 Teknologi yang Digunakan

| Komponen      | Teknologi                           |
|---------------|--------------------------------------|
| Frontend      | Streamlit                            |
| NLP Prepro    | spaCy                                |
| Clustering    | KMeans (Scikit-Learn)                |
| Classifier    | Logistic Regression (Scikit-Learn)   |
| LLM           | Mixtral-8x7b via OpenRouter API      |
| Export PDF    | FPDF                                 |

---

## 🔐 Keamanan

- API Key tidak ditulis langsung di kode.
- Gunakan `st.secrets` untuk keamanan di cloud.
- Model `.pkl` dan `.xlsx` tidak mengandung data sensitif.

---

## 👨‍💻 Team

| Nama                   | NPM                                  |
|------------------------|--------------------------------------|
|  Senia Nur Hasanah     | 140810230021                         |
|  Siti Nailah Eko       | 140810230059                         |
|  Ammara Azwadiena A    | 140810230073                         |


---

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License. Bebas digunakan, dimodifikasi, dan dikembangkan lebih lanjut.

---

## 🌐 Akses Aplikasi Online

👉 Jalankan aplikasi langsung via browser:
**[https://soal-bot.streamlit.app](https://soal-bot.streamlit.app)**
