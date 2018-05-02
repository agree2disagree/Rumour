from app import app
from flask import render_template, flash, redirect, url_for
from flask import request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, EditProfileForm
from datetime import datetime
import requests
from app import socketio
# from flask import session, redirect, url_for, render_template, request
#from . import main

@app.route('/')         #decorator
@app.route('/index')
@login_required
def index():
	user = {'username':'Nico di Angelo'}
	posts = [{
			'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
		}]
	return render_template('index.html',title = 'Home', posts=posts)

@app.route('/login', methods = ['GET', 'POST'])    #view function accepts GET and POST methods, default: only GET
                                                   #else Method Not Allowed error, Post: to the server
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		# session['name'] = form.username.data
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)
		#flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':           #for security, refer below
			return redirect(url_for('index'))
		return redirect(next_page)
	return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET','Post'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Thanks for registering to Rumour! Head out and meet new people!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen=datetime.utcnow()
	
		freegeoip = "http://freegeoip.net/json"
		geo_r = requests.get(freegeoip)
		geo_json = geo_r.json()

		user_position = [geo_json["country_name"], geo_json["city"]]
		current_user.country_name = user_position[0]
		current_user.city_name = user_position[1]
		db.session.commit()

# @app.route('/public_chat') #public chat
# def public_chat():
# 	"""Chat room. The user's name and room must be stored in
# 	the session."""
# 	name = session.get('name', '')
# 	room = 'free-for-all' #open chat session.get('room')
# 	return render_template('public_chat.html', name=name, room=room)

# @app.route('/private_chat/<username>') #private chat
# def private_chat(username):
# 	"""Chat room. The user's name and room must be stored in
# 	the session."""
# 	name = session.get('name', '')
# 	room = 'two-to-tango' #closed chat session.get('room')
# 	return render_template('private_chat.html', name=name, room=room)

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username=form.username.data
		current_user.about_me=form.about_me.data
		db.session.commit()
		flash('Changes have been saved!')
		return redirect(url_for('index'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form = form)

#If the login URL includes a next argument that is set to a full URL that includes a domain name, then the user is redirected to the index page.
#is in place to make the application more secure. An attacker could insert a URL to a malicious site in the next argument,
# so the application only redirects when the URL is relative

#To determine if the URL is relative or absolute, I parse it with Werkzeug's url_parse() function 
#and then check if the netloc component is set or not.

# chat basic
@app.route( '/chat' )
def chat():
	username = current_user.username
	return render_template('chat.html', username=username)

def messageRecived():
	print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
	# print( 'recived my event: ' + str( json ) )
	socketio.emit( 'my response', json, callback=messageRecived )