import ollama
import json

# 1. Definimos un texto de prueba (simulando un correo del archivo)
texto_correo = """
Fecha: 12 de mayo de 2004
De: Mario Levrero
Para: Elvio Gandolfo
Asunto: Las galeradas

Querido Elvio, te escribo desde Montevideo. Anoche por fin terminé de revisar las galeradas de La novela luminosa. 
Fue un parto, estoy agotado y la computadora me está volviendo loco. Decile a Ignacio que la semana que viene 
le mando el disquete con la versión final para la editorial. 

Un abrazo,
Mario
"""

# 2. Diseñamos el "prompt" con instrucciones estrictas para el modelo
prompt_sistema = f"""
Sos un asistente experto en archivística y humanidades digitales. 
Tu tarea es leer el siguiente correo y extraer las entidades solicitadas en formato JSON estricto.

El esquema JSON debe ser exactamente este:
{{
    "emisor": "Nombre del remitente",
    "receptores": ["Lista de destinatarios directos"],
    "personas_mencionadas": ["Otras personas nombradas en el texto"],
    "lugares": ["Lugares geográficos mencionados"],
    "obras_citadas": ["Títulos de libros u obras mencionadas"],
    "resumen_archivistico": "Un párrafo conciso (máximo 3 líneas) resumiendo el asunto y contenido del correo."
}}

Correo a analizar:
{texto_correo}
"""

print("Iniciando conexión con llama3.1:8b en la RTX 5070...")
print("Procesando documento...")

# 3. Llamada a la API local de Ollama (forzando el formato JSON)
respuesta = ollama.chat(
    model='llama3.1:8b',
    messages=[{'role': 'user', 'content': prompt_sistema}],
    format='json'
)

# 4. Parsear y mostrar el resultado
try:
    # Convertimos el string devuelto por Ollama a un diccionario de Python
    datos_extraidos = json.loads(respuesta['message']['content'])
    
    print("\n✅ ¡Extracción exitosa!\n")
    # Imprimimos el JSON formateado para que sea fácil de leer
    print(json.dumps(datos_extraidos, indent=4, ensure_ascii=False))

except json.JSONDecodeError:
    print("\n❌ Error: El modelo no devolvió un JSON válido.")
    print("Respuesta cruda del modelo:")
    print(respuesta['message']['content'])
