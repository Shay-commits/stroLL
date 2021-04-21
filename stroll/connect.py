import sqlite3
import json

DB = 'stroll/site.db'


def get_all_users_json(json_str=True):
    conn = sqlite3.connect(DB)
    # This enables column access by name: row['column_name']
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute('''
    SELECT id, username, water, green_spaces, buildings, traffic from user;
    ''').fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps([dict(ix) for ix in rows])  # CREATE JSON

    return rows


def get_user_json(username, json_str=True):
    conn = sqlite3.connect(DB)
    # This enables column access by name: row['column_name']
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute('''
    SELECT id, username, email, water, green_spaces, buildings, traffic from user WHERE id = ?;
    ''', (username,)).fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps([dict(ix) for ix in rows])  # CREATE JSON

    return rows


def get_all_user_journeys_json(user_id, json_str=True):
    conn = sqlite3.connect(DB)
    # This enables column access by name: row['column_name']
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute('''
    SELECT id, date_posted, user_id, start_point_long, start_point_lat, end_point_long, end_point_lat, waypoints, polyline FROM journey WHERE user_id = ?;
    ''', (user_id,)).fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps([dict(ix) for ix in rows])  # CREATE JSON

    return rows

def get_private_user_journeys_json(user_id, json_str=True):
    conn = sqlite(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute('''
    SELECT id, date_posted, user_id, start_point_long, start_point_lat, end_point_long, end_point_lat, length_distance FROM journey WHERE user_id = ? AND is_private = '1';
    ''')

def get_one_user_journey_json(user_id, id, json_str=True):
    conn = sqlite3.connect(db)
    # This enables column access by name: row['column_name']
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute('''
    SELECT id, date_posted, user_id, start_point_long, start_point_lat, end_point_long, end_point_lat, length_distance FROM journey WHERE user_id = ? AND id = ?;
    ''', (user_id, id,)).fetchall()

    conn.commit()
    conn.close()

    if json_str:
        return json.dumps([dict(ix) for ix in rows])  # CREATE JSON

    return rows


def update_journey(start_point_lat, start_point_long, end_point_lat, end_point_long, waypoints, journey_id, json_str=True):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    rows = cur.execute('''
    UPDATE journey SET start_point_lat = ?, start_point_long = ?, end_point_lat = ?, end_point_long = ?, waypoints = ? WHERE id = ?
    ''', (journey_id))
    if json_str:
        return json.dumps([dict(ix) for ix in rows])  # CREATE JSON

    return rows

# print(get_user_json('1', json_str=True))

# # create an SQL connection to the SQLite database
# con = sqlite3.connect("site.db")

# # # printing everything from user
# # for row in cur.execute('SELECT * FROM user;'):
# #     print(row)

# # # storing an email in a variable
# # cur.execute('SELECT email FROM user WHERE id="1"')
# # email1 = cur.fetchall()
# # print(email1)

# # # returning all attractions where water = true
# # cur.execute('SELECT attr_lat, attr_long FROM attractions WHERE water="true"')
# # water_attractions = cur.fetchall()
# # print(water_attractions)

# # put data into database


# def create_attraction(con, attr_lat, attr_long, attractionName, attractionDescriptor, water, green_spaces, traffic, buildings):
#     sql = """
#         INSERT INTO customers (attr_lat, attr_long, attractionName, attractionDescriptor, water, green_spaces, traffic, buildings)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
#     cur = con.cursor()
#     cur.execute(sql, (attr_lat, attr_long, attractionName,
#                 attractionDescriptor, water, green_spaces, traffic, buildings))
#     return cur.lastrowid

# # get data from database


# # user1 = get_users(con, '1')
# # print(user1)

# def get_journeys(con, id):
#     cur.execute("""
#     SELECT email, username FROM journey WHERE id = ?
#     """, (id))
#     return(cur.fetchall())


def get_attractions(water, green_space, traffic, buildings, json_str=True):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT attr_coordinates, attractionName FROM attractions WHERE water = ? OR green_spaces = ? OR traffic = ? OR buildings = ?
        """, (water, green_space, traffic, buildings))
    coordinates = cur.fetchall()
    #print(str(coordinates))
    if json_str == True:
        coordinates = json.dumps([list(ix) for ix in coordinates])  # CREATE JSON

    coordinates = json.loads(str(coordinates))
    #print(str(coordinates))
    

    for count, coord_pair in enumerate(coordinates):
        innerString = coord_pair[0] #'3453598.5,5348953489.5'
        #print(innerString, 'BEFORE')

        example = coord_pair[1]
        #print(str(example))
        innerString = innerString.split(",") #['3453598.5', '5348953489.5']
        #print(innerString, 'AFTER')
        coord_pair = [float(innerString[0]), float(innerString[1]), example]
        #print(str(coord_pair))
        #print(coord_pair, 'AFTER AFTER')
        coordinates[count] = coord_pair



    #for coord_pair in coordinates:
        #coord_pair = json.loads("[" + coord_pair + "]") #this might error if you do json.loads("23424.4, 34905390.4") instead of json.loads("[23424.4, 34905390.4]")
        #print(coord_pair)
        #coord_pair = coord_pair.split(",")
        #print(coord_pair)
        #coord_pair = list(map(float, coord_pair))
   # print(str(coordinates))
    return coordinates

    # got in column : 123.456,123.456
    # need for func: [123.456, 123.456] 


# def get_users_to_json():
#     cur.execute("""
#     SELECT id, username, email, water, green_spaces, buildings, traffic FROM user FOR JSON PATH
#     """)
#     return (cur.fetchall)


# usersJson = get_users_to_json()
# print(usersJson)

# # close connection
# con.close()
