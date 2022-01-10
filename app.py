
from flask import Flask, render_template,request,flash
from flask.helpers import url_for


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from sqlalchemy.sql.expression import false
from werkzeug.utils import redirect
  
from config import Config
from forms import RegistrationForm


from flask_login import LoginManager, login_manager
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import UserMixin ,login_user,login_required,logout_user


from flask_wtf import FlaskForm
from wtforms import StringField ,SubmitField, fields
from wtforms.fields.simple import BooleanField, PasswordField

from wtforms.validators import DataRequired,Email,length,EqualTo,ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/formation"
app.config.from_object(Config)
login_manager=LoginManager()
bcrypt=Bcrypt()

login_manager.init_app(app)
bcrypt.init_app(app)
login_manager.login_view='login'
login_manager.session_protection='strong'

db = SQLAlchemy(app)

class formation(db.Model):
    __tablename__ ='formation'
    id = db.Column(db.Integer, primary_key=True, )
    titredb = db.Column(db.String(80), unique=False, )
    Categoriedb = db.Column(db.String(120), unique=False, )
    desc_courtedb = db.Column(db.String(500), unique=False, )
    desc_longdb = db.Column(db.String(100000), unique=False, )

    def __init__(self,titredb,Categoriedb,desc_courtedb,desc_longdb):
         
                            self.titredb=titredb
                            self.Categoriedb=Categoriedb
                            self.desc_courtedb=desc_courtedb
                            self.desc_longdb=desc_longdb


class User(UserMixin, db.Model):
    __tablename__ ='users'

    id = db.Column(db.Integer, primary_key=True, )

    user_name = db.Column(db.String(20) )

    user_email = db.Column(db.String(60), unique=True, index=True)

    user_password=db.Column(db.String(200))

    registration_date= db.Column(db.DateTime, default=datetime.now)

    def check_password(self,password)-> bool:
      return bcrypt.check_password_hash(self.user_password ,password)
    
    @classmethod
    def create_user(cls,user,email,password):
        user=cls(
            
             user_name=user,
             user_email=email,
             user_password=bcrypt.generate_password_hash(password).decode('utf-8')
        )


        db.session.add(user)
        db.session.commit()
        return user
@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id) )                 

def email_existe(form,field):
    email=User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError('email already exists')

class RegistrationForm(FlaskForm):
    nom=StringField('nom', validators=[DataRequired(),length(3,15,message='between 3 to 15 characters')])
   
    email=StringField('email', validators=[DataRequired(),Email(), email_existe])
   
    password=PasswordField('password',validators=[DataRequired(),length(5),EqualTo('confirm', message='password must match')])

    confirm=PasswordField('confirm',validators=[DataRequired()])

    submit= SubmitField('register')

class loginForm(FlaskForm):
  email=StringField('Email',validators=[DataRequired(),Email()])
  password=PasswordField('Password',validators=[DataRequired()])
  stay_loggedin=BooleanField('stay logged-in')
  submit=SubmitField('Login')


    







       


@app.route('/admin/', methods=['POST', 'GET'])

def adminpage():
    
  
    return render_template("admin.html")

@app.route('/' , methods=['POST', 'GET'])

def homepage():

    if request.method == 'POST':
       titre=request.form['titre']
       Categorie=request.form['Categorie']
       desc_courte=request.form['desc_courte']
       desc_long=request.form['desc_long']
       newFormation=formation(titre,Categorie,desc_courte,desc_long)
       db.session.add(newFormation)   
       db.session.commit()
    formations=formation.query.all()
    



    return render_template("base.html",formations=formations)
    
    


 


@app.route('/details/<formation_titre>', methods=['POST', 'GET'])
def detailspage(formation_titre):
  formations=formation.query.filter_by(titredb=formation_titre).first()
  return render_template("details.html",formations=formations  )
  

@app.route('/apropos')
def Apropos():
    return render_template('aproposde.html')


@app.route('/register',  methods=['POST', 'GET'])
def register():
  
  form=RegistrationForm()

  if form.validate_on_submit():
    User.create_user(
      user=form.nom.data,
      email=form.email.data,
      password=form.password.data
    )
   
   # flash('registration successful')
    return redirect(url_for('login'))
  return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
  form=loginForm()
  if form.validate_on_submit():
    user= User.query.filter_by(user_email=form.email.data).first()
    if not user or not user.check_password(form.password.data) :
      flash ('invalide credentials please try again')
      return redirect(url_for('login'))
    login_user(user,form.stay_loggedin.data)
    return render_template('succes.html',form=form)
  return render_template ('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('homepage'))



if __name__ == '__main__':
    db.create_all()
    if not User.query.filter_by(user_name='katia').first():
      User.create_user(
        user='katia',
        email='tst@gmail.com',
        password='secret'
      )
   # f1=formation('html','','','')
    #db.session.add(f1)
    #db.session.commit()
  
    app.run(debug = True)




