import os
import json
import requests
import streamlit as st

st.set_page_config(
    page_title="LeadAK - Prospecting",
    page_icon="🎯",
    layout="centered"
)

st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stButton>button {
        width: 100%;
        background-color: #0A66C2;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("GEMINI_API_KEY")

def get_working_model(api_key):
    if not api_key:
        return "models/gemma-2-2b-it"
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
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
st.title("🎯 LeadAK Prospector Pro")
st.caption("أداة صياغة رسائل التواصل المخصصة بناءً على نشاط LinkedIn")
st.divider()

st.subheader("📋 بيانات العميل المستهدف")
target_type = st.radio("نوع الهدف:", ["شخص (VIP)", "شركة (Business)"], horizontal=True)

if "شخص" in target_type:
    lead_name = st.text_input("اسم الشخص والمنصب:", placeholder="مثال: د. أحمد - مدير الاستثمار")
    industry = st.text_input("المجال:", placeholder="مثال: التطوير العقاري")
    post_content = st.text_area("مضمون أحدث منشور له:", placeholder="كتب منشوراً عن التوسع...")
else:
    lead_name = st.text_input("اسم الشركة:", placeholder="مثال: شركة إعمار")
    industry = st.text_input("المجال:", placeholder="مثال: عقارات تجارية")
    post_content = st.text_area("أحدث منشور للشركة:", placeholder="أعلنوا عن افتتاح فرع جديد...")

st.subheader("⚙️ إعدادات الرسالة")
col_tone, col_platform = st.columns(2)
with col_tone:
    tone = st.selectbox("النبرة:", ["احترافي ومباشر", "ودود واحترافي", "رسمي جداً (VIP)", "مختصر ومحفز"])
with col_platform:
    platform = st.selectbox("القناة:", ["LinkedIn InMail", "WhatsApp Message", "Cold Email"])
if st.button("🚀 توليد الرسالة المخصصة"):
    if not API_KEY:
        st.error("مفتاح API غير متوفر!")
    elif not lead_name or not post_content:
        st.warning("يرجى إدخال اسم العميل والمنشور.")
    else:
        with st.spinner("جاري التوليد..."):
            MODEL_NAME = get_working_model(API_KEY)
            prompt = f"""
            أنت خبير مبيعات B2B. اكتب رسالة مخصصة لـ ({target_type}) لفتح باب حوار بيعي.
            البيانات:
            - الهدف: {lead_name} | المجال: {industry}
            - المنشور الأخير: {post_content}
            - النبرة: {tone} | القناة: {platform}

            التعليمات:
            1. اذكر ما ورد في منشوره بذكاء لتأكيد التخصيص.
            2. اربط بين كلامه وبين فرصة التعاون بأسلوب سلس.
            3. انهِ بدعوة بسيطة للتواصل (CTA).
            """
            url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            try:
                res = requests.post(url, json=payload, timeout=45)
                if res.status_code == 200:
                    ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("تم التوليد بنجاح!")
                    st.text_area("النص الجاهز للنسخ:", value=ans, height=200)
                else:
                    st.error(f"خطأ: {res.status_code}")
            except Exception as e:
                st.error(f"خطأ في الاتصال: {str(e)}")
