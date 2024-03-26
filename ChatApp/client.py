import json
import socket
import threading
import tkinter
from tkinter import *
import time
import customtkinter as tk
from PIL import Image, ImageTk
import os
import sys
from tkinter import ttk
import tkinter as tttk
from CTkMessagebox import CTkMessagebox
from plyer import notification
from datetime import datetime

HOST = socket.gethostbyname(socket.gethostname())
PORT = 54569
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
nickname = None
gui_done = False
running = True
textarea = None
win = None
destroy = None

global lb
global nooomi
global option_menu
global input_area


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def gui_loop():
    global gui_done
    global textarea
    global win
    global nickname
    global input_area
    try:
        win = tk.CTkToplevel(root)
        win.title(f"{nickname}")
        win.configure(bg="#fff")
        win.geometry('670x550')
        win.wm_iconbitmap()
        root.after(300, lambda: win.iconphoto(False, iconpath))
        tabview = ttk.Notebook(win)
        tabview.pack(side='right', fill=tk.BOTH, expand=True, anchor=tk.E)
        frm = tk.CTkFrame(tabview, width=650, height=529, fg_color=('white', '#282c35'))
        frm_1 = tk.CTkFrame(tabview, width=650, height=529, fg_color=('white', '#282c35'))
        frm.pack(fill="both", expand=1)
        frm_1.pack(fill="both", expand=1)
        tabview.add(frm, text="chat")
        tabview.add(frm_1, text="options")
        lll = tk.CTkLabel(frm_1, text='CHANGE USERNAME', text_color=('black', 'white'), font=('Georgia bold', 25))
        lll.place(x=20, y=10)
        changer_v_p = tk.CTkEntry(frm_1, width=200, height=35, corner_radius=50, border_color='#83a4cf',
                                  fg_color=('white', 'black'),
                                  bg_color=('white', '#282c35'), text_color=('black', 'white'))
        changer_v_p.place(x=65, y=300)

        def change_op_2():
            global nickname
            new_name = changer_v_p.get()
            if new_name:
                update_label(new_name)

        def update_label(new_name):
            global nickname
            sock.send("change".encode('utf-8'))
            time.sleep(0.1)
            sock.send(nickname.encode('utf-8'))
            time.sleep(0.1)
            nickname = new_name
            sock.send(nickname.encode('utf-8'))
            win.title(f"{new_name}")
            CTkMessagebox(title='success', message=f"you changed your name to {nickname} successfully ", icon='check')

        change_button = tk.CTkButton(frm_1, text='Change', text_color='black', fg_color='#83a4cf', corner_radius=50,
                                     width=170, height=30, command=change_op_2)
        change_button.place(x=75, y=360)
        ll = tk.CTkLabel(frm_1, text='CREATE A ROOM', text_color=('black', 'white'), font=('Georgia bold', 25))
        ll.place(x=380, y=10)
        eent = tk.CTkEntry(frm_1, width=200, height=35, corner_radius=50, border_color='#83a4cf',
                           fg_color=('white', 'black'),
                           bg_color=('white', '#282c35'), text_color=('black', 'white'))
        eent.place(x=400, y=300)

        creer_button = tk.CTkButton(frm_1, text='Create', text_color='black', fg_color='#83a4cf', corner_radius=50,
                                    width=170, height=30, command=lambda: crroom(eent))

        creer_button.place(x=415, y=360)
        grp_icon = tk.CTkImage(Image.open((resource_path("groupico_.png"))), size=(400, 210))
        nk_12 = tk.CTkLabel(frm_1, image=grp_icon, text='')
        nk_12.place(x=300, y=58)
        chu_icon = tk.CTkImage(Image.open(resource_path("chu.png")), size=(350, 210))
        nk_13 = tk.CTkLabel(frm_1, image=chu_icon, text='')
        nk_13.place(x=0, y=58)
        tabview.configure(width=win.winfo_width(), height=win.winfo_height())
        lb = tk.CTkLabel(frm, fg_color=('white', '#282c35'), bg_color=('white', '#282c35'), text='', anchor='n')
        lb.pack()
        menu_bar = tkinter.Menu(win)
        win.configure(menu=menu_bar)
        Online_menu = tkinter.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Online", menu=Online_menu)
        Offline_menu = tkinter.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Offline", menu=Offline_menu)
        rooms_menu = tkinter.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Rooms", menu=rooms_menu)

        def deconnect():
            sock.close()
            root.destroy()
            sys.exit()

        menu_bar.add_command(label="Log out", command=deconnect)

        textarea = tk.CTkTextbox(master=frm, activate_scrollbars=True, width=615, height=400,
                                 bg_color=('white', 'black'), fg_color=('white', 'black'), border_width=3,
                                 text_color=('black', 'white'),
                                 border_color='#83a4cf', font=("Arial", 18))
        textarea.place(x=20, y=20)
        textarea.configure(state='disabled')
        ctk_textbox_scrollbar = tk.CTkScrollbar(master=frm, command=textarea.yview, height=394,
                                                fg_color=('white', 'black'),
                                                corner_radius=50)
        ctk_textbox_scrollbar.place(x=616, y=23)
        textarea.configure(yscrollcommand=ctk_textbox_scrollbar.set)
        input_area = tk.CTkEntry(master=frm, height=50, width=550, border_color='#83a4cf', corner_radius=50,
                                 fg_color=('white', 'black'),
                                 bg_color=('white', '#282c35'), text_color=('black', 'white'))
        input_area.place(x=20, y=430)
        input_area.configure(state='disabled')
        snd = tk.CTkImage(Image.open(resource_path("sendb.png")), size=(60, 60))
        lbs = tk.CTkButton(master=frm, bg_color=('white', '#282c35'), fg_color=('white', '#282c35'), width=65,
                           height=65, image=snd, text='',
                           hover_color=('white', '#282c35'),
                           command=lambda: write(input_area))
        lbs.place(x=570, y=420)

        def on_return(event):
            write(input_area)
            return 'break'

        def ch():
            if switch_var.get() == "on":
                tk.set_appearance_mode('light')
            else:
                tk.set_appearance_mode('dark')

        switch_var = tk.StringVar(value="on")
        switch = tk.CTkSwitch(frm_1, text="", command=ch, variable=switch_var, onvalue="on", offvalue="off")
        switch.place(x=490, y=443)
        tk.set_appearance_mode('light')
        lddm = tk.CTkLabel(frm_1, text='SWITCH TO DARK MODE', font=('Georgia bold', 20), text_color=('black', 'white'))
        lddm.place(x=180, y=440)

        input_area.bind('<KeyPress-Return>', on_return)
        receive_thread = threading.Thread(target=receive, args=(Online_menu, Offline_menu, rooms_menu, lb))
        receive_thread.start()
        sock.send("list".encode('utf'))
        time.sleep(0.1)

        gui_done = True
        win.protocol("WM_DELETE_WINDOW", stop)
    except Exception as inner_exception:
        print(f"An exception occurred while notifying clients: {type(inner_exception).__name__} - {inner_exception}")
        sock.close()
        root.destroy()
        sys.exit()


def monhistorique():
    sock.send('torique'.encode('utf-8'))


def crroom(eent):
    global nickname
    groupname = eent.get()
    if groupname == '':
        CTkMessagebox(title="Error", message="Please enter the name of your group", icon="cancel",
                      text_color='black',
                      fg_color='white', bg_color='#8696a9', title_color='black')
    else:
        sock.send('creergrp'.encode('utf-8'))
        time.sleep(0.1)
        sock.send(groupname.encode('utf-8'))
        time.sleep(0.1)
        sock.send(nickname.encode('utf-8'))
        eent.delete(0, 'end')
        CTkMessagebox(title='success', message='you created your room succesfully', icon='check')


def write(input_area):
    global nooomi
    if '^^!!?%' in nooomi:
        print('?????????')
        l67 = nooomi.split(sep='*')
        message = f"{nickname}@{input_area.get()}${l67[0]}"
        sock.send(message.strip().encode('utf-8'))
        message_1 = f"{input_area.get()}"
        textarea.configure(state='normal')
        textarea.insert('end', f"you: {message_1} ({datetime.now().hour}:{datetime.now().minute})\n")
        textarea.yview('end')
        textarea.configure(state='disabled')
        input_area.delete('0', 'end')
    else:
        if nooomi != nickname:
            message = f"{nickname}@{input_area.get()}@{nooomi}"
            sock.send(message.strip().encode('utf-8'))
            message_1 = f"{input_area.get()}"
            textarea.configure(state='normal')
            textarea.insert('end', f"you: {message_1}  ({datetime.now().hour}:{datetime.now().minute})\n")
            textarea.yview('end')
            textarea.configure(state='disabled')
        input_area.delete('0', 'end')


def stop():
    global running
    running = False
    root.destroy()
    sock.close()
    sys.exit()


def receive(Online_menu, Offline_menu, rooms_menu, lb):
    global textarea, theyear, them, thed
    global received_data
    global win
    global my_menu
    global nooomi
    global nickname
    global current_chat_context
    current_chat_context = None
    global input_area
    global last_clicked_item
    global menu_item_states
    global received_data
    global received_data_2
    menu_item_states = {}
    while running:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message == 'name':
                json_data = sock.recv(1024).decode('utf-8')
                received_data = json.loads(json_data)
                if nickname in received_data:
                    received_data.remove(nickname)
                json_data_1 = sock.recv(2048).decode('utf-8')
                received_data_1 = json.loads(json_data_1)
                received_data_2 = [item for sublist in received_data_1 for item in sublist]
                for offl in received_data:
                    received_data_2.remove(offl)
                received_data_2.remove(nickname)

                def change_op(se):
                    global nooomi
                    global last_clicked_item
                    global current_chat_context
                    lb.configure(text=f"you are chatting with {se}", font=('Georgia bold', 14))
                    if last_clicked_item is not None:
                        if last_clicked_item in received_data:
                            Online_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                        elif last_clicked_item in received_data_2:
                            Offline_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                        else:
                            rooms_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                    nooomi = se
                    Online_menu.entryconfig(se, state=tk.DISABLED)
                    last_clicked_item = se
                    current_chat_context = se

                def change_op_1(se_1):
                    global nooomi
                    global last_clicked_item
                    if last_clicked_item is not None:
                        if last_clicked_item in received_data:
                            Online_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                        elif last_clicked_item in received_data_2:
                            Offline_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                        else:
                            rooms_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                    nooomi = se_1
                    last_clicked_item = se_1
                    Offline_menu.entryconfig(se_1, state=tk.DISABLED)
                    lb.configure(text=f"you are chatting with {se_1}", font=('Georgia bold', 14))

                last_clicked_item = None
                Online_menu.delete(0, tkinter.END)
                for cconni in received_data:
                    menu_item_states[cconni] = tk.NORMAL
                    Online_menu.add_command(label=cconni,
                                            command=lambda selected_op=cconni: (
                                                change_op(selected_op), monhistorique(), enable_input_area()),
                                            state=menu_item_states[cconni])
                Offline_menu.delete(0, tkinter.END)
                for of in received_data_2:
                    menu_item_states[of] = tk.NORMAL
                    Offline_menu.add_command(label=of,
                                             command=lambda selcted_op_1=of: (
                                                 change_op_1(selcted_op_1), monhistorique(), enable_input_area()),
                                             state=menu_item_states[of])

                def enable_input_area():
                    global input_area
                    input_area.configure(state='normal')

                def monhistorique():
                    sock.send('torique'.encode('utf-8'))
            elif message == 'sift':
                global nooomi
                klj = nooomi.split(sep='*')
                sock.send((klj[0] + '#' + nickname).encode('utf-8'))
                hiisto = sock.recv(200000).decode('utf-8')
                liiisto = json.loads(hiisto)
                time.sleep(0.1)
                temps = sock.recv(200000).decode('utf-8')
                tam = json.loads(temps)
                textarea.configure(state='normal')
                textarea.delete(1.0, 'end')
                textarea.configure(state='disabled')
                if tam:
                    theyear = tam[0][0]
                    them = tam[0][1]
                    thed = tam[0][2]
                    textarea.configure(state='normal')
                    textarea.insert('end',
                                    f"                                                       {theyear}/{them}/{thed} \n")
                    textarea.yview('end')
                    textarea.configure(state='disabled')
                for i, j in zip(liiisto, tam):
                    if tam:
                        if i[0] == nickname:
                            if j[0] == theyear and j[1] == them and j[2] == thed:
                                textarea.configure(state='normal')
                                textarea.insert('end', f"you: {i[1].strip()} ({j[3]}:{j[4]})\n")
                                textarea.yview('end')
                                textarea.configure(state='disabled')
                            else:
                                textarea.configure(state='normal')
                                textarea.insert('end',
                                                f"                                                       {j[0]}/{j[1]}/{j[2]} \n")
                                textarea.yview('end')
                                textarea.configure(state='disabled')
                                textarea.configure(state='normal')
                                textarea.insert('end',
                                                f"you: {i[1].strip()} ({j[3]}:{j[4]}) \n")
                                textarea.yview('end')
                                textarea.configure(state='disabled')
                                theyear = j[0]
                                them = j[1]
                                thed = j[2]

                        else:
                            if tam:
                                if j[0] == theyear and j[1] == them and j[2] == thed:
                                    textarea.configure(state='normal')
                                    textarea.insert('end', f"{i[0]}: {i[1].strip()} ({j[3]}:{j[4]})\n")
                                    textarea.yview('end')
                                    textarea.configure(state='disabled')
                                else:
                                    textarea.configure(state='normal')
                                    textarea.insert('end',
                                                    f"                                                       {j[0]}/{j[1]}/{j[2]} \n")
                                    textarea.yview('end')
                                    textarea.configure(state='disabled')
                                    textarea.configure(state='normal')
                                    textarea.insert('end',
                                                    f"you: {i[1].strip()} ({j[3]}:{j[4]})\n")
                                    textarea.yview('end')
                                    textarea.configure(state='disabled')
                                    theyear = j[0]
                                    them = j[1]
                                    thed = j[2]
            elif message == 'touslesroom':
                def change_op_3(seu):
                    global nooomi
                    global current_chat_context
                    global menu_item_states
                    global last_clicked_item
                    if last_clicked_item is not None:
                        if last_clicked_item in received_data:
                            Online_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                        elif last_clicked_item in received_data_2:
                            Offline_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                        else:
                            rooms_menu.entryconfig(last_clicked_item, state=tk.NORMAL)
                    lb.configure(text=f"you are chatting in the room {seu}", font=('Georgia bold', 14))
                    last_clicked_item = seu
                    rooms_menu.entryconfig(seu, state=tk.DISABLED)
                    nooomi = seu + '*' + '^^!!?%'
                    kjl = nooomi.split(sep='*')
                    current_chat_context = kjl[0]
                    sock.send('jo2in'.encode('utf-8'))
                    time.sleep(0.1)
                    sock.send(seu.encode('utf-8'))
                    time.sleep(0.1)
                    sock.send(nickname.encode('utf-8'))

                tous = sock.recv(2048).decode('utf-8')
                trous_2 = json.loads(tous)
                trous_1 = [item for sublist in trous_2 for item in sublist]

                rooms_menu.delete(0, tkinter.END)
                for of_1 in trous_1:
                    try:
                        menu_item_states[of_1] = tk.NORMAL
                        rooms_menu.add_command(label=of_1,
                                               command=lambda selcted_op_3=of_1: (
                                                   change_op_3(selcted_op_3), monhistorique_1(), enable_input_area_1()),
                                               state=menu_item_states[of_1])
                    except Exception as inner_exception:
                        print(
                            f"An exception occurred while notifying clients: {type(inner_exception).__name__} - {inner_exception}")

                def enable_input_area_1():
                    global input_area
                    input_area.configure(state='normal')

                def monhistorique_1():
                    sock.send('torique'.encode('utf-8'))

            else:
                if gui_done:
                    message_ = message.split(sep='#')
                    if current_chat_context != message_[1]:
                        notification.notify(
                            title=f"New Message from {message_[1]}",
                            message=message_[0],
                            app_name='Instant Messaging',
                            app_icon="irst1.ico"
                        )

                    else:
                        textarea.configure(state='normal')
                        textarea.insert('end', f"{message_[0].strip()} ({datetime.now().hour}:{datetime.now().minute}) \n")
                        textarea.yview('end')
                        textarea.configure(state='disabled')
        except ConnectionAbortedError:
            break
        except Exception as e:
            print(f"An exception occurred : {type(e).__name__} - {e}")
            print("Error:")
            sock.close()
            root.destroy()
            sys.exit()
            break


def signup():
    root.withdraw()
    sign = tk.CTkToplevel(root)
    sign.title('Instant Messaging')
    sign.geometry('450x600+100+50')
    sign.configure(fg_color='white')
    sign.resizable(False, False)
    sign.wm_iconbitmap()
    root.after(300, lambda: sign.iconphoto(False, iconpath))

    userim = tk.CTkImage(Image.open(resource_path("user.png")), size=(30, 60))
    lo = tk.CTkImage(Image.open(resource_path("lock.png")), size=(42, 45))
    log1 = tk.CTkImage(Image.open(resource_path("cadre.png")), size=(450, 120))
    em = tk.CTkImage(Image.open(resource_path("emaili.png")), size=(37, 37))
    cad1 = tk.CTkImage(Image.open(resource_path("cadre1.png")), size=(450, 120))

    label_cad = tk.CTkLabel(sign, image=log1, bg_color='white', compound=tttk.BOTTOM, text='')
    label_cad.pack()
    label_cad1 = tk.CTkLabel(sign, image=cad1, bg_color='white', text='')
    label_cad1.place(x=0, y=480)
    labil = tk.CTkLabel(sign, bg_color='white', text='Sing Up', text_color='#333333', font=('Georgia bold', 29))
    labil.pack()

    def on1_enter(e):
        user_1.delete(0, 'end')

    def on1_leave(e):
        name = user_1.get()
        if name == '':
            user_1.insert(0, 'Username')

    frame1 = tk.CTkFrame(sign, corner_radius=50, width=310, height=70, fg_color='#83a4cf')
    frame1.place(x=60, y=170)
    user_1 = tk.CTkEntry(sign, width=250, height=30, bg_color='black', corner_radius=0, border_width=0,
                         fg_color="#83a4cf",
                         font=('Microsoft YaHei UI Light', 19), text_color='white')
    user_1.place(x=110, y=190)
    user_1.insert(0, 'Username')
    user_1.bind('<FocusIn>', on1_enter)
    user_1.bind('<FocusOut>', on1_leave)
    label_20 = tk.CTkLabel(sign, image=userim, bg_color='#83a4cf', text='')
    label_20.place(x=76, y=175)

    def on3_enter(e):
        email_1.delete(0, 'end')

    def on3_leave(e):
        name = email_1.get()
        if name == '':
            email_1.insert(0, 'Email')

    frame_1 = tk.CTkFrame(sign, corner_radius=50, width=310, height=70, fg_color='#83a4cf')
    frame_1.place(x=60, y=250)
    email_1 = tk.CTkEntry(sign, width=250, height=30, bg_color='black', corner_radius=0, border_width=0,
                          fg_color="#83a4cf",
                          font=('Microsoft YaHei UI Light', 19), text_color='white')
    email_1.place(x=110, y=270)
    email_1.insert(0, 'Email')
    email_1.bind('<FocusIn>', on3_enter)
    email_1.bind('<FocusOut>', on3_leave)
    label_em = tk.CTkLabel(sign, image=em, bg_color='#83a4cf', text='')
    label_em.place(x=73, y=267)

    def on_enter(e):
        code_1.delete(0, 'end')

    def on_leave(e):
        name = code_1.get()
        if name == '':
            code_1.insert(0, 'Password')

    frame2 = tk.CTkFrame(sign, corner_radius=50, width=310, height=70, fg_color='#83a4cf')
    frame2.place(x=60, y=330)
    code_1 = tk.CTkEntry(sign, width=250, height=30, bg_color='black', corner_radius=0, border_width=0,
                         fg_color="#83a4cf",
                         font=('Microsoft YaHei UI Light', 19), text_color='white')
    code_1.place(x=115, y=350)
    code_1.insert(0, 'Password')
    code_1.bind('<FocusIn>', on_enter)
    code_1.bind('<FocusOut>', on_leave)
    label_21 = tk.CTkLabel(sign, image=lo, bg_color='#83a4cf', text='')
    label_21.place(x=73, y=344)
    button_mode = True

    def hide():
        global button_mode
        if button_mode:
            if code_1.get() == 'Password':
                eyebutton.configure(image=closeeye, hover_color="#83a4cf")
                code_1.configure(show='')
                button_mode = False
            else:
                eyebutton.configure(image=closeeye, hover_color="#83a4cf")
                code_1.configure(show='*')
                button_mode = False
        else:
            eyebutton.configure(image=openeye, hover_color="#83a4cf")
            code_1.configure(show='')
            button_mode = True

    openeye = tk.CTkImage(Image.open(resource_path("openeye.png")), size=(35, 35))
    closeeye = tk.CTkImage(Image.open(resource_path("closeeye.png")), size=(32, 32))
    eyebutton = tk.CTkButton(sign, image=openeye, text='', fg_color='#83a4cf', corner_radius=0, command=hide, width=50,
                             height=46, hover_color="#83a4cf")
    eyebutton.place(x=309, y=340)

    def conne():
        global nickname
        nickname = user_1.get()
        mycode = code_1.get()
        myemail = email_1.get()
        if nickname == 'Username' or mycode == 'Password' or myemail == 'Email' or mycode == '' or myemail == '' or nickname == '':
            CTkMessagebox(title="Error", message="Please fill out all the required fields", icon="cancel",
                          text_color='black',
                          fg_color='white', bg_color='#8696a9', title_color='black')
        else:
            sock.send("its comming".encode('utf-8'))
            lista = nickname, mycode, myemail
            json_data = json.dumps(lista)
            sock.send(json_data.encode('utf-8'))
            m = sock.recv(1024).decode('utf-8')
            if m == "can't":
                CTkMessagebox(title="Error", message="username already exist", icon="cancel", text_color='black',
                              fg_color='white', bg_color='#8696a9', title_color='black')
            else:
                CTkMessagebox(title='success', message='you created an account succesfully', icon='check')
                root.deiconify()
                sign.destroy()

    button_signup = tk.CTkButton(sign, text='sign Up', bg_color='white', fg_color='#83a4cf', corner_radius=50,
                                 height=60,
                                 command=lambda: threading.Thread(target=conne).start())
    button_signup.place(x=145, y=430)


def conn():
    global nickname
    nickname = user.get()
    cooode = code.get()
    if cooode == 'Password' or cooode == '' or nickname == '' or nickname == 'Username':
        CTkMessagebox(title="Error", message="Please fill out all the required fields", icon="cancel",
                      text_color='black',
                      fg_color='white', bg_color='#8696a9', title_color='black')
    else:
        messaaaage = f"{nickname}#{cooode}"
        sock.send("verf".encode('utf-8'))
        time.sleep(0.1)
        sock.send(messaaaage.encode('utf-8'))
        verfi = sock.recv(1024).decode('utf-8')
        if verfi == "didn't found it":
            CTkMessagebox(title="Error", message="Username or password is wrong", icon="cancel", text_color='black',
                          fg_color='white', bg_color='#8696a9', title_color='black')
            user.delete("0", "end")
            code.delete("0", "end")
        else:
            root.withdraw()
            gui_loop()


def stop_1():
    root.destroy()
    sock.close()
    sys.exit()


root = tk.CTk()
root.title('Instant Messaging')
root.geometry('450x600+100+50')
root.configure(fg_color='white')
root.resizable(False, False)
iconpath = ImageTk.PhotoImage(file=os.path.join(resource_path("irst.png")))
tk.set_appearance_mode('light')
root.wm_iconbitmap()
root.iconphoto(False, iconpath)
userim = tk.CTkImage(Image.open(resource_path("user.png")), size=(30, 60))
lo = tk.CTkImage(Image.open(resource_path("lock.png")), size=(42, 45))
log = tk.CTkImage(Image.open(resource_path("logine.png")), size=(200, 200))
co = tk.CTkImage(Image.open(resource_path("corner.png")), size=(200, 160))
label_27 = tk.CTkLabel(root, image=co, bg_color='white', text='')
label_27.place(x=0, y=0)
co1 = tk.CTkImage(Image.open(resource_path("corner1.png")), size=(200, 160))
label_23 = tk.CTkLabel(root, image=co1, bg_color='white', text='')
label_23.place(x=250, y=440)


def on1_enter(e):
    user.delete(0, 'end')


def on1_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


frame1 = tk.CTkFrame(root, corner_radius=50, width=310, height=70, fg_color='#83a4cf')
frame1.place(x=60, y=250)
user = tk.CTkEntry(root, width=250, height=30, bg_color='black', corner_radius=0, border_width=0, fg_color="#83a4cf",
                   font=('Microsoft YaHei UI Light', 19), text_color='white')
user.place(x=110, y=270)
user.insert(0, 'Username')
user.bind('<FocusIn>', on1_enter)
user.bind('<FocusOut>', on1_leave)
label_20 = tk.CTkLabel(root, image=userim, bg_color='#83a4cf', text='')
label_20.place(x=76, y=255)

label_22 = tk.CTkLabel(root, image=log, bg_color='white', text='')
label_22.place(x=115, y=0)


def on2_enter(e):
    code.delete(0, 'end')


def on2_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')


frame2 = tk.CTkFrame(root, corner_radius=50, width=310, height=70, fg_color='#83a4cf')
frame2.place(x=60, y=350)
code = tk.CTkEntry(root, width=250, height=30, bg_color='black', corner_radius=0, border_width=0, fg_color="#83a4cf",
                   font=('Microsoft YaHei UI Light', 19), text_color='white')
code.place(x=115, y=370)
code.insert(0, 'Password')
code.bind('<FocusIn>', on2_enter)
code.bind('<FocusOut>', on2_leave)
label_21 = tk.CTkLabel(root, image=lo, bg_color='#83a4cf', text='')
label_21.place(x=73, y=364)

button_34 = tk.CTkButton(root, text='Login', bg_color='white', fg_color='#83a4cf', corner_radius=50, height=60,
                         command=lambda: threading.Thread(target=conn).start())
button_34.place(x=145, y=450)


def on_return_1(event):
    threading.Thread(target=conn).start()


code.bind('<KeyPress-Return>', on_return_1)

label = Label(root, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=100, y=530)

sign_up = Button(root, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=signup)
sign_up.place(x=240, y=530)
button_mode = True


def hide():
    global button_mode
    if button_mode:
        if code.get() == 'Password':
            eyebutton.configure(image=closeeye, hover_color="#83a4cf")
            code.configure(show='')
            button_mode = False
        else:
            eyebutton.configure(image=closeeye, hover_color="#83a4cf")
            code.configure(show='*')
            button_mode = False
    else:
        eyebutton.configure(image=openeye, hover_color="#83a4cf")
        code.configure(show='')
        button_mode = True


openeye = tk.CTkImage(Image.open(resource_path("openeye.png")), size=(35, 35))
closeeye = tk.CTkImage(Image.open(resource_path("closeeye.png")), size=(32, 32))
eyebutton = tk.CTkButton(root, image=openeye, text='', fg_color='#83a4cf', corner_radius=0, command=hide, width=50,
                         height=46, hover_color="#83a4cf")
eyebutton.place(x=309, y=365)
label_25 = tk.CTkLabel(root, text='Login', fg_color='white', bg_color='black',
                       text_color='#333333', font=('Georgia bold', 29))
label_25.place(x=175, y=198)
root.protocol("WM_DELETE_WINDOW", stop_1)
try:
    root.mainloop()
except KeyboardInterrupt:
    pass
