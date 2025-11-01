import os
import cv2

def cargar_imagenes_pokemon(pokemons_dir):
    pokemon_imgs = []
    pokemon_nombres = []
    for fname in sorted(os.listdir(pokemons_dir)):
        if fname.endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(pokemons_dir, fname)
            img = cv2.imread(path)
            pokemon_imgs.append(img)
            nombre = os.path.splitext(fname)[0]
            pokemon_nombres.append(nombre)
    return pokemon_imgs, pokemon_nombres