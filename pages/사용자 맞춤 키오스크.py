import streamlit as st
import os

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="맞춤형 카페 키오스크",
    page_icon="☕",
    layout="wide"
)

# --- 2. Gemini API 설정 (gemini-2.5-flash-lite) ---
gemini_available = False
try:
    import google.generativeai as genai
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        gemini_available = True
except Exception:
    gemini_available = False

# --- 3. 세션 상태 초기화 ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'age_group' not in st.session_state:
    st.session_state.age_group = "👵 어르신 쉬운 모드 (60대 이상)"

# --- 4. 공통 카페 메뉴 데이터 ---
COMMON_MENU_DATABASE = {
    "☕ 커피류": {
        "따뜻한 아메리카노": 3000,
        "아이스 아메리카노": 3000,
        "따뜻한 카페 라떼": 4000,
        "바닐라 빈 라떼": 4500,
        "디카페인 커피": 3500,
        "시그니처 크림라떼": 5200
    },
    "🍵 건강차 & 음료": {
        "건강 한방 쌍화차": 5000,
        "알싸한 생강차": 4500,
        "달콤 유자차": 4000,
        "구수한 둥굴레차": 3000,
        "생자몽 에이드": 4800,
        "리얼 생딸기 라떼": 4800
    },
    "🍰 디저트 & 빵": {
        "부드러운 카스테라": 3500,
        "달콤한 단팥빵": 2800,
        "플레인 크로플": 3800,
        "버터 소금빵": 3200,
        "치즈 케이크": 5500
    }
}

# --- 5. 연령별 UI & 스타일 설정 ---
AGE_CONFIG = {
    "👵 어르신 쉬운 모드 (60대 이상)": {
        "badge": "👵 어르신을 위한 큰 글씨 모드",
        "title_size": "42px",
        "sub_size": "28px",
        "text_size": "24px",
        "btn_padding": "20px 30px",
        "btn_size": "26px",
        "sidebar_size": "24px",
        "theme_color": "#1B5E20",
        "bg_color": "#FFFDE7",
        "welcome": "어르신, 반갑습니다! 천천히 보고 편하게 눌러주세요.",
        "voice_guide": "어르신, 잘 오셨습니다. 원하시는 차나 빵을 크고 편한 버튼으로 눌러서 선택해 보세요.",
        "recommended": [
            {"name": "따뜻한 아메리카노", "price": 3000, "desc": "속이 깔끔하고 따뜻한 기본 커피"},
            {"name": "건강 한방 쌍화차", "price": 5000, "desc": "견과류가 들어간 따뜻한 건강차"},
            {"name": "부드러운 카스테라", "price": 3500, "desc": "입에서 녹는 촉촉하고 부드러운 빵"}
        ]
    },
    "🧑 청년/장년 모드 (20~50대)": {
        "badge": "⚡ 빠른 스피드 모드",
        "title_size": "28px",
        "sub_size": "20px",
        "text_size": "16px",
        "btn_padding": "10px 16px",
        "btn_size": "16px",
        "sidebar_size": "18px",
        "theme_color": "#1565C0",
        "bg_color": "#F8F9FA",
        "welcome": "원하시는 메뉴를 빠르고 간편하게 선택하세요.",
        "voice_guide": "에스프레소부터 에이드, 디저트까지 빠르게 주문하실 수 있습니다.",
        "recommended": [
            {"name": "아이스 아메리카노", "price": 3000, "desc": "고소하고 깔끔한 원두 에스프레소"},
            {"name": "시그니처 크림라떼", "price": 5200, "desc": "부드러운 수제 크림 라떼"},
            {"name": "버터 소금빵", "price": 3200, "desc": "고소한 풍미의 바삭한 소금빵"}
        ]
    },
    "🎈 어린이 모드 (10대 미만)": {
        "badge": "🎈 어린이 맞춤 모드",
        "title_size": "32px",
        "sub_size": "22px",
        "text_size": "18px",
        "btn_padding": "12px 20px",
        "btn_size": "18px",
        "sidebar_size": "20px",
        "theme_color": "#E65100",
        "bg_color": "#FFF8E1",
        "welcome": "안녕! 달콤한 딸기 라떼와 맛있는 빵을 골라볼까?",
        "voice_guide": "어린이 손님 환영해요! 달콤하고 신나는 추천 메뉴를 골라보세요.",
        "recommended": [
            {"name": "리얼 생딸기 라떼", "price": 4800, "desc": "달콤한 딸기가 씹히는 인기 음료"},
            {"name": "플레인 크로플", "price": 3800, "desc": "바삭하고 달콤한 인기 디저트"},
            {"name": "달콤 유자차", "price": 4000, "desc": "새콤달콤 따뜻한 차"}
        ]
    }
}

# --- 6. 사이드바 (모드 선택 및 화면 이동) ---
st.sidebar.title("⚙️ 키오스크 설정")
selected_age = st.sidebar.radio(
    "👤 연령대 모드 선택",
    list(AGE_CONFIG.keys()),
    index=list(AGE_CONFIG.keys()).index(st.session_state.age_group)
)
st.session_state.age_group = selected_age

page = st.sidebar.radio(
    "📍 화면 이동",
    ["1. 맞춤 시작 & 음성 가이드", "2. 전체 카페 메뉴 주문", "3. 간소화 결제 및 직원 호출"]
)

config = AGE_CONFIG[st.session_state.age_group]

# --- 7. 어르신 모드 전용 동적 CSS (글씨, 버튼, 사이드바 크기 확대) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {config['bg_color']};
    }}
    .custom-title {{
        font-size: {config['title_size']};
        font-weight: 800;
        color: {config['theme_color']};
        margin-bottom: 16px;
        line-height: 1.3;
    }}
    .custom-sub {{
        font-size: {config['sub_size']};
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 10px;
    }}
    .custom-text {{
        font-size: {config['text_size']};
        line-height: 1.6;
    }}
    /* 버튼 초대형화 */
    .stButton > button {{
        font-size: {config['btn_size']} !important;
        font-weight: bold !important;
        padding: {config['btn_padding']} !important;
        border-radius: 16px !important;
        border: 2px solid {config['theme_color']} !important;
        width: 100% !important;
        margin-top: 6px !important;
        margin-bottom: 6px !important;
    }}
    /* 사이드바 글자 크기 확대 */
    section[data-testid="stSidebar"] div {{
        font-size: {config['sidebar_size']} !important;
    }}
    section[data-testid="stSidebar"] label {{
        font-size: {config['sidebar_size']} !important;
        font-weight: bold !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 8. 페이지 1: 맞춤 시작 & 음성 가이드 ---
if page == "1. 맞춤 시작 & 음성 가이드":
    st.markdown(f"<span style='background-color:{config['theme_color']}; color:white; padding:8px 18px; border-radius:24px; font-size:{config['text_size']}; font-weight:bold;'>{config['badge']}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-title' style='margin-top:15px;'>{config['welcome']}</div>", unsafe_allow_html=True)
    
    st.info(f"🔊 **[맞춤형 음성 가이드]**\n\n\"{config['voice_guide']}\"")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='custom-sub'>💡 현재 적용된 맞춤 서비스</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='custom-text'>
        - <b>선택 모드:</b> {st.session_state.age_group}<br>
        - <b>선택 버튼:</b> 터치하기 편한 대형 버튼 제공<br>
        - <b>인기 추천:</b> 연령대별 자주 찾는 메뉴 상단 자동 노출
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='custom-sub'>🤖 AI 음성 도우미</div>", unsafe_allow_html=True)
        if gemini_available:
            user_question = st.text_input("질문하세요 (예: 속 편한 차 추천해 줘, 부드러운 빵은 뭐야?)")
            if user_question:
                try:
                    prompt = f"""
                    당신은 친절한 카페 AI 도우미입니다.
                    현재 손님 연령층: {st.session_state.age_group}
                    질문: "{user_question}"
                    
                    손님 연령층에 맞는 친절한 어조로 2문장 이내로 답변해 주세요.
                    """
                    response = model.generate_content(prompt)
                    st.success(f"🤖 **AI 답변:** {response.text}")
                except Exception:
                    st.warning("AI 도우미 응답 중 잠시 오류가 발생했습니다.")
        else:
            st.caption("※ GEMINI_API_KEY 설정 시 AI 맞춤 안내가 활성화됩니다.")

    st.markdown("---")
    st.success("👈 메뉴를 선택하시려면 사이드바에서 **'2. 전체 카페 메뉴 주문'**을 눌러주세요.")

# --- 9. 페이지 2: 전체 카페 메뉴 주문 ---
elif page == "2. 전체 카페 메뉴 주문":
    st.markdown(f"<div class='custom-title'>⭐ 맞춤 추천 메뉴</div>", unsafe_allow_html=True)
    st.markdown("<div class='custom-text'>자주 찾으시는 추천 메뉴입니다. 버튼을 누르면 장바구니에 담깁니다.</div>", unsafe_allow_html=True)
    
    rec_cols = st.columns(len(config['recommended']))
    for idx, item in enumerate(config['recommended']):
        with rec_cols[idx]:
            st.markdown(f"<div class='custom-sub'>{item['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='custom-text'>{item['desc']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='custom-sub' style='color:{config['theme_color']};'>{item['price']:,}원</div>", unsafe_allow_html=True)
            if st.button(f"➕ {item['name']} 담기", key=f"rec_{idx}"):
                st.session_state.cart.append({"name": item['name'], "price": item['price']})
                st.toast(f"'{item['name']}' 담기 완료!")

    st.markdown("---")
    
    st.markdown("<div class='custom-title'>☕ 전체 카테고리 메뉴</div>", unsafe_allow_html=True)
    
    cat_names = list(COMMON_MENU_DATABASE.keys())
    tabs = st.tabs(cat_names)
    
    for tab_idx, cat_name in enumerate(cat_names):
        with tabs[tab_idx]:
            items = COMMON_MENU_DATABASE[cat_name]
            item_cols = st.columns(2)
            for item_idx, (item_name, price) in enumerate(items.items()):
                c_idx = item_idx % 2
                with item_cols[c_idx]:
                    st.markdown(f"<div class='custom-sub'>{item_name} — {price:,}원</div>", unsafe_allow_html=True)
                    if st.button(f"선택하기 ({item_name})", key=f"cat_{tab_idx}_{item_idx}"):
                        st.session_state.cart.append({"name": item_name, "price": price})
                        st.toast(f"'{item_name}' 담기 완료!")

    st.markdown("---")
                
