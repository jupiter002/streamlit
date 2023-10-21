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

json_file = '../data/ps_list_crtd.json'
data = pd.read_json(json_file)

all_reviews = []
reviews_counts = {}
reviews = data['후기'].explode().dropna().tolist()
reviews_counts[json_file] = len(reviews)
all_reviews.extend(reviews)

for json_file, count in reviews_counts.items():
    print(f'From {json_file} : {count} reviews')

fontpath = 'c:/Windows/Fonts/malgun.ttf'
twitter = Okt()

def extract_adjectives(text):
    tagged = twitter.pos(text, stem=True)
    return [word for word, tag in tagged if tag == 'Adjective' and len(word) > 1]

def extract_nouns(text):
    tagged = twitter.pos(text, stem=True)
    return [word for word, tag in tagged if tag == 'Noun' and len(word) > 1]

all_reviews_text = ' '.join(all_reviews)
all_adj = extract_adjectives(all_reviews_text)
all_noun = extract_nouns(all_reviews_text)

counted_adj = Counter(all_adj)
counted_noun = Counter(all_noun)

df_adj = pd.DataFrame(counted_adj.most_common(), columns=['Keyword', 'Frequency'])
df_noun = pd.DataFrame(counted_noun.most_common(), columns=['Keyword', 'Frequency'])
merged_df = pd.concat([df_adj, df_noun], axis=0).reset_index(drop=True)

merged_df.to_csv('../data/jeonnam_ps_words_no_stopword.csv', index=False, encoding='utf-8-sig')

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

    st.pyplot(plt)

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

    st.pyplot(plt)
