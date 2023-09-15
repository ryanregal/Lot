import random
import paho.mqtt.client as mqtt
import time

mqtt_host = "192.168.42.1"
mqtt_client = mqtt.Client()
port = 1883
topic_bp = "/public/bp"
topic_hr = "/public/hr"
topic_kidney = "/public/kidney"
topic_brain = "/public/brain"


# 连接服务器
def on_connect():
    mqtt_client.connect(host=mqtt_host, port=port, keepalive=60)
    # 每次连接后运行一个线程来自动调用loop（定期调用处理读取或写入）
    mqtt_client.loop_start()


# 发送消息
def publish(my_topic):
    msg = {}
    my_time = time.strftime("%H:%M:%S", time.localtime())
    if my_topic == topic_bp:
        msg['bqlow'] = random.randint(55, 90)
        msg['bqhigh'] = random.randint(90, 130)
        msg['time'] = my_time
    elif my_topic == topic_hr:
        msg['heartrate'] = random.randint(50, 130)
        msg['time'] = my_time
    elif my_topic == topic_kidney:
        msg['rightkidney'] = random.randint(30, 40)
        msg['leftkidney'] = random.randint(30, 40)
        msg['time'] = my_time
    else:
        msg['time'] = my_time
        msg['alpha'] = random.randint(15, 30)
        msg['beta'] = random.randint(15, 30)
        msg['theta'] = random.randint(15, 30)
        msg['gamma'] = random.randint(15, 30)

    mqtt_client.publish(my_topic, str(msg))
    return msg


def main():
    on_connect()  # 连接服务器
    while True:
        res1 = publish(topic_bp)
        res2 = publish(topic_hr)
        res3 = publish(topic_kidney)
        res4 = publish(topic_brain)
        print("此时发送血压数据:" + str(res1))
        print("此时发送心率数据:" + str(res2))
        print("此时发送肾脏数据:" + str(res3))
        print("此时发送脑电波数据:" + str(res4))
        time.sleep(1)


if __name__ == '__main__':
    main()
