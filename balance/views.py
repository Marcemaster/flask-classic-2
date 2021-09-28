from . import app
from flask import render_template, request, redirect, url_for, flash
from balance.models import DBManager
from balance.forms import MovimientoFormulario
from datetime import date



ruta_basedatos = app.config.get("RUTA_BASE_DE_DATOS")
dbmanager = DBManager(ruta_basedatos)

@app.route("/")
def inicio():

    consulta = '''SELECT *
                 FROM movimiento 
                ORDER BY fecha;'''
    movimientos = dbmanager.consultaSQL(consulta)
    return render_template("inicio.html", items=movimientos)

@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():

    formulario = MovimientoFormulario()

    if request.method == "GET":
        return render_template("nuevo_movimiento.html", el_formulario = formulario)
    else:
        if formulario.validate():
            consulta = '''
                INSERT INTO movimiento (fecha, concepto, ingreso_gasto, cantidad)
                VALUES (:fecha, :concepto, :ingreso_gasto, :cantidad)
            '''

            try:
                dbmanager.modificaSQL(consulta, formulario.data)

            except Exception as e:
                print("Se ha producido un error de acceso a base de datos:",e)
                flash("Se ha  producido un error en la base de datos. Consulte con su administrador")
                return render_template("nuevo_movimiento.html", el_formulario = formulario)

            return redirect(url_for("inicio"))

        else:
            return render_template("nuevo_movimiento.html", el_formulario = formulario)
        
        '''
        Validar formulario ( Si OK, -> insertar registro en tabla y redireccionar a /)
        
        Si la validación es erronea -> devolver el formulario y render template
        y preparar la plantilla para gestionar los errores.
        
        '''

@app.route("/borrar/<int:id>", methods=["GET", "POST"])
def borrar(id):
    if request.method == "GET":
        consulta = '''
            SELECT id, fecha, concepto, ingreso_gasto, cantidad
              FROM movimiento
            WHERE id = ?;
        '''

        movimientos = DBManager.consultaSQL(consulta, [id])
        if len(movimientos) == 0:
            flash(f"Movimiento {id} no encontrado")
            return redirect(url_for("inicio"))

        el_movimiento = movimientos[0]
        el_movimiento["fecha"] = date.fromisoformat(el_movimiento["fecha"])
        formulario = MovimientoFormulario(data=el_movimiento)

        return render_template("borrar_movimiento.html", el_formulario=formulario)
    else:
        #TRABAJO PENDIENTE ( SI EL RESULTADO ES POST CONSTRUIR LA CONSULTA CON UN DELETE ) Lo mismo que va de la linea 31 a la 45 pero en lugar de delete con insert y la validación es opcional
    
    return "Hola"
