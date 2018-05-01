from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from log

# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client

# app = Flask(__name__)

# app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
# socketio = SocketIO( app )

from .__init__ import app

@app.route( '/chat' )
def chat_test():
  username = cur
  return render_template( './chat.html', username='shelly' )

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messageRecived )

# if __name__ == '__main__':
#   socketio.run( app, debug = True )