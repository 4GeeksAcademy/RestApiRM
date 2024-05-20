from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Galaxy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    coordinate_center_x = db.Column(db.Float, nullable=False) 
    coordinate_center_y = db.Column(db.Float, nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    favorites = db.relationship('Favorite')
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
class Characters(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    birth_year = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    mass = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color
        }
    

class Favorite_Characters(db.Model):
    __tablename__ = "favorite_characters"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.String(250), db.ForeignKey("characters.id"))

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
        
class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(240))
    population = db.Column(db.Integer, default=0)
    galaxy_id = db.Column(db.Integer, db.ForeignKey('galaxy.id'), nullable=False)
    galaxy = db.relationship('Galaxy')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "population": self.population,
        }
class Favorite_Planets(db.Model):
    __tablename__ = "favorite_planets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.String(250), db.ForeignKey("planets.id"))

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }
