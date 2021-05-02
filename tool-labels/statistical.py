from numpy.lib.npyio import load
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO
import xlsxwriter
from utils import load_data

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
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download csv file</a>'


def app(params = None):
    data = load_data()
    st.title("Thống kê")
    st.markdown(get_table_download_link(data), unsafe_allow_html=True)
    # labels = 'not_labeled', 'labeled'
    not_labeded = len(data[data['is_labeled'] == 0])
    labeled = len(data[data['is_labeled'] == 1])
    n = len(data)

    st.write('Tổng số bản ghi:', n)
    st.write('Đã gán nhãn:', labeled)
    st.write('Chưa gán nhãn:', not_labeded)

    # sizes = [not_labeded/n, labeled/n]
    # explode = (0, 0.1)
    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    #         shadow=True, startangle=90)
    # ax1.axis('equal')
    # st.pyplot(fig1)
