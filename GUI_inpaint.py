from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy
import scipy.misc
import cv2
import os

class app(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.x = self.y = 0
        self.w = self.h = 256
        #canvases allocation
        self.canvas1 = Canvas(self, width=256,height=256, bd=0, bg='white')
        self.canvas1.grid(row=0, column=0)
        self.canvas2 = Canvas(self, width=256,height=256, bd=0, bg='white')
        self.canvas2.grid(row=0, column=1)
        self.canvas3 = Canvas(self, width=256,height=256, bd=0, bg='white')
        self.canvas3.grid(row=0, column=2)
        self.mask = numpy.zeros((256,256), dtype = int)
        self.points = []
        self.bind('<ButtonPress-1>', self.press)
        self.bind('<ButtonRelease-1>', self.release)

    #the class to show the original image
    def showImg1(self):
        self.mask = numpy.zeros((256,256), dtype = int)
        File = askopenfilename(title='Open Image') 
        e.set(File)
    
        load = Image.open(e.get())
        load = load.resize((self.w, self.h))
        imgfile = ImageTk.PhotoImage(load)
    
        self.canvas1.image = imgfile  # <--- keep reference of your image
        self.canvas1.create_image(2,2,anchor='nw',image=imgfile)
        self.canvas1.old_coords = None

    #the class to show the inpainted image   
    def showImg2(self):    
        scipy.misc.imsave('images/mask.tiff', self.mask)    
        maskpath = 'images/mask.tiff'
        img = cv2.imread(e.get(), 1)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        msk= cv2.imread(maskpath, 0)
        
        if str(l.curselection())[1] == '0': model = 'CelebA'
        if str(l.curselection())[1] == '1': model = 'Places2'
        if str(l.curselection())[1] == '2': model = 'ImageNet'
        command = 'python3 test.py --image ' + e.get() + ' --mask ' + maskpath + ' --output examples/output.png --checkpoint_dir model_logs/' + model
        os.system(command)
        output1 = Image.open('examples/output.png')
        output1 = ImageTk.PhotoImage(output1)

        output2 = cv2.inpaint(img, msk, 5, cv2.INPAINT_NS)
        scipy.misc.imsave('images/output2.tiff', output2) 
        output2 = Image.open('images/output2.tiff')
        output2 = ImageTk.PhotoImage(output2)
        
        self.canvas2.image = output1
        self.canvas2.create_image(2,2,anchor='nw',image=output1)
        self.canvas3.image = output2
        self.canvas3.create_image(2,2,anchor='nw',image=output2)
    
    def press(self, event):
        self.x, self.y = event.x, event.y

    def release(self, event):
        x0, y0 = self.x, self.y
        x1, y1 = event.x, event.y
        self.canvas1.create_rectangle(x0, y0, x1, y1, fill='black')
        self.mask[y0:y1, x0:x1] = 255

root = app()
root.title = 'inpaint'

e = StringVar()

#the file opening button
open_button = Button(root, text ='Open', command = root.showImg1)
open_button.grid(row=1, column=0)

#the image inpainting button
predict_button = Button(root, text ='Inpaint', command = root.showImg2)
predict_button.grid(row=1, column=1)

l = Listbox(root, width=10, height=3, selectmode=EXTENDED)
l.insert(1, 'CelebA')
l.insert(2, 'Places2')
l.insert(3, 'ImageNet')
l.grid(row=1, column=2)

l1=Label(root, text='Please select a model, <Open> a 256x256 RGB image, then press <Inpaint>')
l1.grid(row=2, columnspan = 2)

root.mainloop()
