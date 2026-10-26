import streamlit as st
import os

# --- 1. 페이지 및 기본 설정 ---
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
    st.session_state.age_group = "어르신 모드 (60대 이상)"

# --- 4. 카페 전용 연령별 테마 및 풍성한 메뉴 데이터 ---
AGE_CONFIG = {
    "어린이 모드 (10대 미만)": {
        "badge": "🎈 어린이 맞춤 카페",
        "title_size": "32px",
        "text_size": "18px",
        "theme_color": "#FF8C00",
        "bg_color": "#FFF8DC",
        "welcome": "안녕! 달콤하고 맛있는 카페 음료 골라볼까? 🧃",
        "voice_guide": "어린이 손님 환영해요! 달콤한 딸기 라떼와 스무디를 추천해 줄게요.",
        "voice_speed": "밝고 경쾌한 목소리 (보통 속도)",
        "recommended": [
            {"name": "🍓 생딸기 라떼", "price": 4500, "desc": "달콤한 딸기가 씹히는 인기 음료"},
            {"name": "🍫 초코 쿠키 프라페", "price": 4800, "desc": "바삭한 쿠키가 올려진 초코 스무디"},
            {"name": "🍩 무지개 도넛", "price": 2800, "desc": "알록달록 달콤한 디저트"}
        ],
        "categories": {
            "🧃 달콤 음료": {
                "초코 라떼": 4000,
                "바나나 우유 스무디": 4200,
                "블루에이드": 4000,
                "뽀로로 음료수": 2000
            },
            "🍰 디저트": {
                "초코 컵케이크": 3500,
                "플레인 크로플": 3800,
                "바닐라 아이스크림": 3000
            }
        }
    },
    "청년/장년 모드 (20~50대)": {
        "badge": "⚡ 빠른 주문 모드",
        "title_size": "26px",
        "text_size": "16px",
        "theme_color": "#1E90FF",
        "bg_color": "#F4F4F4",
        "welcome": "바쁜 일상 속, 빠르게 스페셜티 커피를 주문하세요.",
        "voice_guide": "에스프레소 음료부터 시그니처 라떼까지 빠르게 선택하실 수 있습니다.",
        "voice_speed": "명확하고 빠른 안내 (빠른 속도)",
        "recommended": [
            {"name": "☕ 아이스 아메리카노", "price": 3000, "desc": "고소하고 깔끔한 원두 에스프레소"},
            {"name": "🥛 시그니처 크림라떼", "price": 5200, "desc": "부드러운 수제 크림이 올려진 라떼"},
            {"name": "🥪 햄치즈 샌드위치", "price": 5800, "desc": "신선한 재료로 채운 한 끼 식사 대용"}
        ],
        "categories": {
            "☕ 커피 & 에스프레소": {
                "카페 라떼": 4000,
                "바닐라 빈 라떼": 4500,
                "콜드브루": 4200,
                "디카페인 아메리카노": 3500
            },
            "🍹 에이드 & 티": {
                "자몽 블랙티": 4800,
                "청포도 에이드": 4500,
                "얼그레이 티": 3800
            },
            "🥐 베이커리": {
                "쪽파 크림치즈 베이글": 4800,
                "소금빵": 3200,
                "치즈 케이크": 5500
            }
        }
    },
    "어르신 모드 (60대 이상)": {
        "badge": "👵 어르신 쉬운 모드",
        "title_size": "38px",
        "text_size": "22px",
        "theme_color": "#2E8B57",
        "bg_color": "#FFFDD0",
        "welcome": "어르신, 반갑습니다! 따뜻하고 속 편한 차 한잔하세요.",
        "voice_guide": "어르신, 잘 오셨습니다. 드시고 싶은 차나 빵을 천천히 눌러보세요.",
        "voice_speed": "크고 또박또박한 안내 (천천히)",
        "recommended": [
            {"name": "🍵 건강 한방 쌍화차", "price": 5000, "desc": "견과류가 듬뿍 들어간 따뜻한 쌍화차"},
            {"name": "🍠 고구마 라떼", "price": 4500, "desc": "속이 든든하고 달콤한 따뜻한 라떼"},
            {"name": "🍞 부드러운 카스테라", "price": 3500, "desc": "입에서 입으로 녹는 촉촉한 카스테라"}
        ],
        "categories": {
            "🍵 따뜻한 건강차": {
                "알싸한 생강차": 4500,
                "달콤한 유자차": 4000,
                "구수한 둥굴레차": 3000
            },
            "☕ 순한 음료": {
                "따뜻한 우유": 2500,
                "디카페인 따뜻한 라떼": 4200,
                "토마토 생과일 주스": 5000
            },
            "🍞 부드러운 간식": {
                "단팥빵": 2800,
                "쌀 증편 떡": 3000,
                "단호박 스프": 4000
            }
        }
    }
}

# --- 5. 사이드바 (모드 선택 및 메뉴 이동) ---
st.sidebar.title("⚙️ 카페 키오스크 설정")
selected_age = st.sidebar.radio(
    "👤 연령대 맞춤 모드 선택",
    list(AGE_CONFIG.keys()),
    index=list(AGE_CONFIG.keys()).index(st.session_state.age_group)
)
st.session_state.age_group = selected_age

page = st.sidebar.radio(
    "📍 화면 이동",
    ["1. 맞춤 시작 & 음성 가이드", "2. 연령별 메뉴 선택 & 장바구니", "3. 간소화 결제 및 직원 호출"]
)

config = AGE_CONFIG[st.session_state.age_group]

# --- 커스텀 CSS (연령별 글자 크기 및 스타일) ---
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

# --- 6. 페이지 1: 맞춤 시작 & 음성 가이드 ---
if page == "1. 맞춤 시작 & 음성 가이드":
    st.markdown(f"<span style='background-color:{config['theme_color']}; color:white; padding:6px 14px; border-radius:20px; font-weight:bold;'>{config['badge']}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-title'>{config['welcome']}</div>", unsafe_allow_html=True)
    
    st.info(f"🔊 **[맞춤형 음성 가이드]** ({config['voice_speed']})\n\n\"{config['voice_guide']}\"")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 카페 맞춤 서비스 특징")
        st.write(f"- **선택 연령 모드:** {st.session_state.age_group}")
        st.write(f"- **화면 최적화:** 시니어 초대형 글자 / 키즈 맞춤 시각화")
        st.write("- **추천 시스템:** 연령별 가장 많이 찾는 음료 & 디저트 자동 배치")
        
    with col2:
        st.subheader("🤖 AI 음성 도우미 (카페 질문하기)")
        if gemini_available:
            user_question = st.text_input("질문 입력 (예: 달지 않고 부드러운 음료 있어?, 아이가 마실 거 추천해 줘)")
            if user_question:
                try:
                    prompt = f"""
                    당신은 친절한 카페 AI 도우미입니다.
                    현재 손님 연령층: {st.session_state.age_group}
                    질문: "{user_question}"
                    
                    연령층에 꼭 맞는 말투(어르신이면 매우 정중하고 천천히, 어린이면 달콤하고 친근하게)로 2문장 이내로 카페 메뉴를 추천해 주세요.
                    """
                    response = model.generate_content(prompt)
                    st.success(f"🤖 **AI 답변:** {response.text}")
                except Exception:
                    st.warning("AI 도우미 응답 중 잠시 오류가 발생했습니다.")
        else:
            st.caption("※ GEMINI_API_KEY 설정 시 AI 맞춤 추천 기능이 활성화됩니다.")

    st.markdown("---")
    st.success("👈 왼쪽 메뉴에서 **'2. 연령별 메뉴 선택 & 장바구니'**를 눌러 주문을 시작하세요!")

# --- 7. 페이지 2: 연령별 메뉴 선택 & 장바구니 ---
elif page == "2. 연령별 메뉴 선택 & 장바구니":
    st.markdown(f"<div class='custom-title'>⭐ {st.session_state.age_group} 인기 추천 음료/디저트</div>", unsafe_allow_html=True)
    
    # 1) 인기 메뉴 자동 우선 추천
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
    
    # 2) 카테고리별 풍성한 카페 메뉴
    st.subheader("☕ 카테고리별 메뉴 전체 보기")
    
    # 카테고리 탭 생성
    cat_names = list(config['categories'].keys())
    tabs = st.tabs(cat_names)
    
    for tab_idx, cat_name in enumerate(cat_names):
        with tabs[tab_idx]:
            items = config['categories'][cat_name]
            item_cols = st.columns(2)
            for item_idx, (item_name, price) in enumerate(items.items()):
                c_idx = item_idx % 2
                with item_cols[c_idx]:
                    st.write(f"**{item_name}** — {price:,}원")
                    if st.button(f"담기", key=f"cat_{tab_idx}_{item_idx}"):
                        st.session_state.cart.append({"name": item_name, "price": price})
                        st.toast(f"'{item_name}'이(가) 장바구니에 담겼습니다!")

    st.markdown("---")
    
    # 3) 장바구니
    st.subheader("🛒 선택한 주문 목록")
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
        st.info("장바구니가 비어 있습니다. 원하시는 음료나 디저트를 선택해 주세요.")

# --- 8. 페이지 3: 간소화 결제 및 직원 호출 ---
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
