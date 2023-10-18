# 전남 전체 모텔 - 감성분석 코드
# positive/negative로 분류하여 각 1, -1 점으로 구분
# 중립단어는 0인데, 중립단어리스트는 재분류했음(수작업)..

import pandas as pd
from konlpy.tag import Okt

# 데이터 불러오기
mtdata = pd.read_csv('./mdata/jeonnam_motel_wc.csv')
pos_words = pd.read_csv('./mdata/positive_dic.csv')
neg_words = pd.read_csv('./mdata/negative_dic.csv')

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

# 중립인 단어들만 필터링하여 리스트로 저장
neutral_keywords = [keyword for i, keyword in enumerate(mtdata['Keyword']) if sentiments[i] == 'neutral']

for keyword in neutral_keywords:
    print(keyword)

# 결과 추가
mtdata['sentiment'] = sentiments

# 결과 출력 및 저장
print(mtdata)
mtdata.to_csv('./mdata/output.csv', index=False)
