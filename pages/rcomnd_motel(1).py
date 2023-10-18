# 긍정/부정단어를 합해서 긍정이 70% 이상일 경우 추천 숙소로 나눈 코드
# 출력내용: 숙소번호, 모텔명, 숙소별 추천/비추천 구분, 긍정/부정단어 개수, 궁정/부정 비율
# 출력해서 기존데이터


import pandas as pd
import json
from konlpy.tag import Okt

# 데이터 불러오기
with open('../data/motel_list_last.json', 'r', encoding='utf-8') as f:
    motel_data = json.load(f)

pos_words = pd.read_csv('../data/positive_dic.csv')
neg_words = pd.read_csv('../data/negative_dic.csv')

# 긍정/부정 단어 리스트로 변환
pos_word_list = pos_words['긍정'].tolist()
neg_word_list = neg_words['부정'].tolist()

# Okt 형태소 분석기 초기화
okt = Okt()

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
        if pos_ratio > 0.95:
            rcmd = '추천숙소'
            rcmded_motels.append(motel['모텔명'])
        else:
            rcmd = '비추천숙소'
            not_rcmded_motels.append(motel['모텔명'])
    else:
        rcmd = '숙소추천을 위한 데이터가 부족합니다.'
        pos_ratio = 0  # 긍정단어나 부정단어가 없는 경우, 긍정단어 비율은 0으로 설정
        neg_ratio = 0  # 긍정단어나 부정단어가 없는 경우, 긍정단어 비율은 0으로 설정
    rcmd_count[rcmd] += 1

    rcmd_results.append({
        "숙소번호": motel["숙소번호"],
        "모텔명": motel["모텔명"],
        "추천/비추천": rcmd,
        "긍정단어" : total_p_count,
        "부정단어" : total_n_count,
        "긍정비율" : round(pos_ratio * 100, 2),  # 퍼센티지로 변환하고 소수 둘째자리까지 반올림
        "부정비율" : round(neg_ratio * 100, 2)
    })

for result in rcmd_results:
    print(result)

print('추천숙소 개수:', rcmd_count['추천숙소'])
print('비추천숙소 개수:', rcmd_count['비추천숙소'])
print('데이터 부족 숙소 개수:', rcmd_count['데이터부족'])

# 기존 데이터에 각 숙소별 긍정/부정단어 개수와 비율 추가하기
for motel in motel_data:
    for result in rcmd_results:
        if motel["숙소번호"] == result["숙소번호"]:
            motel["추천/비추천"] = result["추천/비추천"]
            motel["긍정단어"] = result["긍정단어"]
            motel["부정단어"] = result["부정단어"]
            motel["긍정비율"] = result["긍정비율"]
            motel["부정비율"] = result["부정비율"]

print('추천숙소 리스트:')
for motel_name in rcmded_motels:
    print(motel_name)

print('\n비추천숙소 리스트:')
for motel_name in not_rcmded_motels:
    print(motel_name)

# 수정된 데이터를 다시 motel_list_last.json 파일에 저장하기
# with open('../data/motel_list_last.json', 'w', encoding='utf-8') as f:
#     json.dump(original_motel_data, f, ensure_ascii=False, indent=4)