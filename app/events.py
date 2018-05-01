from app import app
from flask import session
#from flask_socketio import emit, join_room, leave_room
from .__init import socketio

@socketio.on('joined_public', namespace='/public_chat')
def joined_public(message):
	"""Sent by clients when they enter a room.
	A status message is broadcast to all people in the room."""
	room = 'free-for-all' #open chat session.get('room')
	join_room(room)
	emit('status', {'person': session.get('name'), 'msg': ' has joined.'}, room=room)

@socketio.on('text_public', namespace='/public_chat')
def text_public(message):
	"""Sent by a client when the user entered a new message.
	The message is sent to all people in the room."""
	room = 'free-for-all' #open chat session.get('room')
	emit('message', {'person': session.get('name'), 'msg': ' : ' + message['msg']}, room=room)

@socketio.on('left_public', namespace='/public_chat')
def left_public(message):
	"""Sent by clients when they leave a room.
	A status message is broadcast to all people in the room."""
	room = 'free-for-all' #open chat session.get('room')
	leave_room(room)
	emit('status', {'person': session.get('name'), 'msg': ' has left.'}, room=room)


@socketio.on('joined_private', namespace='/public_chat')
def joined_private(message):
	"""Sent by clients when they enter a room.
	A status message is broadcast to all people in the room."""
	room = 'two-to-tango' #open chat session.get('room')
	join_room(room)
	emit('status', {'msg': session.get('name') + ' is online.'}, room=room)

@socketio.on('text_private', namespace='/public_chat')
def text_private(message):
	"""Sent by a client when the user entered a new message.
	The message is sent to all people in the room."""
	room = 'two-to-tango' #open chat session.get('room')
	emit('message', {'msg': session.get('name') + ' : ' + message['msg']}, room=room)

@socketio.on('left_private', namespace='/public_chat')
def left_private(message):
	"""Sent by clients when they leave a room.
	A status message is broadcast to all people in the room."""
	room = 'two-to-tango' #open chat session.get('room')
	leave_room(room)
	emit('status', {'msg': session.get('name') + ' is offline.'}, room=room)
