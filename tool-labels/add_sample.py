import streamlit as st
import pandas as pd

def app():
    # Đọc dữ liệu
    data = pd.read_csv("./data/data.csv")

    st.title('Thêm dữ liệu')
    # chia cột
    left, right = st.beta_columns(2)

    # Vùng hiển thị câu hỏi và câu trả lời
    txt_question = left.text_input('Câu hỏi:')
    txt_answer = left.text_area('Câu trả lời:')

    # Vùng thêm câu hỏi tương đồng
    values = []
    min_value = 0
    number_question = right.number_input('Số câu hỏi tương đồng muốn thêm', min_value=min_value, max_value=10, value=int())
    for i in range(number_question):
        values.append(right.text_input(f'Câu hỏi tương đồng {i+1}'))
    
    # Vùng button
    submit = st.button("Thêm")

    if submit:
        update = True
        if txt_question == '' or txt_answer == '':
            update = False
        if update:
            new_data = {'answer': txt_answer, 'question': txt_question, 'is_labeled': 0, 'question_similaries': []}
            if number_question > 0:
                new_data['is_labeled'] = 1
                new_data['question_similaries'] = values
                data = data.append(new_data, ignore_index=True)
                data.to_csv('./data/data.csv', index=False)
                st.success(f'Đã thêm câu hỏi vào ID: {len(data)-1}')
        else:
            st.error(f'Không được bỏ trống form câu hỏi hoặc câu trả lời!')


