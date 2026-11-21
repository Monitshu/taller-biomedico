import os

import archivos
import datos
import mongo_db


registros = []
coleccion = None 


def pedir_campo(campo):
    
    while True:
        valor = input(f"  {campo} (ej. {datos.EJEMPLOS[campo]}): ").strip()
        if datos.validar_campo(campo, valor):
            return valor
        print(f"  Formato inválido. Debe ser como {datos.EJEMPLOS[campo]}")

 # Opción 1: generar registros aleatorios o ingresarlos manualmente
def ingresar_datos():
   
    global registros
    print("\n1) Generar 50 registros aleatorios\n2) Ingresar un registro manualmente")
    op = input("Elige: ").strip()
    if op == "1":
        registros = datos.ordenar_por_fc(datos.generar_registros(50))
        archivos.log("Generados 50 registros aleatorios y ordenados por FC")
        print("50 registros generados y ordenados por frecuencia cardiaca.")
    elif op == "2":
        nuevo = {c: pedir_campo(c) for c in ["id", "fr", "fc", "spo2"]}
        valido, errores = datos.validar_registro(nuevo)
        if valido:
            registros = datos.ordenar_por_fc(registros + [nuevo])
            archivos.log(f"Registro manual agregado: {nuevo['id']}")
            print("Registro agregado.")
        else:
            print(f"Valores fuera de rango en: {errores}")
    else:
        print("Opción no válida.")


def exportar():
    
    if not registros:
        print("No hay datos. Usa la opción 1 primero.")
        return
    n = archivos.exportar_todo(registros)
    print(f"Archivos exportados y organizados en data/ ({n} movidos).")


def importar():
    
    global registros
    ruta = input("Ruta del JSON [Enter = data/json/datos_ordenados.json]: ").strip()
    ruta = ruta or archivos.CARPETAS["json"] / "datos_ordenados.json"
    cargados = archivos.importar_json(ruta)
    validos = [r for r in cargados if datos.validar_registro(r)[0]]
    registros = datos.ordenar_por_fc(validos)
    print(f"Importados {len(cargados)} registros, {len(validos)} válidos.")


def validar():
   
    if not registros:
        print("No hay datos para validar.")
        return
    invalidos = 0
    for r in registros:
        ok, errores = datos.validar_registro(r)
        if not ok:
            invalidos += 1
            print(f"{r.get('id')} inválido en: {errores}")
    print(f"Validación terminada: {len(registros) - invalidos} válidos, {invalidos} inválidos.")
    archivos.log(f"Validación: {invalidos} inválidos de {len(registros)}")

#Conecta a Atlas usando MONGO_URI o pidiendo la cadena por teclado.
def conectar_mongo():
    
    global coleccion
    if coleccion is not None:
        return True
    uri = os.environ.get("MONGO_URI") or input("Pega tu cadena MONGO_URI: ").strip()
    try:
        coleccion = mongo_db.conectar(uri)
        print("Conectado a MongoDB Atlas.")
        return True
    except Exception as e:
        archivos.log(f"ERROR conectando a MongoDB: {e}")
        print(f"No se pudo conectar: {e}")
        return False


def subir_mongo():
    
    if not registros:
        print("No hay datos. Usa la opción 1 primero.")
        return
    if not conectar_mongo():
        return
    validos = [r for r in registros if datos.validar_registro(r)[0]]
    mongo_db.insertar_registros(coleccion, validos)
    print(f"{len(validos)} registros validados insertados en 'signos_vitales'.")


def consultas_mongo():
  
    if not conectar_mongo():
        return
    print("\n1) Promedio de FC\n2) SpO2 menor a 94\n3) Buscar por ID\n4) Exportar a resultados_mongo.json")
    op = input("Elige: ").strip()
    try:
        if op == "1":
            print("Promedio FC:", mongo_db.promedio_fc(coleccion), "ppm")
        elif op == "2":
            for d in mongo_db.spo2_bajo(coleccion):
                print(d)
        elif op == "3":
            id_ = input("ID (ej. ID-005): ").strip().upper()
            print(mongo_db.buscar_por_id(coleccion, id_) or "No encontrado.")
        elif op == "4":
            mongo_db.exportar_consultas(coleccion)
            print("Guardado en data/json/resultados_mongo.json")
        else:
            print("Opción no válida.")
    except Exception as e:
        archivos.log(f"ERROR en consulta: {e}")
        print(f"Error en la consulta: {e}")


def menu():
    archivos.crear_estructura()
    acciones = {"1": ingresar_datos, "2": exportar, "3": importar,
                "4": validar, "5": subir_mongo, "6": consultas_mongo}
    while True:
        print("\n=== SISTEMA BIOMÉDICO ===")
        print("1. Ingresar datos (aleatorio o manual)")
        print("2. Exportar archivos (TXT, CSV, JSON)")
        print("3. Importar JSON")
        print("4. Validar datos")
        print("5. Subir datos a MongoDB")
        print("6. Consultas MongoDB")
        print("0. Salir")
        op = input("Opción: ").strip()
        if op == "0":
            archivos.log("Programa finalizado")
            print("Hasta pronto.")
            break
        accion = acciones.get(op)
        if accion:
            accion()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
