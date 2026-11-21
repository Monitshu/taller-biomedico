"""
mongo_db.py
Conexión de Python con MongoDB Atlas, inserción y consultas.
Cubre el ítem 5 del taller.
"""

import json
import os

import certifi
from pymongo import MongoClient

from archivos import CARPETAS, log

NOMBRE_BD = "bioingenieria"
NOMBRE_COLECCION = "signos_vitales"   


def conectar(uri=None):
   
    uri = uri or os.environ.get("MONGO_URI")
    if not uri:
        raise ValueError("No hay cadena de conexión (MONGO_URI).")
    cliente = MongoClient(uri, tlsCAFile=certifi.where(),
                          serverSelectionTimeoutMS=8000)
    cliente.admin.command("ping")     
    log("Conexión exitosa con MongoDB Atlas")
    return cliente[NOMBRE_BD][NOMBRE_COLECCION]

# remplazar los datos y no los duplica 
def insertar_registros(coleccion, registros):
   
    for r in registros:
        doc = dict(r)
        doc["fc_num"] = int(r["fc"][:3])
        doc["spo2_num"] = int(r["spo2"].rstrip("%"))
        coleccion.replace_one({"id": doc["id"]}, doc, upsert=True)
    log(f"MongoDB: {len(registros)} registros insertados en {NOMBRE_COLECCION}")

# promedio de todas las colecciones 
def promedio_fc(coleccion):
    
    res = list(coleccion.aggregate(
        [{"$group": {"_id": None, "promedio": {"$avg": "$fc_num"}}}]))
    return round(res[0]["promedio"], 2) if res else None


def spo2_bajo(coleccion, limite=94):
    """Documentos con SpO2 menor al límite (por defecto 94)."""
    return list(coleccion.find({"spo2_num": {"$lt": limite}}, {"_id": 0}))


def buscar_por_id(coleccion, id_):
    """Busca un documento por su ID (ej. 'ID-005')."""
    return coleccion.find_one({"id": id_}, {"_id": 0})


def exportar_consultas(coleccion, ruta=None):
    """Guarda las consultas en data/json/resultados_mongo.json."""
    ruta = ruta or CARPETAS["json"] / "resultados_mongo.json"
    resultado = {
        "promedio_frecuencia_cardiaca": promedio_fc(coleccion),
        "documentos_spo2_menor_94": spo2_bajo(coleccion),
    }
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)
    log(f"Consultas exportadas a {ruta}")
    return resultado
