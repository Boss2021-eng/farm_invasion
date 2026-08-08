import streamlit as st

st.title("YOLO Environment Test")

import cv2
st.success(f"OpenCV works: {cv2.__version__}")

from ultralytics import YOLO
st.success("Ultralytics YOLO works")

import torch
st.success(f"PyTorch works: {torch.__version__}")
