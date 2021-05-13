import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from utils import load_data
import os

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Nhấn vào đây để tải về dữ liệu</a>'

def app():
    data = load_data()
    st.title("Dataset")
    
    st.markdown("## **Thống kê**")
    not_labeded = len(data[data['is_labeled'] == 0])
    labeled = len(data[data['is_labeled'] == 1])
    n = len(data)

    st.write('Tổng số bản ghi:', n)
    st.write('Đã gán nhãn:', labeled)
    st.write('Chưa gán nhãn:', not_labeded)

    st.markdown("## **Actions**")
    export = st.checkbox("Export Dataset")
    btn_submit = st.button('Submit')
    if btn_submit:
        if export:
            st.markdown(get_table_download_link(data), unsafe_allow_html=True)

    st.markdown("## **View dataset**")
    id_start = st.number_input('ID bắt đầu:', min_value=0, max_value=n-1, value = 0)
    id_end = st.number_input('ID kết thúc:', min_value=0, max_value=n-1, value = 0)
    btn_view = st.button("View")
    if btn_view:
        if id_start <= id_end and id_end - id_start <= 200:
            st.table(data[id_start:id_end + 1])
        elif id_start > id_end:
            st.warning("ID bắt đầu phải nhỏ hơn hoặc bằng ID kết thúc")
        elif id_end - id_start > 200:
            st.warning("Chỉ hiển thị tối đa 200 bản ghi")
    

