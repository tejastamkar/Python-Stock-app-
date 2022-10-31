from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageDraw, ImageFont
import datetime
import tkcalendar as Cal
from tkinter import messagebox
import pymysql

# logout function


def Logout():
    temp = messagebox.askyesno("Warring", "Do you want to Close")
    if (temp):
        cleardata()
        admin.destroy()


def cleardata():
    for record in instock_tv.get_children():
        instock_tv.delete(record)
    for record in outstock_tv.get_children():
        outstock_tv.delete(record)


def reg():

    admin.destroy()
    return True


conn = pymysql.connect(
    host="localhost", user="root", password="root", database="stock")
cur = conn.cursor()

admin = Tk()
admin.geometry("1366x768")
admin.configure(bg='#FFFFFF')
admin.title("Retail Management")


def stockcall(instock_tv, outstock_tv, Admin_tv):
    sql = "select * from stockin"
    cur.execute(sql)
    rows = cur.fetchall()
    sql = "select * from stockout"
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
date_txt.configure(font=('Arial Rounded MT', 18), justify=LEFT, bg='#FFFFFF')
date_txt.place(relx=0.18, rely=0.35, anchor=NE)

# Logo image
header = ImageTk.PhotoImage(Image.open("image/logo.png"))
logo = Label(image=header)
logo.configure(bg='#FFFFFF')
logo.place(relx=0.35, anchor=NE)

# Insert Btn
regbtn_img = ImageTk.PhotoImage(Image.open("image/SignupBtn.png"))
regBtn = Button(admin, image=regbtn_img, command=reg)
regBtn.configure(bd=0, bg='#ffffff')
regBtn.place(relx=0.24, rely=0.25, anchor=NE)

# Logout Btn
Logout_img = ImageTk.PhotoImage(Image.open("image/Admin_LogoutBtn.png"))
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
