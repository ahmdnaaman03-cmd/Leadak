import os
import requests
import streamlit as st
import base64

st.set_page_config(page_title="LeadAK", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .header-box { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; padding: 0 10px; }
    .brand { display: flex; align-items: center; gap: 8px; font-size: 24px; font-weight: 800; color: #1E1B4B; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { border-radius: 10px !important; border: 1px solid #E2E8F0 !important; background: #F8FAFC !important; }
    .stButton>button { width: 100%; background-color: #3730A3 !important; color: white !important; border-radius: 10px !important; font-weight: 600; height: 3.5em; }
    </style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("GEMINI_API_KEY")
st.markdown('<div class="header-box"><div class="brand"><span>🔀</span> LeadAK</div>', unsafe_allow_html=True)
lang = st.radio("L", ["Arabic", "English"], horizontal=True, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if lang == "Arabic":
    T = {"head": "أنشئ رسالة تحقق التحويل", "sub": "أدخل التفاصيل وسأصيغ لك الرسالة المثالية.", "target": "الجهة المستهدفة", "ind": "الشركة / الخدمة", "post": "منشور العميل أو صورة (سكرين شوت)", "btn": "إنشاء الرسالة"}
else:
    T = {"head": "Generate a Message That Converts", "sub": "Provide a few details and I will craft the perfect message.", "target": "Target Name", "ind": "Company / Product / Service", "post": "Client's Latest Post or Screenshot", "btn": "Generate Message"}

st.markdown(f"<h1 style='text-align: center; color: #1E1B4B;'>{T['head']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #64748B;'>{T['sub']}</p>", unsafe_allow_html=True)

target = st.text_input(T["target"], placeholder="Name...")
company = st.text_input(T["ind"], placeholder="Service...")
post_text = st.text_area(T["post"], placeholder="Paste text or upload image below...")
uploaded_img = st.file_uploader("", type=["jpg", "png"], label_visibility="collapsed")

if st.button(T["btn"]):
    if not API_KEY: st.error("API Key missing.")
    else:
        with st.spinner("Analyzing..."):
            model = "gemini-1.5-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
            parts = [{"text": f"Target: {target}, Company: {company}, Text: {post_text}. Write a professional outreach message."}]
            if uploaded_img:
                img_data = base64.b64encode(uploaded_img.getvalue()).decode()
                parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img_data}})
            res = requests.post(url, json={"contents": [{"parts": parts}]})
            if res.status_code == 200:
                st.text_area("Result:", value=res.json()['candidates'][0]['content']['parts'][0]['text'], height=200)

