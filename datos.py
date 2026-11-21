"""
datos.py
Generación, validación (expresiones regulares) y ordenamiento de registros
biomédicos. Cubre los ítems 1 y 4 del taller.
"""

import random
import re

# ---------------------------------------------------------------
# EXPRESIONES REGULARES (Ítem 4)
# Cada patrón define el formato exacto que debe tener cada campo.
# ---------------------------------------------------------------
PATRONES = {
    "id":   re.compile(r"^ID-\d{3}$"),       # Ejemplo: ID-001
    "fr":   re.compile(r"^\d{1,3} Años$"),   # Ejemplo: 18 Años (edad, según enunciado)
    "fc":   re.compile(r"^\d{3}ppm$"),       # Ejemplo: 090ppm
    "spo2": re.compile(r"^\d{2,3}%$"),       # Ejemplo: 95%
}

# Mensajes de ayuda que se muestran cuando el usuario escribe mal un campo
EJEMPLOS = {
    "id": "ID-001",
    "fr": "18 Años",
    "fc": "090ppm",
    "spo2": "95%",
}


def validar_registro(registro):
    """
    Valida que cada campo cumpla su patrón regex y además que los valores
    estén en rangos razonables (SpO2 <= 100, edad <= 120).
    Retorna (es_valido, lista_de_campos_con_error).
    """
    errores = []

    # 1) Validación de formato con regex
    for campo, patron in PATRONES.items():
        valor = str(registro.get(campo, ""))
        if not patron.match(valor):
            errores.append(campo)

    # 2) Validación de rangos (solo si el formato fue correcto)
    if "spo2" not in errores and int(registro["spo2"].rstrip("%")) > 100:
        errores.append("spo2")
    if "fr" not in errores and int(registro["fr"].split()[0]) > 120:
        errores.append("fr")

    return len(errores) == 0, errores


def validar_campo(campo, valor):
    """Valida un solo campo (se usa en el ingreso manual de datos)."""
    return bool(PATRONES[campo].match(valor))


# ---------------------------------------------------------------
# GENERACIÓN DE DATOS ALEATORIOS (Ítem 1)
# ---------------------------------------------------------------
def generar_registros(n=50):
    """
    Genera n registros aleatorios (mínimo 50) con el formato pedido:
      id   -> "ID-001"
      fr   -> "18 Años"
      fc   -> "090ppm"
      spo2 -> "95%"
    """
    registros = []
    for i in range(1, n + 1):
        registros.append({
            "id": f"ID-{i:03d}",
            "fr": f"{random.randint(18, 90)} Años",
            "fc": f"{random.randint(50, 140):03d}ppm",
            "spo2": f"{random.randint(88, 100)}%",
        })
    return registros


# ---------------------------------------------------------------
# ORDENAMIENTO (Ítem 1)
# ---------------------------------------------------------------
def valor_fc(registro):
    """Convierte '090ppm' en el número 90 para poder comparar."""
    return int(registro["fc"][:3])


def ordenar_por_fc(registros):
    """
    Ordena de menor a mayor frecuencia cardiaca con el algoritmo de
    ORDENAMIENTO POR INSERCIÓN, implementado a mano (sin sorted()).
    """
    datos = registros.copy()  # No se modifica la lista original
    for i in range(1, len(datos)):
        actual = datos[i]
        j = i - 1
        # Se desplazan a la derecha los elementos mayores que 'actual'
        while j >= 0 and valor_fc(datos[j]) > valor_fc(actual):
            datos[j + 1] = datos[j]
            j -= 1
        datos[j + 1] = actual
    return datos
