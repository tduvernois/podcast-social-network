from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.models import Podcast, User, Episode, Comment, userPodcast, userEpisode
from flask_login import current_user, login_user, login_required, logout_user
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app.forms import EmptyForm
from flask import jsonify
# g variable provided by Flask is a place where the application can store data that needs to persist through the life of a request
from flask import g
from app.forms import SearchForm


@app.before_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@app.route('/')
@app.route('/index')
@login_required
def index():
    podcasts_featured = Podcast.query.filter_by(category_id=1)
    podcasts_daily = Podcast.query.filter_by(category_id=2)
    podcasts_news = Podcast.query.filter_by(category_id=3)
    return render_template('index.html', title='Home',
                           podcasts_featured=podcasts_featured,
                           podcasts_daily=podcasts_daily,
                           podcasts_news=podcasts_news)


@app.route('/podcast/<id>')
@login_required
def podcast_detail(id):
    podcast = Podcast.query.get(id)
    episodes = podcast.get_all_episodes()
    episode_id = []
    for i in range(episodes.__len__()):
        episode_id.append(episodes[i].id)
    form = EmptyForm()
    form_podcast_details = EmptyForm()
    return render_template('podcast.html', title='Podcast', podcast=podcast, episodes=episodes, form=form,
                           form_podcast_details=form_podcast_details,
                           episode_id=episode_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/follow/<id>', methods=['POST'])
@login_required
def follow(id):
    podcast = Podcast.query.filter_by(id=id).first()
    if podcast is None:
        flash('Podcast {} not found.'.format(id))
        return jsonify({'status': 'error'})
    current_user.follow(podcast)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/unfollow/<id>', methods=['POST'])
@login_required
def unfollow(id):
    podcast = Podcast.query.filter_by(id=id).first()
    if podcast is None:
        flash('Podcast {} not found.'.format(id))
        return jsonify({'status': 'error'})
    current_user.unfollow(podcast)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    podcasts = user.get_liked_podcasts()
    listened_episodes = user.get_listened_episodes()

    return render_template('user.html', user=user, podcasts=podcasts, listened_episodes=listened_episodes)


@app.route('/listen', methods=['POST'])
@login_required
# @cross_origin()
def episode_listened():
    user_id = request.form['userId']
    episode_id = request.form['episodeId']
    user = User.query.filter_by(id=user_id).first()
    episode = Episode.query.filter_by(id=episode_id).first()
    user.listen(episode)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/episode/<id>')
@login_required
def episode_detail(id):
    episode = Episode.query.get(id)
    comments = Comment.query.filter_by(episode_id=id).order_by(Comment.timestamp.desc())
    comments_with_users = []
    comment_number = 0
    for c in comments.all():
        comment_number = comment_number + 1
        replies_with_users = []
        user = User.query.get(c.user_id)
        replies = c.reply.all()
        for r in replies:
            comment_number = comment_number + 1
            reply_user = User.query.get(r.user_id)
            o = {'reply': r, 'user': reply_user}
            replies_with_users.append(o)

        comments_with_users.append({'comment': {'original': c, 'replies': replies_with_users}, 'user': user})

    photo_path = app.config['PHOTO_PATH_STATIC']
    return render_template('episode.html', title='Episode', episode=episode,
                           comments=comments, comments_with_users=comments_with_users,
                           current_user=current_user, comment_number=comment_number, photo_path=photo_path)


@app.route('/comments', methods=['POST'])
@login_required
# @cross_origin()
def comments():
    user_id = current_user.id
    episode_id = request.form['episodeId']
    episode_time = request.form['episodeTime']
    message = request.form['message']
    comment = Comment(user_id=user_id, episode_id=episode_id, episode_time=episode_time, message=message)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'status': 'success', 'commentId': comment.id})


@app.route('/reply', methods=['POST'])
@login_required
# @cross_origin()
def reply():
    user_id = current_user.id
    id = request.form['commentId']
    message = request.form['message']
    comment = Comment.query.filter_by(id=id)[0]
    reply = Comment(user_id=user_id, message=message)
    db.session.add(reply)
    comment.reply.append(reply)
    db.session.commit()
    return jsonify({'status': 'success'})


from app.forms import EditProfileForm
from werkzeug.utils import secure_filename
import os


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():

        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.config['PHOTO_PATH'], filename
        ))
        current_user.username = form.username.data
        current_user.photo = f.filename
        db.session.commit()
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/my_feed')
@login_required
def my_feed():
    page = request.args.get('page', 1, type=int)
    podcast_with_episodes = current_user.get_podcast_with_episodes(page)

    if page == 1:
        return render_template('my_feed.html', podcast_with_episodes=podcast_with_episodes)

    l = []
    for x in podcast_with_episodes:
        l.append({'user': x.User.to_dict(),
                  'podcast_id': x.podcast_id,
                  'podcast_title': x.body,
                  'timestamp': x.timestamp,
                  'podcast_id': x.podcast_id,
                  'episode_id': x.id,
                  'episode_title': x.title,
                  'audio_link': x.audio_link,
                  'image': x.image,
                  'description': x.description
                  })
    return jsonify(l)


@app.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    users, total = User.search(g.search_form.q.data, page,
                               app.config['USERS_PER_PAGE'])
    next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
        if total > page * app.config['USERS_PER_PAGE'] else None
    prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', users=users,
                           next_url=next_url, prev_url=prev_url)


@app.route('/follow_user/<user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    current_user.follow_user(user)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/unfollow_user/<user_id>', methods=['POST'])
@login_required
def unfollow_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    current_user.unfollow_user(user)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/retweet', methods=['POST'])
@login_required
def retweet():
    episode_id = request.form['episodeId']
    episode = Episode.query.filter_by(id=episode_id).first()
    current_user.retweet_episode(episode)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/cancel_retweet', methods=['POST'])
@login_required
def cancel_retweet():
    episode_id = request.form['episodeId']
    episode = Episode.query.filter_by(id=episode_id).first()
    current_user.cancel_retweet_episode(episode)
    db.session.commit()
    return jsonify({'status': 'success'})