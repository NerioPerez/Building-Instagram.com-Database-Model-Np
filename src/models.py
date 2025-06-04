from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    comment = relationship('Comment')
    follower = relationship('Follower')
    post = relationship('Post')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "comments": [c.serialize() for c in self.comment],
            "followers": [f.serialize() for f in self.follower],
            "posts": [p.serialize() for p in self.post],
        }


class Follower(db.Model):
    __tablename__ = 'follower'
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), primary_key=True)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }


class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(120))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post = relationship('Comment')
    media = relationship('Media')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post": [p.serialize() for p in self.post],
            "media": [m.serialize() for m in self.media],
            # do not serialize the password, its a security breach
        }


class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        Enum('image', 'video', 'audio', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
            # do not serialize the password, its a security breach
        }