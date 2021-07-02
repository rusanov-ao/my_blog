from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy  # библиотека для базы данных
from datetime import datetime  # библиотека для времени

app = Flask(__name__)  # указываем что данный файл для flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # подключаем библиотеку sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):  # создаем колонки для базы данных
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # функция для вывода объекта вместе с его id
        return '<Article %r>' % self.id


@app.route('/')  # создаем ссылки главной страницы
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')  # ссылка для страницы О нас
def about():
    return render_template("about.html")


@app.route('/posts')  # ссылка на все посты
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')  # ссылка на отдельный пост
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])  # добавление в базу данных
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:  # если возникла ошибка
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')  # переадресация на страницу posts
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


if __name__ == "__main__":  # говорим что это главный, начальный файл для запуска приложения
    app.run(debug=True)  # включили просмотр всех ошибок
