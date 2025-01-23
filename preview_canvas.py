import tkinter as tk
from PIL import Image, ImageTk
from utils.math import *
import math
from pygame.math import Vector2

RECT_CONTROL_THICKNESS = 6
LINE_THICKNESS = 4

class PreviewCanvas(tk.Canvas):
    def __init__(self, parent, project, **kwargs):
        super().__init__(parent, **kwargs)
        self.project = project

        self.bind("<Configure>", self._on_configure)
        self.bind("<B1-Motion>", self._on_mouse_drag)

    def _on_configure(self, ev):
        self.reload_preview(self.project)

    def _on_mouse_drag(self, ev):
        if not self.control_edge:
            return
        mouse_pos : Vector2 = Vector2(ev.x, ev.y)
        canvas_size : Vector2 = Vector2(self.winfo_width(), self.winfo_height())
        image_size : Vector2 = Vector2(self.image.width, self.image.height)
        
        # print("==========")
        mouse_pos_img_x = mouse_pos.x - math.floor(canvas_size.x / 2) + math.floor(image_size.x / 2)
        mouse_pos_img_y = mouse_pos.y - math.floor(canvas_size.y / 2) + math.floor(image_size.y / 2)
        mouse_pos : Vector2 = Vector2(mouse_pos_img_x, mouse_pos_img_y)
        # print("----------")

        for i, corner in enumerate(self.project.mapping_rect):
            corner_px = corner.elementwise() * image_size
            if (corner_px - mouse_pos).magnitude() < 18.0:
                if i == 0:
                    self.project.mapping_rect.ul = mouse_pos.elementwise() / image_size
                if i == 1:
                    self.project.mapping_rect.ur = mouse_pos.elementwise() / image_size
                if i == 2:
                    self.project.mapping_rect.ll = mouse_pos.elementwise() / image_size
                if i == 3:
                    self.project.mapping_rect.lr = mouse_pos.elementwise() / image_size
                break

        self._redraw_rect_controls()
    
    def _redraw_rect_controls(self):
        self.delete(self.control_edge)

        image_size = Vector2(self.image.width, self.image.height)
        
        ul = self.start + self.project.mapping_rect.ul.elementwise() * image_size
        ur = self.start + self.project.mapping_rect.ur.elementwise() * image_size
        ll = self.start + self.project.mapping_rect.ll.elementwise() * image_size
        lr = self.start + self.project.mapping_rect.lr.elementwise() * image_size

        self.control_edge = self.create_line(
            # upper-left...
            ul.x, ul.y,
            # ...to upper-right...
            ur.x, ur.y,
            # ...to lower-right...
            lr.x, lr.y,
            # ...to lower-left...
            ll.x, ll.y,
            # ...back to upper-left
            ul.x, ul.y,
            width=LINE_THICKNESS,
            fill="blue"
        )

    def reload_preview(self, project):
        self.project = project
        canvas_size = self.winfo_width(), self.winfo_height()
        thumbnail_size = canvas_size[0], canvas_size[1] - (RECT_CONTROL_THICKNESS*3)

        self.image = Image.open(r".\temp\preview.png")
        self.image.thumbnail(thumbnail_size)

        self.start = (Vector2(*canvas_size) / 2) - (Vector2(*self.image.size) / 2)
        self.delete("all")

        self.preview_img = ImageTk.PhotoImage(self.image)
        self.create_image((self.start.x,self.start.y), anchor="nw", image=self.preview_img)

        self.control_edge = None

        if project.show_mapping_rect.get():
            self.control_edge = self.create_line(
                0.0, 0.0,
                0.0, 0.0,
                width=LINE_THICKNESS
            )
            self._redraw_rect_controls()

    def create_circle(self, x, y, r, **kwargs): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.create_oval(x0, y0, x1, y1, **kwargs)

