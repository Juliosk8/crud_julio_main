from flask import Flask 
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify, request 
import pymysql

ruta = Blueprint('ruta', __name__)


def conectar (vhost, vuser, vpass, vdb):

    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn


@ruta.route("/consulta_ruta")
def consulta_general():

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM ruta """)
        datos = cur.fetchall()
        data=[]

        for row in datos:
            dato={'id_rutas': row[0], 'numero_ruta': row[1], 'horarios': row[2]} 
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'ruta': data, 'mensaje': 'rutas_cbc'})

    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

@ruta.route("/consulta_individual/<codigo>")
def consulta_individual(codigo):

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor() 
        cur.execute(""" SELECT * FROM ruta where id_rutas='{0}' """.format(codigo))

        datos=cur.fetchone()
        cur.close()
        conn.close()

        if datos!= None:
            dato={'id_rutas': row[0], 'numero_ruta': row[1], 'horarios': row[2]} 
            return jsonify({'ruta': dato, 'mensaje': 'Registro encontrado'})

        else:
            return jsonify({'mensaje': 'Registro no encontrado'})

    except Exception as ex:
         print(ex)
         return jsonify({'mensaje': 'Error'})

@ruta.route("/registro/") 
def registro():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        query = "insert into ruta (numero_ruta, horarios,) values \
            ('{0}', '{1}')""".format(request.json['numero_ruta'], request.json['horario'])
        x=cur.execute(query)
        conn.commit()
        cur.close() 
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@ruta.route("/eliminar/<codigo>")
def eliminar (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        x=cur.execute(""" delete from ruta where id_rutas={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'eliminado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@ruta.route("/actualizar/<codigo>")
def actualizar (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas') 
        cur = conn.cursor()
        query = query = "update ruta set numero_ruta='{0}', horarios='{1}'""".format(request.json['numero_ruta'], request.json['horarios'], codigo)
        x=cur.execute(query)

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})
        
    except Exception as ex:

        print(ex)

        return jsonify({'mensaje': 'Error'})

if __name__ == '__main__':
    app.run(debug=True)