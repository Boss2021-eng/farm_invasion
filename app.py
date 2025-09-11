import streamlit as st
from ultralytics import YOLO
from PIL import Image
import io

# Streamlit page outline
st.set_page_config(page_title="Farm Invasion Detector", layout="centered")

st.title("Farm Intrusion Detection App")
st.write("Upload an image to detect farm invaders (e.g., cows, goats, humans).")

# Sidebar for model selection
model_choice = st.sidebar.selectbox(
    "Select YOLO Model",
    ("yolov8n","yolov8s", "yolov12n")
)

# Cache model loading for faster switching
@st.cache_resource
def load_model(model_name):
    return YOLO(f"{model_name}.pt")

model = load_model(model_choice)

# Upload image to the app, considering images like jpg, jpeg and png
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
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


