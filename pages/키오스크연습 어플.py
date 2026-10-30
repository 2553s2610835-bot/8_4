
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CAFE 24 Kiosk",
    page_icon="☕",
    layout="wide"
)

# -------------------- 다국어 번역 --------------------
LANGUAGES = {
    "한국어": "ko",
    "English": "en",
    "日本語": "ja"
}

TEXT = {
    "ko": {
        "title": "주문 방식을 선택해주세요",
        "subtitle": "이용 방법을 선택한 후 메뉴를 골라주세요.",
        "dine": "매장 이용",
        "takeout": "포장 주문",
        "dine_desc": "매장에서 편하게 즐기기",
        "takeout_desc": "포장해서 가져가기",
        "dine_btn": "매장에서 먹기",
        "takeout_btn": "포장하기",
        "menu": "메뉴",
        "coffee": "커피",
        "drink": "음료",
        "dessert": "디저트",
        "coffee_desc": "향긋한 커피로 시작하는 하루",
        "drink_desc": "시원하고 달콤한 음료",
        "dessert_desc": "달콤한 디저트로 더 행복하게",
        "cart": "주문 내역",
        "empty": "선택한 메뉴가 없습니다.",
        "choose": "메뉴를 선택해주세요.",
        "add": "담기 +",
        "total": "총 주문 금액",
        "cancel": "전체 취소",
        "order": "주문하기",
        "delete": "삭제",
        "change_order": "주문 방식 변경",
        "order_type": "주문 방식",
        "complete": "주문 연습이 완료되었습니다!",
        "receipt": "주문 확인서",
        "time": "주문 시각",
        "new_order": "새 주문 시작하기",
        "no_items": "먼저 메뉴를 선택해주세요.",
        "practice": "연습용 앱이며 실제 결제는 진행되지 않습니다.",
        "footer": "키오스크 연습 앱 · 실제 결제 기능 없음",
        "language": "언어 선택",
        "coffee_names": ["아메리카노", "카페라떼", "바닐라라떼",
                         "카라멜마끼아또", "카페모카", "콜드브루"],
        "drink_names": ["망고 요거트", "딸기 밀크티", "버블티",
                        "딸기 스무디", "초코라떼", "레몬에이드",
                        "녹차라떼", "복숭아 아이스티", "자몽에이드"],
        "dessert_names": ["딸기 케이크", "초코 브라우니", "크루아상",
                          "마카롱", "치즈케이크", "쿠키"],
        "categories": ["커피", "음료", "디저트"],
        "order_types": ["매장 이용", "포장"],
    },
    "en": {
        "title": "How would you like to order?",
        "subtitle": "Choose your order type, then select your items.",
        "dine": "Dine-in",
        "takeout": "Takeout",
        "dine_desc": "Enjoy your food in our cafe",
        "takeout_desc": "Take your order to go",
        "dine_btn": "Dine In",
        "takeout_btn": "Take Out",
        "menu": "Menu",
        "coffee": "Coffee",
        "drink": "Drinks",
        "dessert": "Desserts",
        "coffee_desc": "Start your day with great coffee",
        "drink_desc": "Refreshing and sweet drinks",
        "dessert_desc": "Make your day sweeter",
        "cart": "Your Order",
        "empty": "Your cart is empty.",
        "choose": "Please select a menu item.",
        "add": "Add +",
        "total": "Total",
        "cancel": "Clear All",
        "order": "Place Order",
        "delete": "Remove",
        "change_order": "Change Order Type",
        "order_type": "Order Type",
        "complete": "Order practice completed!",
        "receipt": "Order Receipt",
        "time": "Order Time",
        "new_order": "Start New Order",
        "no_items": "Please add an item first.",
        "practice": "Practice only. No actual payment will be processed.",
        "footer": "Kiosk Practice App · No Real Payments",
        "language": "Language",
        "coffee_names": ["Americano", "Cafe Latte", "Vanilla Latte",
                         "Caramel Macchiato", "Cafe Mocha", "Cold Brew"],
        "drink_names": ["Mango Yogurt", "Strawberry Milk Tea", "Bubble Tea",
                        "Strawberry Smoothie", "Chocolate Latte", "Lemonade",
                        "Green Tea Latte", "Peach Iced Tea", "Grapefruit Ade"],
        "dessert_names": ["Strawberry Cake", "Chocolate Brownie", "Croissant",
                          "Macaron", "Cheesecake", "Cookie"],
        "categories": ["Coffee", "Drinks", "Desserts"],
        "order_types": ["Dine-in", "Takeout"],
    },
    "ja": {
        "title": "ご注文方法をお選びください",
        "subtitle": "ご利用方法を選んでからメニューをお選びください。",
        "dine": "店内利用",
        "takeout": "テイクアウト",
        "dine_desc": "店内でゆっくりお楽しみください",
        "takeout_desc": "お持ち帰りはこちら",
        "dine_btn": "店内で食べる",
        "takeout_btn": "持ち帰り",
        "menu": "メニュー",
        "coffee": "コーヒー",
        "drink": "ドリンク",
        "dessert": "デザート",
        "coffee_desc": "香り豊かなコーヒーで素敵な一日を",
        "drink_desc": "冷たくて甘いドリンク",
        "dessert_desc": "甘いデザートをお楽しみください",
        "cart": "注文内容",
        "empty": "商品が選択されていません。",
        "choose": "メニューを選択してください。",
        "add": "追加 +",
        "total": "合計金額",
        "cancel": "すべてキャンセル",
        "order": "注文する",
        "delete": "削除",
        "change_order": "注文方法を変更",
        "order_type": "注文方法",
        "complete": "注文練習が完了しました！",
        "receipt": "注文確認書",
        "time": "注文時刻",
        "new_order": "新しい注文を始める",
        "no_items": "先にメニューを選択してください。",
        "practice": "練習用アプリです。実際の決済は行われません。",
        "footer": "キオスク練習アプリ・実際の決済なし",
        "language": "言語選択",
        "coffee_names": ["アメリカーノ", "カフェラテ", "バニララテ",
                         "キャラメルマキアート", "カフェモカ", "コールドブリュー"],
        "drink_names": ["マンゴーヨーグルト", "いちごミルクティー", "タピオカドリンク",
                        "いちごスムージー", "チョコラテ", "レモネード",
                        "抹茶ラテ", "ピーチアイスティー", "グレープフルーツエイド"],
        "dessert_names": ["いちごケーキ", "チョコブラウニー", "クロワッサン",
                          "マカロン", "チーズケーキ", "クッキー"],
        "categories": ["コーヒー", "ドリンク", "デザート"],
        "order_types": ["店内利用", "テイクアウト"],
    }
}

# 내부 메뉴 ID, 가격, 그림
MENU = {
    "coffee": [
        ("americano", 4500, "🧊☕"),
        ("latte", 5000, "☕"),
        ("vanilla", 5500, "🥛☕"),
        ("caramel", 5500, "🍮"),
        ("mocha", 5500, "🍫"),
        ("coldbrew", 5000, "🧋"),
    ],
    "drink": [
        ("mango", 6000, "🥭"),
        ("strawberry_tea", 5500, "🍓"),
        ("bubbletea", 4500, "🧋"),
        ("smoothie", 6000, "🍓"),
        ("choco", 5000, "🍫"),
        ("lemonade", 5000, "🍋"),
        ("greentea", 5500, "🍵"),
        ("peach", 4500, "🍑"),
        ("grapefruit", 5500, "🍊"),
    ],
    "dessert": [
        ("strawberry_cake", 6500, "🍰"),
        ("brownie", 4000, "🍫"),
        ("croissant", 3500, "🥐"),
        ("macaron", 2500, "🍬"),
        ("cheesecake", 6000, "🍰"),
        ("cookie", 2500, "🍪"),
    ],
}

CATEGORY_KEYS = ["coffee", "drink", "dessert"]

st.markdown("""
<style>
.stApp {background:#f4f3ef;color:#202725;}
.block-container {max-width:1500px;padding-top:1rem;}
.header {
    background:#19201f;color:white;padding:22px;
    border-radius:14px 14px 0 0;
}
.header h1 {margin:0;font-size:30px;}
.header p {margin:4px 0 0 4px;letter-spacing:3px;font-size:11px;}
.menu-card {
    background:white;border:1px solid #deded9;
    border-radius:12px;padding:12px;text-align:center;
    min-height:110px;
}
.menu-emoji {font-size:42px;}
.price {font-weight:bold;font-size:17px;}
.order-choice {
    background:white;border:1px solid #deded9;
    border-radius:16px;padding:22px 10px;text-align:center;
}
div.stButton > button {border-radius:8px;min-height:40px;}
div.stButton > button[kind="primary"] {
    background:#29443e;border-color:#29443e;color:white;
}
</style>
""", unsafe_allow_html=True)

# 세션 상태
defaults = {
    "cart": {},
    "category": "coffee",
    "receipt": None,
    "order_type": None,
    "language": "ko",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def tr(key):
    return TEXT[st.session_state.language][key]


def won(amount):
    return f"{amount:,}원" if st.session_state.language == "ko" else (
        f"¥{amount:,}" if st.session_state.language == "ja"
        else f"₩{amount:,}"
    )


def product_name(category, index):
    return tr(f"{category}_names")[index]


def add_item(item_id, name, price):
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id]["qty"] += 1
    else:
        st.session_state.cart[item_id] = {
            "name": name,
            "price": price,
            "qty": 1,
            "category": st.session_state.category,
            "index": next(
                i for i, product in enumerate(MENU[st.session_state.category])
                if product[0] == item_id
            ),
        }
    st.session_state.receipt = None


def total_price():
    return sum(
        item["price"] * item["qty"]
        for item in st.session_state.cart.values()
    )


# 상단 브랜드와 언어 선택
brand, language_col = st.columns([3, 1])

with brand:
    st.markdown("""
    <div class="header">
        <h1>☕ CAFE 24</h1>
        <p>ALWAYS FRESH</p>
        <div style="text-align:right">Fresh coffee, happy day!</div>
    </div>
    """, unsafe_allow_html=True)

with language_col:
    st.write("")
    st.write("")
    selected_language = st.selectbox(
        tr("language"),
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.values()).index(st.session_state.language),
        key="language_selector"
    )
    new_language = LANGUAGES[selected_language]

    if new_language != st.session_state.language:
        st.session_state.language = new_language
        st.rerun()

st.write("")

# 주문 방식 선택
if st.session_state.order_type is None:
    st.title(tr("title"))
    st.caption(tr("subtitle"))

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            f'<div class="order-choice"><div style="font-size:60px">🍽️</div>'
            f'<h2>{tr("dine")}</h2><p>{tr("dine_desc")}</p></div>',
            unsafe_allow_html=True
        )
        if st.button(tr("dine_btn"), type="primary",
                     use_container_width=True, key="dine_btn"):
            st.session_state.order_type = "dine"
            st.rerun()

    with col2:
        st.markdown(
            f'<div class="order-choice"><div style="font-size:60px">🥡</div>'
            f'<h2>{tr("takeout")}</h2><p>{tr("takeout_desc")}</p></div>',
            unsafe_allow_html=True
        )
        if st.button(tr("takeout_btn"), type="primary",
                     use_container_width=True, key="takeout_btn"):
            st.session_state.order_type = "takeout"
            st.rerun()

    st.divider()
    st.caption(tr("footer"))
    st.stop()

# 메뉴와 주문 내역
left, center, right = st.columns([0.8, 2.5, 1.35], gap="medium")

with left:
    st.subheader(tr("menu"))

    for category, index in zip(CATEGORY_KEYS, range(3)):
        if st.button(
            f"{['☕', '🥤', '🍰'][index]} {tr('categories')[index]}",
            key=f"category_{category}",
            use_container_width=True,
            type="primary" if st.session_state.category == category else "secondary"
        ):
            st.session_state.category = category
            st.rerun()

    st.divider()
    st.caption(f"{tr('order_type')}: {tr('dine') if st.session_state.order_type == 'dine' else tr('takeout')}")

    if st.button(tr("change_order"), use_container_width=True):
        st.session_state.order_type = None
        st.session_state.cart = {}
        st.session_state.receipt = None
        st.rerun()

with center:
    category = st.session_state.category
    category_index = CATEGORY_KEYS.index(category)

    st.title(tr("categories")[category_index])
    st.caption(tr(f"{category}_desc"))

    products = MENU[category]

    for start in range(0, len(products), 3):
        cols = st.columns(3, gap="small")

        for col, product in zip(cols, products[start:start + 3]):
            item_id, price, emoji = product
            index = next(i for i, p in enumerate(products) if p[0] == item_id)
            name = product_name(category, index)

            with col:
                st.markdown(
                    f'<div class="menu-card"><div class="menu-emoji">{emoji}</div>'
                    f'<b>{name}</b><p class="price">{won(price)}</p></div>',
                    unsafe_allow_html=True
                )

                if st.button(
                    tr("add"),
                    key=f"add_{category}_{item_id}",
                    use_container_width=True
                ):
                    add_item(item_id, name, price)
                    st.rerun()

with right:
    st.subheader(tr("cart"))
    st.caption(
        f"{tr('order_type')}: "
        f"{tr('dine') if st.session_state.order_type == 'dine' else tr('takeout')}"
    )
    st.divider()

    if not st.session_state.cart:
        st.markdown(
            f'<div style="text-align:center;padding:40px 5px;color:#858585">'
            f'<div style="font-size:45px">🛒</div>{tr("empty")}<br>{tr("choose")}</div>',
            unsafe_allow_html=True
        )
    else:
        for item_id, item in list(st.session_state.cart.items()):
            # 이름은 현재 언어로 다시 표시
            name = product_name(item["category"], item["index"])
            st.markdown(f"**{name}**")
            st.write(f"{won(item['price'])} × {item['qty']}")

            minus, quantity, plus = st.columns([1, 1, 1])

            with minus:
                if st.button("−", key=f"minus_{item_id}"):
                    item["qty"] -= 1
                    if item["qty"] <= 0:
                        del st.session_state.cart[item_id]
                    st.session_state.receipt = None
                    st.rerun()

            with quantity:
                st.write(f"**{item['qty']}**")

            with plus:
                if st.button("+", key=f"plus_{item_id}"):
                    item["qty"] += 1
                    st.session_state.receipt = None
                    st.rerun()

            if st.button(tr("delete"), key=f"delete_{item_id}",
                         use_container_width=True):
                del st.session_state.cart[item_id]
                st.session_state.receipt = None
                st.rerun()

            st.divider()

    st.markdown(f"### {tr('total')}")
    st.markdown(f"## {won(total_price())}")

    if st.button(tr("cancel"), use_container_width=True):
        st.session_state.cart = {}
        st.session_state.receipt = None
        st.rerun()

    if st.button(tr("order"), type="primary", use_container_width=True):
        if not st.session_state.cart:
            st.warning(tr("no_items"))
        else:
            st.session_state.receipt = {
                "items": {
                    k: v.copy() for k, v in st.session_state.cart.items()
                },
                "total": total_price(),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "order_type": st.session_state.order_type,
            }
            st.rerun()

# 영수증
if st.session_state.receipt:
    receipt = st.session_state.receipt

    st.divider()
    st.success(tr("complete"))
    st.subheader(tr("receipt"))
    st.write(f"{tr('time')}: {receipt['time']}")

    order_label = tr("dine") if receipt["order_type"] == "dine" else tr("takeout")
    st.write(f"{tr('order_type')}: **{order_label}**")

    for item_id, item in receipt["items"].items():
        name = product_name(item["category"], item["index"])
        st.write(
            f"- {name} × {item['qty']}: "
            f"{won(item['price'] * item['qty'])}"
        )

    st.markdown(f"### {tr('total')}: {won(receipt['total'])}")
    st.info(tr("practice"))

    if st.button(tr("new_order")):
        st.session_state.cart = {}
        st.session_state.receipt = None
        st.session_state.order_type = None
        st.session_state.category = "coffee"
        st.rerun()

st.divider()
st.caption(f"CAFE 24 · {tr('footer')}")
