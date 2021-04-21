from datetime import datetime
from stroll import app, db, login_manager #used to be from stroll
from flask_login import UserMixin
from sqlalchemy.inspection import inspect

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    water = db.Column(db.Boolean)
    green_spaces = db.Column(db.Boolean)
    traffic = db.Column(db.Boolean)
    buildings = db.Column(db.Boolean)
    pace = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    
class Journey(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_point_long = db.Column(db.Float, nullable=False)
    start_point_lat = db.Column(db.Float, nullable=False)
    end_point_long = db.Column(db.Float, nullable=False)
    end_point_lat = db.Column(db.Float, nullable=False)
    waypoints = db.Column(db.String, nullable=False) #JSON format of a list of coordinates
    is_private = db.Column(db.Boolean, nullable=False)
    polyline = db.Column(db.String)

    def __repr__(self):
        return f"Journey('{self.polyline}', '{self.date_posted}', '{self.is_private}')"

    def serialize(self):
        d = Serializer.serialize(self)
        del d['date_posted']
        return d    

    


class Attractions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attr_coordinates = db.Column(db.String(100), nullable=False)
    attractionName = db.Column(db.String(100), nullable=False)
    attractionDescriptor = db.Column(db.String(100), nullable=False)
    water = db.Column(db.Boolean, nullable=False)
    green_spaces = db.Column(db.Boolean, nullable=False)
    traffic = db.Column(db.Boolean, nullable=False)
    buildings = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Attraction('{self.attractionName}', '{self.attractionDescriptor}', ('{self.latitude}','{self.longitude}')"

