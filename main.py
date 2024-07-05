"""
This project is intended to practice use of opencv library, by creating a small
program which would allow user to perform basic transformation for the image
using OpenCV library for Python
"""

import cv2
import matplotlib.pylab as plt
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import Canvas, Scale, DoubleVar, Button, \
                     E, NW, HORIZONTAL, CENTER
from PIL import Image, ImageTk


################################################################################
# CONSTANTS IN THE PROGRAM
################################################################################


red = 0
green = 0
blue = 0
image_negated = False
wheight = 720
wwidth = 1280


################################################################################
# FUNCITONS FOR IMAGE MANIPULATION
################################################################################


def convert_to_tk_image(cv_image):
    pil_image = Image.fromarray(cv_image)
    tk_image = ImageTk.PhotoImage(image=pil_image)
    return tk_image


def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    scaling_factor = min(max_width / width, max_height / height)
    if scaling_factor < 1:  # Only resize if the image is larger than the desired dimensions
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_image = cv2.resize(image, (new_width, new_height), 
                                   interpolation=cv2.INTER_AREA)
        return resized_image
    return image


def update_image():

    global red, green, blue, image_negated, wheight, wwidth, image_changed

    modified_image = image_RGB.copy()

    modified_image[:, :, 0] = cv2.add(modified_image[:, :, 0], red)
    modified_image[:, :, 1] = cv2.add(modified_image[:, :, 1], green)
    modified_image[:, :, 2] = cv2.add(modified_image[:, :, 2], blue)

    if image_negated:
        modified_image = abs(255 - modified_image[:,:])

    image_changed = modified_image.copy()

    resized = resize_image(modified_image, wwidth, wheight)

    tk_image = convert_to_tk_image(resized)
    canvas.itemconfig(image_on_canvas, image=tk_image)

    # Keep a reference to the image to prevent garbage collection
    canvas.image = tk_image


def update_red(val):
    global red
    red = int(float(val))
    update_image()


def update_green(val):
    global green
    green = int(float(val))
    update_image()


def update_blue(val):
    global blue
    blue = int(float(val))
    update_image()


def show_edges():
    
    global wheight, wwidth

    new_image = resize_image(image_RGB.copy(), wwidth, wheight)

    new_image[:, :, 0] = cv2.add(new_image[:, :, 0], red)
    new_image[:, :, 1] = cv2.add(new_image[:, :, 1], green)
    new_image[:, :, 2] = cv2.add(new_image[:, :, 2], blue)

    if image_negated:
        new_image = abs(255 - new_image[:,:])

    im_gray = cv2.cvtColor(new_image, cv2.IMREAD_GRAYSCALE)
    im_blur = cv2.GaussianBlur(im_gray, (3,3), 0)
    edges = cv2.Canny(im_blur, 40, 70)

    plt.imshow(edges, cmap = 'gray')
    plt.show()


def save_image():
    global image_changed
    dir = askdirectory(parent=root)
    if dir:
        cv2.imwrite(f"{dir}/saved_file.jpg", cv2.cvtColor(image_changed, 
                                                          cv2.COLOR_RGB2BGR))


################################################################################
# CONNECTING FUNCITONS, CREATING LAYOUT, DISPLAYING PICTURE
################################################################################

#
# Beginning - question for the file
#

root = tk.Tk()
source_file_path = askopenfilename(parent=root)
if not source_file_path:
    exit()

#
# Window creation
#

# root = tk.Tk()
root.title("Image Editor")
# root.geometry(f"{wwidth}x{wheight}")

image = cv2.imread(source_file_path)
image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_changed = image_RGB.copy()

#
# Create a frame for the image and another for the controls
#

frame_image = tk.Frame(root)
frame_image.grid(row=0, column=0, padx=20, pady=20, sticky=E)

frame_controls = tk.Frame(root)
frame_controls.grid(row=0, column=1, padx=20, pady=20, sticky=E)

#
# Create a scale (slider) and attach the update_image function
#

s1 = Scale(frame_controls, variable=DoubleVar(),  from_=-255, to=255,  
           orient=HORIZONTAL, sliderlength=10, command=update_red, 
           label="Red")

s2 = Scale(frame_controls, variable=DoubleVar(),  from_=-255, to=255,  
           orient=HORIZONTAL, sliderlength=10, command=update_green, 
           label="Green")

s3 = Scale(frame_controls, variable=DoubleVar(),  from_=-255, to=255,  
           orient=HORIZONTAL, sliderlength=10, command=update_blue, 
           label="Blue")

s1.pack(anchor=CENTER)
s2.pack(anchor=CENTER)
s3.pack(anchor=CENTER)

#
# Buttons and functions for buttons 
#

def reset_colors():
    s1.set(0.0)
    s2.set(0.0)
    s3.set(0.0)


def negate_colors():
    global image_negated
    image_negated = not image_negated
    update_image()

b1 = Button(frame_controls, height=1, width=10, text="Reset colors", 
            command=reset_colors, default="normal", border=10)

b2 = Button(frame_controls, height=1, width=10, text="Negate colors", 
            command=negate_colors, default="normal")

b3 = Button(frame_controls, height=1, width=10, text="Edges", 
            command=show_edges, default="normal")

b4 = Button(frame_controls, height=1, width=10, text="Save image", 
            command=save_image, default="normal")

b1.pack(anchor=CENTER)
b2.pack(anchor=CENTER)
b3.pack(anchor=CENTER)
b4.pack(anchor=CENTER)

#
# Image display
#

resized_image = resize_image(image_RGB, wwidth, wheight)
height, width, _ = resized_image.shape

canvas = Canvas(frame_image, width = width, height = height)
canvas.pack()
tk_image = convert_to_tk_image(resized_image)
image_on_canvas = canvas.create_image(0, 0, anchor=NW, image=tk_image)

#
# Start the Tkinter main loop
#

root.mainloop()
exit()
