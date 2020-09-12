from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.models import Podcast, User
from flask_login import current_user, login_user, login_required, logout_user
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app.forms import EmptyForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    # podcasts = [
    #     {
    #         'author': {'username': 'John'},
    #         'podcast': 'generation do it yourself'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'podcast': 'how I built this'
    #     }
    # ]
    podcasts = Podcast.query.all();
    form = EmptyForm()
    form_podcast_details = EmptyForm()
    return render_template('index.html', title='Home', podcasts=podcasts, form=form, form_podcast_details=form_podcast_details)


@app.route('/podcast/<id>')
@login_required
def podcast_detail(id):
    podcast = Podcast.query.get(id)
    episodes = podcast.get_all_episodes()
    return render_template('podcast.html', title='Podcast', podcast=podcast, episodes=episodes)


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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/follow/<id>', methods=['POST'])
@login_required
def follow(id):
    form = EmptyForm()
    if form.validate_on_submit():
        podcast = Podcast.query.filter_by(id=id).first()
        if podcast is None:
            flash('Podcast {} not found.'.format(id))
            return redirect(url_for('index'))
        current_user.follow(podcast)
        db.session.commit()
        flash('You are following {}!'.format(id))
        return redirect(url_for('index'))

@app.route('/unfollow/<id>', methods=['POST'])
@login_required
def unfollow(id):
    form = EmptyForm()
    if form.validate_on_submit():
        podcast = Podcast.query.filter_by(id=id).first()
        if podcast is None:
            flash('Podcast {} not found.'.format(id))
            return redirect(url_for('index'))
        current_user.unfollow(podcast)
        db.session.commit()
        flash('You are unfollowing {}!'.format(id))
        return redirect(url_for('index'))
