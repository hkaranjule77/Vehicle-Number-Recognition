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

def select_plate():
  ''' Gets all Vehicle Registration Number 
  data from Database. '''
  select_cur = mydb.cursor()
  select_query = "SELECT datetime, number from records"
  select_cur.execute(select_query)
  return select_cur.fetchall()

if __name__=="__main__":
  print(type(select_plate()[0][0]))