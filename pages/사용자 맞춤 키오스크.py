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
model = None

try:
    import google.generativeai as genai
    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        # 안전한 gemini-2.5-flash-lite 모델 호출
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        gemini_available = True
except Exception:
    gemini_available = False

# --- 3. 세션 상태 초기화 ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'age_group' not in st.session_state:
    st.session_state.age_group = "👵 어르신 쉬운 모드"

# --- 4. 공통 카페 메뉴 데이터 (이미지 URL 포함) ---
COMMON_MENU_DATABASE = {
    "☕ 커피류": {
        "따뜻한 아메리카노": {"price": 3000, "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400"},
        "아이스 아메리카노": {"price": 3000, "img": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=400"},
        "따뜻한 카페 라떼": {"price": 4000, "img": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=400"},
        "바닐라 빈 라떼": {"price": 4500, "img": "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=400"},
        "디카페인 커피": {"price": 3500, "img": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400"},
        "시그니처 크림라떼": {"price": 5200, "img": "https://images.unsplash.com/photo-1585494156145-1c60a4fe952b?w=400"}
    },
    "🍵 건강차 & 음료": {
        "건강 한방 쌍화차": {"price": 5000, "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=400"},
        "알싸한 생강차": {"price": 4500, "img": "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=400"},
        "달콤 유자차": {"price": 4000, "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400"},
        "구수한 둥굴레차": {"price": 3000, "img": "https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400"},
        "생자몽 에이드": {"price": 4800, "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=400"},
        "리얼 생딸기 라떼": {"price": 4800, "img": "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=400"}
    },
    "🍰 디저트 & 빵": {
        "부드러운 카스테라": {"price": 3500, "img": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?w=400"},
        "달콤한 단팥빵": {"price": 2800, "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400"},
        "플레인 크로플": {"price": 3800, "img": "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=400"},
        "버터 소금빵": {"price": 3200, "img": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400"},
        "치즈 케이크": {"price": 5500, "img": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=400"}
    }
}

# --- 5. 연령별/모드별 UI & 스타일 설정 ---
AGE_CONFIG = {
    "👵 어르신 쉬운 모드": {
        "badge": "👵 어르신을 위한 큰 글씨 모드",
        "title_size": "40px",
        "sub_size": "26px",
        "text_size": "22px",
        "btn_padding": "18px 24px",
        "btn_size": "24px",
        "sidebar_size": "22px",
        "theme_color": "#1B5E20",
        "bg_color": "#FFFDE7",
        "welcome": "어르신, 반갑습니다! 천천히 보고 편하게 눌러주세요.",
        "recommended": [
            {"name": "따뜻한 아메리카노", "price": 3000, "desc": "속이 깔끔하고 따뜻한 기본 커피", "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400"},
            {"name": "건강 한방 쌍화차", "price": 5000, "desc": "견과류가 들어간 따뜻한 건강차", "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=400"},
            {"name": "부드러운 카스테라", "price": 3500, "desc": "입에서 녹는 촉촉하고 부드러운 빵", "img": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?w=400"}
        ]
    },
    "☕ 일반 모드 (보통 모드)": {
        "badge": "☕ 표준 주문 모드",
        "title_size": "28px",
        "sub_size": "20px",
        "text_size": "16px",
        "btn_padding": "12px 18px",
        "btn_size": "17px",
        "sidebar_size": "18px",
        "theme_color": "#1565C0",
        "bg_color": "#F8F9FA",
        "welcome": "원하시는 카페 음료와 디저트를 편리하게 선택해 보세요.",
        "recommended": [
            {"name": "아이스 아메리카노", "price": 3000, "desc": "고소하고 깔끔한 원두 에스프레소", "img": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=400"},
            {"name": "리얼 생딸기 라떼", "price": 4800, "desc": "달콤한 딸기가 가득 들어간 인기 음료", "img": "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=400"},
            {"name": "버터 소금빵", "price": 3200, "desc": "고소한 풍미의 바삭한 인기 베이커리", "img": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400"}
        ]
    }
}

# --- 6. 사이드바 ---
st.sidebar.title("⚙️ 키오스크 설정")
selected_age = st.sidebar.radio(
    "👤 서비스 모드 선택",
    list(AGE_CONFIG.keys()),
    index=list(AGE_CONFIG.keys()).index(st.session_state.age_group)
)
st.session_state.age_group = selected_age

page = st.sidebar.radio(
    "📍 화면 이동",
    ["1. 맞춤 시작 및 안내", "2. 전체 카페 메뉴 주문", "3. 간소화 결제 및 직원 호출"]
)

config = AGE_CONFIG[st.session_state.age_group]

# --- 7. 동적 CSS (메뉴 높이/크기 완전 통일) ---
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
        margin-top: 8px;
        margin-bottom: 8px;
    }}
    .custom-text {{
        font-size: {config['text_size']};
        line-height: 1.5;
    }}
    
    /* 어르신 모드 카드 전체 높이 및 규격 동일화 */
    .menu-card {{
        background-color: white;
        border: 2px solid {config['theme_color']};
        border-radius: 16px;
        padding: 16px;
        height: 480px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }}
    
    .menu-img {{
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 12px;
    }}

    /* 버튼 크기 및 터치 영역 통일 */
    .stButton > button {{
        font-size: {config['btn_size']} !important;
        font-weight: bold !important;
        padding: {config['btn_padding']} !important;
        border-radius: 14px !important;
        border: 2px solid {config['theme_color']} !important;
        width: 100% !important;
    }}
    
    /* 사이드바 글씨 크기 설정 */
    section[data-testid="stSidebar"] div {{
        font-size: {config['sidebar_size']} !important;
    }}
    section[data-testid="stSidebar"] label {{
        font-size: {config['sidebar_size']} !important;
        font-weight: bold !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 8. 페이지 1: 맞춤 시작 및 안내 ---
if page == "1. 맞춤 시작 및 안내":
    st.markdown(f"<span style='background-color:{config['theme_color']}; color:white; padding:8px 18px; border-radius:24px; font-size:{config['text_size']}; font-weight:bold;'>{config['badge']}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='custom-title' style='margin-top:15px;'>{config['welcome']}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-sub'>🤖 AI 인공지능 음성 도우미</div>", unsafe_allow_html=True)
    
    user_question = st.text_input("궁금하신 점을 편하게 질문해 주세요 (예: 속 편한 차 추천해 줘, 제일 인기 있는 디저트가 뭐야?)")
    if user_question:
        if gemini_available and model:
            try:
                prompt = f"""
                당신은 친절한 카페 AI 도우미입니다.
                현재 손님이 선택한 모드: {st.session_state.age_group}
                질문: "{user_question}"
                
                선택 모드에 맞춰 완전히 한국어로 친절하고 쉬운 어조로 2문장 이내로 답변해 주세요. 영어나 전문 용어를 사용하지 마세요.
                """
                response = model.generate_content(prompt)
                if hasattr(response, 'text') and response.text:
                    st.success(f"🤖 **AI 도우미 답변:** {response.text}")
                else:
                    st.info("🤖 **AI 도우미:** 따뜻한 쌍화차나 카스테라 메뉴를 추천해 드려요!")
            except Exception as e:
                st.warning("AI 도우미 연결 중 오류가 발생했습니다. 키오스크 안내 화면에서 메뉴를 자유롭게 골라주세요.")
        else:
            st.info("💡 **AI 안내:** 현재 API 키가 설정되지 않았거나 연결 대기 중입니다. 상단 및 사이드바 메뉴를 이용해 손쉽게 주문하실 수 있습니다.")

    st.markdown("---")
    st.success("👈 메뉴를 선택하시려면 사이드바에서 **'2. 전체 카페 메뉴 주문'**을 눌러주세요.")

# --- 9. 페이지 2: 전체 카페 메뉴 주문 ---
elif page == "2. 전체 카페 메뉴 주문":
    st.markdown(f"<div class='custom-title'>⭐ 인기 추천 메뉴</div>", unsafe_allow_html=True)
    st.markdown("<div class='custom-text'>자주 찾으시는 추천 메뉴입니다. 버튼을 누르면 장바구니에 담깁니다.</div>", unsafe_allow_html=True)
    
    # 추천 메뉴 카드 (높이 및 규격 완벽 통일)
    rec_cols = st.columns(len(config['recommended']))
    for idx, item in enumerate(config['recommended']):
        with rec_cols[idx]:
            st.markdown(f"""
                <div class='menu-card'>
                    <div>
                        <img src="{item['img']}" class='menu-img'>
                        <div class='custom-sub'>{item['name']}</div>
                        <div class='custom-text'>{item['desc']}</div>
                    </div>
                    <div class='custom-sub' style='color:{config['theme_color']};'>{item['price']:,}원</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"담기", key=f"rec_{idx}"):
                st.session_state.cart.append({"name": item['name'], "price": item['price']})
                st.toast(f"'{item['name']}' 담기 완료!")

    st.markdown("---")
    
    # 전체 카테고리 메뉴 카드 (높이 및 규격 완벽 통일)
    st.markdown("<div class='custom-title'>☕ 전체 카테고리 메뉴</div>", unsafe_allow_html=True)
    
    cat_names = list(COMMON_MENU_DATABASE.keys())
    tabs = st.tabs(cat_names)
    
    for tab_idx, cat_name in enumerate(cat_names):
        with tabs[tab_idx]:
            items = COMMON_MENU_DATABASE[cat_name]
            item_cols = st.columns(3)
            for item_idx, (item_name, item_data) in enumerate(items.items()):
                c_idx = item_idx % 3
                with item_cols[c_idx]:
                    st.markdown(f"""
                        <div class='menu-card'>
                            <div>
                                <img src="{item_data['img']}" class='menu-img'>
                                <div class='custom-sub'>{item_name}</div>
                            </div>
                            <div class='custom-sub' style='color:{config['theme_color']};'>{item_data['price']:,}원</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"선택하기", key=f"cat_{tab_idx}_{item_idx}"):
                        st.session_state.cart.append({"name": item_name, "price": item_data['price']})
                        st.toast(f"'{item_name}' 담기 완료!")

    st.markdown("---")
    
    # 장바구니 목록
    st.markdown("<div class='custom-title'>🛒 내가 선택한 메뉴 목록</div>", unsafe_allow_html=True)
    if st.session_state.cart:
        total_price = 0
        for i, cart_item in enumerate(st.session_state.cart):
            col_a, col_b = st.columns([3, 1])
            col_a.markdown(f"<div class='custom-text'>• <b>{cart_item['name']}</b> ({cart_item['price']:,}원)</div>", unsafe_allow_html=True)
            total_price += cart_item['price']
            if col_b.button("취소", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
        st.markdown(f"<div class='custom-title' style='color:red; margin-top:15px;'>💰 총 금액: {total_price:,}원</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='custom-text'>아직 선택하신 메뉴가 없습니다. 위에서 메뉴를 눌러주세요.</div>", unsafe_allow_html=True)

# --- 10. 페이지 3: 간소화 결제 및 직원 호출 ---
elif page == "3. 간소화 결제 및 직원 호출":
    st.markdown(f"<div class='custom-title'>💳 주문 확인 및 결제</div>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.warning("선택한 메뉴가 없습니다. 2페이지에서 메뉴를 먼저 눌러주세요.")
    else:
        st.markdown("<div class='custom-sub'>📝 최종 주문 내역</div>", unsafe_allow_html=True)
        total_price = sum(item['price'] for item in st.session_state.cart)
        for item in st.session_state.cart:
            st.markdown(f"<div class='custom-text'>• <b>{item['name']}</b> — {item['price']:,}원</div>", unsafe_allow_html=True)
            
        st.markdown(f"<div class='custom-title' style='color:red; margin-top:20px;'>최종 결제 금액: {total_price:,}원</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("<div class='custom-sub'>👇 결제 방법을 눌러주세요</div>", unsafe_allow_html=True)
        col_pay1, col_pay2 = st.columns(2)
        with col_pay1:
            if st.button("💳 신용카드 / 체크카드 결제", key="pay_card"):
                st.balloons()
                st.success("결제가 완료되었습니다! 진동벨을 받아가세요.")
                st.session_state.cart = []
        with col_pay2:
            if st.button("📱 카카오페이 / 모바일 결제", key="pay_mobile"):
                st.balloons()
                st.success("간편 결제가 완료되었습니다!")
                st.session_state.cart = []

    st.markdown("---")
    
    st.markdown("<div class='custom-sub'>🆘 도움이 필요하신가요?</div>", unsafe_allow_html=True)
    if st.button("🔔 직원 호출하기 (도움 필요)", key="call_staff"):
        st.warning("직원을 불렀습니다. 잠시만 기다려 주시면 친절히 안내해 드리겠습니다!")
