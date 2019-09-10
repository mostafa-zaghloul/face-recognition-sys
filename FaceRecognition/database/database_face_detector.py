# take image from database folders to detect it's face
# to be passed to the encoding function
# and then to be stored to the known faces database 
import argparse
#import imutils
import dlib
import cv2

# helper fun
def face_to_bb(face):
    # take a bounding predicted by dlib and convert it
    # to the format (x, y, w, h) as we would normally do
    # with OpenCV

    ## -(int(face.top()/2)) added to take the head with me in the base face image
    x = face.left()
    y = face.top() 
    w = face.right() - x 
    h = face.bottom() - y 

    # return a tuple of (x, y, w, h)
    return (x, y, w, h)

def detect_face(input_image):
    # construct the argument parser and parse the arguments

    #predictor_path = 'shape_predictor_5_face_landmarks.dat'
    #faces_folder_path = 'x/camera_0.jpg'

    # load the input image, resize it, and convert it to grayscale
    PADDING = 0
    image = cv2.imread(input_image)
    frame = image
    # bad for detection :
    #image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()

    faces = detector(gray, 1)
    #print("faces lence : " + str(len(faces)))

    # get the coordinates of the detected face :
    #print(str(face_to_bb(faces[0])))
    #detect if there is no detected faces in the image and handling its exeption error :
    if(len(faces) > 0):
        (x, y, w, h) = face_to_bb(faces[0])
        #print(i, x, y, w, h)
        x1 = x-PADDING
        y1 = y-PADDING
        x2 = x+w+PADDING
        y2 = y+h+PADDING

        """
        Determine whether the face contained within the bounding box exists in our database
     
        x1,y1_____________
        |                 |
        |                 |
        |_________________x2,y2

        """
        #get the orignal image data to use it to create the detected face image
        height, width, channels = frame.shape
        # padding ignored as the accurcy works fine without it 
        # The padding is necessary since the OpenCV face detector creates the bounding box around the face and not the head
        # seting the detected face borders not to exede the orignal image :
        part_image = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]

        #part_image = image[y1:y2, x1:x2]
        #for testing :
        #cv2.imwrite("croped_faces/database_face.jpg", part_image)

        return part_image
    else:
        return input_image


        
        