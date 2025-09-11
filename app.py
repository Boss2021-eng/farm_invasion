# import relevant libraries
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import gdown
import os

# Streamlit page outline
st.set_page_config(page_title="Farm Invasion Detector", layout="centered")

# To create the title
st.title("Farm Intrusion Detection App")

# to create the input box for uploading images
st.write("Upload an image to detect farm invaders (e.g., cows, goats, humans).")

# Sidebar for model selection
model_choice = st.sidebar.selectbox(
    "Select YOLO Model",
    ("yolov8n", "yolov8s", "yolov8m", "yolov12n", "yolov12s", "yolov12m")
)

# Map model names to Google Drive file IDs (replace with your real file IDs)
MODEL_URLS = {
    "yolov8n": "https://drive.google.com/file/d/18dW1ZJt467nsQzWvK6Um5GCs7UsBWzeH/view?usp=sharing",
    "yolov8s": "https://drive.google.com/file/d/13VFzffenaY7qBBk6SLIkebPs7LzrrZTO/view?usp=sharing",
    "yolov8m": "hhttps://drive.google.com/file/d/1bjU7hcaQrWSsrDOnFhJwD8vHjAp6a8jv/view?usp=sharing",
    "yolov12n": "https://drive.google.com/file/d/1af_aE2kMzhpLdck249xIn0p_qap_2HUb/view?usp=sharing",
    "yolov12s": "https://drive.google.com/file/d/1AO5t2zzZsWumIgHGNjs7WTuV3LjSkgr9/view?usp=sharing",
    "yolov12m": "https://drive.google.com/file/d/1ntbnqLCIN63yxm2T9g1k7HJi7QgmU5hA/view?usp=sharing",
}

# Cache model loading
@st.cache_resource
def load_model(model_name):
    url = MODEL_URLS[model_name]
    filename = f"{model_name}.pt"

    # Delete file if it exists but might be corrupted
    if os.path.exists(filename) and os.path.getsize(filename) < 1024 * 1024:  # <1MB likely corrupted
        os.remove(filename)

    # Download only if file is missing
    if not os.path.exists(filename):
        st.info(f"Downloading {model_name} weights...")
        gdown.download(url, filename, quiet=False)

    # Verify file exists after download
    if not os.path.exists(filename):
        st.error(f"Failed to download {filename}. Check your Google Drive link.")
        return None

    # Try loading YOLO model
    try:
        model = YOLO(filename)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Load the chosen model
model = load_model(model_choice)

# Upload image to the app, considering images like jpg, jpeg and png
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file and model:
    # Open and display original image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Run detection button
    if st.button("Run Detection"):
        with st.spinner("Detecting..."):
            results = model.predict(image, imgsz=640, conf=0.25)

            # Save annotated image
            annotated_image = results[0].plot()  # returns numpy array
            annotated_pil = Image.fromarray(annotated_image)

            # Display results side by side both the original and detected
            col1, col2 = st.columns(2)
            col1.image(image, caption="Original", use_column_width=True)
            col2.image(annotated_pil, caption="Detected", use_column_width=True)

            # show labels
            st.subheader("Detection Results")
            for box in results[0].boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                st.write(f"- {model.names[cls]} ({conf:.2f})")
