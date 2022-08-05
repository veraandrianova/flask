from datetime import datetime

from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from UserLogin import UserLogin
from forms import LoginForm, RegisterForm, PasswordChange, CreatePosts

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjflj7492ldnv04kd;v7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
menu = [{"name": 'Главная страница', 'url': '/'},
        {"name": 'Регистрация', 'url': 'register'},
        {"name": 'Войти', 'url': 'login'},
        {"name": 'Создать пост', 'url': 'create_posts'}
        ]


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(150), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Posts %r>' % self.title


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('profiles', lazy=True))

    def __repr__(self):
        return '<Profile %r>' % self.phone


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    psw = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name



@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, User)

@app.route('/')
def index():
    posts = Posts.query.all()
    return render_template('index.html', title='О сайте', menu=menu, posts=posts)


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        phone = form.phone.data
        name = form.name.data
        user = User.query.filter_by(name=name).all()
        if len(user) == 0:
            if (len(phone) >= 11 and len(phone) <= 12) and (phone[0] == '+' or phone.isdecimal()):
                hash = generate_password_hash(form.psw.data)
                print(hash)
                if check_password_hash(hash, form.psw_2.data):
                    try:
                        hash = generate_password_hash(form.psw.data)
                        u = User(name=form.name.data, psw=hash)
                        db.session.add(u)
                        db.session.flush()
                        p = Profile(phone=form.phone.data, user_id=u.id)
                        db.session.add(p)
                        db.session.commit()
                        flash('Регистрация успешна')
                        return redirect(url_for('login'))
                    except:
                        db.session.rollback()
                        print('Ошибка добавления')
                        flash('Ошибка отправки')
                flash('Пароли не совпадают')
                return render_template('contact.html', title='Регистрация', menu=menu, form=form)
            else:
                flash('Номер должен быть вида 89997776655 или +79998887766')
                return render_template('contact.html', title='Регистрация', menu=menu, form=form)
        flash('Пользователь с таким именем существует')
        return redirect(url_for('login'))
    else:
        flash('Заполните корректно форму')
    return render_template('contact.html', title='Регистрация', menu=menu, form=form)


@app.route('/profile/<name>')
@login_required
def profile(name):
    return render_template('profile.html', title='Профиль', menu=menu, name=name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(name=name).all()
        if len(user) > 0:
            id = user[0].id
            cur_user = user[0]
            if cur_user.name == name:
                if check_password_hash(cur_user.psw, form.psw.data):
                    userlogin = UserLogin().create(id)
                    print(userlogin)
                    login_user(userlogin)
                    return redirect(url_for('profile', name=name))
        else:
            flash('Неверная пара логин/пароль')
    return render_template('login.html', menu=menu, title='Авторизация', form=form)


@app.route('/password_change', methods=['POST', 'GET'])
def password_change():
    form = PasswordChange()
    if form.validate_on_submit():
        phone = form.phone.data
        cur_phone = Profile.query.filter_by(phone=phone).all()
        if len(cur_phone) > 0:
            id_user = cur_phone[0].user_id
            hash = generate_password_hash(form.psw.data)
            if check_password_hash(hash, form.psw_2.data):
                u = User.query.get(id_user)
                u.psw = hash
                db.session.commit()
                return redirect(url_for('login'))
            flash('Пароли не совпадают')
        flash('Проверьте правильность номера телефона')
    return render_template('password_change.html', menu=menu, title='Смена пароля', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/create_posts', methods=['POST', 'GET'])
@login_required
def create_posts():
    form = CreatePosts()
    id = current_user.get_id().id
    if form.validate_on_submit():
        title = form.title.data
        url = title.replace(' ', '_')
        print(url)
        cur_title = Posts.query.filter_by(title=title).first()
        if not cur_title:
            try:
                p = Posts(title=title, body=form.body.data, url=url, user_id=id)
                print(p)
                print(p.title)
                print(p.body)
                print(p.user_id)
                db.session.add(p)
                db.session.commit()
                flash('Регистрация успешна')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                print('Ошибка добавления')
                flash('Ошибка отправки')
        flash('Пост с таким названием существует, выберите другое название')
    return render_template('create_posts.html', menu=menu, title='Создать пост', form=form)

@app.route('/post/<url>')
@login_required
def post_detail(url):
    post = Posts.query.filter_by(url=url).first()
    return render_template('post_detail.html', menu=menu, title='Пост', post=post)

@app.errorhandler(404)
def pageNot(error):
    return ("Страница не найдена", 404)

@app.route('/transfer')
def transfer():
    return redirect(url_for('index'), 301)

if __name__ == '__main__':
    app.run(debug=True)
