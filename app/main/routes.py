from datetime import datetime
from flask import render_template,request,redirect,flash,url_for,current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm, MessageForm
from app.models import User, Post ,Message
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Added your post')
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    if posts.has_next:
        next_url = url_for('main.index', page=posts.next_num)
    else:
        next_url = None
    if posts.has_prev:
        prev_url = url_for('main.index', page=posts.prev_num)
    else:
        prev_url = None

    return(render_template('home.html', title='Anecdote-Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    if posts.has_next:
        next_url = url_for('main.explore', page=posts.next_num)
    else:
        next_url = None
    if posts.has_prev:
        prev_url = url_for('main.explore', page=posts.prev_num)
    else:
        prev_url = None
    return render_template('home.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None

    return render_template('user.html', title='Profile', user=user, posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your Changes Has Been Saved')
        return(redirect(url_for('main.edit_profile')))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit_Profile', form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('No user named {}'.format(username))
            return redirect(url_for('main.index'))

        if user == current_user:
            flash('You cannot Follow Yourself')
            return redirect(url_for('main.user', username=username))

        current_user.follow(user)
        db.session.commit()
        flash('You are now following {}'.format(username))
        return redirect(url_for('main.user', username=username))

    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('No user named {} Exists'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow You')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash("you unfollowed {}".format(username))
        return redirect(url_for('main.user', username=username))

    else:
        return redirect(url_for('main.index'))


@bp.route('/send_message/<recipient>',methods=['POST','GET'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user,recipient=user,body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your Message has been sent')
        return redirect(url_for('main.user',username=recipient))
    return render_template('send_message.html',title='Messenger',form=form,recipient=recipient)