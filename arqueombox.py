import mailbox
import os
import email
from email.header import decode_header
import re

def decodificar_seguro(byte_data, charset_sugerido=None):
    """
    Intenta decodificar cadenas de bytes iterando por distintas codificaciones 
    históricas para garantizar la conservación de caracteres especiales (tildes, eñes).
    """
    if not byte_data:
        return ""
        
    codificaciones = []
    
    # 1. Priorizamos la codificación declarada por los metadatos del correo
    if charset_sugerido:
        codificaciones.append(charset_sugerido)
        
    # 2. Agregamos estándares comunes en correos legados de América Latina
    codificaciones.extend(['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1'])
    
    for codificacion in codificaciones:
        try:
            return byte_data.decode(codificacion)
        except (UnicodeDecodeError, LookupError, TypeError):
            continue
            
    # Si todas las codificaciones fallan, forzamos lectura reemplazando errores
    return byte_data.decode('utf-8', errors='replace')

def limpiar_metadato(texto_crudo):
    """
    Limpia y decodifica encabezados de correo (Asunto, De, Para) que suelen 
    llegar fragmentados o codificados en Base64/Quoted-Printable.
    """
    if not texto_crudo:
        return "No especificado"
    
    partes_decodificadas = decode_header(texto_crudo)
    texto_limpio = ""
    
    for parte, encoding in partes_decodificadas:
        if isinstance(parte, bytes):
            texto_limpio += decodificar_seguro(parte, encoding)
        else:
            texto_limpio += str(parte)
            
    return texto_limpio.strip()

def sanitizar_html(texto_html):
    """
    Función auxiliar que utiliza expresiones regulares para limpiar etiquetas HTML, 
    decodificar entidades básicas y retornar texto plano legible.
    """
    texto_limpio = re.sub(r'<[^>]+>', '', texto_html)
    texto_limpio = texto_limpio.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
    texto_limpio = re.sub(r'\n\s*\n', '\n\n', texto_limpio)
    return texto_limpio.strip()

def extraer_cuerpo(mensaje):
    """
    Extrae el cuerpo del mensaje priorizando texto plano. Si no existe, sanitiza el HTML.
    Como última contingencia, fuerza la lectura en bruto ignorando roturas del estándar MIME.
    """
    cuerpo_texto = ""
    cuerpo_html = ""

    # Intento 1: Lectura estándar respetando la estructura MIME
    if mensaje.is_multipart():
        for parte in mensaje.walk():
            tipo_contenido = parte.get_content_type()
            disposicion = str(parte.get("Content-Disposition"))
            
            if "attachment" not in disposicion:
                if tipo_contenido == "text/plain":
                    payload = parte.get_payload(decode=True)
                    charset = parte.get_content_charset()
                    cuerpo_texto = decodificar_seguro(payload, charset)
                elif tipo_contenido == "text/html":
                    payload = parte.get_payload(decode=True)
                    charset = parte.get_content_charset()
                    cuerpo_html = decodificar_seguro(payload, charset)
    else:
        tipo_contenido = mensaje.get_content_type()
        if tipo_contenido == "text/plain":
            payload = mensaje.get_payload(decode=True)
            charset = mensaje.get_content_charset()
            cuerpo_texto = decodificar_seguro(payload, charset)
        elif tipo_contenido == "text/html":
            payload = mensaje.get_payload(decode=True)
            charset = mensaje.get_content_charset()
            cuerpo_html = decodificar_seguro(payload, charset)

    # 1. Priorizamos siempre la versión de texto plano si está disponible
    if cuerpo_texto.strip():
        return cuerpo_texto
    
    # 2. Si solo hay HTML, lo procesamos para extraer el texto legible
    elif cuerpo_html.strip():
        return sanitizar_html(cuerpo_html)
        
    # 3. CONTINGENCIA: Recuperación forzada para correos con estructura MIME corrompida
    try:
        raw_payload = str(mensaje)
        # Separamos el cuerpo de los encabezados cortando en el primer salto doble
        if "\n\n" in raw_payload:
            cuerpo_crudo = raw_payload.split("\n\n", 1)[1]
        else:
            cuerpo_crudo = raw_payload
            
        texto_limpio = sanitizar_html(cuerpo_crudo)
        
        if texto_limpio.strip():
            return "[RECUPERACIÓN FORZADA - ESTRUCTURA ROTA]\n\n" + texto_limpio.strip()
    except Exception:
        pass

    return "[Texto plano/HTML no encontrado o contiene formato no soportado]"

def procesar_archivo_mbox(ruta_mbox, carpeta_salida):
    """
    Abre un archivo histórico .mbox/.mbx, itera sobre sus correos y los exporta 
    como archivos .txt independientes (fragmentación atómica).
    """
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    print(f"\nAbriendo archivo: {ruta_mbox}...")
    caja_correos = mailbox.mbox(ruta_mbox)
    total_correos = len(caja_correos)
    
    print(f"Se encontraron {total_correos} correos. Iniciando extracción...\n")

    correos_procesados = 0
    prefijo_archivo = os.path.splitext(os.path.basename(ruta_mbox))[0]

    for i, mensaje in enumerate(caja_correos):
        fecha = limpiar_metadato(mensaje['Date'])
        emisor = limpiar_metadato(mensaje['From'])
        receptor = limpiar_metadato(mensaje['To'])
        asunto = limpiar_metadato(mensaje['Subject'])
        cuerpo = extraer_cuerpo(mensaje)

        contenido_final = f"Fecha: {fecha}\nDe: {emisor}\nPara: {receptor}\nAsunto: {asunto}\n\n{cuerpo.strip()}"

        nombre_archivo = f"{prefijo_archivo}_{i+1:04d}.txt"
        ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_final)
            
        correos_procesados += 1
        
        if correos_procesados % 100 == 0:
            print(f"Procesados {correos_procesados} de {total_correos}...")

    print(f"\n✅ ¡Extracción completada para {os.path.basename(ruta_mbox)}! Se generaron {correos_procesados} archivos en '{carpeta_salida}'.")

# ==========================================
# RUTINA DE EJECUCIÓN PRINCIPAL
# ==========================================
def main():
    """
    Despliega la interfaz de consola, detecta archivos compatibles en el 
    directorio de trabajo y gestiona la interacción del usuario.
    """
    print("==================================================")
    print(" 📁 ARQUEOMBOX - EXTRACCIÓN DE ARCHIVOS .MBOX/MBX ")
    print("==================================================")

    directorio_script = os.path.dirname(os.path.abspath(__file__))
    carpeta_destino = os.path.join(directorio_script, "corpus_limpio")

    archivos_en_carpeta = os.listdir(directorio_script)
    archivos_mbox = [f for f in archivos_en_carpeta if f.lower().endswith('.mbox') or f.lower().endswith('.mbx')]

    if not archivos_mbox:
        print(f"\n❌ Python buscó en la ruta estricta: {directorio_script}")
        print("Pero no encontró ningún archivo terminado en '.mbox' o '.mbx'.")
        return

    print(f"\n🔍 Se encontraron {len(archivos_mbox)} archivo(s) .mbox/.mbx:")
    for i, archivo in enumerate(archivos_mbox):
        print(f"  [{i + 1}] {archivo}")

    print("\n¿Qué deseás hacer?")
    print("  [Número] Procesar un archivo específico (ej: 1)")
    print("  [T]      Procesar TODOS los archivos de la lista")
    print("  [C]      Cancelar y salir")
    
    opcion = input("\nIngresá tu opción: ").strip().lower()

    if opcion == 'c':
        print("\nOperación cancelada. ¡Hasta luego!")
        return
    elif opcion == 't':
        print(f"\nIniciando procesamiento en lote de {len(archivos_mbox)} archivos...")
        for archivo in archivos_mbox:
            ruta_completa = os.path.join(directorio_script, archivo)
            procesar_archivo_mbox(ruta_completa, carpeta_destino)
    elif opcion.isdigit() and 1 <= int(opcion) <= len(archivos_mbox):
        archivo_seleccionado = archivos_mbox[int(opcion) - 1]
        print(f"\nHas seleccionado: {archivo_seleccionado}")
        confirmacion = input("¿Confirmar procesamiento? (s/n): ").strip().lower()
        if confirmacion == 's':
            ruta_completa = os.path.join(directorio_script, archivo_seleccionado)
            procesar_archivo_mbox(ruta_completa, carpeta_destino)
        else:
            print("\nProcesamiento cancelado.")
    else:
        print("\n❌ Opción no válida. Saliendo del programa.")

if __name__ == "__main__":
    main()
