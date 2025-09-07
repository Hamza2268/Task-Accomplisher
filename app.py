######################################################### Used modules #############################################################
from flask import Flask, redirect, render_template, url_for,request ,session
from flask_wtf import FlaskForm
from sqlalchemy import Null, nullsfirst
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
import uuid
from flask_bcrypt import Bcrypt
from flask_wtf.file import FileAllowed
from datetime import datetime, timezone, timedelta
 
####################################################### App Initialization #####################################################
app = Flask(__name__)
bcrypt = Bcrypt(app)

### File Upload Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'static/profile_pics' 
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  


if __name__ == '__main__':
    app.run(debug=True)

####################################################### DB Configuration #####################################################
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

######################################################### Forms #############################################################
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

##### Personal-Info Form
class PersonalInfoForm(FlaskForm):
    UserName = StringField('UserName', validators=[DataRequired(), Length(min=3, max=20)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    photo = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    Address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    Phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    Submit = SubmitField('Update Info')

##### Change Password Form
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=8)])
    Submit = SubmitField('Change Password')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = StringField('Description', validators=[Length(max=200)])
    Deadline = SelectField('Deadline (in days)',
                                choices =  [( '','Choose your appropiate time'), ('1', '1'), ('2', '2'), ('5', '5'), ('10', '10'),
                                    ('15', '15'), ('20', '20'), ('30', '30')],
                            validators=[DataRequired()],
                            default=''
                            )
    priority = RadioField('Priority',
                           choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'),('Critical', 'Critical')],
                             default='Medium',
                               validators=[DataRequired()])
    Submit = SubmitField('Add Task')

######################################################### Models #############################################################
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
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    StartDate = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    EndDate = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) #I will use Deadline instead
    CompletedDate = db.Column(db.DateTime(timezone=True), nullable=True)  # for both boolean and date when the task was actually completed
    Deadline = db.Column(db.Integer, nullable=False)    # Deadline in days
    # Completion = db.Column(db.Boolean, default=False, nullable=False)
    priority = db.Column(db.String(10), nullable=False, default='Medium')

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}')"


######################################################### Routes #############################################################
### HomePage for the Web info
@app.route('/')
def homepage():
    global id
    id = Null
    return render_template('homepage.html')

### Registeration route
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

###################################################### app Path ########################################################
### Successful Registeration msg
@app.route('/app/successful-process')
def Registered_successfully():
    return render_template('successful.html', title='Registered Successfully', style='register_signin.css')

### Log In route
@app.route('/app/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.Password.data):
            session['user_id'] = user.id
            return redirect(url_for('Home'))
        else:
            form.Email.errors.append("Invalid username or password")
    return render_template("login.html", form=form, title='Login', style='register_signin.css', script='script.js')

###################################################### User Path ########################################################
#User Home route
@app.route('/user/home')
def Home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('home.html', user=user, title='Home', style='register_signin.css', script='script.js')

### Tasks made by User
@app.route('/user/task')
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    tasks = Task.query.filter_by(user_id=session['user_id']).order_by(nullsfirst(Task.CompletedDate)).all()
    acheived = Task.query.filter_by(user_id=session['user_id']).filter(Task.CompletedDate.isnot(None)).count()
    total = Task.query.filter_by(user_id=session['user_id']).count()
    return render_template('viewTasks.html', user=user, acheived=acheived, total=total,  tasks=tasks, title='Tasks', style='register_signin.css', script='script.js')

### User Personal Info
@app.route('/user/personal-info')
def personal_info():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('personal_info.html', user=user, title='Personal Info', style='register_signin.css', script='script.js')

### Edit Personal Info route
@app.route('/user/personal-info/edit', methods=['GET','POST'])
def Edit_Info():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    form = PersonalInfoForm()
    if request.method == 'GET':
        form.UserName.data = user.username
        form.Email.data = user.email
        form.Address.data = user.Address
        form.Phone.data = user.Phone
    
    if form.validate_on_submit():
        if User.query.filter_by(email=form.Email.data).count() > 0 and user.email != form.Email.data:
            form.Email.errors.append("Email already registered")
            return render_template('editInfo.html', form=form, title='Edit Info', style='register_signin.css', script='script.js')
        
        photo_file = request.files.get('photo')   
        if photo_file and photo_file.filename != "":
            filename = secure_filename(photo_file.filename)
            unique_filename = str(uuid.uuid4()) + "_" + filename
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            photo_file.save(photo_path)
            user.photo = unique_filename  
        user.username = form.UserName.data
        user.email = form.Email.data  
        user.Address = form.Address.data
        user.Phone = form.Phone.data
        db.session.commit()
        return redirect(url_for('personal_info'))

    return render_template('editInfo.html', form=form, title='Edit Info', style='register_signin.css', script='script.js')

### Change User Password route
@app.route('/user/personal-info/edit/password', methods=['GET','POST'])
def changePassword():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if(form.new_password.data != form.confirm_new_password.data):
            form.new_password.errors.append("Passwords do not match")
            return render_template('editInfo.html', form=form, title='change password', style='register_signin.css', script='script.js')
        user = User.query.get(session['user_id'])
        if user and bcrypt.check_password_hash(user.password, form.current_password.data):
           hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
           user.password= hashed_password
           db.session.commit()
           return render_template('successful.html',msg='Password Changed successfully', title='Registered Successfully', style='register_signin.css')
    return render_template('editInfo.html', form=form, title='change password', style='register_signin.css', script='script.js')

###################################################### Task Path ########################################################
### Add New Task Route
@app.route('/user/task/add', methods=['GET', 'POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    description=form.description.data,
                    user_id=session['user_id'],
                    Deadline=int(form.Deadline.data),
                    EndDate=datetime.now(timezone.utc) + timedelta(days=int(form.Deadline.data)),
                    priority=form.priority.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('Home'))
    return render_template('add_edit_Task.html',user= user, form=form, title='Add New Task', style='register_signin.css', script='script.js')

### Edit Task content
@app.route('/user/task/edit/<int:task_id>', methods=['GET','POST'])
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        return "You are not authorized to complete this task.", 403
    form = TaskForm()
    user = User.query.get(session['user_id'])
    if request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.Deadline.data = str(task.Deadline)
        form.priority.data = task.priority

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.Deadline = int(form.Deadline.data)
        task.priority = form.priority.data
        task.EndDate = datetime.now(timezone.utc) + timedelta(days=int(form.Deadline.data))
        
        db.session.commit()
        return redirect(url_for('view_tasks'))
    return render_template('add_edit_Task.html', user=user, task=task, form=form, title='Edit Task', style='register_signin.css', script='script.js')

### Deletion of Tasks route
@app.route('/user/task/delete/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        return "You are not authorized to delete this task.", 403
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_tasks'))

### Mark Task as Completed route
@app.route('/user/task/done/<int:task_id>', methods=['GET', 'POST'])
def complete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    task = Task.query.get_or_404(task_id)
    if task.user_id != session['user_id']:
        return "You are not authorized to complete this task.", 403
    task.CompletedDate = datetime.now(timezone.utc)
    db.session.commit()
    return redirect(url_for('view_tasks'))

### Logout Route
@app.route('/app/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('homepage'))

### 404 Error Route
@app.errorhandler(404)
def page_not_found(e):
    return render_template('notFoundError.html', title='404 Error', style='register_signin.css', script='script.js'), 404

########################################################## The End ###############################################################