import numpy as np
import streamlit as st
import pandas as pd
import pymysql
import time
from sensor.DingDing import getDingMes
import os

db = pymysql.connect(host="223.5.208.153", user="user1", password="user@123", database="lot", charset="utf8")
cursor = db.cursor()

if 'user' not in st.session_state or 'height' not in st.session_state or 'weight' not in st.session_state:
    st.warning("Login First!")
    st.write(
        'Input your unique username and some info if you have not login before!')
    st.write(
        'You can find your health-care records by your unique username!')
    user = st.text_input('Username: ')
    global height, weight
    height = st.text_input('Height(cm): ')
    weight = st.text_input('Weight(kg): ')

    if not user or not height or not weight:
        st.stop()
    st.session_state['user'] = user
    st.session_state['height'] = height
    st.session_state['weight'] = weight
    st.success(st.session_state['user'] + ',welcome!')
    time.sleep(1)
    st.experimental_rerun()

# Page settings
st.set_page_config(
    page_title="Health-Care Monitoring System",
    page_icon="❄️️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This app generates scripts for data clean rooms!"
    }
)


def get_data_hr():
    db = pymysql.connect(host="223.5.208.153", user="user1", password="user@123", database="lot", charset="utf8")
    sql = "select * from hr where id = (select max(id) from hr)"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    df = pd.read_sql(sql, con=db)
    return df


def get_data_k():
    db = pymysql.connect(host="223.5.208.153", user="user1", password="user@123", database="lot", charset="utf8")
    sql = "select * from kidney where id = (select max(id) from kidney)"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    df = pd.read_sql(sql, con=db)
    return df


def get_data_bq():
    db = pymysql.connect(host="223.5.208.153", user="user1", password="user@123", database="lot", charset="utf8")
    sql = "select * from bp where id = (select max(id) from bp)"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    df = pd.read_sql(sql, con=db)
    return df


def get_data_brain():
    db = pymysql.connect(host="223.5.208.153", user="user1", password="user@123", database="lot", charset="utf8")
    sql = "select * from brain where id = (select max(id) from brain)"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    df = pd.read_sql(sql, con=db)
    return df


def update_dataframe():
    # 生成新的随机数据
    new_data = pd.DataFrame(
        np.random.randint(15, 25, size=(10, 4)),
        columns=['alpha', 'beta', 'theta', 'gamma'])
    # 更新容器中的DataFrame数据
    df_container.dataframe(new_data.style.highlight_max(axis=0), width=1300)


# Set up main page
col1, col2 = st.columns((6, 1))
col1.title("🐻‍Health-Care Monitoring System🐻‍️")
col2.image("assets/snowflake_dcr_multi.png", width=120)
st.sidebar.image("assets/bear_snowflake_hello.png")
st.sidebar.write("🐻‍❄Hello," + st.session_state['user'] + "! I am your doctor bear!🐻‍❄")
st.sidebar.write("I will help you monitor your health-care data! 🩺")
st.sidebar.write("The abnormal situation will be reported to Dingding robot! ⭐️")

st.markdown("🏥 This is a Health-Care Monitoring System. Please click this button to start monitoring!")

col1, col2, col3 = st.columns(3)
col1.metric(label="Height(cm)", value=int(st.session_state['height']), delta=0)
col2.metric(label="Weight(kg)", value=int(st.session_state['weight']), delta=0)
col3.metric(label="BMI", value=np.round(
    int(st.session_state['weight']) * 100 * 100 / (int(st.session_state['height']) * int(st.session_state['height'])),
    2), delta=0)

if st.button("Monitor"):
    with st.spinner('Starting...Just wait for a moment'):
        res = os.system("sh run.sh")
        time.sleep(3)
    info = st.empty()
    last_rows = pd.DataFrame(data=[70], columns=["heartrate"])
    last_rows2 = pd.DataFrame([[70, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]],
                              columns=["heartrate", 'time'])
    last_rows_hr = pd.DataFrame({
        'heart rate': [70],
        'time': [time.strftime("%H:%M:%S", time.localtime())]
    })

    last_rows_k = pd.DataFrame({
        'right kidney': [40],
        'left kidney': [32],
        'time': [time.strftime("%H:%M:%S", time.localtime())]
    })

    # 创建数据帧
    last_rows_bq = pd.DataFrame({
        'time': [time.strftime("%H:%M:%S", time.localtime())],
        'blood pressure': [110],
        'diastolic pressure': [118],
        'systolic pressure': [90],
        'high': [120],
        'low': [60]
    })
    # 创建空容器
    st.write("Brain Wave Results:")
    df_container = st.empty()
    # 初始化DataFrame数据
    df_b = pd.DataFrame(
        np.random.randint(15, 25, size=(10, 4)),
        columns=['alpha', 'beta', 'theta', 'gamma'])
    df_container.dataframe(df_b.style.highlight_max(axis=0), width=1300)

    # 血压
    st.write("Blood Pressure Results:")
    chart_bq = st.line_chart(last_rows_bq.set_index('time'))

    # 心率
    st.write("Heart Rate Results:")
    chart_hr = st.area_chart(last_rows_hr.set_index('time'))

    # 肾脏
    st.write("Kidney Indicators Results:")
    chart_k = st.bar_chart(last_rows_k.set_index('time'))

    while True:
        info.success("Currently monitoring your Brain Wave Heart Rate, Blood Pressure and Kidney Indicators:")
        # 脑电波
        df = get_data_brain()
        update_dataframe()

        # 血压
        df = get_data_bq()
        bp = np.round(df.loc[0, 'bqlow'] / 3 + df.loc[0, 'bqhigh'] * 2 / 3, 0)
        df2 = pd.DataFrame({
            'time': [df.loc[0, 'time']],
            'blood pressure': [bp],
            'diastolic pressure': [df.loc[0, 'bqhigh']],
            'systolic pressure': [df.loc[0, 'bqlow']],
            'high': [120],
            'low': [60],
        })
        last_rows_bq = pd.concat([last_rows_bq, df2])
        chart_bq.line_chart(last_rows_bq.set_index('time'))
        if df.loc[0, 'bqlow'] < 60:
            getDingMes("警报：血压过低")
        elif df.loc[0, 'bqhigh'] > 130:
            getDingMes("警报：血压过高")

        # 心率
        df = get_data_hr()
        df2 = pd.DataFrame({
            'heart rate': [df.loc[0, 'heartrate']],
            'time': [df.loc[0, 'time']]
        })
        last_rows_hr = pd.concat([last_rows_hr, df2])
        chart_hr.area_chart(last_rows_hr.set_index('time'))
        if df.loc[0, 'heartrate'] < 40:
            getDingMes("警报：心率过低")

        # 肾脏
        df = get_data_k()
        df2 = pd.DataFrame({
            'time': [df.loc[0, 'time']],
            'right kidney': [df.loc[0, 'rightkidney']],
            'left kidney': [df.loc[0, 'leftkidney']],
        })
        last_rows_k = pd.concat([last_rows_k, df2])
        chart_k.bar_chart(last_rows_k.set_index('time'))
        time.sleep(0.5)
