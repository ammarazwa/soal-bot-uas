import requests
import streamlit as st
import re
import os
from dotenv import load_dotenv
load_dotenv()  # Memuat variabel dari .env ke os.environ


try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "DUMMY_API_KEY")

def generate_mcq_llm(sentence, label=None, topic=None):
    prompt = (
        "Dari kalimat berikut:\n"
        f"\"{sentence}\"\n\n"
        "Buatkan satu soal pilihan ganda berbasis HOTS.\n"
        "Format output HARUS seperti ini:\n"
        "Pertanyaan: <isi pertanyaan>\n"
        "A. ...\nB. ...\nC. ...\nD. ...\nJawaban yang benar: <huruf>\n"
        "Tulis dalam Bahasa Indonesia."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://soalbot.streamlit.app",
        "X-Title": "SoalBot"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "Kamu adalah AI yang membuat soal HOTS."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            text = response.json()["choices"][0]["message"]["content"].strip()
            return {"question_raw": text, "label": label, "topic": topic}
        else:
            return {"question_raw": f"⚠ Error {response.status_code}: {response.text}", "label": label, "topic": topic}
    except Exception as e:
        return {"question_raw": f"❌ Error: {str(e)}", "label": label, "topic": topic}

def generate_bulk_essay_llm(text, num_questions):
    prompt = (
        f"Buatkan {num_questions} soal essay HOTS dari materi berikut:\n\n{text}\n\n"
        f"Format: 1. <soal 1>\n2. <soal 2>\n... dst."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://soalbot.streamlit.app",
        "X-Title": "SoalBot"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "Kamu adalah AI pembuat soal essay HOTS."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            text = response.json()["choices"][0]["message"]["content"].strip()
            questions = re.findall(r"\d+\.\s+(.*?)(?=\n\d+\.|\Z)", text, re.DOTALL)
            if not questions:
                return [{"question": text or "⚠ Gagal menghasilkan soal.", "label": None, "topic": None}]
            return [{"question": q.strip(), "label": None, "topic": None} for q in questions[:num_questions]]
        else:
            return [{"question": f"⚠ Error {response.status_code}: {response.text}", "label": None, "topic": None}]
    except Exception as e:
        return [{"question": f"❌ Exception: {str(e)}", "label": None, "topic": None}]

def generate_summary_llm(text):
    prompt = (
        f"Berikan ringkasan singkat dan jelas dalam Bahasa Indonesia dari materi berikut:\n\n{text}\n\n"
        f"Ringkasan maksimal 200 kata."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://soalbot.streamlit.app",
        "X-Title": "SoalBot"
    }

    payload = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {"role": "system", "content": "Kamu adalah AI yang meringkas materi kuliah."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.5
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"⚠ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"
