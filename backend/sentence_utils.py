# sentence_utils.py
import re

def split_sentences(text):
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    return sentences

# Fungsi untuk menyaring kalimat yang tidak layak dijadikan soal
def is_valid_sentence(sentence):
    if len(sentence.split()) < 35:  # Kalimat terlalu pendek
        return False
    if sum(c.isdigit() for c in sentence) > 20 or sum(c.isupper() for c in sentence) > len(sentence) * 0.5:
        return False  # Terlalu banyak angka atau huruf kapital
    if re.search(r"\d{10,}", sentence):  # Hindari nomor panjang (telepon, NIM)
        return False
    return True