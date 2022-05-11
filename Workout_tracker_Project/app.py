
from flask import *
import sqlite3

DATABASE = "[DatabaseName].db"
TABLE = "[TableName]"
COLUMNS = "[ColumnNames]"

app = Flask(__name__)

# load the index.html
@app.route("/")
def index():
	return render_template("index.html")
	
# list items database
@app.route("/list", methods=["POST", "GET"])
def listItems():
	con = sqlite3.connect(DATABASE)
	cur = con.cursor()
	cur.execute("SELECT rowid, * FROM person ORDER BY lastname")
	items = cur.fetchall()
	con.close()
	return render_template("list.html", rows = items)
	
# add an item 
@app.route("/add", methods =["POST", "GET"])
def addItem():
	if request.method == "POST":
		fname = request.form["fname"]
		lname = request.form["lname"]
		age = request.form["age"]
		
		con = sqlite3.connect(DATABASE)
		cur = con.cursor()
		cur.execute("INSERT INTO person (firstname, lastname, age) VALUES (?,?,?)", (fname, lname, age))
		con.commit()
		con.close()
	return render_template("add.html")
	
# delete a row from the database
@app.route("/delete", methods = ["POST", "GET"])
def delete():
	if request.method == "POST":
		delete_key = request.form["deletekey"]
		con = sqlite3.connect(DATABASE)
		cur = con.cursor()
		cur.execute("DELETE FROM person WHERE rowid=?", delete_key)
		con.commit()
		con.close()
	return redirect(url_for("listItems"))

if __name__ == "__main__":
	app.run(debug=True)

