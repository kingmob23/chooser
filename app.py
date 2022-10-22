from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

from logic import get_list_of_films, html_construcktor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/skip/1/me_vs_code/web-projects/film_chooser/watchlists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

    def __repr__(self):
        return f'<Users "{self.username}">'


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)

    def __repr__(self):
        return f'<Movies "{self.title[:20]}...">'


class Linking(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movies.id'), primary_key=True)

    def __repr__(self):
        return f'<Linking "{self.user_id}">'


def add_user(username):
    db.session.add(Users(username=username))
    chel_id = Users.query.filter_by(username=username).first().id

    films = set(get_list_of_films(username))
    for i in films:
        if not Movies.query.filter_by(title=i).first():
            db.session.add(Movies(title=i))
        kinchik_id = Movies.query.filter_by(title=i).first().id
        db.session.add(Linking(user_id=chel_id, movie_id=kinchik_id))

    db.session.commit()


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/my_shining_app', methods=['POST', 'GET'])
def handling():
    if request.method == 'GET':
        return render_template('app-form.html')

    usernames = {}
    for i in range(len(request.form)):
        if len(request.form.getlist('update-db' + str(i))) != 0:
            usernames[request.form.getlist('username' + str(i))[0]] = True
        elif len(request.form.getlist('username' + str(i))) != 0:
            usernames[request.form.getlist('username' + str(i))[0]] = False


    films_intersec = []
    films_with_weight = {}
    for username in usernames:
        if Users.query.filter_by(username=username).first():
            uid = Users.query.filter_by(username=username).first().id

        if usernames[username]:
            for i in Linking.query.filter_by(user_id=uid).all():
                db.session.delete(i)
            db.session.commit()

        if not Users.query.filter_by(username=username).first() or not Linking.query.filter_by(user_id=uid).first():
            try:
                add_user(username)
            except ValueError:
                return render_template('no-such-user.html')

        titles_of_user_films = []
        for i in Linking.query.filter_by(user_id=uid).all():
            titles_of_user_films.append(
                Movies.query.filter_by(id=i.movie_id).first().title)

        for i in titles_of_user_films:
            if i not in films_with_weight:
                films_with_weight[i] = 0
            films_with_weight[i] += 1

    for i in films_with_weight:
        if films_with_weight[i] == len(usernames):
            films_intersec.append(i)

    random.shuffle(films_intersec)
    f = films_intersec[:len(usernames) + 1]

    return render_template('films.html', f=f)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
