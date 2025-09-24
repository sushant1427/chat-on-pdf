import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("⚠️ GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=api_key)

def get_gemini_response(prompt: str) -> str:
    """Get response from Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        return model.generate_content(prompt).text
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}")
