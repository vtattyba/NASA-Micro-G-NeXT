######## Picamera Object Detection Using Tensorflow Classifier #########
#
# Author: Vladimir Tattybayev 
# Date: 10/20/2019
# Description: This code uses Tensor Flow for object detection. 
# Initial code is being used to keep Camera's field of view centered.
# Will trigger motor scripts to either turn left or right depending on 
# relative position of person to camera.  


## Initial Author: Evan Juras
## His source is at
## https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## but I changed it to make it more understandable to me.


# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys

# Set up camera constants / adjust as needed 
IM_WIDTH = 640 
IM_HEIGHT = 480


# This is needed since the working directory is the object_detection folder.
sys.path.append('..')

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Current model in use from directory 
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
#MODEL_NAME = 'ssd_mobilenet_v2_coco_2018_03_29' //Tested this, its slower but more accurate FPS (-0.45)


CWD_PATH = os.getcwd() # Grabs path to current working directory

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','person_label_map.pbtxt') #Person_Label only contains person 

# Number of classes the object detector can identify
NUM_CLASSES = 1

## Load the label map.
# Label maps map indices to category names, so that when the convolution
# network predicts `5`, we know that this corresponds to `airplane`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

#Initialize Coords 
TL_middle = (int(IM_WIDTH*0.48),int(IM_HEIGHT))
BR_middle = (int(IM_WIDTH*0.52),int(IM_HEIGHT*0))

TL_left = (int(IM_WIDTH*0),int(IM_HEIGHT))    
BR_left = (int(IM_WIDTH*0.48),int(IM_HEIGHT*0))


TL_right = (int(IM_WIDTH*0.52),int(IM_HEIGHT))
BR_right = (int(IM_WIDTH),int(IM_HEIGHT*0))


# Initialize Picamera and grab reference to the raw capture
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

    t1 = cv2.getTickCount()
    
    # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
    # i.e. a single-column array, where each item in the column has the pixel RGB value
    frame = np.copy(frame1.array)
    frame.setflags(write=1)
    frame_expanded = np.expand_dims(frame, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})

    # Draw the results of the detection (aka 'visulaize the results')
    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.40)
    ##########################################################################
    
    
    
    #Middle Box
    cv2.rectangle(frame,TL_middle,BR_middle,(20,20,255),3)
    cv2.putText(frame,"C",(TL_middle[0],TL_middle[1]-10),font,1,(20,255,255),1,cv2.LINE_AA)
    #Left Box
    cv2.rectangle(frame,TL_left,BR_left,(20,20,255),3)
    cv2.putText(frame,"L",(TL_left[0]+10,TL_left[1]-10),font,1,(20,255,255),1,cv2.LINE_AA)
    #Right Box
    cv2.rectangle(frame,TL_right,BR_right,(20,20,255),3)
    cv2.putText(frame,"R",(BR_right[0]-25,TL_right[1]-10),font,1,(20,255,255),1,cv2.LINE_AA)
    
    #If highest probability Object is Human
    if (int(classes[0][0] == 1)):
        x = int(((boxes[0][0][1]+boxes[0][0][3])/2)*IM_WIDTH)
        y = int(((boxes[0][0][0]+boxes[0][0][2])/2)*IM_HEIGHT)
        cv2.circle(frame,(x,y), 5, (75,13,180), -1)
        
        #IF in left coords -> Go right
        if ((x > TL_left[0]) and (x < BR_left[0])):
            cv2.putText(frame,'Turn Right',(30,100),font,1,(20,255,255),2,cv2.LINE_AA)
        
        #IF in right coords -> Go left
        if ((x > TL_right[0]) and (x < BR_right[0])):
            cv2.putText(frame,'Turn Left',(30,100),font,1,(20,255,255),2,cv2.LINE_AA)    
            
        #IF in right coords -> Go Straight
        if ((x > TL_middle[0]) and (x < BR_middle[0])):
            cv2.putText(frame,'Go Straight',(30,100),font,1,(20,255,255),2,cv2.LINE_AA)    
            
            
    ###########################################################################
    
    #Returns Current FPS
    cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

    # All the results have been drawn on the frame, so it's time to display it.
    cv2.imshow('Object detector', frame)

    t2 = cv2.getTickCount()
    time1 = (t2-t1)/freq
    frame_rate_calc = 1/time1

    # Press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

    rawCapture.truncate(0)

camera.close()
cv2.destroyAllWindows()

