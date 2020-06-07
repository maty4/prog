import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_sqlalchemy import SQLAlchemy

#Für den Pfad zur Datenbank / sqlite verwendet
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
#Secret Key eingebaut, damit keine Fehlermeldung kommt
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

#Model Table für die Datenbank
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefon = db.Column(db.String(100))
 
 
    def __init__(self, name, email, telefon):
 
        self.name = name
        self.email = email
        self.telefon = telefon

@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", kontakte = all_data)


#Für das Hinzufügen von Kontakten
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telefon = request.form['telefon']

        my_data = Data(name, email, telefon)
        db.session.add(my_data)
        db.session.commit()

        flash("Kontakt erfolgreich hinzugefügt")

        return redirect(url_for('Index'))



#Für das Bearbeiten der Einträge
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.telefon = request.form['telefon']

        db.session.commit()
        flash("Kontakt erfolgreich bearbeitet")

        return redirect(url_for('Index'))




#Für das Löschen der Einträge
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Kontakt erfolgreich gelöscht")

    return redirect (url_for("Index"))




if __name__ == "__main__":
    app.run(debug=True)
