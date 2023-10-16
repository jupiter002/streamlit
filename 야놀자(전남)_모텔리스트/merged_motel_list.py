import json
import os

# 합치려는 JSON 파일들이 있는 폴더
directory_path = './mdata/'

# 모든 JSON 파일 목록을 가져옴
json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

merged_data = []

# os.path.join : 경로를 합칠때 사용. 운영체제에 맞게 경로를 합침

for json_file in json_files:
    with open(os.path.join(directory_path, json_file), 'r', encoding='utf-8') as file:
        data = json.load(file)
        merged_data.extend(data)

# '숙소번호' 재정의 및 전체 숙소 넘버링
for index, motel in enumerate(merged_data, start=1):
    motel['숙소번호'] = index

# 합친 및 넘버링된 데이터를 새 JSON 파일에 저장 : ./mdata 파일에 저장(directory_path 를 ./mdata로 써놨음)
with open(os.path.join(directory_path, 'merged_mlist.json'), 'w', encoding='utf-8') as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)

print(f"{len(json_files)}개의 JSON 파일이 'merged_mlist.json'에 합쳐졌습니다.")
