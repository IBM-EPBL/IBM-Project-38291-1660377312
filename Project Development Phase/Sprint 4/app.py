from flask import Flask, render_template, request, redirect, session,url_for
import ibm_db
from flask_mail import Mail, Message

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=Certificate.crt;UID=ptj61000;PWD=mK1iGb6QWUEsiZQ7;",'','')

app = Flask(__name__)

   

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gurudharan@gmail.com'
app.config['MAIL_PASSWORD'] = '1612002'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = 'asdfgqwert'
global gemail 
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
     try:
         global gemail
         mail = request.form['mail']
         pwd = request.form['psw']
         sql = "SELECT * from employee where email = '{}'".format(mail)        
         stmt = ibm_db.exec_immediate(conn, sql)
         dict = ibm_db.fetch_assoc(stmt)         
         if (mail == dict['EMAIL'].strip() and pwd == dict['PASSWORD'].strip()):
            print("if clause")
            gemail = dict['EMAIL']
            return redirect(url_for("home"))
         else:
            return render_template("signin.html",message = "Not a valid user")
    
             
     except:            
            print ("ex")
    if request.method == 'GET':
        return render_template("signin.html")

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
      try:
        dict = {}
        name = request.form['user_name']
        email = request.form['email']
        age = request.form['age']
        pw = request.form['psw']
        sal = request.form['sal']
        sql1 = "SELECT email from employee where email = '{}'".format(email)
        stmt = ibm_db.exec_immediate(conn, sql1) 
        dict = ibm_db.fetch_assoc(stmt)
        if(dict == False):
            sql = "INSERT into employee values ('{}', '{}','{}', '{}','{}')".format(name, email, age, pw,sal)
            stmt = ibm_db.exec_immediate(conn, sql) 
            sql = "INSERT into target values ('{}', 0,0,0,0)".format(email)
            stmt = ibm_db.exec_immediate(conn, sql)
            sql = "INSERT into expenses values ('{}', 0,0,0,0)".format(email)
            stmt = ibm_db.exec_immediate(conn, sql)
            return render_template('signin.html')
        else:
            return redirect(url_for('exists'))        
     
      except:
        print ("sys.exc_info()[0]")
      
    if request.method == 'GET':
        return render_template('signup.html')

@app.route('/exists')
def exists():
    return render_template('signup.html',exists = "User already exists")


@app.route('/salarysubmit',methods=['POST'])
def salarysubmit():
    if request.method == 'POST':
        food = request.form['food']
        rent = request.form['rent']
        edu = request.form['edu']
        ent = request.form['ent']
        sql1 = "update target set food='{}',rent = '{}' , education = '{}' , entertainment = '{}' where email = '{}'".format(food,rent,edu,ent,gemail)
        stmt = ibm_db.exec_immediate(conn, sql1)
        sql = "SELECT * from target where email = '{}'".format(gemail)
        stmt = ibm_db.exec_immediate(conn, sql) 
        dict = ibm_db.fetch_assoc(stmt)
        sql1 = "SELECT * from employee where email = '{}'".format(gemail)
        stmt = ibm_db.exec_immediate(conn, sql1)
        dict1 = ibm_db.fetch_assoc(stmt)
    return render_template('salary.html',sal = dict1['SALARY'],food = dict['FOOD'],edu = dict['EDUCATION'],ent = dict['ENTERTAINMENT'],rent = dict['RENT'])

@app.route('/expensesubmit',methods=['POST'])
def expensesubmit():
    if request.method == 'POST':
        msg = ""
        food = request.form['food']
        rent = request.form['rent']
        edu = request.form['edu']
        ent = request.form['ent']
        pre = "Select * from target where email = '{}'".format(gemail)
        stmt = ibm_db.exec_immediate(conn, pre) 
        dict = ibm_db.fetch_assoc(stmt)
        if(int(food) > dict['FOOD']):
            print("if")
            msg = Message(
                'Hello',
                sender ='gurudharan@gmail.com',
                recipients = [gemail]
               )
            msg.body = 'Exceeds the limit in food category'
            mail.send(msg)
        if(int(rent) > dict['RENT']):
            print("if")
            msg = Message(
                'Hello',
                sender ='gurudharan@gmail.com',
                recipients = [gemail]
               )
            msg.body = 'Exceeds the limit in rent category'
            mail.send(msg)
        if(int(edu) > dict['EDUCATION']):
            print("if")
            msg = Message(
                'Hello',
                sender ='gurudharan@gmail.com',
                recipients = [gemail]
               )
            msg.body = 'Exceeds the limit in education category'
            mail.send(msg)
        if(int(ent) > dict['ENTERTAINMENT']):
            print("if")
            msg = Message(
                'Hello',
                sender ='gurudharan@gmail.com',
                recipients = [gemail]
               )
            msg.body = 'Exceeds the limit in entertainment category'
            mail.send(msg)
        sql1 = "update expenses set food='{}',rent = '{}' , education = '{}' , entertainment = '{}' where email = '{}'".format(food,rent,edu,ent,gemail)
        stmt = ibm_db.exec_immediate(conn, sql1)
        sql = "SELECT * from expenses where email = '{}'".format(gemail)
        stmt = ibm_db.exec_immediate(conn, sql) 
        dict = ibm_db.fetch_assoc(stmt)
        sql1 = "SELECT * from employee where email = '{}'".format(gemail)
        stmt = ibm_db.exec_immediate(conn, sql1)
        dict1 = ibm_db.fetch_assoc(stmt)
    return render_template('expenses.html',sal = dict1['SALARY'],food = dict['FOOD'],edu = dict['EDUCATION'],ent = dict['ENTERTAINMENT'],rent = dict['RENT'])
@app.route('/home')
def home():
    sql = "select * from employee where email = '{}'".format(gemail)
    stmt = ibm_db.exec_immediate(conn,sql)
    dict = ibm_db.fetch_assoc(stmt)
    return render_template('home.html',name = dict['NAME'],email = dict['EMAIL'],age = dict['AGE'],sal = dict['SALARY'])

@app.route('/addsalary')
def salary():
    global gemail
    sql1 = "SELECT * from employee where email = '{}'".format(gemail)
    sql2 = "SELECT * from target where email = '{}'".format(gemail)
    print(gemail,"gmail")
    stmt = ibm_db.exec_immediate(conn, sql1)    
    stmt1 = ibm_db.exec_immediate(conn, sql2) 
    dict1 = ibm_db.fetch_assoc(stmt)
    dict = ibm_db.fetch_assoc(stmt1)    
    return render_template('salary.html',sal = dict1['SALARY'],food = dict['FOOD'],edu = dict['EDUCATION'],ent = dict['ENTERTAINMENT'],rent = dict['RENT'])

@app.route('/addexpenses')
def expenses():
    global gemail
    sql1 = "SELECT * from employee where email = '{}'".format(gemail)
    sql2 = "SELECT * from expenses where email = '{}'".format(gemail)
    
    print(gemail,"gmail")
    stmt = ibm_db.exec_immediate(conn, sql1)    
    stmt1 = ibm_db.exec_immediate(conn, sql2) 
    
    dict1 = ibm_db.fetch_assoc(stmt)
    dict = ibm_db.fetch_assoc(stmt1)
    
    print("dict1",dict1)
    print("dict",dict)
    return render_template('expenses.html',sal = dict1['SALARY'],food = dict['FOOD'],edu = dict['EDUCATION'],ent = dict['ENTERTAINMENT'],rent = dict['RENT'])

@app.route('/visualization')
def vis():
    sql2 = "SELECT * from expenses where email = '{}'".format(gemail)
    stmt1 = ibm_db.exec_immediate(conn, sql2)
    dict = ibm_db.fetch_assoc(stmt1)
    sql3 = "SELECT * from target where email = '{}'".format(gemail)
    stmt2 = ibm_db.exec_immediate(conn,sql3)
    dict2 = ibm_db.fetch_assoc(stmt2)
    return render_template('vis.html',food = int(dict['FOOD']),edu = int(dict['EDUCATION']),ent = int(dict['ENTERTAINMENT']),rent = int(dict['RENT']),food1 = dict2['FOOD'],edu1 = dict2['EDUCATION'],ent1 = dict2['ENTERTAINMENT'],rent1 = dict2['RENT'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)