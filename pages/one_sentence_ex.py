# 한문장씩 테스트 해보기

import pandas as pd
from konlpy.tag import Okt

# 예시 문장
text = "테이블 밑에서는 과자부스러기가 있었고 화장실에서는 두마리의 바선생과 만났습니다 사장님께서 친절하셨지만 연박시 추가요금이 결제된다는 사실을 사전고지해주지 않으셨는데 1시쯤 전화와서는 대실 받아야 하는데 왜 나가지 않느냐고 하셨습니다 사전 안내 받은 거 없다고 하니 야놀자의 문제이니 전화로 예약해달라고 하셨습니다"

# 긍정/부정 단어 사전 불러오기
pos_words = pd.read_csv('../data/positive_dic.csv')
neg_words = pd.read_csv('../data/negative_dic.csv')

# 긍정/부정 단어 리스트로 변환
pos_word_list = pos_words['긍정'].tolist()
neg_word_list = neg_words['부정'].tolist()

# Okt 형태소 분석기 초기화
okt = Okt()

# 감성분석 수행(pos/neg detected = 긍정/부정단어 리스트
tokenized = okt.morphs(text, stem=True)
pos_detected = [word for word in tokenized if word in pos_word_list]
neg_detected = [word for word in tokenized if word in neg_word_list]

# 긍정/부정 개수 알기
pos_count = len(pos_detected)
neg_count = len(neg_detected)

# 긍정 단어의 비율 계산
total_count = pos_count + neg_count  # 긍정과 부정 단어의 총 개수
if total_count == 0:  # 긍정/부정 단어가 아예 없는 경우를 처리
    sentiment = 'neutral'
else:
    pos_ratio = pos_count / total_count
    if pos_ratio > 0.7:
        sentiment = 'positive'
    elif pos_ratio < 0.3:  # 이 부분은 긍정 단어의 비율이 30% 미만일 때 부정으로 판단하도록 설정
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

print(f"분석된 문장의 감성: {sentiment}")
print(f"긍정적인 단어의 개수: {pos_count}")
print(f"부정적인 단어의 개수: {neg_count}")
print(f"긍정적인 단어 리스트: {pos_detected}")
print(f"부정적인 단어 리스트: {neg_detected}")
