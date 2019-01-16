import face_recognition

known_image = face_recognition.load_image_file("khanh.jpg")
khanh_face_encoding = face_recognition.face_encodings(known_image)[0]
unknown_image = face_recognition.load_image_file("unknown.jpg")
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
known_face_encodings = [
    # tu_face_encoding,
    khanh_face_encoding
]
known_face_names = [
    # "Pham Thanh Tu",
    "Pham Gia Khanh"
]

matches = face_recognition.face_distance(
    known_face_encodings, unknown_encoding)
print(matches)
# for index, match in enumerate(matches):
#     if match:
#         name = known_face_names[index]
#         print(name)
