from shutil import rmtree
from distutils.dir_util import copy_tree
import subprocess
from pathlib import Path

def create_image():
    temp_dir_path = Path("./temp")

    # Clear out previous run
    if temp_dir_path.exists() and temp_dir_path.is_dir():
        rmtree(temp_dir_path)

    temp_dir_path.mkdir(parents=True, exist_ok=True)

    # Copy template files
    copy_tree("./template", "./temp")

    # Run pdflatex to generate preview pdf
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "preview.tex"], cwd=temp_dir_path)
    preview_pdf_path = Path(temp_dir_path, "preview.pdf")

    # If pdf was created successfully, convert to png for displaying in application 
    if preview_pdf_path.exists() and preview_pdf_path.is_file():
        subprocess.run(["magick", "-density", "300", "preview.pdf", "preview.png"], cwd=temp_dir_path)

    # Image creation was successful, if and only if preview.png exists
    preview_png_path = Path(temp_dir_path, "preview.png")
    return preview_png_path.exists() and preview_png_path.is_file()

