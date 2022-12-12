from .database import db
from flask_security import UserMixin, RoleMixin
from flask_login import login_manager
from sqlalchemy import inspect

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=1)
    #fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Cards(db.Model):
    __tablename__ = 'Cards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String)
    deadline = db.Column(db.String)
    completedFlag = db.Column(db.Boolean, default=False)
    parentList = db.Column(db.String)
    lastUpdated = db.Column(db.String, default=None, nullable=True)
    createdOn = db.Column(db.String)
    completedOn = db.Column(db.String, default=None, nullable=True)
    user_id = db.Column(db.Integer)
    
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class Listss(db.Model):
    __tablename__ = 'Lists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer)
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

        
'''class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    authors = db.relationship("User", secondary="article_authors")

class ArticleAuthors(db.Model):
    __tablename__ = 'article_authors'
    user_id = db.Column(db.Integer,   db.ForeignKey("user.id"), primary_key=True, nullable=False)
    article_id = db.Column(db.Integer,  db.ForeignKey("article.article_id"), primary_key=True, nullable=False) 

class ArticleLikes(db.Model):
    __tablename__ = 'article_likes'
    user_id = db.Column(db.Integer,   db.ForeignKey("user.id"), primary_key=True, nullable=False)
    article_id = db.Column(db.Integer,  db.ForeignKey("article.article_id"), primary_key=True, nullable=False) '''