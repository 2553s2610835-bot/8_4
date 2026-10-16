import os
import io
import re
import streamlit as st
from PIL import Image

st.set_page_config(page_title="mPako | 세대 공감 번역기", page_icon="💬", layout="wide")

# -----------------------------
# mPako: MZ어 ↔ 기성세대 표준어
# 기본 사전으로 작동하며, OPENAI_API_KEY가 있으면 AI 번역/이미지·음성 기능을 사용할 수 있습니다.
# -----------------------------
st.markdown("""
<style>
    .block-container {max-width: 1100px; padding-top: 1.5rem; padding-bottom: 2rem;}
    .hero {padding: 1.25rem 1.4rem; border-radius: 18px; background: linear-gradient(120deg,#eef7ff,#f8f1ff); margin-bottom: 1rem;}
    .hero h1 {margin:0; color:#24213b;}
    .hero p {margin:.4rem 0 0 0; color:#55536a;}
    div[data-testid="stMetric"] {background:#f7f8fc; padding:1rem; border-radius:14px;}
    .small-note {color:#777; font-size:.88rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>💬 mPako <span style="font-size: .55em;">마파코</span></h1>
  <p>MZ세대와 기성세대가 서로의 말을 더 쉽게 이해하도록 돕는 양방향 번역 서비스</p>
</div>
""", unsafe_allow_html=True)

# phrase pairs are examples, not an exhaustive or authoritative dictionary.
MZ_TO_STANDARD = {
    "킹받네": "정말 화가 나고 짜증이 난다",
    "억텐": "억지로 분위기를 띄우는 모습",
    "찐이다": "진짜다",
    "레전드": "정말 대단하거나 인상적이다",
    "갑분싸": "갑자기 분위기가 어색해졌다",
    "꾸안꾸": "꾸민 듯 안 꾸민 듯 자연스러운 스타일",
    "스불재": "자신이 한 행동 때문에 스스로 어려움을 겪는 상황",
    "현타": "현실을 깨닫고 허무하거나 의욕이 떨어지는 느낌",
    "좋댓구알": "좋아요, 댓글, 구독, 알림 설정을 부탁한다",
    "알잘딱깔센": "알아서 잘, 딱 맞게, 깔끔하고 센스 있게",
    "폼 미쳤다": "실력이나 상태가 매우 뛰어나다",
    "갓생": "계획적이고 부지런하게 사는 생활",
    "TMI": "굳이 알 필요가 없는 사소한 정보",
    "내돈내산": "내 돈으로 직접 구매한 것",
    "손절": "관계나 교류를 끊다",
    "플렉스": "자신의 소비나 성취를 과시하다",
    "쩐다": "매우 대단하다",
    "노잼": "재미가 없다",
    "꿀잼": "매우 재미있다",
    "멘붕": "정신적으로 크게 당황하거나 혼란스러운 상태",
}
STANDARD_TO_MZ = {
    "정말 화가 나고 짜증이 난다": "킹받네",
    "억지로 분위기를 띄우는 모습": "억텐",
    "진짜다": "찐이다",
    "정말 대단하거나 인상적이다": "레전드",
    "갑자기 분위기가 어색해졌다": "갑분싸",
    "꾸민 듯 안 꾸민 듯 자연스러운 스타일": "꾸안꾸",
    "자신이 한 행동 때문에 스스로 어려움을 겪는 상황": "스불재",
    "현실을 깨닫고 허무하거나 의욕이 떨어지는 느낌": "현타",
    "좋아요, 댓글, 구독, 알림 설정을 부탁한다": "좋댓구알",
    "알아서 잘, 딱 맞게, 깔끔하고 센스 있게": "알잘딱깔센",
    "실력이나 상태가 매우 뛰어나다": "폼 미쳤다",
    "계획적이고 부지런하게 사는 생활": "갓생",
    "굳이 알 필요가 없는 사소한 정보": "TMI",
    "내 돈으로 직접 구매한 것": "내돈내산",
    "관계나 교류를 끊다": "손절",
    "자신의 소비나 성취를 과시하다": "플렉스",
    "매우 대단하다": "쩐다",
    "재미가 없다": "노잼",
    "매우 재미있다": "꿀잼",
    "정신적으로 크게 당황하거나 혼란스러운 상태": "멘붕",
}

def local_translate(text, direction):
    """Simple dictionary-based fallback. Replaces known phrases and leaves other text intact."""
    mapping = MZ_TO_STANDARD if direction == "MZ어 → 기성세대 표준어" else STANDARD_TO_MZ
    result = text
    for phrase in sorted(mapping, key=len, reverse=True):
        result = result.replace(phrase, mapping[phrase])
    if result == text:
        return "등록된 표현을 찾지 못했어요. 아래 사전에서 표현을 찾아보거나, AI 번역을 위해 OPENAI_API_KEY를 설정해 주세요."
    return result

def ai_text(prompt, system_prompt):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        st.error(f"AI 기능을 실행하지 못했어요: {exc}")
        return None

def translate(text, direction):
    system_prompt = (
        "너는 한국어 세대 간 표현 번역 도우미다. 의미와 말하는 사람의 의도를 유지하면서 "
        "입력 문장을 자연스럽게 바꿔라. "
        "MZ어 → 기성세대 표준어는 유행어를 쉬운 표준어로 풀어 쓰고, "
        "기성세대 표준어 → MZ어는 맥락에 맞는 자연스러운 MZ 표현으로 바꿔라. "
        "과도하게 유행어를 붙이지 말고 번역문만 출력하라."
    )
    ai_result = ai_text(f"방향: {direction}\n문장: {text}", system_prompt)
    if ai_result:
        return ai_result, "AI 번역"
    return local_translate(text, direction), "기본 사전 번역"

with st.sidebar:
    st.markdown("## 메뉴")
    page = st.radio(
        "기능 선택",
        ["🏠 홈 번역", "📸 카톡/SNS 캡처 번역", "🎙️ 음성 번역", "📚 표현 사전"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("mPako · 세대 공감 프로젝트")
    if os.getenv("OPENAI_API_KEY"):
        st.success("AI 기능 연결됨")
    else:
        st.info("기본 사전 모드")
        st.caption("AI 기능을 사용하려면 Streamlit Secrets에 OPENAI_API_KEY를 추가하세요.")

if page == "🏠 홈 번역":
    st.subheader("홈 | 양방향 텍스트 번역")
    left, right = st.columns([1, 1])
    with left:
        direction = st.selectbox("번역 방향", ["MZ어 → 기성세대 표준어", "기성세대 표준어 → MZ어"])
        source = st.text_area("번역할 문장을 입력하세요", placeholder="예: 오늘 발표 폼 미쳤다", height=170, key="home_source")
        do_translate = st.button("✨ 번역하기", type="primary", use_container_width=True)
    with right:
        st.markdown("#### 번역 결과")
        if do_translate:
            if source.strip():
                result, mode = translate(source.strip(), direction)
                st.text_area("결과", value=result, height=170, key="home_result")
                st.caption(f"사용 방식: {mode}")
            else:
                st.warning("먼저 문장을 입력해 주세요.")
        else:
            st.info("왼쪽에 문장을 입력한 다음 ‘번역하기’를 누르세요.")
    st.divider()
    st.subheader("이런 표현도 있어요")
    samples = st.columns(3)
    for col, (term, meaning) in zip(samples, list(MZ_TO_STANDARD.items())[:3]):
        with col:
            st.metric(term, meaning)

elif page == "📸 카톡/SNS 캡처 번역":
    st.subheader("카톡/SNS 캡처 번역")
    st.write("이미지를 올리면 글자를 읽어 번역합니다. OCR 프로그램이 설치되지 않은 환경에서는 직접 인식한 문장을 입력해도 됩니다.")
    uploaded = st.file_uploader("캡처 이미지 업로드", type=["png", "jpg", "jpeg", "webp"])
    direction = st.selectbox("번역 방향", ["MZ어 → 기성세대 표준어", "기성세대 표준어 → MZ어"], key="ocr_direction")
    extracted = ""
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="업로드한 이미지", use_container_width=True)
        try:
            import pytesseract
            extracted = pytesseract.image_to_string(image, lang="kor+eng").strip()
            st.success("이미지에서 텍스트를 읽었어요.")
        except Exception:
            st.warning("현재 환경에서 OCR을 사용할 수 없어요. 아래 입력창에 이미지 속 문장을 직접 입력해 주세요.")
    source = st.text_area("인식한 문장 (필요하면 수정하세요)", value=extracted, height=150, key="ocr_text")
    if st.button("📖 캡처 문장 번역", type="primary"):
        if source.strip():
            result, mode = translate(source.strip(), direction)
            st.markdown("#### 번역 결과")
            st.write(result)
            st.caption(f"사용 방식: {mode}")
        else:
            st.warning("이미지를 올리거나 문장을 입력해 주세요.")

elif page == "🎙️ 음성 번역":
    st.subheader("음성 번역")
    st.write("음성 파일을 업로드할 수 있습니다. OPENAI_API_KEY가 설정되어 있으면 음성을 텍스트로 변환한 뒤 번역합니다.")
    audio = st.file_uploader("음성 파일 업로드", type=["mp3", "wav", "m4a", "mp4", "webm"])
    direction = st.selectbox("번역 방향", ["MZ어 → 기성세대 표준어", "기성세대 표준어 → MZ어"], key="audio_direction")
    if audio:
        st.audio(audio)
        if st.button("🎧 음성 인식 및 번역", type="primary"):
            if not os.getenv("OPENAI_API_KEY"):
                st.warning("음성 자동 인식은 API 키가 필요해요. 우선 음성을 들으며 아래 텍스트 입력란에 내용을 적어 번역할 수 있어요.")
            else:
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=(audio.name, audio.getvalue(), audio.type or "audio/mpeg"),
                        language="ko",
                    )
                    transcript = transcription.text
                    st.markdown("#### 인식된 문장")
                    st.write(transcript)
                    result, mode = translate(transcript, direction)
                    st.markdown("#### 번역 결과")
                    st.write(result)
                    st.caption(f"사용 방식: {mode}")
                except Exception as exc:
                    st.error(f"음성 인식에 실패했어요: {exc}")
    manual = st.text_area("또는 음성 내용을 직접 입력하세요", placeholder="음성으로 들은 문장을 입력하세요")
    if st.button("텍스트 번역", key="manual_audio_translate"):
        if manual.strip():
            result, mode = translate(manual.strip(), direction)
            st.markdown("#### 번역 결과")
            st.write(result)
            st.caption(f"사용 방식: {mode}")
        else:
            st.warning("음성 내용을 입력해 주세요.")

elif page == "📚 표현 사전":
    st.subheader("표현 사전")
    query = st.text_input("표현 또는 뜻 검색", placeholder="예: 킹받네")
    rows = []
    for term, meaning in MZ_TO_STANDARD.items():
        if not query or query.lower() in term.lower() or query.lower() in meaning.lower():
            rows.append({"MZ 표현": term, "쉬운 뜻": meaning})
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("검색 결과가 없어요. 다른 표현을 입력해 주세요.")
    st.caption("사전은 예시 중심이며, 유행어의 뜻은 상황과 사람에 따라 달라질 수 있어요.")

st.divider()
st.caption("※ 기본 사전 번역은 등록된 표현만 바꿉니다. 문맥을 고려한 자유로운 번역, OCR 및 음성 인식을 위해서는 필요한 라이브러리와 API 설정이 필요합니다.")
