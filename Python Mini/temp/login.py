from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql
import os.path
import cv2
import sys
import numpy as np
from time import sleep
# All the Function

# Message box fucntion


def message_box():
    messagebox.showinfo("Yes")

# Close Function


def Close():
    temp = messagebox.askyesno("Warring", "Do you want to Close")
    if (temp):
        root.destroy()  # to close the window

# getting the user name 
def getuser(): 
    username_txt = user_id.get()
    return username_txt


# login function
def Login():
    if (user_id.get() == "" and pwd.get() == ""):
        messagebox.showerror("Error", "Plz Enter right Details")
    else:
        try:
            conn = pymysql.connect(
                host="localhost", user="root", password="root", database="stock")
            cur = conn.cursor()
            cur.execute("select  * from login where username = %s", (user_id.get()))
            temp = cur.fetchone()
            if (temp != None):
                cur.execute("select  * from login where password = %s", (pwd.get()))
                temp = cur.fetchone()
                getuser()
                print(username_txt)
                if(temp != "None"):
                    temp = temp[2]
                    if(temp == "Admin"):
                        root.destroy()  
                        import Stockin  
                    elif(temp == "ein"): 
                        root.destroy()  
                        import Stockin 
                    elif(temp == "eout"): 
                        root.destroy()  
                        import Stockout
                    else: 
                        messagebox.showerror("Error", "Something went wrong")
                else: 
                    messagebox.showerror("Error", "Check the Password")
            else:
                messagebox.showerror("Error", "User Not Found")
        except Exception as es:
            messagebox.showerror(
                "Error", "Plz Enter right Details , " + str(es))
    

# Face Login function 
def Facelogin(): 
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
        clf.write("classifier.xml")


    train_classifier("data")


    def draw_boundar(Img, classifier, scalefactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(
            gray_image, scalefactor, minNeighbors)
        coords = []
        for(x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            id, pred = clf.predict(gray_image[y:y+h,x:x+w])
            confidence = int(100*(1 - pred/300))
            if (confidence > 77):
                if id == 1:
                    temp = cv2.putText(img, "Admin", (x, y-5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
                    sleep(4)
                    root.destroy()
                    import Stockout
                    break
                     
                if id == 2:
                    cv2.putText(img, "Ein1", (x, y-5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
                if id == 3:
                    cv2.putText(img, "Ein2", (x, y-5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
            else:
                cv2.putText(img, "Unknow", (x, y-5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            coords = [x, y, w, h]
        return coords


    def recognizers(Img, clf, faceCascade):
        coords = draw_boundar(Img, faceCascade, 1.1, 10,
                            (255, 255, 255), "face", clf)
        return Img


    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")
    video_capture = cv2.VideoCapture(1)
    while True:
        ret, img = video_capture.read();
        # if not img is None: 
        if not ret: continue             
        img = recognizers(img, clf, faceCascade)
        cv2.imshow("face Detection", img)
        if cv2.waitKey(1) == 13:
                break
            
    video_capture.release()
    cv2.destroyAllWindows()
   

# Root to make a root window and set the window size
root = Tk()
root.geometry("1366x768")
root.configure(bg='#FFFFFF')
root.title("Retail Management")


# background image input
BgImg = ImageTk.PhotoImage(Image.open("image/bgwall.png"))
Bg = Label(image=BgImg)
Bg.configure(bg='#FFFFFF')
Bg.place(relx=1, x=0, y=0, anchor=NE)

# Adding header
header = ImageTk.PhotoImage(Image.open("image/head.png"))
head = Label(image=header)
head.configure(bg='#FFFFFF')
head.place(relx=0.45, anchor=NE)

# adding login text
logintxt = ImageTk.PhotoImage(Image.open("image/Logintxt.png"))
login = Label(image=logintxt)
login.configure(bg='#FFFFFF')
login.place(relx=0.33, rely=0.34, anchor=NE)

# adding Face ID Button
FaceID = ImageTk.PhotoImage(Image.open("image/face_id.png"))
Fbtn = Button(root, image=FaceID , command = Facelogin)
Fbtn.configure(bd=0, bg='#ffffff')
Fbtn.place(relx=0.13, rely=0.52, anchor=NE)

# Input box for User ID
user_txt = Canvas(root, width=1, height=1)
user_txt.place(relx=0.3, rely=0.6, anchor=NE)
UserID_txt = Label(root, text='User ID :')
UserID_txt.config(font=('Arial Rounded MT', 20), bg='#FFFFFF')
user_id = Entry(root, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                highlightcolor="black", justify="center", textvariable="Usertxt")
user_txt.create_window(450, 250, window=user_id)
UserID_txt.place(relx=0.25, rely=0.52, anchor=NE)
user_id.place(relx=0.4, rely=0.53, anchor=NE)

# Input box for Password
pwd_txt = Canvas(root, width=1, height=1)
pwd_txt.place(relx=0.5, rely=0.8, anchor=NE)
Pwd_txt = Label(root, text='Password :')
Pwd_txt.config(font=('Arial Rounded MT', 20), bg='#FFFFFF')
pwd = Entry(root, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
            highlightcolor="black", justify="center", textvariable="Pwdtxt", show='*')
pwd_txt.create_window(450, 250, window=pwd)
Pwd_txt.place(relx=0.25, rely=0.62, anchor=NE)
pwd.place(relx=0.4, rely=0.63, anchor=NE)

# Login Btn
Login_img = ImageTk.PhotoImage(Image.open("image/LoginBtn.png"))
LoginBtn = Button(root, image=Login_img, command=Login)
LoginBtn.configure(bd=0, bg='#ffffff')
LoginBtn.place(relx=0.4, rely=0.7, anchor=NE)

# Close Btn
Close_img = ImageTk.PhotoImage(Image.open("image/CloseBtn.png"))
CloseBtn = Button(root, image=Close_img, command=Close)
CloseBtn.configure(bd=0, bg='#ffffff')
CloseBtn.place(relx=0.25, rely=0.7, anchor=NE)



# other use varavles 


# to run the window
root.state('zoomed')
root = mainloop()
