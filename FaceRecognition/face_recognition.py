# Face Recognition system from ( image , video , webcam ) 
# face detection using Dlib and classification using Facenet paper implimentation 
# our model load pretrained weights (facenet model weights)

import sys
# to ignore np and h5 warnings :
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import tensorflow as tf
# to ignore tensorflow warnings appears in runtime shell :
tf.logging.set_verbosity(tf.logging.ERROR)

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from utils.fr_utils import *
from model_components.inception_blocks_v2 import *
from utils.triplet_loss_fun import *
from database.faces_database import *
from system_components.recognize_from_image import *
from system_components.recognize_from_webcam import *

# determine the way floating point numbers, arrays and other NumPy objects are displayed to be unique
np.set_printoptions(threshold=np.nan)    

#tkinter gui to access sysem functionality :
try:
#while(True):
    #main Window
    master = tk.Tk()
    master.geometry("800x400")
    master.title("Face Recognition System")


    #Loading System Components window function :
    def system_loading():
        #print("initiate model")
        label = tk.Label(master, text="Model Initiation", bg="white", fg="green")
        label.pack()
        # initiate our model and specifying the input image shape by accessing model_components.inception_blocks_v2 :
        FRmodel = faceRecoModel(input_shape=(3, 96, 96))

        # print("Total Params:", FRmodel.count_params())
        #print("compile model")
        label = tk.Label(master, text="Model Compilation", bg="white", fg="black")
        label.pack()
        # model configration and specify it's compiling parameters :
        FRmodel.compile(optimizer = 'adam', loss = triplet_loss, metrics = ['accuracy'])

        #print("weights loading")
        label = tk.Label(master, text="Weights Loading", bg="white", fg="red")
        label.pack()
        #Facenet weights loading :
        load_weights_from_FaceNet(FRmodel)

        #print("database loading")
        label = tk.Label(master, text="Database Loading", bg="white", fg="blue")
        label.pack()

        #load cropes faces database data from database.txt :
        database,load_error = load_database(FRmodel)
        if(load_error !=" "):
            #print(load_error)
            #warning message if the database dictionary :
            messagebox.showinfo("Error", load_error)


        label = tk.Label(master, text="Please Add Known People To Your System :", bg="green", fg="white")
        label.pack()

        add_known_faces_button = tk.Button(master, text="Add Known People", command=lambda:add_known_faces_window(FRmodel))
        add_known_faces_button.pack()

        label = tk.Label(master, text="Select your Recognition Input  :", bg="green", fg="white")
        label.pack()

        image_recognition_button = tk.Button(master, text="Recognize People from Image", command=lambda:image_recognition_window(FRmodel,database))
        image_recognition_button.pack()
        cam_recognition_button = tk.Button(master, text="Recognize People from Live Camera Streaming", command=lambda:cam_recognition_window(FRmodel,database))
        cam_recognition_button.pack()
        label = tk.Label(master, text="Terminate The System", bg="green", fg="white")
        label.pack()
        close_button = tk.Button(master, text="Close", command=quit)
        close_button.pack()

    #add_known_faces window function :
    def add_known_faces_window(FRmodel):
        master2 = tk.Tk()
        master2.geometry("600x400")
        master2.title("Adding Known People")

        #Selecting known faces images to store the main window
        label = tk.Label(master2, text="Welcome ..", bg="green", fg="white")
        label.pack()
        label = tk.Label(master2, text="Click Add Pleople Button Below To Add Images Of Your Known People.", bg="green", fg="white")
        label.pack()
        label = tk.Label(master2, text="Please Specify The Seected People Names In Each Image File Name.", bg="green", fg="white")
        label.pack()
        add_faces_button = tk.Button(master2, text="Add Known People", command=lambda:add_known_faces_fun(FRmodel,master2))
        add_faces_button.pack()

    #add_known_faces function :
    def add_known_faces_fun(FRmodel,master):
        try:
            filenames =  filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("jpg files","*.jpg"),("png files","*.png"),("all files","*.*")))
            if not filenames:
                messagebox.showinfo("Error", "No Image Selected !")
            else:
                create_database(FRmodel,filenames,master)
        except:
            messagebox.showinfo("Error", "Image Selection Error!")

    #image regognition window function :
    def image_recognition_window(FRmodel,database):
        master3 = tk.Tk()
        master3.geometry("600x400")
        master3.title("Image Recognition")


        label = tk.Label(master3, text="Welcome .. Start Recognize People By Image :", bg="green", fg="white")
        label.pack()
        label = tk.Label(master3, text="Please Select An Image And Then Click The Recognition Button.", bg="green", fg="white")
        label.pack()


        select_image = tk.Button(master3, text="select image", command=lambda:load_image_fun(FRmodel,database,master3))
        select_image.pack()
        label = tk.Label(master3, text="Terminate Image Recognition", bg="green", fg="white")
        label.pack()
        close_button = tk.Button(master3, text="Close", command=master3.destroy)
        close_button.pack()
        master3.mainloop()

    #load image fun :
    def load_image_fun(FRmodel,database,master):
        try:
            recognition_fraction = 0.59
            filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpg files","*.jpg"),("png files","*.png"),("all files","*.*")))
            if not filename:
                messagebox.showinfo("Error", "No Image Selected !")
            else:
                #print(filename)
                # print("recognizing input image")
                # recognize image :
                empty_database_loading_error = detect_faces(filename,database , FRmodel,recognition_fraction,master)
                # handling the case that the stored known faces database is empty :
                if(empty_database_loading_error != " "):
                    messagebox.showinfo("Error", empty_database_loading_error)
        except:
            messagebox.showinfo("Error", "Image Selection Error!")

    #cam streaming regognition window function :
    def cam_recognition_window(FRmodel,database):
        master4 = tk.Tk()
        master4.geometry("700x650")
        master4.title("Live Camera Streaming Recognition")
        label = tk.Label(master4, text="Live Camera Streaming", bg="green", fg="white")
        label.pack()
        newwindow = tk.Button(master4, text="Start Live Streaming Recognition", command=lambda:cam_fun(FRmodel,database,master4))
        newwindow.pack()
        master4.mainloop()

    #determinatin fun :
    #def determinate_fun(master,):

    #cam function :
    def cam_fun(FRmodel,database,master):
        try:
            recognition_fraction = 0.59
            cam_index = 0
            empty_database_loading_error = webcam_detect_faces(database,FRmodel,recognition_fraction,cam_index,master)
            # handling the case that the stored known faces database is empty :
            if(empty_database_loading_error != " "):
                #print(empty_database_loading_error )
                messagebox.showinfo("Error", empty_database_loading_error)
        except:
            messagebox.showinfo("Error", "Camera Error!")
     
    #main window components :

    #welcoming label in the main window
    label = tk.Label(master, text="Please Click The Button Below And Wait To Start Our System.", bg="green", fg="white")
    label.pack()
    label = tk.Label(master, text="Please Be Patient .. It May Take A Bit To Start.", bg="green", fg="white")
    label.pack()
    system_loading_button = tk.Button(master, text="Start System Componants Loading", command=system_loading)
    system_loading_button.pack()

    master.mainloop()
except:
    # message box display
    messagebox.showinfo("Unexpected Error", "Something went Wrong ..!")