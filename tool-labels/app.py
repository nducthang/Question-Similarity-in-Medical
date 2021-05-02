from numpy.lib.npyio import load
import add_similary
import statistical
import streamlit as st
import add_sample
import BM25
from utils import load_bm25


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
    "Thống kê": statistical,
    "Search engine BM25": BM25
}

params = load_bm25()

st.sidebar.title('PAGES')
selection = st.sidebar.selectbox('', list(PAGES.keys()))
page = PAGES[selection]
page.app(params)
