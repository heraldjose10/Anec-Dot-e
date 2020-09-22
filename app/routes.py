from app import app
from app.forms import LoginForm
from flask import render_template,url_for,redirect,flash

@app.route('/')
@app.route('/index')
def index():
    posts=[
        {
            'author':{'username':'heraldjos'},
            'title':'Im Up',
            'link':'https://www.fullstackpython.com/flask-blueprints-blueprint-examples.html'
        },
        {
            'author':{'username':'iamgodking'},
            'title':'How to win top lane',
            'link':'http://charlesleifer.com/blog/saturday-morning-hack-a-little-note-taking-app-with-flask/'
        }
            ]
    return(render_template('home.html',title='Anecdote-Home',posts=posts))

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash('Loggin in User {},remember me:{}'.format(form.username.data,form.remember_me.data))
        return(redirect('/index'))
    return(render_template('loginpage.html',title='Sign-In',form=form))


# @app.route('/login/<username>')
# def logged_in(username):
#     posts=[
#         {
#             'author':{'username':'heraldjose'},
#             'title':'I fucked Up',
#             'link':'https://www.fullstackpython.com/flask-blueprints-blueprint-examples.html'
#         },
#         {
#             'author':{'username':'iamgodking'},
#             'title':'How to win top lane',
#             'link':'http://charlesleifer.com/blog/saturday-morning-hack-a-little-note-taking-app-with-flask/'
#         }
#             ]
#     user={'username':username}
#     return(render_template('loggedin.html',user=user,title='Anecdote',posts=posts))

