import random
import cv2

def generar_confeti(frame, cantidad=150):
    coords = []
    for _ in range(cantidad):
        x = random.randint(0, frame.shape[1]-1)
        y = random.randint(0, frame.shape[0]-1)
        color = tuple([random.randint(0,255) for _ in range(3)])
        radius = random.randint(3, 7)
        coords.append([x, y, color, radius, random.randint(2,6)])
    return coords

def animar_confeti(coords, frame_shape):
    for c in coords:
        c[1] += c[4]
        if c[1] > frame_shape[0]:
            c[1] = random.randint(-20, 0)
            c[0] = random.randint(0, frame_shape[1]-1)

def dibujar_confeti(frame, coords):
    for x, y, color, radius, _ in coords:
        cv2.circle(frame, (int(x), int(y)), radius, color, -1)