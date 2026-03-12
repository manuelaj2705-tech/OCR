import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

st.set_page_config(page_title="OCR Scanner", page_icon="📷", layout="wide")

st.title("Detecta Texto con tu Cámara (OCR) 📸🔎")

st.write("""
Captura una imagen y permite que el sistema identifique automáticamente el texto que aparece en ella. 
Gracias al reconocimiento óptico de caracteres (OCR), podrás convertir palabras impresas o escritas 
en texto digital de forma rápida y sencilla. Solo toma una foto y el sistema se encargará del resto.
""")

img_file_buffer = st.camera_input("📸 Toma una foto")

with st.sidebar:
    st.header("Deseas aplicar")
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

if img_file_buffer is not None:

    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    st.image(img_rgb, caption="Imagen capturada", use_column_width=True)

    gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh)

    st.subheader("📝 Texto Detectado")
    st.text_area("Resultado OCR", text, height=200)

    st.download_button("Descargar texto", text, file_name="texto_detectado.txt")

    


