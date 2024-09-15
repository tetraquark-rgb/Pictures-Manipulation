"""
Transparent Image to Bichrome Converter with Color Selection

This program converts a transparent image (PNG with alpha channel) to a bichrome version,
with black and a user-selected color. It features a graphical user interface for selecting
the input image and choosing the second color from a color palette. The output image is 
automatically saved in the same directory as the input, with '_bichrome' appended to the 
original filename.

How it works:
1. User selects a transparent PNG image file through a file dialog.
2. User chooses the second color from a color palette.
3. The image is converted to grayscale.
4. A threshold is applied to create a binary image.
5. The binary image is colorized with black and the chosen color.
6. The original alpha channel is preserved in the output.
7. The resulting bichrome image is saved as a new PNG file.

Usage:
Run the script, select a transparent PNG image file, and choose a color when prompted. 
The converted image will be saved automatically.
"""

import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, colorchooser

def portrait_to_bichrome_transparent(input_path, color, threshold=127):
    # Check if the file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")

    # Read the image with alpha channel
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

    # Check if the image was loaded correctly
    if img is None:
        raise ValueError(f"Unable to read the image {input_path}. Check the file format.")

    # Check if the image has an alpha channel
    if len(img.shape) != 3 or img.shape[2] != 4:
        raise ValueError("The input image must have an alpha channel (be transparent)")

    # Separate RGB and alpha channels
    rgb = img[:,:,0:3]
    alpha = img[:,:,3]

    # Convert the image to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to get a bichrome image
    _, bichrome = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Create a black and colored image with 4 channels (RGBA)
    result = np.zeros((bichrome.shape[0], bichrome.shape[1], 4), dtype=np.uint8)
    
    # Convert RGB color to BGR for OpenCV
    color_bgr = tuple(int(c) for c in color[::-1])  # Convert to integers and reverse order
    
    # Apply black and the chosen color
    result[bichrome == 0] = (0, 0, 0, 255)  # Black
    result[bichrome == 255] = color_bgr + (255,)  # Chosen color with full alpha
    
    # Apply the original alpha channel
    result[:,:,3] = alpha

    # Generate output path
    directory, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(directory, f"{name}_bichrome{ext}")

    # Save the resulting image
    cv2.imwrite(output_path, result)

    print(f"Bichrome transparent image saved as {output_path}")

def select_image_and_color():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(
        title="Select a transparent PNG image",
        filetypes=[("PNG files", "*.png")]
    )

    if file_path:
        color = colorchooser.askcolor(title="Choose color for bichrome image")
        if color[0]:  # color is a tuple (RGB tuple, hex string)
            try:
                portrait_to_bichrome_transparent(file_path, color[0])
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("No color selected")
    else:
        print("No file selected")

# Launch the file and color selection interface
select_image_and_color()