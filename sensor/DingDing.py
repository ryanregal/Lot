import json
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://oapi.dingtalk.com/robot/send?access_token' \
      '=15b8710c4d02c3815421d029345887416435494ae4b82ce1541977ca2a78611e'


def getDingMes(data):
    # 更改为自己的钉钉机器人
    baseUrl = "https://oapi.dingtalk.com/robot/send?access_token=15b8710c4d02c3815421d029345887416435494ae4b82ce1541977ca2a78611e"

    # please set charset= utf-8
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    # 这里的message是你想要推送的文字消息
    message = str(data)
    stringBody = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [""],
            "isAtAll": "false"  # @所有人 时为true，上面的atMobiles就失效了
        }
    }
    MessageBody = json.dumps(stringBody)
    result = requests.post(url=baseUrl, data=MessageBody, headers=HEADERS)
