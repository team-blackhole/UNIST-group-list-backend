from app import db
from app.base.models import Base

class Club(Base):
    club_name = db.Column(db.String(32), nullable=False)
    introduce_one_line = db.Column(db.String(128), nullable=False)
    introduce_full = db.Column(db.Text(), nullable=False)
    #thumbnail_image = db.Column(db.Image(), nullable=True)



#class BlogPost(Base):

    #__tablename__ = 'blog_blogpost'

    #title = db.Column(db.String(255), nullable=False)
    #content = db.Column(db.Text(), nullable=False)
    #published = db.Column(db.Boolean, default=False)
    #slug = db.Column(db.String(255), nullable=False, unique=True)

    #def __init__(self, title, content, **kwargs):
        #self.title = title 
        #self.content = content 
        #self.set_slug(self.title)
        #if 'published' in kwargs:
            #self.published = kwargs.get('published')

    #def __repr__(self):
        #return '<BlogPost %r>' % (self.title)


