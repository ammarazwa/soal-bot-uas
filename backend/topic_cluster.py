# topic_cluster.py
import joblib
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "..", "model", "kmeans_topic.pkl")
model, vectorizer = joblib.load(model_path)

def predict_cluster(sentence):
    X = vectorizer.transform([sentence])
    return model.predict(X)[0]
