from app import app, db               #imports the app variable that is a member of the app package
from app.models import User

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'User':User}