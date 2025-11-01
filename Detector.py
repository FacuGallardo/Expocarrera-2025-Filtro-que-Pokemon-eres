import cv2
import time

from componentes.deteccion_rostros import cargar_cascade, detectar_rostros
from componentes.superposicion import overlay_image_fade, pokemon_for_face
from componentes.interfaz import draw_button, draw_countdown, draw_pokemon_name
from componentes.utilidades import cargar_imagenes_pokemon
from componentes.confeti import generar_confeti, animar_confeti, dibujar_confeti

# === Inicialización ===
face_cascade = cargar_cascade()
pokemons_dir = "Pokemon"
pokemon_imgs, pokemon_nombres = cargar_imagenes_pokemon(pokemons_dir)

frame_final = None
foto_tomada = False
inicio = None
DURACION = 5

boton_reiniciar   = (50, 650, 150, 50)
boton_guardar     = (250, 650, 150, 50)
boton_actualizar  = (450, 650, 150, 50)

pokemon_actuales = {}
confeti_coords = []
confeti_anim = 0
fadein_frames = 15

def click_event(event, x, y, flags, param):
    global inicio, foto_tomada, frame_final, pokemon_actuales, confeti_coords, confeti_anim
    if event == cv2.EVENT_LBUTTONDOWN:
        bx, by, bw, bh = boton_reiniciar
        bx2, by2, bw2, bh2 = boton_guardar
        bx3, by3, bw3, bh3 = boton_actualizar
        if bx <= x <= bx+bw and by <= y <= by+bh:
            inicio = None
            foto_tomada = False
            frame_final = None
            pokemon_actuales = {}
            confeti_coords = []
            confeti_anim = 0
            print("Reiniciado")
        elif foto_tomada and bx2 <= x <= bx2+bw2 and by2 <= y <= by2+bh2:
            if frame_final is not None:
                nombre_archivo = f"foto_pokemon_{int(time.time())}.png"
                cv2.imwrite(nombre_archivo, frame_final)
                print(f"Foto guardada como {nombre_archivo}")
        elif foto_tomada and bx3 <= x <= bx3+bw3 and by3 <= y <= by3+bh3:
            inicio = time.time()
            foto_tomada = False
            print("Actualizar presionado")

cv2.namedWindow("Pokemon filtro estilo TikTok", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Pokemon filtro estilo TikTok", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback("Pokemon filtro estilo TikTok", click_event)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detectar_rostros(face_cascade, gray)
    faces = faces[:4]

    fade_alpha = 1.0
    if inicio and not foto_tomada:
        frames_passed = int((time.time() - inicio) * 30)
        fade_alpha = min(1.0, frames_passed / fadein_frames)

    for i, rect in enumerate(faces):
        if i not in pokemon_actuales or not foto_tomada:
            idx, img, nombre = pokemon_for_face(rect, pokemon_imgs, pokemon_nombres)
            pokemon_actuales[i] = (img, nombre)
        x, y, w, h = rect
        px, py = x, y - h
        img, nombre = pokemon_actuales[i]
        if px >= 0 and py >= 0 and px+w <= frame.shape[1] and py+h <= frame.shape[0]:
            if not foto_tomada:
                frame = overlay_image_fade(frame, img, px, py, w, h, alpha=fade_alpha)
            else:
                frame = overlay_image_fade(frame, img, px, py, w, h, alpha=1.0)
            draw_pokemon_name(frame, nombre, px, py, w)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    if len(faces) > 0 and not inicio:
        inicio = time.time()

    if inicio and not foto_tomada:
        segundos_restantes = max(0, int(DURACION - (time.time() - inicio)))
        if segundos_restantes > 0:
            draw_countdown(frame, segundos_restantes)

    if inicio and not foto_tomada and (time.time() - inicio >= DURACION):
        frame_final = frame.copy()
        foto_tomada = True
        confeti_coords = generar_confeti(frame_final, cantidad=150)
        confeti_anim = 0

    if foto_tomada and frame_final is not None:
        frame = frame_final.copy()
        if confeti_anim < 60:
            animar_confeti(confeti_coords, frame.shape)
            dibujar_confeti(frame, confeti_coords)
            confeti_anim += 1

    if len(faces) > 0:
        texto = "Que Pokemon eres:"
        font = cv2.FONT_HERSHEY_SIMPLEX
        escala = 1.5
        grosor = 3
        (ancho_texto, alto_texto), _ = cv2.getTextSize(texto, font, escala, grosor)
        x_texto = (frame.shape[1] - ancho_texto) // 2
        y_texto = 50
        cv2.putText(frame, texto, (x_texto, y_texto), font, escala, (0,255,255), grosor)

    draw_button(frame, boton_reiniciar, "Reiniciar", (0,0,255))
    draw_button(frame, boton_guardar, "Guardar", (0,128,0))

    cv2.imshow("Pokemon filtro estilo TikTok", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()