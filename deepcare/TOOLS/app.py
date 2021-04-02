import add_similary
import thong_ke
import streamlit as st

PAGES = {
    "Thêm câu hỏi tương đồng": add_similary,
    "Thống kê": thong_ke
}

st.sidebar.title('MENU')
selection = st.sidebar.selectbox('', list(PAGES.keys()))
page = PAGES[selection]
page.app()
