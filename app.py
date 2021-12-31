from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from sqlalchemy.sql.expression import false




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:asma0613@localhost:5432/formation"
db = SQLAlchemy(app)

class formation(db.Model):
    __tablename__ ='formation'
    id = db.Column(db.Integer, primary_key=True)
    titredb = db.Column(db.String(80), unique=false)
    Categoriedb = db.Column(db.String(120), unique=false)
    desc_courtedb = db.Column(db.String(120), unique=false)
    desc_longdb = db.Column(db.String(500), unique=false)

    def __init__(self,titredb,Categoriedb,desc_courtedb,desc_longdb):
         
                            self.titredb=titredb
                            self.Categoriedb=Categoriedb
                            self.desc_courtedb=desc_courtedb
                            self.desc_longdb=desc_longdb
                            

@app.route('/admin/', methods=['POST', 'GET'])

def adminpage():
    
  
    return render_template("admin.html")
@app.route('/avis')
def avis():
     return render_template("avis.html")

@app.route('/' , methods=['POST', 'GET'])

def homepage():

    if request.method == 'POST':
       titre=request.form['titre']
       Categorie=request.form['Categorie']
       desc_courte=request.form['desc_courte']
       desc_long=request.form['desc_long']
       newFormation= formation (titre,Categorie,desc_courte,desc_long)
       db.session.add(newFormation)   
       db.session.commit()
    formations=formation.query.all()
    
    


    return render_template("base.html",formations=formations)





def hello():
        return "hello world"

if __name__ == '__main__':
    
    
    app.run(debug = True)
