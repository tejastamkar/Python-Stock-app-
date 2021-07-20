from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql
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

# Registertion Function


def Register():
    name = user__name.get()
    userid = user_id.get()
    password = pwd.get()
    acc = Check_acc.get()
    repwd = re_pwd.get()
    print(repwd)
    if (password == re_pwd.get() and name != " " and userid != " " and password != " "):
        if(acc == "None"):
            messagebox.showerror("Error", "Select Employee Type")
        else:
            conn = pymysql.connect(
                host="localhost", user="root", password="root", database="stock")
            cur = conn.cursor()
            sql = "INSERT INTO login VALUES (%s,%s,%s,%s)"
            cur.execute(sql, (userid, password, acc, name))
            conn.commit()
            user__name.delete(0, 'end')
            user_id.delete(0, 'end')
            pwd.delete(0, 'end')
            re_pwd.delete(0, 'end')
            Admin_ty.deselect()
            InEmp_ty.deselect()
            OutEmp_ty.deselect()
    else:
        messagebox.showerror("Error", "Please Enter details Properly")


# Signup to make a Signup window and set the window size
Signup = Tk()
Signup.geometry("1366x768")
Signup.configure(bg='#FFFFFF')
Signup.title("Retail Management")


# background image input
BgImg = ImageTk.PhotoImage(Image.open("image/Bg_Sign.png"))
Bg = Label(image=BgImg)
Bg.configure(bg='#FFFFFF')
Bg.place(relx=1, x=0, y=0, anchor=NE)

# Adding header
header = ImageTk.PhotoImage(Image.open("image/head.png"))
head = Label(image=header)
head.configure(bg='#FFFFFF')
head.place(relx=0.75, anchor=NE)

# adding Registration text
Regtxt = ImageTk.PhotoImage(Image.open("image/Registration.png"))
reg = Label(image=Regtxt)
reg.configure(bg='#FFFFFF')
reg.place(relx=0.4, rely=0.065, anchor=NE)

# adding Face ID Button
FaceID = ImageTk.PhotoImage(Image.open("image/face_id.png"))
Fbtn = Button(Signup, image=FaceID)
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
reg_img = ImageTk.PhotoImage(Image.open("image/RegBtn.png"))
regBtn = Button(Signup, image=reg_img, command=Register)
regBtn.configure(bd=0, bg='#ffffff')
regBtn.place(relx=0.415, rely=0.8, anchor=NE)

# Clear  Btn
clear_img = ImageTk.PhotoImage(Image.open("image/clearBtn.png"))
clearBtn = Button(Signup, image=clear_img, command=Clear)
clearBtn.configure(bd=0, bg='#ffffff')
clearBtn.place(relx=0.285, rely=0.8, anchor=NE)

# Cancel Btn
Cancel_img = ImageTk.PhotoImage(Image.open("image/CancelBtn.png"))
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
