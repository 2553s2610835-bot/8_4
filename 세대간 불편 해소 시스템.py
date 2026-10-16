
import streamlit as st

st.set_page_config(
    page_title="천천히 키오스크",
    page_icon="🌼",
    layout="centered"
)

# 화면 디자인
st.markdown("""
<style>
.stApp {
    background-color: #F0F6FF;
}
h1, h2, h3, p, label {
    color: #23415B;
}
div.stButton > button {
    width: 100%;
    min-height: 60px;
    font-size: 20px;
    border-radius: 12px;
    border: 2px solid #8BBCE8;
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🌼 천천히 키오스크")
st.subheader("천천히 보고, 편하게 주문하세요!")
st.write("어르신이 편리하게 사용할 수 있는 사용자 맞춤형 키오스크입니다.")

# 사용자 맞춤 설정
st.header("⚙️ 나에게 맞게 설정하기")

big_text = st.checkbox("🔎 큰 글씨 사용하기")
easy_mode = st.checkbox("💬 쉬운 말 사용하기")

if big_text:
    st.markdown("""
    <style>
    html, body, p, label, button {
        font-size: 24px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if easy_mode:
    st.info("원하는 음식을 누르고 주문하기 버튼을 눌러 주세요!")
else:
    st.info("메뉴를 선택한 후 주문 내역을 확인해 주세요.")

# 메뉴
st.header("🍽️ 메뉴 선택")

menus = {
    "🍙 김밥": 3500,
    "🍜 라면": 4500,
    "🍛 돈가스": 9000,
    "🥗 비빔밥": 8000,
    "💧 물": 1000,
    "☕ 커피": 2500
}

if "cart" not in st.session_state:
    st.session_state.cart = {}

for name, price in menus.items():
    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(f"**{name}**")
        st.write(f"{price:,}원")

    with col2:
        if st.button("선택", key=name):
            st.session_state.cart[name] = (
                st.session_state.cart.get(name, 0) + 1
            )

# 주문 내역
st.header("🛒 내 주문 목록")

total = 0

if st.session_state.cart:
    for name, count in st.session_state.cart.items():
        price = menus[name]
        subtotal = price * count
        total += subtotal
        st.write(
            f"{name} × {count}개 = {subtotal:,}원"
        )
else:
    st.write("아직 선택한 메뉴가 없습니다.")

st.markdown("---")
st.subheader(f"💰 총금액: {total:,}원")

# 음성 안내
if st.button("🔊 음성 안내 듣기"):
    st.info(
        "음성 안내는 브라우저의 음성 기능과 연결해야 합니다. "
        "아래 안내문을 읽어 주세요: 원하는 메뉴를 선택해 주세요."
    )

# 주문 확인 및 취소
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ 주문 확인"):
        if total > 0:
            st.success(
                f"주문 확인 완료! 총 {total:,}원입니다."
            )
            st.caption("실제 결제는 진행되지 않습니다.")
        else:
            st.warning("먼저 메뉴를 선택해 주세요.")

with col2:
    if st.button("❌ 주문 취소"):
        st.session_state.cart = {}
        st.rerun()

