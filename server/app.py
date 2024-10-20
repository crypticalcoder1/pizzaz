from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, RestaurantPizza, Pizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route('/')
def index():
    return '<h1>Code Challenge</h1>'

# Define your resources
class RestaurantResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        if not restaurants:
            return jsonify({"message": "No restaurants found"}), 404
        return jsonify([restaurant.to_dict() for restaurant in restaurants])

    def post(self):
        data = request.get_json()
        new_restaurant = Restaurant(name=data['name'], address=data['address'])
        db.session.add(new_restaurant)
        db.session.commit()
        return jsonify(new_restaurant.to_dict()), 201

class PizzaResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        if not pizzas:
            return jsonify({"message": "No pizzas found"}), 404
        return jsonify([pizza.to_dict() for pizza in pizzas])

    def post(self):
        data = request.get_json()
        new_pizza = Pizza(name=data['name'], ingredients=data['ingredients'])
        db.session.add(new_pizza)
        db.session.commit()
        return jsonify(new_pizza.to_dict()), 201

# Adding resources to the API
api.add_resource(RestaurantResource, '/restaurants')
api.add_resource(PizzaResource, '/pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
