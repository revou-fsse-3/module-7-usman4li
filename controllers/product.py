from flask import Blueprint, render_template, request, jsonify
from connectors.mysql_connector import Session
from models.product import Product
from sqlalchemy import select

from flask_login import current_user, login_required
from decorators.role_checker import role_required

from validations.product_schema import product_schema
from cerberus import Validator

product_routes = Blueprint('product_routes', __name__)

@product_routes.route("/product", methods=['GET'])
# @login_required
def product_home():
    response_data = dict()

    session = Session()

    try:
        product_query = select(Product)

        # tambahkan filter apabila ada search query
        if request.args.get('query') is not None:
            search_query = request.args.get('query')
            product_query = product_query.where(Product.name.like(f'%{ search_query }%'))

        products = session.execute(product_query)
        products = products.scalars()
        response_data['products'] = products

    except Exception as e:
        print(e)
        return "Error"
    
    # response_data['name'] = current_user.name
    
    # print(response_data['name'])
    return render_template("products/product_home.html", response_data = response_data)
@product_routes.route("/product/<id>", methods=['GET'])
def product_detail(id):
    response_data = dict()

    session = Session()

    try:
        product = session.query(Product).filter((Product.id==id)).first()
        if (product == None):
            return "Data not found"
        response_data['product'] = product
    except Exception as e:
        print(e)
        return "Error Processing Data"
    
    return render_template("product/product_detail.html", response_data = response_data)

@product_routes.route("/product", methods=['POST'])
@role_required('Admin')
def product_insert():

    v = Validator(product_schema)
    json_data = request.get_json()
    if not v.validate(json_data):
        # validasi gagal
        return jsonify( {"error": v.errors} ), 400

    new_product = Product(
        name=json_data['name'],
        price=json_data['price'],
        description=json_data['description']
    )
    session = Session()
    session.begin()
    try:
        session.add(new_product)
        session.commit()
    except Exception as e:
        # Operation Gagal
        session.rollback()
        print(e)
        return { "message": "Insert Data Gagal"}
    
    # Operation Sukses
    return { "message": "Insert Data Sukses"}

@product_routes.route("/product/<int:id>", methods=['DELETE'])
@login_required
def product_delete(id):
    allowed_user_name = role_required('Admin')

    if current_user.name != allowed_user_name:
        return {"message": "Permission denied. You do not have the necessary privileges"}, 403
    
    session = Session()
    session.begin()
    try:
        product = session.query(Product).filter(Product.id==id).first()
        if product:
            session.delete(product)
            session.commit()
            return {"message": "Delete Data Sukses"}
        else:
            return {"message": "Produk tidak ditemukan"}
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": "Delete Data Gagal" }
    
    # Operation Sukses
    finally:
        session.close()

@product_routes.route("/product/<int:id>", methods=['PUT'])
@role_required('Admin')
def product_update(id):
    session = Session()
    session.begin()

    try:
        product_update = session.query(Product).filter(Product.id==id).first()
        product_update.name = request.form['name']
        product_update.price = request.form['price']
        product_update.description = request.form['description']

        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        return { "message": "Update Data Gagal" }
    
    # Operation Sukses
    return { "message": "Update Data Sukse" }
