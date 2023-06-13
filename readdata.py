import paho.mqtt.client as mqtt
import json
import csv
from datetime import datetime
import sys

data_list = []

def on_message(client, userdata, message):
    # 受信したデータをプリントする
    data = json.loads(message.payload.decode())
    array_data = list(data["data"][0].values())
    print(array_data)
    data_list.append(array_data)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # トピックを指定して購読する
    client.subscribe("cptdata")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def save_data_to_file():
    if data_list:
        # 現在の日時を取得
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")  # フォーマットを指定して日時を文字列化
        
        # ファイル名を構築
        filename = f"data_{timestamp}.csv"
        
        # データをCSVファイルに保存
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data_list)
        
        print(f"Data saved to {filename}.")
    else:
        print("No data received.")

# MQTTクライアントを作成
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# ブローカーに接続
client.connect("192.168.43.113", 1883, 60)

try:
    # メインループ
    client.loop_start()
    while True:
        pass
except KeyboardInterrupt:
    print("Interrupted by user.")
    save_data_to_file()
    client.disconnect()
    client.loop_stop()