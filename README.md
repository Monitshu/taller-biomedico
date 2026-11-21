# Taller: Procesamiento de datos biomédicos con Python y MongoDB

Sistema en Python que genera, valida, ordena, guarda (TXT, CSV, JSON) y
consulta (MongoDB Atlas) registros de signos vitales.

**Integrantes:** _(escribir nombres del grupo)_
**Curso / Docente:** _(completar)_

## Estructura
```
taller_biomedico/
├── main.py            # Menú principal
├── datos.py           # Generación, regex y ordenamiento
├── archivos.py        # TXT, CSV, JSON, carpetas y log
├── mongo_db.py        # Conexión y consultas MongoDB
├── requirements.txt
├── log.txt            # Se crea al ejecutar
└── data/
    ├── txt/
    ├── csv/
    └── json/          # incluye resultados_mongo.json
```

## Requisitos e instalación
1. Python 3.10 o superior.
2. `pip install -r requirements.txt`

## Configurar MongoDB Atlas
1. Crear un cluster gratuito (M0) en mongodb.com/atlas.
2. *Database Access*: crear un usuario y contraseña.
3. *Network Access*: agregar tu IP (o 0.0.0.0/0 para pruebas).
4. *Connect → Drivers*: copiar la cadena `mongodb+srv://...`.
5. Definir la variable de entorno (la contraseña NO va en el código):
   - Windows (PowerShell): `$env:MONGO_URI="tu_cadena"`
   - Mac/Linux: `export MONGO_URI="tu_cadena"`
   - También se puede pegar la cadena cuando el programa la pida.

Base de datos: `bioingenieria` · Colección: `signos_vitales`.

## Ejecución
`python main.py`

| Opción | Función |
|---|---|
| 1 | Genera 50 registros aleatorios (ordenados por FC) o ingresa uno manual validado |
| 2 | Exporta TXT, CSV y JSON y los organiza en `data/` |
| 3 | Importa un JSON (solo acepta registros válidos) |
| 4 | Valida todos los registros con regex |
| 5 | Sube los registros validados a MongoDB |
| 6 | Promedio de FC, SpO2 < 94, búsqueda por ID y exportación a `resultados_mongo.json` |

## Formato de datos y expresiones regulares
| Campo | Ejemplo | Regex |
|---|---|---|
| id | ID-001 | `^ID-\d{3}$` |
| fr (edad) | 18 Años | `^\d{1,3} Años$` |
| fc | 090ppm | `^\d{3}ppm$` |
| spo2 | 95% | `^\d{2,3}%$` |

Nota: el enunciado define `fr` como edad, por eso se usa ese formato.
Se validan además rangos (SpO2 ≤ 100, edad ≤ 120).

## Ordenamiento
Se usa ordenamiento por inserción (implementado manualmente) sobre el valor
numérico de la frecuencia cardiaca, de menor a mayor.

## Log
Todas las acciones y errores quedan registrados en `log.txt`.
