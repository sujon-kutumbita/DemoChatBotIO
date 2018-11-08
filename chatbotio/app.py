#!/usr/bin/env python
import json

from threading import Lock
from flask import Flask, render_template, session, request, abort
from flask_socketio import SocketIO, emit
from constants import HOST, PORT

from chatbotapp.bot import get_response

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


# @app.route('/kt-chatbot', methods=['POST'])
# def chatbot_manage():
#     if not request.json:
#         abort(400)
#     data = request.json
#     print(data)
#     response = {'data': get_response(data['data'])}
#     print(f"chat {response}")
#     return json.dumps(response)

chat_dict = {"response_text":"how are you?"}


@app.route('/kt-chatbot/', methods=['POST'])
def chatbot_manage():
    if not request.json:
        abort(400)
    data = request.json
    chat_dict['response_text'] = get_response(data['msg'])
    print(f"chat {chat_dict}")
    return json.dumps(chat_dict)



@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/kt-chatbot')
def incoming_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    print(f"message {get_response(message['data'])}")
    a = {'data': message['data'], 'count': session['receive_count']}
    print(f"response send {a}")
    emit('my_event',
         {'data': get_response(message['data']), 'count': session['receive_count']})


@socketio.on('connect', namespace='/kt-chatbot')
def server_connect():
    emit('server_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/kt-chatbot')
def server_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host=HOST, port=PORT, debug=True)
