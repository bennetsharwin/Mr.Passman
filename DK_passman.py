# Before running program, you will have to install mysql connector and also set up mysql. then you have to create a database within mysql called 'program'
# and then you will have to create two tables with 'program' called 'data' and 'data2' with the below commands:
# -> CREATE DATABASE program;
# -> CREATE TABLE data(username VARCHAR(150) NOT NULL, password VARCHAR(150) NOT NULL);
# -> CREATE TABLE data2(usern VARCHAR(150) NOT NULL, T VARCHAR(150) NOT NULL, ID VARCHAR(150) NOT NULL, p VARCHAR(150) NOT NULL);
# Please restart mysql after creating database and tables to be able to run program without any errors.

# The program is primarily made with use of functions to simplify code and also to switch between menus (login, creating user, deleting user, etc.) with ease.

import mysql.connector
conn=mysql.connector.connect(user='www-data', password='hackvell', host='127.0.0.1', database='program') #<- please enter your own username and password for mysql
cr=conn.cursor(buffered=True)                                                                            #<- had to use these codes to eliminate errors
conn.autocommit = True                                                                                   #<- had to use these codes to eliminate errors

query=0
data=0

def userlist(user):
    print("\nSaved usernames and passwords for ",user,": \n")
    cr.execute("SELECT * FROM data2")
    for (usern,T, ID, p) in cr:
        if usern==user:
            print(T,"-->   username: ",ID,", password: ",p)
        else:
            pass    
    
def get_user(user,passw):                                                                                      #<- programs are inside functions for ease and 
    x=0                                                                                                        #   also to jump between different programs quickly
    query="SELECT * FROM data"                                                                                 #<- this section searches for a user that is entered in
    cr.execute(query)                                                                                          #   login menu function
    for (username, password) in cr:
        if user == username and passw == password:
            x=1
            break
        elif user != username or passw != password:
            x=2
        else:
            x=0
    if x==1:
        print("\nSuccessful login! Welcome!")
        user_menu(user,passw)
    elif x==2:
        print("Username or password is wrong. Please run program again.")
    else:
        print("Error. Such account does not exist. Please run program again and create an new account")
        
def user_menu(user,passw):                                                                                    #<- this section is the main menu section
    y=0
    print("\nPlease enter the number which you would like to run. \n\n1: Change account password.")
    print("2: Delete account.\n3: Retrieve stored usernames and passwords.\n4: Add new data to database.\n5: Remove data from database. \n6: Exit and run program again.")
    option=input("\nPlease enter your option number: ")
    if option=='2':
        x=input("Are you sure you want to delete your account? (yes,no) : ")
        if x=="yes":
            p=input("Please enter your password: ")
            if p==passw:
                query="DELETE FROM data WHERE username=%s AND password=%s"
                data=(user,passw)
                cr.execute(query,data)
                cr.execute("DELETE FROM data2 WHERE usern=%s",(user,))
                print("Account deleted.")
                login()
            else:
                print("Error occured. Please try again.")
                user_menu(user,passw)
        else:
            print("\nSorry, error occured!")
    elif option=='1':
        if input("\nPlease enter your password to confirm: ")==passw:
            b=input("Please enter new password: ")
            cr.execute("UPDATE data SET password=%s WHERE username=%s",(b,user))
            user_menu(user,passw)
        else:
            print("Error. Please try again from menu.")
            user_menu(user,passw)
    elif option=='6':
        login()
    elif option=='3':
        userlist(user)
        user_menu(user,passw)
    elif option=='4':
        T=input("Enter the name for which you are saving data for: ")
        ID=input("Enter your username or email ID for it: ")
        p=input("Please enter your password for it: ")
        cr.execute("INSERT INTO data2 VALUES (%s, %s, %s, %s)",(user,T,ID,p))
        print("Data added!")
        user_menu(user,passw)
    elif option=='5':
        T=input("Enter the name for which you had saved data for: ")
        ID=input("Enter your username or email ID for it: ")
        p=input("Please enter your password for it: ")
        cr.execute("DELETE FROM data2 WHERE usern=%s AND T=%s AND ID=%s AND p=%s",(user,T,ID,p))
        print("Data deleted!")
        user_menu(user,passw)
        
def create_user(user,passw):                                                          #<- this section creates a new user from login section
    cr.execute("INSERT INTO data (username,password) VALUES (%s,%s)",(user,passw))
    cr.execute("SELECT * FROM data")
    for (username, password) in cr:
        if user == username and passw == password:
            print("\nSuccessfully created user account!")
            user_menu(user,passw)
        elif user != username and passw != password:
            continue
        else:
            print("\nError. Please run program again.")

def user_Check(user,passw):                                                            #<- this section checks if a username is taken. username is the primary key
    cr.execute("SELECT * FROM data")                                                   #   username cannot be changed once set. if a username is not taken, it 
    for (username, password) in cr:                                                    #   will take the inputs and send to create_user function
        if user==username:
            n=1
            break
        else:
            n=0
    if n==1:
        print("Username already in use. Please try again and enter a new username.")
        login()
    else:
        create_user(user,passw)
            
        
            
def login():                                                                                       #<- this is the login section. inputs from here are sent to get_user
    print("\n*********************** Password Manager *********************\n")                    #   function and user_Check functions
    input1=int(input("Please enter 1 for Login, 2 for Create Account, 3 to end program: "))
    if input1 == 1:
        user=input("\nPlease enter your username: ")
        passw=input("Please enter your password: ")
        get_user(user,passw)
    elif input1 == 2:
        user=input("\nPlease enter a username: ")
        passw=input("Please enter a password: ")
        user_Check(user,passw)
    elif input1 == 3:
        conn.close()
        quit()
    else:
        print("\nWrong input. Please run program again.")
        
login()

    
        
    
