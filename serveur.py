# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:46:22 2020
Edited on Mon May  25 22:34:00 2020

@author: Mr ABBAS-TURKI
@student : Valentin Mercy
"""

from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import random
import os
import string
from hashlib import sha256

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Identifiant',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Creer mon compte pilote')

class LoginForm(FlaskForm):
    username = StringField('Identifiant',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Me connecter')

LONGUEUR_CODE = 10

LONGUEUR_HASH = 64 #une longueur de 64 caracteres est a prevoir pour une representation hexadecimale des hash
LONGUEUR_SEL = 100
PBKDF2_NB_ITER = 80000 #nombre d'iterations du hashage avec PBKDF2 (selon les recommandations donnees en cours)

def GenererSel(): #retourne un sel de taille fixe compose de caracteres alphanumeriques
    AlphaNumChars = string.ascii_letters + string.digits
    return ''.join((random.choice(AlphaNumChars) for i in range(LONGUEUR_SEL)))

Authentified = False
CURRENT_USER=""

def randomize_number(length): #renvoie un nombre aleatoire de longueur donnee
    return str(random.randint(10**(length-1),10**length-1))

MESSAGE_SECRET = randomize_number(LONGUEUR_CODE)

app=Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

class Pilot(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(LONGUEUR_HASH),nullable=False)
    password_salt = db.Column(db.String(LONGUEUR_SEL),nullable=False)
    def __repr__(self):
        return "Id : "+str(self.id)+" | Identifiant : "+str(self.username)

print("Mot de passe du hangar genere aleatoirement : "+MESSAGE_SECRET)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/get_code")
def get_secret_message():
    if Authentified:
        return render_template('code.html', title='Login', secret=MESSAGE_SECRET, user=CURRENT_USER)
    else:
        flash("Vous n'etes pas connecté !",'danger')
        return render_template('code.html', title='Login', secret="")

@app.route("/register",methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Votre compte de pilote a ete cree avec succes", 'success')
        return redirect(url_for('/'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("Login form open")
    if form.validate_on_submit():
        print("Soumission formulaire")
        if form.username.data == 'valentin' and form.password.data == 'mercy':
            global CURRENT_USER
            global Authentified
            Authentified = True
            CURRENT_USER = "Valentin"
            print("Authentification ok")
            flash('Connexion reussie !', 'success')
            return redirect(url_for('get_secret_message'))
        else:
            print("Echec connexion")
            flash('Echec de la connexion, veuillez verifier votre identifiant et/ou votre mot de passe.', 'danger')
    else:
        print("Pas de soumission du formulaire")
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    global Authentified
    Authentified = False
    return redirect(url_for('main'))


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0",port=8081)
    #app.run(debug=True, host="0.0.0.0",port=8081,ssl_context=("serveur-cle-publique.pem","serveur-cle-privee.pem"))