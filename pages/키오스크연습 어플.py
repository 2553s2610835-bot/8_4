import streamlit as st
import time

st.set_page_config
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CAFE 24 키오스크</title>
<style>
*{box-sizing:border-box}
:root{--green:#29483f;--cream:#f7f6f1;--line:#deded7}
body{margin:0;background:#202522;font-family:Arial,sans-serif;color:#252923}
button{font:inherit;cursor:pointer;touch-action:manipulation}
button:focus-visible{outline:3px solid #e2a34b}
header{height:85px;background:#202b27;color:white;display:flex;
align-items:center;justify-content:space-between;padding:0 25px}
.logo{font-size:27px;font-weight:900;letter-spacing:2px}
.logo small{display:block;font-size:10px;letter-spacing:4px;text-align:center}
main{display:grid;grid-template-columns:100px minmax(0,1fr) 310px;
height:calc(100dvh - 145px);min-height:540px;background:var(--cream)}
nav{border-right:1px solid var(--line);background:#fff}
nav button{width:100%;min-height:88px;border:0;border-bottom:1px solid var(--line);
background:white;color:#555;font-weight:bold;display:flex;flex-direction:column;
align-items:center;justify-content:center;gap:7px}
nav button span{font-size:25px}
nav button.active{background:var(--green);color:white}
.catalog{padding:20px;overflow:auto}
.heading{margin:0 0 5px;font-size:25px}
.subtitle{margin:0 0 18px;color:#72766e;font-size:14px}
.products{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.product{background:white;border:1px solid var(--line);border-radius:10px;
overflow:hidden;display:flex;flex-direction:column;min-width:0}
.product img{width:100%;height:115px;object-fit:cover;background:#eee}
.info{padding:10px;display:flex;flex-direction:column;flex:1;gap:8px}
.name{font-weight:bold;font-size:15px;min-height:34px}
.price{font-weight:bold;font-size:16px}
.add{background:var(--green);color:white;border:0;border-radius:6px;
padding:10px 3px;font-weight:bold;margin-top:auto}
.add:active,.primary:active{transform:scale(.98)}
.cart{background:#fff;border-left:1px solid var(--line);display:flex;
flex-direction:column;min-height:0}
.cart h2{font-size:23px;margin:0;padding:20px;border-bottom:1px solid var(--line)}
.cart-list{padding:12px 16px;overflow:auto;flex:1}
.empty{text-align:center;color:#888;padding:65px 5px;line-height:2}
.cart-item{padding:12px 0;border-bottom:1px solid #eee}
.cart-top{display:flex;justify-content:space-between;gap:8px;font-weight:bold}
.qty{display:flex;align-items:center;gap:12px;margin-top:10px}
.qty button{width:32px;height:32px;border:1px solid #ddd;background:white;border-radius:5px}
.cart-bottom{padding:16px;border-top:1px solid var(--line)}
.total{display:flex;justify-content:space-between;align-items:center;
font-weight:bold;margin-bottom:14px}
.total strong{font-size:26px}
.secondary,.primary{width:100%;padding:15px;border-radius:8px;font-weight:bold}
.secondary{background:white;border:1px solid #aaa;color:var(--green);margin-bottom:9px}
.primary{background:var(--green);color:white;border:0;font-size:19px}
footer{height:60px;background:#202b27;color:white;display:flex;
align-items:center;justify-content:space-between;padding:0 22px;font-size:13px}
footer button{background:transparent;color:white;border:0;padding:8px}
.modal{position:fixed;inset:0;background:#0009;display:none;align-items:center;
justify-content:center;padding:20px;z-index:5}
.modal.show{display:flex}
.dialog{background:white;border-radius:16px;padding:25px;width:min(430px,100%);
text-align:center;box-shadow:0 10px 40px #0003}
.dialog h2{margin-top:0}
.dialog button{margin-top:10px}
.option{display:flex;justify-content:center;gap:12px;margin:18px 0}
.option button{padding:12px 22px;border:1px solid #bbb;border-radius:8px;background:white}
.option button.selected{background:var(--green);color:white}
@media(min-width:1000px){
 main{grid-template-columns:130px minmax(0,1fr) 340px}
 .product img{height:150px}
 .catalog{padding:25px}
}
@media(max-width:600px){
 header{height:65px;padding:0 12px}
 .logo{font-size:21px}
 main{height:auto;min-height:calc(100dvh - 115px);
 grid-template-columns:65px minmax(0,1fr)}
 nav button{font-size:12px;min-height:76px}
 nav button span{font-size:22px}
 .catalog{padding:12px;min-width:0}
 .heading{font-size:21px}
 .products{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
 .product img{height:105px}
 .info{padding:8px}
 .name{font-size:13px}
 .price{font-size:14px}
 .cart{grid-column:1/-1;border-top:2px solid var(--green)}
 .cart h2{padding:14px;font-size:20px}
 .cart-list{max-height:240px}
 .empty{padding:25px}
 footer{height:50px;padding:0 8px;font-size:11px}
 footer button{padding:5px;font-size:11px}
}
</style>
</head>
<body>
<header>
  <div class="logo">☕ CAFE 24<small>ALWAYS FRESH</small></div>
  <div style="font-size:12px;text-align:right">맛있는 커피와<br>행복한 하루</div>
</header>

<main>
<nav id="categories">
  <button class="active" data-cat="커피"><span>☕</span>커피</button>
  <button data-cat="음료"><span>🥤</span>음료</button>
  <button data-cat="디저트"><span>🍰</span>디저트</button>
</nav>

<section class="catalog">
  <h1 class="heading" id="categoryTitle">커피</h1>
  <p class="subtitle" id="subtitle">향긋한 커피로 시작하는 하루</p>
  <div class="products" id="products"></div>
</section>

<aside class="cart">
  <h2>주문 내역</h2>
  <div class="cart-list" id="cartList"></div>
  <div class="cart-bottom">
    <div class="total"><span>총 주문 금액</span><strong id="total">0원</strong></div>
    <button class="secondary" id="clear">전체 취소</button>
    <button class="primary" id="checkout">주문하기</button>
  </div>
</aside>
</main>

<footer>
  <button id="home">⌂ 처음으로</button>
  <div>
    <button id="language">◎ 언어변경</button>
    <button id="help">⚙ 도움말</button>
  </div>
</footer>

<div class="modal" id="modal">
  <div class="dialog" id="dialog"></div>
</div>

<script>
const menus = [
 {id:1,name:"아메리카노",price:2500,cat:"커피",emoji:"☕",color:"#b8c8bf"},
 {id:2,name:"카페라떼",price:3500,cat:"커피",emoji:"🥛",color:"#e6d4bd"},
 {id:3,name:"바닐라라떼",price:4000,cat:"커피",emoji:"🧋",color:"#d9c3a8"},
 {id:4,name:"카라멜마끼아또",price:4000,cat:"커피",emoji:"☕",color:"#d6b18a"},
 {id:5,name:"카페모카",price:4500,cat:"커피",emoji:"🍫",color:"#c7a28c"},
 {id:6,name:"콜드브루",price:3500,cat:"커피",emoji:"🧊",color:"#c6d2d0"},
 {id:7,name:"딸기주스",price:4000,cat:"음료",emoji:"🍓",color:"#efc1c3"},
 {id:8,name:"레몬에이드",price:4000,cat:"음료",emoji:"🍋",color:"#e8e3ad"},
 {id:9,name:"초코스무디",price:4500,cat:"음료",emoji:"🍫",color:"#c9b4a7"},
 {id:10,name:"치즈케이크",price:4500,cat:"디저트",emoji:"🍰",color:"#e9d7ac"},
 {id:11,name:"초코케이크",price:5000,cat:"디저트",emoji:"🍫",color:"#c7a28c"},
 {id:12,name:"크루아상",price:3000,cat:"디저트",emoji:"🥐",color:"#e7c58d"}
];

let cart = {};
let category = "커피";
let takeout = "매장";
let english = false;

const money = n => n.toLocaleString("ko-KR")+"원";

function renderProducts(){
 const list = menus.filter(m=>m.cat===category);
 document.getElementById("categoryTitle").textContent =
   english ? category==="커피"?"Coffee":category==="음료"?"Drinks":"Desserts" : category;
 document.getElementById("subtitle").textContent =
   category==="커피"?"향긋한 커피로 시작하는 하루":
   category==="음료"?"시원하고 달콤한 음료":"달콤한 디저트";
 document.getElementById("products").innerHTML=list.map(m=>`
 <article class="product">
   <img alt="${m.name}" src="https://placehold.co/400x280/${m.color.slice(1)}/333333?text=${encodeURIComponent(m.emoji)}"
     onerror="this.style.display='none'">
   <div class="info">
     <div class="name">${m.name}</div>
     <div class="price">${money(m.price)}</div>
     <button class="add" data-add="${m.id}">담기</button>
   </div>
 </article>`).join("");
}

function renderCart(){
 const entries=Object.entries(cart);
 document.getElementById("cartList").innerHTML=entries.length?
 entries.map(([id,qty])=>{
  const m=menus.find(x=>x.id===Number(id));
  return `<div class="cart-item">
    <div class="cart-top"><span>${m.name}</span><span>${money(m.price*qty)}</span></div>
    <div class="qty">
      <button data-change="${id}" data-step="-1" aria-label="수량 줄이기">−</button>
      <span>${qty}개</span>
      <button data-change="${id}" data-step="1" aria-label="수량 늘리기">＋</button>
      <button data-remove="${id}" style="margin-left:auto;width:auto;padding:0 8px">삭제</button>
    </div>
  </div>`;
 }).join(""):`<div class="empty">🛒<br>선택한 메뉴가 없습니다.<br>메뉴를 선택해주세요.</div>`;

 const total=entries.reduce((sum,[id,qty])=>
  sum+menus.find(m=>m.id===Number(id)).price*qty,0);
 document.getElementById("total").textContent=money(total);
}

function addItem(id){
 cart[id]=(cart[id]||0)+1;
 renderCart();
}
function changeQty(id,step){
 cart[id]=(cart[id]||0)+step;
 if(cart[id]<=0) delete cart[id];
 renderCart();
}
function clearCart(){
 cart={};
 renderCart();
}

function openModal(html){
 document.getElementById("dialog").innerHTML=html;
 document.getElementById("modal").classList.add("show");
}
function closeModal(){
 document.getElementById("modal").classList.remove("show");
}

document.getElementById("categories").addEventListener("click",e=>{
 const b=e.target.closest("[data-cat]");
 if(!b)return;
 category=b.dataset.cat;
 document.querySelectorAll("#categories button").forEach(x=>
  x.classList.toggle("active",x===b));
 renderProducts();
});

document.getElementById("products").addEventListener("click",e=>{
 const b=e.target.closest("[data-add]");
 if(b)addItem(Number(b.dataset.add));
});

document.getElementById("cartList").addEventListener("click",e=>{
 const q=e.target.closest("[data-change]");
 const r=e.target.closest("[data-remove]");
 if(q)changeQty(q.dataset.change,Number(q.dataset.step));
 if(r){delete cart[r.dataset.remove];renderCart();}
});

document.getElementById("clear").onclick=()=>{
 if(!Object.keys(cart).length){
  openModal("<h2>장바구니가 비어 있습니다.</h2><button class='primary' id='ok'>확인</button>");
 }else{
  openModal("<h2>주문을 전체 취소할까요?</h2><button class='secondary' id='no'>돌아가기</button><button class='primary' id='yes'>전체 취소</button>");
 }
};

document.getElementById("checkout").onclick=()=>{
 if(!Object.keys(cart).length){
  openModal("<h2>메뉴를 선택해주세요.</h2><button class='primary' id='ok'>확인</button>");
  return;
 }
 openModal(`<h2>주문 확인</h2><p>이용 방법을 선택해주세요.</p>
 <div class="option">
 <button class="${takeout==="매장"?"selected":""}" id="dine">매장 식사</button>
 <button class="${takeout==="포장"?"selected":""}" id="pack">포장</button>
 </div><p>총 결제 금액</p><h2>${document.getElementById("total").textContent}</h2>
 <p style="color:#777;font-size:12px">연습용 주문이며 실제 결제되지 않습니다.</p>
 <button class="primary" id="confirm">주문 확인</button>
 <button class="secondary" id="no">취소</button>`);
};

document.getElementById("dialog").addEventListener("click",e=>{
 if(e.target.id==="ok"||e.target.id==="no")closeModal();
 if(e.target.id==="yes"){clearCart();closeModal();}
 if(e.target.id==="dine"||e.target.id==="pack"){
  takeout=e.target.id==="dine"?"매장":"포장";
  document.getElementById("dine").classList.toggle("selected",takeout==="매장");
  document.getElementById("pack").classList.toggle("selected",takeout==="포장");
 }
 if(e.target.id==="confirm"){
  const total=document.getElementById("total").textContent;
  openModal(`<h2>주문이 완료되었습니다.</h2>
   <div style="font-size:55px;margin:20px">✓</div>
   <p>${takeout} 주문</p><h2>${total}</h2>
   <p>이용해 주셔서 감사합니다.</p>
   <button class="primary" id="finish">처음으로</button>`);
 }
 if(e.target.id==="finish"){
  clearCart();category="커피";takeout="매장";
  document.querySelectorAll("#categories button").forEach(b=>
   b.classList.toggle("active",b.dataset.cat==="커피"));
  renderProducts();closeModal();
 }
});

document.getElementById("modal").addEventListener("click",e=>{
 if(e.target.id==="modal")closeModal();
});
document.getElementById("home").onclick=()=>{
 clearCart();category="커피";
 document.querySelectorAll("#categories button").forEach(b=>
  b.classList.toggle("active",b.dataset.cat==="커피"));
 renderProducts();
};
document.getElementById("language").onclick=()=>{
 english=!english;
 renderProducts();
 document.getElementById("language").textContent=english?"◎ Korean":"◎ 언어변경";
};
document.getElementById("help").onclick=()=>{
 openModal("<h2>키오스크 이용 방법</h2><p>1. 왼쪽에서 메뉴를 선택하세요.</p><p>2. 원하는 메뉴를 담으세요.</p><p>3. 수량과 주문 금액을 확인하세요.</p><p>4. 주문하기를 누르세요.</p><button class='primary' id='ok'>확인</button>");
};

renderProducts();
renderCart();
</script>
</body>
</html>

