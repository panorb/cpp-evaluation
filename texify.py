from shutil import rmtree
from distutils.dir_util import copy_tree
import subprocess
from pathlib import Path
from pygame.math import Vector2
import numpy as np
import cv2
import sys
import math
import matplotlib.cm as cm
import pandas as pd

from scout import sync_values

def _transform_points(project, data):
    src_points = np.array([
        [0, 1],    # Bottom-left
        [1, 1],     # Bottom-right
        [0, 0],    # Upper-left
        [1, 0],    # Upper-right
    ], dtype=np.float32)
    dst_points = project.mapping_rect.to_numpy_array()
    
    transform_matrix = cv2.getPerspectiveTransform(dst_points, src_points)
    transform_matrix = np.linalg.inv(transform_matrix)

    x_trans = []
    y_trans = []

    for i, row in data.iterrows():
        transformed_point = np.dot(transform_matrix, [row["X_Norm"], row["Y_Norm"], 1])  # Use homogeneous coordinates
        transformed_point /= transformed_point[2]       # Normalize by the last coordinate

        x_trans.append(transformed_point[0])
        y_trans.append(1-transformed_point[1])

        # print("=====")
        # print(f"Original point: ({pt.x:.3f}, {pt.y:.3f})")
        # print(f"Transformed point: ({transformed_point[0]:.3f}, {transformed_point[1]:.3f})")
        # print("=====")

    data["X_Trans"] = x_trans
    data["Y_Trans"] = y_trans

    print(data.tail())
    data.to_csv("woah.csv")

    return data

def _render_points(data):
    min_distance = data["Distance"].min()
    max_distance = data["Distance"].max()

    res = ""
    # for point in points[::30]:
    # res = "\draw[draw={rgb,255:red,21; green,66; blue,128},line width=10pt] "

    pt_tex = []

    for i, row in data.iterrows():
        dist = row["Distance"]
        dist_norm = (dist - min_distance) / (max_distance - min_distance)
        color = cm.hot(dist_norm)
        red_p = int(color[0] * 255)
        green_p = int(color[1] * 255)
        blue_p = int(color[2] * 255)

        tex = f"\\fill[fill={{rgb,255:red,{red_p}; green,{green_p}; blue,{blue_p}}}] ({row['X_Trans']:.3f},{row['Y_Trans']:.3f}) circle[radius=1pt];\n"
        if not pt_tex or pt_tex[-1] != tex:
            pt_tex.append(tex)
    
    res += "\n".join(pt_tex)
    res += "\n"
    return res

def create_image(project, points):
    data = sync_values(project)
    data = _transform_points(project, data)

    temp_dir_path = Path("./temp")

    # Clear out previous run
    if temp_dir_path.exists() and temp_dir_path.is_dir():
        rmtree(temp_dir_path)

    temp_dir_path.mkdir(parents=True, exist_ok=True)

    # Copy template files
    copy_tree("./template", "./temp")

    with open(Path(temp_dir_path, "generated.tex"), 'w+', encoding="utf-8") as f:
        f.write(_render_points(data))
    
    # Run pdflatex to generate preview pdf
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "preview.tex"], cwd=temp_dir_path)
    preview_pdf_path = Path(temp_dir_path, "preview.pdf")

    # If pdf was created successfully, convert to png for displaying in application 
    if preview_pdf_path.exists() and preview_pdf_path.is_file():
        subprocess.run(["magick", "-density", "300", "preview.pdf", "preview.png"], cwd=temp_dir_path)

    print(f"Distance min: {data['Distance'].min()}")
    print(f"Distance max: {data['Distance'].max()}")

    # Image creation was successful, if and only if preview.png exists
    preview_png_path = Path(temp_dir_path, "preview.png")
    return preview_png_path.exists() and preview_png_path.is_file()

