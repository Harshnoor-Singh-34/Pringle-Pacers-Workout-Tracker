import psycopg2

con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
cur = con.cursor()

id = 69
name = "'Harshnoor'"
lname = "'Singh'"
email = "'harshnoor34@gmail.com'"
password = "'password'"
dob = "'2004-09-27'"
sex = "'Male'"

table = '"Customer"'

cur.execute(f'INSERT INTO {table} ("Userid", "fname", "lname", "email", "password", "birthdate", "sex") VALUES ({id}, {name}, {lname}, {email}, {password}, {dob}, {sex})')
con.commit()
con.close()

# id = 69
# name = "Harshnoor"
# lname = "Singh"
# email = "harshnoor34@gmail.com"
# password = "password"
# dob = "2004-09-27"
# sex = "Male"

# cur.execute('INSERT INTO "Customer" ("Userid", "fname", "lname", "email", "password", "birthdate", "sex") VALUES (?,?,?,?,?,?,?)', (id, name, lname, email, password, dob, sex))
# con.commit()
# con.close()
