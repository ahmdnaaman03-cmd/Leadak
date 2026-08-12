import os
import requests
import streamlit as st

st.set_page_config(page_title="LeadAK", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; font-family: 'Helvetica Neue', Arial, sans-serif; }
    h1 { color: #0F4C81 !important; font-weight: 400 !important; margin-bottom: -10px; }
    .caption-text { color: #64748B; font-size: 14px; margin-bottom: 2rem; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div { 
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 4px; box-shadow: none; 
    }
    .stButton>button {
        width: 100%; background-color: #0F4C81; color: #FFFFFF; 
        font-weight: 500; border-radius: 4px; height: 3em; border: none; transition: 0.2s;
    }
    .stButton>button:hover { background-color: #1A5F7A; color: #FFFFFF; }
    div[data-testid="stExpander"] { background-color: transparent; border: none; box-shadow: none; }
    </style>
""", unsafe_allow_html=True)

lang = st.radio("Language", ["English", "العربية"], horizontal=True, label_visibility="collapsed")

if lang == "العربية":
    T = {
        "title": "LeadAK Prospector",
        "caption": "صياغة رسائل التواصل الاحترافية للمبيعات",
        "target": "الجهة المستهدفة (اسم العميل أو الشركة)",
        "target_ph": "مثال: د. أحمد - مدير استثمار، أو شركة إعمار",
        "ind": "مجال العمل",
        "ind_ph": "مثال: التطوير العقاري",
        "post": "السياق أو المنشور الأخير",
        "post_ph": "أعلنوا عن التوسع في مشاريع جديدة...",
        "adv": "خيارات إضافية",
        "tone": "نبرة الرسالة",
        "tones": ["احترافي ومباشر", "ودود", "رسمي"],
        "platform": "قناة التواصل",
        "platforms": ["LinkedIn InMail", "Email", "WhatsApp"],
        "btn": "توليد الرسالة",
        "err": "يرجى التأكد من المفتاح والبيانات المدخلة.",
        "wait": "جاري المعالجة...",
        "res": "الرسالة الجاهزة:"
    }
else:
    T = {
        "title": "LeadAK Prospector",
        "caption": "Enterprise Outreach & Sales Message Generator",
        "target": "Target Name (Person or Company)",
        "target_ph": "e.g., Dr. Ahmed - CEO, or Emaar Properties",
        "ind": "Industry",
        "ind_ph": "e.g., Real Estate",
        "post": "Context / Recent Activity",
        "post_ph": "They recently announced a new project...",
        "adv": "Advanced Options",
        "tone": "Tone",
        "tones": ["Professional", "Friendly", "Formal"],
        "platform": "Channel",
        "platforms": ["LinkedIn InMail", "Email", "WhatsApp"],
        "btn": "Generate Message",
        "err": "Please check API key and input fields.",
        "wait": "Processing...",
        "res": "Generated Message:"
    }

API_KEY = os.getenv("GEMINI_API_KEY")

st.markdown(f"<h1>{T['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='caption-text'>{T['caption']}</div>", unsafe_allow_html=True)

target_name = st.text_input(T["target"], placeholder=T["target_ph"])
industry = st.text_input(T["ind"], placeholder=T["ind_ph"])
post_content = st.text_area(T["post"], placeholder=T["post_ph"], height=100)

with st.expander(T["adv"]):
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(T["tone"], T["tones"])
    with col2:
        platform = st.selectbox(T["platform"], T["platforms"])

if st.button(T["btn"]):
    if not API_KEY or not target_name or not post_content:
        st.error(T["err"])
    else:
        with st.spinner(T["wait"]):
            output_lang = "Arabic" if lang == "العربية" else "English"
            prompt = f'''You are a senior B2B Sales Specialist. Write a highly personalized, concise outreach message. Target: {target_name}. Industry: {industry}. Context/Activity: {post_content}. Tone: {tone}. Channel: {platform}. Language: {output_lang}. Rules: No emojis. Keep it highly professional, clean, and minimalist. Mention their context naturally. End with a simple CTA. Provide ONLY the message text.'''
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-2-2b-it:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            try:
                res = requests.post(url, json=payload, timeout=45)
                if res.status_code == 200:
                    ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.text_area(T["res"], value=ans, height=200)
                else:
                    st.error("Error connecting to the model.")
            except Exception:
                st.error("Connection failed.")
