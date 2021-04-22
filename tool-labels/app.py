import add_similary
import statistical
import streamlit as st
import add_sample

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()

PAGES = {
    "Gán nhãn câu hỏi tương đồng": add_similary,
    "Thêm dữ liệu": add_sample,
    "Thống kê": statistical
}

st.sidebar.title('PAGES')
selection = st.sidebar.selectbox('', list(PAGES.keys()))
page = PAGES[selection]
page.app()
