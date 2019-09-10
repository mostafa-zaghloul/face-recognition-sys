#import imutils
import dlib
import cv2
import time
import tkinter as tk
from PIL import Image, ImageTk
from system_components.recognition_fun import *
from system_components.output import *

def rect_to_bb(rect):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    # return a tuple of (x, y, w, h)
    return (x, y, w, h)

empty_database_loading_error = " "
def webcam_detect_faces(database , model,recognition_fraction,cam_index,master):

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(cam_index)
    webcam_detect_faces.close_straming_flag = False
    lmain = tk.Label(master)
    lmain.pack()
    def close_streaming():
        webcam_detect_faces.close_straming_flag = True

    label = tk.Label(master, text="Terminate The Camera Streaming ", bg="red", fg="white")
    label.pack()
    close_button = tk.Button(master, text="Stop Camera streaming", command=close_streaming)
    close_button.pack()
    label = tk.Label(master, text="Terminate Camera Recognition Window", bg="green", fg="white")
    label.pack()
    close_window_button = tk.Button(master, text="Close", command=master.destroy)
    close_window_button.pack()

    def video_stream():
        # dictionary of detected faces identities
        ##identities = []
        global empty_database_loading_error
        # Grab a single frame of video
        ret, frame = video_capture.read()
        if ret:
            # load the input image, resize it, and convert it to grayscale
            PADDING = 0
            image = frame
            # bad for detection :
            #image = imutils.resize(image, width=500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # initialize dlib's face detector (HOG-based) and then create
            # the facial landmark predictor
            detector = dlib.get_frontal_face_detector()
            # detect faces in the grayscale image
            faces = detector(gray, 1)

            # Loop through each face in this frame of video
            for (i, face) in enumerate(faces):
                # determine the facial landmarks for the face region, then
                (x, y, w, h) = rect_to_bb(face)
                x1 = x-PADDING
                y1 = y-PADDING
                x2 = x+w+PADDING
                y2 = y+h+PADDING
           
                # See if the face is a match for the known face(s)
                height, width, channels = frame.shape
                # The padding is necessary since the OpenCV face detector creates the bounding box around the face and not the head
                part_image = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]
                identity,empty_database_loading_error = who_is_it(part_image, database, model,recognition_fraction)


                # Draw a box around the face
                cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (face.left(), face.bottom() - int(face.bottom()/12)), (face.right(), face.bottom()), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, identity, (face.left() + 6, face.bottom() - 6), font, ((x2-x1)/300) , (255, 255, 255),1)
                ##identities.append(identity)
            if(webcam_detect_faces.close_straming_flag == False):            
                # Display the resulting image
                #cv2.imshow('Camera Stream', frame)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img,master= master)
                lmain.imgtk = imgtk
                lmain.configure(image=imgtk)
                lmain.configure(image=imgtk)
                lmain.after(1, video_stream)
            else:
                video_capture.release()
                ##master.destroy

            # to print the detected and recognized faces for every taken frame and start all over again by the nect frame :
            ##output(identities,master)
            ##identities = []
            #time.sleep(1)
            # Hit 'q' on the keyboard to quit!
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break
        else:
            video_capture.release()


    # to print the detected and recognized faces at the end of taking shots
    #output(identities)
    # Release handle to the webcam
    ##video_capture.release()
    ##cv2.destroyAllWindows()
    video_stream()
    return empty_database_loading_error