import streamlit as st
import os

# --- 1. 페이지 및 기본 설정 ---
st.set_page_config(
    page_title="사용자 맞춤 키오스크",
    page_icon="🍔",
    layout="wide"
)

# --- 2. Gemini API 설정 (선택적) ---
gemini_available = False
try:
    import google.generativeai as genai
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        gemini_available = True
except Exception as e:
    gemini_available = False

# --- 3. 세션 상태(Session State) 초기화 ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'age_group' not in st.session_state:
    st.session_state.age_group = "어르신 (60대 이상)"

# --- 4. 연령별 설정 데이터 ---
AGE_CONFIG = {
    "어린이 (10대 미만)": {
        "title_size": "32px",
        "bg_color": "#FFF8DC",
        "welcome": "🎈 안녕! 오늘은 어떤 맛있는 걸 먹어볼까?",
        "voice_msg": "어린이 손님 환영해요! 달콤하고 신나는 메뉴를 추천해 줄게요.",
        "recommended": ["달콤 치즈버거", "초코 쉐이크", "바삭 감자튀김"],
        "all_menus": {
            "달콤 치즈버거": 5500,
            "초코 쉐이크": 3500,
            "바삭 감자튀김": 2000,
            "어린이 불고기버거": 5000,
            "오렌지 주스": 2500
        }
    },
    "청년/장년 (20~50대)": {
        "title_size": "26px",
        "bg_color": "#F4F4F4",
        "welcome": "⚡ 빠른 주문과 인기 신메뉴를 확인해보세요.",
        "voice_msg": "원하시는 메뉴를 빠르게 선택하고 결제하실 수 있습니다.",
        "recommended": ["더블 패티 버거", "제로 콜라", "아메리카노"],
        "all_menus": {
            "더블 패티 버거": 7500,
            "제로 콜라": 2000,
            "아메리카노": 3000,
            "핫 크리스피 버거": 6800,
            "치즈 스틱": 2500
        }
    },
    "어르신 (60대 이상)": {
        "title_size": "36px",
        "bg_color": "#EFEFD0",
        "welcome": "👵 어르신, 천천히 보고 편하게 주문해 주세요.",
        "voice_msg": "어르신, 반갑습니다. 어렵지 않게 도와드릴 테니 천천히 눌러보세요.",
        "recommended": ["속 편한 불고기버거", "따뜻한 둥굴레차", "부드러운 단호박 스프"],
        "all_menus": {
            "속 편한 불고기버거": 5000,
            "따뜻한 둥굴레차": 2000,
            "부드러운 단호박 스프": 3000,
            "클래식 치즈버거": 4500,
            "디카페인 커피": 2500
        }
    }
}

# --- 5. 사이드바 (연령 모드 선택 및 메뉴 이동) ---
st.sidebar.title("⚙️ 키오스크 설정")
selected_age = st.sidebar.selectbox(
    "사용자 연령 모드 선택",
    list(AGE_CONFIG.keys()),
    index=list(AGE_CONFIG.keys()).index(st.session_state.age_group)
)
st.session_state.age_group = selected_age

page = st.sidebar.radio(
    "페이지 이동",
    ["1. 맞춤 시작 및 안내", "2. 맞춤 메뉴 추천 & 주문", "3. 주문 확인 및 결제"]
)

config = AGE_CONFIG[st.session_state.age_group]

# --- 6. 페이지 1: 맞춤 시작 및 안내 ---
if page == "1. 맞춤 시작 및 안내":
    st.markdown(f"<h1 style='font-size: {config['title_size']};'>{config['welcome']}</h1>", unsafe_allow_html=True)
    
    st.info(f"🔊 **[맞춤 음성 안내]** {config['voice_msg']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 현재 적용된 맞춤 모드")
        st.write(f"- **선택 연령층:** {st.session_state.age_group}")
        st.write(f"- **글자 크기:** 대형 최적화 ({config['title_size']})")
        st.write("- **화면 구성:** 맞춤형 간소화 레이아웃")
        
    with col2:
        st.subheader("🤖 AI 안내 도우미")
        if gemini_available:
            user_question = st.text_input("궁금한 점을 물어보세요 (예: 매운 거 못 먹는데 뭐 먹을까?)")
            if user_question:
                try:
                    prompt = f"당신은 키오스크 AI 안내원입니다. 사용자 연령층은 {st.session_state.age_group}입니다. 연령에 맞게 아주 친절하고 쉬운 말투로 짧게 2문장 이내로 답변해주세요. 질문: {user_question}"
                    response = model.generate_content(prompt)
                    st.success(f"🤖 답변: {response.text}")
                except Exception as e:
                    st.warning("AI 답변을 불러오는 중 오류가 발생했습니다.")
        else:
            st.caption("※ GEMINI_API_KEY를 설정하면 AI 도우미 기능을 사용할 수 있습니다.")

    st.markdown("---")
    st.success("왼쪽 사이드바에서 **'2. 맞춤 메뉴 추천 & 주문'**을 눌러 메뉴를 선택해주세요.")

# --- 7. 페이지 2: 맞춤 메뉴 추천 & 주문 ---
elif page == "2. 맞춤 메뉴 추천 & 주문":
    st.markdown(f"<h1 style='font-size: {config['title_size']};'>⭐ {st.session_state.age_group} 맞춤 메뉴</h1>", unsafe_allow_html=True)
    
    # 인기 메뉴 우선 추천
    st.subheader("🔥 이 연령대에서 가장 인기 있는 메뉴")
    rec_cols = st.columns(len(config['recommended']))
    for idx, item in enumerate(config['recommended']):
        price = config['all_menus'][item]
        with rec_cols[idx]:
            st.markdown(f"### {item}")
            st.write(f"가격: **{price:,}원**")
            if st.button(f"담기 ({item})", key=f"rec_{idx}"):
                st.session_state.cart.append({"name": item, "price": price})
                st.toast(f"'{item}'이(가) 장바구니에 담겼습니다!")

    st.markdown("---")
    
    # 전체 메뉴 목록
    st.subheader("📋 전체 메뉴 보기")
    all_menu_cols = st.columns(3)
    for idx, (item, price) in enumerate(config['all_menus'].items()):
        col_idx = idx % 3
        with all_menu_cols[col_idx]:
            st.write(f"**{item}** - {price:,}원")
            if st.button("담기", key=f"all_{idx}"):
                st.session_state.cart.append({"name": item, "price": price})
                st.toast(f"'{item}'이(가) 장바구니에 담겼습니다!")

    st.markdown("---")
    # 장바구니 현황
    st.subheader("🛒 내가 담은 메뉴")
    if st.session_state.cart:
        total_price = 0
        for i, cart_item in enumerate(st.session_state.cart):
            col_a, col_b = st.columns([3, 1])
            col_a.write(f"- {cart_item['name']} ({cart_item['price']:,}원)")
            total_price += cart_item['price']
            if col_b.button("삭제", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
        st.markdown(f"### 💰 **총 금액: {total_price:,}원**")
    else:
        st.write("장바구니가 비어 있습니다.")

# --- 8. 페이지 3: 주문 확인 및 결제 ---
elif page == "3. 주문 확인 및 결제":
    st.markdown(f"<h1 style='font-size: {config['title_size']};'>💳 주문 확인 및 결제</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.warning("장바구니에 담긴 메뉴가 없습니다. 2페이지에서 메뉴를 먼저 선택해주세요.")
    else:
        st.subheader("📝 주문 내역")
        total_price = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.write(f"• {item['name']} - {item['price']:,}원")
            
        st.markdown(f"## **최종 결제 금액: {total_price:,}원**")
        
        st.markdown("---")
        st.subheader("결제 수단을 선택해 주세요")
        
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            if st.button("💳 신용카드 / 체크카드", use_container_width=True):
                st.balloons()
                st.success("결제가 완료되었습니다! 카드를 뽑아주세요.")
                st.session_state.cart = []
        with col_pay2:
            if st.button("📱 간편 결제 (페이/바코드)", use_container_width=True):
                st.balloons()
                st.success("간편 결제가 완료되었습니다!")
                st.session_state.cart = []

        st.markdown("---")
        # 디지털 취약계층용 직원 호출 버튼
        if st.button("🔔 도움이 필요하신가요? (직원 호출)", type="secondary", use_container_width=True):
            st.warning("직원을 호출했습니다. 잠시만 기다려 주세요!")
