import requests, time
from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from threading import Thread

def send_message(event = None):
	my_session.get(f'{url}sendMessage.jsp?username={username}&message={txt_message.get()}')
	txt_message.delete(0, last = END)

def get_active_users():
	try:
		while True:
			response = my_session.get(f'{url}activeUsers.jsp?username={username}')
			active_users.config(state = 'normal')
			active_users.delete(1.0, END)
			active_users.insert(END, response.text.strip().replace("<br>", ""))
			active_users.config(state = DISABLED)
			time.sleep(2)
	except:
		print("", end = '')

def get_new_messages():
	try:
		while True:
			response = my_session.get(f'{url}showMessages.jsp?username={username}')
			chat_box.config(state = 'normal')
			if response.text.strip() != "":
				chat_box.delete(1.0, END)
				chat_box.insert(END, f'{response.text.strip()}\n')
			chat_box.config(state = DISABLED)
			time.sleep(1)
	except:
		print("", end = '')

def sign_out(event = None):
	try:
		my_session.get(f'{url}signOut.jsp?username={username}')
		messagebox.showinfo('Message', 'Logged out succesfully!')	
		window.destroy()
		show_login_window()
	except:
		print("", end = '')

def change_status(event):
	btn_send.config(state = ('disabled' if txt_message.get() == '' else 'normal'))

def chat_area(username):
	global txt_message, window, chat_box, active_users, btn_send
	window = Tk()
	window.geometry('500x500')
	window.title('Chat Window!')
	window.resizable(0, 0)
	window.bind("<FocusIn>", change_status)
	window.bind("<ButtonRelease>", change_status)

	lbl_active = Label(window, text = 'Active Users')
	lbl_active.pack()

	active_users = Text(window, height = 4, width = 25)
	active_users.pack()
	active_users.config(state = DISABLED)

	send_msg_lbl = Label(window, text = 'Enter message: ')
	send_msg_lbl.place(x = 55, y = 415)

	chat_box = scrolledtext.ScrolledText(window,  height = 18, width = 25)
	chat_box.pack()
	chat_box.config(state = DISABLED)

	txt_message = Entry(window, width = 20)
	txt_message.bind("<Return>", send_message)
	txt_message.place(x = 165, y = 415)
	txt_message.focus_set()

	btn_send = Button(window, text = 'Send Message', command = send_message)
	btn_send.place(x = 185, y = 440)

	btn_sign_out = Button(window, text = 'Sign out', command = sign_out)
	btn_sign_out.place(x = 340, y = 410)
	Thread(target = get_active_users).start()
	Thread(target = get_new_messages).start()

	window.bind("<Key>", change_status)
	mainloop()

def login_reg(name, password, chat_window):
	global username 
	username = name
	response = my_session.get(f'{url}register.jsp?username={username}&password={password}')
	if (response.text.find('Logged') > 0 or response.text.find('Registered') > 0):
		messagebox.showinfo('Successful', 'Welcome to Chat Room!')
		chat_window.destroy()
		chat_area(username)
	else:
		messagebox.showinfo('Login failed', 'Invalid credentials!')

def change_button_status(event):
	btn_reg_login.config(state = ('disabled' if txt_username.get() == '' or txt_password.get() == '' else 'normal'))

def show_login_window():
	global username, txt_password, btn_reg_login, txt_username
	chat_window = Tk()
	chat_window.geometry('350x250')
	chat_window.title('Login Window!')
	chat_window.resizable(0, 0)
	chat_window.bind('<FocusIn>', change_button_status)

	lbl_username = Label(chat_window, text = 'Enter Username: ')
	lbl_username.pack()

	txt_username = Entry(chat_window, width = 20)
	txt_username.pack()
	txt_username.focus_set()

	lbl_password = Label(chat_window, text = 'Enter Password: ')
	lbl_password.pack()

	txt_password = Entry(chat_window, show='*')
	txt_password.pack()

	btn_reg_login = Button(chat_window, text = 'Login/Register', command = lambda: login_reg(txt_username.get(), txt_password.get(), chat_window))
	btn_reg_login.pack()

	chat_window.bind("<Key>", change_button_status)
	mainloop()

my_session = requests.Session()
url = 'http://165.22.14.77:8080/Narsi/ChatRoom/'
show_login_window()