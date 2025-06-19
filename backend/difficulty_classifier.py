# difficulty_classifier.py
from tensorflow.keras.models import load_model
import os
import os
import joblib
import numpy as np

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, '..', 'model', 'difficulty_model_dl.h5')
model = load_model(model_path)

# Load vectorizer TF-IDF
vectorizer_path = os.path.join(base_dir, '..', 'model', 'tfidf_vectorizer.pkl')
vectorizer = joblib.load(vectorizer_path)

# Load label encoder jika ingin hasil label string
label_encoder_path = os.path.join(base_dir, '..', 'model', 'label_encoder.pkl')
label_encoder = joblib.load(label_encoder_path)

# Fungsi prediksi
def predict_difficulty(sentence):
    x = vectorizer.transform([sentence])  # dari teks jadi vektor
    y_pred = model.predict(x.toarray())  # model keras expect array, bukan sparse matrix
    label_index = np.argmax(y_pred)
    return label_encoder.inverse_transform([label_index])[0]



