# Before running program, you will have to install mysql connector and also set up mysql. then you have to create a database within mysql called 'program'
# and then you will have to create two tables with 'program' called 'data' and 'data2' with the below commands:
# -> CREATE DATABASE program;
# -> CREATE TABLE data(username VARCHAR(150) NOT NULL, password VARCHAR(150) NOT NULL);
# -> CREATE TABLE data2(usern VARCHAR(150) NOT NULL, T VARCHAR(150) NOT NULL, ID VARCHAR(150) NOT NULL, p VARCHAR(150) NOT NULL);
# -> INSERT INTO data (username='test', password='password')
# Please restart mysql after creating database and tables to be able to run program without any errors.

# The program is primarily made with use of functions to simplify code and also to switch between menus (login, creating user, deleting user, etc.) with ease.
import getpass
import hashlib
import os											 													 #<-os library is imported for colored user-prompt
import mysql.connector
conn=mysql.connector.connect(user='www-data', password='hackvell', host='127.0.0.1', database='program') #<- please enter your own username and password for mysql
cr=conn.cursor(buffered=True)                                                                            #<- had to use these codes to eliminate errors
conn.autocommit = True

query=0
data=0

class bcolors:						#<-these colors are added for nice user prompt    
    YELLOW = '\033[93m'	#YELLOW
    PURPLE = '\033[95m'	#purple
    RED = '\033[91m' 	#RED
    BLUE =  '\033[94m'	#BLUE
    GREEN =  '\033[92m'	#GREEN
    RESET = '\033[0m' 	#RESET COLOR's

def login():                                                                                       #<- this is the login section. inputs from here are sent to get_user
    print(bcolors.YELLOW + "\n*********************** Mr.PassMan At Your Service*********************\n" + bcolors.RESET)                   #   function and user_Check functions
    input1=int(input(bcolors.BLUE + "Please enter 1 for Login, 2 for Create Account, 3 to end me: " + bcolors.RESET))
    if input1 == 1:
        user=input(bcolors.GREEN + "\nPlease enter your username: " + bcolors.RESET)
        passw=getpass.getpass(bcolors.GREEN + "Please enter your password : " + bcolors.RESET)
        get_user(user,passw)
    elif input1 == 2:
        user=input(bcolors.BLUE + "\nPlease enter a username: " + bcolors.RESET)
        passw=input(bcolors.BLUE + "Please enter a password : " + bcolors.RESET)
        user_Check(user,passw)
    elif input1 == 3:
        conn.close()
        quit()
        

def check_string(STR):
	out = type(STR)
	if out == "<class 'int'>":
		print(bcolors.RED + "Wrong Output" + bcolors.RESET)
		login()
	else:
		print("Please Type a valid option")
		login()

#---------------------Encryption Area----------------------#

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def encryptNow(string):
	sha_signature = encrypt_string(string)
	print(sha_signature)
encryptNow('ben')

#---------------------End----------------------------------#

def user_Check(user,passw):
	cr.execute('SELECT * FROM data')
	for (username, password) in cr:
		if user==username and passw==password:
			b=1
		else:
			b=0
			create_user(user, passw)
	if b==1:
		print(bcolors.BLUE + "Account Created Successfully. Welcome!" + bcolors.RESET)
		user_menu(user, passw)


def user_menu(user, passw):
	#os.system('clear')
	print(bcolors.YELLOW + "\nHola!. Welcome to Mr.passman's password managing service\n" + bcolors.RESET)
	print(bcolors.BLUE + """		User Menu\n
	1: Retrieve stored usernames and passwords
	2: Delete this account
	3: Delete a stored username or password
	4: Update password
	5: Add data to the database
	6: Exit\n""" + bcolors.RESET)
	
	opt=input(bcolors.GREEN + "enter the number of the option you wish: " + bcolors.RESET)
	if opt=='1':
		pass_list(user)
		user_menu(user,passw)
	elif opt=='2':
		cr.execute("SELECT * FROM data")
		make_sure=input(bcolors.RED + "Are you sure you want to delete your account? all your data will be lost.(yes/no)\n" + bcolors.RESET)
		if make_sure=='yes':
			sure_pass=getpass.getpass(bcolors.RED + "Enter Your Password: " + bcolors.RESET)
			if sure_pass==passw:
				cr.execute("DELETE FROM data WHERE username=%s AND password=%s", (user, passw))
				cr.execute("DELETE FROM data2 WHERE usern=%s", (user,))
				print(bcolors.GREEN + "Account Deleted." + bcolors.RESET)
				login()
			else:
				print(bcolors.RED + "Error occured! Please try again." + bcolors.RESET)
				user_menu()
		else:
			print(bcolors.RED + "Error occured. Please try again." + bcolors.RESET)
			user_menu(user,passw)
	elif opt=='3':
		T=input(bcolors.BLUE + 'type the username of the data you want to remove: ' + bcolors.RESET)
		cr.execute("DELETE FROM data2 WHERE T=%s", (T,))
		print(bcolors.YELLOW + "Data Deleted." + bcolors.RESET)
		user_menu(user, passw)
	elif opt=='4':
		current=getpass.getpass(bcolors.BLUE + "Currunt Password: " + bcolors.RESET)
		if current==passw:
			new_pass=getpass.getpass(bcolors.BLUE + "New Password: " + bcolors.RESET)
			cr.execute("UPDATE data SET password=%s WHERE username=%s", (new_pass,user))
			print(bcolors.GREEN + "Password changed succesfully." + bcolors.RESET)
			user_menu(user, passw)
	elif opt=='5':
		print(bcolors.PURPLE + "\nAdd Data to the database:\n" + bcolors.RESET)
		add_data(user,passw)
	elif opt=='6':
		login()
	else:
		print(bcolors.RED + "You Haven't Selected any options. Please select one, or 6 to exit" + bcolors.RESET)
		user_menu(user,passw)

def add_data(user,passw):
	T=input(bcolors.BLUE + "Enter the id_name for it: " + bcolors.RESET)
	ID=input(bcolors.BLUE + "Please Enter a UserName or Email ID: " + bcolors.RESET)
	p=input(bcolors.BLUE + "Please enter a Password: " + bcolors.RESET)
	cr.execute("INSERT INTO data2 VALUES (%s, %s, %s, %s)",(user,T,ID,p))
	print(bcolors.YELLOW + "Data added to the Database." + bcolors.RESET)
	user_menu(user,passw)
							


def pass_list(user):
	os.system('clear')
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
			print(bcolors.GREEN + "Account Created. Welcome!" + bcolors.RESET)
			user_menu(user, passw)
		else:
			print(bcolors.RED + "Error Occured. please try again." + bcolors.RESET)
			login()


def del_user(user, passw):
	cr.execute("SELECT * FROM data")
	make_sure=input(bcolors.RED + "Are you sure you want to delete your account? all your data will be lost.(yes/no)\n" + bcolors.RESET)
	if make_sure=='yes':
		sure_pass=getpass.getpass(bcolors.PURPLE + "Enter Your Password: " + bcolors.RESET)
		if sure_pass==passw:
			cr.execute("DELETE FROM data WHERE username=%s AND password=%s", (user, passw))
			cr.execute("DELETE FROM data2 WHERE user=%s", (user))
			print(bcolors.GREEN + "Account Deleted." + bcolors.RESET)
			login()
		else:
			print(bcolors.RED + "Error occured! Please try again." + bcolors.RESET)
			user_menu()
	else:
		print(bcolors.RED + "Error occured. Please try again." + bcolors.RESET)
		user_menu(user,passw)


def get_user(user, passw):
	x=0
	cr.execute('SELECT * FROM data;')
	for (username, password) in cr:
		if username==user and password==passw:
			x=1
		elif username != user and password != passw:	#Wrong Password and Username!
			x=2
		elif username == user and password != passw:	#Wrong Password!
			x=3
		elif username != user and password == user:		#Wrong username!
			x=4
		else:
			x=0		#Any other errors.
	if x==1:
		print(bcolors.GREEN + "successfull Login. Welcome" + bcolors.RESET)
		os.system('clear')
		user_menu(user, passw)
	elif x==2:
		print(bcolors.RED + "Username Or password is Incorrect!" + bcolors.RESET)
		login()
	elif x==3:
		print(bcolors.RED + "\nWrong Password!" + bcolors.RESET)
		login()
	elif x==4:
		print(bcolors.RED + "Username Or password is Incorrect!" + bcolors.RESET)
	else:
		print(bcolors.RED + "Something Went Wrong!" + bcolors.RESET)
		os.system('clear')
		login()







login()




