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
      res = requests.post(" http://127.0.0.1:8000/img/",files = {'file':filedata}) 
    # дождаться ответа
    res = json.loads(res)
    st.write(type(res["image"]))

    res_img = requests.get('http://127.0.0.1:8000/get_res_img/'+res["image"]+'.jpg')
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"tempDir","img.jpg"), "wb")
    out.write(res_img["image"])
    out.close()
    

    img = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"tempDir","img.jpg")) # полученный файл
    st.image(img)

    st.write(str(res))
    st.write('плейсхолдер для json')
    