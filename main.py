from datetime import datetime
import sqlite3
from UserLogin import UserLogin
from flask_login import LoginManager, login_user
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fjflj7492ldnv04kd;v7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# login_manager = LoginManager(app)
menu = [{"name": 'Главная страница', 'url': '/'}, {"name": 'Регистрация', 'url': 'register'}]


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('profiles', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    psw = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name
# @login_manager.user_loader
# def load_user(user_id):
#     print('load_user')
#     return UserLogin().fromDB(user_id, db)

@app.route('/')
def index():
    return render_template('index.html', title='О сайте', menu=menu)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        print(request.form)
        if len(request.form['name']) > 2:
            try:
                hash = generate_password_hash(request.form['psw'])
                u = User(name=request.form['name'], psw=hash)
                name = request.form['name']
                db.session.add(u)
                db.session.flush()
                p = Profile(phone=request.form['phone'], user_id=u.id)
                db.session.add(p)
                db.session.commit()
                flash('Регистрация успешна')
                return redirect(url_for('profile', name=name))
            except:
                db.session.rollback()
                print('Ошибка добавления')
                flash('Ошибка отправки')
        else:
            flash('Ошибка отправки')
    return render_template('contact.html', title='Регистрация', menu=menu)


@app.route('/profile/<name>')
def profile(name):
    return render_template('profile.html', title='Профиль', menu=menu, name=name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = db.User.query.get(name=request.form['name'])
        print(user)
        # if user and check_password_hash(user['psw'], request.form['psw']):
#             userlogin = UserLogin().create(user)
#             login_user(userlogin)
#             return redirect(url_for('/'))
#         flash('Неверная пара логин/пароль')
#     return render_template('login.html', menu=menu, title='Авторизация')

if __name__ == '__main__':
    app.run(debug=True)
