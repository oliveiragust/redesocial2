from flask import Flask, render_template, request, redirect, flash, session, url_for, abort
from models import db, Users, Posts, Follow
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegisterForm, LoginForm, PostForm
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost:3306/redesocial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'sua_chave_secreta'

db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return None

    return Users.query.get(user_id)






@app.route('/', methods=['GET', 'POST'])
def home():


    user = current_user
    allow_post = False
    posts = Posts.query.all()
    user_posts = Posts.query.filter_by(user_id=current_user.id).all()

    if current_user.is_authenticated:
        users = Users.query.all()
        followed_user_ids = [followed.followed_id for followed in current_user.following]


        allow_post = True
        followed_posts = Posts.query.filter(Posts.user_id.in_(followed_user_ids)).all()
        posts = user_posts + followed_posts


        form = PostForm()

        if form.validate_on_submit():
            new_post = Posts(content=form.content.data, created_at=datetime.now(), user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')



        return render_template('index.html', user=user, form=form, posts=posts, allow_post=allow_post, users=users)
    else:
        return render_template('index.html', allow_post=allow_post, posts=posts)



@app.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = Users.query.filter_by(username=username).first()
    users = Users.query.all()
    if not user:
        abort(404)


    allow_post = False
    if current_user.is_authenticated:
        allow_post = True


        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'follow':
                follow_relationship = Follow(follower_id=current_user.id, followed_id=user.id)
                db.session.add(follow_relationship)
                db.session.commit()

            elif action == 'unfollow':
                follow_relationship = Follow.query.filter_by(follower_id=current_user.id, followed_id=user.id).first()
                if follow_relationship:
                    db.session.delete(follow_relationship)
                    db.session.commit()


    follower = user.followers
    following = user.following
    is_following = current_user.is_following(user) if current_user.is_authenticated else False

    return render_template('profile.html', user=user, username=username, allow_post=allow_post,
                           follower=follower, following=following, is_following=is_following, users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = Users(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created.', 'success')
        return redirect('login')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('home')

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user)
            session['username'] = user.username
            return redirect('/')


    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    db.create_all()
    app.run()
