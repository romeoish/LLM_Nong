import streamlit as st
from streamlit_chat import message
import pandas as pd
from embedding_query import embedding_query
from answer_llm import answer_llm
from numpy import dot
from numpy.linalg import norm

segments = pd.read_pickle("segments.pkl")

st.title("LLM TEST")
st.write("하이퍼클로바x 기반 RAG(Regenerative Augmented Generatrion 기술 적용 LLM")

question = st.text_area(
    '질문', 
    placeholder='질문을 입력해 주세요', 
)

if question:
    preset_text = question
    query_emb = embedding_query(preset_text)

    top_2 = []
    for i in range(len(segments)):
        a = segments['vector'][i]
        b = query_emb
        cos_sim = dot(a, b)/(norm(a)*norm(b))
        top_2.append(cos_sim)
    top_2 = sorted(range(len(top_2)), key=lambda i: top_2[i])[-2:]

    provided_data = ""
    provided_data = "[정보]: " + str(segments['origin'][top_2[0]]) + str(segments['origin'][top_2[1]])
    user_text = provided_data + "\n\n"+ preset_text

    answer = answer_llm(user_text)
    st.write("답변:", answer)

