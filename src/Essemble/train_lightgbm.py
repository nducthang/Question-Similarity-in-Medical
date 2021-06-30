""" 
Refer:
https://www.python-machinelearning.com/2020/07/27/how-to-retrain-a-saved-lightgbm-model/
"""
import pandas as pd
from utils import word_shares, get_feature
from utils import get_words, get_weight
from collections import Counter
from ruamel import yaml
from sklearn.model_selection import train_test_split
import lightgbm as lgb

# Read data
df_train = pd.read_csv('./data/train.csv')

# setup
words = get_words(df_train)
counts = Counter(words)
weights = {word: get_weight(count) for word, count in counts.items()}
df_train['word_shares'] = df_train.apply(
    lambda x: word_shares(x, weights), axis=1)

# get feature
x = get_feature(df_train)
feature_names = list(x.columns.values)
print("Features:", feature_names)
y = df_train['label'].values

# Load params
params = yaml.safe_load(open('./src/Essemble/params_lightgbm.yaml'))
MODEL_PATH = './models/essemble/lightgbm.bin'
ROUNDS = 200
RS = 123457

def train(X, y, params):
    print('Train for {} rounds, Randomseed: {}'.format(ROUNDS, RS))
    x_train, x_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=RS)
    lgb_train = lgb.Dataset(x_train, label=y_train)
    lgb_val = lgb.Dataset(x_val, label=y_val)
    watchlist = [lgb_train, lgb_val]
    clf = lgb.train(params, lgb_train, ROUNDS, watchlist)
    return clf


def predict(clf, x_test):
    return clf.predict(x_test)

if __name__ == '__main__':
    clf = train(x.fillna(0), y, params)
    clf.save_model(MODEL_PATH)