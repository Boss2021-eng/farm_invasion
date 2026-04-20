# 🛡️ Smart Farm Intrusion Detection System  
### *Smart Farm Perimeter Monitoring for Modern Agriculture*
🌐 [Live App – Farm Intrusion Detector](https://farmintrusion-5isujh7x227c6fjbop8emh.streamlit.app/)
---

## 🌾 Overview

The **Smart Farm Intrusion Detection System** is an AI-driven web application designed to monitor farm environments and detect unauthorized intrusions from **humans or animals** in real time.

Built using **YOLO (You Only Look Once)** object detection and deployed with **Streamlit**, this system transforms static images into actionable insights; helping farmers protect crops, livestock, and property.

---

## 🚀 Key Features
<p align="center">
   <img width="1364" height="634" alt="image" src="https://github.com/user-attachments/assets/bf801df2-c4b6-42ce-a4b2-f471386fa368" />
</p>

✨ **Object Detection**  
Detects humans, livestock, and other objects within farm boundaries using state-of-the-art deep learning models.

🎯 **Adjustable Sensitivity**  
Control detection strictness using a confidence threshold slider.

🖼️ **Visual Intelligence**  
Side-by-side comparison of original vs annotated images for clear interpretation.

📊 **Detection Logs**  
Detailed breakdown of detected objects with confidence scores.

🎨 **Immersive UI Design**  
Farm-themed interface with a security-focused visual experience.

⚡ **Optimized Performance**  
Uses lightweight YOLOv8 models for fast and efficient inference.

---

## 🧠 How It Works

The system follows a simple but powerful pipeline:

### 1️⃣ Image Input
Users upload an image of their farm or surveillance frame via the interface.


### 2️⃣ Model Selection
Choose between different YOLO model variants:
- `yolov8n` → Fastest, lightweight
- `yolov8s` → Balanced performance
- `yolov8m` → Higher accuracy

### 3️⃣ Detection Processing
The model analyzes the image and:
- Identifies objects  
- Draws bounding boxes  
- Assigns confidence scores  

### 4️⃣ Output Generation
Two types of results are produced:
- **Visual Output** → Annotated image with detected objects  
- **Text Output** → Structured detection logs  

---

## 🖼️ Output Example

### 🔍 Visual Analysis
- Original image (raw input)  
- Annotated image (images with detected animals)  

Each detected object is highlighted with:
- Bounding boxes  
- Class labels (e.g., *person, cow, goat*)  
- Confidence scores  

---

### 📊 Detection Logs

Example output:
<p align="center">
  <img width="705" height="356" alt="image" src="https://github.com/user-attachments/assets/50298775-50ed-4122-885f-0e075df79a60" />
</p>

<p align="center">
  <img width="697" height="277" alt="image" src="https://github.com/user-attachments/assets/a944c4fb-e7d1-4204-8772-36ff89646f70" />
</p>
<p align="center">
  <img width="706" height="149" alt="image" src="https://github.com/user-attachments/assets/991fb40a-a147-4044-827d-31a475c30a6b" />
</p>


---

## 🧩 Tech Stack
<p align="center">

   | Component        | Technology Used          |
   |-----------------|--------------------------|
  | Frontend UI      | Streamlit                |
  |  Model           | YOLOv8 and 12 (Ultralytics)     |
  | Image Handling   | PIL (Python Imaging)     |
  | Backend Logic    | Python                   |
</p>


---

## 🎮 How to Use
- Upload an image of your farm 📤
- Select your preferred model 🧠
- Adjust detection sensitivity 🎯
- Click Run Detection 🚀
- View results in:
🖼️ Visual Results tab
📊 Detection Details tab

---
## 🌍 Real-World Applications
- Farm security & surveillance
- Wildlife intrusion monitoring
- Smart agriculture systems
- Rural property protection
