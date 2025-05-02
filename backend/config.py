import os

class Config:
    API_KEY = os.getenv("API_KEY")
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_ORIGINS = ["https://devdoc-ai-frontend.onrender.com", "http://localhost:3000"]
