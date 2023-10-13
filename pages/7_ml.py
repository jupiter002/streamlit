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

st.title('데이터분석 🍔🍔')

# 직렬화 해둔 모델 파일로 데이터 분석
with open('./data/rfc_iris.pickle', 'rb') as pk:
    model = pickle.load(pk)

#pred = model.predict([[5.1, 3.5, 1.4, 0.2]])
#pred = model.predict([[7.0,3.2,4.7,1.4]])
pred = model.predict([[6.8,3.0,5.5,2.1]])

st.info(f' 분석 후 예측된 품종은 {pred} 입니다')

# iris feature에 따른 품종분석
st.subheader('iris 품종분석')
iris = pd.read_csv('./data/iris.csv')
sl_val = st.slider('sepal length', iris.sepal_length.min(), iris.sepal_length.max(), value=iris.sepal_length.mean())
sw_val = st.slider('sepal width', iris.sepal_width.min(), iris.sepal_width.max(), value=iris.sepal_width.mean())
pl_val = st.slider('petal length', iris.petal_length.min(), iris.petal_length.max(), value=iris.petal_length.mean())
pw_val = st.slider('petal width', iris.petal_width.min(), iris.petal_width.max(), value=iris.petal_width.mean())



pred2 = model.predict([[ sl_val, sw_val, pl_val, pw_val]])
st.info(f' 분석 후 예측된 품종은 {pred2} 입니다')


st.subheader('iris 중요 변수 분석')
cols = iris.iloc[:, :4].columns

# 중요도 그래프
fig, ax = plt.subplots()
ax = sns.barplot(x=model.feature_importances_, y=cols, hue=cols)
plt.xlabel('importance')
plt.ylabel('feature')
st.pyplot(fig)

# 변수별 분포 그래프
fig, ax = plt.subplots()
ax = sns.displot(x=iris.sepal_length, kind='kde', hue=iris.species)
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=iris.sepal_width, kind='kde', hue=iris.species)
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=iris.petal_length, kind='kde', hue=iris.species)
st.pyplot(ax)

fig, ax = plt.subplots()
ax = sns.displot(x=iris.petal_width, kind='kde', hue=iris.species)
st.pyplot(ax)

