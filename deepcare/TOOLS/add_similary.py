import streamlit as st
import pandas as pd


data = pd.read_csv("./data.csv")
for i in range(len(data)):
    if data.iloc[i]['is_labeled'] == 0:
        selected = i
        break

def app():
    st.title("Gán nhãn câu hỏi tương đồng DeepCare.IO")
    id = st.number_input('ID:', min_value=0, value=selected)
    question = data.iloc[id]['question']
    answer = data.iloc[id]['answer']
    left, right = st.beta_columns(2)
    left.text_input('Câu hỏi:', value=question)
    left.text_area('Câu trả lời:', value=answer)

    number_question = right.number_input(
        'Số câu hỏi tương đồng muốn thêm:', min_value=1, max_value=10)
    for i in range(number_question):
        right.text_input(f'Câu hỏi tương đồng {i+1}')

    left2, right2 = st.beta_columns(2)
    left2.button('Xóa câu hỏi này')
    right2.button('Hoàn thành')
