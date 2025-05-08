import tkinter as tk
from src.gui.crack_detection_gui import CrackDetectionGUI
from src.preprocessing.edge_detector import CrackDetector

def main():
    root = tk.Tk()
    detector = CrackDetector()
    app = CrackDetectionGUI(root)
    app.detector = detector
    root.mainloop()

if __name__ == "__main__":
    main()
