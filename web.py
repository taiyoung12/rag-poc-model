import streamlit as st
import requests
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="LLM Response Viewer", page_icon="🤖", layout="centered")

st.title("💬 LLM Response Viewer")
st.write("이 도구를 사용하여 LLM에게 메시지를 보내고 응답을 확인하세요.")

st.sidebar.title("🔧 설정")
st.sidebar.write("이 페이지를 통해 LLM과 상호작용할 수 있습니다. API 서버가 작동 중인지 확인하세요.")

st.header("🔍 Send a Message")

disable_send_button = False

with st.form("message_form"):
    keyword = st.selectbox(
        "Choose a keyword:",
        options=["마이데이터", "마이데이터_API"],
        help="메시지를 위한 키워드를 선택하세요."
    )
    
    prompt = st.text_input("Enter your prompt:", help="LLM에 보낼 프롬프트를 입력하세요.")
    
    submitted = st.form_submit_button("Send")

    if submitted:
        disable_send_button = True
        if keyword and prompt:
            try:
                url = f"http://localhost:8080/rag?keyword={keyword}&prompt={prompt}"
                response = requests.get(url)
                response.raise_for_status()
                st.success("✅ 메시지가 성공적으로 전송되었습니다!")
                st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"❌ 메시지 전송 중 오류가 발생했습니다: {e}")
        else:
            st.warning("⚠️ 모든 필드를 입력해야 합니다.")

        time.sleep(1)
        
        disable_send_button = False

st.header("📨 Latest LLM Response")

response_container = st.empty()

count = st_autorefresh(interval=5000, limit=100, key="refresh")

def fetch_latest_response():
    try:
        response = requests.get("http://localhost:8080/llm-response")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"❌ 최신 응답을 가져오는 중 오류가 발생했습니다: {e}"

latest_response = fetch_latest_response()
response_container.write(latest_response)