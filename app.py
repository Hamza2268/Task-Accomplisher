# from click import style
from flask import Flask, redirect, render_template, url_for, request, session
from flask_wtf import FlaskForm
from sqlalchemy import Null
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
import uuid
from flask_bcrypt import Bcrypt
from flask_wtf.file import FileAllowed


app = Flask(__name__)
bcrypt = Bcrypt(app)

### File Upload Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'static/profile_pics' 
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  


if __name__ == '__main__':
    app.run(debug=True)

### DB Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


##### Registeration Form
class RegisterForm(FlaskForm):
    UserName = StringField('UserName', validators=[DataRequired(), Length(min=3, max=20)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    photo = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8)])
    Address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    Phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    Submit = SubmitField('Register')

##### Login Form
class LoginForm(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Length(min=3, max=20)])
    Password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    Submit = SubmitField('Login')

##################################### Models #########################################
### DB Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    photo = db.Column(db.String(20), nullable=True, default='default.jpg')
    Address = db.Column(db.String(100), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

##################################### Routes #########################################

## current user id
id = Null 

@app.route('/')
def homepage():
    global id
    id = Null
    return render_template('homepage.html')

@app.route('/app/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        photo_file = form.photo.data
        if photo_file:
            # give it a safe + unique name
            filename = secure_filename(photo_file.filename)
            unique_filename = str(uuid.uuid4()) + "_" + filename
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            photo_file.save(photo_path)
        else:
            unique_filename = "default.jpg"
        if form.Password.data != form.confirm_password.data:
            form.Password.errors.append("Passwords do not match")
            return render_template('register.html', form=form, title='Registeration Form', style='register_signin.css')
        # User.query.filter_by(email=form.Email.data).count()
        if User.query.filter_by(email=form.Email.data).count() > 0:
            form.Email.errors.append("Email already registered")
            return render_template('register.html', form=form, title='Registeration Form', style='register_signin.css')
        gender = 'M' if form.gender.data == "male" else 'F'
        hashed_password = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user = User(username=form.UserName.data,
                     email=form.Email.data,
                      password= hashed_password,
                      Address=form.Address.data, 
                      Phone=form.Phone.data,
                      gender = gender,
                      photo = unique_filename)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('Registered_successfully'))
    return render_template('register.html', form=form, title='Registeration Form', style='register_signin.css', script='script.js')

@app.route('/app/successful-process')
def Registered_successfully():
    return render_template('successful.html', title='Registered Successfully', style='register_signin.css')

@app.route('/app/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.Email.data, password=form.Password.data).first()
        user = User.query.filter_by(email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.Password.data):
            # global id
            # id = user.id
            session['user_id'] = user.id
            return redirect(url_for('Home'))
        else:
            form.Email.errors.append("Invalid username or password")
    return render_template("login.html", form=form, title='Login', style='register_signin.css', script='script.js')

@app.route('/user/home')
def Home():
    # global id
    # if id == Null:
    #     return redirect(url_for('login'))
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('home.html', user=user, title='Home', style='register_signin.css', script='script.js')

@app.route('/user/personal-info')
def personal_info():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('personal_info.html', user=user, title='Personal Info', style='register_signin.css', script='script.js')

@app.route('/app/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('homepage'))
