#In Python, a sub-directory that includes a __init__.py file is considered a package, and can be imported.
#When you import a package, the __init__.py executes and defines what symbols the package exposes to the outside world.

#export FLASK_APP=microblog.py
#the flask command relies on the FLASK_APP environment variable to know where the Flask application lives. set FLASK_APP=microblog.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__)           #python predefined var set to the name of the module in which it is used, app here is defined as instance of class Flask
app.config.from_object(Config)  #read and apply config file
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
moment = Moment(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
login.login_view = 'login'
from app import routes          #the routes module needs to import the app variable defined in this script, so putting one of the reciprocal imports at the 
								#bottom avoids the error that results from the mutual references between these two files.
#In Flask, handlers for the application routes are written as Python functions, called view functions.

from app import models          #structure of database

socketio.run( app, debug = False )

# if __name__ == '__main__':
# 	print("before")
# 	socketio.run( app, debug = True )
# 	print("after")