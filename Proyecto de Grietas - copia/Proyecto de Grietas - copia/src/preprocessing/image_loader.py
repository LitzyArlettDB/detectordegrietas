import os
from PIL import Image
from pillow_heif import register_heif_opener
import ntpath
import cv2

register_heif_opener()

def convertir_heic_a_png(ruta_entrada, carpeta_destino):
    """
    Convierte una imagen HEIC a PNG y guarda una copia en la carpeta destino.
    """
    nombre_base = os.path.splitext(ntpath.basename(ruta_entrada))[0]
    ruta_salida = os.path.join(carpeta_destino, f"{nombre_base}.png")
    
    imagen = Image.open(ruta_entrada)
    imagen.save(ruta_salida, format="PNG")
    
    print(f"[INFO] Convertida {ruta_entrada} a {ruta_salida}")
    return ruta_salida

def decidir_procesamiento(ruta_imagen, carpeta_salida, tile_size=1024):
    """
    Decide si dividir la imagen o procesarla directamente, según su tamaño y tipo.
    """
    extension = os.path.splitext(ruta_imagen)[1].lower()

    # Convertir si es .heic
    if extension == '.heic':
        ruta_imagen = convertir_heic_a_png(ruta_imagen, carpeta_salida)

    # Cargar imagen (con opencv)
    imagen = cv2.imread(ruta_imagen, cv2.IMREAD_UNCHANGED)
    if imagen is None:
        raise ValueError(f"No se pudo cargar la imagen: {ruta_imagen}")

    alto, ancho = imagen.shape[:2]
    print(f"[INFO] Dimensiones de la imagen: {ancho}x{alto}")

    if alto > 2048 or ancho > 2048:
        from src.preprocessing.tile_splitter import dividir_en_tiles
        dividir_en_tiles(ruta_imagen, carpeta_salida, tile_size)
    else:
        # Copiar la imagen tal cual a la carpeta destino
        nombre = os.path.basename(ruta_imagen)
        destino = os.path.join(carpeta_salida, nombre)
        cv2.imwrite(destino, imagen)
        print(f"[INFO] Imagen guardada directamente (no dividida): {destino}")
