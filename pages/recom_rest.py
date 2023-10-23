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


from numpy import sin, cos, arccos, pi, round


# 멀티 페이지용 제목
st.set_page_config(page_title='안녕하세요! 당신의 숙소추천서비스 숙천이입니다. 🌏🌏🌏',
                   page_icon='╰(*°▽°*)╯╰(*°▽°*)╯╰(*°▽°*)╯')

st.sidebar.header('반가워요!')


def rad2deg(radians): # 라디안을 도로 변환
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees): # 도를 라디안으로 변환
    radians = degrees * pi / 180
    return radians

def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2, unit='kilometers'):
    # 두 점 사이의 경도 차이를 계산
    theta = longitude1 - longitude2
    # 두 점 사이의 거리계산
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) +
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    # 거리를 킬로미터 단위로 변환
    return round(distance * 1.609344, 2)


# csv파일에서 축제 좌표값 가져오기
def getfesdot(fesname):

    fes = pd.read_csv('./data/recom_rest/fesJN2023_최종 (1).csv')

    find = fes['축제명'] == fesname
    idx = fes[find]['좌표'].index

    x = float(fes[find]['좌표'][idx[0]].split(',')[0])
    y = float(fes[find]['좌표'][idx[0]].split(',')[1])
    return x,y


# 숙소와 축제장소의 거리계산
def getdistance(fesname):

    rest_list = []
    result_list = []
    idx = []

    x_1, y_1 = getfesdot(fesname)
    for i in range(len(data)):
        try:
            x_2 = float(data[i]['좌표']['위도'])
            y_2 = float(data[i]['좌표']['경도'])
            distance = getDistanceBetweenPointsNew(x_1, y_1, x_2, y_2)

            # 축제로부터 떨어진 숙소의 거리를 지정
            #print(distance)

            ### select태그를 사용할때 조건문 ###
            print(distance)
            #if select1 == '15km이내':
            #    if distance < 15:
            #        print(data[i]['좌표'], data[i]['모텔명'])
            #        print(distance)
            #        idx.append(i)
            #elif select1 == '15km~30km':
            #    if distance >= 15 and distance <= 30 :
            #        print(data[i]['좌표'], data[i]['모텔명'])
            #        print(distance)
            #        idx.append(i)
            #else:
            #    if distance > 30 and distance <= 60:
            #        print(data[i]['좌표'], data[i]['모텔명'])
            #        print(distance)
            #        idx.append(i)
            ### sliderbar를 사용할때 조건문 ###
            if distance <= slider1:
                #print(data[i]['좌표'], data[i]['모텔명'])
                #print(distance)
                idx = []
                idx.append(i)
                idx.append(distance)
                rest_list.append(idx)
                result_list = sorted(rest_list, key=lambda x: x[1])
        except Exception as e:
            pass
    # 원하는 거리만큼 떨어진 숙소데이터의 인덱스 반환
    return result_list

#a = getdistance('구례산수유꽃축제')
#for i in a:
#    print(i[0])

# 축제 csv파일 불러옴
fes = pd.read_csv('./data/recom_rest/fesJN2023_최종 (1).csv')
fes1 = pd.DataFrame(fes,columns=['시군구명','축제명','축제종류',
                    '개최방식','시작월','시작일','종료월','종료일','개최주소'])




# 축제좌표를 지도에 뿌림
st.write('🎆축제들 좌표🎆')
fig = px.scatter_mapbox(fes, lat='위도', lon='경도', size='예산합계', color='방문객수합계',
                        color_continuous_scale= px.colors.sequential.RdBu,
                        mapbox_style='open-street-map',
                        hover_name= '축제명', hover_data={'예산합계':False,'위도':False,'경도':False,
                                            '개최방식':True, '축제명':False, '개최주소':True,'방문객수합계':False },
                        hover_name= '축제명', hover_data={'위도':False, '경도':False, '축제명':True},
                        opacity=0.9)
fig.update_layout(mapbox_zoom=7.5, width=800, height=600, mapbox_center={"lat": 34.82725246807052, "lon": 126.82132640120547})
st.plotly_chart(fig)



st.write('축제가 열리는 달을 선택해주세요🗓️')



#tab1=st.tabs(["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월",])
#st.write(f'{tab1}월을 선택하셨어요!')

#select_month = 0
#with tab1:
#    select_month = 1


select_month = st.slider('',1,12)
st.write(f'{select_month}월을 선택하셨습니다!')


find = fes1['시작월'] == select_month

st.write(f'🎆{select_month}월의 축제리스트🎆')

fes2 = fes1.sort_values(by='축제명', key=lambda x: x.str.encode('utf-8'))
fes2[find]

st.write('🎆축제리스트🎆')


fes1


fesname=st.text_input("축제명을 검색해주세요🔍")
st.write('입력내용:', fesname)

st.write('')

st.write('원하는 거리의 범위를 선택해주세요🚗')
slider1=st.slider('단위(Km)', 0, 100)
st.write(f'선택한 거리범위는 0km ~ {slider1}km입니다')

#select1=st.selectbox("(위도,경도로 거리를 계산하기 때문에 오차가 있을 수 있습니다)"
                     #["15km이내", "15km~30km", "30km~40km"])
st.write('선택한 값:', slider1)
#select1=st.selectbox("(위도,경도로 거리를 계산하기 때문에 오차가 있을 수 있습니다)", ["15km이내", "15km~30km", "30km~40km"])



st.write('')

select2=st.selectbox("모텔, 펜션중에 선택해주세요🏡", ["모텔", "펜션"])
st.write('선택사항:', select2)


ps = './data/recom_rest/ps_list_last.json'
mt = './data/recom_rest/motel_list_last.json'

# 모텔을 선택할시
if select2 == '모텔':
    with open(mt, 'r', encoding='utf-8') as f:
        rest = f.read()
    rest_csv = pd.read_csv('./data/recom_rest/motel_list_last.csv')
# 펜션을 선택할시
else:
    with open(ps, 'r', encoding='utf-8') as f:
        rest = f.read()
    rest_csv = pd.read_csv('./data/recom_rest/ps_list_last.csv')

data = json.loads(rest)

df = pd.DataFrame()

# 검색한 축제의 좌표를 지도 중앙으로 하기 위해서 가져옴


#getfesdot('거문도백도은빛바다체험행사')
#getdistance('거문도백도은빛바다체험행사')
a = []



try:
    lat, lon = getfesdot(fesname)
    a = getdistance(fesname)
    # 검색한 축제 근처의 숙소들을 지도에 보여줌


    for idx in a:
        df = df._append(rest_csv.iloc[idx[0]], ignore_index=True)


    fig = px.scatter_mapbox(df, lat='좌표/위도', lon='좌표/경도', size='전체평점', color='모텔명',
                            color_continuous_scale= px.colors.sequential.RdBu,
                            mapbox_style='open-street-map',
                            hover_name= '모텔명', hover_data={'좌표/위도':False,'좌표/경도':False,'모텔명':True, '주소':True},
                            opacity=0.9)
    fig.update_layout(mapbox_zoom=10, width=800, height=600, mapbox_center={"lat": lat, "lon": lon})
    st.plotly_chart(fig)

except Exception as e:

    if fesname == '':
        st.warning('어서 축제명을 검색해주세요.현기증 난단 말이예요!😵😵😵')
    elif fesname != '' and slider1 != 0:
        st.error('🤘검색하신 축제명을 다시 확인해주세요! OOPS!!!🤘')
    elif fesname != '' and (slider1 == 0 or len(a) == 0):
        st.error('축제장소에서 숙소까지의 원하는 거리를 선택해주세요')
    else:
        st.write('해당범위내에 숙소가 없습니다. 거리범위를 다시 선택해주세요')

