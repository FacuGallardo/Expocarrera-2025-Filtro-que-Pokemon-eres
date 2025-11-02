import os
import cv2
import re

def cargar_imagenes_pokemon(pokemons_dir):
    pokemon_imgs = []
    pokemon_nombres = []
    if not os.path.isdir(pokemons_dir):
        print(f"[utilidades] Directorio no existe: {pokemons_dir}")
        return pokemon_imgs, pokemon_nombres

    for fname in sorted(os.listdir(pokemons_dir)):
        if fname.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(pokemons_dir, fname)
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # intentar conservar alfa si existe
            if img is None:
                print(f"[utilidades] Advertencia: no se pudo cargar '{fname}', se omite.")
                continue
            if getattr(img, "size", 0) == 0:
                print(f"[utilidades] Advertencia: imagen vacía '{fname}', se omite.")
                continue
            # Normalizar nombre a partir del nombre de archivo:
            base = os.path.splitext(fname)[0]
            base = base.replace('_', ' ').strip()
            # Quitar prefijos numéricos tipo "001 - " o "001."
            base = re.sub(r'^[0-9]+[\s\-\._]*', '', base)
            nombre = base
            pokemon_imgs.append(img)
            pokemon_nombres.append(nombre)
    if len(pokemon_imgs) == 0:
        print("[utilidades] Atención: no se cargó ninguna imagen de Pokémon.")
    return pokemon_imgs, pokemon_nombres