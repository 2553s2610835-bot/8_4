import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="mPako (m파코)",
    page_icon="🐶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 커스텀 CSS (모바일 스타일 및 깔끔한 UI 적용)
st.markdown("""
<style>
    /* 전체 배경 및 컨테이너 스타일 */
    .stApp {
        max-width: 450px;
        margin: 0 auto;
        border-radius: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    /* 타이틀 영역 */
    .header-title {
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        padding: 10px 0;
    }
    /* 카드/박스 스타일 */
    .custom-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #e9ecef;
    }
    /* 하단 네비게이션 바 스타일 */
    div[data-testid="stHorizontalBlock"] {
        background-color: #ffffff;
        padding: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화 (페이지 이동 관리)
if "current_page" not in st.session_state:
    st.session_state.current_page = "홈"

if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

# 앱 헤더 (상단)
st.markdown("<div class='header-title'>🐶 m파코 (mPako)</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# [화면 1] 홈 - 양방향 텍스트 번역 (Default)
# ----------------------------------------------------
if st.session_state.current_page == "홈":
    st.subheader("[홈] 양방향 텍스트 번역")
    
    # 번역 방향 및 톤 선택
    col1, col2, col3 = st.columns([1, 0.3, 1])
    with col1:
        source_lang = st.selectbox("출발", ["MZ어", "표준어"], index=0, label_visibility="collapsed")
    with col2:
        st.markdown("<h3 style='text-align: center; margin: 0;'>⇄</h3>", unsafe_allow_html=True)
    with col3:
        target_lang = st.selectbox("도착", ["표준어", "MZ어"], index=0, label_visibility="collapsed")
        
    tone = st.selectbox("톤 선택", ["비즈니스", "헤어감성", "기본"], index=0)
    
    # 입력 창
    input_text = st.text_area("번역할 텍스트 입력", value='"이번 프로젝트 폼 미쳤다 ㄱㄱㄱㄱㄱ"', height=100)
    
    if st.button("번역하기", use_container_width=True, type="primary"):
        # 예시 번역 로직
        st.session_state.translated_text = '"이 프로젝트는 매우 뛰어난 성과를 보여주고 있습니다."'
    
    # 번역 결과 표시
    translated_result = st.session_state.get("translated_text", '"이 프로젝트는 매우 뛰어난 성과를 보여주고 있습니다."')
    
    st.markdown("---")
    st.markdown(f"**번역 결과:**\n\n### {translated_result}")
    
    # 결과 액션 버튼
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
    with btn_col1:
        if st.button("🔊 듣기"): st.toast("음성을 재생합니다.")
    with btn_col2:
        if st.button("📋 복사"): st.toast("클립보드에 복사되었습니다.")
    with btn_col3:
        if st.button("⭐ 저장"): st.toast("보관함에 저장되었습니다.")
    with btn_col4:
        if st.button("🔗 공유"): st.toast("공유 링크가 생성되었습니다.")
        
    # 문맥 팁
    st.info("💡 **문맥 팁:** '폼 미쳤다'는 기량/성능이 뛰어난다는 뜻입니다.")

# ----------------------------------------------------
# [화면 2] 캡처 - 카톡/SNS 캡처 번역
# ----------------------------------------------------
elif st.session_state.current_page == "캡처":
    st.subheader("🖼️ 카톡/SNS 캡처 번역")
    
    # 이미지 업로드 영역
    uploaded_file = st.file_uploader("[📷 이미지 업로드 Area]\n카톡/DM/밀당 캡처 이미지를 올려주세요", type=["jpg", "jpeg", "png"])
    
    # 옵션 토글
    col_sw1, col_sw2 = st.columns(2)
    with col_sw1:
        st.checkbox("📋 클립보드서 선택", value=False)
    with col_sw2:
        st.checkbox("🔒 프로필/이름 훔쳐 보기 방지", value=True)
        
    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)
        if st.button("캡처 이미지 분석 및 번역", use_container_width=True, type="primary"):
            st.success("스캔 완료! 표준어로 번역되었습니다.")

    st.markdown("---")
    st.markdown("**최근 스캔**")
    scan_col1, scan_col2, scan_col3 = st.columns(3)
    with scan_col1:
        st.button("💬 카톡_1")
    with scan_col2:
        st.button("✉️ DM_02")
    with scan_col3:
        st.button("📸 팀채팅")

# ----------------------------------------------------
# [화면 3] 음성 - Voice 음성숏폼 번역
# ----------------------------------------------------
elif st.session_state.current_page == "음성":
    st.subheader("🎙️ Voice 음성숏폼 번역")
    
    # 모드 선택
    v_mode = st.radio("모드 선택", ["📱 플로팅 오버레이", "💬 대화 모드"], horizontal=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 음성 인식 상태 표시
    st.write("〰️〰️〰️〰️ (음성 수집 중...) 〰️〰️〰️〰️")
    
    st.write("**[인식된 음성]**")
    st.warning('"아 오늘 출근하자마자 억까 당해서 게임밝음^"')
    
    st.write("**[실시간 번역]**")
    st.success('"오늘 출근 직후 억울한 상항을 겪어서 매우 화가 난 상태입니다."')
    
    # 녹음 시작/정지 버튼
    if not st.session_state.is_recording:
        if st.button("🔴 실시간 번역 시작", use_container_width=True, type="primary"):
            st.session_state.is_recording = True
            st.rerun()
    else:
        if st.button("⏹️ 실시간 번역 정지", use_container_width=True):
            st.session_state.is_recording = False
            st.rerun()

# ----------------------------------------------------
# [화면 4] 사전 - 보관함 & 실시간 밈 사전
# ----------------------------------------------------
elif st.session_state.current_page == "사전":
    st.subheader("📚 보관함 & 실시간 밈 사전")
    
    # 검색창
    search_query = st.text_input("🔍 신조어 / 밈 검색어 입력", placeholder="예: 중꺾마, 억까...")
    
    # 탭 메뉴
    tab1, tab2 = st.tabs(["⭐ 즐겨찾기 단어", "🔥 요즘 트렌드 밈 TOP 10"])
    
    with tab1:
        st.write("저장한 단어 목록이 여기에 표시됩니다.")
        st.caption("- 폼 미쳤다")
        st.caption("- 억까")
        
    with tab2:
        st.markdown("**🔥 오늘 많이 검색된 MZ어**")
        
        memes = [
            {"num": 1, "title": "중꺾마", "desc": "중요한 것은 꺾이지 않는 마음"},
            {"num": 2, "title": "폼 미쳤다", "desc": "기량이 뛰어난 상태"},
            {"num": 3, "title": "억까", "desc": "억지로 비판하거나 억울한 상황"},
            {"num": 4, "title": "T발 C야", "desc": "이성적(T)인 반응에 상처받을 때 사용"},
        ]
        
        for meme in memes:
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{meme['num']}. {meme['title']}**")
                    st.caption(f"- {meme['desc']}")
                with c2:
                    st.button("⭐", key=f"star_{meme['num']}")
                st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)

# ----------------------------------------------------
# 하단 네비게이션 바 (공통 고정)
# ----------------------------------------------------
st.markdown("---")
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

with nav_col1:
    if st.button("🏠\n홈", use_container_width=True):
        st.session_state.current_page = "홈"
        st.rerun()

with nav_col2:
    if st.button("📷\n캡처", use_container_width=True):
        st.session_state.current_page = "캡처"
        st.rerun()

with nav_col3:
    if st.button("🎙️\n음성", use_container_width=True):
        st.session_state.current_page = "음성"
        st.rerun()

with nav_col4:
    if st.button("📚\n사전", use_container_width=True):
        st.session_state.current_page = "사전"
        st.rerun()
