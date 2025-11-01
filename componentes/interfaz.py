import cv2

def draw_button(img, rect, text, color):
    x, y, w, h = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
    font_scale = 0.9
    thickness = 2
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2
    cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255,255,255), thickness)

def draw_countdown(frame, segundos_restantes):
    texto = f"{segundos_restantes}"
    font = cv2.FONT_HERSHEY_DUPLEX
    escala = 4
    grosor = 8
    colores = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
    color = colores[segundos_restantes % len(colores)]
    (ancho_texto, alto_texto), _ = cv2.getTextSize(texto, font, escala, grosor)
    x = (frame.shape[1] - ancho_texto) // 2
    y = (frame.shape[0] + alto_texto) // 2
    cv2.putText(frame, texto, (x, y), font, escala, color, grosor, cv2.LINE_AA)

def draw_pokemon_name(frame, nombre, px, py, w):
    (text_w, text_h), _ = cv2.getTextSize(nombre, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    overlay = frame.copy()
    cv2.rectangle(overlay, (px, py-40), (px+text_w+10, py-10), (0,0,0), -1)
    alpha = 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.putText(frame, nombre, (px+5, py-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)