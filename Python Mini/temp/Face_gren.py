import cv2
from PIL import Image
import numpy as np
import os.path
import pymysql


def generate():
    face_classifier = cv2.CascadeClassifier(
        "Python Mini/haarcascade_frontalface_default.xml")

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces == ():
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
            return cropped_face
    cap = cv2.VideoCapture(1)
    id = 4
    img_id = 0
    while True:
        ret, frame = cap.read()
        if face_cropped(frame) is not None:
            img_id += 1
            face = cv2.resize(face_cropped(frame), (250, 250))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = "data/user_" + \
                str(id) + "_" + str(img_id) + ".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(img_id), (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Cropped face", face)
            if cv2.waitKey(1) == 13 or int(img_id) == 50:
                break
    cap.release()

    cv2.destroyAllWindows()
    print("Working....")
generate()


def train_classifier(data):
    path = [os.path.join(data, f) for f in os.listdir(data)]
    faces = []
    ids = []
    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split("_")[1])
        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids)
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("Python Mini/classifier.xml")


# train_classifier("data")


def draw_boundar(Img, classifier, scalefactor, minNeighbors, color, text, clf):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(
        gray_image, scalefactor, minNeighbors)
    temp = 0
    coords = []
    conn = pymysql.connect(
        host="localhost", user="root", password="root", database="stock")
    cur = conn.cursor()
    cur.execute("Select * from login")
    d = cur.fetchall()
    ad = []
    ein = []
    eout = []
    num = 0
    for i in d:
        num += 1
        e = str(num)
        cur.execute("select  * from login where id = %s", e)
        temp = cur.fetchone()
        if temp[3] == "Admin":
            ad.append(temp[0])
        if temp[3] == "In":
            ein.append(temp[0])
        if temp[3] == "Out":
            eout.append(temp[0])

    for(x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        id, pred = clf.predict(gray_image[y:y+h, x:x+w])
        confidence = int(100*(1 - pred/300))
        if (confidence > 75):
            if id in ad:
                cv2.putText(img, "Admin", (x+70, y-5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
                temp = 1
            if id in ein:
                cv2.putText(img, "Ein", (x+80, y-5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
                temp = 2

            if id in eout:
                cv2.putText(img, "Eout", (x+70, y-5),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
                temp = 3
        else:
            cv2.putText(img, "Unknow", (x, y-5),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            temp = 100
        coords = [x, y, w, h]
    return coords, temp


def recognizers(Img, clf, faceCascade):
    coords, temp = draw_boundar(Img, faceCascade, 1.1, 10,
                                (255, 255, 255), "face", clf)
    return Img, temp


faceCascade = cv2.CascadeClassifier("Python Mini/haarcascade_frontalface_default.xml")
clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("Python Mini/classifier.xml")
video_capture = cv2.VideoCapture(1)
temp = 0
while True:
    ret, img = video_capture.read()
    # if not img is None:
    if not ret:
        continue
    img, temp = recognizers(img, clf, faceCascade)
    cv2.imshow("face Detection", img)
    if cv2.waitKey(1) == 13:
        break

# video_capture.release()
cv2.destroyAllWindows()
