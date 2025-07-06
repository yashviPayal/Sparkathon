import streamlit as st
import os
import tempfile
import sys
import base64

# 🔁 Import your model logic
sys.path.append(os.path.abspath(".."))
from detect_review2 import predict_video, predict_image

# 🔧 Page setup
st.set_page_config(page_title="Product Review Validator", layout="wide")

# 🛍️ Product Info
col1, col2 = st.columns([1, 2])
with col1:
    st.image(
        "C:/Users/vasav/OneDrive/Desktop/walmart2025/streamlit/sample_product.jpg",
        caption="UltraSoft Cotton Hoodie",
        width=300  # Smaller image
    )
with col2:
    st.markdown("### 🏷️ Product Name")
    st.write("UltraSoft Cotton Hoodie")

    st.markdown("### 🗒️ Description")
    st.write("""
        This UltraSoft hoodie is made from 100% organic cotton. 
        Breathable, cozy, and perfect for any season. 
        Available in multiple sizes. Machine washable.
    """)

st.markdown("---")

# 📤 Upload Type Selector
media_type = st.radio("Select media type for review analysis:", ["Image", "Video"], horizontal=True)

# 🧠 Upload & Trigger Prediction Automatically
file_types = ["jpg", "jpeg", "png"] if media_type == "Image" else ["mp4", "mov", "avi"]
uploaded_file = st.file_uploader(f"Upload a {media_type.lower()} file", type=file_types)

# 🔍 Automatically predict once file is uploaded
if uploaded_file:
    # Save to temp file
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Show preview
    if media_type == "Image":
        st.image(file_path, caption="Uploaded Image", width=300)

    else:
        # 👇 Resize video using HTML
        video_bytes = open(file_path, "rb").read()
        encoded = base64.b64encode(video_bytes).decode()
        st.markdown(
            f"""
            <video width="300" controls>
                <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            """,
            unsafe_allow_html=True
        )

    # 🔍 Run prediction automatically
    with st.spinner("Analyzing with AI..."):
        if media_type == "Image":
            result = predict_image(file_path)
        else:
            result = predict_video(file_path)

    # 💬 Display result
    st.success("✅ Analysis complete!")
    st.markdown(f"### 🧠 **AI Verdict:** {result}")
    if "FAKE" in result.upper():
        st.error("⚠️ This review appears to be **FAKE**.")
    else:
        st.success("✅ This review appears to be **AUTHENTIC**.")

    # Cleanup
    try:
        os.remove(file_path)
        os.rmdir(temp_dir)
    except:
        pass
