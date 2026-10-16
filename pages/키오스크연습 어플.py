
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CAFE DAY | 키오스크</title>

<style>
:root {
  --main: #426b55;
  --light: #edf3ee;
  --cream: #faf8f2;
  --text: #292f2b;
  --muted: #777e78;
  --white: #ffffff;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont,
    "Malgun Gothic", sans-serif;
  background: var(--cream);
  color: var(--text);
}

button {
  font: inherit;
  cursor: pointer;
}

button:focus-visible {
  outline: 3px solid #8db49a;
  outline-offset: 3px;
}

header {
  background: var(--white);
  padding: 20px 5%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e8e8e2;
}

.logo {
  color: var(--main);
  font-size: 25px;
  font-weight: 900;
  letter-spacing: 1px;
}

header small {
  color: var(--muted);
}

main {
  max-width: 1100px;
  margin: 30px auto;
  padding: 0 18px;
}

.welcome {
  margin-bottom: 25px;
}

.welcome h1 {
  font-size: clamp(25px, 4vw, 36px);
  margin: 0 0 8px;
}

.welcome p {
  color: var(--muted);
  margin: 0;
}

.order-type {
  display: flex;
  gap: 10px;
  margin: 22px 0;
}

.type-btn, .category-btn {
  border: 1px solid #d9dfd9;
  background: white;
  border-radius: 12px;
  padding: 12px 20px;
}

.type-btn.active, .category-btn.active {
  background: var(--main);
  color: white;
  border-color: var(--main);
}

.layout {
  display: grid;
  grid-template-columns: minmax(0, 1.6fr) minmax(280px, 1fr);
  gap: 22px;
  align-items: start;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
}

.menu {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.menu-card {
  background: white;
  border: 1px solid #e8e9e3;
  border-radius: 16px;
  overflow: hidden;
  text-align: left;
  padding: 0;
  color: var(--text);
  transition: transform .15s;
}

.menu-card:hover {
  transform: translateY(-3px);
}

.menu-card:active {
  transform: scale(.98);
}

.food-picture {
  background: var(--light);
  min-height: 125px;
  display: grid;
  place-items: center;
  font-size: 60px;
}

.food-info {
  padding: 14px;
}

.food-info h3 {
  margin: 0 0 7px;
  font-size: 17px;
}

.food-info p {
  margin: 0;
  color: var(--main);
  font-weight: 800;
}

.add-label {
  display: block;
  margin-top: 12px;
  font-size: 13px;
  color: var(--muted);
}

.cart {
  background: white;
  border: 1px solid #e6e8e1;
  border-radius: 18px;
  padding: 20px;
  position: sticky;
  top: 12px;
}

.cart h2 {
  margin: 0 0 5px;
}

.cart-subtitle {
  color: var(--muted);
  font-size: 13px;
  margin-bottom: 18px;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding: 14px 0;
  border-bottom: 1px solid #eeeeea;
}

.cart-name {
  font-weight: 700;
  margin-bottom: 7px;
}

.cart-price {
  color: var(--muted);
  font-size: 13px;
}

.quantity {
  display: flex;
  align-items: center;
  gap: 9px;
  margin-top: 8px;
}

.quantity button {
  width: 29px;
  height: 29px;
  border: 1px solid #dfe3dc;
  background: var(--cream);
  border-radius: 8px;
}

.delete-btn {
  border: 0;
  background: none;
  color: #a34c4c;
  font-size: 12px;
  margin-top: 5px;
  padding: 3px;
}

.empty {
  text-align: center;
  padding: 30px 5px;
  color: var(--muted);
}

.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 22px 0;
  font-weight: 800;
}

.total-price {
  color: var(--main);
  font-size: 25px;
}

.primary-btn, .secondary-btn {
  width: 100%;
  padding: 15px;
  border-radius: 12px;
  font-weight: 800;
}

.primary-btn {
  background: var(--main);
  color: white;
  border: none;
}

.primary-btn:disabled {
  opacity: .45;
  cursor: not-allowed;
}

.secondary-btn {
  background: white;
  color: var(--text);
  border: 1px solid #ddd;
  margin-top: 9px;
}

.notice {
  color: var(--muted);
  font-size: 12px;
  text-align: center;
  line-height: 1.6;
  margin-top: 13px;
}

footer {
  text-align: center;
  padding: 30px;
  color: var(--muted);
  font-size: 12px;
}

.screen {
  display: none;
  max-width: 550px;
  margin: 55px auto;
  padding: 30px 20px;
  background: white;
  border-radius: 20px;
  text-align: center;
}

.screen h1 {
  color: var(--main);
}

.receipt {
  text-align: left;
  background: var(--cream);
  padding: 18px;
  border-radius: 12px;
  margin: 22px 0;
  line-height: 1.9;
}

@media (max-width: 720px) {
  main {
    margin-top: 22px;
    padding: 0 12px;
  }

  .layout {
    grid-template-columns: 1fr;
  }

  .cart {
    position: static;
  }

  .food-picture {
    min-height: 100px;
    font-size: 48px;
  }

  .food-info {
    padding: 11px;
  }

  .type-btn, .category-btn {
    padding: 11px 15px;
  }
}
</style>
</head>

<body>

<header>
  <div>
    <div class="logo">CAFE DAY</div>
    <small>YOUR DAILY MOMENT</small>
  </div>
  <small>셀프 주문 키오스크</small>
</header>

<main id="orderScreen">
  <section class="welcome">
    <h1>무엇을 주문하시겠어요?</h1>
    <p>메뉴를 선택하고 장바구니에서 주문을 확인해 주세요.</p>
  </section>

  <div class="order-type" aria-label="주문 방식">
    <button class="type-btn active"
      data-type="매장" onclick="setType('매장', this)">
      매장 식사
    </button>
    <button class="type-btn"
      data-type="포장" onclick="setType('포장', this)">
      포장하기
    </button>
  </div>

  <div class="layout">
    <section>
      <nav class="categories" aria-label="메뉴 카테고리">
        <button class="category-btn active"
          onclick="setCategory('전체', this)">전체 메뉴</button>
        <button class="category-btn"
          onclick="setCategory('커피', this)">커피</button>
        <button class="category-btn"
          onclick="setCategory('음료', this)">음료</button>
        <button class="category-btn"
          onclick="setCategory('디저트', this)">디저트</button>
      </nav>

      <div class="menu" id="menu"></div>
    </section>

    <aside class="cart">
      <h2>주문 내역</h2>
      <div class="cart-subtitle" id="cartSubtitle">
        매장 식사 · 0개 선택
      </div>

      <div id="cartItems"></div>

      <div class="total-row">
        <span>총 주문 금액</span>
        <span class="total-price" id="total">0원</span>
      </div>

      <button class="primary-btn" id="orderButton"
        onclick="confirmOrder()" disabled>
        주문하기
      </button>
      <button class="secondary-btn" onclick="clearCart()">
        전체 취소
      </button>

      <p class="notice">
        이 사이트는 주문 연습용입니다.<br>
        실제 결제는 진행되지 않습니다.
      </p>
    </aside>
  </div>
</main>

<section class="screen" id="confirmScreen">
  <h1>주문을 확인해 주세요</h1>
  <p>선택한 메뉴와 금액이 맞는지 확인해 주세요.</p>
  <div class="receipt" id="confirmReceipt"></div>
  <button class="primary-btn" onclick="finishOrder()">
    주문 확정
  </button>
  <button class="secondary-btn" onclick="backToOrder()">
    메뉴로 돌아가기
  </button>
</section>

<section class="screen" id="completeScreen">
  <div style="font-size:65px">✓</div>
  <h1>주문이 완료되었습니다!</h1>
  <p>키오스크 주문 연습을 완료했어요.</p>
  <div class="receipt" id="completeReceipt"></div>
  <button class="primary-btn" onclick="restart()">
    처음으로 돌아가기
  </button>
</section>

<footer>
  CAFE DAY · KIOSK PRACTICE
</footer>

<script>
const products = [
  {id: 1, name: "아메리카노", price: 2500, emoji: "☕", category: "커피"},
  {id: 2, name: "카페라떼", price: 3500, emoji: "🥛", category: "커피"},
  {id: 3, name: "바닐라라떼", price: 4000, emoji: "🧋", category: "커피"},
  {id: 4, name: "카페모카", price: 4200, emoji: "🍫", category: "커피"},
  {id: 5, name: "딸기라떼", price: 4300, emoji: "🍓", category: "음료"},
  {id: 6, name: "레몬에이드", price: 4000, emoji: "🍋", category: "음료"},
  {id: 7, name: "초코케이크", price: 4800, emoji: "🍰", category: "디저트"},
  {id: 8, name: "크루아상", price: 3200, emoji: "🥐", category: "디저트"}
];

let cart = {};
let orderType = "매장";
let category = "전체";
let orderNumber = 1001;

const money = value => value.toLocaleString("ko-KR") + "원";

function setType(type, button) {
  orderType = type;

  document.querySelectorAll(".type-btn").forEach(btn => {
    btn.classList.toggle("active", btn === button);
  });

  renderCart();
}

function setCategory(value, button) {
  category = value;

  document.querySelectorAll(".category-btn").forEach(btn => {
    btn.classList.toggle("active", btn === button);
  });

  renderMenu();
}

function renderMenu() {
  const filtered = category === "전체"
    ? products
    : products.filter(item => item.category === category);

  document.getElementById("menu").innerHTML = filtered.map(item => `
    <button class="menu-card"
      onclick="addItem(${item.id})"
      aria-label="${item.name}, ${money(item.price)}, 장바구니에 담기">
      <div class="food-picture">${item.emoji}</div>
      <div class="food-info">
        <h3>${item.name}</h3>
        <p>${money(item.price)}</p>
        <span class="add-label">＋ 장바구니 담기</span>
      </div>
    </button>
  `).join("");
}

function addItem(id) {
  cart[id] = (cart[id] || 0) + 1;
  renderCart();
}

function changeQuantity(id, amount) {
  cart[id] = (cart[id] || 0) + amount;

  if (cart[id] <= 0) {
    delete cart[id];
  }

  renderCart();
}

function removeItem(id) {
  delete cart[id];
  renderCart();
}

function getTotal() {
  return products.reduce((sum, item) => {
    return sum + item.price * (cart[item.id] || 0);
  }, 0);
}

function getCount() {
  return Object.values(cart).reduce((sum, qty) => sum + qty, 0);
}

function renderCart() {
  const selected = products.filter(item => cart[item.id] > 0);
  const container = document.getElementById("cartItems");

  document.getElementById("cartSubtitle").textContent =
    `${orderType} · ${getCount()}개 선택`;

  if (selected.length === 0) {
    container.innerHTML =
      '<div class="empty">장바구니가 비어 있어요.<br>원하는 메뉴를 선택해 주세요.</div>';
  } else {
    container.innerHTML = selected.map(item => `
      <div class="cart-item">
        <div>
          <div class="cart-name">${item.emoji} ${item.name}</div>
          <div class="cart-price">${money(item.price)} / 개</div>
          <div class="quantity">
            <button onclick="changeQuantity(${item.id}, -1)"
              aria-label="${item.name} 수량 줄이기">−</button>
            <span>${cart[item.id]}개</span>
            <button onclick="changeQuantity(${item.id}, 1)"
              aria-label="${item.name} 수량 늘리기">＋</button>
          </div>
        </div>
        <div style="text-align:right">
          <strong>${money(item.price * cart[item.id])}</strong>
          <br>
          <button class="delete-btn"
            onclick="removeItem(${item.id})">삭제</button>
        </div>
      </div>
    `).join("");
  }

  document.getElementById("total").textContent = money(getTotal());
  document.getElementById("orderButton").disabled = getCount() === 0;
}

function makeReceipt(numberText) {
  const lines = products
    .filter(item => cart[item.id] > 0)
    .map(item => `
      <div>${item.name} × ${cart[item.id]}
      <span style="float:right">${money(item.price * cart[item.id])}</span></div>
    `).join("");

  return `
    <div><strong>${numberText}</strong></div>
    <div>주문 방식: ${orderType}</div>
    <hr>
    ${lines}
    <hr>
    <strong>총 금액:
      <span style="float:right">${money(getTotal())}</span>
    </strong>
  `;
}

function confirmOrder() {
  if (getCount() === 0) return;

  document.getElementById("confirmReceipt").innerHTML =
    makeReceipt("주문 내역");
  showScreen("confirmScreen");
}

function finishOrder() {
  document.getElementById("completeReceipt").innerHTML =
    makeReceipt("주문 번호: " + orderNumber);
  orderNumber++;
  showScreen("completeScreen");
}

function backToOrder() {
  showScreen("orderScreen");
}

function clearCart() {
  if (getCount() === 0) return;

  if (confirm("장바구니를 모두 비울까요?")) {
    cart = {};
    renderCart();
  }
}

function restart() {
  cart = {};
  orderType = "매장";
  category = "전체";

  document.querySelectorAll(".type-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.type === "매장");
  });

  document.querySelectorAll(".category-btn").forEach(btn => {
    btn.classList.toggle("active",
      btn.textContent.trim() === "전체 메뉴");
  });

  renderMenu();
  renderCart();
  showScreen("orderScreen");
}

function showScreen(id) {
  document.getElementById("orderScreen").style.display =
    id === "orderScreen" ? "block" : "none";

  document.getElementById("confirmScreen").style.display =
    id === "confirmScreen" ? "block" : "none";

  document.getElementById("completeScreen").style.display =
    id === "completeScreen" ? "block" : "none";

  window.scrollTo({top: 0, behavior: "smooth"});
}

renderMenu();
renderCart();
</script>

</body>
</html>

