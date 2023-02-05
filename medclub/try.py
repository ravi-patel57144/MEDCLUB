import mysql.connector

conn=mysql.connector.connect(user='sandip247' , password='S@ndip123' , host="testdatabase247.database.windows.net.mysql.database.azure.com", port=3306, database='myDataBase')

if conn:
  print("yes")