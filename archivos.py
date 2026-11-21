"""
archivos.py
Manejo de archivos TXT, CSV y JSON, estructura de carpetas, organización
automática de archivos y registro de acciones en log.txt.
Cubre los ítems 2 y 3 del taller.
"""

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

# Carpeta donde está este script (así funciona en cualquier computador)
BASE = Path(__file__).resolve().parent
CARPETAS = {
    "txt": BASE / "data" / "txt",
    "csv": BASE / "data" / "csv",
    "json": BASE / "data" / "json",
}
LOG = BASE / "log.txt"
CAMPOS = ["id", "fr", "fc", "spo2"]


# ---------------------------------------------------------------
# LOG (Ítem 3)
# ---------------------------------------------------------------
def log(mensaje):
    """Agrega una línea con fecha y hora a log.txt."""
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {mensaje}\n")
    except OSError as e:
        print(f"No se pudo escribir en el log: {e}")


# ---------------------------------------------------------------
# CARPETAS Y ORGANIZACIÓN (Ítem 3)
# ---------------------------------------------------------------
def crear_estructura():
    """Crea data/txt, data/csv y data/json si no existen."""
    for ruta in CARPETAS.values():
        ruta.mkdir(parents=True, exist_ok=True)
    log("Estructura de carpetas creada/verificada")


def organizar_archivos():
    """
    Busca archivos .txt, .csv y .json sueltos en la carpeta del proyecto y
    los mueve automáticamente a su carpeta (data/txt, data/csv, data/json).
    El log.txt y el requirements.txt se dejan donde están.
    """
    movidos = 0
    excluidos = {"log.txt", "requirements.txt"}
    for archivo in BASE.glob("*.*"):
        ext = archivo.suffix.lstrip(".").lower()
        if ext in CARPETAS and archivo.name not in excluidos:
            destino = CARPETAS[ext] / archivo.name
            try:
                shutil.move(str(archivo), str(destino))  # sobrescribe si existe
                log(f"Archivo movido: {archivo.name} -> data/{ext}/")
                movidos += 1
            except (OSError, shutil.Error) as e:
                log(f"ERROR moviendo {archivo.name}: {e}")
    return movidos


# ---------------------------------------------------------------
# GUARDAR (Ítem 2) - cada función usa try/except y verifica la ruta
# ---------------------------------------------------------------
def _verificar_carpeta(ruta):
    """Verifica que la carpeta destino exista; si no, la crea."""
    ruta = Path(ruta)
    if not ruta.parent.exists():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        log(f"Carpeta creada: {ruta.parent}")
    return ruta


def guardar_txt(registros, ruta):
    """Guarda los registros en .txt (una línea por registro, separados por coma)."""
    try:
        ruta = _verificar_carpeta(ruta)
        with open(ruta, "w", encoding="utf-8") as f:
            for r in registros:
                f.write(f"{r['id']},{r['fr']},{r['fc']},{r['spo2']}\n")
        log(f"TXT guardado: {ruta.name} ({len(registros)} registros)")
        return True
    except (OSError, KeyError) as e:
        log(f"ERROR guardando TXT: {e}")
        return False


def guardar_csv(registros, ruta):
    """Guarda los registros en .csv con encabezado."""
    try:
        ruta = _verificar_carpeta(ruta)
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(registros)
        log(f"CSV guardado: {ruta.name} ({len(registros)} registros)")
        return True
    except (OSError, ValueError) as e:
        log(f"ERROR guardando CSV: {e}")
        return False


def exportar_json(registros, ruta):
    """Exporta los registros a .json."""
    try:
        ruta = _verificar_carpeta(ruta)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(registros, f, indent=4, ensure_ascii=False)
        log(f"JSON exportado: {ruta.name} ({len(registros)} registros)")
        return True
    except (OSError, TypeError) as e:
        log(f"ERROR exportando JSON: {e}")
        return False


def importar_json(ruta):
    """Importa registros desde un .json. Devuelve [] si hay algún problema."""
    ruta = Path(ruta)
    if not ruta.exists():                       # verificación de ruta
        log(f"ERROR: no existe el archivo {ruta}")
        print(f"No existe el archivo: {ruta}")
        return []
    try:
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
        log(f"JSON importado: {ruta.name} ({len(datos)} registros)")
        return datos
    except (json.JSONDecodeError, OSError) as e:
        log(f"ERROR importando JSON: {e}")
        print(f"Error leyendo el JSON: {e}")
        return []


def exportar_todo(registros):
    """
    Guarda TXT, CSV y JSON primero en la carpeta raíz y luego los organiza
    (mueve) automáticamente a data/txt, data/csv y data/json.
    """
    guardar_txt(registros, BASE / "datos_ordenados.txt")
    guardar_csv(registros, BASE / "datos_ordenados.csv")
    exportar_json(registros, BASE / "datos_ordenados.json")
    return organizar_archivos()
