#import imutils
import dlib
import cv2
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


def detect_faces(image_path, database, model,recognition_fraction,master):

    #print("detecting faces")

    # load the input image, resize it, and convert it to grayscale
    PADDING = 0
    image = cv2.imread(image_path)
    frame = image
    # bad for detection :
    #image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    detector = dlib.get_frontal_face_detector()
    # detect faces in the grayscale image
    faces = detector(gray, 1)

    ##fname = faces_folder_path.split('/')[-1]
    ##name, ext = fname.split('.')

    # dictionary of detected faces identities
    identities = []

    #detect if there is no detected faces in the image and handling its exeption error :
    if(len(faces) > 0):
        # loop over the face detections
        for (i, face) in enumerate(faces):
            # determine the facial landmarks for the face region, then
            # convert the landmark (x, y)-coordinates to a NumPy array
            (x, y, w, h) = rect_to_bb(face)
            x1 = x-PADDING
            y1 = y-PADDING
            x2 = x+w+PADDING
            y2 = y+h+PADDING

            ##fname = '{}_{}.{}'.format(name, i, ext)
            # clone the original image so we can draw on it, then
            # display the name of the face part on the image
            ##clone = image.copy()
            ##cv2.rectangle(clone, (x, y), (x + w, y + h), (0, 255, 0), 1)
            ##startX = x
            ##startY = y - 15 if y - 15 > 15 else y + 15
            ##cv2.putText(clone, str(i), (startX, startY),
            ##cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #roi = image[y:y + h, x:x + w]

            """
            Determine whether the face contained within the bounding box exists in our database
         
            x1,y1_____________
            |                 |
            |                 |
            |_________________x2,y2

            """
            height, width, channels = frame.shape
            # The padding is necessary since the OpenCV face detector creates the bounding box around the face and not the head
            part_image = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]

            #roi = image[y1:y2, x1:x2]
            #roi = cv2.rectangle(frame,(x1, y1),(x2, y2),(255,0,0),2)
            ##cv2.imshow("input", roi)
            #cv2.imwrite("croped_faces/detected_input_face.jpg", part_image)
            #print("recognice")
            identity,empty_database_loading_error = who_is_it(part_image, database, model,recognition_fraction)
            #print("face")
            #cv2.waitKey(0)
            identities.append(identity)
    else:
        empty_database_loading_error = " "

    output(identities,master)
    return empty_database_loading_error