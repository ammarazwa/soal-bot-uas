import streamlit as st  
import re  
# import os
# import requests  
# import spacy  
# import random  

# Import fungsi backend
from backend.extract import extract_text_from_pdf  
from backend.sentence_utils import split_sentences 
from backend.sentence_utils import is_valid_sentence
from backend.difficulty_classifier import predict_difficulty  
from backend.topic_cluster import predict_cluster  
from backend.question_generator import generate_mcq_llm
from backend.question_generator import generate_bulk_essay_llm
from backend.question_generator import generate_summary_llm

# ==================== USER INTERFACE - STREAMLIT =================

# Konfigurasi awal tampilan
st.set_page_config(page_title="SoalBot", layout="centered")
st.title("SoalBot - Ubah Materi Jadi Soal Otomatis")

# Inisialisasi session state untuk menyimpan data antar halaman
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'soal_mcq' not in st.session_state:
    st.session_state.soal_mcq = []
if 'soal_essay' not in st.session_state:
    st.session_state.soal_essay = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'soal_type' not in st.session_state:
    st.session_state.soal_type = "Pilihan Ganda"
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "🏠 Home"

# Sidebar navigasi halaman
selected_page = st.sidebar.selectbox(
    "📖 Navigasi Halaman:",
    ["🏠 Home", "📂 Upload Materi", "📄 Ringkasan", "📝 Lihat Soal"],
    index=["🏠 Home", "📂 Upload Materi", "📄 Ringkasan", "📝 Lihat Soal"].index(st.session_state.selected_page)
)
st.session_state.selected_page = selected_page


# Menentukan halaman aktif
if selected_page == "🏠 Home":
    st.session_state.page = 'home'
elif selected_page == "📂 Upload Materi":
    st.session_state.page = 'upload'
elif selected_page == "📝 Lihat Soal":
    if not st.session_state.soal_mcq and not st.session_state.soal_essay:
        st.warning("⚠ Belum ada soal yang digenerate. Silakan upload dan klik 'Customize Soal' terlebih dahulu.")
        st.session_state.page = 'upload'
    else:
        st.session_state.page = 'soal'
elif selected_page == "📄 Ringkasan":
    st.session_state.page = 'ringkasan'

# ========================== HALAMAN HOME ==========================
if st.session_state.page == 'home':
    st.title("🏠 Selamat Datang di SoalBot!")
    st.markdown("""
    SoalBot adalah aplikasi berbasis AI yang dirancang untuk mengubah file materi (.pdf) menjadi soal otomatis.
    Kamu bisa menghasilkan soal *Pilihan ganda, esai. atau campuran hanya dengan beberapa klik!

    Fitur:
    - Ekstraksi materi dari PDF
    - Deteksi tingkat kesulitan kalimat
    - Generasi soal pilihan ganda HOTS
    - Generasi soal essay HOTS
    - Evaluasi otomatis jawaban pilihan ganda

    Cara Menggunakan:
    1. Masuk ke halaman Upload Materi
    2. Unggah file PDF
    3. Pilih jenis dan jumlah soal
    4. Klik tombol "Customize Soal"
    5. Lihat soal dan jawab di halaman Lihat Soal

    Aplikasi ini menggunakan model LLM dan Klasifikasi topik dan tingkat kesulitan untuk membuat soal yang bervariasi dan menantang
    """)

# ========================== HALAMAN UPLOAD ==========================
elif st.session_state.page == 'upload':
    uploaded_file = st.file_uploader("Unggah file materi (.pdf)", type="pdf")
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        st.success("File berhasil diunggah!")

        if st.button("Summarize" ):
            text = extract_text_from_pdf("temp.pdf")
            summary = generate_summary_llm(text)
            st.session_state.summary = summary
            st.session_state.text = text
            st.session_state.page = 'ringkasan'
            st.session_state.selected_page = "📄 Ringkasan"
            st.rerun()

# ========================== HALAMAN SOAL ==========================
elif st.session_state.page == 'soal':
    st.subheader("Hasil Generate SoalBot")
    jawaban_benar = []

    for i, q in enumerate(st.session_state.soal_mcq):
        lines = q['question_raw'].strip().splitlines()
        question_text = ""
        options = []
        correct_answer = ""

        for line in lines:
            line = line.strip()
            if line.lower().startswith("pertanyaan:"):
                question_text = line.split(":", 1)[1].strip()
            elif re.match(r"^[A-Da-d][\.\)]", line) and len(options) < 4:
                options.append(line)
            elif "jawaban yang benar" in line.lower():
                raw = line.split(":")[-1].strip()
                correct_match = re.match(r"^([A-Da-d])", raw)
                if correct_match:
                    correct_answer = correct_match.group(1).upper()

        jawaban_benar.append(correct_answer)
        st.markdown(f"{i+1}. {question_text}")
        # Setup state untuk setiap radio key
        if f"radio_key_{i}" not in st.session_state:
            st.session_state[f"radio_key_{i}"] = f"mcq_{i}_v1"

        # Tombol Clear
        if st.button("Clear Choice", key=f"clear_{i}"):
            st.session_state.user_answers[i] = None
            # Ganti key agar radio rerender ulang
            current_key = st.session_state[f"radio_key_{i}"]
            new_key = current_key + "_x"
            st.session_state[f"radio_key_{i}"] = new_key
            st.rerun()

        # Render radio dengan key dinamis
        st.session_state.user_answers[i] = st.radio(
            "Pilih jawaban:",
            options,
            key=st.session_state[f"radio_key_{i}"],
            index=None
        )

        if q['label']:
            st.markdown(f"Tingkat Kesulitan: {q['label']}")
        if q['topic'] is not None:
            st.markdown(f"Topik: {q['topic']+1}")

    if st.session_state.soal_essay:
        st.markdown("---")
        st.markdown("### Soal Essay")
        for i, q in enumerate(st.session_state.soal_essay):
            st.markdown(f"{i+1}. {q['question']}")
            if q['label']:
                st.markdown(f"Tingkat Kesulitan: {q['label']}")
            if q['topic'] is not None:
                st.markdown(f"Topik: {q['topic']+1}")
            st.text_area("Jawaban Anda:", key=f"essay_{i}")

    if st.button("Lihat Skor"):
        benar = 0
        for i in range(len(st.session_state.user_answers)):
            user_ans = st.session_state.user_answers[i]
            kunci = jawaban_benar[i]
            if user_ans:
                match = re.match(r"^([A-Da-d])[\.\)]", user_ans.strip())
                if match and match.group(1).upper() == kunci.upper():
                    benar += 1
            st.markdown(f"Soal {i+1}: Jawaban Anda: {user_ans or '❌ Kosong'} — Kunci: {kunci}")
        st.success(f"Skor Pilihan Ganda Anda: {benar} dari {len(jawaban_benar)}")
        if st.session_state.soal_essay:
            st.info("Soal Essay tidak dinilai otomatis.")

# ========================== HALAMAN RINGKASAN ==========================
elif st.session_state.page == 'ringkasan':
    from fpdf import FPDF
    import tempfile
    import textwrap

    st.title("📄 Ringkasan Materi")
    if 'summary' in st.session_state:
        st.write(st.session_state.summary)

        # Tombol unduh PDF ringkasan
        class PDF(FPDF):
            def header(self):
                self.set_font("Times", "B", 12)
                from fpdf.enums import XPos, YPos
                self.cell(0, 10, "Ringkasan Materi", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            def footer(self):
                self.set_y(-15)
                self.set_font("Times", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Times", size=12)

        # Cetak ringkasan sebagai satu blok teks dengan justify
        summary_text = st.session_state.summary.replace("\n", " ")
        pdf.multi_cell(0, 10, summary_text, align="J")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.output(tmp.name)
            with open(tmp.name, "rb") as f:
                st.download_button("💾 Unduh Ringkasan (PDF)", f.read(), file_name="ringkasan.pdf")

        num_questions = st.slider("Jumlah soal", 1, 10, 5)
        soal_type = st.selectbox("Pilih jenis soal:", ["Pilihan Ganda", "Essay", "Campur"])
        st.session_state.soal_type = soal_type

        if st.button("Generate Soal"):
            text = st.session_state.text
            kalimat_list = split_sentences(text)
            valid_sentences = [s for s in kalimat_list if is_valid_sentence(s)]

        if not valid_sentences:
            st.warning("❌ Tidak ada kalimat yang layak dijadikan soal.")
            st.stop()

        soal_mcq = []
        soal_essay = []

        if soal_type == "Essay":
            soal_essay = generate_bulk_essay_llm(text, num_questions)

        elif soal_type == "Pilihan Ganda":
            for kalimat in valid_sentences:
                if len(soal_mcq) >= num_questions:
                    break
                level = predict_difficulty(kalimat)
                try:
                    topic = predict_cluster(kalimat)
                except:
                    topic = None
                soal = generate_mcq_llm(kalimat, label=level, topic=topic)
                if soal:
                    soal_mcq.append(soal)

        elif soal_type == "Campur":
            count_mcq = 0
            count_essay = 0
            for i, kalimat in enumerate(valid_sentences):
                if count_mcq + count_essay >= num_questions:
                    break
                level = predict_difficulty(kalimat)
                try:
                    topic = predict_cluster(kalimat)
                except:
                    topic = None
                if i % 2 == 0 and count_mcq < (num_questions // 2 + num_questions % 2):
                    soal = generate_mcq_llm(kalimat, label=level, topic=topic)
                    if soal:
                        soal_mcq.append(soal)
                        count_mcq += 1
                else:
                    soal_list = generate_bulk_essay_llm(kalimat, 1)
                    if soal_list:
                        soal_essay.extend(soal_list)
                        count_essay += 1

        # Simpan ke session dan pindah ke halaman soal
        st.session_state.soal_mcq = soal_mcq
        st.session_state.soal_essay = soal_essay
        st.session_state.user_answers = [None] * len(soal_mcq)
        st.session_state.page = 'soal'
        st.session_state.selected_page = "📝 Lihat Soal"
        st.rerun()

    else:
        st.info("Belum ada ringkasan. Silakan upload materi terlebih dahulu.")