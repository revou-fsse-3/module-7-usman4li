from flask import Blueprint, redirect, render_template, request
from connectors.mysql_connector import engine

from models.user import User
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, logout_user
user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/register", methods=['GET'])
def user_register():
    return render_template("users/register.html")

@user_routes.route("/register", methods=['POST'])
def do_register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    NewUser = User(name=name, email=email)
    NewUser.set_password(password)

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    session.begin()
    try:
        session.add(NewUser)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error during registration: {e}")
        return { "message": "Gagal Register" }

    return { "message": "Sukses Register" }

@user_routes.route("/login", methods=['GET'])
def user_login():
    return render_template("users/login.html")

@user_routes.route("/login", methods=['POST'])
def do_user_login():
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        users = session.query(User).filter(User.email==request.form['email']).first()

        if users == None:
            return {"message": "Email tidak terdaftar"}
        
        #Check Password
        if not users.check_password(request.form['password']):
            return {"message" : "password Salah"}

        login_user(users, remember=False)
        return redirect('/product')
    
    except Exception as e:
        return { "message": "Login Failed"}
    


@user_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    return (redirect('/login'))