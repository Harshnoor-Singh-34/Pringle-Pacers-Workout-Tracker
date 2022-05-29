import psycopg2
from flask import *
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "pringlepacerspp"

# load the index.html
@app.route("/")
def index():
	if session['user']:
		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"SELECT fname, lname FROM customer WHERE id='{session['user']}'")
		user = cur.fetchone()
		cur.execute(f"select w.*, cw.complete from customer_workout cw join workout w on cw.wid = w.w_id WHERE id={session['user']}")
		workouts = cur.fetchall()
		cur.execute(f"SELECT TO_CHAR(ca.date_finished :: DATE, 'dd/mm/yyyy'), a.name FROM customer_achivement ca JOIN achivements a on ca.aid = a.aid WHERE ca.id='{session['user']}' ORDER BY date_finished")
		achivement = cur.fetchone()
		con.close()
		return render_template("index.html", name = user, workouts = workouts, achivement = achivement)
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
		dob = request.form["dob"] or None
		sex = request.form["sex"]

		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"SELECT email FROM customer WHERE email='{email}'")
		results = cur.fetchall()
		con.close()
		if len(results) != 0 and email == results[0][0]:
			Errormessage = "Email already exists"
			return render_template("signup.html", Error = Errormessage)
		else:
			if password == confirmpass:
				table = 'customer (fname, lname, email, password, dob, sex)'
				con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
				cur = con.cursor()
				cur.execute(f"INSERT INTO {table} VALUES ('{fname}', '{lname}', '{email}', '{password}', '{dob}', '{sex}')")
				cur.execute(f"SELECT aid FROM achivements")
				aid = cur.fetchall() 
				cur.execute(f"SELECT id from customer where email = '{email}'")
				id = cur.fetchone();
				for achivement in aid:
					cur.execute(f"INSERT INTO customer_achivement(id, aid, complete) VALUES({id[0]}, {achivement[0]}, 0)")
				cur.execute(f"SELECT ca.caid from customer_achivement ca join achivements a on ca.aid = a.aid where a.name = 'Register an account' and ca.id = {session['user']}")
				caid = cur.fetchone()
				cur.execute(f"UPDATE customer_achivement set complete = 1, date_finished = NOW()  where caid = '{caid[0]}'")
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
				session['user'] = results[0][0]
				return redirect(url_for("index"))
			else:
				Errormessage = "Password incorrect"
				return render_template("login.html", Error = Errormessage)
	else:
		return render_template("login.html")

@app.route("/about-us", methods = ["GET"])
def aboutus():
	if session['user']:
		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"SELECT ca.caid, ca.complete from customer_achivement ca join achivements a on ca.aid = a.aid where a.name = 'Visit the about us page' and ca.id = {session['user']}")
		results = cur.fetchone()
		if int(results[1]) == 0:
			cur.execute(f"UPDATE customer_achivement set complete = 1, date_finished = NOW() WHERE caid = {results[0]}")
			con.commit()
		con.close()
	return render_template("aboutus.html")

@app.route("/profile", methods = ["GET"])
def profile():
	con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute(f"SELECT id, fname, lname, email, password, TO_CHAR(dob :: DATE, 'dd/mm/yyyy'), sex, height, weight FROM customer WHERE id='{session['user']}'")
	results = cur.fetchone()
	con.close()
	return render_template("profile.html", user = results)

@app.route("/profile-edit", methods = ["POST", "GET"])
def profileedit():
	if request.method == "POST":
		dob = request.form["dob"]
		sex = request.form["sex"]
		height = request.form["height"] or None
		weight = request.form["weight"] or None

		height_weight_sql = ""
		if height and weight:
			height_weight_sql += f",height={height}, weight={weight}"
		elif height:
			height_weight_sql += f",height={height}"
		elif weight:
			height_weight_sql += f",weight={weight}"

		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"UPDATE customer SET dob='{dob}', sex='{sex}' {height_weight_sql} WHERE id = {session['user']}")
		con.commit()
		con.close()

		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"SELECT ca.caid, ca.complete from customer_achivement ca join achivements a on ca.aid = a.aid where a.name = 'Edit your details' and ca.id = {session['user']}")
		results = cur.fetchone()
		if int(results[1]) == 0:
			cur.execute(f"UPDATE customer_achivement set complete = 1, date_finished = NOW() WHERE caid = {results[0]}")
			con.commit()
		con.close()
		return redirect(url_for("profile"))
	else:
		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"SELECT * FROM customer WHERE id='{session['user']}'")
		results = cur.fetchone()
		con.close()
		return render_template("profileedit.html", user = results)

@app.route("/workout-randomizer", methods = ["POST", "GET"])
def randomizer():
	if request.method == "POST":
		difficulty = request.form["difficulty"]
		exclude = request.form["exclude"]
		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"DELETE FROM customer_workout WHERE id = {session['user']}")
		con.commit()
		if difficulty == "":
			difficulty = None
		if exclude == "":
			exclude = None

		if difficulty and exclude:
			cur.execute(f"SELECT * FROM workout WHERE w_difficulty='{difficulty}' AND w_body !='{exclude}'")
		elif difficulty:
			cur.execute(f"SELECT * FROM workout WHERE w_difficulty='{difficulty}'")
		elif exclude:
			cur.execute(f"SELECT * FROM workout WHERE w_body !='{exclude}'")
		else:
			cur.execute(f"SELECT * FROM workout")
		workouts = cur.fetchall()
		random_workouts = []
		counter = 0
		while counter <= 7:
			random_workout = random.choice(workouts)
			if random_workout not in random_workouts:
				random_workouts.append(random_workout)
				cur.execute(f"INSERT INTO customer_workout(id,wid,complete) VALUES({session['user']}, {random_workout[0]}, 0)")
				con.commit()
				counter += 1
			
		con.close()


	con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute(f"select w.* from customer_workout cw join workout w on cw.wid = w.w_id WHERE id={session['user']}")
	results = cur.fetchall()
	con.close()
	return render_template("randomizer.html", workouts = results)


@app.route("/logout", methods = ["POST", "GET"])
def logout():
	session['user'] = None
	return redirect(url_for("login"))

@app.route("/mylist", methods = ["POST", "GET"])
def mylist():
	if request.method == "POST":
		if "workout" in request.form:
			workout = request.form["workout"]
			con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
			cur = con.cursor()
			cur.execute(f"UPDATE customer_workout set complete = 1 WHERE id={session['user']} AND wid='{workout}'")
			con.commit()
			con.close()
	con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute(f"select w.*, cw.complete from customer_workout cw join workout w on cw.wid = w.w_id WHERE id={session['user']};")
	results = cur.fetchall()
	con.close()
	return render_template("mylist.html", workouts = results)

@app.route("/workout", methods = ["POST", "GET"])
def workout():
	con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute(f"select * from workout where w_id not in (select wid from customer_workout WHERE id={session['user']})")
	results = cur.fetchall()
	con.close()
	return render_template("workout-select.html", workouts = results)

@app.route("/workout/<id>", methods = ["POST", "GET"])
def workout_select(id):
	con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute(f"INSERT INTO customer_workout (id,wid,complete) VALUES ({session['user']}, {id}, 0)")
	con.commit()
	con.close()
	return redirect(url_for("workout"))

@app.route("/bmi", methods = ["POST", "GET"])
def bmi():
	bmi = 0
	if request.method == "POST":
		sex = request.form["sex"]
		height = request.form["height"]
		weight = request.form["weight"]
		bmi = round(int(weight) / ((int(height))/100 * (int(height))/100), 2)


	if session['user']:
		print(1)
		con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
		cur = con.cursor()
		cur.execute(f"SELECT height, weight, sex FROM customer WHERE id={session['user']}")
		results = cur.fetchone()
		con.close()
		return render_template("bmi.html", data = results, bmi = bmi)
	return render_template("bmi.html", data = None, bmi = bmi)

@app.route("/achievement", methods = ["POST", "GET"])
def achivement():
	con = psycopg2.connect(dbname = "Workout", user = "PringlePacers", password = "PringlePacers27", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute(f"SELECT ca.complete, a.name, TO_CHAR(ca.date_finished :: DATE, 'dd/mm/yyyy') FROM customer_achivement ca join achivements a on ca.aid = a.aid WHERE ca.id='{session['user']}'")
	results = cur.fetchall()
	con.close()
	return render_template("achivement.html", achieve = results)

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

