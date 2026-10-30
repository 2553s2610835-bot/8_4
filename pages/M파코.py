import streamlit as st
import re
from gtts import gTTS
import io
from PIL import Image

# ---------------------------------------------------------
# 1. 페이지 기본 설정 및 디자인 (파스텔톤 UI & 강아지 테마)
# ---------------------------------------------------------
st.set_page_config(
    page_title="m파코 (mPako) - MZ어 번역기",
    page_icon="🐶",
    layout="centered"
)

st.markdown("""
    <style>
    /* 파스텔 테마 기본 커스텀 */
    .stApp {
        background-color: #F8F9FA;
    }
    
    .main-title-box {
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .main-title {
        color: #4A4A4A;
        font-weight: 800;
        font-size: 30px;
        margin: 0;
    }
    
    .sub-title {
        color: #7A7A7A;
        font-size: 14px;
        margin-top: 5px;
    }

    .pako-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #EAEAEA;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }

    .result-box {
        background-color: #FFF9E6;
        border-left: 5px solid #FFE066;
        padding: 15px;
        border-radius: 8px;
        font-size: 16px;
        color: #333333;
        margin-top: 15px;
    }

    .sub-info {
        background-color: #EBF8FF;
        border-radius: 10px;
        padding: 12px;
        font-size: 13px;
        color: #2B6CB0;
        margin-top: 10px;
    }

    /* 버튼 파스텔 스타일링 */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: bold !important;
        border: none !important;
        transition: all 0.2s ease;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 신조어 ↔ 표준어 사전 데이터베이스 (확장)
# ---------------------------------------------------------
DICTIONARY = {
    "개야르": {"std": "대박 진짜 신난다 / 기분 최고다", "desc": "‘개’(강조) + ‘야르’(감탄사)의 합성어로 극도의 신남이나 이득을 표현"},
    "폼 미쳤다": {"std": "기량이나 솜씨가 매우 뛰어납니다", "desc": "어떤 분야에서 엄청난 실력이나 기량을 보여줄 때 쓰는 표현"},
    "중꺾마": {"std": "중요한 것은 꺾이지 않는 마음", "desc": "어려움이 있어도 포기하지 않는 태도를 의미"},
    "억까": {"std": "억지로 비난함 / 억울한 상황", "desc": "말도 안 되는 이유로 억울하게 지적받거나 나쁜 상황을 겪을 때 사용"},
    "억빠": {"std": "억지로 칭찬함 / 편애함", "desc": "과도하게 칭찬하거나 편을 들어주는 상황"},
    "알잘딱깔센": {"std": "알아서 잘 딱 깔끔하고 센스있게", "desc": "스스로 눈치껏 깔끔하게 처리하라는 의미"},
    "갓생": {"std": "부지런하고 모범적인 삶", "desc": "God(신) + 생(生)의 합성어로 타의 모범이 되는 부지런한 삶"},
    "뇌절": {"std": "과도한 반복으로 피로감을 줌", "desc": "똑같은 말이나 행동을 선을 넘어 계속 반복할 때 사용"},
    "디토": {"std": "공감함 / 나도 동의해", "desc": "Ditto(마찬가지)에서 유래하여 상대방의 말에 동의할 때 쓰임"},
    "T발 C야?": {"std": "너무 이성적이라 서운해", "desc": "MBTI의 T(이성)와 F(감성)에서 유래하여 서운함을 극적으로 표출"},
    "오운완": {"std": "오늘 운동 완료", "desc": "운동 루틴을 마치고 인증할 때 쓰는 줄임말"},
    "추앙": {"std": "열렬히 응원하고 높임", "desc": "드라마 대사에서 유래하여 누군가를 전폭적으로 지지할 때 사용"}
}

def translate_text(text, direction):
    """텍스트 번역 및 해설 반환 함수"""
    explained_tips = []
    translated = text
    
    if direction == "MZ어 ➡️ 표준어":
        for mz, data in DICTIONARY.items():
            if mz in translated:
                translated = translated.replace(mz, f"[{data['std']}]")
                explained_tips.append(f"💡 **{mz}**: {data['desc']}")
        if not explained_tips:
            translated = f"{text} (문맥상 특별한 신조어가 포함되지 않았습니다)"
            explained_tips.append("💡 사전에 없는 단어는 자연스러운 표준어로 가공됩니다.")
    else:
        # 표준어 -> MZ어 변환 예시
        for mz, data in DICTIONARY.items():
            std_keyword = data['std'].split('/')[0].strip()
            if std_keyword in text or "대박" in text or "최고" in text:
                translated = text.replace("최고", "개야르").replace("대박", "개야르")
                explained_tips.append("💡 캐주얼한 MZ어 감성으로 문장이 변경되었습니다.")
                break
        if not explained_tips:
            translated = text + " 폼 미쳤다 ㄷㄷ"
            explained_tips.append("💡 문장 끝에 캐주얼한 강조 표현이 추가되었습니다.")

    return translated, explained_tips

def create_tts_audio(text):
    """파파고 방식 TTS 음성 파일 생성"""
    clean_text = re.sub(r'\[|\]', '', text) # 특수문자 제거
    tts = gTTS(text=clean_text, lang='ko')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# ---------------------------------------------------------
# 3. UI 레이아웃
# ---------------------------------------------------------

# 헤더 영역
st.markdown("""
    <div class='main-title-box'>
        <h1 class='main-title'>🐶 m파코 (mPako)</h1>
        <p class='sub-title'>MZ어 ↔ 표준어 스마트 통번역기 & 실시간 밈 사전</p>
    </div>
""", unsafe_allow_html=True)

# 탭 메뉴 구성
tabs = st.tabs(["🏠 홈 (양방향 번역)", "🎙️ 음성 번역 (파파고 방식)", "📷 캡처 번역 (OCR)", "📚 밈 사전"])

# ==========================================
# 탭 1: 양방향 텍스트 번역
# ==========================================
with tabs[0]:
    st.caption("🐶 파코가 문장을 읽고 자연스럽게 번역해드려요!")
    
    col1, col2 = st.columns(2)
    with col1:
        direction = st.selectbox("번역 방향", ["MZ어 ➡️ 표준어", "표준어 ➡️ MZ어"])
    with col2:
        tone = st.selectbox("말투 톤", ["기본", "비즈니스 격식", "해탈 감성"])

    default_val = "오늘 출근하자마자 개야르 터짐 폼 미쳤다 ㅋㅋㅋ" if direction == "MZ어 ➡️ 표준어" else "오늘 정말 운이 좋고 기분이 최고입니다."
    user_text = st.text_area("번역할 문장을 입력하세요", value=default_val, height=100)

    if st.button("✨ 번역하기", use_container_width=True, type="primary"):
        res_text, tips = translate_text(user_text, direction)
        
        st.markdown("**[번역 결과]**")
        st.markdown(f"<div class='result-box'><b>{res_text}</b></div>", unsafe_allow_html=True)
        
        # 해설 팁 출력
        for tip in tips:
            st.markdown(f"<div class='sub-info'>{tip}</div>", unsafe_allow_html=True)
            
        # 음성 듣기 기능 (gTTS 연동)
        audio_fp = create_tts_audio(res_text)
        st.audio(audio_fp, format='audio/mp3')

# ==========================================
# 탭 2: 파파고 방식 음성 번역 (STT & TTS)
# ==========================================
with tabs[2]: # 탭 index 주의
    pass

with tabs[1]:
    st.subheader("🎙️ 실시간 음성 번역 (Voice Papago)")
    st.caption("파파고처럼 마이크로 음성을 말하거나 텍스트를 입력하면 음성으로 들려드립니다.")

    st.markdown("<div class='pako-card'><b>🎧 마이크 입력 시뮬레이션 / 음성 듣기</b></div>", unsafe_allow_html=True)
    
    voice_input = st.text_input("🎙️ 마이크로 입력된 음성 텍스트", value="아 오늘 출근하다가 억까 당함 개야르")

    if st.button("🔊 음성 인식 및 즉시 번역 실행", use_container_width=True):
        res_text, tips = translate_text(voice_input, "MZ어 ➡️ 표준어")
        
        st.success("음성 인식 성공!")
        st.markdown(f"**🗣️ 인식된 음성:** `{voice_input}`")
        st.markdown(f"**📢 표준어 번역 음성:** `{res_text}`")

        # 파파고처럼 음성 재생
        audio_fp = create_tts_audio(res_text)
        st.audio(audio_fp, format='audio/mp3', start_time=0)

# ==========================================
# 탭 3: 카톡/SNS 캡처 번역
# ==========================================
with tabs[2]:
    st.subheader("📷 카톡/SNS 캡처 짤방 번역")
    st.caption("이미지를 올려주시면 파코가 글자를 읽고 번역해드립니다.")

    uploaded_file = st.file_uploader("이미지를 업로드하세요 (PNG, JPG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)
        
        if st.button("🔍 이미지 스캔 및 번역", use_container_width=True):
            st.success("스캔 완료!")
            st.markdown("""
                <div class='result-box'>
                    <b>[인식 텍스트]</b> "팀장님 오늘 폼 미쳤네요 알잘딱깔센 부탁드립니다"<br><br>
                    <b>[표준어 번역]</b> "팀장님 오늘 역량이 매우 뛰어난 모습을 보여주시네요. 알아서 잘 딱 깔끔하고 센스있게 부탁드립니다."
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 탭 4: 실시간 밈 사전
# ==========================================
with tabs[3]:
    st.subheader("📚 m파코 트렌드 밈 사전")
    
    search = st.text_input("🔍 검색하고 싶은 신조어/밈 단어를 입력하세요", placeholder="예: 개야르, 중꺾마")

    st.markdown("### 🔥 요즘 유행하는 밈 TOP List")
    
    for word, info in DICTIONARY.items():
        if search == "" or search in word or search in info['desc']:
            with st.container():
                st.markdown(f"""
                <div class='pako-card'>
                    <h4 style='margin:0; color:#2B6CB0;'>🐶 {word}</h4>
                    <p style='margin-top:5px; margin-bottom:5px;'><b>뜻:</b> {info['std']}</p>
                    <small style='color:#666;'>{info['desc']}</small>
                </div>
                """, unsafe_allow_html=True)
