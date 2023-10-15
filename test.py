import requests

files = {'file': open('/home/dobryydenechek/Magica/HacksAI/frame0-00-04.50.jpg', 'rb')}
r = requests.post('http://127.0.0.1:8000/img/',files=files)
print(r.content)

