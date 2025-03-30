import cv2
import streamlit as st
import numpy as np
from PIL import Image

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Check if model loaded correctly
if face_cascade.empty():
    st.error("Error loading face detection model. Check OpenCV installation.")

# Streamlit App Title
st.title("🔍 Face Detection App")

# Instructions for users
st.markdown("""
### How to Use This App:
1. **Upload an image** to detect faces.
2. **Adjust detection parameters** (`scaleFactor` & `minNeighbors`) for better accuracy.
3. **Choose a rectangle color** for detected faces.
4. **Click 'Detect Faces'** to process the image.
5. **Save the result** if you wish.
""")

# File uploader for user to upload an image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

# Color picker for rectangle color
rect_color = st.color_picker("Choose Rectangle Color", "#FF0000")  # Default is red

# Convert hex color to BGR
def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip("#")
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb[::-1]  # Convert RGB to BGR

bgr_color = hex_to_bgr(rect_color)

# Sliders for adjusting face detection parameters
scaleFactor = st.slider("Scale Factor", min_value=1.1, max_value=2.0, value=1.3, step=0.1)
minNeighbors = st.slider("Min Neighbors", min_value=1, max_value=10, value=5, step=1)

# Process image if uploaded
if uploaded_file:
    # Convert file to OpenCV image
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    # Fix transparency issue for PNGs
    if image_np.shape[-1] == 4:  # If image has an alpha channel (RGBA)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)

    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image_np, (x, y), (x+w, y+h), bgr_color, 2)

    # Display detected faces (Fix color conversion)
    st.image(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB), caption="Detected Faces", use_column_width=True)

    # Save the processed image
    if st.button("Save Image"):
        save_path = "detected_faces.jpg"
        cv2.imwrite(save_path, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))  # Convert RGB to BGR before saving
        st.success(f"Image saved as {save_path}")
