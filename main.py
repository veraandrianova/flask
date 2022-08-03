from flask import Flask, render_template, request
app = Flask(__name__)
menu =[{"name": 'Главная страница', 'url': '/'}, {"name": 'Логин', 'url': 'contact'}]
@app.route('/')
def index():
    return render_template('index.html', title='О сайте', menu=menu)

@app.route('/contact',methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        print(request.form)
    return render_template('contact.html', title='Профиль', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
