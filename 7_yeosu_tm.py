import pandas as pd
from konlpy.tag import Okt
import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# import nltk
# nltk.download()

# 단어를 원형으로 바꿔서  변환.. 정렬하기

st.set_page_config(page_title='Hello, Yeosu Motel! 😉 ', page_icon='😉')
st.sidebar.header('Hello, Yeosu Motel!!')
st.title('야놀자 여수 모텔 리뷰 워드클라우드 ✏✏')

data = pd.read_json('./data/yeosu_motel.json')
reviews = data['후기'].explode().dropna().tolist()  # `explode`로 리스트형태로 되어있는 후기 펼치기


fontpath = 'c:/Windows/Fonts/malgun.ttf'
twitter = Okt()

# stopwords 불러오기
with open("./data/stopwords-kor.txt", "r", encoding="utf-8") as f:
    stopwords = f.readlines()
stopwords = [word.strip() for word in stopwords]  # 줄바꿈 문자 제거

one_char_words = set()  # 1글자짜리 단어는 stopwords에 저장하도록 집합

# 형용사 추출
def extract_adjectives(text):
    tagged = twitter.pos(text, stem=True)
    words = []
    for word, tag in tagged:
        if tag == 'Adjective':
            if word not in stopwords and len(word) > 1:
                words.append(word)
            elif len(word) == 1:
                one_char_words.add(word)
    return words


# 부사추출
def extract_adverbs(text):
    tagged = twitter.pos(text, stem=True)
    words = []
    for word, tag in tagged:
        if tag == 'Adverb':  # 'Adverb' 태그만 확인
            if word not in stopwords and len(word) > 1:
                words.append(word)
            elif len(word) == 1:
                one_char_words.add(word)
    return words

    # # 명사와 형용사는 추출하고 불용어는 가져오지마
    # return [word for word, tag in tagged if tag in ['Noun', 'Adjective'] and word not in stopwords]

all_reviews = ' '.join(reviews)             # 여수모텔 파일에서 리뷰내용 문자열로 연결
yeosu_adj = extract_adjectives(all_reviews)    # 가져온 문자열에서 형용사 추출
yeosu_adv = extract_adverbs(all_reviews)    # 가져온 문자열에서 부사 추출

counted_adj = Counter(yeosu_adj)   # 형용사카운트 해서 counter_words에 저장
counted_adv = Counter(yeosu_adv)   # 명사카운트 해서 counter_words에 저장


# 1글자 짜리 단어를 stopwords-kor.txt 파일에 추가
with open('./data/stopwords-kor.txt', 'a', encoding='utf-8') as f:
    for word in one_char_words:
        f.write(f'\n{word}')

# 형용사용 워드클라우드 생성
counted_adjectives = Counter(yeosu_adj)
with st.spinner('워드클라우드 생성중... (형용사)'):
    wc_adjectives = WordCloud(font_path=fontpath,
                              background_color="white",
                              width=800,
                              height=600).generate_from_frequencies(counted_adjectives)

    plt.figure(figsize=(10, 8))
    plt.imshow(wc_adjectives, interpolation="bilinear")
    plt.title("형용사 워드클라우드")
    plt.axis('off')
    plt.show()

    st.pyplot(plt)  # Streamlit에 형용사용 워드클라우드 출력

# 부사용 워드클라우드 생성
counted_adverbs = Counter(yeosu_adv)
with st.spinner('워드클라우드 생성중... (부사)'):
    wc_adverbs = WordCloud(font_path=fontpath,
                              background_color="white",
                              width=800,
                              height=600).generate_from_frequencies(counted_adverbs)

    plt.figure(figsize=(10, 8))
    plt.imshow(wc_adverbs, interpolation="bilinear")
    plt.title("부사 워드클라우드")
    plt.axis('off')
    plt.show()

    st.pyplot(plt)  # Streamlit에 부사용 워드클라우드 출력





# def extract_nouns(text):
#     tagged = twitter.pos(text, stem=True)
#     words = []
#     for word, tag in tagged:
#         if tag == 'Noun':
#             if word not in stopwords and len(word) > 1:
#                 words.append(word)
#             elif len(word) == 1:
#                 one_char_words.add(word)
#     return words

# 명사용 워드클라우드 생성
# counted_nouns = Counter(yeosu_n)
# with st.spinner('워드클라우드 생성중... (명사)'):
#     wc_nouns = WordCloud(font_path=fontpath,
#                          background_color="white",
#                          width=800,
#                          height=600).generate_from_frequencies(counted_nouns)
#
#     plt.figure(figsize=(10, 8))
#     plt.imshow(wc_nouns, interpolation="bilinear")
#     plt.title("명사 워드클라우드")
#     plt.axis('off')
#     plt.show()
#
#     st.pyplot(plt)  # Streamlit에 명사용 워드클라우드 출력