from flask import Flask 
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify, request 
import pymysql

programa = Blueprint('programa', __name__)


def conectar (vhost, vuser, vpass, vdb):

    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn


@programa.route("/consulta_programa")
def consulta_general():

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM programa """)
        datos = cur.fetchall()
        data=[]

        for row in datos:
            dato={'id_programa': row[0], 'nombre_programa': row[1]} 
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'programa': data, 'mensaje': 'rutas_cbc'})

    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

@programa.route("/consulta_individual/<codigo>")
def consulta_individual(codigo):

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor() 
        cur.execute(""" SELECT * FROM programa where id_programa='{0}' """.format(codigo))

        datos=cur.fetchone()
        cur.close()
        conn.close()

        if datos!= None:
            dato={'id_programa': row[0], 'nombre_programa': row[1]} 
            return jsonify({'programa': dato, 'mensaje': 'Registro encontrado'})

        else:
            return jsonify({'mensaje': 'Registro no encontrado'})

    except Exception as ex:
         print(ex)
         return jsonify({'mensaje': 'Error'})

@programa.route("/registro_programa/") 
def registro():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        query = "insert into programa (nombre_programa) values \
            ('{0}', '{1}')""".format(request.json['nombre_programa'])
        x=cur.execute(query)
        conn.commit()
        cur.close() 
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@programa.route("/eliminar/<codigo>")
def eliminar (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        x=cur.execute(""" delete from programa where id_programa={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'eliminado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@programa.route("/actualizar/<codigo>")
def actualizar (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas') 
        cur = conn.cursor()
        query = query = "update programa set nombre_programa='{0}'""".format(request.json['nombre_completo'], codigo)
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