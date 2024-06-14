from flask_socketio import SocketIO, emit

socketio = SocketIO()

@socketio.on('show_popup')
def handle_show_popup(data):
    emit('popup_notification', {'message': data['message'], 'type': data['type']}, broadcast=True)
