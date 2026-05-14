import streamlit as st
import requests
from PIL import Image
import io

import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Image Label Detection",
    page_icon="🔍",
    layout="centered",
)

st.title("🔍 Image Label Detection")
st.caption("Powered by Amazon Rekognition")

st.divider()

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "webp"],
    help="Supported formats: JPEG, PNG, WEBP",
)

min_confidence = st.slider(
    "Minimum Confidence (%)",
    min_value=50,
    max_value=99,
    value=70,
    step=1,
    help="Filter labels below this confidence threshold",
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if st.button("🚀 Detect Labels", use_container_width=True, type="primary"):
        with st.spinner("Analyzing image with Amazon Rekognition..."):
            uploaded_file.seek(0)
            files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}

            try:
                response = requests.post(f"{BACKEND_URL}/detect", files=files)
                response.raise_for_status()
                result = response.json()

                labels = [l for l in result["labels"] if l["confidence"] >= min_confidence]

                st.divider()
                st.subheader(f"✅ Detected {len(labels)} Labels")

                if not labels:
                    st.warning("No labels found above the confidence threshold.")
                else:
                    for label in labels:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{label['name']}**")
                            if label["categories"]:
                                st.caption("Categories: " + ", ".join(label["categories"]))
                        with col2:
                            confidence = label["confidence"]
                            color = "green" if confidence >= 90 else "orange" if confidence >= 75 else "red"
                            st.markdown(
                                f"<span style='color:{color}; font-weight:bold'>{confidence}%</span>",
                                unsafe_allow_html=True,
                            )
                        st.progress(confidence / 100)

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure FastAPI is running on port 8000.")
            except requests.exceptions.HTTPError as e:
                st.error(f"❌ API Error: {response.json().get('detail', str(e))}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")