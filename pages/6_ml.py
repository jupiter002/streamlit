import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# 멀티 페이지용 제목
st.set_page_config(page_title='Hello, machine learning!🏃‍♀️ ',
                   page_icon='🏃')

st.sidebar.header('Hello, machine learning!!')

st.write('머신러닝 학습 및 시각화')

# iris 데이터를 이용한 학습 및 모델 생성
iris = pd.read_csv('./data/iris.csv')
st.write(iris.head())

data = iris[['sepal_length','sepal_width','petal_length','petal_width']]
target = iris['species']

st.title('iris feature')
st.write(data.head())

st.title('iris target')
st.write(target.head())

st.title('RandomForestClassifier')
x_train, x_test, y_train, y_test = train_test_split(
    data, target, test_size=.75, stratify=target)
rfc = RandomForestClassifier(random_state=15)
rfc.fit(x_train, y_train)
y_pred = rfc.predict(x_test.values)
score = accuracy_score(y_pred, y_test)

st.success(f' 랜덤포레스트 분류기로 학습된 모델의 정확도는 {score} 입니다!')

# 학습된 모델을 직렬화 객체로 생성 - pickle
with open('./data/rfc_iris.pickle', 'wb') as p:
    pickle.dump(rfc, p)



# 다중 분류기로 iris 데이터 학습 및 모델 생성
st.selectbox('학습에 사용할 분류기를 선택하세요',
             ['로지스틱 회귀','의사결정 나무','랜덤포레스트','그라디언트부스팅','최근접이웃분류', '서포트벡터분류', 'LightGB'])