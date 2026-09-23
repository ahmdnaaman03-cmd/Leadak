import os
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def generate_email(name, industry, pain_point):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    prompt = f'اكتب رسالة B2B لـ {name} مجال {industry} يعاني من {pain_point}. أجب بـ JSON: {{"subject":"العنوان", "body":"النص"}}'
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json"}}
    try:
        res = requests.post(url, json=payload, timeout=30)
        return json.loads(res.json()['candidates'][0]['content']['parts'][0]['text']) if res.status_code == 200 else None
    except: return None
