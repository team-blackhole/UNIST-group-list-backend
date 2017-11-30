from app import db
from app.base.models import Base

class Notice(Base):

    __tablename__ = 'notice_notice'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    contents = db.Column(db.Text(), nullable=False)
    is_shown = db.Column(db.Boolean(), nullable=False)
    is_public = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return '<Notice %r>' % (self.title)

    def serialize(self):
        serialized_data = {
            "title": self.title,
            "contents": self.contents,
            "is_shown": self.is_shown,
            "is_public": self.is_public
        }
        return serialized_data


