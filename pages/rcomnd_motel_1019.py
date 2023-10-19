# 긍정/부정단어를 합해서 긍정이 70% 이상일 경우 추천 숙소로 나눈 코드
# 출력내용: 숙소번호, 모텔명, 숙소별 추천/비추천 구분, 긍정/부정단어 개수, 궁정/부정 비율
# output 파일(sentiment 열 추가)을 토대로 감성분석하기


import pandas as pd
import json
from konlpy.tag import Okt

# 데이터 불러오기
with open('../data/motel_list_last.json', 'r', encoding='utf-8') as f:
    motel_data = json.load(f)

senti_data = pd.read_csv('../data/output5_1019.csv')

# pos_word_list, neg_word_list 업데이트
pos_word_list = senti_data[senti_data['sentiment'] == 'positive']['Keyword'].tolist()
neg_word_list = senti_data[senti_data['sentiment'] == 'negative']['Keyword'].tolist()

# Okt 형태소 분석기 초기화
okt = Okt()

# 숙소별 레벨 나누기
def sookso_level(pos_ratio):
    if pos_ratio >= 0.95:
        return '매우완전추천'
    elif 0.85 <= pos_ratio < 0.95:
        return '완전추천'
    elif 0.70 <= pos_ratio < 0.85:
        return '보통추천'
    else:
        return '비추천'

rcmd_results = []
rcmded_motels=[]
not_rcmded_motels=[]
rcmd_count = {
    '추천숙소': 0,
    '비추천숙소': 0,
    '데이터부족': 0
}

for motel in motel_data:
    total_p_count = 0 # 각 모텔의 긍정단어 총 개수
    total_n_count = 0 # 각 모텔의 부정단어 총 개수

    reviews = motel.get("후기", []) # 예외처리: 후기가 없는 경우 빈 리스트를 반환
    if not reviews:
        rcmd_results.append({
            "숙소번호": motel["숙소번호"],
            "모텔명": motel["모텔명"],
            "추천/비추천": "데이터부족",
            "긍정단어": 0,
            "부정단어": 0,
            "긍정비율": 0,
            "부정비율": 0
        })
        rcmd_count['데이터부족'] += 1
        continue

    for review in motel["후기"]:
        tokenized = okt.morphs(review)
        pos_count = sum(word in tokenized for word in pos_word_list)
        neg_count = sum(word in tokenized for word in neg_word_list)

        total_p_count += pos_count
        total_n_count += neg_count

    # 긍정단어의 비율이 70%가 넘는지 확인
    total_words = total_p_count + total_n_count
    if total_words > 0:
        pos_ratio = total_p_count / total_words
        neg_ratio = total_n_count / total_words
        if pos_ratio > 0.90:
            rcmd = '추천숙소'
            rcmded_motels.append(motel['모텔명'])
        else:
            rcmd = '비추천숙소'
            not_rcmded_motels.append(motel['모텔명'])
    else:
        rcmd = '데이터부족'
        pos_ratio = 0  # 긍정단어나 부정단어가 없는 경우, 긍정단어 비율은 0으로 설정
        neg_ratio = 0  # 긍정단어나 부정단어가 없는 경우, 긍정단어 비율은 0으로 설정
    rcmd_count[rcmd] += 1

    s_level = sookso_level(pos_ratio)
    rcmd_results.append({
        "숙소번호": motel["숙소번호"],
        "모텔명": motel["모텔명"],
        "추천/비추천": s_level,
        "긍정단어" : total_p_count,
        "부정단어" : total_n_count,
        "긍정비율" : round(pos_ratio * 100, 2),  # 퍼센티지로 변환하고 소수 둘째자리까지 반올림
        "부정비율" : round(neg_ratio * 100, 2)
    })

for result in rcmd_results:
    print(result)


# 기존 데이터에 각 숙소별 긍정/부정단어 개수와 비율 추가하기
for motel in motel_data:
    for result in rcmd_results:
        if motel["숙소번호"] == result["숙소번호"]:
            motel.update(result) # motel 딕셔너리에 result 딕셔너리의 내용을 갱신

# DataFrame으로 변환 후 CSV 파일로 저장
df = pd.DataFrame(rcmd_results)
df.to_csv('../data/sookso_level.csv', index=False, encoding='utf-8-sig')

