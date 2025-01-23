import tkinter as tk
import tomllib
from .math import Rect2
from pygame.math import Vector2

class Project:
    def __init__(self):
        # Input files
        self.trace_file = tk.StringVar()
        self.sensor_file = tk.StringVar()
        self.background_image_file = tk.StringVar()
        self.mapping_rect = Rect2()
        self.show_mapping_rect = tk.BooleanVar(value=True)
        self.begin_index = tk.IntVar(value=0)

    def save(self, filename):
        with open(filename, mode='w+') as file:
            file.write(
f"""[input_files]
# This section contains all the file paths in use
trace_file = "{self.trace_file.get()}"
sensor_file = "{self.sensor_file.get()}"
background_image_file = "{self.background_image_file.get()}"

[display]
show_mapping_rect = {str(self.show_mapping_rect.get()).lower()}

[transformation]
# This section contains transformations applied to the input data
begin_index = {self.begin_index.get()}
upper_left = {{ x = {self.mapping_rect.ul.x:.2f}, y = {self.mapping_rect.ul.y:.2f} }}
upper_right = {{ x = {self.mapping_rect.ur.x:.2f}, y = {self.mapping_rect.ur.y:.2f} }}
lower_left = {{ x = {self.mapping_rect.ll.x:.2f}, y = {self.mapping_rect.ll.y:.2f} }}
lower_right = {{ x = {self.mapping_rect.lr.x:.2f}, y = {self.mapping_rect.lr.y:.2f} }}
""" 
            )

    def _set_setting(self, variable, value):
        if value:
            variable.set(value)

    def load(self, filename):
        with open(filename, mode='rb') as file:
            data = tomllib.load(file)

            # Read input file section
            input_section = data.get("input_files", {})
            self._set_setting(self.trace_file, input_section.get("trace_file")) 
            self._set_setting(self.sensor_file, input_section.get("sensor_file"))
            self._set_setting(self.background_image_file, input_section.get("background_image_file"))

            transformation_section = data.get("transformation", {})
            self._set_setting(self.begin_index, transformation_section.get("begin_index"))
            self._set_setting(self.mapping_rect, transformation_section)

            display_section = data.get("display", {})
            self._set_setting(self.show_mapping_rect, display_section.get("show_mapping_rect"))



