# Before running program, you will have to install mysql connector and also set up mysql. then you have to create a database within mysql called 'program'
# and then you will have to create two tables with 'program' called 'data' and 'data2' with the below commands:
# -> CREATE DATABASE program;
# -> CREATE TABLE data(username VARCHAR(150) NOT NULL, password VARCHAR(150) NOT NULL);
# -> CREATE TABLE data2(usern VARCHAR(150) NOT NULL, T VARCHAR(150) NOT NULL, ID VARCHAR(150) NOT NULL, p VARCHAR(150) NOT NULL);
# -> INSERT INTO data (username='test', password='password')
# Please restart mysql after creating database and tables to be able to run program without any errors.

# The program is primarily made with use of functions to simplify code and also to switch between menus (login, creating user, deleting user, etc.) with ease.

import mysql.connector
conn=mysql.connector.connect(user='www-data', password='hackvell', host='127.0.0.1', database='program') #<- please enter your own username and password for mysql
cr=conn.cursor(buffered=True)                                                                            #<- had to use these codes to eliminate errors
conn.autocommit = True                                                                                   #<- had to use these codes to eliminate errors

query=0
data=0

def login():                                                                                       #<- this is the login section. inputs from here are sent to get_user
    print("\n*********************** Mr.PassMan At Your Service*********************\n")                   #   function and user_Check functions
    input1=int(input("Please enter 1 for Login, 2 for Create Account, 3 to end me: "))
    if input1 == 1:
        user=input("\nPlease enter your username: ")
        passw=input("Please enter your password : ")
        get_user(user,passw)
    elif input1 == 2:
        user=input("\nPlease enter a username: ")
        passw=input("Please enter a password : ")
        user_Check(user,passw)
    elif input1 == 3:
        conn.close()
        quit()
    else:
        print("\nWrong input. Please run program again.")


def user_Check(user,passw):
	cr.execute('SELECT * FROM data')
	for (username, password) in cr:
		if user==username and passw==password:
			b=1
		else:
			b=0
			create_user(user, passw)
	if b==1:
		print("Account Created Successfully. Welcome!")
		user_menu(user, passw)


def user_menu(user, passw):
	print("\nHola!. Welcome to Mr.passman's password managing service\n")
	print("\n1: Retrieve stored usernames and passwords\n2: Delete this account\n3: Delete a stored username or password\n4: Update password")
	print("5: Exit\n")
	opt=input("enter the number of the option you wish: ")
	if opt=='1':
		pass_list(user)
		user_menu(user,passw)
	elif opt=='2':
		cr.execute("SELECT * FROM data")
		make_sure=input("Are you sure you want to delete your account? all your data will be lost.(yes/no)\n")
		if make_sure=='yes':
			sure_pass=input("Enter Your Password: ")
			if sure_pass==passw:
				cr.execute("DELETE FROM data WHERE username=%s AND password=%s", (user, passw))
				cr.execute("DELETE FROM data2 WHERE usern=%s", (user,))
				print("Account Deleted.")
				login()
			else:
				print("Error occured! Please try again.")
				user_menu()
		else:
			print("Error occured. Please try again.")
			user_menu(user,passw)
	elif opt=='3':
		T=input('type the username of the data you want to remove: ')
		cr.execute("DELETE FROM data2 WHERE T=%s", (T,))
		print("Data Deleted.")
		user_menu(user, passw)
	elif opt=='4':
		current=input("Currunt Password: ")
		if current==passw:
			new_pass=input("New Password: ")
			cr.execute("UPDATE data SET password=%s WHERE username=%s", (new_pass,user))
			print("Password changed succesfully.")
			user_menu(user, passw)
			

							


def pass_list(user):
    print("\nSaved usernames and passwords for ",user,": \n")
    cr.execute("SELECT * FROM data2")
    for (usern,T, ID, p) in cr:
        if usern==user:
            print(T,"-->   username: ",ID,", password: ",p)
        else:
            pass
            
            
def create_user(user, passw):
	cr.execute("INSERT INTO data (username, password) VALUES (%s, %s)", (user, passw))
	cr.execute("SELECT * FROM data WHERE username=%s AND password=%s", (user, passw))
	for (username, password) in cr:
		if username == user and password==passw:
			print("Account Created. Welcome!")
			user_menu(user, passw)
		else:
			print("Error Occured. please try again.")
			login()


def del_user(user, passw):
	cr.execute("SELECT * FROM data")
	make_sure=input("Are you sure you want to delete your account? all your data will be lost.(yes/no)\n")
	if make_sure=='yes':
		sure_pass=input("Enter Your Password: ")
		if sure_pass==passw:
			cr.execute("DELETE FROM data WHERE username=%s AND password=%s", (user, passw))
			cr.execute("DELETE FROM data2 WHERE user=%s", (user))
			print("Account Deleted.")
			login()
		else:
			print("Error occured! Please try again.")
			user_menu()
	else:
		print("Error occured. Please try again.")
		user_menu(user,passw)


def get_user(user, passw):
	x=0
	cr.execute('SELECT * FROM data;')
	for (username, password) in cr:
		if username==user and password==passw:
			x=1
		elif username != user and password != passw:
			x=2
		else:
			x=0
	if x==1:
		print("successfull Login. Welcome")
		user_menu(user, passw)
	elif x==2:
		print("Username Or password is Incorrect!")
	else:
		print("Something Went Wrong!")







login()





