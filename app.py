import streamlit as st
from ultralytics import YOLO
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Farm Intrusion Detector", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ Control Panel")

    model_choice = st.selectbox(
        "🧠 Choose Detection Model",
        ("yolov8n", "yolov8s", "yolov8m")
    )

    st.divider()

    st.subheader("🎯 Detection Sensitivity")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25)
    st.caption("Lower = more detections | Higher = more certainty")

# ---------------- HEADER ----------------
st.title("🛡️ Smart Farm Intrusion Detector")
st.markdown(
    "Keep an eye on your farm in real-time. Detect **humans, animals, or intruders** "
    "crossing into restricted areas instantly."
)

# ---------------- MODEL ----------------
@st.cache_resource
def load_model(model_name):
    return YOLO(f"{model_name}.pt")

model = load_model(model_choice)

# ---------------- STATE ----------------
if "run" not in st.session_state:
    st.session_state.run = False

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📤 Upload an image to scan",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.divider()

    btn_col, data_col = st.columns([1, 3])

    # ---------------- BUTTON ----------------
    with btn_col:
        st.subheader("🚀 Action")
        if st.button("Run Detection"):
            st.session_state.run = True

    # ---------------- RESULTS ----------------
    with data_col:
        tab1, tab2 = st.tabs(["🖼️ Visual Results", "📊 Detection Details"])

        # BEFORE RUN
        if not st.session_state.run:
            with tab1:
                st.image(
                    image,
                    caption="👀 Your image is ready. Click 'Run Detection' to begin.",
                    use_container_width=True
                )

        # AFTER RUN
        if st.session_state.run:
            with st.spinner("🔍 Scanning the area for intrusions..."):
                results = model(image, imgsz=640, conf=conf_threshold)
                result = results[0]

                annotated = result.plot()
                annotated_image = Image.fromarray(annotated)

            # VISUAL TAB
            with tab1:
                c1, c2 = st.columns(2)

                c1.image(
                    image,
                    caption="📷 Original Image",
                    use_container_width=True
                )

                c2.image(
                    annotated_image,
                    caption="🧠 Detection Output",
                    use_container_width=True
                )

            # DATA TAB
            with tab2:
                st.subheader("📍 What was detected?")

                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        cls = int(box.cls.item())
                        conf = float(box.conf.item())

                        st.success(
                            f"✅ **{model.names[cls].upper()}** spotted "
                            f"with **{conf:.2%} confidence**"
                        )
                else:
                    st.warning("🚫 No intrusions detected. Your farm looks secure!")
