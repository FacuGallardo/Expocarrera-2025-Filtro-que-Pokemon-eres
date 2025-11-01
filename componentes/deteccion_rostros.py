import cv2

def cargar_cascade():
    return cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detectar_rostros(face_cascade, frame_gray):
    return face_cascade.detectMultiScale(frame_gray, 1.3, 5)