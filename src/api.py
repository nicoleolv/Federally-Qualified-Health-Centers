from flask import Flask, jsonify,request
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import geopandas as gpd
from geopy.exc import GeocoderUnavailable
import folium
from folium.plugins import HeatMap
import threading
import os
from redis import Redis
from hotqueue import HotQueue
import requests
import json
import time
import uuid
from jobs import add_job,  get_job_by_id
import pandas as pd
# Get the Redis service hostname from the environment
#from worker import do_work
redis_host = os.environ.get('REDIS_HOST', 'redis')

# # Define the Redis connection
rd = Redis(host=redis_host, port=6379, db=0)
q = HotQueue('queue', host=redis_host, port=6379, db=1)
rd2 = Redis(host=redis_host, port=6379, db=2)
app = Flask(__name__)

# Define the path to the CSV file
# csv_file_path = './data/SITE_HCC_FCT_DET.csv'

def fetch_data():
    """
     Fetches health center data from an external source (CSV file).

     Returns:
         list: Health center data in list of dictionaries format.
     """
    df = (pd.read_csv('https://query.data.world/s/3zhr263bmtw3sdxb7wakvqo3j5ih2i?dws=00000'))
    data = df.to_dict('records')
    return data

#def get_help():
@app.route('/help', methods=['GET'])
def help():
    help_text = {
        "/data (POST, GET, DELETE)": "Manages health center data. Use POST to load data, GET to retrieve data, DELETE to clear all data.",
        "/healthcenter/<site_telephone_number> (GET)": "Retrieves health center information by site telephone number.",
        "/sites/<site_name> (GET)": "Retrieves important information about a health center by site name.",
        "/state/<state_name> (GET)": "Retrieves health centers in a specific state by state name.",
        "/location/<state>/<city> (GET)": "Retrieves health centers in a specific location by state and city.",
        "/program/<sitename> (GET)": "Retrieves program information for a health center by site name.",
        "/results/<jobid> (GET)": "Retrieves the results of a job by job ID. Use with 'heatmap' or 'nearesthealthcenter' job IDs.",
        # Add more routes here if needed
    }

    return jsonify(help_text)
@app.route('/data', methods=['POST', 'GET', 'DELETE'])
def data():
    """
       Manages health center data.

       POST:
           Returns health center data.
       GET:
           Retrieves health center data.
       DELETE:
           Clears all health center data.

       Returns:
           str: Response message.
    """
    data = fetch_data()
    if request.method == 'POST':
        return jsonify(data)

    if request.method == 'GET':
        return jsonify(data)

    if request.method == 'DELETE':
        data.clear()
        return 'Data cleared\n'

@app.route('/healthcenter/<site_telephone_number>', methods=['GET'])
def getallhealthcenter(site_telephone_number):
    clinicinfo=[]
    data = fetch_data()
    for x in data:
        if 'Site Telephone Number' in x:
            if x['Site Telephone Number'] == site_telephone_number:
                clinicinfo.append(x)

    return jsonify(clinicinfo)
@app.route('/sites/<site_name>', methods = ['GET'])
def get_important(site_name):
    clinicinfo =[]
    data = fetch_data()
    for x in data:
        if 'Site Name' in x:
            if x['Site Name'] == site_name:
                clinicinfo.append({
                    'Site Name': x['Site Name'],
                    'Site Telephone Number': x['Site Telephone Number'],
                    'Site Address': x['Site Address'],
                    'Operating Hours per Week': x['Operating Hours per Week'],
                    'Site City': x['Site City'],
                    'Site State Abbreviation': x['Site State Abbreviation']
                })
    return jsonify(clinicinfo)
@app.route('/state/<state_name>', methods = ['GET'])
def get_state(state_name):
    clinicinfo = []
    data = fetch_data()

    print(f"Fetching data for state: {state_name}")  # Print the state
    for x in data:
        print(x['State Name'])  # Print the state abbreviation of each item
        if 'State Name' in x:
            if x['State Name'].lower().strip() == state_name.lower().strip():
                clinicinfo.append({'Site Name': x['Site Name']})

    print(f"Found {len(clinicinfo)} matching items")  # Print the number of matching items
    return jsonify(clinicinfo)
@app.route('/location/<state>/<city>', methods = ['GET'])
def get_location(state, city):
    clinicinfo = []
    data = fetch_data()
    for x in data:
        if 'State Name' in x and 'Site City' in x:
            if x['State Name'].lower().strip() == state.lower().strip() and x['Site City'].lower().strip() == city.lower().strip():
                clinicinfo.append({
                    'Site Name': x['Site Name'],
                })
    return jsonify(clinicinfo)

@app.route('/program/<sitename>', methods = ['GET'])
def getprogram(sitename):
    clinicinfo=[]
    data = fetch_data()
    for x in data:
        if 'Site Name' in x:
            if x['Site Name'] == sitename:
                # a= x['Migrant Health Centers HRSA Grant Subprogram Indicator']
                # b = x['Community Health HRSA Grant Subprogram Indicator']
                # c = x['School Based Health Center HRSA Grant Subprogram Indicator']
                # d = x['Public Housing HRSA Grant Subprogram Indicator']
                # e = x['Health Care for the Homeless HRSA Grant Subprogram Indicator']
                clinicinfo.append({
                    'Migrant Health Centers HRSA Grant Subprogram Indicator': x['Migrant Health Centers HRSA Grant'
                                                                                ' Subprogram Indicator'],
                    'Community Health HRSA Grant Subprogram Indicator': x['Community Health HRSA Grant Subprogram '
                                                                          'Indicator'],
                    'School Based Health Center HRSA Grant Subprogram Indicator' :x['School Based Health Center HRSA'
                                                                                    ' Grant Subprogram Indicator'],
                    'Public Housing HRSA Grant Subprogram Indicator': x['Public Housing HRSA Grant Subprogram Indica'
                                                                        'tor'],
                    'Health Care for the Homeless HRSA Grant Subprogram Indicator': x['Health Care for the Homeless '
                                                                                      'HRSA Grant Subprogram Indicator']
                })
    return jsonify(clinicinfo)
@app.route('/data', methods=['POST', 'GET', 'DELETE'])
def data():
    """
       Manages health center data in Redis.

       POST:
           Loads health center data into Redis.
       GET:
           Retrieves health center data from Redis.
       DELETE:
           Clears all health center data stored in Redis.

       Returns:
           str: Response message.
       """
    data = fetch_data()
    if request.method == 'POST':
        for item in data:
            if 'Health Center Site Fact Identification Number' in item:
                return item['Health Center Site Fact Identification Number']
                #rd.set(item['Health Center Site Fact Identification Number'], json.dumps(item))
        #return 'Data loaded to Redis', 201

    if request.method == 'GET':
        for item in data:
            return jsonify(item['Health Center Site Fact Identification Number'])
        #return_value = [json.loads(rd.get(item)) for item in rd.keys()]
        #return jsonify(return_value)

    if request.method == 'DELETE':
        for item in rd.keys():
            rd.delete(item)
        return 'Data deleted from Redis\n'
@app.route('/data', methods=['DELETE'])
def delete_data() -> str:
    rd2.delete('data')
    message = 'Successfully deleted all the data from the dictionary!\n'
    return message


@app.route('/data', methods=['POST'])
def post_data() -> str:
    data = parse_csv_data(csv_file_path)
    try:
        rd2.set('healthcare_data', json.dumps(data))
        return "Data stored in Redis successfully."
    except Exception as e:
        return "Error storing data in Redis:" + str(e)


def list_of_jobs():
    """
    Retrieve a list of all job IDs.

    Returns:
        list: A list of job IDs.
    """
    # Fetch all keys from the Redis database (assuming job IDs are used as keys)
    job_ids = rd2.keys()
    return job_ids

#@app.route('/poop', methods = ['GET'])
def get_healthcenters():
    health_centers = []
    data = fetch_data()
    for x in data:
        if 'Site Name' in x and 'Site Address' in x and 'Site City' in x and 'Site State Abbreviation' in x:
            center = {
                "name": x['Site Name'],
                "address": f"{x['Site Address']}, {x['Site City']}, {x['Site State Abbreviation']}, USA"
            }
            health_centers.append(center)
    return health_centers

@app.route('/jobs', methods=['GET'])
def get_list_of_jobs():
    jobsList = list_of_jobs()
    # Convert bytes objects to strings before jsonify
    jobsList = [job.decode('utf-8') if isinstance(job, bytes) else job for job in jobsList]
    return jsonify(jobsList)


def get_addresshealthcenters():
    health_centers = []
    data = fetch_data()
    for x in data:
        if 'Site Name' in x and 'Site Address' in x and 'Site City' in x and 'Site State Abbreviation' in x:
            center = {
                "name": x['Site Name'],
                "address": f"{x['Site Address']}, {x['Site City']}, {x['Site State Abbreviation']}, USA"
            }
            health_centers.append(center)
    return health_centers
def get_coordinates_from_data(data):
    # Extract the coordinates directly from the data
    coordinates = []
    for item in data:
        if 'Geocoding Artifact Address Primary X Coordinate' in item and 'Geocoding Artifact Address Primary Y Coordinate' in item:
            x = item['Geocoding Artifact Address Primary X Coordinate']
            y = item['Geocoding Artifact Address Primary Y Coordinate']
            coordinates.append((x, y))
    return coordinates

def get_coordinates(address):
    geolocator = Nominatim(user_agent="myfinalproject", timeout= 15)
    try:
        location = geolocator.geocode(address)
        if location is not None:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not get coordinates for address: {address}")
            return None
    except GeocoderUnavailable:
        print(f"GeocoderUnavailable for address: {address}, retrying...")
        time.sleep(5)  # wait for 5 seconds before retrying
        return get_coordinates(address)


def find_nearest_center(user_location):
    user_coordinates = None
    if isinstance(user_location, str):
        user_coordinates = get_coordinates(user_location)
    else:
        user_coordinates = user_location
    health_centers = get_addresshealthcenters()
    nearest_center = min(health_centers, key=lambda center: geodesic(user_coordinates, get_coordinates(center["address"])).miles)
    return nearest_center

def generate_heatmap():
    # Convert the health center addresses to coordinates
    data = fetch_data()
    coordinates = get_coordinates_from_data(data)

    # Create a GeoDataFrame from the coordinates
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy([coord[0] for coord in coordinates], [coord[1] for coord in coordinates]))

    # Extract the x and y coordinates from the geometry column
    gdf['x'] = gdf.geometry.x
    gdf['y'] = gdf.geometry.y
    gdf = gdf.dropna(subset=['x', 'y'])

    # Create a map centered at the average coordinates
    m = folium.Map(location=[gdf['y'].mean(), gdf['x'].mean()], zoom_start=6)

    # Add a heatmap to the map
    HeatMap(data=gdf[['y', 'x']].values, radius=15).add_to(m)

    # Display the map
    m.save('heatmap.html')

def plot_route(user_location, center):
    user_coordinates = get_coordinates(user_location)
    center_coordinates = get_coordinates(center["address"])

    # Create a map centered at the user's location
    m = folium.Map(location=user_coordinates, zoom_start=14)

    # Add markers for the user and the health center
    folium.Marker(user_coordinates, popup='User', icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(center_coordinates, popup=center['name'], icon=folium.Icon(color='blue')).add_to(m)

    # Draw a line between the user and the health center
    folium.PolyLine([user_coordinates, center_coordinates], color="green", weight=2.5, opacity=1).add_to(m)

    # Display the map
    m.save('route.html')
.keys())

@app.route('/results/<jobid>', methods = ['GET'])
def get_results(jobid):
    # Get the userlocation from the query parameters (default to None if not provided)
    userlocation = request.args.get('userlocation')
    if jobid == 'heatmap':

        generate_heatmap()
        return "Heatmap generated successfully", 200
    elif jobid == 'nearesthealthcenter':
        if userlocation is None:
            return {"error": "User location is required for nearesthealthcenter job"}, 400
        center = find_nearest_center(userlocation)
        plot_route(userlocation, center)


@app.route('/jobs', methods = ['GET','POST'])
def submit_job():
    global job_ids
    if request.method == 'POST':
        data = request.get_json()
        job_dict = None
        if data['type'] == 'maptonearestcenter':
            job_dict = add_job(data['type'], data['params'])
        elif data['type'] == 'heatmap':
            job_dict = add_job(data['type'], data['params'])
        # Add the new job ID to the list
        job_ids.append(job_dict['id'])
        return job_dict
    elif request.method == 'GET':
        # Return the list of job IDs
        return job_ids

@app.route('/jobs', methods = ['GET','POST'])
def submit_job():
    if request.method == 'POST':
        data = request.get_json()
        job_dict = None
        if data['type'] == 'maptonearestcenter':
            job_dict = add_job(data['type'], data['params'])
        elif data['type'] == 'heatmap':
            job_dict = add_job(data['type'], data['params'])
        return job_dict

    elif request.method == 'GET':
        job_ids = [job.decode('utf-8') for job in rd.keys()]
        return job_ids


@app.route('/jobs/<string:jid>', methods=['GET'])
def get_job(jid: str) -> dict:
    results = rd2.get(jid)
    if results is None:
        return jsonify({'error': 'The job ID is invalid, please try again.'}), 404
    else:
        try:
            json_results = json.loads(results)
            return jsonify(json_results)
        except json.JSONDecodeError as e:
            return jsonify({'error': 'Failed to decode job results: {}'.format(str(e))}), 500


@app.route('/jobs/clear', methods=['DELETE'])
def clear_jobs() -> str:
    rd.flushdb()
    return 'Successfully cleared the jobs list!\n'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
