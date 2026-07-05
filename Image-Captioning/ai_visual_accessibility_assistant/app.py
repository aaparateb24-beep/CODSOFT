import time

start = time.time()
print("START")
import os 
print("Imported PIL")
print("Imported Plotly")
print("Imported Streamlit")
print("Imported dotenv")
print("Imported BLIP")
print("Imported YOLO")
print("Imported Gemini")
print("Imported Database")
print("Imported Speech")
print("Imported Exporter")
import time
print("Imported PIL")
print("Imported Plotly")
print("Imported Streamlit")
print("Imported dotenv")
print("Imported BLIP")
print("Imported YOLO")
print("Imported Gemini")
print("Imported Database")
print("Imported Speech")
print("Imported Exporter")
import pandas as pd
print("Imported PIL")
print("Imported Plotly")
print("Imported Streamlit")
print("Imported dotenv")
print("Imported BLIP")
print("Imported YOLO")
print("Imported Gemini")
print("Imported Database")
print("Imported Speech")
print("Imported Exporter")
from PIL import Image
print("Imported PIL")
print("Imported Plotly")
print("Imported Streamlit")
print("Imported dotenv")
print("Imported BLIP")
print("Imported YOLO")
print("Imported Gemini")
print("Imported Database")
print("Imported Speech")
print("Imported Exporter")
import plotly.express as px
print("Imported PIL")
print("Imported Plotly")
print("Imported Streamlit")
print("Imported dotenv")
print("Imported BLIP")
print("Imported YOLO")
print("Imported Gemini")
print("Imported Database")
print("Imported Speech")
print("Imported Exporter")
import streamlit as st
print("Imported PIL")
print("Imported Plotly")
print("Imported Streamlit")
print("Imported dotenv")
print("Imported BLIP")
print("Imported YOLO")
print("Imported Gemini")
print("Imported Database")
print("Imported Speech")
print("Imported Exporter")
from dotenv import load_dotenv
print("Imported PIL")
print("Imported Plotly")
print("Imported Streamlit")
print("Imported dotenv")
print("Imported BLIP")
print("Imported YOLO")
print("Imported Gemini")
print("Imported Database")
print("Imported Speech")
print("Imported Exporter")

# Load environment variables
load_dotenv()

# Import local modules
from models.blip_captioner import BlipCaptioner
from models.yolo_detector import YoloDetector
from models.gemini_client import GeminiClient
from utils.database import DatabaseManager
from utils.speech import generate_speech
from utils.document_exporter import generate_txt_report, generate_pdf_report

# Page config
st.set_page_config(
    page_title="AI Visual Accessibility Assistant",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Startup CSS Styles
CUSTOM_CSS = """
<style>
    /* Gradient Background and Theme Tweaks */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f1f5f9;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid #1e293b;
    }
    
    /* Glassmorphism Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        margin-bottom: 15px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.2);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .metric-header {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 5px;
        font-weight: 600;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    /* Detailed description box */
    .desc-box {
        background: rgba(14, 116, 144, 0.15);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        font-size: 1.15rem;
        line-height: 1.6;
        color: #e2e8f0;
    }
    
    /* Tab Styling Override */
    button[data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 600;
        color: #94a3b8;
        padding: 10px 20px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }
    
    /* Chat bubbles */
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .chat-user {
        background: #1e3a8a;
        color: #f8fafc;
        align-self: flex-end;
        margin-left: auto;
    }
    .chat-assistant {
        background: #334155;
        color: #f8fafc;
        align-self: flex-start;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------- SESSION STATE & INITIALIZATION -----------------

# Directory setups
for d in ["uploads", "outputs", "data"]:
    os.makedirs(d, exist_ok=True)

# Initialize SQLite database manager
if "blip_captioner" not in st.session_state:
    st.session_state.blip_captioner = None

if "yolo_detector" not in st.session_state:
    st.session_state.yolo_detector = None

if "gemini_client" not in st.session_state:
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    st.session_state.gemini_client = GeminiClient(gemini_key)

# <<< PUT IT HERE >>>
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager("data/database.db")
    # -----------------------------
# Cache Analytics
# ----------------------------

# Initialize models in session state
if "blip_captioner" not in st.session_state:
    st.session_state.blip_captioner = None
if "yolo_detector" not in st.session_state:
    st.session_state.yolo_detector = None
if "gemini_client" not in st.session_state:
    # Try fetching key from env first
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    st.session_state.gemini_client = GeminiClient(gemini_key)

# App analytical status
if "active_analysis" not in st.session_state:
    st.session_state.active_analysis = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None
if "model_load_status" not in st.session_state:
    st.session_state.model_load_status = {"BLIP": "Not Loaded", "YOLOv8": "Not Loaded"}

def load_local_models():
    """Trigger cached model loading for local models."""
    with st.spinner("Loading BLIP Captioner and YOLOv8 models into memory..."):
        if not st.session_state.blip_captioner:
            st.session_state.blip_captioner = BlipCaptioner(
                os.getenv("BLIP_MODEL_NAME", "Salesforce/blip-image-captioning-base")
            )
            st.session_state.model_load_status["BLIP"] = "Ready"
            
        if not st.session_state.yolo_detector:
            st.session_state.yolo_detector = YoloDetector(
                os.getenv("YOLO_MODEL_NAME", "yolov8n.pt")
            )
            st.session_state.model_load_status["YOLOv8"] = "Ready"

# ----------------- SIDEBAR -----------------

with st.sidebar:
    st.title("👁️ Visual Access AI")
    st.markdown("---")
    
    # Gemini Key Setup
    st.subheader("🔑 Gemini API Settings")
    api_key_input = st.text_input(
        "Enter Gemini API Key", 
        value=st.session_state.gemini_client.api_key or "",
        type="password",
        help="Required for detailed scene descriptions, VQA, and summaries."
    )
    if api_key_input != st.session_state.gemini_client.api_key:
        st.session_state.gemini_client.set_api_key(api_key_input)
        st.success("API Key updated!")
        
    if not st.session_state.gemini_client.is_configured():
        st.warning("⚠️ Gemini API Key is missing. Vision AI features are disabled.")
    else:
        st.success("✅ Gemini API Connected")
        
    st.markdown("---")
    st.subheader("🖥️ Hardware & Models")
    
    # Lazy model loading trigger button
    if st.session_state.model_load_status["BLIP"] == "Not Loaded":
        if st.button("🔌 Initialize Local Models", width="stretch"):
            load_local_models()
            st.rerun()
    else:
        st.info("🤖 Local Models Initialized (CPU/GPU)")
        
    # Metrics
    stats = st.session_state.db.get_analytics()
    st.markdown(f"**Processed Images:** `{stats.get('total_images', 0)}`")
    
    # System settings
    st.markdown("---")
    st.subheader("⚙️ System Control")
    if st.button("🗑️ Clear Database History", type="secondary", width="stretch"):
        st.session_state.db.clear_all_history()
        st.session_state.active_analysis = None
        st.session_state.chat_history = []
        st.session_state.audio_path = None
        st.success("Database cleared!")
        st.rerun()
        
    st.caption("AI Visual Accessibility Assistant v1.0.0")

# ----------------- MAIN INTERFACE -----------------

st.title("AI Visual Accessibility Assistant")
st.markdown("An intelligent companion enabling visually impaired individuals to perceive, navigate, and query their environment.")

# Define main application tabs
tabs = st.tabs([
    "📥 Image Analyzer", 
    "🔊 Accessibility Mode", 
    "💬 Visual Q&A", 
    "📊 Analytics", 
    "📜 History Explorer", 
    "💾 Download Center"
])

# ----------------- TAB 1: UPLOAD & ANALYZE -----------------
with tabs[0]:
    st.header("Upload and Process Image")
    col_upload, col_preview = st.columns([1, 1])
    
    with col_upload:
        # File uploader
        uploaded_file = st.file_uploader(
            "Select an image file (JPG, JPEG, PNG)", 
            type=["jpg", "jpeg", "png"]
        )
        
        if uploaded_file is not None:
            # File specs
            img = Image.open(uploaded_file)
            width, height = img.size
            file_size_kb = len(uploaded_file.getvalue()) / 1024.0
            
            # Save file locally
            temp_path = f"uploads/{uploaded_file.name}"
            img.save(temp_path)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">File Details</div>
                <div><b>Name:</b> {uploaded_file.name}</div>
                <div><b>Resolution:</b> {width} x {height} pixels</div>
                <div><b>File Size:</b> {file_size_kb:.2f} KB</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Trigger analysis
            # Ensure local models are loaded first
            if st.session_state.model_load_status["BLIP"] == "Not Loaded":
                st.warning("⚠️ Local computer vision models are not initialized. Initialize them via the button in the sidebar or below to start.")
                if st.button("Initialize Models & Run", type="primary", width="stretch"):
                    load_local_models()
                    st.rerun()
            else:
                if st.button("🚀 Analyze Image", type="primary", width="stretch"):
                    # Progress indicators
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Step 1: Captioning (BLIP)
                        status_text.text("1/5 Running BLIP Image Captioning...")
                        progress_bar.progress(20)
                        caption, caption_conf = st.session_state.blip_captioner.generate_caption(img)
                        
                        # Step 2: Object Detection (YOLO)
                        status_text.text("2/5 Performing YOLOv8 Object Detection...")
                        progress_bar.progress(40)
                        annotated_img, detections = st.session_state.yolo_detector.detect_objects(img)
                        
                        # Save annotated image
                        annotated_path = f"outputs/annotated_{uploaded_file.name}"
                        annotated_img.save(annotated_path)
                        
                        # Step 3: Scene Understanding (Gemini)
                        status_text.text("3/5 Querying Gemini for Scene Categorization...")
                        progress_bar.progress(60)
                        scene_data = st.session_state.gemini_client.get_scene_understanding(img)
                        
                        # Step 4: Accessibility Description & Summary (Gemini)
                        status_text.text("4/5 Generating Alt-Text and Summary...")
                        progress_bar.progress(80)
                        desc = st.session_state.gemini_client.get_accessibility_description(img)
                        
                        det_names = [d["name"] for d in detections]
                        summary = st.session_state.gemini_client.get_ai_summary(
                            img, caption, det_names, scene_data["category"]
                        )
                        
                        # Step 5: AI Insights
                        status_text.text("5/5 Formulating AI Insights...")
                        progress_bar.progress(95)
                        insights = st.session_state.gemini_client.get_ai_insights(img)
                        
                        # Save to database
                        record_data = {
                            "filename": uploaded_file.name,
                            "resolution": f"{width}x{height}",
                            "file_size_kb": file_size_kb,
                            "caption": caption,
                            "caption_confidence": caption_conf,
                            "scene_category": scene_data["category"],
                            "scene_explanation": scene_data["explanation"],
                            "accessibility_description": desc,
                            "summary": summary,
                            "main_subject": insights["main_subject"],
                            "activity": insights["activity"],
                            "environment": insights["environment"],
                            "context": insights["context"],
                            "use_case": insights["use_case"],
                            "original_image_path": temp_path,
                            "annotated_image_path": annotated_path
                        }
                        
                        history_id = st.session_state.db.save_record(record_data, detections)
                        record_data["id"] = history_id
                        
                        # Update active analysis session state
                        st.session_state.active_analysis = {
                            "record": record_data,
                            "detections": detections
                        }
                        
                        # Clear old audio narration when a new image is processed
                        st.session_state.audio_path = None
                        st.session_state.chat_history = []
                        
                        progress_bar.progress(100)
                        status_text.text("Analysis Complete!")
                        time.sleep(1)
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.success("Image successfully analyzed! Click on the other tabs to view results.")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
                        import traceback
                        st.text(traceback.format_exc())
                        progress_bar.empty()
                        status_text.empty()
                        
    with col_preview:
        st.subheader("Image Views")
        if st.session_state.active_analysis:
            record = st.session_state.active_analysis["record"]
            
            # Show original and annotated tabs
            preview_tabs = st.tabs(["Original", "Object Bounding Boxes (YOLO)"])
            with preview_tabs[0]:
                if os.path.exists(record["original_image_path"]):

                   image = Image.open(record["original_image_path"])
                   st.image(image)
                else:
                    st.image(img, width="stretch")
            with preview_tabs[1]:
                if os.path.exists(record["annotated_image_path"]):
                    st.image(record["annotated_image_path"], width="stretch")
                else:
                    st.info("Annotated view not available.")
        else:
            # Placeholder default view
            st.info("Please upload and run analysis on an image to see details.")

    # Show results panels if an active analysis exists
    if st.session_state.active_analysis:
        record = st.session_state.active_analysis["record"]
        detections = st.session_state.active_analysis["detections"]
        
        st.markdown("---")
        st.subheader("🔍 Local Vision Results")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">BLIP Image Caption</div>
                <div style="font-size: 1.25rem; font-weight: 500; color: #f8fafc; margin-bottom: 5px;">"{record['caption']}"</div>
                <div><b>Confidence:</b> {record['caption_confidence'] * 100:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Scene description
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">Scene Understanding</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: #10b981; margin-bottom: 5px;">{record['scene_category']}</div>
                <div>{record['scene_explanation']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">Detected Objects ({len(detections)})</div>
            </div>
            """, unsafe_allow_html=True)
            if detections:
                df_det = pd.DataFrame(detections)
                df_det["Confidence"] = df_det["confidence"].apply(lambda x: f"{x * 100:.1f}%")
                st.dataframe(df_det[["name", "Confidence"]], width="stretch")
            else:
                st.write("No objects detected above model threshold.")
                
        # Row 2: AI Summary and Insights
        st.markdown("---")
        st.subheader("💡 Generative AI Insights")
        
        c3, c4 = st.columns([3, 2])
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">AI Summary</div>
                <div style="font-size: 1.15rem; line-height: 1.6; color: #e2e8f0;">{record['summary']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown("<div class='metric-header'>Analysis Taxonomy</div>", unsafe_allow_html=True)
            st.markdown(f"**Subject:** {record['main_subject']}")
            st.markdown(f"**Activity:** {record['activity']}")
            st.markdown(f"**Environment:** {record['environment']}")
            st.markdown(f"**Context:** {record['context']}")
            st.markdown(f"**Use Case:** {record['use_case']}")
            st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 2: ACCESSIBILITY MODE & NARRATION -----------------
with tabs[1]:
    st.header("🔊 Audio Narration & Accessibility Reader")
    st.markdown("This section presents the primary visual details in a large, readable text format with a built-in text-to-speech narrator.")
    
    if st.session_state.active_analysis:
        record = st.session_state.active_analysis["record"]
        
        st.subheader("Detailed Image Description")
        st.markdown(f"""
        <div class="desc-box">
            {record['accessibility_description']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Audio Controls")
        
        ac1, ac2 = st.columns([1, 2])
        with ac1:
            tts_engine_choice = st.radio(
                "Select Speech Engine",
                ["High Quality Online (gTTS)", "Local Offline (pyttsx3)"],
                index=0
            )
            
            if st.button("🔊 Generate Audio Narration", type="primary", width="stretch"):
                with st.spinner("Generating speech..."):
                    filename = os.path.splitext(record["filename"])[0]
                    audio_filename = f"outputs/{filename}_speech.mp3"
                    
                    prefer_gtts = "gTTS" in tts_engine_choice
                    success = generate_speech(
                        record['accessibility_description'], 
                        audio_filename, 
                        prefer_gtts=prefer_gtts
                    )
                    
                    if success:
                        st.session_state.audio_path = audio_filename
                        st.success("Audio narration generated successfully!")
                    else:
                        st.error("Could not generate audio. Please check your network connection (for gTTS) or speech drivers (for pyttsx3).")
                        
        with ac2:
            if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
                st.write("### Play Audio")
                st.audio(st.session_state.audio_path)
                
                # Reading audio for download
                with open(st.session_state.audio_path, "rb") as f:
                    audio_bytes = f.read()
                st.download_button(
                    label="💾 Download Audio Narration (MP3)",
                    data=audio_bytes,
                    file_name=os.path.basename(st.session_state.audio_path),
                    mime="audio/mp3",
                    width="stretch"
                )
            else:
                st.info("Click 'Generate Audio Narration' to synthesize voice output.")
    else:
        st.info("Upload and process an image in the 'Image Analyzer' tab to generate accessibility descriptions.")

# ----------------- TAB 3: VISUAL QUESTION ANSWERING (VQA) -----------------
with tabs[2]:
    st.header("💬 Visual Question Answering")
    st.markdown("Ask anything about the image. The AI uses multimodal vision reasoning and maintains session chat history.")
    
    if st.session_state.active_analysis:
        record = st.session_state.active_analysis["record"]
        
        c_img, c_chat = st.columns([1, 2])
        
        with c_img:
            st.image(record["original_image_path"], caption=record["filename"], width="stretch")
            
        with c_chat:
            # Display past messages
            st.markdown("### Conversation")
            chat_container = st.container(height=350)
            
            with chat_container:
                for q, a in st.session_state.chat_history:
                    st.markdown(f'<div class="chat-bubble chat-user">🗣️ <b>You:</b> {q}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-bubble chat-assistant">🤖 <b>AI:</b> {a}</div>', unsafe_allow_html=True)
            
            # Input query
            user_question = st.chat_input("Ask a question about this image...")
            if user_question:
                with st.spinner("Analyzing image details..."):
                    img_obj = Image.open(record["original_image_path"])
                    response_text = st.session_state.gemini_client.answer_question(
                        img_obj, user_question, st.session_state.chat_history
                    )
                    st.session_state.chat_history.append((user_question, response_text))
                    st.rerun()
    else:
        st.info("Upload and process an image first to enable the conversational interface.")

# ----------------- TAB 4: ANALYTICS DASHBOARD -----------------
with tabs[3]:
    st.header("📊 Usage & Analysis Analytics")
    
    # Reload stats from SQLite
    
    stats = st.session_state.db.get_analytics()
    
    if stats["total_images"] > 0:
        # Row 1: Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">Total Images Processed</div>
                <div class="metric-val">{stats['total_images']}</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">Avg. Caption Confidence</div>
                <div class="metric-val">{stats['avg_caption_confidence']}%</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-header">Avg. Object Detection Confidence</div>
                <div class="metric-val">{stats['avg_detection_confidence']}%</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Row 2: Charts
        st.markdown("---")
        ch1, ch2 = st.columns(2)
        
        with ch1:
            st.subheader("Top 10 Detected Objects")
            if stats["top_objects"]:
                df_objects = pd.DataFrame(stats["top_objects"])
                fig_objects = px.bar(
                    df_objects, 
                    x="object", 
                    y="count",
                    title="Most Detected Object Classes",
                    labels={"object": "Object Class", "count": "Occurrences"},
                    color_discrete_sequence=["#38bdf8"]
                )
                fig_objects.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#f1f5f9"
                )
                st.plotly_chart(fig_objects, width="stretch")
            else:
                st.info("No object detection stats available.")
                
        with ch2:
            st.subheader("Scene Categories Distribution")
            if stats["scene_distribution"]:
                df_scenes = pd.DataFrame([
                    {"category": k, "count": v} for k, v in stats["scene_distribution"].items()
                ])
                fig_scenes = px.pie(
                    df_scenes,
                    values="count",
                    names="category",
                    title="Scene Type Distribution",
                    color_discrete_sequence=px.colors.sequential.Tealgrn
                )
                fig_scenes.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#f1f5f9"
                )
                st.plotly_chart(fig_scenes, width="stretch")
            else:
                st.info("No scene categorization stats available.")
                
        # Row 3: History Trend
        if stats["recent_activity"]:
            st.markdown("---")
            st.subheader("Processing History Over Time")
            df_trend = pd.DataFrame(stats["recent_activity"])
            fig_trend = px.line(
                df_trend,
                x="date",
                y="count",
                markers=True,
                title="Images Processed Daily (Last 7 Active Days)",
                labels={"date": "Date", "count": "Processed Count"},
                color_discrete_sequence=["#10b981"]
            )
            fig_trend.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f1f5f9"
            )
            st.plotly_chart(fig_trend, width="stretch")
    else:
        st.info("No records in database. Upload images to build analytics metrics.")

# ----------------- TAB 5: HISTORY EXPLORER -----------------
with tabs[4]:
    st.header("📜 Past Analyses History")
    st.markdown("Explore and revisit previous visual descriptions and detections.")
    
    if "history" not in st.session_state:
        

        history_records = st.session_state.db.get_history()
    
    if history_records:
        selected_record_title = st.selectbox(
            "Select past analysis record",
            options=[f"ID: {r['id']} | {r['filename']} | {r['timestamp'][:16]}" for r in history_records]
        )
        
        if selected_record_title:
            # Parse out ID
            selected_id = int(selected_record_title.split("|")[0].replace("ID: ", "").strip())
            
            # Fetch complete record from DB
            hist_rec, detections = st.session_state.db.get_record(selected_id)
            
            if hist_rec:
                hc1, hc2 = st.columns([1, 1])
                
                with hc1:
                    st.write("### Image Preview")
                    # Check original and annotated
                    hist_tabs = st.tabs(["Annotated (YOLO)", "Original Image"])
                    with hist_tabs[0]:
                        if os.path.exists(hist_rec["annotated_image_path"]):
                            st.image(hist_rec["annotated_image_path"], width="stretch")
                        else:
                            st.info("Annotated image file not found on disk.")
                    with hist_tabs[1]:
                        if os.path.exists(hist_rec["original_image_path"]):
                            st.image(hist_rec["original_image_path"], width="stretch")
                        else:
                            st.info("Original image file not found on disk.")
                            
                with hc2:
                    st.write("### Results Summary")
                    st.markdown(f"**Filename:** `{hist_rec['filename']}`")
                    st.markdown(f"**Timestamp:** `{hist_rec['timestamp']}`")
                    
                    st.info(f"**BLIP Caption:** \"{hist_rec['caption']}\"")
                    st.success(f"**Accessibility Alt-Text:** {hist_rec['accessibility_description']}")
                    st.warning(f"**AI Summary:** {hist_rec['summary']}")
                    
                    st.markdown("#### Detected Objects")
                    if detections:
                        st.dataframe(pd.DataFrame(detections)[["name", "confidence"]], width="stretch")
                    else:
                        st.write("No objects detected.")
                        
                # Set as active session state on click
                if st.button("📂 Load into Active Session", type="primary", width="stretch"):
                    st.session_state.active_analysis = {
                        "record": hist_rec,
                        "detections": detections
                    }
                    st.session_state.audio_path = None
                    st.session_state.chat_history = []
                    st.success(f"Loaded Record ID {selected_id} into active view! Switching tabs...")
                    st.rerun()
    else:
        st.info("No past analyses found. Start by uploading an image!")

# ----------------- TAB 6: DOWNLOAD CENTER -----------------
with tabs[5]:
    st.header("💾 Export and Download Center")
    st.markdown("Download reports, speech files, and annotated images of the active analysis.")
    
    if st.session_state.active_analysis:
        record = st.session_state.active_analysis["record"]
        detections = st.session_state.active_analysis["detections"]
        
        # Grid layout for downloads
        dc1, dc2 = st.columns(2)
        
        with dc1:
            st.subheader("📄 Text & PDF Reports")
            
            # Plain Text report
            txt_content = generate_txt_report(record, detections)
            st.download_button(
                label="📥 Download Plain Text Report (TXT)",
                data=txt_content,
                file_name=f"report_{os.path.splitext(record['filename'])[0]}.txt",
                mime="text/plain",
                width="stretch"
            )
            
            # PDF report
            pdf_filename = f"outputs/report_{os.path.splitext(record['filename'])[0]}.pdf"
            if st.button("Generate PDF Report"):


                pdf_filename = ...

                generate_pdf_report(...)

                st.success("PDF Generated!")
            if success_pdf and os.path.exists(pdf_filename):
                with open(pdf_filename, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    label="📥 Download Structured PDF Report (PDF)",
                    data=pdf_bytes,
                    file_name=os.path.basename(pdf_filename),
                    mime="application/pdf",
                    width="stretch"
                )
            else:
                st.error("Failed to generate PDF document.")
                
        with dc2:
            st.subheader("🖼️ Images & Audio Media")
            
            # Annotated image download
            if os.path.exists(record["annotated_image_path"]):
                with open(record["annotated_image_path"], "rb") as f:
                    img_bytes = f.read()
                st.download_button(
                    label="📥 Download Annotated Image (PNG)",
                    data=img_bytes,
                    file_name=os.path.basename(record["annotated_image_path"]),
                    mime="image/png",
                    width="stretch"
                )
            else:
                st.warning("Annotated image file is unavailable.")
                
            # Audio download
            if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
                with open(st.session_state.audio_path, "rb") as f:
                    audio_bytes = f.read()
                st.download_button(
                    label="📥 Download Audio Narration (MP3)",
                    data=audio_bytes,
                    file_name=os.path.basename(st.session_state.audio_path),
                    mime="audio/mp3",
                    width="stretch"
                )
            else:
                st.warning("Audio narration is not generated yet. Please generate it in 'Accessibility Mode'.")
    else:
        st.info("Upload and process an image to populate the Download Center.")
print(f"Startup Time : {time.time()-start:.2f} sec")