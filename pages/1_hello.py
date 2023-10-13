import streamlit as st
import time

print(st.__version__)

# 멀티 페이지용 제목
st.set_page_config(page_title='Hello, Widget!',
                            page_icon='╰(*°▽°*)╯╰(*°▽°*)╯╰(*°▽°*)╯')

st.sidebar.header('Hello, Widget!')


# 제목 위젯
st.title('My 제목')
st.header('My 헤더')
st.subheader('My 소제목')

# 텍스트 위젯
st.text('간단한 문장문장문선 출력')

# 수식 위젯
st.latex(r''' e^{i\pi} + 1 = 0 ''')

# 코드 위젯
st.code('for i in range(8): foo()')

# 버튼 위젯
if st.button('Click me'):
    st.write('helllllllllo, world!')

# 체크박스위젯
if st.checkbox("I agree"):
    st.write('동의 ㅇㅋ')

option1= st.radio("Pick one", ["cats", "dogs"])
st.write('선택사항:', option1)

option2=st.selectbox("Pick one", ["cats", "dogs"])
st.write('선택사항:', option2)

option3=st.multiselect("what do you wanna buy?", ["milk", "apples", "potatoes"])
st.write('선택사항:', option3)

# 입력 위젯
text1=st.text_input("First name")
st.write('입력내용:', text1)

text1a=st.text_input("your password", type='password')
st.write('입력내용:', text1a)

nums=st.number_input("Pick a number", 0, 10)
st.write('입력내용:', nums)

text2=st.text_area("Text to translate")
st.write('입력내용:', text2)

date1=st.date_input("Your birthday")
st.write(' 오늘날짜:', date1)

time1=st.time_input("Meeting time")
st.write('오늘시간:', time1)

csv1=st.file_uploader("Upload a CSV")
st.write('파일:', csv1)

# ui 위젯

slider1=st.slider('Pick a number', 0, 100)
st.write('선택한 값:', slider1)

slider2=st.select_slider('Pick a size', ['s','m','l'])
st.write('선택한 사이즈:', slider2)

# progress, status 위젯
st.toast('Warming up...')
st.error('Error message')
st.warning('Warning message')
st.info('Info message')
st.success('Success message')


# with st.spinner(text='In progress'):
#     time.sleep(3)
#     st.success('Done')
#
# bar = st.progress(0)
# for i in range(0, 100+1, 10):
#     bar.progress(i)
#     time.sleep(1)

# sidebar 위젯
st.sidebar.radio('Select one:', [1, 2])

# 레이아웃 위젯
col1, col2 = st.columns(2)
col1.write("This is column 1")
col2.write("This is column 2")

# 탭 위젯
tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
tab1.write("this is tab 1")
tab2.write("this is tab 2")
