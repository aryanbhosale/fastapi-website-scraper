import re
import json
import google.generativeai as genai
from app.config import GEMINI_API_KEY

# Gemini API Configuration
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_homepage_content(text: str) -> dict:
    """
    Sends the homepage text to Gemini and asks for:
      1. The industry.
      2. The company size.
      3. The location.
    Returns a dictionary with these fields.
    """
    if not GEMINI_API_KEY:
        # Default response
        return {
            "industry": None,
            "company_size": None,
            "location": None
        }
    
    # Prompt engineering
    prompt = f"""
    Based on the following homepage text, please determine:
    1) The industry of the company.
    2) The company size if mentioned (small, medium, large, or a numeric detail).
    3) The location of the company if mentioned.

    Homepage text:
    \"{text}\"

    Return your answer in JSON format with the keys:
    "industry", "company_size", "location".
    """

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Remove MD fences for ```json...
    content = response.text.strip()
    content = re.sub(r'^```[a-zA-Z]*|```$', '', content, flags=re.MULTILINE).strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {
            "industry": None,
            "company_size": None,
            "location": None
        }

    return {
        "industry": data.get("industry"),
        "company_size": data.get("company_size"),
        "location": data.get("location"),
    }
