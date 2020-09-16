from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

userPodcast = db.Table('UserPodcast',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('podcast_id', db.Integer, db.ForeignKey('podcast.id'), primary_key=True)
                       )


# inherit from UserMixin for flask-login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    podcasts = db.relationship('Podcast', secondary=userPodcast, lazy='dynamic',
                               # primaryjoin=(userPodcast.c.user_id == id),
                               backref=db.backref('user')
                               )

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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
