# handling known faces database creation and updating and loading

import os
import glob
import pickle
import cv2
from utils.fr_utils import *
from database.database_face_detector import *
import tkinter as tk

#empty_database_creating_error = " "
def create_database(FRmodel,filenames,master):
    #global empty_database_creating_error
    database = {}

    # load all the images of individusals to recognize into the database

    #for file in glob.glob("images/*"):
    #    identity = os.path.splitext(os.path.basename(file))[0]
    #    database[identity] = img_path_to_encoding(file, FRmodel)
    #    print("x")


    #path = 'images'
    #croped_path = 'croped_faces'
    #if(len(os.listdir(path)) !=0):
    #    for i in os.listdir(path):
            #for f in os.listdir(os.path.join(path, i)):
    for path in filenames:
                #img = detect_face(os.path.join(path,i,f))
        #print(path)
        img = detect_face(path)
                #if(img != os.path.join(path,i,f)):
        if(img != path):
            image_name = os.path.basename(path)
            #print(image_name)
            # Check file extension. Allow only jpg/jpeg' files.
            ext = os.path.splitext(image_name)[1]
            if ext == '.jpg' or ext == '.jpeg' or ext == '.png':
                #database.append(IdentityMetadata(path, i, f))
                identity = os.path.splitext(image_name)[0]
                        #for testing the database :
                        #cv2.imshow("database", img)
                        #cv2.waitKey(0)
                        #print(os.path.join(croped_path,f))
                        # save detected face croped image in croped_faces folder
                        #cv2.imwrite(os.path.join(croped_path,f), img)
                        # remove the orignal input knowen face image :
                        #os.remove(os.path.join(path,i,f))
                database[identity] = img_to_encoding(img, FRmodel)
                        #print(str(identity) + "    :         " + str(img_to_encoding(img, FRmodel)))
                        #print(str(len(database)))
                empty_image_error = " "
        else:
            #handleing the case that input image of to be known face has no face detected
            empty_image_error = "No Person Detected in : " + path + "  Plese Try Another Shot."
            #print(empty_image_error)
            label = tk.Label(master, text=empty_image_error, bg="red", fg="white")
            label.pack()

    # using 'ab' to append to the file and 'wb' to write on in from the begining :
    with open('database/database.txt', 'ab') as handle:
        pickle.dump(database, handle)
    #empty_database_creating_error =  " "
    #return empty_database_creating_error
    #else:
    #    empty_database_creating_error = "NO KNOWN FACES SAVED PLEASE ADD SOME PEOPLE YOU KNOW"
    #    return empty_database_creating_error


def load_database(FRmodel):

    #to be called in system intation and updating and adding database faces
    ########

    #create_database(FRmodel)

    ########
    #print("loading faces incoding")

    # load identitys and it's encodings from database txt file :
    try:
        with open('database/database.txt', 'rb') as handle:
            data = pickle.loads(handle.read())
            load_error = " "
        return data,load_error
    except:
        load_error = "LOADING ERROR, NO KNOWN PEOPLE SAVED PLEASE ADD SOME PEOPLE YOU KNOW"
        data = {}
        return data,load_error


#def load_database(FRmodel):

#    database = {}
#    database["danielle"] = img_to_encoding("images/danielle.png", FRmodel)
#    database["younes"] = img_to_encoding("images/younes.jpg", FRmodel)
#    database["tian"] = img_to_encoding("images/tian.jpg", FRmodel)
#    database["andrew"] = img_to_encoding("images/andrew.jpg", FRmodel)
#    database["kian"] = img_to_encoding("images/kian.jpg", FRmodel)
#    database["dan"] = img_to_encoding("images/dan.jpg", FRmodel)
#    database["sebastiano"] = img_to_encoding("images/sebastiano.jpg", FRmodel)
#    database["bertrand"] = img_to_encoding("images/bertrand.jpg", FRmodel)
#    database["kevin"] = img_to_encoding("images/kevin.jpg", FRmodel)
#    database["felix"] = img_to_encoding("images/felix.jpg", FRmodel)
#    database["benoit"] = img_to_encoding("images/benoit.jpg", FRmodel)
#    database["arnaud"] = img_to_encoding("images/arnaud.jpg", FRmodel)
#    database["mostafa"] = img_to_encoding("images/mostafa.jpg", FRmodel)

#    return database
