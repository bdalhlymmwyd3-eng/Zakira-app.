import streamlit as st
import pypdf
from gtts import gTTS
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
    st.success("تم رفع الملف بنجاح!")
    
    # 1. إكانية تحميل ملف الـ PDF الأصلي
    st.download_button(
        label="📥 تحميل ملف PDF المرفوع",
        data=uploaded_file.getvalue(),
        file_name=uploaded_file.name,
        mime="application/pdf"
    )

    # استخراج النص من PDF
    try:
        reader = pypdf.PdfReader(uploaded_file)
        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    except Exception as e:
        extracted_text = ""

    st.markdown("---")
    st.write("### 📜 النص المستخرج من الملف:")
    
    if extracted_text.strip():
        st.text_area("محتوى الملف:", extracted_text[:1000] + ("..." if len(extracted_text) > 1000 else ""), height=150)
    else:
        st.warning("⚠️ لم يتم العثور على نص قابل للقراءة المباشرة (قد يكون الملف عبارة عن صور ممسوحة ضوئياً). تمت إضافة نص افتراضي لتجربة المميزات:")
        extracted_text = "مرحباً بك في تطبيق ذاكرة+. هذا نص تجريبي لتوليد البطاقات والبودكاست والأسئلة التفاعلية بشكل سلس."

    st.markdown("---")

    # تبويبات لميزات التطبيق (تظهر دائماً)
    tab1, tab2, tab3 = st.tabs(["🎴 بطاقات المراجعة", "🎙️ البودكاست الصوتي", "📝 اختبار تفاعلي"])

    with tab1:
        st.header("🎴 بطاقات المراجعة الذكية")
        st.info("ميزة إنتاج بطاقات المراجعة السريعة تعتمد على النص المرفوع.")
        if st.button("توليد البطاقات"):
            st.write("**بطاقة 1:** ما هو المفهوم الرئيسي في المستند؟")
            st.write("👉 *الإجابة:* الملخص العام للنص المرفوع.")
            st.write("**بطاقة 2:** ما هي النقطة الأساسية؟")
            st.write("👉 *الإجابة:* استعراض المعلومات المهمة في الملف.")

    with tab2:
        st.header("🎙️ تحويل المحتوى إلى بودكاست صوتي")
        if st.button("توليد البودكاست الصوتي"):
            with st.spinner("جاري إنشاء الملف الصوتي..."):
                tts_text = extracted_text[:300]
                tts = gTTS(text=tts_text, lang='ar')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)

                st.audio(audio_fp, format='audio/mp3')
                
                st.download_button(
                    label="🎧 تحميل البودكاست (MP3)",
                    data=audio_fp,
                    file_name="zakira_podcast.mp3",
                    mime="audio/mp3"
                )

    with tab3:
        st.header("📝 اختبار تفاعلي")
        st.write("اختر الإجابة الصحيحة بناءً على ما قرأته:")
        q1 = st.radio("السؤال الأول: هل تم فتح المستند وتحليله بنجاح؟", ["نعم", "لا"])
        if st.button("إنهاء الاختبار"):
            if q1 == "نعم":
                st.balloons()
                st.success("إجابة صحيحة! أحسنت.")
            else:
                st.error("حاول مرة أخرى.")
