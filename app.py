import streamlit as st
from ultralytics import YOLO
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Farm Invasion Detector", layout="wide")

# ---------------- CUSTOM UI ----------------
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        height: 3em;
        background-color: #2e7d32;
        color: white;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🚜 App Settings")

    # Removed invalid model
    model_choice = st.selectbox(
        "Model Version",
        ("yolov8n", "yolov8s", "yolov8m")
    )

    st.divider()

    st.subheader("Detection Parameters")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25)
    st.caption("Higher values = fewer, more confident detections")

# ---------------- HEADER ----------------
st.title("🛡️ Farm Intrusion Detection")
st.write("Detect humans or livestock entering restricted farm zones.")

# ---------------- MODEL LOADING ----------------
@st.cache_resource
def load_model(model_name):
    return YOLO(f"{model_name}.pt")

model = load_model(model_choice)

# ---------------- SESSION STATE ----------------
if "run" not in st.session_state:
    st.session_state.run = False

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.divider()

    btn_col, data_col = st.columns([1, 3])

    with btn_col:
        st.subheader("Process")
        if st.button("🔍 Run Analysis"):
            st.session_state.run = True

    with data_col:
        tab1, tab2 = st.tabs(["🖼️ Visual Analysis", "📊 Data Logs"])

        # ---------------- BEFORE RUN ----------------
        if not st.session_state.run:
            with tab1:
                st.image(image, caption="Waiting for analysis...", use_container_width=True)

        # ---------------- RUN MODEL ----------------
        if st.session_state.run:
            with st.spinner("Analyzing perimeter..."):
                results = model(image, imgsz=640, conf=conf_threshold)

                result = results[0]

                # Safe annotation
                annotated = result.plot()
                annotated_image = Image.fromarray(annotated)

            # ---------------- TAB 1 ----------------
            with tab1:
                c1, c2 = st.columns(2)
                c1.image(image, caption="Original", use_container_width=True)
                c2.image(annotated_image, caption="Detected Objects", use_container_width=True)

            # ---------------- TAB 2 ----------------
            with tab2:
                st.subheader("Detection Log")

                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        cls = int(box.cls.item())
                        conf = float(box.conf.item())

                        st.success(
                            f"Detected: **{model.names[cls].upper()}** | Confidence: **{conf:.2%}**"
                        )
                else:
                    st.warning("No intruders detected.")
