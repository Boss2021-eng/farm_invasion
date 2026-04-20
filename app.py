import streamlit as st
from ultralytics import YOLO
from PIL import Image
import base64
from io import BytesIO

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AgriGuard · Farm Intrusion Detector",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --green-deep:   #1a3a2a;
    --green-mid:    #2e6b4a;
    --green-bright: #3d8c5f;
    --gold:         #c9a84c;
    --cream:        #f7f4ee;
    --dark:         #0f1f17;
    --glass:        rgba(255,255,255,0.08);
    --glass-border: rgba(255,255,255,0.15);
}

/* ── Full-page hero background (Unsplash farm field) ── */
[data-testid="stAppViewContainer"] {
    background-image:
        linear-gradient(160deg, rgba(15,31,23,0.82) 0%, rgba(26,58,42,0.72) 55%, rgba(15,31,23,0.88) 100%),
        url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1800&q=80&auto=format&fit=crop");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}

/* ── Sidebar glass card ── */
[data-testid="stSidebar"] {
    background: rgba(15, 31, 23, 0.85) !important;
    backdrop-filter: blur(18px);
    border-right: 1px solid var(--glass-border);
}
[data-testid="stSidebar"] * { color: #d8e8dd !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label { color: var(--gold) !important; font-family: 'DM Sans', sans-serif; font-size: 0.85rem; letter-spacing: 0.07em; text-transform: uppercase; }

/* ── Sidebar widget backgrounds ── */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stSlider { background: var(--glass); border-radius: 8px; }

/* ── Main content text defaults ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--cream);
}

/* ── Hero header ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    line-height: 1.15;
    margin-bottom: 0.2rem;
}
.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 300;
    color: rgba(215,230,220,0.85);
    max-width: 620px;
    line-height: 1.6;
    margin-bottom: 1.8rem;
}
.gold-rule {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, var(--gold), transparent);
    border-radius: 2px; margin: 0.6rem 0 1.2rem;
}

/* ── Stat pills ── */
.stat-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.8rem; }
.stat-pill {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(10px);
    border-radius: 50px;
    padding: 0.45rem 1.1rem;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--gold);
    display: flex; align-items: center; gap: 0.4rem;
}

/* ── Upload card ── */
.upload-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.5rem;
}
.upload-label {
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.6rem;
}

/* ── Streamlit uploader tweak ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px dashed rgba(201,168,76,0.45) !important;
    border-radius: 10px !important;
}

/* ── Detection button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--green-mid), var(--green-bright)) !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    height: 3.2em !important;
    box-shadow: 0 4px 20px rgba(61,140,95,0.35) !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #245c3c, var(--green-mid)) !important;
    box-shadow: 0 6px 28px rgba(61,140,95,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Result panels ── */
.result-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
}

/* ── Tab styling ── */
[data-baseweb="tab-list"] { background: var(--glass) !important; border-radius: 10px !important; padding: 4px !important; }
[data-baseweb="tab"] { color: rgba(215,230,220,0.7) !important; font-family: 'DM Sans', sans-serif !important; border-radius: 8px !important; }
[aria-selected="true"][data-baseweb="tab"] { background: var(--green-mid) !important; color: #fff !important; }

/* ── Detection alert cards ── */
.detect-card {
    display: flex; align-items: center; gap: 0.9rem;
    background: rgba(46,107,74,0.25);
    border: 1px solid rgba(61,140,95,0.4);
    border-left: 4px solid var(--green-bright);
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.7rem;
    font-family: 'DM Sans', sans-serif;
}
.detect-icon { font-size: 1.4rem; }
.detect-label { font-weight: 600; font-size: 0.95rem; color: #fff; }
.detect-conf { font-size: 0.8rem; color: rgba(215,230,220,0.7); margin-top: 2px; }

.clear-card {
    background: rgba(201,168,76,0.12);
    border: 1px solid rgba(201,168,76,0.35);
    border-left: 4px solid var(--gold);
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    font-family: 'DM Sans', sans-serif;
    color: var(--gold);
}

/* ── Sidebar brand block ── */
.sidebar-brand {
    padding: 0.3rem 0 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 1.2rem;
}
.brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem; font-weight: 700;
    color: #ffffff !important;
    letter-spacing: -0.3px;
}
.brand-tag {
    font-size: 0.72rem; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--gold) !important;
    margin-top: 2px;
}

/* ── Spinner text ── */
.stSpinner > div { color: var(--gold) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-name">🌿 AgriGuard</div>
        <div class="brand-tag">Intelligent Farm Security</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 🧠 Detection Model")
    model_choice = st.selectbox(
        "Model",
        ("yolov8n", "yolov8s", "yolov8m"),
        format_func=lambda x: {
            "yolov8n": "YOLOv8 Nano  — Fastest",
            "yolov8s": "YOLOv8 Small — Balanced",
            "yolov8m": "YOLOv8 Medium — Most Accurate",
        }[x],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown("##### 🎯 Confidence Threshold")
    conf_threshold = st.slider(
        "Threshold", 0.0, 1.0, 0.25, step=0.01,
        label_visibility="collapsed",
        help="Lower = more detections · Higher = higher certainty",
    )
    st.caption(f"Current threshold: **{conf_threshold:.0%}**")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem; color:rgba(215,230,220,0.5); line-height:1.7;">
        AgriGuard uses real-time object detection to identify humans, animals,
        and vehicles on your farmland. Powered by YOLOv8.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-title">Farm Intrusion<br>Detection System</div>
<div class="gold-rule"></div>
<div class="hero-subtitle">
    AI-powered perimeter monitoring for your farmland. Upload an image and AgriGuard
    will instantly identify humans, livestock, vehicles, or any unexpected activity —
    keeping your land safe around the clock.
</div>
<div class="stat-row">
    <div class="stat-pill">⚡ Real-time Analysis</div>
    <div class="stat-pill">🎯 Multi-class Detection</div>
    <div class="stat-pill">🔒 Offline Processing</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MODEL LOADER
# ─────────────────────────────────────────────
@st.cache_resource
def load_model(model_name: str) -> YOLO:
    return YOLO(f"{model_name}.pt")

model = load_model(model_choice)


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "run" not in st.session_state:
    st.session_state.run = False


# ─────────────────────────────────────────────
#  IMAGE UPLOAD
# ─────────────────────────────────────────────
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<div class="upload-label">📤 Upload a Farm Image to Inspect</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drag & drop or browse — JPG / JPEG / PNG",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)
st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN PANEL
# ─────────────────────────────────────────────
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.markdown("---")
    btn_col, spacer, result_col = st.columns([1, 0.05, 3])

    # ── Action panel ──────────────────────────
    with btn_col:
        st.markdown("#### Run Analysis")
        st.caption(
            f"Model: **{model_choice.upper()}** · "
            f"Confidence: **{conf_threshold:.0%}**"
        )
        if st.button("🔍 Detect Intrusions"):
            st.session_state.run = True
        st.markdown("&nbsp;")
        st.info(
            "Upload an image, configure the model in the sidebar, "
            "then click **Detect Intrusions** to begin scanning.",
            icon="ℹ️",
        )

    # ── Results panel ─────────────────────────
    with result_col:
        tab_visual, tab_data = st.tabs(["🖼️  Visual Results", "📊  Detection Report"])

        # — Before scan —
        if not st.session_state.run:
            with tab_visual:
                st.image(
                    image,
                    caption="Uploaded image — awaiting scan",
                    use_container_width=True,
                )

        # — After scan —
        if st.session_state.run:
            with st.spinner("🔍 Scanning for intrusions…"):
                results = model(image, imgsz=640, conf=conf_threshold)
                result  = results[0]
                annotated_image = Image.fromarray(result.plot())

            # Visual tab
            with tab_visual:
                c1, c2 = st.columns(2)
                c1.image(image, caption="📷 Original", use_container_width=True)
                c2.image(annotated_image, caption="🧠 AI Analysis", use_container_width=True)

            # Data tab
            with tab_data:
                st.markdown("#### 📍 Detection Report")

                boxes = result.boxes
                if boxes is not None and len(boxes) > 0:
                    # Summary metric row
                    unique_classes = set(int(b.cls.item()) for b in boxes)
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Detections", len(boxes))
                    m2.metric("Unique Object Types", len(unique_classes))
                    m3.metric(
                        "Highest Confidence",
                        f"{max(float(b.conf.item()) for b in boxes):.0%}",
                    )

                    st.markdown("---")
                    st.markdown("**Detected Objects**")

                    for box in boxes:
                        cls   = int(box.cls.item())
                        conf  = float(box.conf.item())
                        label = model.names[cls].replace("_", " ").title()
                        bar   = "█" * int(conf * 10) + "░" * (10 - int(conf * 10))
                        st.markdown(f"""
                        <div class="detect-card">
                            <div class="detect-icon">🔴</div>
                            <div>
                                <div class="detect-label">{label}</div>
                                <div class="detect-conf">{bar} &nbsp; {conf:.1%} confidence</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Export annotated image
                    buf = BytesIO()
                    annotated_image.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️  Download Annotated Image",
                        data=buf.getvalue(),
                        file_name="agriguard_detection.png",
                        mime="image/png",
                        use_container_width=True,
                    )

                else:
                    st.markdown("""
                    <div class="clear-card">
                        ✅ &nbsp;<strong>All Clear</strong> — No intrusions detected.
                        Your farm perimeter appears secure.
                    </div>
                    """, unsafe_allow_html=True)
