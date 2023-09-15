import threading
import pymysql
import paho.mqtt.client as mqtt
import json

mqtt_host = "192.168.42.1"
port = 1883
topic_bp = "/public/bp"
topic_hr = "/public/hr"
topic_kidney = "/public/kidney"
topic_brain = "/public/brain"
db = pymysql.connect(host="223.5.208.153", user="user1", password="user@123", database="lot", charset="utf8")
cursor = db.cursor()


def connect_mqtt() -> mqtt:
    def on_connect(client: mqtt, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        client.subscribe(topic_bp)
        client.subscribe(topic_hr)
        client.subscribe(topic_kidney)
        client.subscribe(topic_brain)

    def on_message(client: mqtt, userdata, msg):
        str_message = str(msg.payload.decode())
        message = json.dumps(str_message)
        message = eval(json.loads(message))
        if msg.topic == topic_bp:
            sql = "insert into bp (time,bqlow,bqhigh) values ('%s','%s','%s');" % (
                message['time'], message['bqlow'], message['bqhigh'])
            cursor.execute(sql)
            db.commit()
        elif msg.topic == topic_hr:
            sql = "insert into hr (time,heartrate) values ('%s','%s');" % (message['time'], message['heartrate'])
            cursor.execute(sql)
            db.commit()
        elif msg.topic == topic_kidney:
            sql = "insert into kidney (time,rightkidney,leftkidney) values ('%s','%s','%s');" % (
                message['time'], message['rightkidney'], message['leftkidney'])
            cursor.execute(sql)
            db.commit()
        else:
            sql = "insert into brain (time,alpha,beta,theta,gamma) values ('%s','%s','%s','%s','%s');" % (
                message['time'], message['alpha'], message['beta'], message['theta'], message['gamma'])
            cursor.execute(sql)
            db.commit()
        print(msg.topic)
        print(message)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_host, port, 60)
    client.loop_forever()  # 直到客户端调用disconnect函数时才会返回


if __name__ == '__main__':
    threading.Thread(target=connect_mqtt, args=()).start()
