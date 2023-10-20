import requests
import json
import time

# 네이버 맞춤법 검사 함수
def correction(text):
    url = "https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy"
    params = {
        "passportKey": "f889d5ee7ab9379c02331da9f04cc4b36001c960",
        "q": text,
        "where": "nexearch",
        "color_blindness": 0
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error with status code {response.status_code}: {response.text}")
        return text  # 에러 발생시 원본 텍스트 반환

    try:
        json_str = response.text.split('(', 1)[1].rsplit(')', 1)[0]
        data = json.loads(json_str)
        return data['message']['result']['notag_html']
    except Exception as e:
        print(f"Error processing the response: {response.text}")
        return text  # 에러 발생시 원본 텍스트 반환

# json 파일에서 후기 가져오기
with open('../data/ps_list_last.json', 'r', encoding='utf-8') as f:
    data= json.load(f)

    # 각 후기에 대해 맞춤법 검사를 진행
    for i, item in enumerate(data):
        print(f"Processing item {i+1}/{len(data)}...")

        for j, review in enumerate(item["후기"]):
            corrected_review = correction(review)
            item["후기"][j] = corrected_review

            # API 호출 간에 약간의 딜레이를 추가하여 네이버 서버에 부담을 주지 않도록 합니다.
            time.sleep(0.5)

# 업데이트된 후기를 다시 JSON 파일에 저장
with open("../data/ps_list_crtd.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

