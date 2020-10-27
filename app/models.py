from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import os
from app import app, db

userPodcast = db.Table('UserPodcast',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('podcast_id', db.Integer, db.ForeignKey('podcast.id'), primary_key=True)
                       )

userEpisode = db.Table('UserEpisode',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('episode_id', db.Integer, db.ForeignKey('episode.id'), primary_key=True)
                       )

replies = db.Table('replies',
                   db.Column('original', db.Integer, db.ForeignKey('comment.id')),
                   db.Column('reply', db.Integer, db.ForeignKey('comment.id'))
                   )

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


def default_avatar():
    return 'default.png'


from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


# inherit from UserMixin for flask-login
class User(SearchableMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    podcasts = db.relationship('Podcast', secondary=userPodcast, lazy='dynamic',
                               # primaryjoin=(userPodcast.c.user_id == id),
                               backref=db.backref('user')
                               )
    episodes = db.relationship('Episode', secondary=userEpisode, lazy='dynamic',
                               # primaryjoin=(userEpisode.c.user_id == id),
                               backref=db.backref('user')
                               )
    __searchable__ = ['username']
    photo = db.Column(db.String(200), default=default_avatar())
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow_user(self, user):
        if not self.is_following_user(user):
            self.followed.append(user)

    def unfollow_user(self, user):
        if self.is_following_user(user):
            self.followed.remove(user)

    def is_following_user(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def avatar(self, size):
        if self.photo is not None:
            return os.path.join(
                app.config['PHOTO_PATH'], self.photo)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username
        }
        return data

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, podcast):
        if not self.is_following(podcast):
            self.podcasts.append(podcast)

    def unfollow(self, podcast):
        if self.is_following(podcast):
            self.podcasts.remove(podcast)

    def is_following(self, podcast):
        return self.podcasts.filter(
            userPodcast.c.podcast_id == podcast.id).count() > 0

    def listen(self, episode):
        if not self.has_listened_episode(episode):
            self.episodes.append(episode)

    def has_listened_episode(self, episode):
        return self.episodes.filter(
            userEpisode.c.episode_id == episode.id).count() > 0

    def get_liked_podcasts(self):
        return self.podcasts

    def get_listened_episodes(self):
        return User.query.join(userEpisode).filter(User.id == self.id) \
            .join(Episode) \
            .join(Podcast) \
            .add_columns(Podcast.body, Podcast.id.label("podcast_id"), Episode.timestamp,
                         Episode.id.label("episode_id"),
                         Episode.title,
                         Episode.audio_link, Episode.image, Episode.description) \
            .order_by(Episode.timestamp.desc())

    def get_podcast_with_episodes(self, page):
        return User.query.join(userPodcast).filter(User.id == self.id) \
            .join(Podcast) \
            .join(Episode) \
            .add_columns(Podcast.body, Podcast.id.label("podcast_id"), Episode.timestamp, Episode.id, Episode.title,
                         Episode.audio_link, Episode.image, Episode.description) \
            .order_by(Episode.timestamp.desc()) \
            .paginate(page, 5, False).items

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    author = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users = db.relationship('User', secondary=userPodcast, lazy='dynamic',
                            # primaryjoin=(userPodcast.c.podcast_id == id),
                            # backref=db.backref('podcasts')
                            )
    episodes = db.relationship('Episode', backref='podcast', lazy=True)
    image = db.Column(db.String(500))
    description = db.Column(db.String(5000))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def number_of_followers(self):
        return self.users.count()

    def get_all_episodes(self):
        return self.episodes

    def __repr__(self):
        return '<Podcast {}>'.format(self.body)


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcast.id'),
                           nullable=False)
    audio_link = db.Column(db.String(500))
    description = db.Column(db.String(5000))
    image = db.Column(db.String(500))
    users = db.relationship('User', secondary=userEpisode, lazy='dynamic')

    def get_podcast(self):
        return Podcast.query.get(self.podcast_id)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    podcasts = db.relationship('Podcast', backref='category', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    message = db.Column(db.String(5000))
    episode_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), nullable=True)
    reply = db.relationship(
        'Comment', secondary=replies,
        primaryjoin=(replies.c.original == id),
        secondaryjoin=(replies.c.reply == id),
        backref=db.backref('replies', lazy='dynamic'), lazy='dynamic')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
