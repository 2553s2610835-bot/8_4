import streamlit as st
import os

# --- 1. 페이지 및 기본 설정 ---
st.set_page_config(
    page_title="사용자 맞춤 키오스크",
    page_icon="🍔",
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

# --- 3. 세션 상태(Session State) 초기화 ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'age_group' not in st.session_state:
    st.session_state.age_group = "어르신 모드 (60대 이상)"

# --- 4. 연령별 UX/UI 테마 및 데이터 설정 ---
AGE_CONFIG = {
    "어린이 모드 (10대 미만)": {
        "badge": "🎈 어린이 맞춤",
        "title_size": "32px",
        "text_size": "18px",
        "theme_color": "#FF8C00",
        "bg_color": "#FFF8DC",
        "welcome": "안녕! 오늘은 어떤 맛있는 음식을 먹어볼까? 🍔",
        "voice_guide": "어린이 손님 환영해요! 달콤하고 맛있는 세트 메뉴를 추천해 줄게요.",
        "voice_speed": "밝고 경쾌한 목소리 (보통 속도)",
        "recommended": [
            {"name": "달콤 치즈버거 세트", "price": 6500, "desc": "달콤한 소스와 고소한 치즈가 듬뿍!"},
            {"name": "바삭 치킨너겟 (6조각)", "price": 3500, "desc": "어린이가 좋아하는 한입 장난감 세트"},
            {"name": "초코 쿠키 쉐이크", "price": 3000, "desc": "시원하고 달콤한 초코 쉐이크"}
        ],
        "all_menus": {
            "불고기버거": 4500,
            "감자튀김": 2000,
            "오렌지 주스": 2500,
            "치즈 스틱": 2500
        }
    },
    "청년/장년 모드 (20~50대)": {
        "badge": "⚡ 빠른 주문 모드",
        "title_size": "26px",
        "text_size": "16px",
        "theme_color": "#1E90FF",
        "bg_color": "#F4F4F4",
        "welcome": "빠르고 편리하게 원하시는 메뉴를 선택해 보세요.",
        "voice_guide": "원하시는 카테고리나 메뉴를 선택하시면 빠르게 주문이 진행됩니다.",
        "voice_speed": "명확하고 빠른 안내 (빠른 속도)",
        "recommended": [
            {"name": "더블 패티 수제버거", "price": 8500, "desc": "육즙 가득한 프리미엄 수제버거"},
            {"name": "핫 크리스피 버거 세트", "price": 7800, "desc": "매콤하고 바삭한 스파이시 세트"},
            {"name": "제로 콜라 (L)", "price": 2200, "desc": "칼로리 부담 없는 시원한 탄산"}
        ],
        "all_menus": {
            "베이컨 치즈버거": 6500,
            "아메리카노": 3000,
            "어니언 링": 3000,
            "콘샐러드": 1800
        }
    },
    "어르신 모드 (60대 이상)": {
        "badge": "👵 어르신 쉬운 모드",
        "title_size": "38px",
        "text_size": "22px",
        "theme_color": "#2E8B57",
        "bg_color": "#FFFDD0",
        "welcome": "어르신, 반갑습니다! 천천히 편하게 보고 눌러주세요.",
        "voice_guide": "어르신, 어렵지 않으시도록 차근차근 도와드리겠습니다. 마음에 드는 그림을 눌러보세요.",
        "voice_speed": "크고 또박또박한 안내 (천천히)",
        "recommended": [
            {"name": "속 편한 불고기버거", "price": 5000, "desc": "부드러운 고기와 순한 양념"},
            {"name": "따뜻한 둥굴레차", "price": 2000, "desc": "구수하고 따뜻한 건강 차"},
            {"name": "부드러운 단호박 스프", "price": 3500, "desc": "속을 편안하게 해주는 고소한 스프"}
        ],
        "all_menus": {
            "클래식 치즈버거": 4500,
            "계란 샐러드": 3500,
            "디카페인 따뜻한 커피": 2500,
            "우유": 2000
        }
    }
}

# --- 5. 사이드바 (모드 선택 및 메뉴 이동) ---
st.sidebar.title("⚙️ 키오스크 설정을 선택하세요")
selected_age = st.sidebar.radio(
    "👤 연령대 맞춤 모드",
    list(AGE_CONFIG.keys()),
    index=list(AGE_CONFIG.keys()).index(st.session_state.age_group)
)
st.session_state.age_group = selected_age

page = st.sidebar.radio(
    "📍 화면 이동",
    ["1. 맞춤 시작 & 음성 가이드", "2. 연령별 인기 메뉴 추천 & 주문", "3. 간소화 결제 및 직원 호출"]
)

config = AGE_CONFIG[st.session_state.age_group]

# --- 커스텀 CSS 적용 (글자 크기 및 테마 반영) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {config['bg_color']};
    }}
    .custom-title {{
        font-size: {config['title_size']};
        font-weight: bold;
        color: {config['theme_color']};
        margin-bottom: 10px;
    }}
    .custom-text {{
        font-size: {config['text_size']};
    }}
    .stButton>button {{
        border-radius: 12px;
        font-size: {config['text_size']};
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. 페이지 1: 맞춤 시작 & 음성 가이드 ---
if page == "1. 맞춤 시작 & 음성 가이드":
    st.markdown(f"<span style='background-color:{config['theme_color']}; color:white; padding:5px 12px; border-radius:20px; font-weight:bold;'>{config['badge']}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-title'>{config['welcome']}</div>", unsafe_allow_html=True)
    
    # 맞춤형 음성 가이드 박스
    st.info(f"🔊 **[맞춤형 음성 가이드]** ({config['voice_speed']})\n\n\"{config['voice_guide']}\"")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 모드별 최적화 안내")
        st.write(f"- **선택 모드:** {st.session_state.age_group}")
        st.write(f"- **글자 크기:** 최적화 적용 ({config['title_size']})")
        st.write("- **추천 알고리즘:** 연령대별 최다 판매 메뉴 최상단 자동 배치")
        
    with col2:
        st.subheader("🤖 AI 음성 도우미 (질문하기)")
        if gemini_available:
            user_question = st.text_input("질문을 입력하세요 (예: 속이 안 좋은데 추천해 줘, 어린이 세트 알려줘)")
            if user_question:
                try:
                    prompt = f"""
                    당신은 친절한 키오스크 AI 도우미입니다.
                    현재 고객의 연령층: {st.session_state.age_group}
                    고객의 질문: "{user_question}"
                    
                    위 연령층에 맞는 말투와 어조(어르신이면 천천히 존댓말, 어린이면 친근한 말투)로 2문장 이내로 친절하게 메뉴나 이용 방법을 추천해 주세요.
                    """
                    response = model.generate_content(prompt)
                    st.success(f"🤖 **AI 도우미:** {response.text}")
                except Exception as e:
                    st.warning("AI 도우미 응답 중 잠시 오류가 발생했습니다.")
        else:
            st.caption("※ GEMINI_API_KEY 설정 시 연령 맞춤 AI 음성 도우미 기능이 활성화됩니다.")

    st.markdown("---")
    st.success("👈 메뉴를 선택하시려면 사이드바에서 **'2. 연령별 인기 메뉴 추천 & 주문'**을 누르세요.")

# --- 7. 페이지 2: 연령별 인기 메뉴 추천 & 주문 ---
elif page == "2. 연령별 인기 메뉴 추천 & 주문":
    st.markdown(f"<div class='custom-title'>⭐ {st.session_state.age_group} 맞춤 인기 추천 메뉴</div>", unsafe_allow_html=True)
    st.write("사용자 나이대에 맞는 선호 메뉴가 최상단에 자동 추천됩니다.")
    
    # 연령별 추천 메뉴 배치
    rec_cols = st.columns(len(config['recommended']))
    for idx, item in enumerate(config['recommended']):
        with rec_cols[idx]:
            st.markdown(f"### {item['name']}")
            st.caption(item['desc'])
            st.write(f"**가격: {item['price']:,}원**")
            if st.button(f"🛒 담기 ({item['name']})", key=f"rec_{idx}", use_container_width=True):
                st.session_state.cart.append({"name": item['name'], "price": item['price']})
                st.toast(f"'{item['name']}'이(가) 장바구니에 담겼습니다!")

    st.markdown("---")
    
    # 기타 전체 메뉴
    st.subheader("📋 전체 일반 메뉴")
    all_menu_cols = st.columns(2)
    for idx, (item_name, price) in enumerate(config['all_menus'].items()):
        col_idx = idx % 2
        with all_menu_cols[col_idx]:
            st.write(f"**{item_name}** — {price:,}원")
            if st.button(f"담기", key=f"all_{idx}"):
                st.session_state.cart.append({"name": item_name, "price": price})
                st.toast(f"'{item_name}'이(가) 장바구니에 담겼습니다!")

    st.markdown("---")
    
    # 장바구니 영역
    st.subheader("🛒 내 장바구니 목록")
    if st.session_state.cart:
        total_price = 0
        for i, cart_item in enumerate(st.session_state.cart):
            col_a, col_b = st.columns([3, 1])
            col_a.write(f"• **{cart_item['name']}** ({cart_item['price']:,}원)")
            total_price += cart_item['price']
            if col_b.button("❌ 취소", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
        st.markdown(f"## **총 주문 금액: {total_price:,}원**")
    else:
        st.info("장바구니가 비어 있습니다. 위에서 메뉴를 선택해 주세요.")

# --- 8. 페이지 3: 간소화 결제 및 직원 호출 ---
elif page == "3. 간소화 결제 및 직원 호출":
    st.markdown(f"<div class='custom-title'>💳 주문 확인 및 간단 결제</div>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.warning("장바구니에 담긴 메뉴가 없습니다. 2페이지에서 먼저 메뉴를 담아주세요.")
    else:
        st.subheader("📝 최종 주문 내역")
        total_price = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"• **{item['name']}** — {item['price']:,}원")
            
        st.markdown(f"# **최종 결제 금액: {total_price:,}원**")
        st.markdown("---")
        
        st.subheader("👇 원하시는 결제 방법을 눌러주세요")
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            if st.button("💳 신용카드 / 체크카드 결제", use_container_width=True, type="primary"):
                st.balloons()
                st.success("결제가 성공적으로 완료되었습니다! 이용해 주셔서 감사합니다.")
                st.session_state.cart = []
        with col_pay2:
            if st.button("📱 간편 결제 (카카오페이/제로페이)", use_container_width=True):
                st.balloons()
                st.success("간편 결제가 완료되었습니다!")
                st.session_state.cart = []

    st.markdown("---")
    
    # 디지털 취약계층을 위한 직원 호출 서비스
    st.subheader("🆘 도움이 필요하신가요?")
    if st.button("🔔 직원 호출하기 (도움 요청)", type="secondary", use_container_width=True):
        st.warning("직원에게 호출 알림을 보냈습니다. 카운터 직원이 곧 안내해 드릴 예정입니다.")
