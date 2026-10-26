import streamlit as st
import os

# --- 1. 페이지 및 기본 설정 ---
st.set_page_config(
    page_title="맞춤형 프리미엄 카페 키오스크",
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
    st.session_state.age_group = "청년/장년 모드 (20~50대)"

# --- 4. 공통 전체 카페 메뉴 데이터 (일반 카페 메뉴 표준) ---
COMMON_MENU_DATABASE = {
    "☕ 커피 & 에스프레소": {
        "아이스 아메리카노": 3000,
        "따뜻한 아메리카노": 3000,
        "카페 라떼": 4000,
        "바닐라 빈 라떼": 4500,
        "카라멜 마키아또": 4800,
        "시그니처 아인슈페너": 5200,
        "디카페인 아메리카노": 3500,
        "콜드브루": 4200
    },
    "🍹 에이드 & 프라페": {
        "생자몽 에이드": 4800,
        "청포도 에이드": 4500,
        "레몬 에이드": 4500,
        "리얼 생딸기 라떼": 4800,
        "초코 쿠키 프라페": 5000,
        "플레인 요거트 스무디": 4800,
        "망고 스무디": 5000
    },
    "🍵 티 & 건강 음료": {
        "자몽 허니 블랙티": 4800,
        "얼그레이 티": 3800,
        "캐모마일 티": 3800,
        "건강 한방 쌍화차": 5000,
        "알싸한 생강차": 4500,
        "달콤 유자차": 4000,
        "구수한 둥굴레차": 3000
    },
    "🍰 디저트 & 베이커리": {
        "플레인 크로플": 3800,
        "아이스크림 크로플": 5200,
        "부드러운 치즈 케이크": 5500,
        "초코 티라미수": 5800,
        "쪽파 크림치즈 베이글": 4800,
        "버터 소금빵": 3200,
        "부드러운 카스테라": 3500,
        "단팥빵": 2800
    }
}

# --- 5. 연령별 모드 맞춤 설정 ---
AGE_CONFIG = {
    "어린이 모드 (10대 미만)": {
        "badge": "🎈 어린이 맞춤 모드",
        "title_size": "32px",
        "text_size": "18px",
        "theme_color": "#FF8C00",
        "bg_color": "#FFF8DC",
        "welcome": "안녕! 달콤한 스무디와 맛있는 디저트를 골라봐! 🍓",
        "voice_guide": "어린이 손님 환영해요! 달콤한 딸기 라떼와 초코 프라페를 추천해 줄게요.",
        "voice_speed": "밝고 경쾌한 안내 (보통 속도)",
        "recommended": [
            {"name": "리얼 생딸기 라떼", "price": 4800, "desc": "달콤한 딸기가 가득 들어간 인기 음료"},
            {"name": "초코 쿠키 프라페", "price": 5000, "desc": "바삭한 쿠키가 올려진 초코 프라페"},
            {"name": "아이스크림 크로플", "price": 5200, "desc": "달콤한 바닐라 아이스크림이 얹어진 크로플"}
        ]
    },
    "청년/장년 모드 (20~50대)": {
        "badge": "⚡ 스피디 주문 모드",
        "title_size": "26px",
        "text_size": "16px",
        "theme_color": "#1E90FF",
        "bg_color": "#F8F9FA",
        "welcome": "원하시는 커피와 디저트를 빠르고 간편하게 주문하세요.",
        "voice_guide": "에스프레소 음료부터 시그니처 크림 라떼까지 빠르게 선택하실 수 있습니다.",
        "voice_speed": "명확하고 빠른 안내 (빠른 속도)",
        "recommended": [
            {"name": "아이스 아메리카노", "price": 3000, "desc": "깊고 고소한 풍미의 원두 에스프레소"},
            {"name": "시그니처 아인슈페너", "price": 5200, "desc": "부드러운 수제 크림이 올려진 아인슈페너"},
            {"name": "쪽파 크림치즈 베이글", "price": 4800, "desc": "신선한 크림치즈와 쪽파의 환상 조합"}
        ]
    },
    "어르신 모드 (60대 이상)": {
        "badge": "👵 어르신 쉬운 모드",
        "title_size": "38px",
        "text_size": "22px",
        "theme_color": "#2E8B57",
        "bg_color": "#FFFDD0",
        "welcome": "어르신, 반갑습니다! 천천히 보고 편하게 주문하세요.",
        "voice_guide": "어르신, 잘 오셨습니다. 아메리카노부터 따뜻한 전통차까지 편하게 눌러보세요.",
        "voice_speed": "크고 또박또박한 안내 (천천히)",
        "recommended": [
            {"name": "아이스 아메리카노", "price": 3000, "desc": "기본 깔끔한 커피 (따뜻한 커피도 가능)"},
            {"name": "건강 한방 쌍화차", "price": 5000, "desc": "견과류가 듬뿍 들어간 따뜻한 전통차"},
            {"name": "부드러운 카스테라", "price": 3500, "desc": "입에서 부드럽게 녹는 촉촉한 카스테라"}
        ]
    }
}

# --- 6. 사이드바 (모드 선택 및 메뉴 이동) ---
st.sidebar.title("⚙️ 카페 키오스크 설정")
selected_age = st.sidebar.radio(
    "👤 연령대 맞춤 모드 선택",
    list(AGE_CONFIG.keys()),
    index=list(AGE_CONFIG.keys()).index(st.session_state.age_group)
)
st.session_state.age_group = selected_age

page = st.sidebar.radio(
    "📍 화면 이동",
    ["1. 맞춤 시작 & 음성 가이드", "2. 전체 카페 메뉴 주문", "3. 간소화 결제 및 직원 호출"]
)

config = AGE_CONFIG[st.session_state.age_group]

# --- 커스텀 CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {config['bg_color']};
    }}
    .custom-title {{
        font-size: {config['title_size']};
        font-weight: bold;
        color: {config['theme_color']};
        margin-bottom: 12px;
    }}
    .stButton>button {{
        border-radius: 12px;
        font-size: {config['text_size']};
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 7. 페이지 1: 맞춤 시작 & 음성 가이드 ---
if page == "1. 맞춤 시작 & 음성 가이드":
    st.markdown(f"<span style='background-color:{config['theme_color']}; color:white; padding:6px 14px; border-radius:20px; font-weight:bold;'>{config['badge']}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-title'>{config['welcome']}</div>", unsafe_allow_html=True)
    
    st.info(f"🔊 **[맞춤형 음성 가이드]** ({config['voice_speed']})\n\n\"{config['voice_guide']}\"")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 연령 맞춤 서비스 특징")
        st.write(f"- **현재 모드:** {st.session_state.age_group}")
        st.write("- **화면 최적화:** 어르신 모드 선택 시 초대형 글자 적용")
        st.write("- **메뉴 구성:** 일반 카페 전체 메뉴 + 연령별 인기 메뉴 상단 추천")
        
    with col2:
        st.subheader("🤖 AI 음성 도우미 (질문하기)")
        if gemini_available:
            user_question = st.text_input("질문 입력 (예: 덜 달고 시원한 음료 추천해 줘, 부드러운 디저트 있어?)")
            if user_question:
                try:
                    prompt = f"""
                    당신은 친절한 카페 AI 도우미입니다.
                    현재 손님 연령층: {st.session_state.age_group}
                    질문: "{user_question}"
                    
                    연령층에 적합한 어조로 2문장 이내로 매장의 커피나 에이드, 디저트 메뉴를 추천해 주세요.
                    """
                    response = model.generate_content(prompt)
                    st.success(f"🤖 **AI 답변:** {response.text}")
                except Exception:
                    st.warning("AI 도우미 응답 중 잠시 오류가 발생했습니다.")
        else:
            st.caption("※ GEMINI_API_KEY 설정 시 AI 맞춤 추천 기능이 활성화됩니다.")

    st.markdown("---")
    st.success("👈 왼쪽 메뉴에서 **'2. 전체 카페 메뉴 주문'**을 눌러 커피와 디저트를 골라보세요!")

# --- 8. 페이지 2: 전체 카페 메뉴 주문 ---
elif page == "2. 전체 카페 메뉴 주문":
    st.markdown(f"<div class='custom-title'>⭐ {st.session_state.age_group} 우선 추천 메뉴</div>", unsafe_allow_html=True)
    
    # 1) 연령별 인기 메뉴 자동 우선 추천
    rec_cols = st.columns(len(config['recommended']))
    for idx, item in enumerate(config['recommended']):
        with rec_cols[idx]:
            st.markdown(f"### {item['name']}")
            st.caption(item['desc'])
            st.write(f"**{item['price']:,}원**")
            if st.button(f"🛒 담기", key=f"rec_{idx}", use_container_width=True):
                st.session_state.cart.append({"name": item['name'], "price": item['price']})
                st.toast(f"'{item['name']}'이(가) 장바구니에 담겼습니다!")

    st.markdown("---")
    
    # 2) 전체 카페 카테고리별 메뉴 (모든 연령 공통 제공)
    st.subheader("☕ 전체 카페 메뉴 보기")
    
    cat_names = list(COMMON_MENU_DATABASE.keys())
    tabs = st.tabs(cat_names)
    
    for tab_idx, cat_name in enumerate(cat_names):
        with tabs[tab_idx]:
            items = COMMON_MENU_DATABASE[cat_name]
            item_cols = st.columns(2)
            for item_idx, (item_name, price) in enumerate(items.items()):
                c_idx = item_idx % 2
                with item_cols[c_idx]:
                    st.write(f"**{item_name}** — {price:,}원")
                    if st.button("담기", key=f"cat_{tab_idx}_{item_idx}"):
                        st.session_state.cart.append({"name": item_name, "price": price})
                        st.toast(f"'{item_name}'이(가) 장바구니에 담겼습니다!")

    st.markdown("---")
    
    # 3) 장바구니
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
        st.info("장바구니가 비어 있습니다. 원하시는 커피, 음료, 디저트를 담아보세요.")

# --- 9. 페이지 3: 간소화 결제 및 직원 호출 ---
elif page == "3. 간소화 결제 및 직원 호출":
    st.markdown(f"<div class='custom-title'>💳 주문 내역 확인 및 결제</div>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.warning("장바구니에 담긴 메뉴가 없습니다. 2페이지에서 먼저 음료나 디저트를 담아주세요.")
    else:
        st.subheader("📝 최종 주문 내역")
        total_price = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"• **{item['name']}** — {item['price']:,}원")
            
        st.markdown(f"# **최종 결제 금액: {total_price:,}원**")
        st.markdown("---")
        
        st.subheader("👇 결제 방식을 선택하세요")
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            if st.button("💳 신용카드 / IC카드 결제", use_container_width=True, type="primary"):
                st.balloons()
                st.success("결제가 성공적으로 완료되었습니다! 진동벨을 받아가세요.")
                st.session_state.cart = []
        with col_pay2:
            if st.button("📱 카카오페이 / 모바일 쿠폰", use_container_width=True):
                st.balloons()
                st.success("간편 결제가 완료되었습니다!")
                st.session_state.cart = []

    st.markdown("---")
    
    # 직원 호출 버튼
    st.subheader("🆘 도움이 필요하신가요?")
    if st.button("🔔 직원 호출하기 (도움 요청)", type="secondary", use_container_width=True):
        st.warning("카운터 직원에게 호출 알림이 전달되었습니다. 잠시만 기다려 주세요!")
