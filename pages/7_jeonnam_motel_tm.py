# 전남 모텔 텍스트마이닝
# 전남 모텔정보 json 형식을 가져와서 리뷰내용을 워드클라우드로 분석
# 형용사만 했지만 텍스트마이닝 결과가 부족해보여 명사도 추가
# ../data/jeonnam_motel_words_1018.csv 파일로 저장

import pandas as pd
from konlpy.tag import Okt
import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title='Hello, Jeonnam Motel! 😉 ', page_icon='😉')
st.sidebar.header('Hello, Jeonnam Motel!!')
st.title('야놀자 전남 모텔 리뷰 워드클라우드 ✏✏')

# 여러 json파일의 경로
# json_files = ['../mdata/damyang_ghg_motel.json','../mdata/gwangyang_motel.json','../mdata/haenam_wjkjbg_motel.json','../mdata/mokpo_motel.json','../mdata/mooan_sinan_ya_motel.json','../mdata/najoo_hyj_motel.json','../mdata/sooncheon_motel.json','../mdata/yeosu_motel.json']
json_file = '../data/motel_list_last.json'
data = pd.read_json(json_file)


all_reviews = []   # 모든 리뷰를 담자

reviews_counts = {}   # 리뷰개수를 잘 가져왔나 보려고 쓴 코드


reviews = data['후기'].explode().dropna().tolist()  # `explode`로 리스트형태로 되어있는 후기 펼치기

reviews_counts[json_file] = len(reviews)

all_reviews.extend(reviews)

for json_file, count in reviews_counts.items():
    print(f'From {json_file} : {count} reviews')

# 각 지역별 숙소 몇개인지 출력
#print(f'Total reviews in all_reviews: {len(all_reviews)}')

fontpath = 'c:/Windows/Fonts/malgun.ttf'
twitter = Okt()

# stopwords 불러오기
with open("../data/stopwords-kor.txt", "r", encoding="utf-8") as f:
    stopwords = f.readlines()
stopwords = [word.strip() for word in stopwords]  # 줄바꿈 문자 제거

one_char_words = set()  # 1글자짜리 단어는 stopwords에 저장하도록 집합

# 형용사 추출
# tagged: 한국어텍스트에서 형태소 분석결과를 저장하는 변수
def extract_adjectives(text):
    tagged = twitter.pos(text, stem=True)
    words = []
    for word, tag in tagged:
        if tag == 'Adjective':
            if len(word) == 1:    # 1글자 단어면 집합에 추가하고, words에는 추가하지 않는다.
                one_char_words.add(word)
            elif word not in stopwords:  # 1글자 이상의 단어이면서 불용어에 없으면 words에 추가
                words.append(word)
    return words

def extract_nouns(text):
    tagged = twitter.pos(text, stem=True)
    words = []
    for word, tag in tagged:
        if tag == 'Noun':
            if len(word) == 1:    # 1글자 단어면 집합에 추가하고, words에는 추가하지 않는다.
                one_char_words.add(word)
            elif word not in stopwords:  # 1글자 이상의 단어이면서 불용어에 없으면 words에 추가
                words.append(word)
    return words

    # # 명사와 형용사는 추출하고 불용어는 가져오지마
    # return [word for word, tag in tagged if tag in ['Noun', 'Adjective'] and word not in stopwords]

all_reviews_text = ' '.join(all_reviews)     # 전체파일에서 리뷰내용 문자열로 연결
all_adj = extract_adjectives(all_reviews_text)    # 가져온 문자열에서 형용사 추출
all_noun = extract_nouns(all_reviews_text)    # 가져온 문자열에서 명사 추출


counted_adj = Counter(all_adj)   # 형용사카운트 해서 counter_words에 저장
counted_noun = Counter(all_noun)   # 형용사카운트 해서 counter_words에 저장

# 형용사와 명사의 데이터프레임 생성
df_adj = pd.DataFrame(counted_adj.most_common(), columns=['Keyword', 'Frequency'])
df_noun = pd.DataFrame(counted_noun.most_common(), columns=['Keyword', 'Frequency'])

# 두 데이터프레임을 합치기
merged_df = pd.concat([df_adj, df_noun], axis=0).reset_index(drop=True)

# 합친 데이터프레임을 CSV로 저장
merged_df.to_csv('../data/jeonnam_motel_2letters.csv', index=False, encoding='utf-8-sig')

# 1글자 짜리 단어를 stopwords-kor.txt 파일에 추가
with open('../data/stopwords-kor.txt', 'a', encoding='utf-8') as f:
    for word in one_char_words:
        f.write(f'\n{word}')

# 형용사용 워드클라우드 생성
counted_adjectives = Counter(all_adj)
with st.spinner('워드클라우드 생성중... (형용사)'):
    wc_adjectives = WordCloud(font_path=fontpath,
                              background_color="white",
                              width=800,
                              height=600,
                              max_words=10000,
                              max_font_size=100,
                              min_font_size=10
                              ).generate_from_frequencies(counted_adjectives)

    plt.figure(figsize=(10, 8))
    plt.imshow(wc_adjectives, interpolation="bilinear")
    plt.title("형용사 워드클라우드")
    plt.axis('off')

    st.pyplot(plt)  # Streamlit에 형용사용 워드클라우드 출력


#명사용 워드클라우드 생성
counted_nouns = Counter(all_noun)
with st.spinner('워드클라우드 생성중... (명사)'):
    wc_nouns = WordCloud(font_path=fontpath,
                         background_color="white",
                         width=800,
                         height=600,
                         max_words=10000,
                         max_font_size=100,
                         min_font_size=10
                         ).generate_from_frequencies(counted_nouns)

    plt.figure(figsize=(10, 8))
    plt.imshow(wc_nouns, interpolation="bilinear")
    plt.title("명사 워드클라우드")
    plt.axis('off')
    plt.show()

    st.pyplot(plt)  # Streamlit에 명사용 워드클라우드 출력