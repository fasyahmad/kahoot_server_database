from flask  import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import Users

db = SQLAlchemy()
app = Flask (__name__)

POSTGRES = {
        'user': 'postgres',
        'pw': 'fasyaemad03',
        'db': 'kahoot_database',
        'host': 'localhost',
        'port': '5432'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# postgresql://username:password@localhost:5432/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

@app.route('/')
def main():
    return 'Hello World!'

@app.route('/getAllUsers', methods=["GET"])
def get_all_users():
        try:
                users = Users.query.order_by(Users.user_id).all()
                return jsonify([usr.serialize() for usr in users])
        except Exception as e:
                return (str(e))

# @app.route('/getCustomerBy/<id_>', methods=["GET"])
# def get_customer_id(id_):
#     try:
#         customer=Customer.query.filter_by(customer_id=id_).first()
#         return jsonify(customer.serialize())
#     except Exception as e:
#         return(str(e))

@app.route('/addCustomer', methods=["POST"])
def add_customer():
    username=request.args.get('username')
    password=request.args.get('password')
    email=request.args.get('email')

    try:
        customer=Customer(
            username=username,
            password=password,
            email=email
        )

        db.session.add(customer)
        db.session.commit()
        return "Customer added. customer id={}".format(customer.customer_id)

    except Exception as e:
        return(str(e))


if __name__ == '__main__':
    app.run()