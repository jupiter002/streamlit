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
json_files = ['./mdata/damyang_ghg_motel.json','./mdata/gwangyang_motel.json','./mdata/haenam_wjkjbg_motel.json','./mdata/mokpo_motel.json','./mdata/mooan_sinan_ya_motel.json','./mdata/najoo_hyj_motel.json','./mdata/sooncheon_motel.json','./mdata/yeosu_motel.json']

all_reviews = []   # 모든 리뷰를 담자

for json_file in json_files:
    data = pd.read_json(json_file)
    reviews = data['후기'].explode().dropna().tolist()  # `explode`로 리스트형태로 되어있는 후기 펼치기
    all_reviews.extend(reviews)

fontpath = 'c:/Windows/Fonts/malgun.ttf'
twitter = Okt()

# stopwords 불러오기
with open("./mdata/stopwords-kor.txt", "r", encoding="utf-8") as f:
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

    # # 명사와 형용사는 추출하고 불용어는 가져오지마
    # return [word for word, tag in tagged if tag in ['Noun', 'Adjective'] and word not in stopwords]

all_reviews_text = ' '.join(all_reviews)     # 전체파일에서 리뷰내용 문자열로 연결
all_adj = extract_adjectives(all_reviews_text)    # 가져온 문자열에서 형용사 추출


counted_adj = Counter(all_adj)   # 형용사카운트 해서 counter_words에 저장



# 1글자 짜리 단어를 stopwords-kor.txt 파일에 추가
with open('./mdata/stopwords-kor.txt', 'a', encoding='utf-8') as f:
    for word in one_char_words:
        f.write(f'\n{word}')

# 형용사용 워드클라우드 생성
counted_adjectives = Counter(all_adj)
with st.spinner('워드클라우드 생성중... (형용사)'):
    wc_adjectives = WordCloud(font_path=fontpath,
                              background_color="white",
                              width=800,
                              height=600).generate_from_frequencies(counted_adjectives)

    words = list(wc_adjectives.words_.items())
    df_words =pd.DataFrame(words,columns=['Keyword','Frequency'])
    df_words.to_csv('./mdata/jeonnam_motel_wc.csv', index=False, encoding='utf-8-sig')

    plt.figure(figsize=(10, 8))
    plt.imshow(wc_adjectives, interpolation="bilinear")
    plt.title("형용사 워드클라우드")
    plt.axis('off')

    st.pyplot(plt)  # Streamlit에 형용사용 워드클라우드 출력





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