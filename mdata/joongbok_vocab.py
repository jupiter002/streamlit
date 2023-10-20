# txt 파일 중복삭제
def remove_duplicates(sw):
    with open(sw, 'r', encoding='utf-8') as f:  # encoding='utf-8'로 변경
        lines = f.readlines()

    # 중복확인
    unique_lines = set()
    cleaned_lines = []

    for line in lines:
        # 이미 unique_lines에 존재하지 않는 라인만 추가
        if line not in unique_lines:
            cleaned_lines.append(line)
            unique_lines.add(line)

    # 결과를 다시 파일에 쓰기
    with open(sw, 'w', encoding='utf-8') as f:  # encoding='utf-8'로 변경
        f.writelines(cleaned_lines)

    print(f"{len(lines) - len(cleaned_lines)}개의 중복된 라인을 제거했습니다.")

# 사용 예시
sw = '../data/stopwords-kor.txt'
remove_duplicates(sw)


# 파일의 타입 확인하기
# import chardet
#
# def detect_encoding(filename):
#     with open(filename, 'rb') as f:
#         result = chardet.detect(f.read())
#     return result['encoding']
#
# filename = '../data/stopwords-kor.txt'
# encoding = detect_encoding(filename)
# print(f"Detected encoding: {encoding}")



# 중복요소 삭제
# import json
#
# # JSON 파일 불러오기
# with open('../data/motel_list_last.json', 'r', encoding='utf-8') as f:
#     motel_data = json.load(f)
#
# # 223번 항목 삭제
# motel_data = [motel for motel in motel_data if motel['숙소번호'] != 223]
#
# # 다시 넘버링
# for idx, motel in enumerate(motel_data, start=1):
#     motel['숙소번호'] = idx
#
# # 수정된 데이터를 JSON 파일에 저장
# with open('../data/motel_list_last.json', 'w', encoding='utf-8') as f:
#     json.dump(motel_data, f, ensure_ascii=False, indent=4)

# 중복 모텔 체크
# import json
# import pandas as pd
#
# # JSON 파일 불러오기
# with open('../data/motel_list_last.json', 'r', encoding='utf-8') as f:
#     motel_data = json.load(f)
#
# # 데이터를 DataFrame으로 변환
# df = pd.DataFrame(motel_data)
#
# # "모텔명" 컬럼에서 중복된 요소 확인
# duplicated_motel_names = df[df["모텔명"].duplicated(keep=False)]["모텔명"].unique()
#
# # 중복된 모텔명 출력
# if len(duplicated_motel_names) > 0:
#     print("중복된 모텔명:")
#     for name in duplicated_motel_names:
#         print(name)
# else:
#     print("중복된 모텔명이 없습니다.")


# 중복 단어 체크
# import pandas as pd
#
# pos_words = pd.read_csv('../data/positive_dic.csv')
# neg_words = pd.read_csv('../data/negative_dic.csv')
# # 긍정/부정 단어 리스트 변환
# pos_word_list = pos_words['긍정'].tolist()
# neg_word_list = neg_words['부정'].tolist()
#
# # 중복된 단어 확인
# duplicated_words = set(pos_word_list) & set(neg_word_list)
#
# # 중복된 단어 출력
# print("중복된 단어:", duplicated_words)
#
# # 중복된 단어의 개수 출력
# print("중복된 단어 개수:", len(duplicated_words))