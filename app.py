import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# إعدادات الصفحة
st.set_page_config(
    page_title="القناص الرقمي V8",
    page_icon="🎯",
    layout="wide"
)

# CSS مخصص لتحسين المظهر
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #667eea;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 30px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #764ba2;
        transform: scale(1.05);
    }
    .analysis-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# دالة التحليل الرئيسية
def analyze_stock(api_key, symbol, image):
    if not api_key:
        return "⚠️ يرجى إدخال مفتاح الـ API الجديد"
    
    if not symbol:
        return "⚠️ يرجى إدخال رمز السهم"
    
    try:
        # إعداد الاتصال
        genai.configure(api_key=api_key)
        
        # استخدام النموذج
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # البرومبت الاحترافي
        prompt = f"""
        أنت الآن كبير المحللين الفنيين في 'القناص الرقمي V8'. 
        المهمة: تحليل السهم {symbol} بناءً على الشارت المرفق بدقة متناهية.
        
        مطلوب منك في التقرير:
        1. قراءة حركة السعر (Price Action) وتحديد الاتجاه الحالي.
        2. تحديد مستويات الدعم والمقاومة الأساسية الظاهرة في الشارت.
        3. تحليل الشموع اليابانية (مثل الابتلاعية، المطرقة، إلخ) وتوقع الحركة القادمة.
        4. تقييم المخاطر (Risk Assessment).
        5. التوصية النهائية: (شراء/دخول، انتظار، أو تخفيف/خروج) مع تبرير فني قوي.
        
        اجعل الأسلوب احترافياً، منظماً في نقاط، ومباشراً.
        استخدم الإيموجي لتحسين القراءة (📈 📉 ✅ ⚠️ 🎯).
        """
        
        if image is not None:
            # دمج الصورة مع التعليمات
            response = model.generate_content([prompt, image])
        else:
            # تحليل عام في حال عدم توفر صورة
            response = model.generate_content(
                f"قدم تحليل فني وتوقعات لسهم {symbol} بناءً على بيانات السوق الحالية."
            )
        
        return response.text
    
    except Exception as e:
        return f"❌ تنبيه من النظام: {str(e)}\n\nتأكد من صحة المفتاح API وصلاحياته."

# العنوان الرئيسي
st.markdown("""
<div class="main-header">
    <h1>🎯 القناص الرقمي V8</h1>
    <p style="font-size: 18px;">الإصدار الاحترافي | تحليل فني متقدم بالذكاء الاصطناعي</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# القسم الجانبي للإدخالات
with st.sidebar:
    st.header("⚙️ إعدادات التحليل")
    
    # إدخال مفتاح API
    api_key = st.text_input(
        "🔑 مفتاح Google Gemini API",
        type="password",
        placeholder="AIzaSy...",
        help="احصل على المفتاح من: https://makersuite.google.com/app/apikey"
    )
    
    # إدخال رمز السهم
    symbol = st.text_input(
        "📊 رمز السهم (Ticker)",
        placeholder="مثال: NVDA, AAPL, TSLA",
        help="أدخل رمز السهم الأمريكي"
    ).upper()
    
    st.markdown("---")
    
    # رفع الصورة
    st.subheader("📸 رفع شارت السهم")
    uploaded_file = st.file_uploader(
        "اختر صورة الشارت",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="ارفع صورة واضحة للشارت للحصول على تحليل دقيق"
    )
    
    # عرض الصورة المرفوعة
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="الشارت المرفوع", use_container_width=True)
    else:
        image = None
    
    st.markdown("---")
    
    # زر التحليل
    analyze_button = st.button("🚀 إطلاق التحليل العميق V8", use_container_width=True)

# القسم الرئيسي - عرض النتائج
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 تقرير التحليل الفني")
    
    # عند الضغط على زر التحليل
    if analyze_button:
        if not api_key:
            st.error("⚠️ يرجى إدخال مفتاح API في القائمة الجانبية")
        elif not symbol:
            st.error("⚠️ يرجى إدخال رمز السهم")
        else:
            with st.spinner(f"🔍 جاري تحليل السهم {symbol}... يرجى الانتظار"):
                result = analyze_stock(api_key, symbol, image)
                
                # عرض النتيجة في صندوق مخصص
                st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # زر لتحميل التقرير
                st.download_button(
                    label="📥 تحميل التقرير",
                    data=result,
                    file_name=f"{symbol}_analysis.txt",
                    mime="text/plain"
                )

with col2:
    st.header("ℹ️ معلومات الاستخدام")
    
    st.info("""
    **كيفية الاستخدام:**
    
    1️⃣ أدخل مفتاح Gemini API
    
    2️⃣ اكتب رمز السهم (Ticker)
    
    3️⃣ ارفع صورة الشارت (اختياري)
    
    4️⃣ اضغط على زر التحليل
    """)
    
    st.success("""
    **مميزات V8:**
    
    ✅ تحليل Price Action
    
    ✅ كشف الدعم والمقاومة
    
    ✅ تحليل الشموع اليابانية
    
    ✅ تقييم المخاطر
    
    ✅ توصيات واضحة
    """)
    
    st.warning("""
    **ملاحظات هامة:**
    
    ⚠️ المفتاح يُحفظ في الجلسة فقط
    
    ⚠️ للتحليل الدقيق، ارفع شارت واضح
    
    ⚠️ التحليل للاستئناس فقط
    """)

# الفوتر
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🎯 القناص الرقمي V8 | تم التطوير بواسطة الذكاء الاصطناعي</p>
    <p style="font-size: 12px;">⚠️ تنويه: هذا التطبيق للأغراض التعليمية فقط. استشر خبيراً مالياً قبل اتخاذ قرارات الاستثمار.</p>
</div>
""", unsafe_allow_html=True)
