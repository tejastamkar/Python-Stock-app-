from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import datetime
from tkinter import messagebox
import pymysql
import cv2
import os.path
import numpy as np


cameraport = 0
conn = pymysql.connect(
    host="localhost", user="root", password="root", database="stock")
cur = conn.cursor()


class Loginscreen:
    def main(self):
        def Close():
            temp = messagebox.askyesno("Warring", "Do you want to Close")
            if (temp):
                root.destroy()

        # getting the user name
        def getuser(self):
            username_txt = user_id.get()
            return username_txt

        def Login(event=None):
            if (user_id.get() == "" and pwd.get() == ""):
                messagebox.showerror("Error", "Plz Enter right Details")
            else:
                try:

                    cur.execute(
                        "select  * from login where Username = %s", (user_id.get()))
                    temp = cur.fetchone()
                    if (temp != None):
                        cur.execute(
                            "select  * from login where Password = %s", (pwd.get()))
                        temp = cur.fetchone()
                        username_txt = getuser(self)
                        if (temp != None):
                            temp = temp[3]
                            if (temp == "Admin"):
                                root.destroy()
                                ad.main()
                            elif (temp == "In"):
                                root.destroy()
                                Sin.main()
                            elif (temp == "Out"):
                                root.destroy()
                                Sout.main()
                            else:
                                messagebox.showerror(
                                    "Error", "Something went wrong")
                        else:
                            messagebox.showerror("Error", "Check the Password")
                    else:
                        messagebox.showerror("Error", "User Not Found")
                except Exception as es:
                    temp = messagebox.askyesno(
                        "Error", "Plz Check the Inputed Details ")
                    if (temp != True):
                        messagebox.showerror(
                            "Error", "Plz Enter right Details , " + str(es))

        # Close Function

        def Close():
            temp = messagebox.askyesno("Warring", "Do you want to Close")
            if (temp):
                root.destroy()  # to close the window
        # face_id Function

        def getface():
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

            train_classifier("Python Mini/data")

            def draw_boundar(Img, classifier, scalefactor, minNeighbors, color, text, clf):
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                features = classifier.detectMultiScale(
                    gray_image, scalefactor, minNeighbors)
                temp = 0
                coords = []

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
                for (x, y, w, h) in features:
                    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                    id, pred = clf.predict(gray_image[y:y+h, x:x+w])
                    confidence = int(100*(1 - pred/300))
                    if (confidence > 88):
                        if id in ad:
                            cv2.putText(img, "Admin", (x, y-5),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
                            temp = 1
                        if id in ein:
                            cv2.putText(img, "Ein", (x, y-5),
                                        cv2.FONT_HERSHEY_COMPLEX, 0.8, color, 1, cv2.LINE_AA)
                            temp = 2

                        if id in eout:
                            cv2.putText(img, "Eout", (x, y-5),
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

            faceCascade = cv2.CascadeClassifier(
                "Python Mini/haarcascade_frontalface_default.xml")
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("Python Mini/classifier.xml")
            video_capture = cv2.VideoCapture(cameraport)
            temp = 0
            while True:
                ret, img = video_capture.read()
                # if not img is None:
                if not ret:
                    continue
                img, temp = recognizers(img, clf, faceCascade)
                cv2.imshow("face Detection", img)
                cout = 1
                cout += 1
                if cv2.waitKey(1) == 13 or cout == 100:
                    break
            video_capture.release()
            cv2.destroyAllWindows()
            if temp == 1:
                root.destroy()
                ad.main()
            elif temp == 2:
                root.destroy()
                Sin.main()
            elif temp == 3:
                root.destroy()
                Sout.main()
            else:
                messagebox.showerror(
                    "Error", "User not found try again or login with ID and Password")

        root = Tk()
        root.geometry("1366x768")
        root.configure(bg='#FFFFFF')
        root.title("Retail Management")

        # background image input
        BgImg = ImageTk.PhotoImage(Image.open("Python Mini/Image/bgwall.png"))
        Bg = Label(image=BgImg)
        Bg.configure(bg='#FFFFFF')
        Bg.place(relx=1, x=0, y=0, anchor=NE)

        # Adding header
        header = ImageTk.PhotoImage(Image.open("Python Mini/Image/Head.png"))
        head = Label(image=header)
        head.configure(bg='#FFFFFF')
        head.place(relx=0.45, anchor=NE)

        # adding login text
        logintxt = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/Logintxt.png"))
        login = Label(image=logintxt)
        login.configure(bg='#FFFFFF')
        login.place(relx=0.33, rely=0.34, anchor=NE)

        # adding Face ID Button
        FaceID = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/face_id.png"))
        Fbtn = Button(root, image=FaceID, command=getface)
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
        user_id.focus_set()

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
        Login_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/LoginBtn.png"))
        LoginBtn = Button(root, image=Login_img, command=Login)
        LoginBtn.configure(bd=0, bg='#ffffff')
        LoginBtn.place(relx=0.4, rely=0.7, anchor=NE)
        root.bind('<Return>', Login)

        # Close Btn
        Close_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/CloseBtn.png"))
        CloseBtn = Button(root, image=Close_img, command=Close)
        CloseBtn.configure(bd=0, bg='#ffffff')
        CloseBtn.place(relx=0.25, rely=0.7, anchor=NE)

        root.state('zoomed')
        root.mainloop()


class Stockin:
    def main(self):
        # logout function

        def Logout():
            temp = messagebox.askyesno("Warring", "Do you want to Close")
            if (temp):
                cleardata()
                stockin.destroy()
                L.main()

        def cleardata():
            for record in instock_tv.get_children():
                instock_tv.delete(record)
            for record in outstock_tv.get_children():
                outstock_tv.delete(record)

        def Insert(event=None):
            hour = str(e.hour)
            minute = str(e.minute)
            sec = str(e.second)
            day = str(e.day)
            month = str(e.month)
            year = str(e.year)
            realtime = (hour + ":" + minute + ":" + sec)
            realdate = (year + "-" + month + "-" + day)
            Time = (hr.get() + ":" + mins.get())
            stock_name = name.get()
            date_forinsert = date.get()
            sql = "INSERT INTO stockin VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, (date_forinsert, stock_name,
                        Time, Username, realtime, realdate))
            conn.commit()
            name.delete(0, 'end')
            date.delete(0, 'end')
            hr.delete(0, 'end')
            mins.delete(0, 'end')
            cleardata()
            date.focus_set()
            stockcall(instock_tv, outstock_tv)
            return True

        # sql treeveiw query

        def stockcall(instock_tv, outstock_tv):
            sql = "select * from stockin ORDER by Date DESC"
            cur.execute(sql)
            rows = cur.fetchall()
            sql = "select * from stockout ORDER by Date DESC"
            cur.execute(sql)
            rows_out = cur.fetchall()
            for i in rows:
                instock_tv.insert('', 'end', values=i)
            for i in rows_out:
                outstock_tv.insert('', 'end', values=i)
            return rows, rows_out

        # stockin to make a stockin window and set the window size
        stockin = Tk()
        stockin.geometry("1366x768")
        stockin.configure(bg='#FFFFFF')
        stockin.title("Retail Management")

        # header image input
        header = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/In_head.png"))
        head = Label(image=header)
        head.configure(bg='#FFFFFF')
        head.place(relx=0.40, rely=0.31, anchor=NE)
        username = Username = ("Ein")
        e = datetime.datetime.now()

        # Logo image
        Frame = Image.open("Python Mini/Image/logo.png")
        Frame = ImageTk.PhotoImage(Frame)
        frame = Label(image=Frame)
        frame.configure(bg='#FFFFFF')
        frame.place(relx=0.30, anchor=NE)

        #  data btn and label
        date_txt = Label(stockin, text='Date: ')
        date_hint = Label(stockin, text='YYYY-MM-DD')
        date_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        date_txt.place(relx=0.08, rely=0.53, anchor=NE)
        date_hint.configure(font=('Arial Rounded MT', 14), bg='#FFFFFF')
        date_hint.place(relx=0.17, rely=0.54, anchor=NE)
        #  select btn for date
        Date_txt = Canvas(stockin, width=1, height=1)
        Date_txt.place(relx=0.3, rely=0.6, anchor=NE)
        date = Entry(stockin, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                     highlightcolor="black", justify="center", textvariable="datetxt")
        Date_txt.create_window(450, 250, window=date)
        date.place(relx=0.39, rely=0.54, anchor=NE)

        # Name txt for stock
        Name_txt = Label(stockin, text='Name of the Stock:')
        Name_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        Name_txt.place(relx=0.198, rely=0.64, anchor=NE)
        name_txt = Canvas(stockin, width=1, height=1)
        name_txt.place(relx=0.3, rely=0.6, anchor=NE)
        name = Entry(stockin, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                     highlightcolor="black", justify="center", textvariable="Usertxt")
        name_txt.create_window(450, 250, window=name)
        name.place(relx=0.39, rely=0.65, anchor=NE)

        # Time  txt and Btn
        time_txt = Label(stockin, text='Time:')
        time_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        time_txt.place(relx=0.08, rely=0.75, anchor=NE)
        #  select btn for Time
        # hr txt and input box
        hr_txt = Label(stockin, text='Hour')
        hr_txt.configure(font=('Arial Rounded MT', 14), bg='#FFFFFF')
        hr_txt.place(relx=0.28, rely=0.76, anchor=NE)
        Hr_txt = Canvas(stockin, width=1, height=1)
        Hr_txt.place(relx=0.3, rely=0.6, anchor=NE)
        hr = Entry(stockin, width=5, font=('Arial Rounded MT', 10), borderwidth=2,
                   highlightcolor="black", justify="center", textvariable="hrtxt")
        Hr_txt.create_window(10, 30, window=hr)
        hr.place(relx=0.31, rely=0.765, anchor=NE)
        # mins txt and input box
        min_txt = Label(stockin, text='Minutes')
        min_txt.configure(font=('Arial Rounded MT', 14), bg='#FFFFFF')
        min_txt.place(relx=0.36, rely=0.76, anchor=NE)
        Min_txt = Canvas(stockin, width=1, height=1)
        Min_txt.place(relx=0.3, rely=0.6, anchor=NE)
        mins = Entry(stockin, width=5, font=('Arial Rounded MT', 10), borderwidth=2,
                     highlightcolor="black", justify="center", textvariable="mintxt")
        Min_txt.create_window(10, 30, window=mins)
        mins.place(relx=0.39, rely=0.765, anchor=NE)

        # Insert Btn
        insert_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/InsertBtn.png"))
        InsertBtn = Button(stockin, image=insert_img, command=Insert)
        InsertBtn.configure(bd=0, bg='#ffffff')
        InsertBtn.place(relx=0.4, rely=0.85, anchor=NE)

        # Logout Btn
        Logout_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/LogoutBtn.png"))
        LogoutBtn = Button(stockin, image=Logout_img, command=Logout)
        LogoutBtn.configure(bd=0, bg='#ffffff')
        LogoutBtn.place(relx=0.14, rely=0.85, anchor=NE)

        # Instock table txt
        instock_txt = Label(stockin, text='In Stock Table:')
        instock_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        instock_txt.place(relx=0.53, anchor=NW)
        # Instock table view
        instock_tv = ttk.Treeview(stockin, columns=(
            1, 2, 3), show="headings", height=14)
        instock_tv['columns'] = ('Date', 'Name', 'Time')
        instock_tv.column('Date', anchor=CENTER, width=200)
        instock_tv.column('Name', anchor=CENTER, width=200)
        instock_tv.column('Time', anchor=CENTER, width=200)
        # instock_tv.column(, width=0, stretch=NO)
        instock_tv.heading(0, text="Date")
        instock_tv.heading(1, text="Name")
        instock_tv.heading(2, text="Time")

        instock_tv.place(relx=0.5, rely=0.07, anchor=NW)

        # Outstock table txt
        outstock_txt = Label(stockin, text='Out Stock Table:')
        outstock_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        outstock_txt.place(relx=0.53, rely=0.5, anchor=NW)
        # outstock table view
        outstock_tv = ttk.Treeview(stockin, columns=(
            1, 2, 3), show="headings", height=14)
        outstock_tv['columns'] = ('Date', 'Name', 'Time')
        outstock_tv.column('Date', anchor=CENTER, width=200)
        outstock_tv.column('Name', anchor=CENTER, width=200)
        outstock_tv.column('Time', anchor=CENTER, width=200)
        outstock_tv.heading(0, text="Date")
        outstock_tv.heading(1, text="Name")
        outstock_tv.heading(2, text="Time")

        rows, rows_out = stockcall(instock_tv, outstock_tv)
        outstock_tv.place(relx=0.5, rely=0.57, anchor=NW)
        stockin.state('zoomed')
        stockin.bind('<Return>', Insert)
        stockin.mainloop()


class Stockout:
    def main(self):
        def Logout():
            temp = messagebox.askyesno("Warring", "Do you want to Close")
            if (temp):
                cleardata()
                stockout.destroy()
                L.main()

        def cleardata():
            for record in instock_tv.get_children():
                instock_tv.delete(record)
            for record in outstock_tv.get_children():
                outstock_tv.delete(record)

        def Insert(event=None):
            hour = str(e.hour)
            minute = str(e.minute)
            sec = str(e.second)
            day = str(e.day)
            month = str(e.month)
            year = str(e.year)
            realtime = (hour + ":" + minute + ":" + sec)
            realdate = (year + "-" + month + "-" + day)
            Time = (hr.get() + ":" + mins.get())
            stock_name = name.get()
            date_forinsert = date.get()
            sql = "INSERT INTO stockout VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, (date_forinsert, stock_name,
                        Time, username, realtime, realdate))
            conn.commit()
            name.delete(0, 'end')
            date.delete(0, 'end')
            hr.delete(0, 'end')
            mins.delete(0, 'end')
            cleardata()
            date.focus_set()
            stockcall(instock_tv, outstock_tv)
            return True

        # sql treeveiw query

        def stockcall(instock_tv, outstock_tv):
            sql = "select * from stockin ORDER by Date DESC"
            cur.execute(sql)
            rows = cur.fetchall()
            sql = "select * from stockout ORDER by Date DESC"
            cur.execute(sql)
            rows_out = cur.fetchall()
            for i in rows:
                instock_tv.insert('', 'end', values=i)
            for i in rows_out:
                outstock_tv.insert('', 'end', values=i)
            return rows, rows_out

        # stockout to make a stockout window and set the window size
        stockout = Tk()
        stockout.geometry("1366x768")
        stockout.configure(bg='#FFFFFF')
        stockout.title("Retail Management")

        # header image input
        header = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/out_head.png"))
        head = Label(image=header)
        head.configure(bg='#FFFFFF')
        head.place(relx=0.40, rely=0.31, anchor=NE)
        username = ("Eout")
        e = datetime.datetime.now()
        # Logo image
        Frame = Image.open("Python Mini/Image/logo.png")
        Frame = ImageTk.PhotoImage(Frame)
        frame = Label(image=Frame)
        frame.configure(bg='#FFFFFF')
        frame.place(relx=0.30, anchor=NE)

        #  data btn and label
        date_txt = Label(stockout, text='Date: ')
        date_hint = Label(stockout, text='YYYY-MM-DD')
        date_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        date_txt.place(relx=0.08, rely=0.53, anchor=NE)
        date_hint.configure(font=('Arial Rounded MT', 14), bg='#FFFFFF')
        date_hint.place(relx=0.17, rely=0.54, anchor=NE)
        #  select btn for date
        Date_txt = Canvas(stockout, width=1, height=1)
        Date_txt.place(relx=0.3, rely=0.6, anchor=NE)
        date = Entry(stockout, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                     highlightcolor="black", justify="center", textvariable="datetxt")
        Date_txt.create_window(450, 250, window=date)
        date.place(relx=0.39, rely=0.54, anchor=NE)

        # Name txt for stock
        Name_txt = Label(stockout, text='Name of the Stock:')
        Name_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        Name_txt.place(relx=0.198, rely=0.64, anchor=NE)
        name_txt = Canvas(stockout, width=1, height=1)
        name_txt.place(relx=0.3, rely=0.6, anchor=NE)
        name = Entry(stockout, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                     highlightcolor="black", justify="center", textvariable="Usertxt")
        name_txt.create_window(450, 250, window=name)
        name.place(relx=0.39, rely=0.65, anchor=NE)

        # Time  txt and Btn
        time_txt = Label(stockout, text='Time:')
        time_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        time_txt.place(relx=0.08, rely=0.75, anchor=NE)
        #  select btn for Time
        # hr txt and input box
        hr_txt = Label(stockout, text='Hour')
        hr_txt.configure(font=('Arial Rounded MT', 14), bg='#FFFFFF')
        hr_txt.place(relx=0.28, rely=0.76, anchor=NE)
        Hr_txt = Canvas(stockout, width=1, height=1)
        Hr_txt.place(relx=0.3, rely=0.6, anchor=NE)
        hr = Entry(stockout, width=5, font=('Arial Rounded MT', 10), borderwidth=2,
                   highlightcolor="black", justify="center", textvariable="hrtxt")
        Hr_txt.create_window(10, 30, window=hr)
        hr.place(relx=0.31, rely=0.765, anchor=NE)
        # mins txt and input box
        min_txt = Label(stockout, text='Minutes')
        min_txt.configure(font=('Arial Rounded MT', 14), bg='#FFFFFF')
        min_txt.place(relx=0.36, rely=0.76, anchor=NE)
        Min_txt = Canvas(stockout, width=1, height=1)
        Min_txt.place(relx=0.3, rely=0.6, anchor=NE)
        mins = Entry(stockout, width=5, font=('Arial Rounded MT', 10), borderwidth=2,
                     highlightcolor="black", justify="center", textvariable="mintxt")
        Min_txt.create_window(10, 30, window=mins)
        mins.place(relx=0.39, rely=0.765, anchor=NE)

        # Insert Btn
        insert_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/InsertBtn.png"))
        InsertBtn = Button(stockout, image=insert_img, command=Insert)
        InsertBtn.configure(bd=0, bg='#ffffff')
        InsertBtn.place(relx=0.4, rely=0.85, anchor=NE)

        # Logout Btn
        Logout_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/LogoutBtn.png"))
        LogoutBtn = Button(stockout, image=Logout_img, command=Logout)
        LogoutBtn.configure(bd=0, bg='#ffffff')
        LogoutBtn.place(relx=0.14, rely=0.85, anchor=NE)

        # Instock table txt
        instock_txt = Label(stockout, text='In Stock Table:')
        instock_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        instock_txt.place(relx=0.53, rely=0.5, anchor=NW)
        # Instock table view
        instock_tv = ttk.Treeview(stockout, columns=(
            1, 2, 3), show="headings", height=14)
        instock_tv['columns'] = ('Date', 'Name', 'Time')
        instock_tv.column('Date', anchor=CENTER, width=200)
        instock_tv.column('Name', anchor=CENTER, width=200)
        instock_tv.column('Time', anchor=CENTER, width=200)
        # instock_tv.column(, width=0, stretch=NO)
        instock_tv.heading(0, text="Date")
        instock_tv.heading(1, text="Name")
        instock_tv.heading(2, text="Time")

        instock_tv.place(relx=0.5, rely=0.57, anchor=NW)

        # Outstock table txt
        outstock_txt = Label(stockout, text='Out Stock Table:')
        outstock_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        outstock_txt.place(relx=0.53, anchor=NW)
        # outstock table view
        outstock_tv = ttk.Treeview(stockout, columns=(
            1, 2, 3), show="headings", height=14)
        outstock_tv['columns'] = ('Date', 'Name', 'Time')
        outstock_tv.column('Date', anchor=CENTER, width=200)
        outstock_tv.column('Name', anchor=CENTER, width=200)
        outstock_tv.column('Time', anchor=CENTER, width=200)
        outstock_tv.heading(0, text="Date")
        outstock_tv.heading(1, text="Name")
        outstock_tv.heading(2, text="Time")

        rows, rows_out = stockcall(instock_tv, outstock_tv)
        outstock_tv.place(relx=0.5, rely=0.07, anchor=NW)
        stockout.state('zoomed')
        stockout.bind('<Return>', Insert)
        stockout.mainloop()


class Admin:
    # logout function
    def main(self):
        def Logout():
            temp = messagebox.askyesno("Warring", "Do you want to Close")
            if (temp):
                cleardata()
                admin.destroy()
                L.main()

        def cleardata():
            for record in instock_tv.get_children():
                instock_tv.delete(record)
            for record in outstock_tv.get_children():
                outstock_tv.delete(record)

        def reg():
            admin.destroy()
            Sign.main()
            return True

        admin = Tk()
        admin.geometry("1366x768")
        admin.configure(bg='#FFFFFF')
        admin.title("Retail Management")

        def stockcall(instock_tv, outstock_tv, Admin_tv):
            sql = "select * from stockin ORDER by Date DESC"
            cur.execute(sql)
            rows = cur.fetchall()
            sql = "select * from stockout ORDER by Date DESC"
            cur.execute(sql)
            rows_out = cur.fetchall()
            sql = "select * from login"
            cur.execute(sql)
            rows_ad = cur.fetchall()
            for i in rows:
                instock_tv.insert('', 'end', values=i)
            for i in rows_out:
                outstock_tv.insert('', 'end', values=i)
            for i in rows_ad:
                Admin_tv.insert('', 'end', values=i)
            return rows, rows_out, rows_ad

        # User Info
        e = datetime.datetime.now()
        User_name = Label(admin, text='User:Admin')
        hour = str(e.hour)
        minute = str(e.minute)
        sec = str(e.second)
        day = str(e.day)
        month = str(e.month)
        year = str(e.year)
        txt = 'Update Database on\nDate:' + day + '-' + month + \
            '-' + year + '\nTime: '+hour+':'+minute+':'+sec
        date_txt = Label(admin, text=txt)
        User_name.configure(font=('Arial Rounded MT', 20),
                            justify=LEFT, bg='#FFFFFF', fg='#989898')
        User_name.place(relx=0.999, anchor=NE)
        date_txt.configure(font=('Arial Rounded MT', 18),
                           justify=LEFT, bg='#FFFFFF')
        date_txt.place(relx=0.18, rely=0.35, anchor=NE)

        # adding logo
        header = ImageTk.PhotoImage(Image.open("Python Mini/Image/logo.png"))
        logo = Label(image=header)
        logo.configure(bg='#FFFFFF')
        logo.place(relx=0.35, anchor=NE)
        # Insert Btn
        regbtn_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/SignupBtn.png"))
        regBtn = Button(admin, image=regbtn_img, command=reg)
        regBtn.configure(bd=0, bg='#ffffff')
        regBtn.place(relx=0.24, rely=0.25, anchor=NE)

        # Logout Btn
        Logout_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/Admin_LogoutBtn.png"))
        LogoutBtn = Button(admin, image=Logout_img, command=Logout)
        LogoutBtn.configure(bd=0, bg='#ffffff')
        LogoutBtn.place(relx=0.48, rely=0.25,  anchor=NE)

        # Admin table txt
        Admintbl_txt = Label(admin, text='Admin Table:')
        Admintbl_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        Admintbl_txt.place(relx=0.53, rely=0.01, anchor=NW)
        Admin_tv = ttk.Treeview(admin, columns=(
            1, 2, 3), show="headings", height=13)
        Admin_tv['columns'] = ('Username', 'Password', 'Type', "Name")
        Admin_tv.column('Username', anchor=CENTER, width=165)
        Admin_tv.column('Password', anchor=CENTER, width=165)
        Admin_tv.column('Type', anchor=CENTER, width=165)
        Admin_tv.column('Name', anchor=CENTER, width=165)

        Admin_tv.heading(0, text="Username")
        Admin_tv.heading(1, text="Password")
        Admin_tv.heading(2, text="Type")
        Admin_tv.heading(3, text="Name")

        Admin_tv.place(relx=0.5, rely=0.07, anchor=NW)

        # Instock table txt
        instock_txt = Label(admin, text='In Stock Table:')
        instock_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        instock_txt.place(relx=0.156, rely=0.5, anchor=NE)
        # Instock table view
        instock_tv = ttk.Treeview(admin, columns=(
            1, 2, 3), show="headings", height=15)
        instock_tv['columns'] = ('Date', 'Name', 'Time',
                                 "Username", "Input time", "Input date")
        instock_tv.column('Date', anchor=CENTER, width=110)
        instock_tv.column('Name', anchor=CENTER, width=110)
        instock_tv.column('Time', anchor=CENTER, width=110)
        instock_tv.column('Username', anchor=CENTER, width=110)
        instock_tv.column('Input time', anchor=CENTER, width=110)
        instock_tv.column('Input date', anchor=CENTER, width=110)

        instock_tv.heading(0, text="Date")
        instock_tv.heading(1, text="Name")
        instock_tv.heading(2, text="Time")
        instock_tv.heading(3, text="Username")
        instock_tv.heading(4, text="Input time")
        instock_tv.heading(5, text="Input date")

        instock_tv.place(relx=0.49, rely=0.55, anchor=NE)

        # Outstock table txt
        outstock_txt = Label(admin, text='Out Stock Table:')
        outstock_txt.configure(font=('Arial Rounded MT', 20), bg='#FFFFFF')
        outstock_txt.place(relx=0.53, rely=0.5, anchor=NW)
        # outstock table view
        outstock_tv = ttk.Treeview(admin, columns=(
            1, 2, 3), show="headings", height=15)
        outstock_tv['columns'] = ('Date', 'Name', 'Time',
                                  "Username", "Input time", "Input date")
        outstock_tv.column('Date', anchor=CENTER, width=110)
        outstock_tv.column('Name', anchor=CENTER, width=110)
        outstock_tv.column('Time', anchor=CENTER, width=110)
        outstock_tv.column('Username', anchor=CENTER, width=110)
        outstock_tv.column('Input time', anchor=CENTER, width=110)
        outstock_tv.column('Input date', anchor=CENTER, width=110)

        outstock_tv.heading(0, text="Date")
        outstock_tv.heading(1, text="Name")
        outstock_tv.heading(2, text="Time")
        outstock_tv.heading(3, text="Username")
        outstock_tv.heading(4, text="Input time")
        outstock_tv.heading(5, text="Input date")

        rows, rows_out, rows_ad = stockcall(instock_tv, outstock_tv, Admin_tv)
        outstock_tv.place(relx=0.5, rely=0.55, anchor=NW)
        admin.state('zoomed')
        admin.mainloop()


class Signup:
    def main(self):
        # All the Function
        # Clear Function
        def Clear():
            user__name.delete(0, 'end')
            user_id.delete(0, 'end')
            pwd.delete(0, 'end')
            re_pwd.delete(0, 'end')

        # Cancel Function

        def Cancel():
            temp = messagebox.askyesno("Warring", "Do you want to Close")
            if (temp):
                Signup.destroy()  # to close the window
                ad.main()

        # Registertion Function

        def Register():
            name = user__name.get()
            userid = user_id.get()
            password = pwd.get()
            acc = Check_acc.get()
            repwd = re_pwd.get()
            if (password == re_pwd.get() and name != " " and userid != " " and password != " "):
                if (acc == "None"):
                    messagebox.showerror("Error", "Select Employee Type")
                else:

                    id = 1
                    cur.execute("select * from login")
                    result = cur.fetchall()
                    for x in result:
                        id += 1
                    sql = "INSERT INTO login VALUES (%s,%s,%s,%s,%s)"
                    id = str(id)
                    cur.execute(sql, (id, userid, password, acc, name))
                    conn.commit()
                    user__name.delete(0, 'end')
                    user_id.delete(0, 'end')
                    pwd.delete(0, 'end')
                    re_pwd.delete(0, 'end')
                    Admin_ty.deselect()
                    InEmp_ty.deselect()
                    OutEmp_ty.deselect()
                    for i in range(1, 51):
                        file_name_path = "Python Mini/data/user_" + \
                            str(id) + "_" + str(i) + ".jpg"
                        # original = r'C:\Users\Ron\Desktop\Test_1\my_folder'
                        # target = r'C:\Users\Ron\Desktop\Test_2\my_folder'
                        # shutil.move(original, target)
            else:
                messagebox.showerror("Error", "Please Enter details Properly")

        def generate():
            face_classifier = cv2.CascadeClassifier(
                "Python Mini/haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 3)
                if faces == ():
                    return None
                for (x, y, w, h) in faces:
                    cropped_face = img[y:y + h, x:x + w]
                    return cropped_face
            cap = cv2.VideoCapture(cameraport)
            id = 1
            cur.execute("select * from login")
            result = cur.fetchall()
            for x in result:
                id += 1
            img_id = 0
            while True:
                ret, frame = cap.read()
                if face_cropped(frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_cropped(frame), (250, 250))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = "Python Mini/data/user_" + \
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

        # Signup to make a Signup window and set the window size
        Signup = Tk()
        Signup.geometry("1366x768")
        Signup.configure(bg='#FFFFFF')
        Signup.title("Retail Management")

        # background image input
        BgImg = ImageTk.PhotoImage(Image.open("Python Mini/Image/Bg_Sign.png"))
        Bg = Label(image=BgImg)
        Bg.configure(bg='#FFFFFF')
        Bg.place(relx=1, x=0, y=0, anchor=NE)

        # Adding header
        header = ImageTk.PhotoImage(Image.open("Python Mini/Image/Head.png"))
        head = Label(image=header)
        head.configure(bg='#FFFFFF')
        head.place(relx=0.75, anchor=NE)

        # adding Registration text
        Regtxt = ImageTk.PhotoImage(Image.open(
            "Python Mini/Image/Registration.png"))
        reg = Label(image=Regtxt)
        reg.configure(bg='#FFFFFF')
        reg.place(relx=0.4, rely=0.065, anchor=NE)

        # adding Face ID Button
        FaceID = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/face_id.png"))
        Fbtn = Button(Signup, image=FaceID, command=generate)
        Fbtn.configure(bd=0, bg='#ffffff')
        Fbtn.place(relx=0.74, rely=0.44, anchor=NE)

        # Input box for User name
        username_txt = Canvas(Signup, width=0, height=0)
        username_txt.place(relx=0.04, rely=0.6, anchor=NE)
        User_name_txt = Label(Signup, text='Enter User Name :')
        User_name_txt.config(font=('Arial Rounded MT', 25), bg='#FFFFFF')
        user__name = Entry(Signup, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                           highlightcolor="black", justify="center", textvariable="Nametxt")
        username_txt.create_window(450, 250, window=user__name)
        User_name_txt.place(relx=0.25, rely=0.42, anchor=NE)
        user__name.place(relx=0.4, rely=0.434, anchor=NE)

        # Input box for User ID
        user_txt = Canvas(Signup, width=0, height=0)
        user_txt.place(relx=0.04, rely=0.6, anchor=NE)
        UserID_txt = Label(Signup, text='Enter User ID :')
        UserID_txt.config(font=('Arial Rounded MT', 25), bg='#FFFFFF')
        user_id = Entry(Signup, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                        highlightcolor="black", justify="center", textvariable="Usertxt")
        user_txt.create_window(450, 250, window=user_id)
        UserID_txt.place(relx=0.25, rely=0.52, anchor=NE)
        user_id.place(relx=0.4, rely=0.534, anchor=NE)

        # Input box for Password
        pwd_txt = Canvas(Signup, width=0, height=0)
        pwd_txt.place(relx=0.5, rely=0.8, anchor=NE)
        Pwd_txt = Label(Signup, text='Password :')
        Pwd_txt.config(font=('Arial Rounded MT', 25), bg='#FFFFFF')
        pwd = Entry(Signup, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                    highlightcolor="black", justify="center", textvariable="Pwdtxt")
        pwd_txt.create_window(450, 250, window=pwd)
        Pwd_txt.place(relx=0.25, rely=0.62, anchor=NE)
        pwd.place(relx=0.4, rely=0.634, anchor=NE)

        # Input box for Password
        Re_pwd_txt = Canvas(Signup, width=0, height=0)
        Re_pwd_txt.place(relx=0.5, rely=0.8, anchor=NE)
        re_pwd_txt = Label(Signup, text='Re-Enter Password :')
        re_pwd_txt.config(font=('Arial Rounded MT', 25), bg='#FFFFFF')
        re_pwd = Entry(Signup, width=17, font=('Arial Rounded MT', 15), borderwidth=2,
                       highlightcolor="black", justify="center", textvariable="re_pwdtxt", show='*')
        Re_pwd_txt.create_window(450, 250, window=re_pwd)
        re_pwd_txt.place(relx=0.25, rely=0.72, anchor=NE)
        re_pwd.place(relx=0.4, rely=0.734, anchor=NE)

        # Registration  Btn
        reg_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/RegBtn.png"))
        regBtn = Button(Signup, image=reg_img, command=Register)
        regBtn.configure(bd=0, bg='#ffffff')
        regBtn.place(relx=0.415, rely=0.8, anchor=NE)

        # Clear  Btn
        clear_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/ClearBtn.png"))
        clearBtn = Button(Signup, image=clear_img, command=Clear)
        clearBtn.configure(bd=0, bg='#ffffff')
        clearBtn.place(relx=0.285, rely=0.8, anchor=NE)

        # Cancel Btn
        Cancel_img = ImageTk.PhotoImage(
            Image.open("Python Mini/Image/CancelBtn.png"))
        CancelBtn = Button(Signup, image=Cancel_img, command=Cancel)
        CancelBtn.configure(bd=0, bg='#ffffff')
        CancelBtn.place(relx=0.15, rely=0.8, anchor=NE)

        # Checkbox title
        select_acc = Label(Signup, text='Account Type:')
        select_acc.config(font=('Arial Rounded MT', 25), bg='#FFFFFF')
        select_acc.place(relx=0.57, rely=0.42, anchor=NE)
        Check_acc = StringVar()

        # adding Check Box

        # Admine Check Box
        Admin_ty = Checkbutton(Signup, text="Admin", bg="#FFFFFF", font=(
            'Arial Rounded MT', 20), variable=Check_acc, onvalue="Admin", offvalue="None", height=1, width=5)
        Admin_ty.deselect()
        Admin_ty.place(relx=0.42, rely=0.5, anchor=NW)
        # Instock Employee Check Box
        InEmp_ty = Checkbutton(Signup, text="Employee_In", bg="#FFFFFF", font=(
            'Arial Rounded MT', 20), variable=Check_acc, onvalue="In", offvalue="None", height=1, width=10)
        InEmp_ty.deselect()
        InEmp_ty.place(relx=0.42, rely=0.615, anchor=W)
        # Outstock Employee Check Box
        OutEmp_ty = Checkbutton(Signup, text="Employee_Out", bg="#FFFFFF", font=(
            'Arial Rounded MT', 20), variable=Check_acc, onvalue="Out", offvalue="None", height=1, width=12)
        OutEmp_ty.deselect()
        OutEmp_ty.place(relx=0.417, rely=0.7, anchor=W)

        # to run the window
        Signup.state('zoomed')
        Signup = mainloop()


L = Loginscreen()
Sin = Stockin()
Sout = Stockout()
ad = Admin()
Sign = Signup()
L.main()
