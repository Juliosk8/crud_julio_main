from flask import Flask 
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify, request 
import pymysql

aprendiz = Blueprint('aprendiz', __name__)



def conectar (vhost, vuser, vpass, vdb):

    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset = 'utf8mb4')
    return conn


@aprendiz.route("/consulta_aprendiz")
def consulta_general():

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM aprendiz """)
        datos = cur.fetchall()
        data=[]

        for row in datos:
            dato={'id_aprendiz': row[0], 'nombre_completo': row[1], 'T_documento': row[2], 'N_documento' :row[3], 'celular' :row[4], 'correo' :row[5], 'ficha' :row[6], 'password' :row[7]} 
            data.append(dato)

        cur.close()
        conn.close()
        return jsonify({'aprendiz': data, 'mensaje': 'rutas_cbc'})

    except Exception as ex:
        print (ex)
        return jsonify({'mensaje': 'Error'})

@aprendiz.route("/consulta_individual_aprendiz/<codigo>", methods=['get'])
def consulta_individual(codigo):

    try:
        conn=conectar('localhost', 'root', '','gestor_rutas')
        cur = conn.cursor() 
        cur.execute(""" SELECT * FROM aprendiz where id_aprendiz='{0}' """.format(codigo))

        datos=cur.fetchone()
        cur.close()
        conn.close()

        if datos!= None:
            datos={'id_aprendiz': dato[0], 'nombre_completo': dato[1], 'T_documento': dato[2], 'N_documento' :dato[3], 'celular' :dato[4], 'correo' :dato[5], 'ficha' :dato[6], 'password' :dato[7]} 
            return jsonify({'aprendiz': dato, 'mensaje': 'Registro encontrado'})

        else:
            return jsonify({'mensaje': 'Registro no encontrado'})

    except Exception as ex:
         print(ex)
         return jsonify({'mensaje': 'Error'})

@aprendiz.route("/registro_aprendiz") 
def registro():
    try:
        conn = conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        query = "insert into aprendiz (nombre_completo, T_documento, N_documento, celular, correo, ficha, password) values \
            ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')""".format(request.json['nombre_completo'], request.json['T_documento'], request.json['N_documento'], request.json['celular'], request.json['correo'], request.json['ficha'], request.json['password'])
        x=cur.execute(query)
        conn.commit()
        cur.close() 
        conn.close()

        return jsonify({'mensaje': 'Registro agregado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@aprendiz.route("/eliminar_aprendiz/<codigo>", methods=['delete'])
def eliminar (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas')
        cur = conn.cursor()
        x=cur.execute(""" delete from aprendiz where id_aprendiz={0}""".format(codigo))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'mensaje': 'eliminado'})

    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

@aprendiz.route("/actualizar/<codigo>")
def actualizar (codigo):
    try:
        conn=conectar('localhost', 'root', '', 'gestor_rutas') 
        cur = conn.cursor()
        query = query = "update aprendiz set nombre_completo='{0}', T_documento='{1}', N_documento='{2}', celular='{3}', correo='{4}', ficha='{5}', password='{6}' where id_aprendiz={7}""".format(request.json['nombre_completo'], request.json['T_documento'], request.json['N_documento'], request.json['celular'], request.json['correo'], request.json['ficha'] ,request.json['password'], codigo)
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