import pandas as pd
import numpy as np


def get_words(df):
    train_qs = pd.Series(df['question1'].tolist() +
                         df['question2'].tolist()).astype(str)
    words = (" ".join(train_qs)).lower().split()
    return words


def get_weight(count, eps=10000, min_count=2):
    return 0 if count < min_count else 1/(count+eps)


def word_shares(row, weights):
    # Lấy danh sách các từ trong q1
    q1_list = str(row['question1']).lower().split()
    q1words = set(q1_list)
    if len(q1words) == 0:
        return '0:0:0:0:0:0'

    # Lấy danh sách các từ trong q2
    q2_list = str(row['question2']).lower().split()
    q2words = set(q2_list)
    if len(q2words) == 0:
        return '0:0:0:0:0:0'

    words_hamming = sum(1 for i in zip(q1_list, q2_list)
                        if i[0] == i[1])/max(len(q1_list), len(q2_list))

    # Trả về các cặp 2gram của câu hỏi
    q1_2gram = set([i for i in zip(q1_list, q1_list[1:])])
    q2_2gram = set([i for i in zip(q2_list, q2_list[1:])])

    # Các cặp 2gram chung giữa 2 cây hỏi
    shared_2gram = q1_2gram.intersection(q2_2gram)

    # Các từ chung giữa 2 câu hỏi (Đã loại bỏ stop word)
    shared_words = q1words.intersection(q2words)

    # weight là dict chứa từ và trọng số của từ
    # Lấy vector chứa các trọng số của từ chung giữa 2 câu
    shared_weights = [weights.get(w, 0) for w in shared_words]
    # Lấy vector chứa các trọng số của từng câu
    q1_weights = [weights.get(w, 0) for w in q1words]
    q2_weights = [weights.get(w, 0) for w in q2words]
    # Nối 2 list lại
    total_weights = q1_weights + q2_weights

    # Tính toán các đặc trưng
    R1 = np.sum(shared_weights)/np.sum(total_weights)  # TF-IDF share
    R2 = len(shared_words)/(len(q1words)+len(q2words) -
                            len(shared_words))  # count share
    # R31 = len(q1stops) / len(q1words) #stops in q1
    # R32 = len(q2stops) / len(q2words) #stops in q2

    Rcosine_denominator = (np.sqrt(np.dot(q1_weights, q1_weights))
                           * np.sqrt(np.dot(q2_weights, q2_weights)))
    Rcosine = np.dot(shared_weights, shared_weights) / \
        Rcosine_denominator  # Khoảng cách consine

    if len(q1_2gram) + len(q2_2gram) == 0:
        R2gram = 0
    else:
        R2gram = len(shared_2gram) / (len(q1_2gram) + len(q2_2gram))
    return '{}:{}:{}:{}:{}:{}'.format(R1, R2, len(shared_words), R2gram, Rcosine, words_hamming)


def get_feature(df):
    x = pd.DataFrame()

    x['word_match'] = df['word_shares'].apply(lambda x: float(x.split(':')[0]))
    x['word_match_2root'] = np.sqrt(x['word_match'])
    x['tfidf_word_match'] = df['word_shares'].apply(
        lambda x: float(x.split(':')[1]))
    x['shared_count'] = df['word_shares'].apply(
        lambda x: float(x.split(':')[2]))

    x['shared_2gram'] = df['word_shares'].apply(
        lambda x: float(x.split(':')[3]))
    x['cosine'] = df['word_shares'].apply(lambda x: float(x.split(':')[4]))
    x['words_hamming'] = df['word_shares'].apply(
        lambda x: float(x.split(':')[5]))

    x['len_q1'] = df['question1'].apply(lambda x: len(str(x)))
    x['len_q2'] = df['question2'].apply(lambda x: len(str(x)))
    x['diff_len'] = x['len_q1'] - x['len_q2']

    x['caps_count_q1'] = df['question1'].apply(
        lambda x: sum(1 for i in str(x) if i.isupper()))
    x['caps_count_q2'] = df['question2'].apply(
        lambda x: sum(1 for i in str(x) if i.isupper()))
    x['diff_caps'] = x['caps_count_q1'] - x['caps_count_q2']

    # Đếm xem mỗi câu có bao nhiêu ký tự khác trắng
    x['len_char_q1'] = df['question1'].apply(
        lambda x: len(str(x).replace(' ', '')))
    x['len_char_q2'] = df['question2'].apply(
        lambda x: len(str(x).replace(' ', '')))
    x['diff_len_char'] = x['len_char_q1'] - x['len_char_q2']

    # Đếm số từ ở mỗi câu
    x['len_word_q1'] = df['question1'].apply(lambda x: len(str(x).split()))
    x['len_word_q2'] = df['question2'].apply(lambda x: len(str(x).split()))
    x['diff_len_word'] = x['len_word_q1'] - x['len_word_q2']

    x['exactly_same'] = (df['question1'] == df['question2']).astype(
        int)  # giống nhau hoàn toàn hay không
    x['duplicated'] = df.duplicated(['question1', 'question2']).astype(int)

    return x

