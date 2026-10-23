import streamlit as st
from PIL import Image

# 1. 페이지 기본 설정 및 타이틀
st.set_page_config(
    page_title="m파코 (mPako)",
    page_icon="🐶",
    layout="centered"
)

# 기본 커스텀 CSS (모바일 앱 느낌 레이아웃 및 스타일링)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-weight: bold;
        font-size: 28px;
        margin-bottom: 20px;
    }
    .sub-info {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        font-size: 13px;
        color: #555;
        margin-top: 15px;
    }
    .card {
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        background-color: #ffffff;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 하단 Navigation 메뉴 구성 (시안 4개 탭 구조 반영)
st.markdown("<h2 class='main-title'>🐶 m파코 (mPako)</h2>", unsafe_allow_html=True)

tabs = st.tabs(["🏠 홈 (양방향)", "📷 캡처 번역", "🎙️ 음성/숏폼", "📚 사전/보관함"])


# ==========================================
# 탭 1: [홈] 양방향 텍스트 번역 (Default)
# ==========================================
with tabs[0]:
    st.caption("양방향 텍스트 번역 (MZ어 ↔ 표준어)")
    
    # 방향 및 톤 선택 UI
    col1, col2 = st.columns([1, 1])
    with col1:
        direction = st.selectbox("번역 방향", ["MZ어 ➡️ 표준어", "표준어 ➡️ MZ어"])
    with col2:
        tone = st.selectbox("톤 선택", ["비즈니스", "해탈감성", "기본"])
    
    # 입력 창
    user_text = st.text_area(
        "번역할 문장을 입력하세요", 
        value="이번 프로젝트 폼 미쳤다 ㄱㄱㄱㄱㄱ",
        height=100
    )
    
    if st.button("번역하기", use_container_width=True, type="primary"):
        st.markdown("---")
        st.markdown("**[번역 결과]**")
        
        # 예시 번역 동작 (실제 서비스 구현 시 OpenAI API 등을 연동하는 파트입니다)
        if direction == "MZ어 ➡️ 표준어":
            result_text = "이 프로젝트는 매우 뛰어난 성과를 보여주고 있습니다."
            tip_text = "💡 '폼 미쳤다'는 기량/실력이 뛰어남을 의미합니다."
        else:
            result_text = "이번 프로젝트 폼 미쳤다 ㄷㄷ"
            tip_text = "💡 진지한 어조를 캐주얼한 MZ 스타일로 변환했습니다."
            
        st.info(f"✨ {result_text}")
        
        # 하단 팁 / 보충 설명
        st.markdown(f"<div class='sub-info'>{tip_text}</div>", unsafe_allow_html=True)
        
        # 기능 버튼 (듣기, 복사, 저장, 공유 시뮬레이션)
        b1, b2, b3, b4 = st.columns(4)
        with b1: st.button("🔊 듣기")
        with b2: st.button("📋 복사")
        with b3: st.button("⭐ 저장")
        with b4: st.button("🔗 공유")


# ==========================================
# 탭 2: 카톡 / SNS 캡처 번역 (OCR)
# ==========================================
with tabs[1]:
    st.subheader("카톡/SNS 캡처 번역")
    st.caption("카톡, DM, 밈 짤방 이미지를 올리면 글자를 인식해 번역합니다.")
    
    uploaded_file = st.file_uploader("이미지를 업로드하세요 (카톡/DM/짤방)", type=["png", "jpg", "jpeg"])
    
    toggle_option = st.checkbox("프로필/이름 블러 처리", value=True)
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)
        
        if st.button("스캔 및 번역 실행", use_container_width=True):
            st.success("이미지 텍스트 스캔 완료!")
            st.markdown("""
            **[스캔 인식 결과]**
            > "아 뇌절 오지네..."
            
            **[표준어 번역]**
            > "동일한 말을 과도하게 반복하여 피로감을 유발하네요."
            """)

    st.markdown("---")
    st.caption("📷 최근 스캔한 이미지 목록")
    rec_col1, rec_col2, rec_col3 = st.columns(3)
    rec_col1.button("카톡 1")
    rec_col2.button("DM_02")
    rec_col3.button("짤방 1")


# ==========================================
# 탭 3: Voice 음성 / 숏폼 번역
# ==========================================
with tabs[2]:
    st.subheader("실시간 음성 / 숏폼 번역")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.button("📱 플로팅 오버레이", use_container_width=True)
    with m_col2:
        st.button("💬 대화 모드", use_container_width=True)
        
    st.markdown("---")
    
    # 음성 인식 상태 표시 시뮬레이션
    is_listening = st.toggle("🎙️ 실시간 번역 시작 / 정지", value=False)
    
    if is_listening:
        st.warning("🎧 음성을 수집/분석하고 있습니다...")
        
        st.markdown("<div class='card'><b>[인식된 음성]</b><br>'아 오늘 출근하자마자 억까 당해서 게임터짐ㅠ'</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><b>[실시간 해석]</b><br>'오늘 출근 직후 억울한 상황을 겪어서 업무 진행이 매우 차질을 빚고 있습니다.'</div>", unsafe_allow_html=True)
    else:
        st.info("버튼을 켜면 실시간 자막 번역이 시작됩니다.")


# ==========================================
# 탭 4: [사전] 보관함 & 실시간 밈 사전
# ==========================================
with tabs[3]:
    st.subheader("📚 보관함 & 실시간 밈 사전")
    
    search_query = st.text_input("🔍 신조어 / 밈 단어 검색", placeholder="예: 중꺾마, 폼 미쳤다")
    
    sub_tab1, sub_tab2 = st.tabs(["⭐ 즐겨찾기 밀억", "🔥 요즘 트렌드 밈 TOP 10"])
    
    with sub_tab1:
        st.write("보관한 단어가 없습니다.")
        
    with sub_tab2:
        st.markdown("### 🔥 오늘 많이 검색된 MZ어")
        
        memes = [
            ("1. 중꺾마", "중요한 것은 꺾이지 않는 마음"),
            ("2. 폼 미쳤다", "기량이나 솜씨가 매우 뛰어남"),
            ("3. 억까", "억지로 까기 (억울하게 당하거나 나쁜 상황)"),
            ("4. T발 C야?", "이성적(T)인 반응에 대해 서운함을 표할 때 쓰는 표현")
        ]
        
        for title, desc in memes:
            with st.container():
                c1, c2 = st.columns([4, 1])
                c1.markdown(f"**{title}**\n- {desc}")
                c2.button("⭐", key=title)
                st.markdown("---")
