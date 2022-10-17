from turtle import st
from flask import Flask,render_template, request
import sqlite3 as sql

app = Flask(__name__)
app.secret_key="secret-key"


@app.route('/')
def Homepage():
   return render_template('Homepage.html')

@app.route('/ProfilesandSections')
def ProfilesandSections():
   return render_template('ProfilesandSections.html')

@app.route('/AboutandHomepage')
def AboutandHomepage():
   return render_template('AboutandHomepage.html')


@app.route('/Login',methods=["GET","POST"])
def Login():
   if request.method=='POST':
     try:
        name = request.form['name']
        email=request.form['email']
        password=request.form['password']

        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO login (name,email,password) VALUES (?,?,?)",(name,email,password))
            con.commit()
            msg = "Record successfully added!"
     except:
       msg = "error in insert operation"


  

@app.route('/SignUp',methods = ['POST', 'GET'])
def SignUp():
   if request.method == 'POST':
      try:
         name = request.form['name']
         email = request.form['email']
         password = request.form['password']
         password1 = request.form['password1']
         if(password==password1):
            return render_template("Login.html")
         else:
            msg="Password mismatch"
            return render_template("SignUp.html")
      except:

         @app.route('/logout')
         def logout():
           return render_template("Homepage")


if __name__ == '__main__':
   app.run(debug = True)
