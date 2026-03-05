import urllib.request
import os

os.makedirs('static/images', exist_ok=True)
url = 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80&w=800&h=600'
urllib.request.urlretrieve(url, 'static/images/fastapi_thumbnail.png')
print("Image downloaded successfully!")
