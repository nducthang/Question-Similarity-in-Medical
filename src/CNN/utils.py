from pyvi import ViTokenizer
import pandas as pd
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
import matplotlib.pyplot as plt

def save_vocabulary(path, vocabulary, word_to_num, num_to_word):
    data = {'vocabulary': vocabulary,
            'word_to_num': word_to_num,
            'num_to_word': num_to_word
            }
    with open(path, 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_vocabulary(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data['vocabulary'], data['word_to_num'], data['num_to_word']


def clean(text):
    text = text.lower().split()
    text = " ".join(text)
    text = ViTokenizer.tokenize(text)
    return text


def build(df):
    df['question1'] = df['question1'].apply(lambda t: clean(t))
    df['question2'] = df['question2'].apply(lambda t: clean(t))

    word_to_num = {}
    num_to_word = {}
    lst_question1 = df['question1'].tolist()
    lst_question2 = df['question2'].tolist()
    words = ['<UNK>', '<PAD>']

    for sent in lst_question1:
        words += sent.split()
    for sent in lst_question2:
        words += sent.split()

    for i, w in enumerate(words):
        word_to_num[w] = i
        num_to_word[i] = w

    return df, words, word_to_num, num_to_word


def convert_data(lst_question, word_to_num):
    questions = [[word_to_num[w] for w in sent.split()]
                 for sent in lst_question]
    questions = pad_sequences(
        questions, maxlen=50, padding='post', truncating='post', value=word_to_num['<PAD>'])
    return questions


def preprocessing(df, word_to_num):
    question1 = convert_data(df['question1'].tolist(), word_to_num)
    question2 = convert_data(df['question2'].tolist(), word_to_num)
    labels = np.array([int(l) for l in df['label'].tolist()])
    return {'question1': question1, 'question2': question2, 'labels': labels}


def plot(history, arr):
    fig, ax = plt.subplots(1, 2, figsize=(20, 5))
    for idx in range(2):
        ax[idx].plot(history.history[arr[idx][0]])
        ax[idx].plot(history.history[arr[idx][1]])
        ax[idx].legend([arr[idx][0], arr[idx][1]], fontsize=18)
        ax[idx].set_xlabel('A', fontsize=16)
        ax[idx].set_ylabel('B', fontsize=16)
        ax[idx].set_title(arr[idx][0] + ' x ' + arr[idx][1], fontsize=16)
    # plt.show()
    plt.savefig('./models/cnn/result.png', dpi=300, bbox_inches='tight')
