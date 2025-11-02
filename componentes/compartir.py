import os
import time
import cv2
import qrcode
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def guardar_foto(frame):
    carpeta = "fotos"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    nombre_archivo = os.path.join(carpeta, f"foto_pokemon_{int(time.time())}.png")
    cv2.imwrite(nombre_archivo, frame)
    return nombre_archivo

def subir_a_drive(nombre_archivo):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Abre navegador la primera vez para autorizar
    drive = GoogleDrive(gauth)
    file_drive = drive.CreateFile({'title': os.path.basename(nombre_archivo)})
    file_drive.SetContentFile(nombre_archivo)
    file_drive.Upload()
    file_drive.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    return file_drive['alternateLink']  # URL pública

def generar_qr(url, nombre_archivo_qr):
    img = qrcode.make(url)
    img.save(nombre_archivo_qr)

def mostrar_qr(nombre_archivo_qr):
    qr_img = cv2.imread(nombre_archivo_qr)
    if qr_img is None:
        print(f"[ERROR] No se pudo leer el QR: {nombre_archivo_qr}")
        return
    cv2.imshow("Escanea tu foto", qr_img)
    cv2.waitKey(0)
    cv2.destroyWindow("Escanea tu foto")