from flask_socketio import emit
from html_code import socketio


@socketio.on('show_popup')
def handle_show_popup(data):
    emit('popup_notification', {'message': data['message'], 'type': data['type']}, broadcast=True)
