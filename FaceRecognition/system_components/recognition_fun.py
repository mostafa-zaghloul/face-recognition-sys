from keras import backend as K
import time
from multiprocessing.dummy import Pool
K.set_image_data_format('channels_first')
import cv2
import os
import numpy as np
from numpy import genfromtxt
import pandas as pd
import tensorflow as tf
# to ignore tensorflow warnings appears in runtime shell :
tf.logging.set_verbosity(tf.logging.ERROR)

from utils.fr_utils import *
from model_components.inception_blocks_v2 import *
from utils.triplet_loss_fun import *
from utils.name_parser import *

#empty_database_loading_error = ""
def who_is_it(image, database, model,recognition_fraction):
    """
    Implements face recognition by finding who is the person on the image_path image.
    
    Arguments:
    image_path -- path to an image
    database -- database containing image encodings along with the name of the person on the image
    model -- your Inception model instance in Keras
    
    Returns:
    min_dist -- the minimum distance between image_path encoding and the encodings from the database
    identity -- string, the name prediction for the person on image_path
    """
    # print("test image incoding")

    ## Step 1: Compute the target "encoding" for the image. Use img_to_encoding()
    encoding = img_to_encoding(image,model)
    #print("input encoding    :   " + str(encoding))

    ## Step 2: Find the closest encoding ##
    
    # Initialize "min_dist" to a large value, say 100
    min_dist = 100

    # print("looking for the incoding in the database")
    #detect if the known faces database is empty and handle its exeption :
    if(len(database) > 0 ):
        # Loop over the database dictionary's names and encodings.
        for (name, db_enc) in database.items():
            
            # Compute L2 distance between the target "encoding" and the current "db_enc" from the database.
            dist = np.linalg.norm(encoding - db_enc)
            # If this distance is less than the min_dist, then set min_dist to dist, and identity to name.
            if dist < min_dist:
                min_dist = dist
                identity = name
    
        if min_dist > recognition_fraction:
            #print("Not in the database." + ", the distance is " + str(min_dist))
            identity = "unknown"
        else:
            id = get_name(str(identity))
            identity = id
            #print ("it's " + id + " and was stored as " + str(identity) + ", the distance is " + str(min_dist))
        empty_database_loading_error = " "
        return identity,empty_database_loading_error
    #the known faces database is empty throwing exeption :
    else:
        empty_database_loading_error = "EMPTY DATABASE ERROR, NO KNOWN PEOPLE SAVED PLEASE ADD SOME PEOPLE YOU KNOW"
        return "unknown",empty_database_loading_error