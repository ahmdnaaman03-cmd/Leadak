import os
import requests
import streamlit as st

st.set_page_config(page_title="LeadAK", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .brand-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 15px; margin-bottom: 2rem; }
    .brand-logo { font-size: 24px; font-weight: 700; color: #1E1B4B; letter-spacing: -0.5px; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #FFFFFF !important; color: #1E1B4B !important; border: 1px solid #CBD5E1 !important; border-radius: 8px !important; padding: 10px !important; }
    .stButton>button { width: 100%; background-color: #3730A3; color: #FFFFFF; font-weight: 500; border-radius: 8px; height: 3.4em; border: none; transition: 0.2s; }
    .stButton>button:hover { background-color: #312E81; color: #FFFFFF; }
    .footer-copyright { text-align: center; color: #94A3B8; font-size: 12px; margin-top: 3rem; border-top: 1px solid #E2E8F0; padding-top: 15px; }
    </style>
""", unsafe_allow_html=True)

lang = st.radio("Language", ["English", "العربية"], horizontal=True, label_visibility="collapsed")

if lang == "العربية":
    T = {"title": "LeadAK", "heading": "أنشئ رسالة تحقق التحويل المستهدف", "subheading": "أدخل بعض التفاصيل وسيقوم الذكاء الاصطناعي بصياغة الرسالة المثالية لجمهورك.", "target": "الجهة المستهدفة", "target_ph": "اسم الشخص أو الشركة المستهدفة", "ind": "مجال العمل / المنتج / الخدمة", "ind_ph": "مثال: التطوير العقاري أو SaaS", "post": "النشاط أو المنشور الأخير للعميل", "post_ph": "الصق منشور العميل الأخير هنا...", "post_sub": "سيقوم الذكاء الاصطناعي بتحليل المنشور وإنشاء رسالة مخصصة.", "btn": "إنشاء الرسالة", "err": "يرجى إدخال البيانات المطلوبة وتأكد من المفتاح.", "wait": "جاري التحليل والإنشاء...", "res": "النتيجة النهائية:", "footer": "© 2026 LeadAK. All rights reserved."}
else:
    T = {"title": "LeadAK", "heading": "Generate a Message That Converts", "subheading": "Provide a few details and AI will craft the perfect message for your audience.", "target": "Target Name", "target_ph": "Person or Company name", "ind": "Company / Product / Service", "ind_ph": "e.g., Real Estate or SaaS", "post": "Client's Latest Post", "post_ph": "Paste the client's latest post here...", "post_sub": "AI will analyze this post and create a personalized message.", "btn": "Generate Message", "err": "Please check input fields and API key.", "wait": "Analyzing & generating...", "res": "Generated Message:", "footer": "© 2026 LeadAK. All rights reserved."}

API_KEY = os.getenv("GEMINI_API_KEY")

st.markdown(f"""
    <div class='brand-header'>
        <div class='brand-logo'>⚡ LeadAK</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"<h2 style='text-align: center; color: #1E1B4B; font-weight: 600;'>{T['heading']}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #64748B; margin-bottom: 2rem;'>{T['subheading']}</p>", unsafe_allow_html=True)

target_name = st.text_input(T["target"], placeholder=T["target_ph"])
industry = st.text_input(T["ind"], placeholder=T["ind_ph"])
post_content = st.text_area(T["post"], placeholder=T["post_ph"], height=120)
st.markdown(f"<p style='color: #94A3B8; font-size: 12px; margin-top: -10px; margin-bottom: 1.5rem;'>{T['post_sub']}</p>", unsafe_allow_html=True)

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
            prompt = f'''You are a senior B2B Sales Specialist. Write a highly personalized, concise outreach message. Target: {target_name}. Industry: {industry}. Context/Activity: {post_content}. Language: {output_lang}. Rules: No emojis. Keep it highly professional, clean, and minimalist. Mention their context naturally. End with a simple CTA. Provide ONLY the message text.'''
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            try:
                res = requests.post(url, json=payload, timeout=45)
                if res.status_code == 200:
                    ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.text_area(T["res"], value=ans, height=180)
                else:
                    st.error(f"Error connecting to model. Code: {res.status_code}")
            except Exception:
                st.error("Connection failed.")

st.markdown(f"<div class='footer-copyright'>{T['footer']}</div>", unsafe_allow_html=True)
