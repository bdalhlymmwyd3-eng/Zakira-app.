import streamlit as st
import pypdf
from gtts import gTTS
import os
import io

# إعداد الصفحة الرئيسية
st.set_page_config(
    page_title="ذاكرة+ | Zakira+",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 تطبيق ذاكرة+ (Zakira+)")
st.subheader("حول ملفات الـ PDF إلى بطاقات مراجعة، بودكاست، واختبارات تفاعلية")

# رفع ملف الـ PDF
uploaded_file = st.file_uploader("قم برفع ملف PDF الخاص بك هنا", type=["pdf"])

if uploaded_file is not None:
    # 1. إمكانية تحميل ملف الـ PDF الأصلي
    st.success("تم رفع الملف بنجاح!")
    st.download_button(
        label="📥 تحميل ملف PDF المرفوع",
        data=uploaded_file.getvalue(),
        file_name=uploaded_file.name,
        mime="application/pdf"
    )

    # استخراج النص من PDF
    reader = pypdf.PdfReader(uploaded_file)
    extracted_text = ""
