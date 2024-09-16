from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from .modles import User
from werkzeug.security import generate_password_hash,check_password_hash
from .modles import db 
from flask_login import login_required,login_user,logout_user,current_user
from .init import socketio
auth=Blueprint('auth',__name__)
default_room="General Room"
@auth.route("/login",methods=['GET','POST'])
def login():
    
    if request.method=='POST':
        email=request.form.get("email")
        password=request.form.get('password')
     
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password): 
                flash('Logged in Successfully!',category='success')
                login_user(user,remember=True)
                print(f"{user.first_name}  email-{user.email} has logged in")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password',category='error')
        else:
            flash("email dosen't exist",category='error')
        session['name']=user.first_name
        session['room']=default_room
    return render_template('login.html',user=current_user)  
      
    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    print(f"has logged out")
    return redirect(url_for('auth.login'))


@auth.route("/sign-up",methods=['GET','POST'])
def signup():
    from flaskapi.modles import db
    session.clear()
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstname")
        password1 = request.form.get("password")
        password2 = request.form.get("password2")

        user=User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist',category="error") 
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category="error")
        elif len(first_name) < 2:
            flash('First Name must be greater than 2 characters', category="error")
        elif password1 != password2:
            flash('Passwords must match', category="error")
        elif len(password1) < 3:
            flash('Password must be greater than 7 characters', category="error")
        else:
            new_user=User(email=email,first_name=first_name,password=generate_password_hash(password1,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash('Account created successfully!', category='success') 
            print(f"{first_name}  email-{email} has logged in")
            return redirect(url_for('view.home'))

    return render_template("signup.html", user=current_user)

