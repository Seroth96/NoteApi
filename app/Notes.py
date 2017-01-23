from app import db

class Note(db.Model):
    __tablename__ = 'note_content'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref=db.backref('category', lazy='dynamic'))

    tag_id =db.Column(db.Integer, db.ForeignKey('tag.id'))
    tag = db.relationship('Tag',
                backref=db.backref('tag', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
                             backref=db.backref('users', lazy='dynamic'))

    def __init__(self, title, body, category_id, tag_id, user_id):
        self.title = title
        self.body = body
        self.category_id = category_id
        self.tag_id = tag_id
        self.user_id = user_id

    def __repr__(self):
        return '<Note %r>' % self.title

    def serialize(self):
        return dict(title=self.title,
                    body=self.body,
                    category_id=self.category_id,
                    tag_id=self.tag_id,
                    user_id=self.user_id,
                    id=self.id)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id= user_id

    def __repr__(self):
        return '<Category %r>' % self.name

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id= user_id

    def __repr__(self):
        return '<Tag %r>' % self.name
