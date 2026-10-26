
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CAFE 24 키오스크",
    page_icon="☕",
    layout="wide"
)

MENU = {
    "커피": [
        ("아메리카노", 4500, "🧊☕"),
        ("카페라떼", 5000, "☕"),
        ("바닐라라떼", 5500, "🥛☕"),
        ("카라멜마끼아또", 5500, "🍮"),
        ("카페모카", 5500, "🍫"),
        ("콜드브루", 5000, "🧋"),
    ],
    "음료": [
        ("망고요거트", 6000, "🥭"),
        ("딸기주얼리 밀크티", 5500, "🍓"),
        ("또팡", 4500, "🧋"),
        ("딸기 스무디", 6000, "🍓"),
        ("초코라떼", 5000, "🍫"),
        ("레몬에이드", 5000, "🍋"),
        ("녹차라떼", 5500, "🍵"),
        ("복숭아 아이스티", 4500, "🍑"),
        ("자몽에이드", 5500, "🍊"),
    ],
    "디저트": [
        ("딸기 케이크", 6500, "🍰"),
        ("초코 브라우니", 4000, "🍫"),
        ("크루아상", 3500, "🥐"),
        ("마카롱", 2500, "🍬"),
        ("치즈케이크", 6000, "🍰"),
        ("쿠키", 2500, "🍪"),
    ],
}

st.markdown("""
<style>
.stApp {
    background-color: #f4f3ef;
    color: #202725;
}
.block-container {
    max-width: 1500px;
    padding-top: 1rem;
}
.header {
    background: #19201f;
    color: white;
    padding: 22px;
    border-radius: 14px 14px 0 0;
}
.header h1 {
    margin: 0;
    font-size: 30px;
}
.header p {
    margin: 4px 0 0 4px;
    letter-spacing: 3px;
    font-size: 11px;
}
.menu-card {
    background: white;
    border: 1px solid #deded9;
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    min-height: 115px;
}
.menu-emoji {
    font-size: 42px;
}
.price {
    font-weight: bold;
    font-size: 17px;
}
div.stButton > button {
    border-radius: 8px;
    min-height: 40px;
}
div.stButton > button[kind="primary"] {
    background: #29443e;
    border-color: #29443e;
    color: white;
}
.order-choice {
    background: white;
    border: 1px solid #deded9;
    border-radius: 16px;
    padding: 25px 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 주문 상태
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "category" not in st.session_state:
    st.session_state.category = "커피"

if "receipt" not in st.session_state:
    st.session_state.receipt = None

if "order_type" not in st.session_state:
    st.session_state.order_type = None


def won(amount):
    return f"{amount:,}원"


def add_item(name, price):
    if name in st.session_state.cart:
        st.session_state.cart[name]["qty"] += 1
    else:
        st.session_state.cart[name] = {
            "price": price,
            "qty": 1
        }
    st.session_state.receipt = None


def total_price():
    return sum(
        item["price"] * item["qty"]
        for item in st.session_state.cart.values()
    )


# 상단 헤더
st.markdown("""
<div class="header">
    <h1>☕ CAFE 24</h1>
    <p>ALWAYS FRESH</p>
    <div style="text-align:right">
        맛있는 커피와 행복한 하루 되세요
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# 첫 화면: 주문 방식 선택
if st.session_state.order_type is None:
    st.title("주문 방식을 선택해주세요")
    st.caption("이용하실 방법을 선택한 후 메뉴를 골라주세요.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="order-choice">
            <div style="font-size:65px">🍽️</div>
            <h2>매장 이용</h2>
            <p>카페 안에서 편하게 즐기기</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "매장에서 먹기",
            key="dine_in",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.order_type = "매장 이용"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="order-choice">
            <div style="font-size:65px">🥡</div>
            <h2>포장 주문</h2>
            <p>테이크아웃으로 가져가기</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "포장하기",
            key="takeout",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.order_type = "포장"
            st.rerun()

    st.divider()
    st.caption("CAFE 24 · 키오스크 연습 앱")
    st.stop()


# 메뉴 화면
left, center, right = st.columns(
    [0.8, 2.5, 1.35],
    gap="medium"
)

with left:
    st.subheader("메뉴")

    for category, emoji in [
        ("커피", "☕"),
        ("음료", "🥤"),
        ("디저트", "🍰")
    ]:
        if st.button(
            f"{emoji} {category}",
            key=f"category_{category}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.category == category
                else "secondary"
            )
        ):
            st.session_state.category = category
            st.rerun()

    st.divider()
    st.caption(f"주문 방식: {st.session_state.order_type}")

    if st.button("주문 방식 변경", use_container_width=True):
        st.session_state.order_type = None
        st.session_state.cart = {}
        st.session_state.receipt = None
        st.rerun()

with center:
    category = st.session_state.category

    st.title(category)

    descriptions = {
        "커피": "향긋한 커피로 시작하는 하루",
        "음료": "시원하고 달콤한 음료",
        "디저트": "달콤한 디저트로 더 행복하게"
    }

    st.caption(descriptions[category])

    products = MENU[category]

    for start in range(0, len(products), 3):
        columns = st.columns(3, gap="small")

        for col, product in zip(
            columns,
            products[start:start + 3]
        ):
            name, price, emoji = product

            with col:
                st.markdown(
                    f"""
                    <div class="menu-card">
                        <div class="menu-emoji">{emoji}</div>
                        <b>{name}</b>
                        <p class="price">{won(price)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "담기 +",
                    key=f"add_{category}_{name}",
                    use_container_width=True
                ):
                    add_item(name, price)
                    st.rerun()

with right:
    st.subheader("주문 내역")
    st.caption(f"이용 방법: {st.session_state.order_type}")
    st.divider()

    if not st.session_state.cart:
        st.markdown("""
        <div style="text-align:center;padding:45px 5px;color:#858585">
            <div style="font-size:45px">🛒</div>
            선택한 메뉴가 없습니다.<br>
            메뉴를 선택해주세요.
        </div>
        """, unsafe_allow_html=True)

    else:
        for name, item in list(st.session_state.cart.items()):
            st.markdown(f"**{name}**")
            st.write(
                f"{won(item['price'])} × {item['qty']}개"
            )

            minus, quantity, plus = st.columns([1, 1, 1])

            with minus:
                if st.button("−", key=f"minus_{name}"):
                    item["qty"] -= 1

                    if item["qty"] <= 0:
                        del st.session_state.cart[name]

                    st.session_state.receipt = None
                    st.rerun()

            with quantity:
                st.write(f"**{item['qty']}**")

            with plus:
                if st.button("+", key=f"plus_{name}"):
                    item["qty"] += 1
                    st.session_state.receipt = None
                    st.rerun()

            if st.button(
                "삭제",
                key=f"delete_{name}",
                use_container_width=True
            ):
                del st.session_state.cart[name]
                st.session_state.receipt = None
                st.rerun()

            st.divider()

    st.markdown("### 총 주문 금액")
    st.markdown(f"## {won(total_price())}")

    if st.button("전체 취소", use_container_width=True):
        st.session_state.cart = {}
        st.session_state.receipt = None
        st.rerun()

    if st.button(
        "주문하기",
        type="primary",
        use_container_width=True
    ):
        if not st.session_state.cart:
            st.warning("먼저 메뉴를 선택해주세요.")
        else:
            st.session_state.receipt = {
                "items": {
                    name: item.copy()
                    for name, item in st.session_state.cart.items()
                },
                "total": total_price(),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "order_type": st.session_state.order_type
            }
            st.rerun()


# 주문 완료 영수증
if st.session_state.receipt:
    receipt = st.session_state.receipt

    st.divider()
    st.success("주문 연습이 완료되었습니다!")

    st.subheader("주문 확인서")
    st.write(f"주문 시각: {receipt['time']}")
    st.write(f"주문 방식: **{receipt['order_type']}**")

    for name, item in receipt["items"].items():
        st.write(
            f"- {name} × {item['qty']}개: "
            f"{won(item['price'] * item['qty'])}"
        )

    st.markdown(f"### 총 주문 금액: {won(receipt['total'])}")
    st.info("연습용 앱이며 실제 결제는 진행되지 않습니다.")

    if st.button("새 주문 시작하기"):
        st.session_state.cart = {}
        st.session_state.receipt = None
        st.session_state.order_type = None
        st.session_state.category = "커피"
        st.rerun()

st.divider()
st.caption("CAFE 24 · 키오스크 연습 앱 · 실제 결제 기능 없음")
