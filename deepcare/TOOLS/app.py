import add_similary
import statistical
import streamlit as st

PAGES = {
    "Thêm câu hỏi tương đồng": add_similary,
    "Thống kê": statistical
}

st.sidebar.title('PAGES')
selection = st.sidebar.selectbox('', list(PAGES.keys()))
page = PAGES[selection]
page.app()
