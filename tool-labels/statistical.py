import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def app():
    data = pd.read_csv("./data.csv")
    st.title("Thống kê")
    labels = 'not_labeled', 'labeled'
    not_labeded = len(data[data['is_labeled'] == 0])
    labeled = len(data[data['is_labeled'] == 1])
    n = len(data)

    st.write('Tổng số bản ghi:', n)
    st.write('Đã gán nhãn:', labeled)
    st.write('Chưa gán nhãn:', not_labeded)

    sizes = [not_labeded/n, labeled/n]
    explode = (0, 0.1)
    fig1, ax1 = plt.subplots()
#     SMALL_SIZE = 3
#     matplotlib.rc('font', size=SMALL_SIZE)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)
