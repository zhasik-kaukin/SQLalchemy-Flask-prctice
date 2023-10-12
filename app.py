from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page:" + name + "-" + str(id)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post = Article(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Error while adding new post'


    else:
        return render_template('create.html')

@app.route('/posts')
def posts():
    posts = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', posts=posts)

@app.route('/posts/<int:id>')
def posts_detail(id):
    post = Article.query.get(id)
    return render_template("post_detail.html", post=post)

@app.route('/posts/<int:id>/del')
def delete(id):
    post = Article.query.get_or_404(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error while deleting post"

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    post = Article.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.text = request.form['text']


        try:
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Error while updating new post'


    else:
        posts = Article.query.get(id)
        return render_template('post_update.html', posts=posts)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Article %r>" % self.id



if __name__ == "__main__":
    app.run(debug=True)