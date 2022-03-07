from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import DATETIME
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
	__tablename__ = 'user'
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(36), nullable=False, unique=True)
	password_hash = db.Column(db.String(256), nullable=False)

	def __repr__(self):
		return "<{0}: {1}>".format(self.user_id, self.username)

	def get_id(self):
		return self.user_id

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Message(db.Model):
	__tablename__ = 'message'
	message_id = db.Column(db.Integer, primary_key=True)
	owner_id = db.Column(
		db.Integer,
		db.ForeignKey("user.user_id",
					  ondelete='CASCADE'),
	)
	text = db.Column(db.String(1024), nullable=False)
	date = db.Column(DATETIME(fsp=6), nullable=False)


class UsernameHistory(db.Model):
	__tablename__ = 'usernamehistory'
	event_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey("user.user_id",
					  ondelete='CASCADE'),
	)
	old_username = db.Column(db.String(36), nullable=False)
	new_username = db.Column(db.String(36), nullable=False)
	date = db.Column(DATETIME(fsp=6), nullable=False)


class ConnectionHistory(db.Model):
	__tablename__ = 'connectionhistory'
	event_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey("user.user_id",
					  ondelete='CASCADE'),
	)
	is_connected = db.Column(db.Boolean, nullable=False) # connection if true, disconnection if false
	date = db.Column(DATETIME(fsp=6), nullable=False)