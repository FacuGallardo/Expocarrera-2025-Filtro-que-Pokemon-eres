import cv2
import hashlib

def overlay_image_fade(bg, fg, x, y, w, h, alpha=1.0):
    fg = cv2.resize(fg, (w, h))
    if fg.shape[2] == 3:
        fg = cv2.cvtColor(fg, cv2.COLOR_BGR2BGRA)
    roi = bg[y:y+h, x:x+w]
    if roi.shape[2] == 3:
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2BGRA)
    blended = cv2.addWeighted(roi, 1-alpha, fg, alpha, 0)
    bg[y:y+h, x:x+w] = blended[:, :, :3]
    return bg

def pokemon_for_face(rect, pokemon_imgs, pokemon_nombres):
    x, y, w, h = rect
    hsh = hashlib.sha256(f"{x}{y}{w}{h}".encode()).hexdigest()
    idx = int(hsh, 16) % len(pokemon_imgs)
    return idx, pokemon_imgs[idx], pokemon_nombres[idx]