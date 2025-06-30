import streamlit as st
from PIL import Image
from ultralytics import YOLO
import tempfile
import time
from datetime import datetime

st.set_page_config(page_title="Klasifikasi Plat Nomor YOLO", layout="centered", page_icon=":car:")
@st.cache_resource
def load_model():
    model = YOLO("./model/best.pt")  
    return model

model = load_model()

def classify_plate_yolo(image):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        image.save(tmp_file.name)
        results = model(tmp_file.name)

    names = model.names
    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0:
        box = boxes[0]
        class_id = int(box.cls[0])
        conf = float(box.conf[0])
        label = names[class_id]

        result_img = results[0].plot() 
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_path = f"results/detected_{timestamp}.jpg"
        Image.fromarray(result_img).save(result_path) 
        return label, conf, result_img
    else:
        return None, None, None

st.title("🚘 Klasifikasi Plat Nomor Kendaraan")
st.markdown("Upload gambar plat nomor kendaraan dan klik tombol klasifikasi untuk melihat hasil deteksi.")

uploaded_file = st.file_uploader("📤 Upload Gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang di-upload", use_column_width=True)

    if st.button("🔍 Klasifikasi"):
        with st.spinner("Sedang mengklasifikasikan..."):
            label, confidence, result_img = classify_plate_yolo(image)
            time.sleep(1)

        if label:
            st.success("✅ Plat Nomor Terdeteksi!")
            st.image(result_img, caption=f"Hasil Deteksi: {label} ({confidence*100:.2f}%)", use_column_width=True)

            st.markdown(f"**Label:** `{label}`")
            st.markdown(f"**Confidence:** `{confidence*100:.2f}%`")
        else:
            st.warning("⚠️ Tidak ada plat nomor terdeteksi.")

else:
    st.info("Silakan upload gambar terlebih dahulu.")
