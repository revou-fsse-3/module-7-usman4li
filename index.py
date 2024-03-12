from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from sqlalchemy import select, text
from connectors.mysql_connector import engine
from models.product import Product
from models.user import User
from sqlalchemy.orm import sessionmaker
from controllers.product import product_routes
from controllers.user import user_routes
from flask_login import LoginManager
import os

load_dotenv()

app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(product_routes)
app.register_blueprint(user_routes)

# Product Route
@app.route("/")
def hello_world():
    # # Insert using SQL
    # session = sessionmaker(connection)
    # with session() as s:
    #     s.execute(text("INSERT INTO product (name, price, description, created_at) VALUES ('Wallet', 15000, 'Create from cow skin','2024-02-01 00:00:00')"))
    #     s.commit()

    # # ORM WAY
    # NewProduct = Product(name='Snake Wallet', price=3000, description='Created from Snake Skin', created_at='2024-02-01 00:00:00')
    # Session = sessionmaker(connection)
    # with Session() as s:
    #     s.add(NewProduct)
    #     s.commit()
    # return "Hello World"
    product_querry = select(Product)
    Session = sessionmaker(engine)
    with Session() as session:
        result = session.execute(product_querry)
        for row in result.scalars():
            print(f'ID: {row.id}, Name: {row.name}')
    return redirect(url_for('user_routes.do_user_login'))
