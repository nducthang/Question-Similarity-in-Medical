import numpy as np

def word_match_share(row):
    q1words = {}
    q2words = {}
    for word in str(row['question1']).lower().split():
        q1words[word] = 1
    for word in str(row['question2']).lower().split():
        q2words[word] = 1
    if len(q1words) == 0 or len(q2words) == 0:
        return 0
    share_words_in_q1 = [w for w in q1words.keys() if w in q2words]
    share_words_in_q2 = [w for w in q2words.keys() if w in q1words]
    R = (len(share_words_in_q1) + len(share_words_in_q2))/(len(q1words)+len(q2words))
    return R

def get_weight(count, eps=10000, min_count=2):
    # Nếu một từ chỉ xuất hiện một lần, chúng tôi sẽ bỏ qua nó hoàn toàn (có thể là lỗi chính tả)
    # Epsilon xác định một hằng số làm mịn, làm cho hiệu ứng của các từ cực hiếm trở nên nhỏ hơn
    if count < min_count:
        return 0
    else:
        return 1.0 /(count+ eps)