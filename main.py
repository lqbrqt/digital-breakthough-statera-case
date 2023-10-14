import streamlit as st
import os
from PIL import Image


image_file = st.file_uploader("Upload An Image",type=['png','jpeg','jpg'])
if image_file is not None:
    file_details = {"FileName":image_file.name,"FileType":image_file.type}
    st.write(file_details)
    img = Image.open(image_file)
    st.image(img)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"tempDir",image_file.name),"wb") as f: 
      f.write(image_file.getbuffer())         
    st.success("Saved File")

    # отправить запрос 
    # дождаться ответа
    
    img = Image.open(image_file) # полученный файл
    st.image(img)

    st.write('плейсхолдер для числа')
    st.write('плейсхолдер для json')
    