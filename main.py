import streamlit as st
import os
from PIL import Image
import requests
import json


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
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"tempDir",image_file.name),'rb') as filedata: 
      res = requests.post("http://127.0.0.1:8000/img/?save_img=True",files = {'file':filedata}).text 
    # дождаться ответа
    a = json.loads(res)

    
    res_img = requests.get('http://127.0.0.1:8000/get_res_img/'+a["image"])
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"tempDir","img.jpg"), "wb")
    out.write(res_img.content)
    out.close()
    

    img = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"tempDir","img.jpg")) # полученный файл
    st.image(img)

    st.write('JSON:')
    st.write(str(a))
    