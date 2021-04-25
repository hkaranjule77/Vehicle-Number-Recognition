import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="anpr_db"
)

mycursor = mydb.cursor()
a="MH 05 1154"

sql = "INSERT INTO records(number) VALUES ('%s')"
number = a
mycursor.execute(sql %(number))

mydb.commit()

print(mycursor.rowcount, "record inserted.")