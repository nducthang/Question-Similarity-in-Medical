import pandas as pd
import numpy as np
from collections import Counter
from utils import get_weight, word_match_share
from sklearn.model_selection import train_test_split
import xgboost as xgb

df_train = pd.read_csv("./data/processed/train.csv")
train_qs = pd.Series(df_train['question1'].tolist(
) + df_train['question2'].tolist()).astype(str)
eps = 5000
words = (" ".join(train_qs)).lower().split()
counts = Counter(words)
weights = {word: get_weight(count) for word, count in counts.items()}


def tfidf_word_match_share(row):
    q1words = {}
    q2words = {}
    for word in str(row['question1']).lower().split():
        q1words[word] = 1
    for word in str(row['question2']).lower().split():
        q2words[word] = 1
    if len(q1words) == 0 or len(q2words) == 0:
        return 0
    shared_weights = [weights.get(w, 0) for w in q1words.keys(
    ) if w in q2words] + [weights.get(w, 0) for w in q2words.keys() if w in q1words]
    total_weights = [weights.get(w, 0) for w in q1words] + \
        [weights.get(w, 0) for w in q2words]

    R = np.sum(shared_weights) / np.sum(total_weights)
    return R


if __name__ == '__main__':
    train_word_match = df_train.apply(word_match_share, axis=1)
    tfidf_train_word_match = df_train.apply(tfidf_word_match_share, axis=1)

    x_train = pd.DataFrame()
    x_train['word_match'] = train_word_match
    x_train['tfidf_word_match'] = tfidf_train_word_match
    y_train = df_train['label'].values

    x_train, x_val, y_train, y_val = train_test_split(
        x_train, y_train, test_size=0.2, random_state=28091997)

    # Set parameters for xgboost
    params = {}
    params['objective'] = 'binary:logistic'
    params['eval_metric'] = 'logloss'
    params['eta'] = 0.02
    params['max_depth'] = 4

    d_train = xgb.DMatrix(x_train, label=y_train)
    d_val = xgb.DMatrix(x_val, label=y_val)

    watchlist = [(d_train, 'train'), (d_val, 'valid')]
    bst = xgb.train(params, d_train, 400, watchlist,
                    early_stopping_rounds=50, verbose_eval=10)
