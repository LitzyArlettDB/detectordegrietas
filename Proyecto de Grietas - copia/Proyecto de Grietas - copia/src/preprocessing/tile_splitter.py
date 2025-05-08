import cv2
import os
import ntpath

def dividir_en_tiles(ruta_imagen, salida_dir, tile_size=1024):
    """
    Divide una imagen en bloques de tamaño fijo.
    Si un bloque es incompleto, se rellena con negro hasta completar el tamaño.
    """
    os.makedirs(salida_dir, exist_ok=True)

    imagen = cv2.imread(ruta_imagen, cv2.IMREAD_UNCHANGED)
    if imagen is None:
        raise ValueError(f"No se pudo cargar la imagen: {ruta_imagen}")

    alto, ancho = imagen.shape[:2]
    canales = imagen.shape[2] if len(imagen.shape) > 2 else 1
    nombre_base = os.path.splitext(ntpath.basename(ruta_imagen))[0]

    conteo = 0
    for y in range(0, alto, tile_size):
        for x in range(0, ancho, tile_size):
            tile = imagen[y:y+tile_size, x:x+tile_size]

            # Rellenar si no tiene tamaño completo
            tile_h, tile_w = tile.shape[:2]
            if tile_h != tile_size or tile_w != tile_size:
                top = 0
                bottom = tile_size - tile_h
                left = 0
                right = tile_size - tile_w

                tile = cv2.copyMakeBorder(
                    tile, top, bottom, left, right,
                    borderType=cv2.BORDER_CONSTANT,
                    value=(0, 0, 0) if canales == 3 else (0, 0, 0, 0)
                )

            nombre_tile = f"{nombre_base}_tile_{conteo}.png"
            ruta_tile = os.path.join(salida_dir, nombre_tile)
            cv2.imwrite(ruta_tile, tile)
            conteo += 1

    print(f"Se guardaron {conteo} bloques (rellenados si fue necesario) en {salida_dir}")

