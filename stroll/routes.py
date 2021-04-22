import os
import secrets
import sqlite3
import json
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from flask_cors import CORS
from stroll import app, db, bcrypt
from stroll.models import User, Journey
from flask_login import login_user, current_user, logout_user, login_required
from stroll.connect import get_all_users_json, get_user_json, get_all_user_journeys_json, get_one_user_journey_json, update_journey, get_attractions
from stroll.journeys import RadialJourney, SimpleJourney, getPolyline


# /users    GET: Shows list of users, POST: Add new user
# /users/user_id  GET: Just that user, PUT: Update user, DELETE
# /users/user_id/journeys   GET: List of journeys, POST: Create new journey
# /users/user_id/journeys/journey_id   PUT: Update journey, DELETE: Delete journey
# /login  POST
# /logout POST nothing
#! If have time: /users/username/.../?client_id=stuff&client_secret=stuff    for OAuth authentication
#! If have time: /users/username/attractions + /users/username/attractions/?attraction_id=stuff, otherwise just put in our own attractions
# https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/

CORS(app)
@app.route("/", methods=['GET'])
def home():
    print("Person accessed website")
    return "<h1>Welcome to stroLL</h1>"


@app.route('/check_login_status')
def check_login_status():
    print(current_user)
    return str(current_user.is_authenticated)


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        content = get_all_users_json(json_str=True)
        return content
    elif request.method == "POST" and request.is_json:  # register new user
        content = request.get_json()
        hashed_password = bcrypt.generate_password_hash(
            content['password']).decode('utf-8')
        user = User(username=content['username'],
                    email=content['email'],
                    password=hashed_password,
                    water=content['water'] or 1,
                    green_spaces=content['green_spaces'] or 1,
                    buildings=content['buildings'] or 1,
                    pace=content['pace'] or 7
                    )
        db.session.add(user)
        db.session.commit()
        userCredentials = user.serialize()
        
        return userCredentials


@app.route("/login", methods=['POST'])
def login():
    content = request.get_json()
    user = User.query.filter_by(username=content['username']).first()
    if not user or not bcrypt.check_password_hash(user.password, content['password']):
        return abort(403)

    print(user)
    print(login_user(user))   
    login_user(user)
    userCredentials = user.serialize()
    return userCredentials


@app.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return redirect('/')


@app.route("/users/<user_id>", methods=['GET'])
def userRequest(user_id):
    if request.method == 'GET':
        # show some stuff but don't show sensitive information like passwords
        content = get_user_json(user_id, json_str=True)
        return content


@app.route("/users/<user_id>/journeys", methods=['GET', 'POST'])
def journeys(user_id):
    if request.method == 'GET':
        # TODO: if user has access, show all journeys, if not, show only is_private = false journeys

        content = get_all_user_journeys_json(user_id, json_str=True)
        return content

    elif request.method == 'POST' and request.is_json:  # need to make error proof if malformed input passed
        content = request.get_json()
        # does user have access? if not 400 access denied
        """Expecting JSON in format:
        {
            journey_type: "Simple" or "Radial"
            origin: "[latitude (float), longitude (float)]"
            destination: "[latitude (float), longitude (float)]"
            [optional] waypoints: "[ [latitude (float), longitude (float)], [latitude (float), longitude (float)], ... ]"
            [optional] visit_nearby_attractions: "True" or "False"
            [optional, default 10] radius: kilometers (float)
        }
        """

        journey_type = content['journey_type']
        origin, destination = json.loads(content['origin']), json.loads(content['destination'])
        start_point_lat, start_point_long = origin[0], origin[1]
        end_point_lat, end_point_long = destination[0], destination[1]
        waypoints = json.loads(content['waypoints']) or []
        gmapsOutput = None
        if journey_type == "Simple":
            journey = SimpleJourney(origin, destination, waypoints)
            gmapsOutput = journey.getGmapsDirections()
        elif journey_type == "Radial":
            radius = content['radius'] or 10
            journey = RadialJourney(origin, destination, radius, 5, waypoints)
            gmapsOutput = journey.getGmapsDirections()
        else:
            return abort(404, "Unknown journey type")

        if len(gmapsOutput) == 0:
            return abort(404, "Coordinates are in ocean or don't work with googlemaps")

        user = User.query.filter_by(id = user_id).first()

        if content['visit_nearby_attractions'] == "True":
            attractionsList = get_attractions(user.water, user.green_spaces, user.traffic, user.buildings, json_str=True) #1 or 0 values as input
            #for dictionary in attractionsList:

            #print(attractionsList, 'egreeeeeeeeeeeeeeeeeeeeeeeghuegurhguehgiuehgieushgsui')
            journey.makeVisitAttractions(attractionsList)
            print(str(journey.makeVisitAttractions(attractionsList)))
            gmapsOutput = journey.getGmapsDirections()

        waypoints = journey.waypoints

        newJourney = Journey(
            user_id=user_id,
            start_point_long=start_point_long,
            start_point_lat=start_point_lat,
            end_point_long=end_point_long,
            end_point_lat=end_point_lat,
            waypoints=str(jsonify(waypoints)),
            is_private=False,
            polyline=getPolyline(gmapsOutput)
        )
        db.session.add(newJourney)
        db.session.commit()

        temp = newJourney.serialize()
        print(temp)
        temp["attractions"] = attractionsList
        print(temp)
        
        #return json.dumps(newJourney.serialize()) + 'This is the attraction list: ' + str(attractionsList)
        return json.dumps(temp)


@app.route("/users/<user_id>/journeys/<journey_id>", methods=['PUT'])
def journeyRequest(user_id, journey_id):
    if request.method == 'PUT' and request.is_json:
        content = request.get_json()
        start_point_lat, start_point_long = content['origin'][
            'start_point_lat'], content['origin']['start_point_long']
        end_point_lat, end_point_long = content['destination'][
            'end_point_lat'], content['destination']['end_point_long']
        page_content = update_journey(start_point_lat, start_point_long, end_point_lat,
                                      end_point_long, content['waypoints'], content['journey_id'], json_str=True)
        # TODO: also update the polyline string, dont update journey_id, careful with waypoints as should be optional
        return page_content
