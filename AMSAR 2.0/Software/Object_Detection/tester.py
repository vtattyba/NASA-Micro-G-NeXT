from object_detection import Detector
import cv2

det = Detector(use_TPU=False, model_name='./tflite1/Sample_TFLite_model')


while True:
    print(det.check_tf())
    cv2.waitKey(1)
cv2.destroyAllWindows()