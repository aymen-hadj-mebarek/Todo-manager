import os
from datetime import datetime,date
from flask import Flask, redirect, render_template, session, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "aymen"

# creating or importing the databases
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase.db'    # this is a relative path to the database

# linking the databases to the server
db = SQLAlchemy(app)

class task(db.Model):
    """the database of the tasks

    Args:
        db (database): holds the structure of the database

    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100),nullable=False)
    date_created = db.Column(db.Date,default=datetime.utcnow)
    date_due = db.Column(db.Date)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer)
    
    def __repr__(self):
        return "<task %r>" % self.id

class user(db.Model):
    """the data base of users

    Args:
        db (database): this will hold the structure of the database
_description_
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    
    def __repr__(self):
        return "<user %r>" % self.id
    
    
@app.route('/')
def index():
    """the default index of the website that we are goind to have will be "/"   

    Returns:
        _type_: a redirect to the home page
    """
    return redirect("home")

@app.route('/home')
def home(param=None):
    if session:
        email = session.get('email')
        param = db.session.query(user).filter(user.email==email).first().name
    else:
        param = None 
    return render_template('Home.html',param=param)

@app.route('/SignUp', methods=['POST','GET'])
def signup():
    """the signup method that is used to sign up a newuser

    Returns:
        depends on the signing up prcess it can return : the home page, the signup page, error while signing up
    """
    if not session.get("email"):
        if request.method=='POST':
            if request.form['mdps'] == request.form['mdps_check']:
                # sign up process begin and we save the infos of the used in the database 
                user_name = request.form['name']
                user_email = request.form['emailad']
                user_password = request.form['mdps']
                
                new_user = user(name=user_name, email=user_email, password=user_password)
                try:
                    if not (db.session.query(user).filter(user.email == user_email).first()) :
                        if(password_ceck(user_password)):    
                            db.session.add(new_user)
                            db.session.commit()
                            session["email"] = user_email
                            flash("Account created successfully",category="info")
                            return redirect(url_for("home"))
                        else:
                            flash("password must contain at least 8 caracteres",category="error")
                            return redirect(url_for("signup"))
                    else:
                        flash("account already existed",category="error")
                        return redirect(url_for("signup"))
                except:
                    return "error adding user"   
            else:
                flash("Password doesnt match with the confirmation password",category="error")
                return render_template('Signup.html')
        else:
            # if there is no information posted then there is no signup process
            return render_template('Signup.html')
    else:
        flash("You can't Sign Up when you are already Logged in",category="error")
        return redirect(url_for("home"))

@app.route('/login', methods=['POST','GET'])
def login():
    """Login function that verifies if the user have an account or not in the database

    Returns:
        url_for: depends if the user could log in or not it will redirect it to the login page or the signup page, or the home page
    """
    if not session.get("email"):
        if request.method == 'POST':
            user_email = request.form.get("emailad")
            user_password = request.form.get("mdps")
            if (not db.session.query(user).filter(user.email == user_email).first()):
                flash("You don't have an existing element, you have to sign up",category="error")
                print("You don't have an existing element, you have to sign up")
                return redirect(url_for("signup"))
            elif (db.session.query(user).filter(user.email == user_email).first()).password != user_password:
                flash("Password wrong try again",category="error")
                print("Password wrong try again")
                return redirect(url_for("login"))
            else:
                flash("You Logged in successfully",category="info")
                print("You Logged in successfully")
                session["email"] = user_email
                return redirect(url_for("home"))
        else:
            return render_template('Login.html')
    else:
        flash("You can't Log in when you are already Logged in",category="error")
        return redirect(url_for("home"))
    
@app.route('/tasks', methods=['POST','GET'])
def tasks():
    if session.get('email'):
        session['id'] = db.session.query(user).filter(user.email == session.get("email")).first().id
        tasks = task.query.filter(task.user_id == session['id'])
        today_date = datetime.today().date()
        if request.method == 'POST':
            task_content = request.form['task_added']
            task_due = (request.form['task_date'])
            task_due = datetime.strptime(task_due, "%Y-%m-%d")
            new_task = task(content=task_content, date_due=task_due,user_id=session["id"])
            try:
                print("creating task")
                print(type(task_due))
                db.session.add(new_task)
                db.session.commit()
                return redirect(url_for("tasks"))
            except:
                return "error creating task"
        else:
            # tasks = task.query.filter(task.user_id == session['id'])
            return render_template("tasks.html",param=session.get('email'),tasks=tasks,today=today_date)
    else:
        flash("You need to log in to access to your tasks",category="error")
        return redirect(url_for("home"))
    # return render_template('tasks.html',param=param)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/delete/<id>")
def delete(id):
    task_to_delete = task.query.get_or_404(id)
    if task_to_delete :
        db.session.delete(task_to_delete)
        db.session.commit()
        
    return redirect(url_for('tasks'))

@app.route("/update/<id>")
def update(id):
    task_to_update = task.query.get_or_404(id)
    if task_to_update:
        if task_to_update.done == False:
            task_to_update.done = True
        else:
            task_to_update.done = False
            
        db.session.commit()
        return redirect(url_for("tasks"))
    else:
        return "error updating the task"


@app.route("/database/<email>")
def database(email):
    use = db.session.query(user).filter(user.email == email).first()
    print((use.password))
    return( "test" )

def password_ceck(mdps):
    if len(mdps) > 7:
        return True
    else:
        return False

def date_comp(date1, date2):
    date1 = date1.split('-')
    date2 = date2.split('-')
    if int(date1[0]) == int(date2[0]):
        if int(date1[1]) == int(date2[1]):
            if int(date1[2]) == int(date2[2]):
                return 0
            elif int(date1[2]) > int(date2[2]):
                return 1
            else:
                return -1
        elif int(date1[1]) > int(date2[1]):
            return 1
        else:
            return -1
    elif int(date1[0]) > int(date2[0]):
        return 1
    else:
        return -1

if __name__ == '__main__':
    """
    this will just create the database *
    """
    if not os.path.exists("instance\DataBase.db"):
        with app.app_context():
            db.create_all()
            print("created database")
    
    # then we will start running the server
    app.run(debug=True)
