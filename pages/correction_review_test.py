import requests
import json

# JSON 파일에서 데이터 로드
with open('../data/ps_list_last.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1번 숙소의 20개 후기
reviews = data[0]['후기']
base_url = "https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy"



headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

corrected_reviews = []

for review in reviews:
    params = {
        'passportKey':'f889d5ee7ab9379c02331da9f04cc4b36001c960',
        'q': review,
        'where': 'nexearch',
        'color_blindness': 0
    }

    response = requests.get(base_url, headers=headers, params=params)
    print(response.text)


    # JSON 형태의 응답 추출
    # json_str = response.text.split('(', 1)[1].rsplit(')', 1)[0]
    result_data = json.loads(response.text)

    corrected_review = result_data['message']['result']['notag_html']
    corrected_reviews.append(corrected_review)

# 결과 출력
for original, corrected in zip(reviews, corrected_reviews):
    print(f"원본: {original}")
    print(f"교정: {corrected}")
    print("------")
