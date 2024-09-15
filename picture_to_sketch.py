"""
Image to Sketch Converter

This program converts an image to a pencil sketch-like effect. It supports various image formats,
including those with transparency (alpha channel). The program features a graphical user interface
for selecting the input image. The output image is automatically saved in the same directory as
the input, with '_drawing' appended to the original filename.

How it works:
1. User selects an image file through a file dialog.
2. The image is converted to grayscale (if not already).
3. The grayscale image is inverted and blurred.
4. The original grayscale image is divided by the inverted blurred image to create a sketch effect.
5. If the original image had an alpha channel, it's preserved in the output.
6. The resulting sketch is saved as a new image file.

Usage:
Run the script and select an image file when prompted. The converted image will be saved automatically.
"""

import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog

def photo_to_sketch(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return

    # Read the image with alpha channel
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Check if the image was loaded correctly
    if img is None:
        print(f"Error: Unable to read the image {image_path}.")
        return

    # Check the number of channels
    if len(img.shape) == 2:  # Grayscale image
        gray = img
    elif len(img.shape) == 3 and img.shape[2] == 3:  # RGB image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif len(img.shape) == 3 and img.shape[2] == 4:  # RGBA image
        # Separate RGB and alpha channels
        rgb = img[:,:,0:3]
        alpha = img[:,:,3]
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    else:
        print(f"Error: Unsupported image format for {image_path}.")
        return

    # Invert the grayscale image
    inverted = cv2.bitwise_not(gray)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)

    # Invert the blurred image
    inverted_blurred = cv2.bitwise_not(blurred)

    # Create the sketch effect
    sketch = cv2.divide(gray, inverted_blurred, scale=256.0)

    # If the original image had an alpha channel, apply it to the sketch
    if len(img.shape) == 3 and img.shape[2] == 4:
        sketch = cv2.merge([sketch, sketch, sketch, alpha])

    # Generate output path
    directory, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(directory, f"{name}_drawing{ext}")

    # Save the resulting image
    cv2.imwrite(output_path, sketch)

    print(f"Sketch image saved as {output_path}")

def select_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )

    if file_path:
        try:
            photo_to_sketch(file_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No file selected")

# Launch the file selection interface
select_image()