import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

class CrackDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Grietas Mejorado")
        self.root.geometry("1000x600")
        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.detector = None  # Se asignará desde main

        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Cargar Imagen", command=self.load_image).pack(side=tk.LEFT, padx=10)

        self.process_btn = tk.Button(control_frame, text="Procesar Imagen", command=self.process_image, state=tk.DISABLED)
        self.process_btn.pack(side=tk.LEFT, padx=10)

        # Sliders para umbral inferior y superior
        tk.Label(control_frame, text="Umbral Inferior:").pack(side=tk.LEFT)
        self.lower_thresh = tk.Scale(control_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.lower_thresh.set(50)
        self.lower_thresh.pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Umbral Superior:").pack(side=tk.LEFT)
        self.upper_thresh = tk.Scale(control_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.upper_thresh.set(150)
        self.upper_thresh.pack(side=tk.LEFT, padx=5)

        # Área para mostrar imágenes
        image_frame = tk.Frame(self.root)
        image_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.original_panel = tk.Label(image_frame)
        self.original_panel.pack(side="left", padx=10, expand=True)

        self.processed_panel = tk.Label(image_frame)
        self.processed_panel.pack(side="right", padx=10, expand=True)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if path:
            self.image_path = path
            self.original_image = Image.open(path)
            self.display_image(self.original_image, self.original_panel)
            self.process_btn.config(state=tk.NORMAL)

    def process_image(self):
        if not self.image_path or not self.detector:
            messagebox.showwarning("Advertencia", "Cargue una imagen y asigne un detector")
            return

        try:
            original, processed = self.detector.aplicar_filtro_y_bordes(
                self.image_path,
                self.lower_thresh.get(),
                self.upper_thresh.get()
            )

            # Mostrar imagen procesada
            self.processed_image = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
            self.display_image(self.processed_image, self.processed_panel)

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la imagen: {e}")

    def display_image(self, img, panel):
        img = img.resize((450, 400))
        tk_image = ImageTk.PhotoImage(img)
        panel.img = tk_image  # Evita que la imagen sea eliminada por el recolector
        panel.config(image=tk_image)

# --- Detector actualizado ---
class CrackDetector:
    def aplicar_filtro_y_bordes(self, ruta_imagen, umbral_inferior=50, umbral_superior=150):
        original = cv2.imread(ruta_imagen)
        if original is None:
            raise ValueError("No se pudo cargar la imagen")

        suavizada = cv2.GaussianBlur(original, (5, 5), 0)
        gris = cv2.cvtColor(suavizada, cv2.COLOR_BGR2GRAY)
        bordes = cv2.Canny(gris, umbral_inferior, umbral_superior)
        bordes_bgr = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)

        return original, bordes_bgr

# --- Main ---
def main():
    root = tk.Tk()
    app = CrackDetectionGUI(root)
    app.detector = CrackDetector()
    root.mainloop()

if __name__ == "__main__":
    main()
