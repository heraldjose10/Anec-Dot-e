from app import app
from app import db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():

    posts = [
        {
            'author': {'username': 'heraldjos'},
            'title': 'Im Up',
            'link': 'https://www.fullstackpython.com/flask-blueprints-blueprint-examples.html'
        },
        {
            'author': {'username': 'iamgodking'},
            'title': 'How to win top lane',
            'link': 'http://charlesleifer.com/blog/saturday-morning-hack-a-little-note-taking-app-with-flask/'
        }
    ]

    return(render_template('home.html', title='Anecdote-Home', posts=posts))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(password=form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('loginpage.html', title='Sign In', form=form)


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

        flash('Congratulations.. You are Registered..!!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            'author': user,
            'title': 'Im Up',
            'link': 'https://www.fullstackpython.com/flask-blueprints-blueprint-examples.html'
        },
        {
            'author': user,
            'title': 'How to win top lane',
            'link': 'http://charlesleifer.com/blog/saturday-morning-hack-a-little-note-taking-app-with-flask/'
        }
    ]
    return render_template('user.html', title='Profile', user=user, posts=posts,form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your Changes Has Been Saved')
        return(redirect(url_for('edit_profile')))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit_Profile', form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('No user named {}'.format(username))
            return redirect(url_for('index'))

        if user == current_user:
            flash('You cannot Follow Yourself')
            return redirect(url_for('user', username=username))

        current_user.follow(user)
        db.session.commit()
        flash('You are now following {}'.format(username))
        return redirect(url_for('user', username=username))

    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('No user named {} Exists'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow You')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash("you unfollowed {}".format(username))
        return redirect(url_for('user', username=username))

    else:
        return redirect(url_for('index'))
