from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from sqlalchemy.sql.expression import false

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:asma0613@localhost:5432/formation"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:asma0613@localhost/formation"

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
class Inscription(db.Model):
    __tablename__ ='Inscription'
    id = db.Column(db.Integer, primary_key=True, )
    nom = db.Column(db.String(30), unique=False, )
    prenom = db.Column(db.String(30), unique=False, )
    Email = db.Column(db.String(30), unique=False, )
    téléphone = db.Column(db.String(20), unique=False, )
    formation_insc= db.Column(db.String(30), unique=False, )

    def __init__(self,nom,prenom,Email,téléphone,formation_insc):
         
                            self.nom=nom
                            self.prenom=prenom
                            self.Email=Email
                            self.téléphone=téléphone
                            self.formation_insc=formation_insc   

@app.route('/admin/', methods=['POST', 'GET'])

def adminpage():
    return render_template('admin.html')



@app.route('/' , methods=['POST', 'GET'])

def homepage():

    if request.method == 'POST':
       titre=request.form['titre']
       Categorie=request.form['Categorie']
       desc_courte=request.form['desc_courte']
       desc_long=request.form['desc_long']

       newFormation= formation (titre,Categorie,desc_courte,desc_long)

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

@app.route('/inscription' ,  methods=['POST', 'GET'])
def inscr():
  if request.method == 'POST':
        nom=request.form['nom']
        prenom=request.form['prenom']
        Email=request.form['Email']
        téléphone=request.form['téléphone']
        formation_insc=request.form['formation_insc']
        newInscription=Inscription(nom,prenom,Email,téléphone,formation_insc)
        db.session.add(newInscription)   
        db.session.commit()



  formations=formation.query.all()
  return render_template('inscrp.html',formations=formations )


if __name__ == '__main__':
   # db.create_all()
   # f1=formation('html','','','')
    #db.session.add(f1)
    #db.session.commit()
  
    app.run(debug = True)




