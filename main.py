__author__ = 'Lesmed'
import view as view
import pygame.font, pygame.event, pygame.draw
from Tkinter import *
from tkFileDialog import askopenfilename

from PIL import Image
import Tkinter as tk

v0=Tk(className="OCR Lesmed - Randall")

def loadView():
    view.main(False, 0)
def uploadImage():
    filename = askopenfilename()
    pygame.Surface((350, 350))
    img = Image.open(filename)
    view.Process_image(img)
    view.main(True, filename)


v0.geometry("500x500")
frame1 = tk.Frame(v0).pack(side= RIGHT)
drawButton = Button(frame1,text="Dibujar",command=lambda:loadView()).pack()
uploadImageButton=Button(frame1,text="Subir imagenes",command=lambda:uploadImage()).pack()




v0.mainloop()