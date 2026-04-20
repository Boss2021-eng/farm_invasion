import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io

# To design the page
st.set_page_config(page_title="Farm Invasion Detector", layout="wide")

# Custom CSS to make the interface feel modern
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2e7d32; color: white; }
    </style>
    """, unsafe_allow_value=True)

# SIDEBAR (Inputs & Controls)
with st.sidebar:
    st.title("🚜 App Settings")
    model_choice = st.selectbox("Model Version", ("yolov8n", "yolov8s", "yolov12n"))
    
    st.divider()
    
    st.subheader("Detection Parameters")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25)
    st.info("Adjust threshold: Higher values show only high-certainty detections.")

#  HEADER
st.title("🛡️ Farm Intrusion Detection")
st.write("Real-time identification of unauthorized livestock or humans within farm perimeters.")

# 4. MODEL LOADING 
@st.cache_resource
def load_model(model_name):
    return YOLO(f"{model_name}.pt")

model = load_model(model_choice)

# 5. MAIN INTERFACE (Three distinct sections)
upload_container = st.container()
results_container = st.container()

with upload_container:
    uploaded_file = st.file_uploader("Drop an image here", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    
    with results_container:
        st.divider()
        # Use columns to separate the Action button from the Results
        btn_col, data_col = st.columns([1, 3])
        
        with btn_col:
            st.subheader("Process")
            run_btn = st.button("🔍 Run Analysis")
            
        with data_col:
            # Using Tabs to keep the UI clean
            tab1, tab2 = st.tabs(["🖼️ Visual Analysis", "📊 Data Logs"])
            
            if run_btn:
                with st.spinner("Analyzing perimeter..."):
                    results = model.predict(image, imgsz=640, conf=conf_threshold)
                    
                    # Annotate
                    annotated_image = results[0].plot()
                    annotated_pil = Image.fromarray(annotated_image)
                    
                    with tab1:
                        # Side-by-side comparison
                        c1, c2 = st.columns(2)
                        c1.image(image, caption="Original View", use_container_width=True)
                        c2.image(annotated_pil, caption="Detection Result", use_container_width=True)
                    
                    with tab2:
                        st.subheader("Object Log")
                        if len(results[0].boxes) > 0:
                            # Displaying results as a clean list
                            for box in results[0].boxes:
                                cls = int(box.cls[0])
                                conf = float(box.conf[0])
                                st.success(f"**Detected:** {model.names[cls].upper()} | **Confidence:** {conf:.2%}")
                        else:
                            st.warning("No intruders detected in the frame.")
            else:
                with tab1:
                    st.image(image, caption="Waiting for Analysis...", width=400)
