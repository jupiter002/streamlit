#  이거는 최종 완성본을 가져와서 결과만 볼 수 있게끔 하는게 좋음. // 전처리를 여기서 하는건 힘듦
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
import altair as alt
import plotly.express as px
from bokeh.plotting import figure

import json
import plotly.graph_objects as go

# 멀티 페이지용 제목
st.set_page_config(page_title='Hello, geopraphy! 🌏🌏🌏',
                   page_icon='╰(*°▽°*)╯╰(*°▽°*)╯╰(*°▽°*)╯')

st.sidebar.header('Hello, geopraphy!')

st.write('지리정보 시각화')

st.subheader('서울시 인구 데이터 2023')
seoulpop = pd.read_csv('./data/seoulpop_2023.csv')
st.write(seoulpop.head())

# 지도시각화 1 - st.map : 근데 영어기반이라 비추
seoulpop['pop2']=seoulpop['pop'].apply(lambda x: x / 10000)
print(seoulpop['pop2'])
st.map(seoulpop, latitude='lat', longitude='lon', color='#ff0000', size='pop2')

# 지도시각화 2 - plotly : open-street-map 쓰면 한글도 나옴
fig = px.scatter_mapbox(seoulpop, lat='lat', lon='lon', size='pop2', color='pop2',
                                 color_continuous_scale= px.colors.sequential.BuGn,
                                 mapbox_style='open-street-map',
                                 hover_name= 'gu', hover_data={'lat':False, 'lon':False, 'pop2':False, 'pop':True},
                                 opacity=0.9)
fig.update_layout(mapbox_zoom=10.5, width=800, height=600, mapbox_center={"lat": 37.532600, "lon": 127.024612})
st.plotly_chart(fig)

# 지도시각화 3 - 동적시각화
option1 = st.selectbox('보고싶은 인구현황을 선택하세요', ['구별 총인구수', '구별 총내국인수','구별 총외국인수'])
optcols = 'pop' if option1 == '구별 총인구수' else \
            'korpop' if option1 == '구별 총내국인수' else 'forepop'

optcolor = px.colors.sequential.RdBu if option1 == '구별 총인구수' else \
            px.colors.sequential.YlGn if option1 == '구별 총내국인수' else \
            px.colors.sequential.Rainbow

seoulpop['pop2']=seoulpop[optcols].apply(lambda x: x / 10000)

fig = px.scatter_mapbox(seoulpop, lat='lat', lon='lon', size='pop2', color='pop2',
                        color_continuous_scale= optcolor,
                        mapbox_style='open-street-map',
                        hover_name= 'gu', hover_data={'lat':False, 'lon':False, 'pop2':False, optcols:True},
                        opacity=0.9)

fig.update_layout(mapbox_zoom=10.5, width=800, height=600, mapbox_center={"lat": 37.532600, "lon": 127.024612})
st.plotly_chart(fig)

#  지도시각화 4 - 단계구분도
with open('./data/seoul_geo_simple.json', encoding='utf-8') as f:
    geo = json.load(f)

#st.write(geo['features'][0]['properties']['name'])

fig = go.Figure(
    go.Choroplethmapbox(geojson=geo, locations=seoulpop['gu'], featureidkey='properties.name', z=seoulpop['pop'], colorscale='Viridis', marker_opacity=0.5)
)
fig.update_layout( mapbox_style = 'open-street-map',mapbox_zoom=10.5, width=800, height=600, mapbox_center={"lat": 37.532600, "lon": 127.024612}, margin={'t':0,'r':0,'b':0,'l':0})
st.plotly_chart(fig)

# 지도시각화 4 - 동적시각화

with open('./data/seoul_geo_simple.json', encoding='utf-8') as f:
    geo = json.load(f)

# option2 = st.selectbox('보고싶은 구별 인구현황을 선택하세요', ['강동구','송파구','강남구','서초구','관악구','동작구','영등포구','금천구','구로구','강서구','양천구','마포구','서대문구','은평구','노원구','도봉구','','','','','','','',','','','','','','','',''])
# optcols = 'pop' if option1 == '구별 총인구수' else \
#     'korpop' if option1 == '구별 총내국인수' else 'forepop'
#
# optcolor = px.colors.sequential.RdBu if option1 == '구별 총인구수' else \
#     px.colors.sequential.YlGn if option1 == '구별 총내국인수' else \
#         px.colors.sequential.Rainbow
#
# seoulpop['pop2']=seoulpop[optcols].apply(lambda x: x / 10000)

fig = px.scatter_mapbox(seoulpop, lat='lat', lon='lon', size='pop2', color='pop2',
                        color_continuous_scale= optcolor,
                        mapbox_style='open-street-map',
                        hover_name= 'gu', hover_data={'lat':False, 'lon':False, 'pop2':False, optcols:True},
                        opacity=0.9)

fig.update_layout(mapbox_zoom=10.5, width=800, height=600, mapbox_center={"lat": 37.532600, "lon": 127.024612})
st.plotly_chart(fig)

