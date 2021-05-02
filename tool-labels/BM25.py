import streamlit as st


def app(params = None):
    bm25_obj = params['BM25']
    texts = params['texts']
    dictionary = params['dictionary']
    st.title("Tìm kiếm câu hỏi tương đồng sử dụng BM25")
    query = st.text_input("Nhập vào câu hỏi:")
    submit = st.button("Tìm kiếm")

    if submit or query:
        st.markdown("## TOP 10 câu hỏi tương đồng")
        query_doc = dictionary.doc2bow(query.split())
        scores = bm25_obj.get_scores(query_doc)
        best_docs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:10]
        for i, idx in enumerate(best_docs):
            st.markdown("**{}** - **Question:** {}".format(i + 1, " ".join(texts[idx])))
