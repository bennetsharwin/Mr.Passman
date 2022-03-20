from time import sleep
import subprocess as sp
import pyautogui as pg

def install_packages():
    sp.run("sudo apt install python3", shell=True)
    sp.run("sudo python3 -m pip install mysql-connector", shell=True)
    sp.run("sudo systemctl start mysql.service", shell=True)
    sp.run("sudo python3 -m pip install pyautogui", shell=True)

install_packages()


def create_user():
    sp.run("gnome-terminal &", shell=True)
    sleep(5)
    pg.write("sudo mysql")
    pg.press('Enter')
    sleep(8)
    pg.write("CREATE USER 'passman' IDENTIFIED BY 'password123';")
    sleep(0.5)
    pg.press('Enter')
    sleep(0.5)
    pg.write('exit')
    pg.press('Enter')
    pg.press('Enter')
    pg.write("exit")
    pg.press('Enter')

create_user()

import mysql.connector as MC

print("You need to run this programm once only.")

MCU = input("Enter Your Mysql User Name: ")
MCP = input("Enter your Mysql User Password: ")

conn = MC.connect(user=MCU, 
                    password=MCP,
                    host="127.0.0.1"
                    )

cr = conn.cursor(buffered=True)
conn.autocommit = True

def DB():
    cr.execute("CREATE DATABASE program;")
    print("Created database 'Program'\n ")
    cr.execute("USE program;")
    cr.execute("CREATE TABLE data(username VARCHAR(150) NOT NULL, password VARCHAR(150) NOT NULL);")
    print("Created Table 'data'\n")
    cr.execute("CREATE TABLE data2(usern VARCHAR(150) NOT NULL, T VARCHAR(150) NOT NULL, ID VARCHAR(150) NOT NULL, p VARCHAR(150) NOT NULL);")
    print("Created Table 'data2'\n")
    cr.execute("INSERT INTO data (username, password) VALUES ('main', 'password')")
    print("Inserted Main credentials")

def MySQL_USER():
    cr.execute("CREATE USER 'passman'@'localhost' IDENTIFIED BY 'password123';")
    print("Created User passman")
    cr.execute("GRANT ALL PRIVILEGES ON program.* TO 'passman'@'localhost'")
    print("Granted privilages of database to user: passman")




DB()
MySQL_USER()