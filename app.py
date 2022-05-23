import psycopg2
from flask import *

app = Flask(__name__)

# load the index.html
@app.route("/")
def index():
	return render_template("index.html")

# Sign-up page
@app.route("/sign-up", methods =["POST", "GET"])
def signup():
	Errormessage = None
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		confirmpass = request.form["confirmpass"]
		fname = request.form["fname"]
		lname = request.form["lname"]
		dob = request.form["dob"]
		sex = request.form["sex"]

		if password == confirmpass:
			table = 'customer (fname, lname, email, password, dob, sex)'
			con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
			cur = con.cursor()
			cur.execute(f"INSERT INTO {table} VALUES ('{fname}', '{lname}', '{email}', '{password}', '{dob}', '{sex}')")
			con.commit()
			con.close()
			return redirect(url_for("login"))
		else:
			Errormessage = "Paswords don't match"
			return render_template("signup.html", Error = Errormessage)
		
	else:
		return render_template("signup.html")

# Log-in page
@app.route("/login", methods =["POST", "GET"])
def login():
	Errormessage = None
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"SELECT * FROM customer WHERE email='{email}'")
		results = cur.fetchall()
		con.close()

		if len(results) == 0:
			Errormessage = "No such Email exists"
			return render_template("login.html", Error = Errormessage)
		else:
			if results[0][4] == password:
				return redirect(url_for("index"))
			else:
				Errormessage = "Password incorrect"
				return render_template("login.html", Error = Errormessage)
	else:
		return render_template("login.html")



# list items database
# @app.route("/list", methods=["POST", "GET"])
# def listItems():
	#con = sqlite3.connect(DATABASE)
	#cur = con.cursor()
	#cur.execute("SELECT rowid, * FROM person ORDER BY lastname")
	#items = cur.fetchall()
	#con.close()
	#return render_template("list.html", rows = items)
	
# add an item 
#@app.route("/add", methods =["POST", "GET"])
# def addItem():
# 	if request.method == "POST":
# 		fname = request.form["fname"]
# 		lname = request.form["lname"]
# 		age = request.form["age"]
		
		# con = sqlite3.connect(DATABASE)
		# cur = con.cursor()
		# cur.execute("INSERT INTO person (firstname, lastname, age) VALUES (?,?,?)", (fname, lname, age))
		# con.commit()
		# con.close()
	# return render_template("add.html")
	
# delete a row from the database
# @app.route("/delete", methods = ["POST", "GET"])
# def delete():
# 	if request.method == "POST":
# 		delete_key = request.form["deletekey"]
# 		# con = sqlite3.connect(DATABASE)
# 		# cur = con.cursor()
# 		# cur.execute("DELETE FROM person WHERE rowid=?", delete_key)
# 		# con.commit()
# 		# con.close()
# 	return redirect(url_for("listItems"))

if __name__ == "__main__":
	app.run(debug=True)

