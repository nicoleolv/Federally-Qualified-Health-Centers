#!/usr/bin/env python3
import csv
import pandas as pd
from flask import Flask, request, jsonify
import requests
from io import StringIO
import json
import redis
from jobs import add_job, get_job_by_id, rd

app = Flask(__name__)

# Initialize Redis connection
rd = redis.Redis(host='redis-db', port=6379, db=0)

def fetch_data():
    """
     Fetches health center data from an external source (CSV file).

     Returns:
         list: Health center data in list of dictionaries format.
     """
    df = list(pd.read_csv('https://query.data.world/s/3zhr263bmtw3sdxb7wakvqo3j5ih2i?dws=00000'))

    return df

@app.route('/healthcenter/<Health_Center_Site_Fact_Identification_Number>', methods=['GET'])
def get_specific_gene(id_num):
    """
    Retrieves all data associated with a specific Health Center Site Fact Identification Number.

    Args:
        Health_Center_Site_Fact_Identification_Number (str): Health Center Site Fact Identification Number to retrieve data for.

    Returns:
        dict: Health center data for the specified ID.
    """
    results = []
    for x in data:
        if 'Health Center Site Fact Identification Number' in x:
            if x['Health Center Site Fact Identification Number'] == id_num:
                results.append(x)


    return jsonify(results)

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
    if request.method == 'POST':
        data = fetch_data()
        for item in data:
            if 'Health Center Site Fact Identification Number' in item:
                rd.set(item['Health Center Site Fact Identification Number'], json.dumps(item))
        return 'Data loaded to Redis', 201

    elif request.method == 'GET':
        data = [json.loads(rd.get(item)) for item in rd.keys()]
        return jsonify(data)

    elif request.method == 'DELETE':
        for item in rd.keys():
            rd.delete(item)
        return 'Data deleted from Redis\n'
    
@app.route('/healthcenter/<site_name>', methods=['GET'])
def get_phone_num(site_name):
    phone_num = []
    data = fetch_data()
    for i in data():
        if 'site name' in i:
            if i['site name'] == site_name:
                phone_num.append(x)

    return jsonify(phone_num)

def get_health_centers(city,state):
    if not city or not state:
        return jsonify({'message': 'Both city and state are required.'})
    cityhealthcenter = []
    data = fetch_data()
    for x in data():
        if 'site city' in x and 'site state abbreviation' in x:
            if x['site city'] == city and x['site state abbreviation'] == state:
                cityhealthcenter.append(x)
    return jsonify(cityhealthcenter)

def fetch_healthcenter_type():
    data = fetch_data()
    listofhealthcentertypes = []
    health_center_types = [
        'Migrant Health Centers HRSA Grant Subprogram Indicator',
        'Community Health HRSA Grant Subprogram Indicator',
        'School Based Health Center HRSA Grant Subprogram Indicator',
        'Public Housing HRSA Grant Subprogram Indicator',
        'Health Care for the Homeless HRSA Grant Subprogram Indicator'
    ]
    for record in data:
        for key in record.keys():
            if key in health_center_types:
                listofhealthcentertypes.append(key)
    return listofhealthcentertypes
def get_type_of_healthcenter(city,state, typeofcenter):
    yourhealthcenters = get_health_centers(city,state)
    for x in yourhealthcenters:
        for y in x.keys():
            if typeofcenter == y:
                z = x[y]
                if z == 'N':
                    return 'The health center you are looking for is not available in your area'
                elif z == 'Y':
                    return jsonify(y)



@app.route('/jobs', methods = ['GET','POST'])
def submit_job():
    if request.method == 'POST':
        data = request.get_json()
        job_dict = None
        if data['type'] == 'health_center_lookup':
            job_dict = add_job(data['type'], data['params'])
        elif data['type'] == 'type_of_healthcenter':
            job_dict = add_job(data['type'], data['params'])
        return job_dict

    elif request.method == 'GET':
        job_ids = [job.decode('utf-8') for job in rd.keys()]
        return job_ids

@app.route('/results/<jobid>', methods=['GET'])
def get_results(jobid):
    """
    Returns the analysis the worker made given a job id
    """
    try:
        job_data = get_job_by_id(jobid)
        if job_data['status'] == 'complete':
            results = get_analysis_results(jobid)
            return jsonify(results)
        else:
            return "Job is still in progress..."
    except raise ValueError('Job id provided is invalid.')

@app.route('/jobs/<jobid>', methods=['GET'])
def get_job(jobid):
    """
    Returns a job specified by a unique jobid
    """
    return get_job_by_id(jobid)    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
