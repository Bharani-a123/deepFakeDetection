import streamlit as st
import requests
import time

# Backend endpoints
API_BASE = "http://127.0.0.1:8000"
IMAGE_URL = f"{API_BASE}/detect-image/"
VIDEO_URL = f"{API_BASE}/detect-video/"
WEBCAM_URL = f"{API_BASE}/detect-webcam-frame/"

# Page configuration
st.set_page_config(
    page_title="AI Deepfake Detector", 
    page_icon="🔍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(255, 107, 107, 0.3)); }
        to { filter: drop-shadow(0 0 30px rgba(69, 183, 209, 0.5)); }
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
    }
    
    .stRadio > div {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stRadio label {
        color: white !important;
        font-weight: 500;
        font-size: 1.1rem;
    }
    
    .upload-section {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        background: linear-gradient(45deg, #ff5252, #26c6da);
    }
    
    .result-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .fake-result {
        color: #e74c3c;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .real-result {
        color: #27ae60;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 2px dashed rgba(255, 255, 255, 0.3);
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: rgba(255, 255, 255, 0.6);
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stImage > div {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🔍 AI Deepfake Detector</h1>
    <p class="subtitle">Advanced AI-powered detection system for identifying synthetic media</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### 🎯 Detection Modes")
mode = st.sidebar.radio(
    "",
    ["📸 Image Detection", "🎥 Video Detection", "📹 Webcam Detection"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### ℹ️ About
This AI system uses advanced deep learning models to detect deepfakes and synthetic media with high accuracy.

**Features:**
- Real-time detection
- Multiple format support
- High accuracy analysis
- Detailed confidence scores
""")

# Main content based on selected mode
if mode == "📸 Image Detection":
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📸 Upload Image for Analysis")
    
    uploaded_image = st.file_uploader(
        "Choose an image file", 
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG"
    )
    
    if uploaded_image:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_image, caption="📷 Uploaded Image", use_container_width=True)
        
        with col2:
            st.markdown("### 🔍 Analysis")
            if st.button("🚀 Analyze Image", key="analyze_img"):
                with st.spinner("🤖 AI is analyzing your image..."):
                    files = {"file": (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)}
                    response = requests.post(IMAGE_URL, files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Determine if fake or real
                        fake_prob = result.get('fake', 0)
                        real_prob = result.get('real', 0)
                        
                        verdict = "FAKE" if fake_prob > real_prob else "REAL"
                        confidence = max(fake_prob, real_prob) * 100
                        
                        result_class = "fake-result" if verdict == "FAKE" else "real-result"
                        
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-title">🎯 Detection Results</div>
                            <div class="{result_class}">Verdict: {verdict}</div>
                            <div style="margin: 1rem 0;">
                                <div class="metric-card">
                                    <strong>Confidence: {confidence:.1f}%</strong>
                                </div>
                                <div style="margin-top: 1rem;">
                                    <div>🔴 Fake Probability: {fake_prob:.3f}</div>
                                    <div>🟢 Real Probability: {real_prob:.3f}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Analysis failed. Status code: {response.status_code}")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif mode == "🎥 Video Detection":
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 🎥 Upload Video for Analysis")
    
    uploaded_video = st.file_uploader(
        "Choose a video file", 
        type=["mp4", "avi", "mov"],
        help="Supported formats: MP4, AVI, MOV"
    )
    
    if uploaded_video:
        st.video(uploaded_video)
        
        if st.button("🚀 Analyze Video", key="analyze_vid"):
            with st.spinner("🎬 Processing video frames... This may take a while."):
                files = {"file": (uploaded_video.name, uploaded_video.read(), uploaded_video.type)}
                response = requests.post(VIDEO_URL, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    verdict = result['video_verdict'].upper()
                    verdict_class = "fake-result" if verdict == "FAKE" else "real-result"
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">🎬 Video Analysis Results</div>
                        <div class="{verdict_class}">Overall Verdict: {verdict}</div>
                        <div style="margin-top: 1.5rem;">
                            <div class="metric-card">
                                <strong>Average Fake Probability: {result['average_fake_prob']:.3f}</strong>
                            </div>
                            <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                                <div class="metric-card" style="flex: 1;">
                                    <div>📊 Total Frames</div>
                                    <div style="font-size: 1.5rem; font-weight: bold;">{result['total_frames']}</div>
                                </div>
                                <div class="metric-card" style="flex: 1;">
                                    <div>✅ Processed</div>
                                    <div style="font-size: 1.5rem; font-weight: bold;">{result['frames_processed']}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Video analysis failed. Status code: {response.status_code}")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif mode == "📹 Webcam Detection":
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📹 Real-time Webcam Analysis")
    
    frame = st.camera_input("📸 Capture a frame from your webcam")
    
    if frame:
        if st.button("🚀 Analyze Frame", key="analyze_cam"):
            with st.spinner("📹 Analyzing webcam frame..."):
                files = {"frame": ("frame.jpg", frame.getvalue(), "image/jpeg")}
                response = requests.post(WEBCAM_URL, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    fake_prob = result.get('fake', 0)
                    real_prob = result.get('real', 0)
                    
                    verdict = "FAKE" if fake_prob > real_prob else "REAL"
                    confidence = max(fake_prob, real_prob) * 100
                    
                    result_class = "fake-result" if verdict == "FAKE" else "real-result"
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">📹 Webcam Frame Analysis</div>
                        <div class="{result_class}">Verdict: {verdict}</div>
                        <div style="margin: 1rem 0;">
                            <div class="metric-card">
                                <strong>Confidence: {confidence:.1f}%</strong>
                            </div>
                            <div style="margin-top: 1rem;">
                                <div>🔴 Fake Probability: {fake_prob:.3f}</div>
                                <div>🟢 Real Probability: {real_prob:.3f}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Frame analysis failed. Status code: {response.status_code}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.7); padding: 2rem;">
    <p>🤖 Powered by Advanced AI • Built with ❤️ for Digital Security</p>
</div>
""", unsafe_allow_html=True)