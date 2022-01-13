
from flask import Flask, render_template,request,flash
from flask.helpers import url_for

from flask_wtf import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from sqlalchemy.sql.expression import false, null
from werkzeug.utils import redirect
  
from config import Config




app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/formation"


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:post@localhost/formation"

app.config.from_object(Config)



db = SQLAlchemy(app)




       


@app.route('/' , methods=['POST', 'GET'])
def homepage():

    return render_template("home.html")
@app.route('/admin/', methods=['POST', 'GET'])

def adminpage():
    
    return render_template("admin.html")


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


@app.route('/formations/', methods=['POST', 'GET'])
def formations():
  
  if request.method == 'POST' and request.form['flag'] != "1" :
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
  if request.method == 'POST' and request.form['flag']=="1":

       Categoriefilter= request.form['Categoriefilter']
       print(Categoriefilter)
       formations = formation.query.filter_by(Categoriedb=Categoriefilter)
        

       
  
  return render_template('formations.html',formations=formations)



  #details
@app.route('/details/<formation_titre>', methods=['POST', 'GET'])

def detailspage(formation_titre):
  formations=formation.query.filter_by(titredb=formation_titre).first()
  return render_template("details.html",formations=formations  )
#fin details
   
#log
  

from flask_wtf import FlaskForm
from wtforms import StringField ,SubmitField, fields
from wtforms.fields.simple import BooleanField, PasswordField
from wtforms.validators import DataRequired,Email,length,EqualTo,ValidationError

from flask_login import LoginManager, login_manager
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import UserMixin ,login_user,login_required,logout_user,current_user


login_manager=LoginManager()
bcrypt=Bcrypt()


login_manager.init_app(app)
bcrypt.init_app(app)
login_manager.login_view='login'
login_manager.session_protection='strong'



#logggin



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




       


@app.route('/admin/', methods=['POST', 'GET'])

def adminpage():
    
  
    return render_template("admin.html")

@app.route('/' , methods=['POST', 'GET'])

def homepage():

   



    return render_template("home.html")
    
    


 


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
  if request.method == 'POST' and request.form['flag'] != "1":
       titre=request.form['titre']
       Categorie=request.form['Categorie']
       desc_courte=request.form['desc_courte']
       desc_long=request.form['desc_long']
      # print(titre,Categorie,desc_courte,desc_long)
      
       

  
       newFormation= formation (titre,Categorie,desc_courte,desc_long)
       db.session.add(newFormation)   
       db.session.commit()
  formations=formation.query.all()

  if request.method == 'POST' and request.form['flag']=="1":

       Categoriefilter= request.form['Categoriefilter']
       print(Categoriefilter)
       formations = formation.query.filter_by(Categoriedb=Categoriefilter)
    
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
   
    flash('votre compte a été cree avec succès')
    return redirect(url_for('login'))
  return render_template('register.html',form=form)

class loginForm(FlaskForm):
  email=StringField('Email',validators=[DataRequired(),Email()])
  password=PasswordField('Password',validators=[DataRequired()])
  stay_loggedin=BooleanField('stay logged-in')
  submit=SubmitField('Login')


@app.route('/login',methods=['GET','POST'])
def login():
  form=loginForm()
  if form.validate_on_submit():
    user= User.query.filter_by(user_email=form.email.data).first()
    if not user or not user.check_password(form.password.data) :
      flash ('invalide identifiants veuillez réessayer')
      return redirect(url_for('login'))
    login_user(user,form.stay_loggedin.data)
    return render_template('home.html',form=form)
  return render_template ('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('homepage'))




#fin login 


#inscription a une formation 

class inscription(db.Model):
    __tablename__ ='inscription'
    id = db.Column(db.Integer, primary_key=True, )
    user_name = db.Column(db.String(80), unique=False, )
    email = db.Column(db.String(120), unique=False, )
    formation= db.Column(db.String(100000), unique=False, )

    def __init__(self,user_name,email,formation):
         
                            self.user_name=user_name
                            self.email=email
                            self.formation=formation

@app.route('/inscrire/<formation_titre>', methods=['POST', 'GET'])
def inscrire(formation_titre):
  
 
  if current_user.is_authenticated:
            formations=formation.query.filter_by(titredb=formation_titre).first()
            titre=formations.titredb
            user=current_user.user_name.title()

            email=current_user.user_email.title()
          
          
            if db.session.query(inscription).filter(inscription.email == email,inscription.formation==titre).count()!= 0:
                flash ('vous etes deja inscrit a cette formation')
                return render_template('details.html',formations=formations)
            else:

                newInsc=inscription(user,email,titre)
                db.session.add(newInsc)
                    
                db.session.commit()
                flash('votre inscription a été acceptée avec succès')
                return render_template("details.html",formations=formations  )
                
  else:
    form=loginForm()

    return render_template('login.html',form=form)

  
    
#FIN Inscription
       

#Evenement


@app.route('/evenements')

def evenements():
  
  return render_template('evenements.html')


@app.route('/evenements_details')

def evenements_details():
  
  return render_template('evenements_details.html')

#Fin evenement




#AVIS
## la partie avis 
class avis(db.Model):
    __tablename__ ='avis'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20),unique=False)
    Commentaire = db.Column(db.String(500),unique=False)

    def __init__(self,nom,Commentaire):
                self.nom=nom
                self.Commentaire=Commentaire


@app.route('/avis', methods=['POST', 'GET'])
def lesavis():
        if request.method == 'POST': 
             nom=request.form['nom']
             Commentaire=request.form['Commentaire']
             newAvis=avis(nom,Commentaire)
             db.session.add(newAvis)
             db.session.commit()
        lesavis = avis.query.all()
        return render_template('avis.html',lesavis=lesavis)

@app.route('/cmntr')

def commentaire():

    return render_template('cmntr.html')


#FIN AVIS


#CONTACT
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




#FIN CONTACTE


                          

                            


#Apropos

@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

@app.route('/ecole')
def ecole():
    return render_template('ecole.html')

@app.route('/paiement')
def paiement():
    return render_template('paiement.html')

@app.route('/certificat')
def certificat():
    return render_template('certificat.html')

#fin apropos

if __name__ == '__main__':
    db.create_all()
    
 

if __name__ == '__main__':
    db.create_all()
    
   # f1=formation('html','','','')
    #db.session.add(f1)
    #db.session.commit()

  
    app.run(debug = True)




