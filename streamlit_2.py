import streamlit as st
from streamlit_chat import message
import pandas as pd
from embedding_query import embedding_query
from answer_llm import answer_llm
from numpy import dot
from numpy.linalg import norm

segments = pd.read_pickle("segments_combined.pkl")

st.title("농기평 x 솔리드이앤지 LLM")
st.write("하이퍼클로바 기반 RAG(Regenerative Augmented Generatrion) 기술을 적용한 전문LLM")

# Initialize conversation history as an empty list
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

# Add user input and submit button
user_input = st.text_input('질문을 입력해주세요 : ', '')
submit_button = st.button('전송')

provided_data = '정보없음'
table_phrases = ['표','엑셀','테이블','자세히','짧게','간략','한문장','두문장','간결','핵심','요약','결론','중요한','길게']
if submit_button and user_input:

    preset_text = user_input
    query_emb = embedding_query(preset_text)

    top_2 = []
    for i in range(len(segments)):
        a = segments['vector'][i]
        b = query_emb
        cos_sim = dot(a, b)/(norm(a)*norm(b))
        top_2.append(cos_sim)
    
    if max(top_2) >= 0.990:
        top_2 = sorted(range(len(top_2)), key=lambda i: top_2[i])[-2:]
        provided_data = "[정보]: " + str(segments['origin'][top_2[0]]) + str(segments['origin'][top_2[1]])
    
    if provided_data == '정보없음':
        if any(phrase in user_input for phrase in table_phrases):
            if 'conversation_history' in st.session_state:
                for interaction in st.session_state['conversation_history']:
                    provided_data = "[정보]: " + interaction['bot_answer']
                    break

    user_text = provided_data + "\n\n" + preset_text
    answer = answer_llm(user_text)

    # Store the current interaction in the conversation history
    current_interaction = {'user_input': user_input, 'bot_answer': answer}
    st.session_state['conversation_history'].insert(0, current_interaction)
i=0
# Display the conversation history in order
for interaction in st.session_state['conversation_history']:
    i = i+1
    message(interaction['user_input'], is_user=True, key =f"{i}_user")
    message(interaction['bot_answer'],key =f"{i}_bot")