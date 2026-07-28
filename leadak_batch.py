import requests
import json
import os

API_KEY = os.getenv("GEMINI_API_KEY")

def get_working_model():
    if not API_KEY:
        print("❌ خطأ: متغير البيئة GEMINI_API_KEY غير موجود.")
        return None
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    try:
        res = requests.get(list_url)
        if res.status_code == 200:
            for m in res.json().get('models', []):
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    model_name = m['name']
                    test_url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={API_KEY}"
                    test_res = requests.post(test_url, headers={'Content-Type': 'application/json'}, data=json.dumps({"contents": [{"parts": [{"text": "مرحبا"}]}]}))
                    if test_res.status_code == 200:
                        return model_name
    except Exception:
        pass
    return None

def process_batch():
    MODEL_NAME = get_working_model()
    if not MODEL_NAME:
        return
    URL = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={API_KEY}"
    
    if not os.path.exists("leads_input.txt"):
        return

    with open("leads_input.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if "|" in line:
            parts = line.strip().split("|")
            name, ind, post = parts[0].strip(), parts[1].strip(), parts[2].strip()
            prompt = f'اكتب رسالة B2B للعميل {name} في مجال {ind} يعاني من: {post}. أجب بـ JSON فقط بهذه الصيغة: {{"message": "النص"}}'
            res = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}))
            if res.status_code == 200:
                try:
                    ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                    clean_ans = ans.replace("```json", "").replace("```", "").strip()
                    print(json.loads(clean_ans).get("message", clean_ans))
                except:
                    print(ans)

if __name__ == "__main__":
    process_batch()
