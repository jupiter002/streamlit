# 긍정/부정단어 개수 카운팅
# 전남 전체 모텔 - 감성분석 코드
# positive/negative로 분류하여 각 1, -1 점으로 구분
# 중립단어는 0인데, 긍정/부정 분류가 정확한 단어가 0으로 되어있는 경우가 많아서 중립단어리스트는 재분류했음(수작업)..

import pandas as pd
from konlpy.tag import Okt

# 데이터 불러오기
mtdata = pd.read_csv('../data/jeonnam_motel_words_1018.csv')
pos_words = pd.read_csv('../data/positive_dic.csv')
neg_words = pd.read_csv('../data/negative_dic.csv')

# 긍정/부정 단어 리스트로 변환
pos_word_list = pos_words['긍정'].tolist()
neg_word_list = neg_words['부정'].tolist()

# Okt 형태소 분석기 초기화
okt = Okt()

# 감성분석 수행
scores = []

for text in mtdata['Keyword']:
    tokenized = okt.morphs(text)
    pos_count = sum([word in tokenized for word in pos_word_list])
    neg_count = sum([word in tokenized for word in neg_word_list])

    score = pos_count - neg_count
    scores.append(score)

# 점수에 따라 감성 판단(긍정: 1, 부정: -1, 중립: 0)
sentiments = ['positive' if score > 0 else 'negative' if score < 0 else 'neutral' for score in scores]

# # 숙소별 긍정/부정단어 개수 카운팅
# def get_sentiment_details(mtdata, motel_number, pos_word_list, neg_word_list, okt):
#     motel_row = mtdata[mtdata['숙소번호'] == motel_number]
#     if motel_row.empty:
#         print("해당 숙소번호를 찾을 수 없습니다.")
#         return
#
#     text = motel_row['Keyword'].iloc[0]
#     tokenized = okt.morphs(text)
#     pos_keywords = [word for word in tokenized if word in pos_word_list]
#     neg_keywords = [word for word in tokenized if word in neg_word_list]
#
#     print(f"숙소번호 {motel_number}의 긍정단어 개수:", len(pos_keywords))
#     print(f"숙소번호 {motel_number}의 부정단어 개수:", len(neg_keywords))
#     print("긍정단어 리스트:", pos_keywords)
#     print("부정단어 리스트:", neg_keywords)
#
# # 원하는 숙소번호로 분석 진행
# motel_number_to_check = 47  # 예시로 1번 숙소를 지정. 원하는 숫자로 변경 가능
# get_sentiment_details(mtdata, motel_number_to_check, pos_word_list, neg_word_list, okt)

# 결과 추가
mtdata['sentiment'] = sentiments

# 긍정, 부정 감성 단어개수 카운트
positive_count = sentiments.count('positive')
negative_count = sentiments.count('negative')
neutral_count = sentiments.count('neutral')


print(f"긍정적인 단어의 개수: {positive_count}")
print(f"부정적인 단어의 개수: {negative_count}")
print(f"중립 단어의 개수: {neutral_count}")

# 결과 출력 및 저장
print(mtdata)
mtdata.to_csv('../data/output4.csv', index=False)
