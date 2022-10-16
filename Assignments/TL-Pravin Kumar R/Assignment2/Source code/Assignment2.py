from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from markupsafe import escape



conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=<hostname>;PORT=<port>;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=<username>;PWD=<password>",'','')
print(conn)
print("connection successful...")

app = Flask(__name__)
app.secret_key="secret-key"


@app.route('/')
def home():
   return render_template('home.html')

@app.route('/profile')
def profile():
   return render_template('profile.html')

@app.route('/about')
def about():
   return render_template('about.html')


@app.route('/signin',methods=["GET","POST"])
def signin():
   if request.method=='POST':
      email=request.form['email']
      password=request.form['password']
      sql =f"SELECT * from users where email='{escape(email)}' and password='{escape(password)}'"
      stmt = ibm_db.exec_immediate(conn, sql)
      data = ibm_db.fetch_both(stmt)
      if data:
         session["name"]=escape(name)
         session["email"]=escape(email)
         session["password"]=escape(password)
         return redirect(url_for("profile"))
      else:
         flash("Username and Password Mismatch","danger")
         return redirect(url_for("signin"))
   return render_template('signin.html')

@app.route('/signup',methods = ['POST', 'GET'])
def signp():
   if request.method == 'POST':
      try:
         name = request.form['name']
         email = request.form['email']
         contact=request.form['contact']
         password = request.form['password']
         password1 = request.form['password1']
         if(password==password1):
            insert_sql = "INSERT INTO users(name,email,contact,password,password1)values(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,name)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,contact)
            ibm_db.bind_param(prep_stmt,4,password)
            ibm_db.bind_param(prep_stmt,5,password1)
            ibm_db.execute(prep_stmt)
            return redirect(url_for("signin"))
         else:
            flash("Password Mismatch","danger")
            return redirect(url_for("signup"))
      except:
         flash("Error","danger")
      
   return render_template("signup.html")


@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for("home"))


if __name__ == '__main__':
   app.run(debug = True)