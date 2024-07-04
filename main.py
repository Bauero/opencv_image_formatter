"""
This project is intended to practice use of opencv library, by creating a small
program which would allow user to perform basic transformation for the image
using OpenCV library for Python
"""

import cv2
import matplotlib.pylab as plt
import pandas as pd
import tkinter as tk
from tkinter import Canvas, NW, Scale, HORIZONTAL, DoubleVar, E, Button
from PIL import Image, ImageTk


# Create the Tkinter window
root = tk.Tk()
root.title("Image Editor")
root.geometry("1280x720")

red = 0
green = 0
blue = 0
image_negated = False

# Function to convert OpenCV image to a PhotoImage
def convert_to_tk_image(cv_image):
    pil_image = Image.fromarray(cv_image)
    tk_image = ImageTk.PhotoImage(image=pil_image)
    return tk_image

# Function to update the image based on the slider value
def update_image():

    global red, green, blue, image_negated

    modified_image = image_RGB.copy()

    modified_image[:, :, 0] = cv2.add(modified_image[:, :, 0], red)
    modified_image[:, :, 1] = cv2.add(modified_image[:, :, 1], green)
    modified_image[:, :, 2] = cv2.add(modified_image[:, :, 2], blue)

    if image_negated:
        modified_image = abs(255 - modified_image[:,:])

    tk_image = convert_to_tk_image(modified_image)
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
    
    im_gray = cv2.cvtColor(image_RGB.copy(), cv2.IMREAD_GRAYSCALE)
    im_blur = cv2.GaussianBlur(im_gray, (3,3), 0)
    edges = cv2.Canny(im_blur, 40, 70)

    plt.imshow(edges, cmap = 'gray')
    plt.show()


source_file_path = "cat_images/cat.4003.jpg"

image = cv2.imread(source_file_path)
image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
height, width, _ = image.shape






# Create a scale (slider) and attach the update_image function
s1 = Scale(root, variable=DoubleVar(),  
           from_=-255, to=255,  
           orient=HORIZONTAL, sliderlength=10, command = update_red)
s1.pack(anchor=E)

s2 = Scale(root, variable=DoubleVar(),  
           from_=-255, to=255,  
           orient=HORIZONTAL, sliderlength=10, command = update_green)
s2.pack(anchor=E)

s3 = Scale(root, variable=DoubleVar(),  
           from_=-255, to=255,  
           orient=HORIZONTAL, sliderlength=10, command = update_blue)
s3.pack(anchor=E)

def reset_colors():
    s1.set(0.0)
    s2.set(0.0)
    s3.set(0.0)

def negate_colors():
    global image_negated
    image_negated = True if not image_negated else False
    update_image()

b1 = Button(root, height=1, width=10, text="Reset colors", 
            command = reset_colors, default="normal")
b1.pack(anchor=E)

b2 = Button(root, height=1, width=10, text="Negate colors", 
            command = negate_colors, default="normal")
b2.pack(anchor=E)

b3 = Button(root, height=1, width=10, text="Edges", 
            command = show_edges, default="normal")
b3.pack(anchor=E)

canvas = Canvas(root, width=width, height=height)
canvas.pack()
tk_image = convert_to_tk_image(image_RGB)
image_on_canvas = canvas.create_image(0, 0, anchor=NW, image=tk_image)

# Start the Tkinter main loop
root.mainloop()
exit()
