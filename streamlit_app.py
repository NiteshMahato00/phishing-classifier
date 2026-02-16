import streamlit as st
import pandas as pd
import pickle
import os

st.title("Phishing Detection App")

model_path = os.path.join("artifacts", "model.pkl")

@st.cache_resource
def load_model():
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(df)

    if st.button("Predict"):
        predictions = model.predict(df)
        df["Prediction"] = predictions
        df["Prediction"] = df["Prediction"].map({0: "phishing", 1: "safe"})
        
        st.success("Prediction completed!")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Prediction File",
            csv,
            "predicted_file.csv",
            "text/csv",
        )