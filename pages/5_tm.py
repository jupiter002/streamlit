import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud


# 멀티 페이지용 제목
st.set_page_config(page_title='Hello, textmining! ⛏⛏⛏',
                   page_icon='╰⛏╯')

st.sidebar.header('Hello, textmining! ⛏⛏⛏')

st.write('텍스트마이닝 시각화')

# 폰트 및 형태소 분석 초기화
fontpath = 'c:/Windows/Fonts/malgun.ttf'
twitter = Okt()

with open('./data/trump_ko.txt', encoding='utf-8') as f:
    docs = f.read()

st.write(docs[:300])

# 워드클라우스 시각화 1
tokens = twitter.nouns(docs)
words = [ t for t in tokens if len(t) > 1 ]

with st.spinner('워드클라우드 생성중...'):
    wc = Counter(words)
    wc = dict(wc.most_common())

    wcimg = WordCloud(font_path=fontpath, background_color='white', width=650, height=480).generate_from_frequencies(wc)
    fig = plt.figure()
    ax = plt.imshow(wcimg, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)

# 워드클라우드 시각화 2

with open('./data/stevejobs_ko.txt') as f:
    docs = f.read()

option1 = st.selectbox('보고싶은 연설문을 선택하세요', ['잡스형', '도람뿌'])
# optcols = 'pop' if option1 == '구별 총인구수' else \
#     'korpop' if option1 == '구별 총내국인수'



