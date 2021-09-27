import pandas as pnd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfile as aof
from PIL import ImageTk
import pyodbc as pd
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
import random as ran
import base64
import pickle
import webbrowser
import os

user_name=''

def padding(s):
        return s+(16-len(s)%16)*'{'

#Function to encrypt data before inserting it into the database
def encrypt_db(msg):
    key='thiskeyissecret'
    hash_obj=SHA256.new(key.encode('utf-8'))
    key=hash_obj.digest()
    if key!=None:
        iv='youcanseetheiv'
        hashiv=MD5.new(iv.encode('utf-8'))
        iv=hashiv.digest()
        cipher=AES.new(key, AES.MODE_CBC, iv)
        result=cipher.encrypt(padding(msg).encode('utf-8'))
        return base64.b64encode(result).decode('utf-8')

#Function to decrypt data after extracting it from the database
def decrypt_db(cipher_text):
    key='thiskeyissecret'
    hash_obj=SHA256.new(key.encode('utf-8'))
    key=hash_obj.digest()
    if key!=None:
        iv='youcanseetheiv'
        hashiv=MD5.new(iv.encode('utf-8'))
        iv=hashiv.digest()
        cipher_text=base64.b64decode(cipher_text.encode('utf-8'))
        decipher=AES.new(key, AES.MODE_CBC, iv)
        msg=decipher.decrypt(cipher_text).decode('utf-8')
        pad_index=msg.find('{')
        result=msg[:pad_index]
        return result

#Creating a class login
class login:
    def __init__(self, root):
        self.root=root
        self.root.title('Login_Here')
        self.root.geometry('1200x600+100+20')
        self.root.resizable(False, False)

        self.btn=ImageTk.PhotoImage(file='C:/Project/Project_photos/login.png')
        self.btn0=ImageTk.PhotoImage(file='C:/Project/Project_photos/register.png')
        self.btn1=ImageTk.PhotoImage(file='C:/Project/Project_photos/check_username.png')
        self.btn2=ImageTk.PhotoImage(file='C:/Project/Project_photos/check.png')
        self.btn3=ImageTk.PhotoImage(file='C:/Project/Project_photos/update_password.png')

        self.bg=ImageTk.PhotoImage(file='C:/Project/Project_photos/BG_image.jpg')
        self.bg_image=tk.Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        frame_login=tk.Frame(self.root, bg='white')
        frame_login.place(x=355, y=75, height=450, width=490)

        title=tk.Label(frame_login, text='Login_Here', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.place(x=70, y=30)
        
        desc=tk.Label(frame_login, text='User_login Area', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=70, y=100)
        
        lab_user=tk.Label(frame_login, text='User_Name', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab_user.place(x=70, y=140)
        
        self.txt_user_0=tk.Entry(frame_login, font=('times new roman', 15), bg='lightgray')
        self.txt_user_0.place(x=70, y=170, width=350, height=35)
        
        lab_password=tk.Label(frame_login, text='Password', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab_password.place(x=70, y=210)
        
        self.txt_password_0=tk.Entry(frame_login, font=('times new roman', 15), bg='lightgray')
        self.txt_password_0.place(x=70, y=240, width=350, height=35)
        
        forget_btn=tk.Button(frame_login, text='Forget_Password?', fg='#2e6788', bg='white', font=('times new roman', 12), bd=0, command=self.change_password)
        forget_btn.place(x=70, y=280)

        create_btn=tk.Button(frame_login, text='Register', fg='#2e6788', bg='white', font=('times new roman', 12), bd=0, command=self.register_here)
        create_btn.place(x=370, y=280, width=50)
        
        login_btn=tk.Button(self.root, image=self.btn, bd=0, bg='white', command=self.login_func)
        login_btn.place(x=500, y=400, height=100, width=200)
    
    def register_here(self):
        self.new=tk.Toplevel(self.root)
        self.new.title('Register_Here')
        self.new.geometry('1200x600+100+20')
        self.new.resizable(False, False)
        
        put=tk.Label(self.new, image=self.bg)
        put.place(x=0, y=0, relwidth=1, relheight=1)

        frame=tk.Frame(self.new, bg='white')
        frame.place(x=355, y=25, height=550, width=490)

        title=tk.Label(frame, text='Register_Here', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.place(x=70, y=30)
        
        desc=tk.Label(frame, text='User_registration Area', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=70, y=100)
        
        lab=tk.Label(frame, text='User_Name', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab.place(x=70, y=140)
        
        self.txt_user_1=tk.Entry(frame, font=('times new roman', 15), bg='lightgray')
        self.txt_user_1.place(x=70, y=170, width=350, height=35)
        
        lab1=tk.Label(frame, text='Password', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab1.place(x=70, y=210)
        
        self.txt_password_1=tk.Entry(frame, font=('times new roman', 15), bg='lightgray')
        self.txt_password_1.place(x=70, y=240, width=350, height=35)

        lab2=tk.Label(frame, text='Password recovery question', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab2.place(x=70, y=280)
        
        self.txt_recoverquestion_1=tk.Entry(frame, font=('times new roman', 15), bg='lightgray')
        self.txt_recoverquestion_1.place(x=70, y=310, width=350, height=35)
        
        lab1=tk.Label(frame, text='Answer', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab1.place(x=70, y=350)
        
        self.txt_answer_1=tk.Entry(frame, font=('times new roman', 15), bg='lightgray')
        self.txt_answer_1.place(x=70, y=380, width=350, height=35)
        
        register_btn=tk.Button(self.new, image=self.btn0, bd=0, background='white', command=self.registration)
        register_btn.place(x=500, y=475, width=200, height=100)

    def change_password(self):
        self.new1=tk.Toplevel(self.root)
        self.new1.title('Register_Here')
        self.new1.geometry('1200x600+100+20')
        self.new1.resizable(False, False)
        
        put=tk.Label(self.new1, image=self.bg)
        put.place(x=0, y=0, relwidth=1, relheight=1)

        frame=tk.Frame(self.new1, bg='white')
        frame.place(x=355, y=25, height=550, width=490)

        title=tk.Label(frame, text='Change', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.place(x=70, y=30)

        title=tk.Label(frame, text='Password', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.place(x=70, y=90)
        
        desc=tk.Label(frame, text='Change your password here', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=70, y=150)
        
        lab=tk.Label(frame, text='User_Name', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab.place(x=70, y=180)
        
        self.txt_user_2=tk.Entry(frame, font=('times new roman', 15), bg='lightgray')
        self.txt_user_2.place(x=70, y=210, width=350, height=35)

        change_pass=tk.Button(self.new1, image=self.btn1, bd=0, background='white', command=lambda: self.change(frame))
        change_pass.place(x=500, y=475, width=200, height=100)

    def login_func(self):
        if self.txt_password_0.get()=='' or self.txt_user_0.get()=='':
            messagebox.showerror('Error', 'All fields are required', parent=self.root)
        else:
            self.check_details()
    
    #Member function of class login to enter new user details
    def registration(self):
        if self.txt_user_1.get()=='' or self.txt_password_1.get()=='' or self.txt_recoverquestion_1.get()=='' or self.txt_answer_1.get()=='':
            messagebox.showerror('Error', 'All fields are required', parent=self.new)
        else:
            conn=pd.connect('Driver={SQL Server};' 'Server=LAPTOP-HNP465U9;' 'Database=Project_DB;' 'Trusted_Connection=yes;')
            user_name=encrypt_db(self.txt_user_1.get())
            pass_word=encrypt_db(self.txt_password_1.get())
            question=encrypt_db(self.txt_recoverquestion_1.get())
            answer=encrypt_db(self.txt_answer_1.get())
            cur=conn.cursor()
            cur.execute(f'''SELECT S_no
                            FROM [login_details]
                            WHERE Name='{user_name}';''')
            r=[]
            for row in cur:
                r.append(row)
            if list(r)!=[]:
                messagebox.showerror('Incorrect User name', 'Username already exsists, Please change it...', parent=self.new)
            else:
                cur=conn.cursor()
                cur.execute(f'''INSERT INTO [login_details]
                                VALUES
                                ('{user_name}', '{pass_word}', '{question}', '{answer}');''')
                cur.commit()
                messagebox.showinfo('Complete', 'Registration_Successful', parent=self.new)
                self.new.destroy()

    #Member function of class login to check login details
    def check_details(self):
        global user_name
        conn=pd.connect('Driver={SQL Server};' 'Server=LAPTOP-HNP465U9;' 'Database=Project_DB;' 'Trusted_Connection=yes;')
        user_name=encrypt_db(self.txt_user_0.get())
        pass_word=encrypt_db(self.txt_password_0.get())
        cur=conn.cursor()
        cur.execute(f'''SELECT * 
                        FROM [login_details] 
                        WHERE Name='{user_name}' AND Pass_word='{pass_word}';''')
        if list(cur)==[]:
            messagebox.showerror('Error', 'Invalid Username/Passswoed', parent=self.root)
        else:
            self.root.destroy()
            Working_space()

    #Member function of class login to change password of a user
    def change(self, frame):
        if self.txt_user_2.get()=='':
            messagebox.showerror('Error', 'All fields are required', parent=self.new1)
        else:
            conn=pd.connect('Driver={SQL Server};' 'Server=LAPTOP-HNP465U9;' 'Database=Project_DB;' 'Trusted_Connection=yes;')
            user_name=encrypt_db(self.txt_user_2.get())
            cur=conn.cursor()
            cur.execute(f'''SELECT pass_word_question 
                            FROM [login_details] 
                            WHERE Name='{user_name}';''')
            r=[]
            for row in cur:
                r.append(row)
            if list(r)==[]:
                messagebox.showerror('Error', 'Invalid Username', parent=self.new1)
            else:
                title=tk.Label(frame, text=f'Questuion: {decrypt_db(r[0][0])}?', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
                title.place(x=70, y=250)

                lab=tk.Label(frame, text='Answer', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
                lab.place(x=70, y=280)

                self.txt_answer_2=tk.Entry(frame, font=('times new roman', 15), bg='lightgray')
                self.txt_answer_2.place(x=70, y=310, width=350, height=35)
                
                change_pass=tk.Button(self.new1, image=self.btn2, bd=0, background='white', command=lambda: self.canwechange(frame))
                change_pass.place(x=500, y=475, width=200, height=100)
    
    def canwechange(self, frame):
        if self.txt_answer_2.get()=='' or self.txt_user_2.get()=='':
            messagebox.showerror('Error', 'All fields are required', parent=self.new1)
        else:
            conn=pd.connect('Driver={SQL Server};' 'Server=LAPTOP-HNP465U9;' 'Database=Project_DB;' 'Trusted_Connection=yes;')
            user_name=encrypt_db(self.txt_user_2.get())
            answer=encrypt_db(self.txt_answer_2.get())
            cur=conn.cursor()
            cur.execute(f'''SELECT answer 
                            FROM [login_details] 
                            WHERE Name='{user_name}' and answer='{answer}';''')
            r=[]
            for row in cur:
                r.append(row)
            if list(r)==[]:
                messagebox.showerror('Error', 'Wrong Answer', parent=self.new1)
            else:
                title=tk.Label(frame, text='New Password', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
                title.place(x=70, y=350)

                self.txt_password_2=tk.Entry(frame, font=('times new roman', 15), bg='lightgray')
                self.txt_password_2.place(x=70, y=380, width=350, height=35)
                
                change_pass=tk.Button(self.new1, image=self.btn3, bd=0, background='white', command=self.changeitfinally)
                change_pass.place(x=500, y=475, width=200, height=100)

    def changeitfinally(self):
        if self.txt_user_2.get()=='' or self.txt_password_2.get()=='':
            messagebox.showerror('Error', 'All fields are required', parent=self.new1)
        else:
            conn=pd.connect('Driver={SQL Server};' 'Server=LAPTOP-HNP465U9;' 'Database=Project_DB;' 'Trusted_Connection=yes;')
            cur=conn.cursor()
            user_name=encrypt_db(self.txt_user_2.get())
            password=encrypt_db(self.txt_password_2.get())
            cur.execute(f'''UPDATE [login_details]  
                            SET Pass_word='{password}'
                            WHERE Name='{user_name}';''')
            cur.commit()
            messagebox.showinfo('Complete', 'Password change successful', parent=self.new1)
            self.new1.destroy()
    
#Creating a class Working_space
class Working_space:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title('Work_space')
        self.root.geometry('1200x600+100+20')
        self.root.resizable(False, False)

        self.bg=ImageTk.PhotoImage(file='C:/Project/Project_photos/BG_image.jpg')
        self.bg_image=tk.Label(self.root, image=self.bg)
        self.bg_image.place(x=0, y=0, relwidth=1, relheight=1)

        self.btn1=ImageTk.PhotoImage(file='C:/Project/Project_photos/WS_1.png')
        self.btn2=ImageTk.PhotoImage(file='C:/Project/Project_photos/WS_2.png')
        self.btn3=ImageTk.PhotoImage(file='C:/Project/Project_photos/WS_3.png')
        self.btn4=ImageTk.PhotoImage(file='C:/Project/Project_photos/WS_4.png')
        self.btn5=ImageTk.PhotoImage(file='C:/Project/Project_photos/WS_5.png')
        
        self.obj_pw=pass_word(self.root)
        self.obj_aes=AES_encryption(self.root)
        self.obj_url=mal_URL(self.root)
        self.obj_email=email_check(self.root)

        _btn1=tk.Button(self.bg_image, image=self.btn1, bd=0, highlightcolor='green', background=None, command=lambda: self.obj_pw.generate_password(True))
        _btn1.place(x=397, y=155.5, width=153, height=63)

        _btn2=tk.Button(self.root, image=self.btn2, bd=0, background='white', command=lambda: self.obj_aes.text_encryption(True))
        _btn2.place(x=397, y=268.5, width=151, height=63)

        _btn3=tk.Button(self.root, image=self.btn3, bd=0, background='white', command=self.obj_email.check_mail)
        _btn3.place(x=397, y=381.5, width=153, height=63)

        _btn4=tk.Button(self.root, image=self.btn4, bd=0, background='white', command=self.obj_url.mal_check)
        _btn4.place(x=650, y=187, width=153, height=63)

        _btn5=tk.Button(self.root, image=self.btn5, bd=0, background='white', command=self.contact_expert)
        _btn5.place(x=650, y=300, width=153, height=63)

        self.root.mainloop()
    #Member function of class Working_space to open a web link
    def contact_expert(self):
        url='www.google.com'
        webbrowser.open(url)
        #self.root.destroy()

#Creating a class pass_word
class pass_word:
    def __init__(self, root):
        self.root=root
        self.var=tk.IntVar()
        self.var1=tk.IntVar()

        self.bg=ImageTk.PhotoImage(file='C:/Project/Project_photos/BG_image.jpg')
        
        self.btn=ImageTk.PhotoImage(file='C:/Project/Project_photos/save.png')
        self.btn0=ImageTk.PhotoImage(file='C:/Project/Project_photos/Generate.png')
        self.btn1=ImageTk.PhotoImage(file='C:/Project/Project_photos/Generate0.png')
        self.btn2=ImageTk.PhotoImage(file='C:/Project/Project_photos/save1.png')
        self.btn3=ImageTk.PhotoImage(file='C:/Project/Project_photos/save2.png')
        self.btn4=ImageTk.PhotoImage(file='C:/Project/Project_photos/view.png')
        
        self.click=True

    #Member function of class pass_word to generate random passwords
    def ret_pass(self):    
        self.output.delete(0, 'end')

        length=self.var1.get()

        low='abcdefghijklmnopqrstuvwxyz0123456789'
        mid='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        high='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=~`?.>,<|]}[{'
        password=''

        if self.var.get()==1:
            for _ in range(0, length):
                password=password+ran.choice(low)
            return password
        elif self.var.get()==2:
            for _ in range(0, length):
                password=password+ran.choice(mid)
            return password
        else:
            for _ in range(0, length):
                password=password+ran.choice(high)
            return password

    def generator(self):
        if self.website.get()=='':
            messagebox.showerror('Error', 'Website field is required', parent=self.new1)
        else:
            password=self.ret_pass()
            self.output.insert(10, password)

    #Member function of class pass_word to print all pass_words of a perticular user
    def show_db(self):
        global user_name

        self.frame=tk.Frame(self.new1, bg='white')
        self.frame.place(x=200, y=50, height=500, width=800)

        conn=pd.connect('Driver={SQL Server};' 'Server=LAPTOP-HNP465U9;' 'Database=Project_DB;' 'Trusted_Connection=yes;')
        cur=conn.cursor()
        cur.execute(f'''SELECT Website, Pass_word
                        FROM [pass_word_table] 
                        WHERE Name='{user_name}';''')
        
        title=tk.Label(self.frame, text='Saved Passwords', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.pack(anchor='c', pady=30)

        desc=tk.Label(self.frame, text='Your Saved Passwords', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=230, y=100)

        m=0

        db=tk.Label(self.frame, text='Website', font=('Impact', 12, 'bold'), fg='#2e6788', bg='white')
        db.place(x=230, y=130)

        db=tk.Label(self.frame, text='Pass Word', font=('Impact', 12, 'bold'), fg='#2e6788', bg='white')
        db.place(x=500, y=130)
        

        for row in cur:
            n=0
            for i in row:
                db=tk.Label(self.frame, text=decrypt_db(i), font=('Impact', 12, 'bold'), fg='grey', bg='white')
                db.place(x=230+n, y=150+m)
                n=n+270
            m=m+20
        
        next_btn1=tk.Button(self.new1, image=self.btn1, bd=0, background='white', command=lambda: self.generate_password(False))
        next_btn1.place(x=23.5, y=212, width=153, height=63)

        next_btn2=tk.Button(self.new1, image=self.btn2, bd=0, background='white', command=self.insert_in_db)
        next_btn2.place(x=23.5, y=325, width=153, height=63)

    def insert_in_db(self):
        self.frame=tk.Frame(self.new1, bg='white')
        self.frame.place(x=200, y=50, height=500, width=800)

        title=tk.Label(self.frame, text='Insert_new Password', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.pack(anchor='c', pady=30)
        
        desc=tk.Label(self.frame, text='Insert password here', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=190, y=100)
        
        lab=tk.Label(self.frame, text='Website', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab.place(x=190, y=140)
        
        self.website=tk.Entry(self.frame, font=('times new roman', 15), bg='lightgray')
        self.website.place(x=190, y=170, width=350, height=35)

        lab0=tk.Label(self.frame, text='Password', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab0.place(x=190, y=210)
        
        self.output=tk.Entry(self.frame, font=('times new roman', 15), bg='lightgray')
        self.output.place(x=190, y=240, width=350, height=35)

        save_this=tk.Button(self.frame, image=self.btn, bd=0, background='white', command=self.save_it)
        save_this.place(x=300, y=370, height=100, width=200)

        next_btn1=tk.Button(self.new1, image=self.btn1, bd=0, background='white', command=lambda: self.generate_password(False))
        next_btn1.place(x=23.5, y=212, width=153, height=63)

        next_btn2=tk.Button(self.new1, image=self.btn4, bd=0, background='white', command=self.show_db)
        next_btn2.place(x=23.5, y=325, width=153, height=63)

    def generate_password(self, cli):
        self.click=cli
        if self.click:
            self.new1=tk.Toplevel(self.root)
            self.new1.title('Password_manager')
            self.new1.geometry('1200x600+100+20')
            self.new1.resizable(False, False)
            
            put=tk.Label(self.new1, image=self.bg)
            put.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.frame.destroy()

        self.frame=tk.Frame(self.new1, bg='white')
        self.frame.place(x=200, y=50, height=500, width=800)

        title=tk.Label(self.frame, text='Generate_new Password', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.pack(anchor='c', pady=30)
        
        desc=tk.Label(self.frame, text='Generate password here', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=160, y=100)
        
        lab=tk.Label(self.frame, text='Website', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab.place(x=160, y=140)
        
        self.website=tk.Entry(self.frame, font=('times new roman', 15), bg='lightgray')
        self.website.place(x=160, y=170, width=350, height=35)

        lab0=tk.Label(self.frame, text='Password', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab0.place(x=160, y=210)

        combo=ttk.Combobox(self.frame, textvariable=self.var1, font=('Goudy old style', 15, 'bold'))
        combo['values']=(6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,'Length')
        combo.current(0)
        combo.bind('<<ComboboxSelected>>')
        combo.place(x=160, y=240, width=350, height=35)
        
        low=tk.Radiobutton(self.frame, text='Low', variable=self.var, value=1, font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        low.place(x=160, y=280)
        mid=tk.Radiobutton(self.frame, text='Medium', variable=self.var, value=2, font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        mid.place(x=230, y=280)
        high=tk.Radiobutton(self.frame, text='High', variable=self.var, value=3, font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        high.place(x=335, y=280)

        lab0=tk.Label(self.frame, text='Password', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab0.place(x=160, y=320)
        
        self.output=tk.Entry(self.frame, font=('times new roman', 15), bg='lightgray')
        self.output.place(x=160, y=350, width=350, height=35)

        generate_it=tk.Button(self.frame, image=self.btn0, bd=0, background='white', command=self.generator)
        generate_it.place(x=140, y=400, width=200, height=100)
        
        save_this=tk.Button(self.frame, image=self.btn, bd=0, background='white', command=self.save_it)
        save_this.place(x=350, y=400, width=200, height=100)

        next_btn1=tk.Button(self.new1, image=self.btn3, bd=0, background='white', command=self.insert_in_db)
        next_btn1.place(x=23.5, y=212, width=153, height=63)

        next_btn2=tk.Button(self.new1, image=self.btn4, bd=0, background='white', command=self.show_db)
        next_btn2.place(x=23.5, y=325, width=153, height=63)

    #Member function of class pass_word to insert or update passwords
    def save_it(self):
        if self.website.get()=='' or self.output.get()=='':
            messagebox.showerror('Error', 'All fields are required', parent=self.new1)
        else:
            global user_name
            conn=pd.connect('Driver={SQL Server};' 'Server=LAPTOP-HNP465U9;' 'Database=Project_DB;' 'Trusted_Connection=yes;')
            website=encrypt_db(self.website.get())
            pass_w=encrypt_db(self.output.get())
            cur=conn.cursor()
            cur.execute(f'''SELECT S_no
                            FROM [pass_word_table]
                            WHERE Website='{website}';''')
            r=[]
            for row in cur:
                r.append(row)
            if r!=[]:
                stamp=messagebox.askquestion('Update?', 'Password for this website\nis already saved..\nWant to update?', parent=self.root)
                if stamp=='yes':
                    cur=conn.cursor()
                    cur.execute(f'''UPDATE [pass_word_table]
                                    SET Pass_word='{pass_w}'
                                    WHERE Website='{website}';''')
                    cur.commit()
                    messagebox.showinfo('Success', 'Password Saved', parent=self.new1)
                    self.website.delete(0, 'end')
                    self.output.delete(0, 'end')
                else:
                    messagebox.showinfo('Done', 'Password not Saved', parent=self.new1)
                    self.website.delete(0, 'end')
                    self.output.delete(0, 'end')
            else:
                cur=conn.cursor()
                cur.execute(f'''INSERT INTO [pass_word_table]
                                VALUES
                                ('{website}', '{pass_w}', '{user_name}');''')
                cur.commit()
                messagebox.showinfo('Success', 'Password Saved', parent=self.new1)
                self.website.delete(0, 'end')
                self.output.delete(0, 'end')

#Creating a class AES_encryption
class AES_encryption:
    def __init__(self, root):
        self.root=root

        self.bg=ImageTk.PhotoImage(file='C:/Project/Project_photos/BG_image.jpg')

        self.btn=ImageTk.PhotoImage(file='C:/Project/Project_photos/encrypt.png')
        self.btn0=ImageTk.PhotoImage(file='C:/Project/Project_photos/decrypt.png')
        self.btn1=ImageTk.PhotoImage(file='C:/Project/Project_photos/encrypt_file.png')
        self.btn2=ImageTk.PhotoImage(file='C:/Project/Project_photos/decrypt_file.png')
        self.btn3=ImageTk.PhotoImage(file='C:/Project/Project_photos/ef.png')
        self.btn4=ImageTk.PhotoImage(file='C:/Project/Project_photos/et.png')

        self.click=True

    def get_key(self):
        key=self.key.get()
        if key!='':
            hash_obj=SHA256.new(key.encode('utf-8'))
            key=hash_obj.digest()
            return key
    
    #Member function of class AES_encryption to encrypt data
    def encrypt(self, msg):
        key=self.get_key()
        if key!=None:
            cipher=AES.new(key, AES.MODE_ECB)
            result=cipher.encrypt(padding(msg).encode('utf-8'))
            return base64.b64encode(result).decode('utf-8')

    #Member function of class AES_encryption to encrypt data
    def decrypt(self, cipher_text):
        key=self.get_key()
        if key!=None:
            cipher_text=base64.b64decode(cipher_text.encode('utf-8'))
            decipher=AES.new(key, AES.MODE_ECB)
            msg=decipher.decrypt(cipher_text).decode('utf-8')
            pad_index=msg.find('{')
            result=msg[:pad_index]
            return result

    #Member function of class AES_encryption to open a file for encryption
    def open_file_encrypt(self):
        if self.key.get()=='':
            messagebox.showerror('Error', 'Enter Key first', parent=self.new1)
        else:
            file=aof(mode='r', filetypes=[('Text Files', '*.txt')], parent=self.new1)
            if file is not None:
                content=file.read()
                cipher_text=self.encrypt(content)
                f=open('new.txt', 'w+')
                f.write(cipher_text)
                f.close()
                path=file.name
                file.close()
                os.remove(path)
                os.rename('new.txt', path)
                messagebox.showinfo('Complete', 'Encryption Complete', parent=self.new1)

    #Member function of class AES_encryption to open a file for decryption
    def open_file_decrypt(self):
        if self.key.get()=='':
            messagebox.showerror('Error', 'Enter Key first', parent=self.new1)
        else:
            file=aof(mode='r', filetypes=[('Text Files', '*.txt')], parent=self.new1)
            if file is not None:
                content=file.read()
                msg=self.decrypt(content)
                f=open('new.txt', 'w+')
                f.write(msg)
                f.close()
                path=file.name
                file.close()
                os.remove(path)
                os.rename('new.txt', file.name)
                messagebox.showinfo('Complete', 'Decryption Complete', parent=self.new1)
    
    def encrypt_this(self):
        self.output.delete('1.0', 'end')
        msg=self.mess.get('1.0', 'end')
        if msg=='\n' or self.get_key()==None:
            messagebox.showerror('Error', 'All fields are required', parent=self.new1)
        else:
            result=self.encrypt(msg)
            self.output.insert('end', result)
        
    def decrypt_this(self):
        self.mess.delete('1.0', 'end')
        ct=self.output.get('1.0', 'end')
        if ct=='\n' or self.get_key()==None:
            messagebox.showerror('Error', 'All fields are required', parent=self.new1)
        else:
            result=self.decrypt(ct)
            self.mess.insert('end', result)

    def text_encryption(self, cli):
        self.click=cli
        if self.click:
            self.new1=tk.Toplevel(self.root)
            self.new1.title('Encryption/Decryption')
            self.new1.geometry('1200x600+100+20')
            self.new1.resizable(False, False)
            
            put=tk.Label(self.new1, image=self.bg)
            put.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.frame.destroy()

        self.frame=tk.Frame(self.new1, bg='white')
        self.frame.place(x=200, y=50, height=500, width=800)

        title=tk.Label(self.frame, text='Text Encryption/Decryption', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.pack(anchor='c', pady=30)
        
        desc=tk.Label(self.frame, text='Encrypt/Decrypt text here', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=130, y=100)
        
        lab_txt=tk.Label(self.frame, text='Message/ Decrypted Text', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab_txt.place(x=130, y=140)
        
        self.mess=ScrolledText(self.frame, font=('times new roman', 15), bg='lightgray')
        self.mess.place(x=130, y=170, width=300, height=120)

        lab_output=tk.Label(self.frame, text='Encrypted Text', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab_output.place(x=465, y=140)

        self.output=ScrolledText(self.frame, font=('times new roman', 15), bg='lightgray')
        self.output.place(x=465, y=170, width=300, height=120)
        
        lab_key=tk.Label(self.frame, text='Key', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab_key.place(x=130, y=300)

        self.key=tk.Entry(self.frame, font=('times new roman', 15), bg='lightgray')
        self.key.place(x=130, y=330, width=300, height=35)

        encrypt_btn=tk.Button(self.frame, image=self.btn, bd=0, background='white', command=self.encrypt_this)
        encrypt_btn.place(x=110, y=390, width=200, height=80)

        decrypt_btn=tk.Button(self.frame, image=self.btn0, bd=0, background='white', command=self.decrypt_this)
        decrypt_btn.place(x=510, y=390, width=200, height=80)

        next_btn=tk.Button(self.new1, image=self.btn3, bd=0, background='white', command=self.file_encryption)
        next_btn.place(x=23.5, y=268.5, width=153, height=63)

    def file_encryption(self):
        self.frame=tk.Frame(self.new1, bg='white')
        self.frame.place(x=200, y=50, height=500, width=800)

        title=tk.Label(self.frame, text='File Encryption/Decryption', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.pack(anchor='c', pady=30)
        
        desc=tk.Label(self.frame, text='Encrypt/Decrypt file here', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=130, y=100)
        
        lab_key=tk.Label(self.frame, text='Key', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab_key.place(x=130, y=140)
        
        self.key=tk.Entry(self.frame, font=('times new roman', 15), bg='lightgray')
        self.key.place(x=130, y=170, width=350, height=35)

        desc=tk.Label(self.frame, text='*You can choose only text files', font=('Goudy old style', 15), bg='white')
        desc.place(x=130, y=210)

        encrypt_btn=tk.Button(self.frame, image=self.btn1, bd=0, background='white', command=self.open_file_encrypt)
        encrypt_btn.place(x=110, y=370, width=200, height=100)

        decrypt_btn=tk.Button(self.frame, image=self.btn2, bd=0, background='white', command=self.open_file_decrypt)
        decrypt_btn.place(x=380, y=370, width=200, height=100)

        next_btn=tk.Button(self.new1, image=self.btn4, bd=0, background='white', command=lambda: self.text_encryption(False))
        next_btn.place(x=23.5, y=268.5, width=153, height=63)

#Creating class mal_URL
class mal_URL:
    def __init__(self, root):
        self.root=root
        self.click=True

        self.bg=ImageTk.PhotoImage(file='C:/Project/Project_photos/BG_image.jpg')

        self.btn=ImageTk.PhotoImage(file='C:/Project/Project_photos/detect.png')

    #Member function of class mal_URL to tokenize the given data
    def my_tokenizer(self, x):
        tokens_by_slash=str(x.encode('utf-8')).split('/')
        total_tokens=[]
        
        for i in tokens_by_slash:
            tokesn_by_hyphen=str(i).split('-')
            tokens_by_dot=[]
            for j in range(0,len(tokesn_by_hyphen)):
                tokens_by_dot=str(tokesn_by_hyphen[j]).split('.')
            total_tokens=total_tokens+tokens_by_dot
            total_tokens=list(set(total_tokens))
        
        if 'com' in total_tokens:
            total_tokens.remove('com')
        if 'www' in total_tokens:
            total_tokens.remove('www')
        return total_tokens
        
    #Member function of class mal_URL to predict about URLs
    def malicious_checker(self):
        if self.url.get()=='':
            messagebox.showerror('Error', 'URL field is required', parent=self.new1)
        else:
            df=pnd.read_csv("C:/Project/DataSet/urldata.csv")
            df.head()
            url=df['url']

            vectorizer=TfidfVectorizer(self.my_tokenizer)
            
            vectorizer.fit_transform(url)
            
            with open('C:/Project/Project0/finalized_model0.sav', 'rb') as f:
                mp=pickle.load(f)
            
            to_be_predicted=self.url.get()
            
            X_predict=[to_be_predicted]
            X_predict=vectorizer.transform(X_predict)
            
            New_predict=mp.predict(X_predict)
            if New_predict[0]==1:
                messagebox.showinfo('Safe', 'This URL is safe to use', parent=self.new1)
                desc=tk.Label(self.frame, text='Safe URL', font=('Goudy old style', 15), bg='white')
                desc.place(x=160, y=210, height=50, width=100)
            else:
                messagebox.showwarning('Malicious URL Detected', f'This URL is not safe to use', parent=self.new1)
                desc=tk.Label(self.frame, text='Spam URL', font=('Goudy old style', 15), bg='white')
                desc.place(x=160, y=210, height=50, width=100)

    def mal_check(self):
        self.new1=tk.Toplevel(self.root)
        self.new1.title('URL_Detector')
        self.new1.geometry('1200x600+100+20')
        self.new1.resizable(False, False)
        
        put=tk.Label(self.new1, image=self.bg)
        put.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame=tk.Frame(self.new1, bg='white')
        self.frame.place(x=200, y=50, height=500, width=800)

        title=tk.Label(self.frame, text='Malicious URL Detector', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.pack(anchor='c', pady=30)
        
        desc=tk.Label(self.frame, text='Enter URL here', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=170, y=100)
        
        lab=tk.Label(self.frame, text='URL', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab.place(x=170, y=140)
        
        self.url=tk.Entry(self.frame, font=('times new roman', 15), bg='lightgray')
        self.url.place(x=170, y=170, width=350, height=35)
        
        check_btn=tk.Button(self.frame, image=self.btn, bd=0, background='white', command=self.malicious_checker)
        check_btn.place(x=300, y=370, width=200, height=100)

#Creating a class email_check
class email_check:
    def __init__(self, root):
        self.root=root
        self.click=True

        self.bg=ImageTk.PhotoImage(file='C:/Project/Project_photos/BG_image.jpg')

        self.btn=ImageTk.PhotoImage(file='C:/Project/Project_photos/detect.png')
    
    #Member function of class email_check to predict spam percentage of a given mail
    def email_checker(self):
        if self.mail.get('1.0')=='\n':
            messagebox.showerror('Error', 'E-mail field is required', parent=self.new1)
        else:
            df=pnd.read_csv('C:/Project/DataSet/final_dataset.csv')
        
            stop_words=set(stopwords.words('english'))
            df['text']=df['text'].apply(lambda x: ' '.join([ word for word in word_tokenize(x)  if not word in stop_words]))
            
            with open('C:/Project/Project0/finalized_model1.sav', 'rb') as f:
                mp=pickle.load(f)

            with open('C:/Project/Project0/vectorizer.pickle', 'rb') as f:
                cVect=pickle.load(f)

            text=self.mail.get('1.0', 'end')
            text=[' '.join([ word for word in word_tokenize(text) if not word in stop_words])]
            
            t_dtv=cVect.transform(text).toarray()
            prob=mp.predict_proba(t_dtv)*100
            a=int(prob[0][0])
            
            if a>50:
                messagebox.showinfo('Message', 'The mail is Not-Spam.', parent=self.new1)
            else:
                messagebox.showinfo('Message', 'The mail is Spam.', parent=self.new1)
            
            lab=tk.Label(self.frame, text=f"Spam: {100-a}%", font=('Goudy old style', 15), bg='white')
            lab.place(x=180, y=330)

    def check_mail(self):
        self.new1=tk.Toplevel(self.root)
        self.new1.title('Email_cheker')
        self.new1.geometry('1200x600+100+20')
        self.new1.resizable(False, False)
        
        put=tk.Label(self.new1, image=self.bg)
        put.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame=tk.Frame(self.new1, bg='white')
        self.frame.place(x=200, y=50, height=500, width=800)
        
        title=tk.Label(self.frame, text='Spam E-mail Detector', font=('Impact', 35, 'bold'), fg='#429ac9', bg='white')
        title.pack(anchor='c', pady=30)
        
        desc=tk.Label(self.frame, text='Copy E-mail here', font=('Goudy old style', 15, 'bold'), fg='#2e6788', bg='white')
        desc.place(x=190, y=100)
        
        lab=tk.Label(self.frame, text='E-mail', font=('Goudy old style', 15, 'bold'), fg='gray', bg='white')
        lab.place(x=190, y=140)
        
        self.mail=ScrolledText(self.frame, font=('times new roman', 15), bg='lightgray')
        self.mail.place(x=190, y=170, width=450, height=150)
        
        check_btn=tk.Button(self.frame, image=self.btn, bd=0, background='white', command=self.email_checker)
        check_btn.place(x=300, y=370, width=200, height=100)

root=tk.Tk()
obj=login(root)
root.mainloop()