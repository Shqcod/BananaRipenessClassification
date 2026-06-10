import streamlit as st
import requests
import base64
import io
from PIL import Image

# Set page config
st.set_page_config(
    page_title="BananaScan - Analyzer",
    page_icon="🍌",
    layout="centered"
)

# Initialize Session State
if "step" not in st.session_state:
    st.session_state.step = "upload"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None
if "uploader_counter" not in st.session_state:
    st.session_state.uploader_counter = 0

# Custom CSS Injection (Dark Mode Theme)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* Hide default streamlit UI */
header {visibility: hidden; height: 0px !important;}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
div[data-testid="stDecoration"] {display: none;}

/* Body styling (Dark Mode) */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0b0f17 !important;
    font-family: 'Hanken Grotesk', sans-serif !important;
    color: #ffffff !important;
}

[data-testid="stAppViewBlockContainer"] {
    max-width: 720px !important;
    padding-top: 4.5rem !important;
    padding-bottom: 2rem !important;
    margin: 0 auto !important;
}

/* Header style (Dark Mode) */
.custom-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 2rem;
    background-color: #111827;
    border-bottom: 1px solid #1f2937;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 999;
    box-sizing: border-box;
}
.header-logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.header-logo-text {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #facc15;
}
.header-nav {
    display: flex;
    align-items: center;
}
.header-nav-link {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #facc15;
    text-decoration: none;
    border-bottom: 2px solid #facc15;
    padding-bottom: 0.25rem;
}

/* Card container (Dark Mode) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111827 !important;
    border: 1px solid #1f2937 !important;
    border-radius: 1.5rem !important;
    padding: 0px !important;
    box-shadow: 0px 4px 25px rgba(0, 0, 0, 0.3) !important;
    max-width: 720px !important;
    margin: 0 auto !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

/* Reset inner vertical block gaps inside the card */
div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlock"] {
    padding: 0px !important;
    gap: 0px !important;
}

/* Card content padding wrapper */
.card-content-wrapper {
    padding: 2.5rem 3.5rem !important;
    display: flex !important;
    flex-direction: column !important;
    box-sizing: border-box !important;
}

/* Titles (Dark Mode) */
.card-title {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    line-height: 40px;
    text-align: center;
    color: #ffffff;
    margin-bottom: 0.75rem;
    margin-top: 0;
}
.card-subtitle {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 400;
    line-height: 22px;
    text-align: center;
    color: #94a3b8;
    margin-bottom: 2.25rem;
}

/* Upload Area container spacing */
.upload-container {
    position: relative;
    width: 100%;
    margin-bottom: 1.5rem !important;
}
.custom-upload-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2px dashed #10b981;
    border-radius: 1rem;
    background-color: #1f2937;
    padding: 2rem 1.5rem;
    height: 220px;
    box-sizing: border-box;
    text-align: center;
    transition: all 0.3s ease;
}
.custom-upload-box.has-file {
    padding: 1.5rem;
    border-style: solid;
}
.camera-circle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background-color: #facc15;
    margin-bottom: 1rem;
}
.upload-title {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 0.25rem;
}
.upload-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    color: #94a3b8;
}
.upload-preview-img {
    max-width: 100%;
    max-height: 140px;
    border-radius: 0.5rem;
    object-fit: contain;
    margin-bottom: 0.75rem;
}
.file-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
}
.file-name {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
}
.file-change-text {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 12px;
    color: #facc15;
    text-decoration: underline;
}

/* Style the native file uploader container directly to be transparent and borderless */
div[data-testid="stFileUploader"] {
    width: 100% !important;
    background-color: transparent !important;
    border: none !important;
    padding: 0px !important;
    margin: 0.5rem 0 0 0 !important;
}
div[data-testid="stFileUploader"] section {
    background-color: transparent !important;
    border: none !important;
    padding: 0px !important;
}
div[data-testid="stFileUploaderDropzone"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0px !important;
    justify-content: flex-start !important;
    gap: 1rem !important;
}

/* File uploader helper text color */
div[data-testid="stFileUploader"] span, 
div[data-testid="stFileUploader"] div {
    color: #94a3b8 !important;
}

/* Style the native browse files button inside the file uploader widget to match yellow gold */
div[data-testid="stFileUploader"] button {
    height: 40px !important;
    width: auto !important;
    padding: 0.5rem 1.5rem !important;
    font-size: 14px !important;
    background-color: #facc15 !important;
    color: #6c5700 !important;
    border: none !important;
    border-radius: 0.5rem !important;
    box-shadow: 0px 4px 6px rgba(115, 92, 0, 0.1) !important;
    cursor: pointer !important;
}
div[data-testid="stFileUploader"] button p {
    color: #6c5700 !important;
    font-weight: 700 !important;
}
div[data-testid="stFileUploader"] button:hover {
    background-color: #eec200 !important;
}

/* Global button styling (Classify & Reset) - Yellow background, gold text, 100% width */
div[data-testid="stButton"] button {
    background-color: #facc15 !important;
    color: #6c5700 !important;
    border: none !important;
    border-radius: 0.5rem !important;
    font-family: 'Hanken Grotesk', sans-serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    width: 100% !important;
    height: 52px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0px 4px 10px rgba(115, 92, 0, 0.1) !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stButton"] button p {
    color: #6c5700 !important;
    margin: 0 !important;
    font-weight: 700 !important;
}

div[data-testid="stButton"] button:hover {
    background-color: #eec200 !important;
    box-shadow: 0px 6px 14px rgba(115, 92, 0, 0.15) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stButton"] button:active {
    transform: translateY(0px) !important;
}

/* Brain icon (brown) for Classify button */
div[data-testid="element-container"]:has(.classify-btn-container) + div[data-testid="element-container"] button p::before {
    content: "";
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 8px;
    vertical-align: middle;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%236c5700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.44 2.5 2.5 0 0 1 0-3.12 3 3 0 0 1 0-3.88 2.5 2.5 0 0 1 0-3.12A2.5 2.5 0 0 1 9.5 2zM14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.44 2.5 2.5 0 0 0 0-3.12 3 3 0 0 0 0-3.88 2.5 2.5 0 0 0 0-3.12A2.5 2.5 0 0 0 14.5 2z"/></svg>');
    background-size: contain;
    background-repeat: no-repeat;
}

/* Camera icon (brown) for Reset button */
div[data-testid="element-container"]:has(.reset-btn-container) + div[data-testid="element-container"] button p::before {
    content: "";
    display: inline-block;
    width: 18px;
    height: 18px;
    margin-right: 8px;
    vertical-align: middle;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%236c5700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>');
    background-size: contain;
    background-repeat: no-repeat;
}

/* Result Screen Layout */
.result-image-container {
    position: relative;
    width: 100%;
    height: 380px;
    overflow: hidden;
    margin: 0;
    padding: 0;
}
.result-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.verified-badge {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    background-color: #facc15;
    color: #6c5700;
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
}
.result-content-wrapper {
    padding: 2.5rem 3.5rem 3.5rem 3.5rem !important;
    display: flex !important;
    flex-direction: column !important;
    box-sizing: border-box !important;
}

.classification-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
}
.classification-left {
    display: flex;
    flex-direction: column;
}
.muted-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94a3b8;
    margin-bottom: 0.25rem;
}
.class-label {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
}
.confidence-badge {
    background-color: #065f46;
    color: #34d399;
    padding: 0.5rem 1rem;
    border-radius: 0.75rem;
    text-align: right;
    box-shadow: 0px 2px 8px rgba(0, 109, 54, 0.2);
}
.conf-title {
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 10px;
    font-weight: 500;
    color: #a7f3d0;
    margin-bottom: 0.1rem;
}
.conf-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# Fixed Custom Header
st.markdown("""
<div class="custom-header">
    <div class="header-logo">
        <svg class="header-logo-icon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#facc15" stroke-width="2">
            <path d="M12 2L19.07 4.93L22 12L19.07 19.07L12 22L4.93 19.07L2 12L4.93 4.93L12 2Z" fill="none" stroke="#facc15" stroke-width="2"/>
            <circle cx="12" cy="12" r="5" fill="#facc15"/>
            <path d="M12 9v6M9 12h6" stroke="#111827" stroke-width="1.5"/>
        </svg>
        <span class="header-logo-text" style="color: #ffffff !important;">BananaScan</span>
    </div>
    <div class="header-nav">
        <a href="#" class="header-nav-link">Analyzer</a>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------
# UPLOAD STEP
# -----------------
if st.session_state.step == "upload":
    with st.container(border=True): # Use native border container wrapper
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-content-wrapper">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="card-title">Klasifikasi Kematangan Pisang</h1>', unsafe_allow_html=True)
        st.markdown('<p class="card-subtitle">Unggah foto pisang untuk memeriksa tingkat kematangannya dengan model penilaian kami.</p>', unsafe_allow_html=True)
        
        # Prepare upload box HTML
        if st.session_state.uploaded_file is None:
            upload_html = """
            <div class="custom-upload-box">
                <div class="camera-circle">
                    <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#6c5700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h3l2-3h4l2 3h3a2 2 0 0 1 2 2z" />
                        <circle cx="12" cy="13" r="3" />
                        <line x1="18" y1="9" x2="18" y2="13" />
                        <line x1="16" y1="11" x2="20" y2="11" />
                    </svg>
                </div>
                <div class="upload-title">Masukkan Gambar Pisang</div>
                <div class="upload-subtitle">MENDUKUNG JPG, PNG, WEBP</div>
            </div>
            """
        else:
            file_bytes = st.session_state.uploaded_file.getvalue()
            img_b64 = base64.b64encode(file_bytes).decode('utf-8')
            mime_type = st.session_state.uploaded_file.type
            upload_html = f"""
            <div class="custom-upload-box has-file">
                <img src="data:{mime_type};base64,{img_b64}" class="upload-preview-img" />
                <div class="file-info">
                    <svg class="file-check-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#006d36" stroke-width="2">
                        <circle cx="12" cy="12" r="10" fill="#6dfe9c" stroke="none" />
                        <path d="M9 12l2 2 4-4" stroke="#006d36" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                    <span class="file-name">{st.session_state.uploaded_file.name}</span>
                </div>
            </div>
            """
            
        # Render Upload Area
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        st.markdown(upload_html, unsafe_allow_html=True)
        
        # Native file uploader overlay (renders inline below the graphics)
        uploaded = st.file_uploader(
            label="Upload Image",
            type=["jpg", "jpeg", "png", "webp"],
            key=f"uploader_{st.session_state.uploader_counter}",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True) # close upload-container
        
        # If new file is uploaded, update session state and rerun
        if uploaded != st.session_state.uploaded_file:
            st.session_state.uploaded_file = uploaded
            st.rerun()
            
        # Classify button marker and button
        st.markdown('<div class="classify-btn-container"></div>', unsafe_allow_html=True)
        classify_clicked = st.button("Klasifikasi Kematangan", key="classify_btn_widget")
        
        st.markdown('</div>', unsafe_allow_html=True) # close card-content-wrapper

    # Classify click action
    if classify_clicked:
        if st.session_state.uploaded_file is None:
            st.warning("Mohon unggah foto pisang terlebih dahulu.")
        else:
            try:
                files = {
                    "file": (
                        st.session_state.uploaded_file.name,
                        st.session_state.uploaded_file.getvalue(),
                        st.session_state.uploaded_file.type
                    )
                }
                with st.spinner("Classifying banana ripeness..."):
                    response = requests.post(
                        "http://127.0.0.1:8000/predict",
                        files=files
                    )
                    if response.status_code == 200:
                        st.session_state.prediction_result = response.json()
                        st.session_state.step = "result"
                        st.rerun()
                    else:
                        st.error(f"Error classifying image: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend server: {str(e)}")

# -----------------
# RESULT STEP
# -----------------
elif st.session_state.step == "result":
    # Prepare result data
    result = st.session_state.prediction_result
    label = result["label"]
    confidence = result["confidence"]
    
    label_display = label.capitalize()
    
    file_bytes = st.session_state.uploaded_file.getvalue()
    img_b64 = base64.b64encode(file_bytes).decode('utf-8')
    mime_type = st.session_state.uploaded_file.type
    
    if label == "rotten":
        label_display = "Rotten"
        
    with st.container(border=True): # Use native border container wrapper
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        
        # 1. Image with Verified Badge
        st.markdown(f"""
        <div class="result-image-container">
            <img class="result-image" src="data:{mime_type};base64,{img_b64}" />
            <div class="verified-badge">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#6c5700" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                Verified Result
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Content Details Wrapper
        st.markdown('<div class="result-content-wrapper">', unsafe_allow_html=True)
        
        # Classification Header & Confidence Badge
        st.markdown(f"""
        <div class="classification-row">
            <div class="classification-left">
                <div class="muted-label">CURRENT CLASSIFICATION</div>
                <div class="class-label">{label_display}</div>
            </div>
            <div class="confidence-badge">
                <div class="conf-title">Confidence</div>
                <div class="conf-val">{confidence}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Reset Button Marker and widget
        st.markdown('<div class="reset-btn-container"></div>', unsafe_allow_html=True)
        reset_clicked = st.button("Start New Scan", key="reset_btn_widget")
        
        st.markdown('</div>', unsafe_allow_html=True) # close result-content-wrapper
        
    if reset_clicked:
        st.session_state.step = "upload"
        st.session_state.uploaded_file = None
        st.session_state.prediction_result = None
        st.session_state.uploader_counter += 1
        st.rerun()