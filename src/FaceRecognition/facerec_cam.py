import face_recognition
import cv2

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture(0)

# # Load a sample picture and learn how to recognize it.
# tu_image = face_recognition.load_image_file("tu.png")
# tu_face_encoding = face_recognition.face_encodings(tu_image)[0]

# Load a second sample picture and learn how to recognize it.
known_face_encoding1 = face_recognition.face_encodings(
    face_recognition.load_image_file('agiletech/know/dung.jpg'))[0]
known_face_encoding2 = face_recognition.face_encodings(
    face_recognition.load_image_file('agiletech/know/khanh.jpg'))[0]
known_face_encoding3 = face_recognition.face_encodings(
    face_recognition.load_image_file('agiletech/know/tu.jpg'))[0]
known_face_encoding4 = face_recognition.face_encodings(
    face_recognition.load_image_file('agiletech/know/tuan.jpg'))[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    known_face_encoding1,
    known_face_encoding2,
    known_face_encoding3,
    known_face_encoding4
]
known_face_names = [
    "Dung",
    "Khanh",
    "Tu",
    "Tuan"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
tolerance = 0.4
scale = 1

# while True:
# # Grab a single frame of video
# ret, frame = video_capture.read()

# # Resize frame of video to 1/4 size for faster face recognition processing
# small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

# frame = cv2.imread('agiletech/unknown/agiletech.jpg')
# frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# rgb_small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

frame = cv2.imread('agiletech/unknown/agiletech.jpg', cv2.IMREAD_COLOR)
small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
rgb_small_frame = small_frame[:, :, ::-1]

# Only process every other frame of video to save time
# if process_this_frame:
# Find all the faces and face encodings in the current frame of video
# image = face_recognition.load_image_file('agiletech/unknown/agiletech.jpg')
# face_locations = face_recognition.face_locations(image, model="cnn")

face_locations = face_recognition.face_locations(rgb_small_frame)
face_encodings = face_recognition.face_encodings(
    rgb_small_frame, face_locations)

face_names = []
for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
    distances = face_recognition.face_distance(
        known_face_encodings, face_encoding)
    name = "Unknown"

    distance = max(distances)
    if distance <= tolerance:
        index = [i for i, j in enumerate(distances) if j == distance][0]
        name = known_face_names[index]

    face_names.append(name + ":" + str(round(distance * 100, 2)) + "%")

# process_this_frame = not process_this_frame

# Display the results
for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    top = round(top / scale)
    right = round(right / scale)
    bottom = round(bottom / scale)
    left = round(left / scale)

    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    font = cv2.FONT_HERSHEY_DUPLEX
    labelSize, baseLine = cv2.getTextSize(
        name, font, 1.0, 1)
    cv2.rectangle(frame, (left, bottom - labelSize[1]),
                  (left + labelSize[0], bottom + baseLine), (0, 0, 255), cv2.FILLED)

    cv2.putText(frame, name, (left + 6, bottom + baseLine - 6),
                font, 1.0, (255, 255, 255), 1)

# Display the resulting image
# cv2.imshow('agiletech', frame)
cv2.imwrite('result.jpg', frame)

# # Hit 'q' on the keyboard to quit!
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     break

# Release handle to the webcam
# video_capture.release()
# cv2.destroyAllWindows()
