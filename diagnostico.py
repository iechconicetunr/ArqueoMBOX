import os

def diagnosticar():
    # Obtenemos la ruta donde está guardado este script
    directorio = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "="*50)
    print(" 🕵️ DIAGNÓSTICO DE DIRECTORIO")
    print("="*50)
    print(f"Ruta absoluta que Python está leyendo: \n{directorio}\n")
    print("Archivos encontrados (nombre real a nivel sistema):")
    print("-" * 50)
    
    archivos = os.listdir(directorio)
    
    if not archivos:
        print("¡La carpeta está completamente vacía para Python!")
        return

    for archivo in archivos:
        ruta_completa = os.path.join(directorio, archivo)
        # Solo listamos archivos, ignoramos carpetas como levrero_env
        if os.path.isfile(ruta_completa):
            print(f" -> '{archivo}'")
            
    print("-" * 50 + "\n")

if __name__ == "__main__":
    diagnosticar()
