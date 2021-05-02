import streamlit as st
from utils import load_data, find_question_similary

def app(params = None):
    data = load_data()
    # Tìm kiếm xem ID nào chưa gán
    for i in range(len(data)):
        if data.iloc[i]['is_labeled'] == 0:
            selected = i
            break

    st.title("Gán nhãn câu hỏi tương đồng DeepCare.IO")
    id = st.number_input('ID:', min_value=0, value=selected, max_value=len(data)-1)
    st.write('Tình trạng: {}'.format('**Đã gán nhãn**' if data.iloc[id]['is_labeled']==1 else '**Chưa gán nhãn**'))
    question = data.iloc[id]['question']
    answer = data.iloc[id]['answer']
    left, right = st.beta_columns(2)
    
    # Vùng hiển thị câu hỏi và câu trả lời
    txt_quesion = left.text_input('Câu hỏi:', value=question)
    txt_answer = left.text_area('Câu trả lời:', value=answer)

    # Vùng thêm câu hỏi tương đồng
    values = []
    if data.iloc[id]['is_labeled'] == 0:
        # Chưa được gán nhãn
        lst_question_similary = find_question_similary(txt_quesion, params)
        min_value = 1
        number_question = right.number_input('Số câu hỏi tương đồng muốn thêm:', min_value=1, max_value=10)
        for i in range(number_question):
            values.append(right.text_input(f'Câu hỏi tương đồng {i+1}', value = lst_question_similary[i]))
    else:
        # Đã được gán nhãn
        min_value = len(data.iloc[id]['question_similaries'])
        number_question = right.number_input('Số câu hỏi tương đồng muốn thêm:', min_value=min_value, max_value=10)
        for i in range(number_question):
            values.append(right.text_input(f'Câu hỏi tương đồng {i+1}', value=data.iloc[id]['question_similaries'][i]))

    # Vùng button
    left2, middle2 , right2 = st.beta_columns(3)
    delete = left2.button('Xóa câu hỏi này')
    clear = middle2.button('Xóa nhãn đã gán')
    add = right2.button('Hoàn thành')

    # Vùng hiển thị kết quả
    if clear:
        data.at[id,'is_labeled'] = 0
        data.at[id,'question_similaries'] = []
        st.write(data.iloc[id])
        data.to_csv('./data/data.csv', index=False)
        st.success(f'Xóa dữ liệu đã gán cho câu hỏi ID: {id} thành công! Ấn phím R để xem lại cập nhật!')

    if delete:
        data.drop(id,inplace=True)
        # data.reset_index(inplace=True)
        data.to_csv('./data/data.csv', index=False)
        st.info('Xóa dữ liệu thành công! Ấn phím R để xem lại cập nhật!')

    if add:
        update = True
        for q in values:
            if q == '':
                st.error('Tồn tại form câu hỏi tương đồng trống')
                update = False
                break
        if update:
            data.at[id, 'question'] = txt_quesion
            data.at[id, 'answer'] = txt_answer
            data.at[id,'is_labeled'] = 1
            data.at[id,'question_similaries'] = values
            st.write(data.iloc[id])
            data.to_csv('./data/data.csv', index=False)
            st.success('Thêm dữ liệu thành công! Ấn phím R để xem lại cập nhật!')