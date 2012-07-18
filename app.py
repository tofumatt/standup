from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///flask_app.db')
db = SQLAlchemy(app)


class User(db.Model):
    """A standup participant."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    irc_handle = db.Column(db.String(100))
    github_hanlde = db.Column(db.String(100))


class Project(db.Model):
    """A project that does standups."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    irc_channel = db.Column(db.String(100))


class Status(db.Model):
    """A standup update for a user on a given project."""
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    irc_handle = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User', backref=db.backref('statuses', lazy='dynamic'))
    project_id = db.Column(
        db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship(
        'Project', backref=db.backref('statuses', lazy='dynamic'))
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)

# TODO: M2M Users <-> Projects


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/user', methods=['POST'])
# def user():
#     if request.method == 'POST':
#         u = User(request.form['name'], request.form['email'])
#         db.session.add(u)
#         db.session.commit()
#     return redirect(url_for('index'))


if __name__ == '__main__':
    print app.config['SQLALCHEMY_DATABASE_URI']
    db.create_all()
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)