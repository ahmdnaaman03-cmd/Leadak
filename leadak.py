import os
import json
import requests

API_KEY = os.getenv("GEMINI_API_KEY")

def get_working_model():
    if not API_KEY:
        return "models/gemma-2-2b-it"
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    try:
        res = requests.get(list_url, timeout=15)
        if res.status_code == 200:
            models = res.json().get('models', [])
            for m in models:
                name = m.get('name', '')
                if 'gemma' in name.lower() and 'generateContent' in m.get('supportedGenerationMethods', []):
                    return name if name.startswith("models/") else f"models/{name}"
            for m in models:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    name = m.get('name', '')
                    return name if name.startswith("models/") else f"models/{name}"
    except Exception:
        pass
    return "models/gemma-2-2b-it"

def main():
    print("=" * 30)
    print("       LEADAK - GEMMA")
    print("=" * 30)
    
    if not API_KEY:
        print("\n[خطأ]: مفتاح البيئة غير موجود.")
        return

    company_name = input("\nاسم الشركة: ").strip()
    if not company_name:
        return

    industry = input("المجال: ").strip()
    if not industry:
        return

    recent_post = input("نقطة الألم (اختياري): ").strip()

    print("\n[جاري فحص النماذج والاتصال...]")
    MODEL_NAME = get_working_model()

    url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={API_KEY}"
    prompt = f"للعميل B2B اكتب رسالة احترافية للشركة {company_name} تعاني من {recent_post} في مجال {industry}."
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        res = requests.post(url, json=payload, timeout=45)
        if res.status_code == 200:
            ans = res.json()['candidates'][0]['content']['parts'][0]['text']
            clean = ans.replace("```json", "").replace("```", "").strip()
            
            try:
                data = json.loads(clean)
                msg = data.get("message", clean)
            except:
                msg = clean  # عرض النص مباشرة إذا لم يكن JSON

            print("\n" + "=" * 30)
            print(msg)
            print("=" * 30)
        else:
            print(f"\n[خطأ]: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"\n[خطأ في الاتصال]: {str(e)}")

if __name__ == "__main__":
    main()
