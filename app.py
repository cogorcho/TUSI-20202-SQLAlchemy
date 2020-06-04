from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from model.db import (
    Base, 
    Persona, 
    Usuario, 
    Provincia, 
    Sector, 
    Ambito, 
    Localidad,
    Escuela)

engine = create_engine('sqlite:///db/escuela.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

app = Flask(__name__)

@app.route('/')
def show_login():
    return render_template('login.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        passwd = request.form.get('passwd')
        return "<h1>%s: %s</h1>" % (email, passwd)
    else:
        print(request.method)
        return render_template('login.html')


@app.route('/sector')
def sector():
    session = DBSession()
    rows = []
    secs = session.query(Sector).all()
    for s in secs:
        e = { "id": s.id, "nombre" : s.nombre }
        rows.append(e)
    data = {
        "titulo":"Sectores",
        "rows" : rows
    }
    return render_template('keyval.html', data=data)

@app.route('/ambito')
def ambito():
    session = DBSession()
    rows = []
    secs = session.query(Ambito).all()
    for s in secs:
        e = { "id": s.id, "nombre" : s.nombre }
        rows.append(e)
    data = {
        "titulo":"Ambitos",
        "rows" : rows
    }
    return render_template('keyval.html', data=data)

@app.route('/provincia')
def provincia():
    session = DBSession()
    rows = []
    secs = session.query(Provincia).all()
    for s in secs:
        e = { "id": s.id, "nombre" : s.nombre }
        rows.append(e)
    data = {
        "titulo":"Provincias",
        "rows" : rows
    }
    return render_template('keyval.html', data=data)

@app.route('/localidad/<locid>')
def localidad(locid):
    session = DBSession()
    rows = []
    secs = session.query(Localidad).filter(Localidad.id == locid).all()
    for s in secs:
        e = { "id": s.id, "nombre" : s.nombre }
        rows.append(e)
    data = {
        "titulo":"Localidad",
        "rows" : rows
    }
    return render_template('keyval.html', data=data)

@app.route('/localidades/<pciaid>')
def localidades(pciaid):
    session = DBSession()
    rows = []
    secs = session.query(Localidad).filter(Localidad.provincia_id == pciaid).all()
    for s in secs:
        e = { "id": s.id, "nombre" : s.nombre }
        rows.append(e)
    data = {
        "titulo":"Localidades",
        "rows" : rows
    }
    return render_template('keyval.html', data=data)

@app.route('/escuelas/<locid>')
def listar_escuelas(locid):
    session = DBSession()
    rows = []
    escs = session.query(Escuela).filter_by(localidad_id=locid).order_by(Escuela.nombre).all()
    for esc in escs:
        e = {"id" : esc.id, "nombre" : esc.nombre.title() }
        rows.append(e)
    data = {
        "titulo":"Escuelas",
        "rows" : rows
    }
    return render_template('keyval.html', data=data)

if __name__ == '__main__':
    app.run()