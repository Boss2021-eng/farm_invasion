import streamlit as st
from ultralytics import YOLO
from PIL import Image
import base64
from io import BytesIO

st.write("OpenCV version:", cv2.__version__)
