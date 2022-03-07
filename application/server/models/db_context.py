from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import DATETIME
from flask_login import UserMixin
from enum import IntEnum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class MessageTypes(IntEnum):
	NEW_MESSAGE = 0
	CONNECTION = 1
	DISCONNECTION = 2
	NAME_CHANGED = 3


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
	user_id = db.Column(
		db.Integer,
		db.ForeignKey("user.user_id",
					  ondelete='CASCADE'),
	)
	msg_type = db.Column(db.Enum(MessageTypes), nullable=False)
	old_username = db.Column(db.String(36))
	new_username = db.Column(db.String(36))
	text = db.Column(db.String(1024))
	date = db.Column(DATETIME(fsp=6), nullable=False)