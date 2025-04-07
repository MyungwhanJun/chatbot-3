### 📁 파일: app.py
import streamlit as st

st.set_page_config(page_title="산티아고 순례길 여행", page_icon="🛤️", layout="wide")

st.title("🚶‍♀️ 산티아고 순례길 여행에 오신 것을 환영합니다!")
st.markdown("""
이 사이트는 산티아고 순례길에 대해 알고 싶은 모든 정보를 제공합니다.
- 다양한 **코스 정보**
- **여행 준비물**, 날씨, 숙소 정보
- **챗봇을 통한 실시간 상담**
- 다른 순례자들의 **후기 및 사진 공유**까지!

왼쪽 메뉴에서 원하는 항목을 선택해 주세요.
""")


### 📁 폴더: pages/1_🏠_홈.py
import streamlit as st

st.title("🏠 산티아고 순례길이란?")
st.markdown("""
산티아고 순례길(Camino de Santiago)은 스페인의 산티아고 데 콤포스텔라 대성당까지 이어지는 유서 깊은 순례길입니다.
기독교 순례자뿐 아니라 자연과 여유를 찾는 전 세계 사람들이 걷는 평화로운 길입니다.

- 총 길이: 800km 이상 (전체 프랑스길 기준)
- 주요 루트: 프랑스길, 포르투갈길, 북쪽길 등
- 하이라이트 구간만 걷는 것도 가능 (예: 사리아 ~ 산티아고)
""")


### 📁 pages/2_🗺️_코스안내.py
import streamlit as st

st.title("🗺️ 주요 코스 안내")

st.header("1️⃣ 프랑스길 (Sarria → Santiago)")
st.markdown("""
- 거리: 약 115km  
- 소요 기간: 5~7일  
- 특징: 가장 인기 많은 구간, 인증서 발급 가능
""")

st.header("2️⃣ 포르투갈길 (Tui → Santiago)")
st.markdown("""
- 거리: 약 120km  
- 소요 기간: 5~7일  
- 특징: 평탄하고 조용한 경로, 가을 풍경이 아름다움
""")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Camino_de_santiago_routes.svg/1200px-Camino_de_santiago_routes.svg.png", caption="산티아고 순례길 전체 루트")


### 📁 pages/3_🎒_여행준비.py
import streamlit as st

st.title("🎒 여행 준비 체크리스트")

st.markdown("""
#### ✅ 필수 준비물
- 배낭 (30~40L 권장)
- 걷기 좋은 운동화 또는 트레킹화
- 순례자 여권 (현지에서 구매 가능)
- 여권 및 복사본
- 개인 세면도구, 빨랫줄 등

#### 📦 짐 운반 서비스
- 평균 요금: 하루 4~7유로
- 대표 업체: Correos, Pilbeo 등
- 무거운 짐은 숙소 간 운반 가능 (15~20kg 제한)

#### 🌤️ 날씨 팁
- 5월: 꽃 피는 계절, 아침저녁 쌀쌀
- 9월: 가을 햇살, 포도 수확철
""")


### 📁 pages/4_💬_챗봇상담.py
import streamlit as st
from openai import OpenAI

st.title("💬 산티아고 순례길 챗봇 상담")

st.write(
    "안녕하세요! 👋\n"
    "이 챗봇은 OpenAI의 GPT-3.5 모델을 활용하여 산티아고 순례길에 대한 다양한 정보를 안내해 드립니다. "
    "코스, 날씨, 준비물, 짐 운반 서비스 등 궁금한 것을 자유롭게 질문해 주세요!"
)

openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("서비스를 이용하려면 OpenAI API 키가 필요합니다.", icon="🔐")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("궁금한 내용을 입력해 주세요. 예: 5월에 가기 좋은가요?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


### 📁 pages/5_📸_후기갤러리.py
import streamlit as st

st.title("📸 후기 & 갤러리")

st.markdown("""
여기서 다른 순례자들의 사진과 후기를 공유하거나, 본인의 경험을 나눌 수 있습니다. 
아래에 사진을 업로드해 보세요!
""")

uploaded_files = st.file_uploader("사진 업로드 (여러 장 가능)", accept_multiple_files=True, type=["jpg", "png", "jpeg"])

if uploaded_files:
    for file in uploaded_files:
        st.image(file, use_column_width=True)
        st.caption(f"{file.name}")
