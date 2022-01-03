import json
import sys
import time
import os

from flask import Flask, request
from flask_cors import CORS

import dateutil.parser as dparser
from datetime import datetime

# from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
CORS(app)
app.config['CORS_AUTOMATIC_OPTIONS'] = True
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
# app.config['CORS_HEADERS'] = 'Content-Type'

# socketio = SocketIO(app, cors_allowed_origins="*")

init_flag = True

user_response = ""
ok_intents = ['好', 'OK', 'ok', '沒問題', '請幫我安排', '是']
nAnswer = 0

date = None


@app.route('/', methods=['GET'])
def main():
    return "Home"


@app.route("/data", methods=['GET'])
def test():
    return "Flask server"


@app.route("/connection", methods=['GET', 'PUT'])
def send_problem():
    global user_response, init_flag, nAnswer, date
    print("establish connection")
    print('user_response: ', user_response)

    if request.method == 'GET':
        isInPattern = False
        for patt in ok_intents:
            if user_response.startswith(patt) and user_response != '':
                isInPattern = True
        if isInPattern:
            init_flag = False
            if nAnswer == 0:
                nAnswer += 1
                user_response = ""
                msg = '行程已安排於1月2號，仁愛路192號，是否預約此時段'
                date = dparser.parse(msg, fuzzy=True)
                date = date.strftime('%Y-%m-%d')
                return_val = json.dumps({'data': msg, 'date': None})
                return return_val
            elif nAnswer == 1:
                nAnswer = 0
                user_response = ""
                return_val = json.dumps({'data': '預約已完成',
                                         'date': {'start': date, 'end': date, 'title': '進廠維修',
                                                  'description': '維修進場'}})

                return return_val

            else:
                user_response = ""
                return_val = json.dumps({'data': '', 'date': None})
                return return_val
        else:
            if init_flag:
                # 送出錯誤訊息
                time.sleep(1)
                return_val = json.dumps({'data': '車子已達定期檢修標準，是否要安排維修行程', 'date': None})
                return return_val
            else:
                return_val = json.dumps({'data': '', 'date': None})
                return return_val
    elif request.method == 'PUT':
        user_json = request.get_json()
        user_response = user_json['data'].split(" ")[-1]
        print('Client answer: ', user_response)
        return user_json
    else:
        print('傳入狀態非GET或是PUT')
        return ''


# @socketio.on("json")
# def handle_json(json):
#     print('received json: ', json)
#
#
# @socketio.on("message")
# def handleMessage(msg):
#     print('received message: ', msg)
#
#
# @socketio.on('connect')
# def test_connect():
#     print('Connected!')
#
#
# @socketio.on("disconnect")
# def test_disconnect():
#     print('Client disconnected')
#
#
# @socketio.on('newMessage')
# def handle_client_msg(msg):
#     print('newMessage')
#     print(msg)
#     # 發送訊息
#     emit("myresponse", 'newMessage')
#
#
# @socketio.on('getMessage')
# def handle_send_message():
#     emit("server_response", 'handle_send_message')


if __name__ == "__main__":
    print('Python version', sys.version)
    port = int(os.environ.get('PORT', 5000))
    print('PORT: ', port)
    app.run(debug=True, port=port)
    # socketio.run(app, port=port)

    msg = '行程已安排於1月2號，仁愛路192號，是否預約此時段'
    # date = dparser.parse(msg, fuzzy=True)
    # print(date)
    # date = date.strftime('%Y-%m-%d')
    # print(date)
