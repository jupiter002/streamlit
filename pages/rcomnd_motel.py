import pandas as pd
import json
from konlpy.tag import Okt

# 데이터 불러오기
with open('../mdata/merged_mlist.json', 'r', encoding='utf-8') as f:
    motel_data = json.load(f)

pos_words = pd.read_csv('../data/positive_dic.csv')
neg_words = pd.read_csv('../data/negative_dic.csv')

# 긍정/부정 단어 리스트로 변환
pos_word_list = pos_words['긍정'].tolist()
neg_word_list = neg_words['부정'].tolist()

# Okt 형태소 분석기 초기화
okt = Okt()

recommendation_results = []

for motel in motel_data:
    scores = []
    total_p_count = 0 # 각 모텔의 긍정단어 총 개수
    total_n_count = 0 # 각 모텔의 부정단어 총 개수
    for review in motel["후기"]:
        tokenized = okt.morphs(review)
        pos_count = sum(word in tokenized for word in pos_word_list)
        neg_count = sum(word in tokenized for word in neg_word_list)

        total_p_count += pos_count
        total_n_count += neg_count

        score = pos_count - neg_count
        scores.append(score)

    # 후기들의 평균 점수를 구함
    avg_score = sum(scores) / len(scores) if scores else 0

    # 평균 점수에 따라 추천/비추천 결정
    if avg_score > 0:
        recommendation = "추천숙소"
    else:
        recommendation = "비추천숙소"

    recommendation_results.append({
        "숙소번호": motel["숙소번호"],
        "모텔명": motel["모텔명"],
        # "추천/비추천": recommendation,
        "긍정단어" : total_p_count,
        "부정단어" : total_n_count
    })

for result in recommendation_results:
    print(result)

# 긍정 및 부정 단어 개수의 평균을 구하는 부분
total_pos_words = sum(item['긍정단어'] for item in recommendation_results)
total_neg_words = sum(item['부정단어'] for item in recommendation_results)

avg_positive_words = total_pos_words / len(recommendation_results) if recommendation_results else 0
avg_negative_words = total_neg_words / len(recommendation_results) if recommendation_results else 0

print(f"평균 긍정단어 개수: {avg_positive_words:.2f}")
print(f"평균 부정단어 개수: {avg_negative_words:.2f}")


# rcmd_count = sum(1 for item in recommendation_results if item["추천/비추천"] == "추천숙소")
# notrcmd_count = sum(1 for item in recommendation_results if item["추천/비추천"] == "비추천숙소")
#
# print(f"추천숙소 개수: {rcmd_count}")
# print(f"비추천숙소 개수: {notrcmd_count}")

# JSON으로 저장 (추가)
with open('../mdata/mchoocheon_or_not.json', 'w', encoding='utf-8') as f:
    json.dump(recommendation_results, f, ensure_ascii=False, indent=4)
