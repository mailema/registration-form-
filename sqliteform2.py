from flask import Flask,render_template,redirect,session,flash,request
import sqlite3
import os

app=Flask(__name__)
app.secret_key='secret'

conn=sqlite3.connect('mysqlite.db')
curs=conn.cursor()
curs.execute("""CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT,password TEXT)""")
conn.commit()
conn.close()


@app.route('/home',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def loginpage():
    if request.method=='POST':
        myemail=request.form['email']
        mypassword=request.form['password']
        conn=sqlite3.connect('mysqlite.db')
        curs=conn.cursor()
        curs.execute("SELECT * FROM students WHERE email=? AND password=?",(myemail,mypassword))
        existing_user=curs.fetchone()
        if existing_user:
            return redirect('/result')
        else:
            flash("Invalid credentials!",'fail')
            return render_template('sqlogin.html')
    return render_template('sqlogin.html')


@app.route('/signup',methods=['GET','POST'])
def signuppage():
    if request.method=='POST':  
        myemail=request.form['email']
        mypassword=request.form['password']
        myname=request.form['fullname']
        mymobile=request.form['mobile']    
        conn=sqlite3.connect("mysqlite.db")
        curs=conn.cursor()
        curs.execute("SELECT * FROM students WHERE email=?",(myemail,))
        row=curs.fetchone()
        if row:
            flash("user already exist!",'fail')
        elif len(mypassword) > 10:
            flash("password too long!","fail")
            return render_template()
        elif len(mypassword) < 6:
            flash("password too short",'fail') 
        elif len(myname) > 12:
            flash("name too long!","fail")
            return render_template()
        elif len(myname) < 3:
            flash("name too short",'fail')
        elif  len(mymobile) != 11:
            flash("invalid number provided",'fail') 
        else:            
            #conn=sqlite3.connect('mysqlite.db') 
            #curs=conn.cursor()  
            curs.execute("INSERT INTO students (name,email,password) VALUES (?,?,?)", (myname,myemail,mypassword))
            conn.commit()
            flash("successfully registered","succeed") 
            return render_template('sqlsignup.html')            
    return render_template('sqlsignup.html')
    

@app.route('/update',methods=['GET','POST'])
def updatepage():
    if request.method=='POST':
        myemail=request.form['email']
        newpassword=request.form['password']
        conn=sqlite3.connect("mysqlite.db")
        curs=conn.cursor()
        curs.execute("UPDATE students SET password=? WHERE email=?",(newpassword,myemail))
        if curs.rowcount > 0:
            flash("successfully updated","succeed")
            conn.commit()
            return render_template('sqlupdate.html')
        else:
            flash("email not found!",'fail')
            return render_template('sqlupdate.html')
    return render_template('sqlupdate.html')



@app.route('/delete',methods=['GET','POST'])
def deletepage():
    if request.method=='POST':
        myemail=request.form['email']
        mypassword=request.form['password']   
        conn=sqlite3.connect("mysqlite.db")
        curs=conn.cursor()
        #curs.execute("DELETE FROM students WHERE email=? AND password=?",(myemail,mypassword))
        curs.execute("SELECT * FROM students WHERE email=? AND password=?",(myemail,mypassword))
        myuser=curs.fetchone()
        if myuser:
            curs.execute("DELETE FROM students WHERE email=? AND password=?",(myemail,mypassword))
            flash("user deleted successfully","succeed")
            conn.commit()
            conn.close()
        else:
            flash("invalid credential!","fail")
            conn.close()
            return render_template('sqldelete.html')
    return render_template('sqldelete.html')


@app.route('/result')
def resultpage():
    return render_template('sqlresult.html')
    
    

@app.route('/check')
def checkpage():
    conn=sqlite3.connect("mysqlite.db")
    curs=conn.cursor()
    curs.execute("SELECT * FROM students")
    rows=curs.fetchall()
    return render_template('checkresult.html',rows=rows)
    
@app.route('/adminpage',methods=['GET','POST'])   
def adminpage():
    if request.method=='POST':
        myemail=request.form['email']
        mypassword=request.form['password']  
        if myemail != 'ismailaufiydt@gmail.com':
            flash('incorrect email!','fail')
            return render_template('sqladminpage.html')
        elif mypassword != '106472023':
            flash('incorrect password!','fail')
            return render_template('sqladminpage.html')
        else:
            flash('login successful','succeed')
            return redirect('/admincheck')
    return render_template('sqladminpage.html')
            
@app.route('/admincheck')
def admincheck():
    return render_template('sqladmincheck.html')
        

if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port)
