import secrets
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# configuration
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialization
db = SQLAlchemy(app)
migrate = Migrate(app, db)

ROWS_PER_PAGE = 5

# OUR MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.name)


# OUR FORMS
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email("Please enter valid email address!")])    
    submit = SubmitField('Submit')


# OUR ROUTES
@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Successfully Submited!")
    return render_template('name.html', title='NameApp', name=name, form=form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user_data = User(name=form.name.data, email=form.email.data)
            db.session.add(user_data)
            db.session.commit()
            name = form.name.data
            form.name.data = ''
            form.email.data = ''
            flash("User successfully added!")
            return redirect(url_for('user_list'))
        else:
            flash("User already exist!")
    
    return render_template('adduser.html', title='Add User', form=form)


@app.route('/userlist')
def user_list():

    # users = User.query.order_by(User.date_created)
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.date_created).paginate(page=page, per_page=ROWS_PER_PAGE)

    next_url = url_for('user_list', page=users.next_num) if users.has_next else None
    prev_url = url_for('user_list', page=users.prev_num) if users.has_prev else None

        
    return render_template('userlist.html', title='User List', users=users, next_url=next_url, prev_url=prev_url)