from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

from logic import get_list_of_films, html_construcktor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/skip/PycharmProjects/film_chooser/films2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    movies = db.relationship('Movie', backref='user')

    def __repr__(self):
        return f'<User "{self.username}">'


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Movie "{self.title[:20]}...">'


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/my_shining_app', methods=['POST', 'GET'])
def handling():
    if request.method == 'POST':

        unames = request.form.getlist('username')

        films_intersec = set()

        for username in unames:

            if not User.query.filter_by(username=username).first():

                chel = User(username=username)
                db.session.add(chel)

                films = get_list_of_films(username)

                for i in films:
                    db.session.add(Movie(title=i, user=chel))

                db.session.commit()

            for i in User.query.filter_by(username=username).first().movies:
                films_intersec.add(i.title)

        f = random.choices(list(films_intersec), k=len(unames) + 1)

        return render_template('films.html', f=f)

    return render_template('app_form.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
