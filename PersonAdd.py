from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from pony.orm import *

db = Database("sqlite", "person.sqlite", create_db=True)

class CustomerX(db.Entity):
    emailX = Required(str, unique=True)
    passwordX = Required(str)
    nameX = Required(str)
    countryX = Required(str)
    addressX = Required(str)

sql_debug(True)

db.generate_mapping(create_tables=True)

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    country = TextField('country:', validators=[validators.required()])
    address = TextField('address:', validators=[validators.required()])

@db_session
def populate_database():
    c1 = CustomerX(emailX=request.form['email'], passwordX=request.form['password'],
                  nameX=request.form['name'], countryX=request.form['country'], addressX=request.form['address'])			  
				  
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        country=request.form['country']
        address=request.form['address']
		
        print (name, " ", email, " ", password , " ", country, " ", address)
 
        if form.validate():
            # All fields have been validated
            populate_database()
            flash(name + 'has been added to the database')
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('formPersonAdd.html', form=form)
 
if __name__ == "__main__":
    app.run()
