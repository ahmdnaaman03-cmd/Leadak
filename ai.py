import os
import requests
import json
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def get_working_model(api_key):
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        res = requests.get(list_url, timeout=15)
        if res.status_code == 200:
            for m in res.json().get('models', []):
                name = m.get('name', '')
                if 'gemini-1.5' in name.lower() and 'generateContent' in m.get('supportedGenerationMethods', []):
                    return name if name.startswith("models/") else f"models/{name}"
            # في حال لم يجد 1.5 يجلب أي نموذج gemini داعم
            for m in res.json().get('models', []):
                name = m.get('name', '')
                if 'gemini' in name.lower() and 'generateContent' in m.get('supportedGenerationMethods', []):
                    return name if name.startswith("models/") else f"models/{name}"
    except Exception as e:
        logging.error(f"خطأ في فحص النماذج: {e}")
    return "models/gemini-1.5-flash-latest" # قيمة افتراضية

def generate_email(name, industry, pain_point):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logging.error("❌ مفتاح API غير موجود!")
        return None
        
    model_name = get_working_model(api_key)
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
    prompt = f'اكتب رسالة B2B لـ {name} مجال {industry} يعاني من {pain_point}. أجب بـ JSON فقط: {{"subject":"العنوان", "body":"النص"}}'
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"response_mime_type": "application/json"}}
    
    try:
        res = requests.post(url, json=payload, timeout=30)
        if res.status_code == 200:
            return json.loads(res.json()['candidates'][0]['content']['parts'][0]['text'])
        else:
            logging.error(f"❌ خطأ من API: {res.text}")
            return None
    except Exception as e:
        logging.error(f"❌ فشل الاتصال: {e}")
        return None
