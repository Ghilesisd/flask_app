
from flask import Flask, render_template,request,flash
from flask.helpers import url_for
from flask import  Response
from werkzeug.utils import secure_filename


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from sqlalchemy.sql.expression import false
from werkzeug.utils import redirect
  
from config import Config



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
    file_name= db.Column(db.String(100000), unique=False, )

    def __init__(self,titredb,Categoriedb,desc_courtedb,desc_longdb,file_name):
         
                            self.titredb=titredb
                            self.Categoriedb=Categoriedb
                            self.desc_courtedb=desc_courtedb
                            self.desc_longdb=desc_longdb
                            self.file_name=file_name


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


    
class aviss(db.Model):
    __tablename__ ='avis'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20),unique=True)
    Commentaire = db.Column(db.String(500),unique=True)

    def __init__(self,nom,Commentaire):
                self.nom=nom
                self.Commentaire=Commentaire


class feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    telephone = db.Column(db.String(10))
    comments = db.Column(db.Text())

    def __init__(self, nom, email, telephone, comments):
        self.nom = nom
        self.email = email
        self.telephone = telephone
        self.comments = comments



class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


       


@app.route('/admin/', methods=['POST', 'GET'])

def adminpage():
    
    return render_template("admin.html")

@app.route('/' , methods=['POST', 'GET'])
def homepage():

    return render_template("home.html")



    
@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)




    
    


 


@app.route('/details/<formation_titre>', methods=['POST', 'GET'])
def detailspage(formation_titre):
  formations=formation.query.filter_by(titredb=formation_titre).first()
  return render_template("details.html",formations=formations  )
  



@app.route('/ecole')
def ecole():
    return render_template('ecole.html')

@app.route('/paiement')
def paiement():
    return render_template('paiement.html')

@app.route('/certificat')
def certificat():
    return render_template('certificat.html')

@app.route('/formations/', methods=['POST', 'GET'])
def formations():
  if request.method == 'POST' :
       titre=request.form['titre']
       Categorie=request.form['Categorie']
       desc_courte=request.form['desc_courte']
       desc_long=request.form['desc_long']
      # print(titre,Categorie,desc_courte,desc_long)
       pic = request.files['pic']

       filename = secure_filename(pic.filename)
      
       newFormation= formation (titre,Categorie,desc_courte,desc_long,filename)
       
       db.session.add(newFormation)
       
       db.session.commit()
       
  formations=formation.query.all()
        

       
  
  return render_template('formations.html',formations=formations)



@app.route('/register',  methods=['POST', 'GET'])
def register():
  
  form=RegistrationForm()

  if form.validate_on_submit():
    User.create_user(
      user=form.nom.data,
      email=form.email.data,
      password=form.password.data
    )
   
    flash('registration successful')
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


@app.route('/avis', methods=['POST', 'GET'])
def avis():
        if request.method == 'POST':
             nom=request.form['nom']
             Commentaire=request.form['Commentaire']
             newAvis=aviss(nom,Commentaire)
             db.session.add(newAvis)
             db.session.commit()
        lesavis = aviss.query.all()
        return render_template('avis.html',lesavis=lesavis)

@app.route('/cmntr')

def commentaire():

    return render_template('cmntr.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        telephone= request.form['telephone']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if nom == '' or email == '' or telephone=='':
            return render_template('contacte.html', message='Please enter required fields')
        if db.session.query(feedback).filter(feedback.email == email).count() == 0:
          base = feedback(nom, email,telephone, comments)
          db.session.add(base)
          db.session.commit()
          return render_template('reussir.html')
        return render_template('contacte.html', message='existe deja')


@app.route('/contacte', methods=['POST','GET'])

def contacte():

    return render_template("contacte.html")






if __name__ == '__main__':
    db.create_all()
    
   # f1=formation('html','','','')
    #db.session.add(f1)

    #db.session.commit()
  
    app.run(debug = True)




