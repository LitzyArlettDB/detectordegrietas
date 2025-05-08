from preprocessing.edge_detector import aplicar_filtro_y_bordes
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from src.preprocessing.image_loader import decidir_procesamiento



def seleccionar_y_procesar():
    # Ventana oculta
    root = tk.Tk()
    root.withdraw()

    archivo = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.tif *.tiff *.heic")]
    )

    if not archivo:
        messagebox.showinfo("Cancelado", "No se seleccionó ninguna imagen.")
        return

    nombre_base = os.path.splitext(os.path.basename(archivo))[0]
    carpeta_destino = os.path.join("data/results/files", nombre_base)
    os.makedirs(carpeta_destino, exist_ok=True)

    try:
        # Procesamiento original
        decidir_procesamiento(archivo, carpeta_destino)

        # Aplicar detección de bordes
        ruta_bordes = aplicar_filtro_y_bordes(archivo, carpeta_destino)

        # Mostrar imagen en ventana nueva
        mostrar_imagen_bordes(ruta_bordes)

        messagebox.showinfo("Éxito", f"Imagen procesada y con bordes guardada en:\n{carpeta_destino}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un problema:\n{str(e)}")

def mostrar_imagen_bordes(ruta_imagen):
    ventana = tk.Toplevel()
    ventana.title("Imagen con bordes")

    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)

    etiqueta = tk.Label(ventana, image=imagen)
    etiqueta.image = imagen  # Evitar recolección de basura
    etiqueta.pack()
