
import streamlit as st
from datetime import date, time

st.set_page_config(
    page_title="병원 이용 도우미",
    page_icon="🏥",
    layout="centered"
)

# 화면 디자인
st.markdown("""
<style>
.stApp {
    background-color: #F0F6FF;
}
.block-container {
    max-width: 850px;
    padding-top: 2rem;
}
h1, h2, h3, p, label {
    color: #23415B;
}
div.stButton > button {
    width: 100%;
    min-height: 45px;
    border-radius: 12px;
    background-color: white;
    color: #23415B;
    border: 1px solid #B9D5F5;
}
</style>
""", unsafe_allow_html=True)

# 글씨 크기 설정
st.sidebar.header("⚙️ 편의 설정")
large_text = st.sidebar.checkbox("큰 글씨 사용하기", value=True)

font_size = "23px" if large_text else "17px"
st.markdown(
    f"<style>p, label, li {{font-size:{font_size};}}</style>",
    unsafe_allow_html=True
)

# 제목
st.title("🏥 병원 이용 도우미")
st.subheader("병원 이용, 더 쉽고 편하게!")
st.write(
    "병원 이용이 낯선 어르신도 필요한 정보를 쉽게 확인할 수 있어요."
)

# 메뉴
page = st.radio(
    "원하는 서비스를 선택하세요.",
    ["🏥 진료과 안내", "📅 예약 관리", "🎒 방문 준비물", "💬 쉬운 의료 용어"],
    horizontal=False
)

st.divider()

# 1. 진료과 안내
if page == "🏥 진료과 안내":
    st.header("어떤 진료과를 찾아야 할까요?")

    departments = {
        "내과": "감기, 소화 불편, 고혈압 등 일반적인 내과 진료가 필요할 때 방문해요.",
        "정형외과": "뼈, 관절, 근육 등에 불편함이 있을 때 방문해요.",
        "피부과": "피부 발진, 가려움, 여드름 등 피부 문제가 있을 때 방문해요.",
        "안과": "시력 저하, 눈의 불편함 등이 있을 때 방문해요.",
        "이비인후과": "귀, 코, 목과 관련된 불편함이 있을 때 방문해요.",
        "치과": "치아 통증, 잇몸 문제 등이 있을 때 방문해요.",
        "가정의학과": "어떤 진료과를 가야 할지 잘 모를 때 상담할 수 있어요."
    }

    selected = st.selectbox(
        "진료과를 선택하세요.",
        list(departments.keys())
    )

    st.info(departments[selected])
    st.caption(
        "※ 이 안내는 일반적인 정보입니다. "
        "정확한 진료과는 의료진에게 확인하세요."
    )

# 2. 예약 관리
elif page == "📅 예약 관리":
    st.header("진료 예약 기록하기")
    st.write("예약 정보를 입력하면 이 화면에서 확인할 수 있어요.")

    if "appointments" not in st.session_state:
        st.session_state.appointments = []

    hospital = st.text_input(
        "병원 이름",
        placeholder="예: 행복병원"
    )

    department = st.selectbox(
        "진료과",
        ["내과", "정형외과", "피부과", "안과",
         "이비인후과", "치과", "가정의학과", "기타"]
    )

    appointment_date = st.date_input(
        "예약 날짜",
        value=date.today(),
        min_value=date.today()
    )

    appointment_time = st.time_input(
        "예약 시간",
        value=time(9, 0),
        step=1800
    )

    if st.button("예약 기록 저장하기"):
        if not hospital.strip():
            st.warning("병원 이름을 입력해 주세요.")
        else:
            st.session_state.appointments.append({
                "hospital": hospital.strip(),
                "department": department,
                "date": appointment_date,
                "time": appointment_time
            })
            st.success("예약 정보를 기록했어요!")

    st.divider()
    st.subheader("📋 내 예약 목록")

    if not st.session_state.appointments:
        st.write("아직 기록된 예약이 없어요.")
    else:
        for i, item in enumerate(
            st.session_state.appointments
        ):
            with st.container(border=True):
                st.write(f"🏥 병원: {item['hospital']}")
                st.write(f"진료과: {item['department']}")
                st.write(f"날짜: {item['date']}")
                st.write(
                    "시간: "
                    + item["time"].strftime("%H:%M")
                )

                if st.button(
                    "예약 기록 삭제",
                    key=f"delete_{i}"
                ):
                    st.session_state.appointments.pop(i)
                    st.rerun()

    st.caption(
        "예약 기록용 기능이며 병원에 실제 예약을 신청하지는 않아요."
    )

# 3. 방문 준비물
elif page == "🎒 방문 준비물":
    st.header("병원 방문 전 확인하기")
    st.write("필요한 준비물을 하나씩 체크해 보세요.")

    items = [
        "신분증",
        "건강보험 관련 정보",
        "복용 중인 약 목록 또는 약 봉투",
        "이전에 받은 검사 결과나 진료 기록",
        "예약 날짜와 시간 확인",
        "병원 위치와 교통편 확인"
    ]

    if "checked_items" not in st.session_state:
        st.session_state.checked_items = {}

    for i, item in enumerate(items):
        st.checkbox(
            item,
            key=f"prepare_{i}"
        )

    checked = sum(
        st.session_state.get(f"prepare_{i}", False)
        for i in range(len(items))
    )

    st.progress(checked / len(items))
    st.write(f"준비 완료: {checked}/{len(items)}개")

    if checked == len(items):
        st.success("모든 항목을 확인했어요!")

    st.caption(
        "병원과 진료 상황에 따라 필요한 준비물이 다를 수 있어요."
    )

# 4. 쉬운 의료 용어
elif page == "💬 쉬운 의료 용어":
    st.header("어려운 병원 용어 쉽게 이해하기")

    terms = {
        "접수": "병원에 도착해 진료를 받기 위해 신청하는 과정이에요.",
        "진료": "의사 선생님이 몸 상태를 확인하고 상담하는 과정이에요.",
        "처방전": "의사가 필요한 약과 복용 방법 등을 적어 주는 문서예요.",
        "검사": "몸의 상태나 질병 여부를 확인하기 위해 살펴보는 과정이에요.",
        "수납": "진료비를 계산하고 내는 과정이에요.",
        "재진": "이전에 진료받은 병원에 다시 방문해 진료받는 것이에요.",
        "초진": "해당 병원이나 진료에서 처음으로 진료받는 것을 말해요.",
        "금식": "검사 등의 이유로 일정 시간 음식물을 먹지 않는 것이에요."
    }

    for term, meaning in terms.items():
        with st.expander(term):
            st.write(meaning)

    st.divider()
    st.subheader("직접 어려운 말 기록하기")

    custom_term = st.text_input(
        "어려운 용어",
        placeholder="예: 혈압"
    )

    custom_meaning = st.text_area(
        "알아보기 쉽게 정리한 내용",
        placeholder="설명 내용을 입력해 보세요."
    )

    if st.button("내 용어 정리하기"):
        if custom_term.strip() and custom_meaning.strip():
            st.success(
                f"{custom_term.strip()}: "
                f"{custom_meaning.strip()}"
            )
        else:
            st.warning("용어와 설명을 모두 입력해 주세요.")

# 하단 안내
st.divider()
st.caption(
    "🏥 병원 이용 도우미 | 어르신의 편리한 병원 이용을 위한 교육용 앱"
)
