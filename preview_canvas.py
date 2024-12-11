import tkinter as tk
from PIL import Image, ImageTk
from utils.math import *

RECT_CONTROL_THICKNESS = 10
LINE_THICKNESS = 8

class PreviewCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.mapping_rect = Rect2(
            Vector2(0.0, 0.0), # upper left
            Vector2(1.0, 0.0), # upper right
            Vector2(0.0, 1.0), # lower left
            Vector2(1.0, 1.0) # lower right
        )

        self.bind("<Configure>", self._on_configure)
        self.bind("<B1-Motion>", self._on_mouse_drag)

    def _on_configure(self, ev):
        print(f"winfo w|{self.winfo_width()} h|{self.winfo_height()}")
        print(f"event w|{ev.width} h|{ev.height}")

        self.reload_preview()

    def _on_mouse_drag(self, ev):
        print(f"winfo x|{self.winfo_x()} y|{self.winfo_y()}")
        print(f"event x|{ev.x} y|{ev.y}")

    def reload_preview(self):
        canvas_size = self.winfo_width(), self.winfo_height()
        thumbnail_size = canvas_size[0], canvas_size[1] - (RECT_CONTROL_THICKNESS*3)

        self.image = Image.open(r".\temp\preview.png")
        self.image.thumbnail(thumbnail_size)

        self.start_x = (canvas_size[0] / 2) - (self.image.width / 2)
        self.start_y = (canvas_size[1] / 2) - (self.image.height / 2)
        # self.configure(width=self.image.width, height=self.image.height)
        self.delete("all")

        self.preview_img = ImageTk.PhotoImage(self.image)
        self.create_image((self.start_x,self.start_y), anchor="nw", image=self.preview_img)

        ul_x = self.start_x + self.mapping_rect.ul.x * int(self.image.width)
        ul_y = self.start_y + self.mapping_rect.ul.y * int(self.image.height)

        ur_x = self.start_x + self.mapping_rect.ur.x * int(self.image.width)
        ur_y = self.start_y + self.mapping_rect.ur.y * int(self.image.height)

        ll_x = self.start_x + self.mapping_rect.ll.x * int(self.image.width)
        ll_y = self.start_y + self.mapping_rect.ll.y * int(self.image.height)

        lr_x = self.start_x + self.mapping_rect.lr.x * int(self.image.width)
        lr_y = self.start_y + self.mapping_rect.lr.y * int(self.image.height)

        self.create_line(
            # upper-left...
            ul_x, ul_y,
            # ...to upper-right...
            ur_x, ur_y,
            # ...to lower-right...
            lr_x, lr_y,
            # ...to lower-left...
            ll_x, ll_y,
            # ...back to upper-left
            ul_x, ul_y,
            width=LINE_THICKNESS
        )

        self.create_circle(ul_x, ul_y, RECT_CONTROL_THICKNESS, fill="aqua")
        self.create_circle(ur_x, ur_y, RECT_CONTROL_THICKNESS, fill="aqua")
        self.create_circle(ll_x, ll_y, RECT_CONTROL_THICKNESS, fill="aqua")
        self.create_circle(lr_x, lr_y, RECT_CONTROL_THICKNESS, fill="aqua")

    def create_circle(self, x, y, r, **kwargs): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.create_oval(x0, y0, x1, y1, **kwargs)

