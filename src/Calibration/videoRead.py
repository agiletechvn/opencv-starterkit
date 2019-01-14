import cv2
import numpy as np
import click
import time
import sys

cv2_version = str(cv2.__version__)
major_ver, minor_ver, subminor_ver = cv2_version.split('.')

assert float(cv2.__version__.rsplit('.', 1)[
             0]) >= 3, 'OpenCV version 3 or newer required.'


# Initialize the parameters
confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.3  # Non-maximum suppression threshold
inpWidth = 416  # Width of network's input image
inpHeight = 416  # Height of network's input image


# Load names of classes
classesFile = "coco.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "yolov3.cfg"
modelWeights = "yolov3.weights"

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(frame, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv2.getTextSize(
        label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv2.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(
        1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, label, (left, top),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame, classIds[i], confidences[i], left,
                 top, left + width, top + height)


@click.command()
@click.option('--videopath', default='fisheye.3gp',
              help='The recorded camera video.')
@click.option('--start', default=3600,
              help='The position in seconds.')
def main(videopath, start):

    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(videopath)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    cv2.namedWindow('fisheye', cv2.WINDOW_NORMAL)

    scale = 0.33

    # get cap property
    cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale   # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale  # float
    # x, y = round(400), round(400)
    # w, h = round(width - 2*x), round(height - 2*y)
    cv2.resizeWindow('fisheye', round(width), round(height))
    # K = [fx 0 cx]
    #     [0 fy cy]
    #     [0  0  1]

    K = np.array([[width/3,     0.,  width/2],
                  [0.,   width/3,   height/2],
                  [0.,     0.,     1.]])

    # zero distortion coefficients work well for this image
    D = np.array([0., 0., 0., 0.])

    # use Knew to scale the output
    Knew = K.copy()
    # Knew[(0, 1), (0, 1)] = 1.1 * Knew[(0, 1), (0, 1)]

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            dst_frame = cv2.resize(frame, None, fx=scale, fy=scale)
            # frame_cropped = frame[y:y+h, x:x+w]
            # frame_undistorted = dst_frame
            frame_undistorted = cv2.fisheye.undistortImage(
                dst_frame, K, D=D, Knew=Knew)

            # Create a 4D blob from a frame.
            blob = cv2.dnn.blobFromImage(
                frame_undistorted, 1/255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)
            # blob = cv2.dnn.blobFromImage(
            #     frame_undistorted, swapRB=True, crop=False)
            # Sets the input to the network
            net.setInput(blob)

            # Runs the forward pass to get output of the output layers
            outs = net.forward(getOutputsNames(net))

            # Remove the bounding boxes with low confidence
            postprocess(frame_undistorted, outs)

            # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
            t, _ = net.getPerfProfile()
            label = 'Inference time: %.2f ms' % (
                t * 1000.0 / cv2.getTickFrequency())
            cv2.putText(frame_undistorted, label, (0, 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

            # Display the resulting frame
            cv2.imshow('fisheye', frame_undistorted)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            # time.sleep(.500)

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
