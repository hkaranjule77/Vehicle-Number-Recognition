# third-party library
from mysql import connector

# credentials for Database
mydb = connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="anpr_db"
)



def insert_plate(num_plate):
  ''' Inserts value of plate in a anpr_db(database name). '''
  mycursor = mydb.cursor()

  insert_query = "INSERT INTO records(number) VALUES ('%s')"
  mycursor.execute(insert_query %(num_plate))

  mydb.commit()

  if mycursor.rowcount > 0:
    return True
  return False