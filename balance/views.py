from . import app
from flask import render_template
from balance.models import DBManager


ruta_basedatos = app.config.get("RUTA_BASE_DE_DATOS")
dbmanager = DBManager(ruta_basedatos)

@app.route("/")
def inicio():

    movimientos = dbmanager.consultaSQL("SELECT * FROM movimiento order by fecha;")

    return render_template("inicio.html", items=movimientos)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    return "Página de alta de movimiento"


@app.route("/borrar/<int:id>", methods=["GET", "POST"])
def borrar(id=None):
    return f"Página de borrado de {id}"