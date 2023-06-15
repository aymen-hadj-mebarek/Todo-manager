import os
from datetime import datetime
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
        param = session.get('email')
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
    if session:
        param = session.get('email')
    else:
        param = None 
    return render_template('tasks.html',param=param)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route("/delete")
def delete():
    return redirect(url_for('home'))

@app.route("/database/<email>")
def database(email):
    use = db.session.query(user).filter(user.email == email).first()
    print((use.password))
    return( "test" )

def password_ceck(mdps):
    if len(mdps) > 7:
        return True


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
