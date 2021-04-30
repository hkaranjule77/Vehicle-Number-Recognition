from mysql import connector

mydb = connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="anpr_db"
)



def insert_plate(num_plate):
  mycursor = mydb.cursor()

  insert_query = "INSERT INTO records(number) VALUES ('%s')"
  mycursor.execute(insert_query %(num_plate))

  mydb.commit()

  print(mycursor.rowcount, "record inserted.")
  return True