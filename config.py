import mysql.connector

config = {
  'user': 'passman',
  'password': 'passmanme',
  'host': '127.0.0.1',
  'database': 'accounts',
  'raise_on_warnings': True
}

cnx = mysql.connector.connect(**config)

cnx.close()