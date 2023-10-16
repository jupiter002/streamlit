import pandas as pd

pos_words = pd.read_csv('../data/positive_dic.csv')
neg_words = pd.read_csv('../data/negative_dic.csv')
# 긍정/부정 단어 리스트 변환
pos_word_list = pos_words['긍정'].tolist()
neg_word_list = neg_words['부정'].tolist()

# 중복된 단어 확인
duplicated_words = set(pos_word_list) & set(neg_word_list)

# 중복된 단어 출력
print("중복된 단어:", duplicated_words)

# 중복된 단어의 개수 출력
print("중복된 단어 개수:", len(duplicated_words))