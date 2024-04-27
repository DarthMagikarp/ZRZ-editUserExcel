# chat conversation
import json
import pymysql
import requests
import http.client
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from itertools import cycle
import pandas as pd
from sqlalchemy import create_engine

# Leer el Excel
excel_file = r"C:\Users\dbravofl\Downloads\Alumnos pre SM.xlsx"  # Nombre del archivo Excel
df = pd.read_excel(excel_file)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["POST"])
@cross_origin()
def function(self):
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_DDBB = os.getenv("DB_DDBB")
    #try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DDBB)
    cursor = connection.cursor()

    print("conexión exitosa")

    for index, row in df.iterrows():
        # Extraer datos de la fila del Excel
        rut = row['rut']
        nombre = row['Nombre'].split()[0]  # Dividir el nombre completo en nombre y apellido
        apellido = ' '.join(row['Nombre'].split()[1:])
        telefono = row['fono'] if not pd.isnull(row['fono']) else None
        email = row['email']
        fecha_nacimiento = pd.to_datetime(row['fecha_nacimiento'], format='%Y%m%d').strftime('%Y-%m-%d')
        carrera = row['carr_nombre']
        direccion = row['Direccion']
        comuna = row['Comuna']

        print(email)

        # Añade el resto de los campos que se deseen actualizar en la base de datos
        
        # Verificar si el registro ya existe
        query_check = f'''SELECT * FROM '''+DB_DDBB+'''.usuarios
                        WHERE rut = {rut}'''
        cursor.execute(query_check)
        existing_record = cursor.fetchone()
        
        if existing_record:
            # El registro ya existe, entonces actualízalo
            query_update = f'''
                UPDATE '''+DB_DDBB+'''.usuarios
                SET nombre = '{nombre}',
                    apellido = '{apellido}',
                    telefono = '{telefono}',
                    email = '{email}',
                    fecha_nacimiento = '{fecha_nacimiento}',
                    carrera = '{carrera}',
                    direccion = '{direccion}',
                    comuna = '{comuna}'
                WHERE rut = {rut}
            '''
            cursor.execute(query_update)
        else:
            # El registro no existe, entonces inserta uno nuevo
            query_insert = f'''
                INSERT INTO '''+DB_DDBB+'''.usuarios 
                (nombre, apellido, telefono, email, fecha_nacimiento, carrera, direccion, comuna, rut)
                VALUES ('{nombre}', '{apellido}', '{telefono}', '{email}', '{fecha_nacimiento}', '{carrera}', '{direccion}', '{comuna}', {rut})
            '''
            cursor.execute(query_insert)

    # Confirmar los cambios
    conn.commit()

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()

    return retorno

    #except Exception as e:
    #    print('Error: '+ str(e))
    #    retorno = {           
    #        "detalle":"algo falló", 
    #        "validacion":False
    #    }
    #    return retorno

if __name__ == "__main__":
    app.run(debug=True, port=8002, ssl_context='adhoc')