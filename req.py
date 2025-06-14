import requests

url = "http://localhost:8000/predict/"
file_path = "9.jpeg"

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

# Сохраняем полученное изображение
with open("result.jpg", "wb") as f:
    f.write(response.content)