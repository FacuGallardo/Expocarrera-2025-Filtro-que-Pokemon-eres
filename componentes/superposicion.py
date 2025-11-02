import cv2
import hashlib

def overlay_image_fade(bg, fg, x, y, w, h, alpha=1.0):
    # Validaciones básicas
    if fg is None:
        return bg
    try:
        if fg.size == 0:
            return bg
    except Exception:
        return bg

    # Comprobar límites del ROI en el fondo
    bh, bw = bg.shape[:2]
    if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > bw or y + h > bh:
        return bg

    # Intentar redimensionar con manejo de errores
    try:
        fg_resized = cv2.resize(fg, (w, h))
    except Exception as e:
        print(f"[superposicion] Error al redimensionar fg: {e}")
        return bg

    # Asegurar que ambas ROI tienen 4 canales (BGRA) para blend
    if fg_resized.ndim == 3 and fg_resized.shape[2] == 3:
        fg_resized = cv2.cvtColor(fg_resized, cv2.COLOR_BGR2BGRA)
    elif fg_resized.ndim == 2:
        fg_resized = cv2.cvtColor(fg_resized, cv2.COLOR_GRAY2BGRA)

    roi = bg[y:y+h, x:x+w]
    if roi.ndim == 2:
        roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGRA)
    elif roi.ndim == 3 and roi.shape[2] == 3:
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2BGRA)

    # Asegurar tamaños coincidentes (por si hay desajuste)
    if roi.shape[:2] != fg_resized.shape[:2]:
        fg_resized = cv2.resize(fg_resized, (roi.shape[1], roi.shape[0]))

    try:
        blended = cv2.addWeighted(roi, 1.0 - alpha, fg_resized, alpha, 0)
        bg[y:y+h, x:x+w] = blended[:, :, :3]
    except Exception as e:
        print(f"[superposicion] Error al mezclar imágenes: {e}")
        return bg

    return bg

def pokemon_for_face(rect, pokemon_imgs, pokemon_nombres):
    x, y, w, h = rect
    if not pokemon_imgs or len(pokemon_imgs) == 0:
        # Retornar un placeholder seguro si no hay imágenes cargadas
        return 0, None, "Desconocido"
    hsh = hashlib.sha256(f"{x}{y}{w}{h}".encode()).hexdigest()
    idx = int(hsh, 16) % len(pokemon_imgs)
    nombre = pokemon_nombres[idx] if idx < len(pokemon_nombres) else "Desconocido"
    return idx, pokemon_imgs[idx], nombre