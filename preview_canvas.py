import tkinter as tk

class PreviewCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Configure>", self._on_configure)
        self.bind("<B1-Motion>", self._on_mouse_drag)

    def _on_configure(self, ev):
        print(f"winfo w|{self.winfo_width()} h|{self.winfo_height()}")
        print(f"event w|{ev.width} h|{ev.height}")

    def _on_mouse_drag(self, ev):
        print(f"winfo x|{self.winfo_x()} y|{self.winfo_y()}")
        print(f"event x|{ev.x} y|{ev.y}")

