import streamlit as st
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="맞춤형 카페 키오스크",
    page_icon="☕",
    layout="wide"
)

# --- 2. 세션 상태 초기화 ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'age_group' not in st.session_state:
    st.session_state.age_group = "👵 어르신 쉬운 모드"
if 'page' not in st.session_state:
    st.session_state.page = "홈"
if 'time_left' not in st.session_state:
    st.session_state.time_left = 90  # 기본 대기시간 90초
if 'last_time' not in st.session_state:
    st.session_state.last_time = time.time()

# 홈으로 돌아가기(초기화) 함수
def reset_to_home():
    st.session_state.cart = []
    st.session_state.page = "홈"
    st.session_state.time_left = 90
    st.session_state.last_time = time.time()

# 메뉴 담기 함수 (담기 누를 때 시간 30초 자동 연장)
def add_to_cart(item_name, price):
    st.session_state.cart.append({"name": item_name, "price": price})
    st.session_state.time_left = max(st.session_state.time_left, 60)  # 담기 누르면 60초 보장
    st.toast(f"'{item_name}' 담기 완료!")

# --- 3. 공통 카페 메뉴 데이터 ---
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

# --- 4. 연령별/모드별 UI & 스타일 설정 ---
AGE_CONFIG = {
    "👵 어르신 쉬운 모드": {
        "badge": "👵 어르신을 위한 큰 글씨 모드",
        "title_size": "40px",
        "sub_size": "28px",
        "text_size": "24px",
        "btn_padding": "18px 24px",
        "btn_size": "24px",
        "nav_btn_size": "36px",
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
        "btn_size": "18px",
        "nav_btn_size": "22px",
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

# --- 5. 타이머 경과 계산 로직 ---
now = time.time()
elapsed = int(now - st.session_state.last_time)
if elapsed >= 1:
    st.session_state.time_left -= elapsed
    st.session_state.last_time = now

if st.session_state.time_left <= 0:
    reset_to_home()

# --- 6. 사이드바 ---
st.sidebar.title("⚙️ 키오스크 설정")
selected_age = st.sidebar.radio(
    "👤 서비스 모드 선택",
    list(AGE_CONFIG.keys()),
    index=list(AGE_CONFIG.keys()).index(st.session_state.age_group)
)
st.session_state.age_group = selected_age

st.sidebar.markdown("---")
if st.sidebar.button("🏠 처음으로 (주문 취소)", key="side_home", use_container_width=True):
    reset_to_home()
    st.rerun()

config = AGE_CONFIG[st.session_state.age_group]

# --- 7. 동적 CSS ---
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

    .stButton > button, 
    .stButton > button * {{
        font-size: {config['btn_size']} !important;
        font-weight: 800 !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
    }}
    
    .stButton > button {{
        padding: {config['btn_padding']} !important;
        border-radius: 16px !important;
        border: 2px solid {config['theme_color']} !important;
        width: 100% !important;
    }}
    
    div[data-testid="column"] .stButton > button,
    div[data-testid="column"] .stButton > button * {{
        font-size: {config['nav_btn_size']} !important;
        font-weight: 900 !important;
    }}
    
    div[data-testid="column"] .stButton > button {{
        padding: 15px 5px !important;
        min-height: 80px !important;
    }}

    section[data-testid="stSidebar"] div {{
        font-size: {config['sidebar_size']} !important;
    }}
    section[data-testid="stSidebar"] label {{
        font-size: {config['sidebar_size']} !important;
        font-weight: bold !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 8. 상단 공통 헤더 ---
head_col1, head_col2, head_col3 = st.columns([2, 2, 1])

with head_col1:
    st.markdown(f"<span style='background-color:{config['theme_color']}; color:white; padding:8px 18px; border-radius:24px; font-size:{config['text_size']}; font-weight:bold;'>{config['badge']}</span>", unsafe_allow_html=True)

with head_col2:
    st.markdown(f"<div style='font-size:{config['sub_size']}; font-weight:bold; color:red; line-height:2.2;'>⏳ 남은 시간: {st.session_state.time_left}초</div>", unsafe_allow_html=True)

with head_col3:
    if st.button("➕ 시간 연장 (+30초)", key="global_add_time", use_container_width=True):
        st.session_state.time_left += 30
        st.toast("이용시간이 30초 연장되었습니다!")

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# --- 9. 상단 대형 네비게이션 버튼 (홈 / 메뉴 / 결제) ---
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("🏠 홈", key="nav_home", use_container_width=True):
        st.session_state.page = "홈"
        st.rerun()
with nav_col2:
    if st.button("☕ 메뉴", key="nav_menu", use_container_width=True):
        st.session_state.page = "메뉴"
        st.rerun()
with nav_col3:
    if st.button("💳 결제", key="nav_pay", use_container_width=True):
        st.session_state.page = "결제"
        st.rerun()

st.markdown("---")

# --- 10. 페이지 1: 홈 화면 ---
if st.session_state.page == "홈":
    st.markdown(f"<div class='custom-title'>{config['welcome']}</div>", unsafe_allow_html=True)
    st.markdown("<div class='custom-text'>위의 버튼이나 아래 버튼을 눌러 원하시는 메뉴를 주문해 주세요.</div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("☕ 주문하러 가기 (메뉴 선택)", key="go_to_menu", use_container_width=True):
        st.session_state.page = "메뉴"
        st.rerun()

# --- 11. 페이지 2: 메뉴 화면 ---
elif st.session_state.page == "메뉴":
    st.markdown(f"<div class='custom-title'>⭐ 인기 추천 메뉴</div>", unsafe_allow_html=True)
    st.markdown("<div class='custom-text'>자주 찾으시는 추천 메뉴입니다. 버튼을 누르면 장바구니에 담깁니다.</div>", unsafe_allow_html=True)
    
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
                add_to_cart(item['name'], item['price'])

    st.markdown("---")
    
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
                        add_to_cart(item_name, item_data['price'])

    st.markdown("---")
    
    # 장바구니 및 결제 버튼
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
        
        if st.button("💳 결제하러 가기", key="go_to_pay", use_container_width=True):
            st.session_state.page = "결제"
            st.rerun()
    else:
        st.markdown("<div class='custom-text'>아직 선택하신 메뉴가 없습니다. 위에서 메뉴를 눌러주세요.</div>", unsafe_allow_html=True)

# --- 12. 페이지 3: 결제 화면 ---
elif st.session_state.page == "결제":
    st.markdown(f"<div class='custom-title'>💳 주문 확인 및 결제</div>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.warning("선택한 메뉴가 없습니다. 상단의 '☕ 메뉴' 버튼을 눌러 메뉴를 선택해 주세요.")
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
                reset_to_home()
        with col_pay2:
            if st.button("📱 카카오페이 / 모바일 결제", key="pay_mobile"):
                st.balloons()
                st.success("간편 결제가 완료되었습니다!")
                reset_to_home()

    st.markdown("---")
    
    st.markdown("<div class='custom-sub'>🆘 도움이 필요하신가요?</div>", unsafe_allow_html=True)
    if st.button("🔔 직원 호출하기 (도움 필요)", key="call_staff"):
        st.warning("직원을 불렀습니다. 잠시만 기다려 주시면 친절히 안내해 드리겠습니다!")
