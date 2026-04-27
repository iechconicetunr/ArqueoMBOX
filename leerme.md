# ArqueoMBOX - Extractor y Sanitizador para Archivos Históricos

*[Read this documentation in English](readme.md)*

Este repositorio contiene **ArqueoMBOX**, una herramienta desarrollada en Python para la extracción robusta, limpieza y fragmentación atómica de correos electrónicos históricos almacenados en formatos `.mbox` y `.mbx`. 

Esta herramienta forma parte del Proyecto de Investigación Orientada (IO 2025) financiado por el **Gobierno de la Provincia de Santa Fe**, Argentina. El desarrollo fue llevado a cabo por el **Laboratorio de Humanidades Digitales (LHD) del IECH (UNR/CONICET)**, enfocado en la integración de Inteligencia Artificial en la descripción archivística para el tratamiento del Fondo Digital Mario Levrero.

*Nota: La creación y el diseño de la arquitectura de este software fueron asistidos por IA mediante el uso de Gemini Pro.*

## 📌 Características Principales

Los formatos históricos de correo presentan múltiples desafíos para su procesamiento mediante Modelos de Lenguaje (LLMs) debido a la alta concentración de ruido informático y estándares obsoletos. Este script soluciona estos problemas mediante:

* **Fragmentación Atómica:** Descompone grandes archivos `.mbox` en archivos `.txt` individuales por cada correo, facilitando el procesamiento iterativo de la IA.
* **Decodificación Políglota:** Integra un sistema de traducción que rescata caracteres del español (tildes, eñes) iterando de forma segura por codificaciones históricas (`latin-1`, `windows-1252`, `iso-8859-1`).
* **Sanitización de HTML:** Utiliza expresiones regulares (`re`) para limpiar correos encapsulados en etiquetas `<x-html>`, extrayendo exclusivamente el texto humanamente legible.
* **Fallback de Emergencia (Recuperación Forzada):** Implementa un mecanismo de contingencia para correos con estructuras MIME severamente corrompidas (ej. exportaciones defectuosas de clientes como *Qualcomm Eudora 5*). Extrae la información a nivel de texto crudo y preserva huellas forenses invaluables.

## ⚙️ Requisitos

La herramienta está diseñada para ser liviana y fácil de implementar. No requiere la instalación de librerías de terceros, ya que utiliza exclusivamente módulos nativos de Python:
* `Python 3.x`
* Librerías nativas empleadas: `mailbox`, `os`, `email`, `re`.

## 🚀 Instrucciones de Uso

1. **Clonar el repositorio** o descargar el archivo `arqueombox.py` en tu equipo local.
2. **Preparar los archivos:** Coloca tus archivos `.mbox` o `.mbx` en la misma carpeta donde se encuentra el script.
3. **Ejecutar la herramienta:** Abre tu terminal o consola de comandos, navega hasta la carpeta del proyecto y ejecuta:

   ```bash
   python3 arqueombox.py

4. **Menú Interactivo:** El programa detectará automáticamente los archivos compatibles en el directorio y te presentará un menú (en español) donde podrás elegir procesar un archivo específico o realizar un procesamiento por lotes de todos los archivos encontrados.

5. **Resultados:** Se generará automáticamente una carpeta llamada corpus_limpio en el mismo directorio. Allí encontrarás todos los correos extraídos como archivos .txt limpios y numerados, listos para ser consumidos por modelos de Inteligencia Artificial o bases de datos relacionales.

👥 Equipo y Créditos

**Desarrollo:** Laboratorio de Humanidades Digitales (LHD) - IECH (UNR/CONICET).

**Financiamiento:** Programa Investigación Orientada 2025 (IO 2025), Gobierno de la Provincia de Santa Fe.

**Asistencia IA:** Generación de código asistida por Gemini Pro.
