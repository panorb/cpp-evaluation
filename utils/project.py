import tkinter as tk
import tomllib

class Project:
    def __init__(self):
        # Input files
        self.trace_file = tk.StringVar()
        self.sensor_file = tk.StringVar()
        self.background_image_file = tk.StringVar()
        self.path_rotation = tk.DoubleVar()

    def save(self, filename):
        with open(filename, mode='w+') as file:
            file.write(
f"""[input_files]
# This section contains all the file paths in use
trace_file = "{self.trace_file.get()}"
sensor_file = "{self.sensor_file.get()}"
background_image_file = "{self.background_image_file.get()}"

[transformation]
# This section contains transformations applied to the input data
path_rotation = {self.path_rotation.get():.2f}
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
            self._set_setting(self.path_rotation, transformation_section.get("path_rotation"))


