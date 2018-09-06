from flask import Flask, render_template, g, request, redirect, session
app = Flask(__name__)
import sqlite3
import os
app.secret_key = "super secret key"
app.database = "userdb.db"

def create_connection(db_file):

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT);")
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (username TEXT , tasks TEXT, state TEXT);")

if __name__ == '__main__':
    create_connection("userdb.db")

@app.before_request
def before_request():
    g.db = sqlite3.connect("userdb.db")
 
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/signup', methods = ['POST'])
def signup():
    username = request.form["username"]
    g.db.execute("INSERT INTO users VALUES (?)", [username])
    g.db.commit()
    return redirect('/')

@app.route('/addedit', methods = ['GET', 'POST'])
def addedit():
    if request.method == 'POST':    
       username = session["username"]
       new_task = request.form['add']
       c_state = "No" 
       g.db.cursor()   
       g.db.execute("INSERT INTO tasks (username,tasks,state) VALUES (?,?,?)", (username,new_task,c_state))
       g.db.commit()
    return redirect('/userpg')

@app.route('/deledit', methods = ['GET', 'POST'])
def deledit():
    username = session["username"]
    task = request.form['delete'] 

    g.db.cursor()   
    g.db.execute("DELETE FROM tasks WHERE username=? AND tasks=?", (username,task))
    g.db.commit()

    return redirect('/userpg')

@app.route('/modedit', methods = ['GET', 'POST'])
def modedit():
    username = session["username"]
    task = request.form['modify']
    state = "Yes" 

    g.db.cursor()   
    g.db.execute("UPDATE tasks SET state=? WHERE username=? AND tasks=?", (state, username,task))
    g.db.commit()

    return redirect('/userpg')

@app.route('/logincpl', methods=['POST'])
def logincpl():
    if request.method == 'POST':
        session['username'] = request.form['username']
        c_user = session['username']
        conn = g.db.cursor()
        conn = g.db.execute("SELECT * FROM users WHERE username=?", (c_user,))        
        user = conn.fetchall()
        if not is_empty(user):
            return redirect('userpg')    
    if is_empty(user):
        return "No Record Found. <a href='/register'>Register Here</a>"
    else:
        session['logged_in'] = True
    return home()
    #    return redirect('/userpg')
   #return ''''''

@app.route('/logout')
def logout():
   session.pop('username')
   return redirect('/')

@app.route('/userpg')
def userpg(): 
    c_user = session['username']
    temp = sqlite3.connect("userdb.db")
    temp.row_factory = sqlite3.Row 
    conn = temp.cursor()
    conn.execute("SELECT * FROM tasks WHERE username=?", (c_user,))        
    rows = conn.fetchall()  
    return render_template('edittable.html', rows = rows)

@app.route("/")
def home():
    return render_template('hometodolist.html')

@app.route("/login")
def login():
    return render_template('form.html')

@app.route("/register")
def register():
    return render_template('formreg.html')  

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True


if __name__ == "__main__":
     app.run(host = '0.0.0.0')



#sh file
#create
#login
#view
#update
#delete
#https://goo.gl/forms/vxEUs8RssyXQyLLx1

#sql
#create table
#select
#update
#delete
