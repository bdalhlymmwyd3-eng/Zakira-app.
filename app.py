import streamlit as st
import pypdf
from gtts import gTTS
import io
import time

# إعداد الصفحة الرئيسية والتصميم
st.set_page_config(
    page_title="Zakira+ | ذاكرة+",
    page_icon="🧠",
    layout="wide"
)

# دعم اللغات (Language Selector)
lang = st.sidebar.selectbox("🌐 اختر اللغة / Select Language", ["العربية", "English"])

# قاموس النصوص لدعم اللغتين
TEXTS = {
    "العربية": {
        "title": "🧠 تطبيق ذاكرة+ الخيالي (Zakira+)",
        "subtitle": "بوابة التعلم الذكية: بطاقات بصرية، بودكاست صوتي، اختبارات متدرجة، ومحادثات ذكية تفاعلية!",
        "upload_label": "قم برفع ملف PDF الخاص بك هنا",
        "upload_success": "تم رفع الملف بنجاح!",
        "download_pdf": "📥 تحميل ملف PDF المرفوع",
        "tab_cards": "🎴 بطاقات بصرية مصورة",
        "tab_audio": "🎙️ بودكاست صوتي حقيقي",
        "tab_quiz": "📝 اختبار مستويات تفاعلي",
        "tab_video": "🎬 فيديو تعليمي",
        "tab_call": "🎧 اختبار المحادثة الصوتية الذكية",
        "select_level": "اختر مستوى الأسئلة:",
        "levels": ["مبتدئ 🟢", "متوسط 🟡", "خبير 🔴"],
        "call_start": "بدء اختبار المحادثة مع الذكاء الاصطناعي",
        "call_active": "🎙️ المحادثة جارية... الذكاء الاصطناعي يناقشك في محتوى الملف ويراقب التزامك بالموضوع!",
        "timer_select": "حدد وقت المحادثة (بالدقائق):",
        "topic_warning": "⚠️ تنبيه: يبدو أنك خرجت عن موضوع الملف المرفوع! تم إنهاء الاختبار الصوتي حفاظاً على مسار التعلم."
    },
    "English": {
        "title": "🧠 Futuristic Zakira+ App",
        "subtitle": "Smart Learning Portal: Visual Cards, Podcasts, Leveled Quizzes, and Smart Voice Conversations!",
        "upload_label": "Upload your PDF file here",
        "upload_success": "File uploaded successfully!",
        "download_pdf": "📥 Download Uploaded PDF",
        "tab_cards": "🎴 Visual Flashcards",
        "tab_audio": "🎙️ Real Voice Podcast",
        "tab_quiz": "📝 Leveled Quiz",
        "tab_video": "🎬 Educational Video",
        "tab_call": "🎧 Smart Voice Conversation Exam",
        "select_level": "Select Quiz Difficulty Level:",
        "levels": ["Beginner 🟢", "Intermediate 🟡", "Expert 🔴"],
        "call_start": "Start AI Conversation Exam",
        "call_active": "🎙️ Conversation in Progress... AI is discussing the document and monitoring your focus!",
        "timer_select": "Select conversation duration (minutes):",
        "topic_warning": "⚠️ Warning: It seems you went off-topic! The voice exam has been ended to keep your learning on track."
    }
}

t = TEXTS[lang]

# العنوان الرئيسي
st.title(t["title"])
st.caption(t["subtitle"])

# رفع الملف
uploaded_file = st.file_uploader(t["upload_label"], type=["pdf"])

if uploaded_file is not None:
    st.success(t["upload_success"])
    st.download_button(label=t["download_pdf"], data=uploaded_file.getvalue(), file_name=uploaded_file.name, mime="application/pdf")
    
    # استخراج النص
    try:
        reader = pypdf.PdfReader(uploaded_file)
        extracted_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except:
        extracted_text = ""
        
    if not extracted_text.strip():
        extracted_text = "Zakira+ AI Smart Content Processing System." if lang == "English" else "محتوى ذكي معالج تلقائياً بواسطة نظام ذاكرة+."

    st.markdown("---")

    # التبويبات الخمسة الرئيسية
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t["tab_cards"], 
        t["tab_audio"], 
        t["tab_quiz"], 
        t["tab_video"], 
        t["tab_call"]
    ])

    # 1. البطاقات البصرية المصورة
    with tab1:
        st.header(t["tab_cards"])
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600", caption="المفهوم الأساسي للمستند / Core Concept")
            st.info("**المفهوم الرئيسي:** الشرح البصري المبسط للملف مرفق برسم توضيحي." if lang == "العربية" else "**Main Concept:** Visual simplified explanation of the document.")
        with col2:
            st.image("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600", caption="الربط المعرفي / Knowledge Mapping")
            st.info("**النقطة المحورية:** تحويل المعلومات المعقيدية إلى خريطة مفاهيم بسيطة." if lang == "العربية" else "**Core Point:** Transforming complex information into simple mind maps.")

    # 2. البودكاست الصوتي البشري
    with tab2:
        st.header(t["tab_audio"])
        if st.button("توليد البودكاست / Generate Podcast"):
            with st.spinner("جاري إنشاء المقاطع الصوتية بصوت طبيعي..."):
                tts_text = extracted_text[:400]
                lang_code = 'en' if lang == "English" else 'ar'
                tts = gTTS(text=tts_text, lang=lang_code, slow=False)
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)

                st.audio(audio_fp, format='audio/mp3')

    # 3. اختبار المستويات التفاعلي
    with tab3:
        st.header(t["tab_quiz"])
        level = st.select_slider(t["select_level"], options=t["levels"])
        st.write(f"**المستوى المختار / Selected Level:** {level}")
        
        q = st.radio(
            "السؤال: ما هي الفكرة الأساسية من الملف المرفوع؟" if lang == "العربية" else "Question: What is the main idea of the uploaded document?",
            ["الملخص الشامل والاستيعاب" if lang == "العربية" else "Comprehensive Summary", "التطبيق العملي" if lang == "العربية" else "Practical Application"]
        )
        if st.button("اعتماد الإجابة / Submit Answer"):
            st.balloons()
            st.success("إجابة ممتازة ومطابقة للمستوى! 🎉" if lang == "العربية" else "Excellent and accurate answer! 🎉")

    # 4. مستعرض الفيديو التعليمي
    with tab4:
        st.header(t["tab_video"])
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.write("📌 **نقاط التلخيص من الفيديو:**" if lang == "العربية" else "📌 **Video Key Takeaways:**")
        st.markdown("- شرح المفاهيم المعقدة بالأنيميشن.\n- الربط بين المادة النظرية والتطبيق.")

    # 5. اختبار المحادثة الصوتية الذكية (مع التحكم بالوقت ومراقبة الخروج عن الموضوع)
    with tab5:
        st.header(t["tab_call"])
        st.write("🎙️ **ناقش محتوى الملف صوتياً مع الذكاء الاصطناعي. النظام يراقب التزامك بالموضوع ويقيس وقتك المخصص.**" if lang == "العربية" else "🎙️ **Discuss the document's content with AI via voice. The system monitors your focus and custom duration.**")
        
        # اختيار الوقت بحرية من الطالب
        duration_mins = st.slider(t["timer_select"], min_value=1, max_value=30, value=5)
        
        # خيار تجريبي لمحاكاة الخروج عن الموضوع
        is_off_topic = st.checkbox("🧪 (وضع تجريبي) محاكاة الخروج عن موضوع الملف" if lang == "العربية" else "🧪 (Test Mode) Simulate going off-topic")
        
        if st.button(t["call_start"]):
            if is_off_topic:
                st.error(t["topic_warning"])
            else:
                st.success(t["call_active"])
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
                
                # مؤشر الوقت بناءً على اختيار الطالب
                timer_placeholder = st.empty()
                total_seconds = duration_mins * 60
                
                for remaining in range(total_seconds, 0, max(1, total_seconds // 10)):
                    mins, secs = divmod(remaining, 60)
                    timer_placeholder.metric(label="الوقت المتبقي / Time Remaining:", value=f"{mins:02d}:{secs:02d}")
                    time.sleep(0.3)
                st.success("🎉 أحسنت! أكملت جلسة المحادثة الصوتية بنجاح ضمن الوقت المحدد." if lang == "العربية" else "🎉 Great job! You successfully completed the voice session within the designated time.")
else:
    st.info("👈 يرجى رفع ملف PDF من القائمة العلوية لبدء التجربة الخيالية!" if lang == "العربية" else "👈 Please upload a PDF file above to start the futuristic experience!")
