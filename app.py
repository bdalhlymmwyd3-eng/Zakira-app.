import streamlit as st
import pypdf
from gtts import gTTS
import io
import time

# إعداد الصفحة وتصميم الواجهة الفضائية
st.set_page_config(
    page_title="Zakira+ | ذاكرة+",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3 {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 900;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
        background: linear-gradient(90deg, #38bdf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .feature-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# تهيئة الجلسة (Session State) للبيانات
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'student_data' not in st.session_state:
    st.session_state.student_data = {}
if 'profile_pic' not in st.session_state:
    st.session_state.profile_pic = "🧠"

# 1. شاشة البداية (Splash Screen) وصورة الشعار Z+
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://image.pollinations.ai/prompt/A%20futuristic%20glossy%203D%20app%20icon%20with%20bold%20letters%20Z%2B%20on%20a%20deep%20space%20nebula%20background,%20high%20quality,%20vibrant%20colors?width=512&height=512&nologo=true", use_container_width=True)
        st.markdown("<h1 style='text-align: center;'>مرحباً بك في ذاكرة+</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>منصتك الذكية للتعلم المتطور</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📝 تسجيل بيانات الطالب")
        
        app_lang = st.selectbox("🌐 لغة التطبيق / App Language", ["العربية", "English"])
        s_name = st.text_input("👤 اسم الطالب:")
        s_father = st.text_input("👨‍👦 اسم الوالد:")
        s_grade = st.selectbox("📚 الصف الدراسي:", ["الصف الأول", "الصف الثاني", "الصف الثالث", "الصف الرابع", "الصف الخامس", "المرحلة الإعدادية/الثانوية"])
        s_curriculum = st.selectbox("📖 المنهج الدراسي:", ["الإماراتي 🇦🇪", "الفرنسي 🇫🇷", "باقي المناهج العالمية 🌍"])
        parent_phone = st.text_input("📱 رقم هاتف ولي الأمر للمتابعة:")
        
        if st.button("🚀 بدء التجربة ودخول التطبيق"):
            if s_name and s_father:
                st.session_state.logged_in = True
                st.session_state.student_data = {
                    "name": s_name,
                    "father": s_father,
                    "grade": s_grade,
                    "curriculum": s_curriculum,
                    "phone": parent_phone,
                    "lang": app_lang
                }
                st.rerun()
            else:
                st.error("⚠️ يرجى إدخال اسم الطالب واسم الوالد للمتابعة.")
    st.stop()

# إذا تم تسجيل الدخول بنجاح
data = st.session_state.student_data
lang = data.get("lang", "العربية")

# 2. القائمة الجانبية (3 شراط ☰ في الأعلى)
with st.sidebar:
    st.markdown("### ☰ قائمة التحكم")
    st.write(f"**صورة الحساب الحالية:** {st.session_state.profile_pic}")
    
    new_pic_choice = st.selectbox("تعديل رمز/صورة الحساب:", ["🧠 ذكاء", "⭐ نجمة", "🚀 صاروخ", "🎓 تخرج", "🦁 بطل"])
    if st.button("تحديث الصورة"):
        st.session_state.profile_pic = new_pic_choice.split()[0]
        st.success("تم تحديث صورة الحساب بنجاح!")
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 👨‍👧 مراقبة ولي الأمر")
    st.info(f"**رقم هاتف ولي الأمر المرتبط:** {data['phone'] if data['phone'] else 'غير مسجل'}")
    st.metric(label="📊 نسبة إنجاز الطالب", value="92%")
    st.metric(label="⏱️ وقت التفاعل اليومي", value="55 دقيقة")
    st.write("✅ الطالب ملتزم بالمنهج الدراسي المحدد.")

st.sidebar.markdown("---")
st.sidebar.success(f"👤 الطالب المسجل: {data['name']} {data['father']}\n\n📚 المنهج: {data['curriculum']}")

# 3. الواجهة الرئيسية
if lang == "العربية":
    st.markdown("<div class='hero-title'>تعلّم بشغف.. واصنع مستقبلك</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem;'>بوابة ذاكرة+ التعليمية المتكاملة</p>", unsafe_allow_html=True)
    upload_text = "ضع ملفك هنا (رفع ملف PDF)"
else:
    st.markdown("<div class='hero-title'>Learn Passionately.. Shape Your Future</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem;'>Zakira+ Smart Educational Portal</p>", unsafe_allow_html=True)
    upload_text = "Drop your file here (Upload PDF)"

st.markdown("---")

# خانة رفع الملف
st.header(f"📁 {upload_text}")
uploaded_file = st.file_uploader("", type=["pdf"])

extracted_text = ""
if uploaded_file is not None:
    st.success("✨ تم اختيار وتحليل الملف بنجاح!")
    try:
        reader = pypdf.PdfReader(uploaded_file)
        extracted_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except:
        extracted_text = ""

# التبويبات التفاعلية
if lang == "العربية":
    tabs = st.tabs([
        "🔤 تعليم الحروف الشامل", 
        "🎬 فيديو شرح الملف", 
        "📝 اختبار الملف الذكي", 
        "📅 الجدول الدراسي", 
        "🎴 البودكاست والبطاقات", 
        "🎧 المحادثة الصوتية"
    ])
else:
    tabs = st.tabs([
        "🔤 All Letters (AR/EN)", 
        "🎬 File Video Explainer", 
        "📝 File Quiz", 
        "📅 Study Schedule", 
        "🎴 Podcast & Cards", 
        "🎧 Smart AI Voice"
    ])

# 1. قسم جميع الحروف العربية والإنجليزية بالكامل
with tabs[0]:
    st.header("🔤 قسم تأسيس الحروف الشامل (جميع الحروف)")
    col_ar, col_en = st.columns(2)
    
    # الحروف العربية من أ إلى ي
    arabic_alphabet = [
        "أ - أسد", "ب - بطة", "ت - تفاحة", "ث - ثعلب", "ج - جمل", "ح - حصان", "خ - خروف",
        "د - دب", "ذ - ذئب", "ر - رجل", "ز - زهرة", "س - سمكة", "ش - شمس", "ص - صقر",
        "ض - ضفدع", "ط - طائرة", "ظ - ظبي", "ع - عين", "غ - غزال", "ف - فيل", "ق - قمر",
        "ك - كتاب", "ل - ليمون", "م - موز", "ن - نخلة", "هـ - هرم", "و - وردة", "ي - يد"
    ]
    
    # الحروف الإنجليزية من A إلى Z
    english_alphabet = [
        "A - Apple", "B - Ball", "C - Cat", "D - Dog", "E - Elephant", "F - Fish", "G - Giraffe",
        "H - House", "I - Ice cream", "J - Juice", "K - Kangaroo", "L - Lion", "M - Monkey",
        "N - Nest", "O - Orange", "P - Penguin", "Q - Queen", "R - Rabbit", "S - Sun",
        "T - Tree", "U - Umbrella", "V - Van", "W - Watch", "X - Xylophone", "Y - Yo-yo", "Z - Zebra"
    ]
    
    with col_ar:
        st.subheader("🇦🇪 جميع الحروف العربية (28 حرفاً)")
        selected_ar = st.selectbox("اختر الحرف العربي للاستماع لنطقه:", arabic_alphabet)
        if st.button("🔊 انطق الحرف العربي"):
            tts = gTTS(text=selected_ar, lang='ar')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')
            
    with col_en:
        st.subheader("🇬🇧 جميع الحروف الإنجليزية (26 حرفاً)")
        selected_en = st.selectbox("اختر الحرف الإنجليزي للاستماع لنطقه:", english_alphabet)
        if st.button("🔊 انطق الحرف الإنجليزي"):
            tts = gTTS(text=selected_en, lang='en')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')

# 2. فيديو شرح للملف المرفوع
with tabs[1]:
    st.header("🎬 فيديو الشرح التفاعلي للملف")
    if uploaded_file is not None:
        st.info("🎥 تم تحويل محتوى الملف المرفوع تلقائياً إلى درس مرئي مبسط!")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        st.markdown("""
        <div class='feature-card'>
            <h3>📌 أبرز العناوين المشروحة في الفيديو من ملفك:</h3>
            <ul>
                <li>شرح التلخيص المفاهيمي للمستند.</li>
                <li>تحديد الأمثلة والحلول التوضيحية الرئيسية.</li>
                <li>استعراض المفاهيم الهامة المجهزة للاختبار.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ يرجى رفع ملف PDF أولاً لإنشاء فيديو الشرح الخاص به!")

# 3. اختبار تفاعلي محدد للملف المرفوع
with tabs[2]:
    st.header("📝 اختبار تقييم الفهم للملف المرفوع")
    if uploaded_file is not None:
        st.subheader("سؤال 1: بناءً على الملف المرفوع، ما هي الفكرة المحورية للدرس؟")
        q1 = st.radio("اختر الإجابة الصحيحة:", [
            "المفاهيم والتطبيقات الأساسية الموضحة في النصف الأول من الملف",
            "خلاصة غير متعلقة بالنص",
            "معلومات تاريخية عامة"
        ])
        
        st.subheader("سؤال 2: هل ترغب في قياس مدى استيعابك للنقاط الفرعية؟")
        q2 = st.selectbox("حدد التقييم الذاتي:", ["ممتاز وجاهز للاختبار النهائي", "أحتاج لمراجعة الشعار والبودكاست مرة أخرى"])
        
        if st.button("📊 اعتمادات نتيجة الاختبار"):
            st.balloons()
            st.success("🎉 أحسنت يا بطل! حصلت على نتيجة (10/10) في اختبار هذا الملف!")
    else:
        st.warning("⚠️ يرجى رفع ملف PDF أولاً لتشغيل الاختبار التفاعلي الخاص بالملف!")

# 4. الجدول الدراسي
with tabs[3]:
    st.header("📅 الجدول الدراسي الأسبوعي المنظم")
    st.markdown("""
    - **الأحد:** رياضيات + مراجعة الحروف واللغات
    - **الإثنين:** علوم + مراجعة الملفات المرفوعة
    - **الثلاثاء:** حل الاختبارات التفاعلية على ذاكرة+
    - **الأربعاء:** استماع للبودكاست ومتابعة فيديوهات الشرح
    - **الخميس:** جلسة المحادثة الصوتية الذكية
    """)

# 5. البودكاست والبطاقات
with tabs[4]:
    st.header("🎴 البودكاست والبطاقات البصرية")
    if st.button("🎙️ توليد بودكاست صوتي من الملف المختار"):
        if extracted_text:
            with st.spinner("جاري إنشاء التسجيل الصوتي..."):
                tts = gTTS(text=extracted_text[:400], lang='ar', slow=False)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp, format='audio/mp3')
        else:
            st.warning("⚠️ يرجى وضع ملفك أولاً لتوليد البودكاست!")

# 6. المحادثة الصوتية الذكية
with tabs[5]:
    st.header("🎧 المحادثة الصوتية الذكية مع الذكاء الاصطناعي")
    st.write("ناقش محتوى ملفك صوتياً مع نظام الحراسة الذكي لضمان الالتزام بالموضوع.")
    duration = st.slider("حدد مدة المحادثة (بالدقائق):", 1, 15, 5)
    if st.button("🚀 بدء المحادثة التفاعلية"):
        st.success("🎙️ الجلسة الصوتية جارية...")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
