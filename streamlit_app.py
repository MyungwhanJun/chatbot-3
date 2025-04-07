import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 산티아고 순례길 여행 소개 서비스")
st.write(
    "안녕하세요! 👋\n"
    "이 챗봇은 OpenAI의 GPT-3.5 모델을 활용하여 산티아고 순례길에 대한 다양한 정보를 안내해 드립니다. "
    "코스, 날씨, 준비물, 짐 운반 서비스 등 궁금한 것을 자유롭게 질문해 주세요!"
)


openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("서비스를 이용하려면 OpenAI API 키가 필요합니다.", icon="🔐")

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 채팅 내용 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("궁금한 내용을 입력해 주세요. 예: 5월에 가기 좋은가요?"):
        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API로 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답 표시 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
