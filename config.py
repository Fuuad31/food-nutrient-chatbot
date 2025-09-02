# config.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from exa_py import Exa

# Muat environment variables dari file .env
load_dotenv()

# Ambil API keys dari environment
GOOGLE_API_KEY = "AIzaSyBJq6or5XLV863Bs_Ff6bk1J1Oonv5iWAI"
print(f"DEBUG: KEY IS {GOOGLE_API_KEY}")
EXA_API_KEY = os.getenv("EXA_API_KEY")

# Inisialisasi klien LLM dan Exa di satu tempat
# Ini adalah "singleton" instances yang akan kita impor di file lain
# config.py
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY,
    max_output_tokens=512  # <-- ADD THIS LINE
)
exa_client = Exa(api_key=EXA_API_KEY)