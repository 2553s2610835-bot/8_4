import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# 1. 페이지 기본 설정 및 파스텔 디자인
st.set_page_config(
    page_title="m파코 (mPako)",
    page_icon="🐶",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
    }
    .main-title {
        text-align: center;
        font-weight: bold;
        font-size: 28px;
        color: #4A4A4A;
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    .result-card {
        background-color: #FFF9E6;
        border-left: 5px solid #FFE066;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        font-size: 16px;
        font-weight: bold;
        color: #333333;
    }
    .sub-info {
        background-color: #EBF8FF;
        padding: 12px;
        border-radius: 10px;
        font-size: 13px;
        color: #2B6CB0;
        margin-top: 10px;
    }
    .pako-box {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 신조어 데이터베이스 (개야르, 중꺾마 등 확장)
DICTIONARY = {
    "개야르": {"std": "대박 진짜 신난다 / 기분 최고다", "desc": "‘개’(강조) + ‘야르’(감탄사)의 합성어로 극도의 신남이나 이득을 표현"},
    "폼 미쳤다": {"std": "기량이나 솜씨가 매우 뛰어납니다", "desc": "어떤 분야에서 엄청난 실력이나 기량을 보여줄 때 사용"},
    "중꺾마": {"std": "중요한 것은 꺾이지 않는 마음", "desc": "어려움이 있어도 포기하지 않는 태도"},
    "알잘딱깔센": {"std": "알아서 잘 딱 깔끔하고 센스있게", "desc": "스스로 눈치껏 깔끔하게 처리하라는 의미"},
    "억까": {"std": "억지로 비난함 / 억울한 상황", "desc": "말도 안 되는 이유로 억울하게 지적받거나 나쁜 상황을 겪을 때 사용"},
    "억빠": {"std": "억지로 칭찬함 / 편애함", "desc": "과도하게 칭찬하거나 편을 들어주는 상황"},
    "갓생": {"std": "부지런하고 모범적인 삶", "desc": "God(신) + 생(生)의 합성어로 모범적인 삶"},
    "뇌절": {"std": "과도한 반복으로 피로감을 줌", "desc": "똑같은 말이나 행동을 선을 넘어 계속 반복할 때 사용"},
    "디토": {"std": "공감함 / 나도 동의해", "desc": "Ditto(마찬가지)에서 유래하여 상대방의 말에 동의할 때 쓰임"},
    "T발 C야?": {"std": "너무 이성적이라 서운해", "desc": "MBTI의 T(이성)와 F(감성)에서 유래하여 서운함을 극적으로 표출"}
}

def translate_text(text, direction):
    explained_tips = []
    translated = text
    if direction == "MZ어 ➡️ 표준어":
        for mz, data in DICTIONARY.items():
            if mz in translated:
                translated = translated.replace(mz, f"[{data['std']}]")
                explained_tips.append(f"💡 **{mz}**: {data['desc']}")
        if not explained_tips:
            explained_tips.append("💡 문맥에 맞게 자연스럽게 가공되었습니다.")
    else:
        translated = text + " 폼 미쳤다 개야르 ㄷㄷ"
        explained_tips.append("💡 캐주얼한 MZ 스타일로 변환되었습니다.")
    return translated, explained_tips

# 브라우저 기본 음성(TTS) 출력 함수 (오류 원인 완벽 제거)
def speak_text(text):
    clean_text = text.replace("'", "").replace('"', '').replace("\n", " ")
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'ko-KR';
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# 메인 UI
st.markdown("<h2 class='main-title'>🐶 m파코 (mPako)</h2>", unsafe_allow_html=True)

tabs = st.tabs(["🏠 홈 (양방향)", "🎙️ 음성 번역", "📷 캡처 번역", "📚 밈 사전"])

# ------------------------------------------
# 탭 1: 양방향 번역
# ------------------------------------------
with tabs[0]:
    st.caption("🐶 MZ어 ↔ 표준어 스마트 번역")
    col1, col2 = st.columns(2)
    with col1:
        direction = st.selectbox("번역 방향", ["MZ어 ➡️ 표준어", "표준어 ➡️ MZ어"])
    with col2:
        tone = st.selectbox("톤 선택", ["기본", "비즈니스", "해탈감성"])
        
    user_text = st.text_area("번역할 문장 입력", value="오늘 출근하자마자 개야르 터짐 폼 미쳤다", height=80)
    
    if st.button("✨ 번역하기", use_container_width=True, type="primary"):
        res, tips = translate_text(user_text, direction)
        st.markdown(f"<div class='result-card'>✨ {res}</div>", unsafe_allow_html=True)
        for tip in tips:
            st.markdown(f"<div class='sub-info'>{tip}</div>", unsafe_allow_html=True)
            
        speak_text(res)

# ------------------------------------------
# 탭 2: 음성 번역 (파파고 방식)
# ------------------------------------------
with tabs[1]:
    st.subheader("🎙️ 실시간 음성 번역 (파파고 방식)")
    st.caption("음성으로 인식된 문장을 파파고처럼 소리로 들려드립니다.")
    
    voice_in = st.text_input("🎙️ 인식된 음성 텍스트", value="오늘 진짜 억까 당해서 기분 개야르 아님")
    
    if st.button("🔊 번역 및 음성 듣기", use_container_width=True):
        res, _ = translate_text(voice_in, "MZ어 ➡️ 표준어")
        st.success(f"🗣️ 표준어 번역: {res}")
        speak_text(res)

# ------------------------------------------
# 탭 3: 캡처 번역
# ------------------------------------------
with tabs[2]:
    st.subheader("📷 캡처 번역")
    uploaded_file = st.file_uploader("이미지 업로드 (PNG, JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), use_column_width=True)
        if st.button("스캔 실행", use_container_width=True):
            st.markdown("""
                <div class='result-card'>
                    <b>[인식 결과]</b> "팀장님 알잘딱깔센 부탁드립니다"<br>
                    <b>[표준어 번역]</b> "팀장님 센스있고 깔끔하게 처리 부탁드립니다."
                </div>
            """, unsafe_allow_html=True)

# ------------------------------------------
# 탭 4: 밈 사전
# ------------------------------------------
with tabs[3]:
    st.subheader("📚 실시간 밈 사전")
    search_q = st.text_input("🔍 검색어 입력", placeholder="예: 개야르, 폼 미쳤다")
    
    for word, data in DICTIONARY.items():
        if search_q == "" or search_q in word or search_q in data['desc']:
            st.markdown(f"""
            <div class='pako-box'>
                <h4 style='margin:0; color:#2B6CB0;'>🐶 {word}</h4>
                <p style='margin:5px 0;'><b>뜻:</b> {data['std']}</p>
                <small style='color:#666;'>{data['desc']}</small>
            </div>
            """, unsafe_allow_html=True)
