from typing import Counter
import streamlit as st
import lightgbm as lgb
import pandas as pd
from src.Essemble.utils import get_feature, get_words, get_weight, word_shares
import numpy as np

MODEL_PATH = './models/lightgbm.bin'
QUESTION_LIST = './data/questions.csv'

def predict(clf, x_test):
    return clf.predict(x_test)

def build_feature(df):
    words = get_words(df)
    counts = Counter(words)
    weights = {word: get_weight(count) for word, count in counts.items()}
    df['word_shares'] = df.apply(lambda x: word_shares(x, weights), axis=1)
    x = get_feature(df)
    x = x.fillna(0)
    return x

if __name__ == '__main__':
    st.title('Demo tìm kiếm câu hỏi tương đồng')
    query = st.text_input('Nhập câu hỏi:')
    btn = st.button('Tìm kiếm')

    # Load model for prediction
    model = lgb.Booster(model_file=MODEL_PATH)
    # load question
    x_test = pd.read_csv(QUESTION_LIST)

    if btn:
        if query == '':
            st.error('Bạn chưa nhập câu hỏi.')
        else:
            # Find similary
            x_test['question2'] = [query] * len(x_test)
            
            # build feature
            x = build_feature(x_test)
            
            # prediction
            preds = predict(model, x)
            
            # select top 5
            top5_idx = np.argsort(preds)[-5:]

            top5_idx = top5_idx[::-1]
            results = [{'question': x_test.iloc[i]['question1'], 'answer': x_test.iloc[i]['answer'], 'score': preds[i]} for i in top5_idx]
            
            # Print result
            st.markdown('### Danh sách kết quả tìm kiếm:')
            for item in results:
                with st.beta_expander('{} ({:.3f}%)'.format(item['question'], item['score'] * 100)):
                    st.write(item['answer'])

