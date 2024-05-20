"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Favorite_Characters, Favorite_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


current_logged_user_id = 1

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()

    user_list = [element.serialize() for element in users]

    return jsonify(user_list), 200

@app.route('/planet', methods=['GET'])
def get_planets():
    allPlanets = Planets.query.all()
    result = [element.serialize() for element in allPlanets]
    return jsonify(result), 200

@app.route('/planet-galaxy', methods=['GET'])
def get_relation_planet_galaxy():
    planets = Planets.query.all()
    response = []
    for planet in planets:
        response.append({
            'planet': planet.name,
            'galaxy_id': planet.galaxy_id,
            'galaxy_name': planet.galaxy.name
        })
    return jsonify(response)

@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user_id = request.json.get("user_id")

    favorite_planets = Favorite_Planets.query.filter_by(id=user_id)
    favorite_planets = list(map(lambda planet: planet.serialize(), favorite_planets))

    favorite_characters = Favorite_Characters.query.filter_by(id=user_id)
    favorite_characters = list(map(lambda character: character.serialize(), favorite_characters))

    return jsonify({
        "planets": favorite_planets,
        "characters": favorite_characters
    }),200

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_character(people_id):

    favorite_character = Favorite_Characters()
    favorite_character.user_id = request.json.get("user_id")
    favorite_character.character_id_id = people_id

    db.session.add(favorite_character)
    db.session.commit()

    return jsonify({
      "msg": "Character added to favorites",
      "status": "ok"}
    ), 201


@app.route('/planet', methods=['POST'])
def get_all_planets():
    planets = Planets.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))

    return jsonify({"planets": planets}), 200

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    planet_to_delete = Favorite_Planets.query.filter(Favorite_Planets.user_id == request.json.get("user_id"), Favorite_Planets.planet_id == planet_id).first()
    db.session.delete(planet_to_delete)
    db.session.commit()

    return f"Planet deleted from favorites", 201

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_character(people_id):
    character_to_delete = Favorite_Planets.query.filter(Favorite_Planets.user_id == request.json.get("user_id"), Favorite_Planets.character_id == people_id).first()
    db.session.delete(character_to_delete)
    db.session.commit()
    
    return f"Character deleted from favorites", 201




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
