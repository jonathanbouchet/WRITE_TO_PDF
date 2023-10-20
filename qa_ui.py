import streamlit as st
from streamlit_chat import message
from pdf_utils import *
import os
from pathlib import Path
from pydantic_models import *


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.responses.append(user_input)


def on_btn_click():
    del st.session_state['questions']
    del st.session_state['responses']


st.session_state.setdefault('questions', [])

st.title("Survey QA Bot")
os.makedirs("tempDir", exist_ok=True)

uploaded_file = st.sidebar.file_uploader(label="Upload PDF files", type=["pdf"], accept_multiple_files=False)
if uploaded_file:
    save_path = Path("tempDir", uploaded_file.name)
    tmp_pathname = os.path.join("tempDir", uploaded_file.name)
    with open(save_path, mode='wb') as w:
        w.write(uploaded_file.getvalue())

    if save_path.exists():
        st.success(f'File {uploaded_file.name} is successfully saved!')

questions_list = ['medicare_number', 'signed_up_medicare', 'full_name', 'mailing_address',
                  'city', 'state', 'zipcode', 'phone_number']

if 'responses' not in st.session_state.keys():
    st.session_state.questions.extend(questions_list)
    st.session_state.responses = []
    st.session_state.qa = []
    st.session_state.counter_current_question = None

chat_placeholder = st.empty()
st.button("Clear message", on_click=on_btn_click)

# test
user_details = Tags()

message(st.session_state.questions[0])
st.session_state.counter_current_question = st.session_state.questions[0]
# print(f"counter current question :{st.session_state.counter_current_question}")

with st.container():
    for response, question in zip(st.session_state.responses, st.session_state.questions[1:]):
        message(response, is_user=True)
        message(question)
        st.session_state.counter_current_question = question
        # st.write(st.session_state)

with st.container():
    res = st.text_input("User Response:", on_change=on_input_change, key="user_input")
    # print(f"submitted answer: {res}, type: {type(res)}")
    # st.write(res)
    # test : hack
    # print(f"counter current question :{st.session_state.counter_current_question}")
    # print(f"question submitted so far:{st.session_state.questions[st.session_state.counter_current_question]}")

if st.button("submit data", type="primary"):
    print(f"questions:{st.session_state.questions}")
    print(f"answers:{st.session_state.responses}")
    blocks = []
    for q, a in zip(st.session_state.questions, st.session_state.responses):
        tmp = {'field': q, 'data': a}
        blocks.append(tmp)

    pdf_output = data_submitted(blocks, uploaded_file, tmp_pathname)
    pdf_output_name = pdf_output.split("/")[-1]

    print(pdf_output, pdf_output_name)

    with open(pdf_output, "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Export_Report",
                        data=PDFbyte,
                        file_name=pdf_output_name,
                        mime='application/octet-stream')
