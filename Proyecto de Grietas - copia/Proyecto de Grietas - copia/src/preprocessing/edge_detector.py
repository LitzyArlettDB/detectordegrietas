import cv2

class CrackDetector:
    def aplicar_filtro_y_bordes(self, ruta_imagen, umbral1=50, umbral2=150):
        original = cv2.imread(ruta_imagen)
        if original is None:
            raise ValueError("No se pudo cargar la imagen")

        suavizada = cv2.GaussianBlur(original, (5, 5), 0)
        gris = cv2.cvtColor(suavizada, cv2.COLOR_BGR2GRAY)
        bordes = cv2.Canny(gris, umbral1, umbral2)
        bordes_bgr = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)

        return original, bordes_bgr
