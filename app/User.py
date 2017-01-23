from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False, unique=True)

    password = db.Column(db.String(120), nullable=False, unique=False)

    notes = db.relationship('Note', backref='db_users', lazy='dynamic')

    categories = db.relationship('Category', backref='user', lazy='dynamic')

    tags = db.relationship('Tag', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return dict(
            id=self.id,
            username=self.username
        )

