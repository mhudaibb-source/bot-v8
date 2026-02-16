“””
محلل الأسهم الأمريكية الاحترافي - Streamlit Version
Professional US Stock Analyzer with Beautiful UI
Powered by Streamlit + Claude AI (Optional)
“””

import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import os
from typing import Dict, Optional

try:
import plotly.graph_objects as go
PLOTLY_AVAILABLE = True
except:
PLOTLY_AVAILABLE = False

# إعدادات الصفحة

st.set_page_config(
page_title=“محلل الأسهم الاحترافي”,
page_icon=“📈”,
layout=“wide”,
initial_sidebar_state=“expanded”
)

# CSS مخصص

st.markdown(”””

<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #764ba2;
    }
</style>

“””, unsafe_allow_html=True)

# الإعدادات

ANTHROPIC_API_KEY = os.getenv(“ANTHROPIC_API_KEY”, “”)
USE_AI_ANALYSIS = bool(ANTHROPIC_API_KEY)

# جلب البيانات

@st.cache_data(ttl=300)
def get_stock_data(symbol: str) -> Dict:
“”“جلب بيانات السهم من Yahoo Finance”””
try:
symbol = symbol.strip().upper()
ticker = yf.Ticker(symbol)
info = ticker.info
hist = ticker.history(period=“1mo”)

```
    if hist.empty or not info:
        return {"error": f"لم يتم العثور على بيانات للرمز {symbol}"}
    
    current_price = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
    previous_close = info.get('previousClose') or hist['Close'].iloc[-2] if len(hist) > 1 else current_price
    open_price = info.get('open') or info.get('regularMarketOpen') or hist['Open'].iloc[-1]
    
    change = current_price - previous_close
    change_percent = (change / previous_close * 100) if previous_close else 0
    
    post_price = info.get('postMarketPrice', current_price)
    post_change = info.get('postMarketChange', 0)
    
    volume = info.get('volume') or hist['Volume'].iloc[-1]
    avg_volume = info.get('averageVolume') or hist['Volume'].mean()
    volume_ratio = volume / avg_volume if avg_volume else 1
    
    high_52w = info.get('fiftyTwoWeekHigh', hist['High'].max())
    low_52w = info.get('fiftyTwoWeekLow', hist['Low'].min())
    
    recent_20d = hist.tail(20)
    support = recent_20d['Low'].min()
    resistance = recent_20d['High'].max()
    
    # Reverse Split
    reverse_split = False
    try:
        actions = ticker.actions
        if not actions.empty and 'Stock Splits' in actions.columns:
            thirty_days_ago = datetime.now() - timedelta(days=30)
            recent_splits = actions[actions.index >= thirty_days_ago]['Stock Splits']
            reverse_split = ((recent_splits < 1) & (recent_splits != 0)).any() if not recent_splits.empty else False
    except:
        pass
    
    # الأخبار
    news_list = []
    try:
        news = ticker.news[:3] if hasattr(ticker, 'news') and ticker.news else []
        for article in news:
            news_time = datetime.fromtimestamp(article.get('providerPublishTime', 0))
            hours_ago = int((datetime.now() - news_time).total_seconds() / 3600)
            news_list.append({
                "title": article.get('title', 'No title')[:80],
                "publisher": article.get('publisher', 'Unknown'),
                "hours_ago": hours_ago
            })
    except:
        pass
    
    return {
        "symbol": symbol,
        "name": info.get('longName') or info.get('shortName') or symbol,
        "current_price": float(current_price),
        "previous_close": float(previous_close),
        "open_price": float(open_price),
        "change": float(change),
        "change_percent": float(change_percent),
        "post_price": float(post_price),
        "post_change": float(post_change),
        "volume": int(volume),
        "avg_volume": int(avg_volume),
        "volume_ratio": float(volume_ratio),
        "high_52w": float(high_52w),
        "low_52w": float(low_52w),
        "support": float(support),
        "resistance": float(resistance),
        "reverse_split": bool(reverse_split),
        "news": news_list,
        "market_cap": info.get('marketCap', 0),
        "sector": info.get('sector', 'Unknown'),
        "history": hist
    }
    
except Exception as e:
    return {"error": f"خطأ في جلب البيانات: {str(e)}"}
```

# التحليل بالذكاء الاصطناعي

def analyze_with_claude(data: Dict) -> Optional[str]:
“”“تحليل ذكي بواسطة Claude AI”””
if not USE_AI_ANALYSIS:
return None

```
try:
    import anthropic
    
    prompt = f"""أنت محلل أسهم محترف. قم بتحليل هذا السهم وإعطاء توصية واضحة.
```

البيانات:

- الرمز: {data[‘symbol’]} ({data[‘name’]})
- السعر الحالي: ${data[‘current_price’]:.2f}
- التغيير: {data[‘change_percent’]:+.2f}%
- الدعم: ${data[‘support’]:.2f}
- المقاومة: ${data[‘resistance’]:.2f}
- الفوليوم: {data[‘volume’]:,} (نسبة {data[‘volume_ratio’]:.2f}x من المتوسط)
- أعلى 52 أسبوع: ${data[‘high_52w’]:.2f}
- أقل 52 أسبوع: ${data[‘low_52w’]:.2f}
- Reverse Split: {‘نعم’ if data[‘reverse_split’] else ‘لا’}

المطلوب: تحليل سريع بالعربية في 100-150 كلمة.”””

```
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text
    
except Exception as e:
    return None
```

# التحليل التقليدي

def traditional_analysis(data: Dict) -> Dict:
“”“التحليل التقليدي المتقدم”””
current = data[‘current_price’]
support = data[‘support’]
resistance = data[‘resistance’]

```
entry = support * 1.01 if current > support * 1.02 else current
target_near = entry * 1.04
target_far = entry * 1.12
stop_loss = entry * 0.94

bag_holders = current < (data['high_52w'] * 0.70)

if data['volume_ratio'] > 1.2:
    vol_status = "🟢 حقيقي وقوي"
elif data['volume_ratio'] > 0.8:
    vol_status = "🟡 متوسط"
else:
    vol_status = "🔴 ضعيف"

distance_support = ((current - support) / support) * 100
distance_resistance = ((resistance - current) / current) * 100

if current < stop_loss:
    recommendation = "🔴 ارفض الصفقة"
    reason = "السعر تحت مستوى الأمان"
elif distance_support < 3:
    recommendation = "🟢 اشتري الآن"
    reason = "السعر قريب من الدعم - فرصة ممتازة"
elif distance_resistance < 5:
    recommendation = "🟡 انتظر"
    reason = "السعر قريب من المقاومة"
elif data['change_percent'] > 5:
    recommendation = "🟡 انتظر تصحيح"
    reason = "السهم ارتفع كثيراً اليوم"
else:
    recommendation = "🟢 اشتري"
    reason = "الظروف مناسبة للدخول"

return {
    "entry": entry,
    "target_near": target_near,
    "target_far": target_far,
    "stop_loss": stop_loss,
    "bag_holders": bag_holders,
    "volume_status": vol_status,
    "recommendation": recommendation,
    "reason": reason,
    "risk_reward": round((target_far - entry) / (entry - stop_loss), 2)
}
```

# رسم الشارت

def create_chart(data: Dict, analysis: Dict):
“”“إنشاء شارت تفاعلي”””
if not PLOTLY_AVAILABLE:
return None

```
hist = data['history'].tail(30)

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=hist.index,
    open=hist['Open'],
    high=hist['High'],
    low=hist['Low'],
    close=hist['Close'],
    name='السعر'
))

fig.add_hline(y=data['support'], line_dash="dash", line_color="green", 
              annotation_text=f"الدعم: ${data['support']:.2f}")
fig.add_hline(y=data['resistance'], line_dash="dash", line_color="red",
              annotation_text=f"المقاومة: ${data['resistance']:.2f}")

fig.update_layout(
    title=f"{data['symbol']} - آخر 30 يوم",
    yaxis_title="السعر ($)",
    xaxis_title="التاريخ",
    height=500,
    showlegend=False
)

return fig
```

# الواجهة الرئيسية

def main():
“”“الواجهة الرئيسية”””

```
st.markdown('<h1 class="main-header">📈 محلل الأسهم الأمريكية الاحترافي</h1>', 
            unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ الإعدادات")
    
    symbol = st.text_input(
        "🔤 رمز السهم",
        placeholder="مثال: AAPL",
        help="أدخل رمز السهم الأمريكي"
    ).upper()
    
    analyze_btn = st.button("🚀 تحليل الآن", use_container_width=True)
    
    st.divider()
    
    st.markdown("### ⚡ أمثلة سريعة")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("AAPL", use_container_width=True):
            st.session_state.symbol = "AAPL"
            st.rerun()
        if st.button("NVDA", use_container_width=True):
            st.session_state.symbol = "NVDA"
            st.rerun()
    with col2:
        if st.button("TSLA", use_container_width=True):
            st.session_state.symbol = "TSLA"
            st.rerun()
        if st.button("MSFT", use_container_width=True):
            st.session_state.symbol = "MSFT"
            st.rerun()
    
    st.divider()
    
    st.markdown("### 💡 معلومات")
    ai_status = "🤖 مفعّل" if USE_AI_ANALYSIS else "⚡ غير مفعّل"
    st.info(f"**التحليل الذكي:** {ai_status}")
    st.success("**مصدر البيانات:** Yahoo Finance")
    
    st.divider()
    st.warning("⚠️ **تنبيه:** هذا التحليل لأغراض تعليمية فقط.")

# المحتوى الرئيسي
if 'symbol' in st.session_state:
    symbol = st.session_state.symbol
    del st.session_state.symbol
    analyze_btn = True

if not symbol:
    st.markdown("""
    ## 🎯 مرحباً بك في محلل الأسهم الاحترافي
    
    ### ✨ المميزات:
    - 📊 بيانات حية من Yahoo Finance
    - 📈 تحليل فني متقدم
    - 💰 إدارة مخاطر احترافية
    - 📰 آخر الأخبار
    - 🤖 تحليل ذكي بواسطة Claude AI (اختياري)
    - 📉 رسوم بيانية تفاعلية
    
    ### 🚀 كيفية الاستخدام:
    1. أدخل رمز السهم في الشريط الجانبي
    2. اضغط "تحليل الآن"
    3. شاهد التحليل الشامل!
    """)
    
    st.markdown("### 📊 أمثلة شائعة:")
    cols = st.columns(4)
    examples = [
        ("AAPL", "Apple", "🍎"),
        ("TSLA", "Tesla", "🚗"),
        ("NVDA", "NVIDIA", "💻"),
        ("MSFT", "Microsoft", "🪟")
    ]
    for col, (sym, name, emoji) in zip(cols, examples):
        with col:
            st.metric(label=f"{emoji} {name}", value=sym)
    
    return

if analyze_btn:
    with st.spinner(f"⏳ جاري تحليل {symbol}..."):
        data = get_stock_data(symbol)
    
    if "error" in data:
        st.error(f"❌ {data['error']}")
        st.info("**الحلول:** تأكد من صحة رمز السهم (AAPL وليس APPLE)")
        return
    
    # عرض النتائج
    st.markdown(f"## 💵 [{data['symbol']}] - {data['name']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if data['change'] >= 0 else "inverse"
        st.metric(
            label="السعر الحالي",
            value=f"${data['current_price']:.2f}",
            delta=f"{data['change_percent']:+.2f}%",
            delta_color=delta_color
        )
    
    with col2:
        st.metric(
            label="After Hours",
            value=f"${data['post_price']:.2f}",
            delta=f"{data['post_change']:+.2f}"
        )
    
    with col3:
        st.metric(
            label="الفوليوم",
            value=f"{data['volume']:,}",
            delta=f"{data['volume_ratio']:.2f}x"
        )
    
    with col4:
        st.metric(
            label="القطاع",
            value=data['sector']
        )
    
    st.divider()
    
    # التحليل
    analysis = traditional_analysis(data)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 التحليل الفني", "💰 إدارة المخاطر", "📈 الرسم البياني", "📰 الأخبار"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 المستويات الفنية")
            
            levels_df = pd.DataFrame({
                "المستوى": ["الدعم", "السعر الحالي", "المقاومة", "أعلى 52 أسبوع", "أقل 52 أسبوع"],
                "القيمة": [
                    f"${data['support']:.2f}",
                    f"${data['current_price']:.2f}",
                    f"${data['resistance']:.2f}",
                    f"${data['high_52w']:.2f}",
                    f"${data['low_52w']:.2f}"
                ]
            })
            st.dataframe(levels_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 🔍 التحليل")
            st.markdown(f"**الفوليوم:** {analysis['volume_status']}")
            st.markdown(f"**Bag Holders:** {'⚠️ نعم' if analysis['bag_holders'] else '✅ لا'}")
            st.markdown(f"**Reverse Split:** {'✅ نعم' if data['reverse_split'] else '❌ لا'}")
            st.markdown(f"**نسبة المخاطرة للعائد:** 1:{analysis['risk_reward']}")
    
    with tab2:
        st.markdown("### 💰 نقاط التداول")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🎯 الدخول المثالي", f"${analysis['entry']:.2f}")
        
        with col2:
            near_pct = ((analysis['target_near']/analysis['entry']-1)*100)
            st.metric("🎯 الهدف القريب", f"${analysis['target_near']:.2f}", 
                     delta=f"+{near_pct:.1f}%")
        
        with col3:
            far_pct = ((analysis['target_far']/analysis['entry']-1)*100)
            st.metric("🎯 الهدف البعيد", f"${analysis['target_far']:.2f}",
                     delta=f"+{far_pct:.1f}%")
        
        with col4:
            stop_pct = ((1-analysis['stop_loss']/analysis['entry'])*100)
            st.metric("🛑 وقف الخسارة", f"${analysis['stop_loss']:.2f}",
                     delta=f"-{stop_pct:.1f}%", delta_color="inverse")
        
        st.divider()
        
        st.markdown("### 🎯 التوصية النهائية")
        
        if "🟢" in analysis['recommendation']:
            st.success(f"# {analysis['recommendation']}\n\n**السبب:** {analysis['reason']}")
            st.markdown("""
            #### ✅ خطة التنفيذ:
            1. ضع أمر شراء عند السعر المثالي
            2. ضع هدف أول عند الهدف القريب
            3. ضع هدف ثاني عند الهدف البعيد
            4. **وقف الخسارة الصارم** عند المستوى المحدد
            5. لا تتجاوز **5% من رأس مالك**
            """)
        elif "🟡" in analysis['recommendation']:
            st.warning(f"# {analysis['recommendation']}\n\n**السبب:** {analysis['reason']}")
            st.info("💡 راقب السهم عن قرب")
        else:
            st.error(f"# {analysis['recommendation']}\n\n**السبب:** {analysis['reason']}")
            st.error("⚠️ لا تدخل حالياً")
        
        # تحليل AI
        if USE_AI_ANALYSIS:
            st.divider()
            st.markdown("### 🤖 تحليل AI بواسطة Claude")
            with st.spinner("جاري التحليل الذكي..."):
                ai_insight = analyze_with_claude(data)
                if ai_insight:
                    st.info(ai_insight)
    
    with tab3:
        st.markdown("### 📈 الشارت التفاعلي")
        if PLOTLY_AVAILABLE:
            fig = create_chart(data, analysis)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("تثبيت plotly لعرض الرسوم البيانية: pip install plotly")
    
    with tab4:
        st.markdown("### 📰 آخر الأخبار")
        
        if data['news']:
            for i, article in enumerate(data['news'], 1):
                with st.expander(f"📰 {article['title']}"):
                    st.markdown(f"**المصدر:** {article['publisher']}")
                    st.markdown(f"**منذ:** {article['hours_ago']} ساعة")
        else:
            st.info("لا توجد أخبار حديثة")
    
    st.divider()
    st.caption(f"آخر تحديث: {datetime.now().strftime('%d %B %Y - %H:%M UTC')}")
    st.caption("⚠️ هذا التحليل لأغراض تعليمية فقط")
```

if **name** == “**main**”:
main()
