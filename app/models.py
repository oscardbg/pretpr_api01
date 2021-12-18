from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.String(100), unique=True)
	name = db.Column(db.String(100))
	password = db.Column(db.String(100))
	admin = db.Column(db.Boolean)
	todos = db.relationship('Todo', backref='user')

	def __str__(self):
		return f'{self.id}, {self.name} '

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(150))
	complete = db.Column(db.Boolean)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __str__(self):
		return f'Todo {self.id} '
