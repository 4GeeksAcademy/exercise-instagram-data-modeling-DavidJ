import os
import sys
from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum as EnumColumn
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class MediaType(Enum):
    image = 'image'
    video = 'video'

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    followers = relationship('Follower', foreign_keys='Follower.user_to_id')
    following = relationship('Follower', foreign_keys='Follower.user_from_id')
    comments = relationship('Comment', back_populates='author')
    posts = relationship('Post', back_populates='user')

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
    author = relationship('User', back_populates='comments')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    user = relationship('User', back_populates='posts')
    media = relationship('Media', back_populates='post')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(EnumColumn(MediaType), nullable=False)  
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
    post = relationship('Post', back_populates='media')

    def to_dict(self):
        return {}

# Dibuja el diagrama de la base de datos
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! Verifica el archivo diagram.png")
except Exception as e:
    print("Hubo un problema al generar el diagrama")
    raise e
