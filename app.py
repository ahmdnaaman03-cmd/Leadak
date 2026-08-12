import os
import requests
import streamlit as st

st.set_page_config(page_title="LeadAK", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .brand-title { font-size: 24px; font-weight: 600; color: #0F4C81; letter-spacing: -0.5px; margin-bottom: 2rem; border-bottom: 1px solid #E2E8F0; padding-bottom: 15px; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #FFFFFF !important; color: #0F4C81 !important; border: 1px solid #CBD5E1 !important; border-radius: 6px !important; padding: 10px !important; }
    .stSelectbox>div>div>div { background-color: #FFFFFF !important; color: #0F4C81 !important; border: 1px solid #CBD5E1 !important; border-radius: 6px !important; }
    .stButton>button { width: 100%; background-color: #0F4C81; color: #FFFFFF; font-weight: 500; border-radius: 6px; height: 3.2em; border: none; transition: 0.2s; }
    .stButton>button:hover { background-color: #1A5F7A; color: #FFFFFF; }
    div[data-testid="stExpander"] { background-color: transparent; border: none; box-shadow: none; }
    .footer-copyright { text-align: center; color: #94A3B8; font-size: 12px; margin-top: 3rem; border-top: 1px solid #E2E8F0; padding-top: 15px; letter-spacing: 0.5px; }
    </style>
""", unsafe_allow_html=True)

lang = st.radio("Language", ["English", "العربية"], horizontal=True, label_visibility="collapsed")

if lang == "العربية":
    T = {"title": "LeadAK", "target": "الجهة المستهدفة", "target_ph": "مثال: د. أحمد - مدير استثمار", "ind": "مجال العمل", "ind_ph": "مثال: التطوير العقاري", "post": "السياق أو الأنشطة الأخيرة", "post_ph": "أعلنوا عن التوسع في مشاريع جديدة...", "adv": "خيارات متقدمة", "tone": "نبرة الرسالة", "tones": ["احترافي ومباشر", "ودود", "رسمي"], "platform": "القناة", "platforms": ["LinkedIn InMail", "Email", "WhatsApp"], "btn": "إنشاء الرسالة", "err": "يرجى إدخال البيانات المطلوبة وتأكد من المفتاح.", "wait": "جاري فحص النماذج المتاحة والتوليد...", "res": "النتيجة النهائية:", "footer": "© 2026 LeadAK. All rights reserved."}
else:
    T = {"title": "LeadAK", "target": "Target Name", "target_ph": "e.g., Dr. Ahmed - CEO", "ind": "Industry", "ind_ph": "e.g., Real Estate", "post": "Context / Recent Activity", "post_ph": "They recently announced...", "adv": "Advanced Options", "tone": "Tone", "tones": ["Professional", "Friendly", "Formal"], "platform": "Channel", "platforms": ["LinkedIn InMail", "Email", "WhatsApp"], "btn": "Generate Message", "err": "Please check input fields and API key.", "wait": "Checking available models & generating...", "res": "Generated Message:", "footer": "© 2026 LeadAK. All rights reserved."}

API_KEY = os.getenv("GEMINI_API_KEY")

st.markdown(f"<div class='brand-title'>{T['title']}</div>", unsafe_allow_html=True)

target_name = st.text_input(T["target"], placeholder=T["target_ph"])
industry = st.text_input(T["ind"], placeholder=T["ind_ph"])
post_content = st.text_area(T["post"], placeholder=T["post_ph"], height=90)

with st.expander(T["adv"]):
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(T["tone"], T["tones"])
    with col2:
        platform = st.selectbox(T["platform"], T["platforms"])

def get_working_model(api_key):
    try:
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        res = requests.get(list_url, timeout=10)
        if res.status_code == 200:
            models = res.json().get("models", [])
            for m in models:
                name = m.get("name", "")
                methods = m.get("supportedGenerationMethods", [])
                if "generateContent" in methods and "flash" in name:
                    return name.replace("models/", "")
            for m in models:
                name = m.get("name", "")
                methods = m.get("supportedGenerationMethods", [])
                if "generateContent" in methods:
                    return name.replace("models/", "")
    except Exception:
        pass
    return "gemini-1.5-flash"

if st.button(T["btn"]):
    if not API_KEY or not target_name or not post_content:
        st.error(T["err"])
    else:
        with st.spinner(T["wait"]):
            model_name = get_working_model(API_KEY)
            output_lang = "Arabic" if lang == "العربية" else "English"
            prompt = f'''You are a senior B2B Sales Specialist. Write a highly personalized, concise outreach message. Target: {target_name}. Industry: {industry}. Context/Activity: {post_content}. Tone: {tone}. Channel: {platform}. Language: {output_lang}. Rules: No emojis. Keep it highly professional, clean, and minimalist. Mention their context naturally. End with a simple CTA. Provide ONLY the message text.'''
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            try:
                res = requests.post(url, json=payload, timeout=45)
                if res.status_code == 200:
                    ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.text_area(T["res"], value=ans, height=180)
                else:
                    st.error(f"Error connecting to model {model_name}. Code: {res.status_code}")
            except Exception:
                st.error("Connection failed.")

st.markdown(f"<div class='footer-copyright'>{T['footer']}</div>", unsafe_allow_html=True)
