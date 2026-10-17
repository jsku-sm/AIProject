import streamlit as st

from agents import Agent, Runner, SQLiteSession


# =========================================================
# 1. Page
# =========================================================

st.set_page_config(
    page_title="수학코치",
    page_icon="🔬"
)


# =========================================================
# 2. Agent
# =========================================================

mathmatics_agent = Agent(
    name="수학",

    instructions="""
    [ROLE]
   너는 고등학교 1학년 학생 수학 교과 학습을 지원하는 전문 학습 assistant야.


   [GOAL]
   학생이 질문하는 문제를 스스로 확실하게 개념적으로 이해하고 정리할 수 있도록 하는게 목표야.


   [RULES]
   학습 지원을 하는 중에 하지 말아야 할 사항은
   1. 정답을 말하지 않는거야.
   2. 너무 어려운 내용 제시 금지
   3. 교육과정, 교과서 및 교사의 유인물 수준을 넘지 않아야 해.


   학습 지원을 하는 중에 했으면 좋은 사항은
   1. 학생의 수준을 판단할 수 있는 적절한 질문을 통해 수준별 학습
   2. 학생의 의욕을 높일 수 있도록 격려와 칭찬을 많이 해주고
   3. 개념 설명 후에는 반드시 쉬운 예시를 들어서 개념을 더 잘 정리할 수 있도록 해줘.
   4. 필요하면 심화 내용을 제시하는 것과 관련 분야를 언급해 주는 것도 좋을 것 같아.
   5. 기초가 아주 약한 학생이 문제해결을 위해 문제를 복사-붙여넣기했을 때 문제를 해결하기 위한 핵심키워드를 제시해준다


   [PROCESS]
   학생 질문 입력 - 개념 설명 - 적절한 예시 - 심화 내용 제시 및 관련 분야 안내


   [OUTPUT]
   상황에 따라 다음을 제공한다.
   - 현재 아이디어 분석
   - 개선이 필요한 부분
   - 개선 방향
   - 필요한 경우 질문 후보
   - 학생이 다음으로 생각할 질문

    """
)


# =========================================================
# 3. UI State
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# 4. Agent Session
# =========================================================

if "agent_session" not in st.session_state:

    st.session_state.agent_session = SQLiteSession(
        "student_session",
        "mathmatics_agent.db"
    )


# =========================================================
# 5. UI
# =========================================================

st.title("수학코치")

st.caption(
    "학생이 스스로 좋은 수학 탐구질문을 "
    "발전시키도록 지원하는 AI Agent"
)


# =========================================================
# 6. Previous Messages
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# 7. User Input
# =========================================================

user_input = st.chat_input(
    "수학 탐구에 관심 있는 주제를 입력하세요."
)


# =========================================================
# 8. Run Agent
# =========================================================

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)


    with st.chat_message("assistant"):

        with st.spinner("생각하고 있습니다..."):

            try:

                result = Runner.run_sync(
                    mathmatics_agent,
                    user_input,
                    session=st.session_state.agent_session
                )

                response = result.final_output

                st.markdown(response)

            except Exception as e:

                response = f"오류가 발생했습니다: {e}"

                st.error(response)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )
