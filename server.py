from flask import Flask, render_template, request, redirect, session, flash #make sure to import request and redirect
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

#RUN THIS TO LAUNCH python -m pipenv install flask PyMySQL

app = Flask(__name__)
app.secret_key = "speak friend and enter"

@app.route("/")
def index():
    mysql = connectToMySQL('email_schema')           # call the function, passing in the name of our db
    emails = mysql.query_db('SELECT * FROM emails;')  # call the query_db function, pass in the query as a string
    return render_template("index.html", emails = emails)

@app.route('/post_email', methods=["POST"]) 
def create_post_method():
#REGEX VALIDATION
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        flash("Invalid email address!")
#CONNECT TO DB
    else:
        mysql = connectToMySQL('email_schema')

        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());" 

        data = {
            "email": request.form["email"],
        }

        db = connectToMySQL('email_schema')
        mysql.query_db(query, data)
        flash("Success Message")

    return redirect("/") #you need to redirect or it will keep posting

if __name__ == "__main__":
    app.run(debug=True)