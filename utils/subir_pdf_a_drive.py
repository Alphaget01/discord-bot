from googleapiclient.discovery import build
import os

def subir_a_drive(pdf_path, serie):
    # Conectar con Google Drive API
    service = build('drive', 'v3')

    # Subir el archivo a las carpetas de la serie en Google Drive
    # Usar las rutas y IDs desde Firestore
