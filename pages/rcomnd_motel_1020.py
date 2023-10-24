# 출력내용: 숙소번호, 모텔명, 숙소별 추천/비추천 구분, 긍정/부정단어 개수, 궁정/부정 비율
# output 파일(sentiment 열 추가)을 토대로 감성분석하는 코드임

# 숙소의 각 리뷰별 긍정/부정 단어 비율로 다시 분류하여 추천기준에 따라 다시 나눔.....


import pandas as pd
import json
from konlpy.tag import Okt

# 데이터 불러오기
with open('../data/motel_list_last.json', 'r', encoding='utf-8') as f:
    motel_data = json.load(f)

senti_data = pd.read_csv('../data/output6_1020.csv')

# pos_word_list, neg_word_list 업데이트
pos_word_list = senti_data[senti_data['sentiment'] == 'positive']['Keyword'].tolist()
neg_word_list = senti_data[senti_data['sentiment'] == 'negative']['Keyword'].tolist()

# Okt 형태소 분석기 초기화
okt = Okt()

boonseok_results = []

for motel in motel_data:
    pos_reviews = 0 # 긍정리뷰 카운트
    pos_w_freq = {} # 긍정 단어 빈도수
    neg_w_freq = {} # 부정 단어 빈도수

    review_detail = []  # 리뷰별 상세 정보를 저장할 리스트

    reviews = motel.get("후기", []) # 예외처리: 후기가 없는 경우 빈 리스트를 반환

    if not reviews:
        boonseok_results.append({
            "숙소번호": motel["숙소번호"],
            "모텔명": motel["모텔명"],
            "추천여부":"데이터부족"
        })
        continue

    for idx, review in enumerate(motel["후기"], start=1):
        tokenized = okt.morphs(review)
        pos_count = 0
        neg_count = 0
        for word in tokenized:
            if word in pos_word_list:
                pos_reviews += 1
                pos_w_freq[word] = pos_w_freq.get(word, 0) + 1
                pos_count += 1
            if word in neg_word_list:
                neg_w_freq[word] = neg_w_freq.get(word, 0) + 1
                neg_count += 1

        review_detail.append({
            "리뷰순": idx,
            "긍정단어 개수": pos_count,
            "부정단어 개수": neg_count
        })

    # 상위 5개 긍정/부정 단어 가져오기
    top5_pos_words = sorted(pos_w_freq, key=pos_w_freq.get, reverse=True)[:5]
    top5_neg_words = sorted(neg_w_freq, key=neg_w_freq.get, reverse=True)[:5]

    if pos_reviews >= 15:
        rcmd = "매우추천숙소"
    elif 10 <= pos_reviews < 15:
        rcmd = "추천숙소"
    elif 5 <= pos_reviews < 10:
        rcmd = "보통숙소"
    else:
        rcmd = "비추천숙소"


    boonseok_results.append({
        "숙소번호": motel["숙소번호"],
        "모텔명": motel["모텔명"],
        "리뷰별 상세": review_detail,
        "추천여부": rcmd,
        "상위5긍정단어": ", ".join(top5_pos_words),
        "상위5부정단어": ", ".join(top5_neg_words)
    })


# DataFrame으로 변환 후 CSV 파일로 저장
df = pd.DataFrame(boonseok_results)
df.to_csv('../data/sookso_each_review_count.csv', index=False, encoding='utf-8-sig')

