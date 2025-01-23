import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
import toml
from utils.project import Project
from utils.config import load_config
from utils.math import Rect2

from texify import create_image
from preview_canvas import PreviewCanvas

from scout import get_path

class EvaluationApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Evaluation App")

        self.config = load_config() 
        self.project = Project()

        self.updaters = []

        # Initialize GUI
        self._init_gui()

        # Load default project, if configured
        startup_project_path = self.config.get("startup_project")

        if startup_project_path:
            self.project.load(startup_project_path)
            self._update_all()

        self.root.mainloop()

    def _load_project(self):
        """Load settings from a TOML project file."""
        load_path = filedialog.askopenfilename(
            filetypes=[("TOML files", "*.toml")],
            initialdir=self.config["saveload_initialdir"],
            title="Load project file..."
        )
        if load_path:
            self.project.load(load_path)
            self._update_all()

    def _save_project(self):
        """Save current settings to a TOML project file."""
        save_path = filedialog.asksaveasfilename(
            defaultextension=".toml",
            initialdir=self.config["saveload_initialdir"],
            filetypes=[("TOML files", "*.toml")],
            title="Save project file..."
        )
        if save_path:
            self.project.save(save_path)

    def _select_file(self, variable, initialdir=None, filetypes=[("Any file", "*")], title="Select file"):
        """Generalized file selection method."""
        filepath = filedialog.askopenfilename(
            initialdir=initialdir, title=title, filetypes=filetypes
        )
        if filepath:  # Set only if a valid file is selected
            variable.set(filepath)

    def _create_input_file_frame(self, parent, display_name, variable, initialdir=None, filetypes=None):
        frame = ttk.Frame(parent)
        frame.columnconfigure(1, weight=1)  # Make entry stretchable

        ttk.Label(frame, text=f"{display_name}:").grid(row=0, column=0, sticky="e", padx=5)
        
        entry = ttk.Entry(frame, textvariable=variable)
        entry.grid(row=0, column=1, sticky="ew", padx=5)
        
        ttk.Button(frame, text="...", command=lambda: self._select_file(
            variable, initialdir=initialdir, filetypes=filetypes, title=f"Select {display_name.lower()}..."
        )).grid(row=0, column=2, padx=5)
        
        return frame

    def _create_scale_frame(self, parent, display_name, variable, from_=0.0, to=0.0):
        frame = ttk.Frame(parent)
        frame.columnconfigure(2, weight=1)  # Make scale stretchable

        ttk.Label(frame, text=f"{display_name}:").grid(row=0, column=0, sticky="e", padx=5)

        value_label = ttk.Label(frame, text=f"{variable.get()}")
        value_label.grid(row=0, column=1, sticky="e", padx=5)

        scale_update = lambda _: value_label.configure(text=f"{variable.get()}")
        
        scale = ttk.Scale(frame, orient="horizontal", variable=variable, command=scale_update)
        self.updaters.append(scale_update)
        scale["from"] = from_
        scale["to"] = to
        scale.grid(row=0, column=2, sticky="ew", padx=5)

        return frame

    def _init_gui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        config_frame = ttk.Frame(main_frame, padding=10, relief="raised")
        config_frame.grid(sticky="n", row=0, column=0) # iack(fill="both", expand=True)

        loadsave_frame = ttk.Frame(config_frame, padding=5)
        ttk.Button(loadsave_frame, text="Load project...", command=self._load_project).grid(column=0, row=0)
        ttk.Button(loadsave_frame, text="Save project...", command=self._save_project).grid(column=1, row=0)
        loadsave_frame.pack(fill="x")

        # Input frames
        trace_frame = self._create_input_file_frame(
            config_frame,
            "Trace file",
            self.project.trace_file,
            initialdir=self.config["trace_initialdir"],
            filetypes=[("Trace file", "*.csv")]
        )
        trace_frame.pack(fill="x", pady=5)

        sensor_frame = self._create_input_file_frame(
            config_frame,
            "Sensor measurement file",
            self.project.sensor_file,
            initialdir=self.config["sensor_initialdir"],
            filetypes=[("Sensor measurement file", "*.csv")]
        )
        sensor_frame.pack(fill="x", pady=5)

        bgimg_frame = self._create_input_file_frame(
            config_frame,
            "Background image file",
            self.project.background_image_file,
            initialdir=self.config["background_image_initialdir"],
            filetypes=[("Background image", "*.png;*.jpg;*jpeg")]
        )
        bgimg_frame.pack(fill="x", pady=5)

        ttk.Separator(config_frame, orient="horizontal").pack(fill="x", pady=10)

    #   def _create_scale_frame(self, parent, display_name, variable, from_=0.0, to=0.0):
        begin_index_frame = self._create_scale_frame(config_frame, "Begin index (sensor)", self.project.begin_index, from_=1800, to=2400)
        begin_index_frame.pack(fill="x", pady=5)

        ttk.Button(config_frame, text="Show graphs", command=self._show_graphs).pack(anchor="n", fill="x")

        # def _create_scale_frame(self, parent, display_name, variable, from_=0.0, to=0.0):
        ttk.Separator(config_frame, orient="horizontal").pack(fill="x", pady=10)

        ttk.Checkbutton(config_frame, text="Show mapping rect", variable=self.project.show_mapping_rect, command=lambda: self.preview_canvas.reload_preview(self.project)).pack(anchor="n")
        ttk.Button(config_frame, text="Reset mapping rect", command=self._reset_mapping_rect).pack(anchor="n", fill="x")

        # Separator
        ttk.Separator(config_frame, orient="horizontal").pack(fill="x", pady=10)

        preview_button = ttk.Button(config_frame, text="Update preview", command=self._update_preview)
        preview_button.pack(anchor="n", fill="x")

        ttk.Separator(config_frame, orient="horizontal").pack(fill="x", pady=10)

        self.preview_canvas = PreviewCanvas(main_frame, self.project) #, bg="red")
        self.preview_canvas.grid(row=0, column=1, sticky="news")

    def _update_all(self):
        for updater in self.updaters:
            updater(0)
        self._update_preview()

    def _update_preview(self):
        if create_image(self.project, get_path(self.project)):
            self.preview_canvas.reload_preview(self.project)

    def _reset_mapping_rect(self):
        self.project.mapping_rect = Rect2()
        self.preview_canvas.reload_preview(self.project)

    def _show_graphs(self):
        print("show graphs")
        print(self.project.sensor_file.get())

