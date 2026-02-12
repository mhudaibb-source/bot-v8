import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# إعدادات الصفحة
st.set_page_config(
    page_title="القناص الرقمي V8",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 15px 40px;
        border: none;
        font-size: 18px;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .analysis-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        border-right: 5px solid #667eea;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        direction: rtl;
    }
    
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# دالة التحليل
def analyze_stock(api_key, symbol, image):
    """تحليل السهم باستخدام Gemini"""
    
    if not api_key or api_key.strip() == "":
        return "⚠️ **خطأ:** يرجى إدخال مفتاح Google Gemini API في القائمة الجانبية"
    
    if not symbol or symbol.strip() == "":
        return "⚠️ **خطأ:** يرجى إدخال رمز السهم (Ticker)"
    
    try:
        # تكوين API
        genai.configure(api_key=api_key)
        
        # استخدام النموذج
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # البرومبت الاحترافي
        prompt = f"""
أنت محلل فني محترف متخصص في أسواق الأسهم. قم بتحليل السهم **{symbol}** بناءً على {"الشارت المرفق" if image else "البيانات المتاحة"}.

📊 **التحليل المطلوب:**

1️⃣ **حركة السعر (Price Action):**
   - ما هو الاتجاه الحالي؟ (صاعد/هابط/عرضي)
   - تحديد النمط السعري الظاهر

2️⃣ **الدعم والمقاومة:**
   - أهم مستويات الدعم القريبة
   - أهم مستويات المقاومة القريبة

3️⃣ **تحليل الشموع اليابانية:**
   - الأنماط الظاهرة (إن وجدت)
   - التوقعات القصيرة المدى

4️⃣ **تقييم المخاطر:**
   - مستوى المخاطر (منخفض/متوسط/عالي)
   - أسباب التقييم

5️⃣ **التوصية النهائية:**
   - 🟢 شراء / 🟡 انتظار / 🔴 بيع
   - التبرير الفني للتوصية
   - نقطة الدخول المقترحة (إن كانت شراء)
   - وقف الخسارة المقترح

⚠️ **ملاحظة:** استخدم الإيموجي لتحسين القراءة، وكن دقيقاً ومختصراً.
        """
        
        # إرسال الطلب
        if image is not None:
            response = model.generate_content([prompt, image])
        else:
            response = model.generate_content(prompt)
        
        return response.text
    
    except Exception as e:
        error_msg = str(e)
        
        if "API_KEY_INVALID" in error_msg or "API key" in error_msg:
            return """
❌ **خطأ في مفتاح API:**

المفتاح غير صحيح أو منتهي الصلاحية.

**الحل:**
1. اذهب إلى: https://makersuite.google.com/app/apikey
2. أنشئ مفتاحاً جديداً
3. انسخه والصقه في الحقل بالأعلى
            """
        elif "quota" in error_msg.lower():
            return "⚠️ **تحذير:** وصلت للحد الأقصى من الطلبات. انتظر قليلاً وحاول مرة أخرى."
        else:
            return f"❌ **خطأ غير متوقع:**\n\n```\n{error_msg}\n```\n\nتحقق من المفتاح والاتصال بالإنترنت."

# الواجهة الرئيسية
def main():
    # العنوان
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 42px;">🎯 القناص الرقمي V8 PRO</h1>
        <p style="margin:10px 0 0 0; font-size: 18px; opacity: 0.9;">
            تحليل فني احترافي مدعوم بالذكاء الاصطناعي
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # الشريط الجانبي
    with st.sidebar:
        st.markdown("## ⚙️ لوحة التحكم")
        st.markdown("---")
        
        # مفتاح API
        api_key = st.text_input(
            "🔑 مفتاح Gemini API",
            type="password",
            placeholder="AIzaSy...",
            help="احصل على المفتاح من: https://makersuite.google.com/app/apikey"
        )
        
        if api_key:
            st.success("✅ تم إدخال المفتاح")
        
        st.markdown("---")
        
        # رمز السهم
        symbol = st.text_input(
            "📊 رمز السهم",
            placeholder="NVDA",
            help="مثال: AAPL, TSLA, GOOGL"
        ).upper()
        
        st.markdown("---")
        
        # رفع الصورة
        st.markdown("### 📸 شارت السهم")
        uploaded_file = st.file_uploader(
            "ارفع صورة الشارت (اختياري)",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="لتحليل أدق، ارفع شارت واضح"
        )
        
        image = None
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="✅ تم رفع الشارت", use_container_width=True)
        
        st.markdown("---")
        
        # زر التحليل
        analyze_btn = st.button("🚀 تحليل الآن", use_container_width=True)
    
    # المحتوى الرئيسي
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 📊 نتيجة التحليل")
        
        # مساحة النتائج
        result_container = st.container()
        
        if analyze_btn:
            with st.spinner("🔍 جاري التحليل... يرجى الانتظار"):
                result = analyze_stock(api_key, symbol, image)
                
                with result_container:
                    st.markdown(f'<div class="analysis-box">{result}</div>', unsafe_allow_html=True)
                    
                    # زر التحميل
                    if not result.startswith("❌") and not result.startswith("⚠️"):
                        st.download_button(
                            label="📥 تحميل التقرير كملف نصي",
                            data=result,
                            file_name=f"analysis_{symbol}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
    
    with col2:
        st.markdown("## ℹ️ دليل الاستخدام")
        
        st.markdown("""
        <div class="info-card">
            <h4>📝 الخطوات:</h4>
            <ol style="text-align: right; direction: rtl;">
                <li>أدخل مفتاح Gemini API</li>
                <li>اكتب رمز السهم</li>
                <li>ارفع شارت (اختياري)</li>
                <li>اضغط "تحليل الآن"</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card" style="background: #e8f5e9;">
            <h4>✨ المميزات:</h4>
            <ul style="text-align: right; direction: rtl;">
                <li>تحليل Price Action</li>
                <li>كشف الدعم والمقاومة</li>
                <li>تحليل الشموع اليابانية</li>
                <li>تقييم المخاطر</li>
                <li>توصيات واضحة</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card" style="background: #fff3e0;">
            <h4>⚠️ تنبيهات:</h4>
            <ul style="text-align: right; direction: rtl;">
                <li>المفتاح آمن ولا يُحفظ</li>
                <li>التحليل استشاري فقط</li>
                <li>لا يُعد نصيحة استثمارية</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # الفوتر
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p style="font-size: 16px;">🎯 <strong>القناص الرقمي V8 PRO</strong></p>
        <p style="font-size: 12px; margin-top: 10px;">
            ⚠️ هذا التطبيق للأغراض التعليمية فقط • استشر خبيراً مالياً قبل اتخاذ قرارات الاستثمار
        </p>
        <p style="font-size: 12px; color: #999; margin-top: 5px;">
            Powered by Google Gemini AI • Made with ❤️
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
