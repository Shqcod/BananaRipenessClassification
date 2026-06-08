import streamlit as st
import requests

st.title("🍌 Banana Ripeness Classification")

uploaded_file = st.file_uploader(
    "Upload Banana Image",
    type=["jpg","jpeg","png"]
)

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Uploaded Image",
        use_container_width=True
    )

    if st.button("Predict"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            files=files
        )

        result = response.json()

        st.success(
            f"Label : {result['label']}"
        )

        st.info(
            f"Confidence : {result['confidence']}%"
        )