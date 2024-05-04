# jobs.py

import os
import json
import uuid  # Add this import for generating UUIDs
from hotqueue import HotQueue
import csv
from pprint import pprint

from redis import Redis

redis_ip = os.environ.get('REDIS_IP')
print("REDIS_IP:", redis_ip)  # Add this line for debugging
if not redis_ip:
    raise Exception()

rd = Redis(host=redis_ip, port=6379, db=0)
q = HotQueue("queue", host=redis_ip, port=6379, db=1)
rd2 = Redis(host=redis_ip, port=6379, db=2)

# Define the path to the CSV file relative to the current working directory
csv_file_path = os.path.join(os.getcwd(), 'data', 'SITE_HCC_FCT_DET.csv')

# Ensure that the CSV file exists
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"CSV file not found at: {csv_file_path}")

def parse_csv_data(csv_file: str) -> list:
    """
    Parse the CSV file containing healthcare center data and return as a list of dictionaries.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        data (list): A list of dictionaries representing each row of data.
    """
    data = []

    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error parsing CSV data: {e}")
    else:
        print("CSV data parsed successfully:")
        #for row in data:
        #    print(row)

    return data

parsed_data = parse_csv_data(csv_file_path)

# Print the parsed data
#for row in parsed_data:
#    print(row)
    
def _generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def _instantiate_job(jid, status, route):
    """
    Create the job object description as a python dictionary. Requires the job id,
    status, and route parameters.
    """
    return {'id': jid,
            'status': status,
            'route': route}

def _save_job(jid, job_dict):
    """Save a job object in the Redis database."""
    rd2.set(jid, json.dumps(job_dict))
    return

def _queue_job(q, jid):
    """Add a job to the redis queue."""
    q.put(jid)
    return

def add_job(q, route, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, route)
    _save_job(jid, job_dict)
    _queue_job(q, jid)  # Pass 'q' as an argument
    return job_dict

def get_job_by_id(jid):
    """Return job dictionary given jid"""
    return json.loads(rd2.get(jid))

def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    job_dict = get_job_by_id(jid)
    if job_dict:
        job_dict['status'] = status
        _save_job(jid, job_dict)
    else:
        raise Exception()

def get_data(csv_file: str = './data/SITE_HCC_FCT_DET.csv') -> dict:
    """
    Retrieve the healthcare center data from the csv file and return as a dictionary.

    Args:
        csv_file (str, optional): The path to the XML file. Defaults to 'SITE_HCC_FCT_DET.xml'.

    Returns:
        data (dict): The healthcare center data.
    """
    data = parse_csv_data(csv_file)

    # Store the data in Redis
    try:
        rd.set('healthcare_data', json.dumps(data))
    except Exception as e:
        print(f"Error storing data in Redis: {e}")

    return data

def compute_average_hours(data: dict) -> float:
    """
    Compute the average operating hours per week for all healthcare centers.

    Args:
        data (dict): The healthcare center data.

    Returns:
        average_hours (float): The average operating hours per week.
    """
    total_hours = 0
    num_centers = len(data['sites'])

    for site in data['sites']:
        hours = site.get('Operating Hours per Week', 0)  # Get the operating hours for each site
        total_hours += float(hours)

    if num_centers > 0:
        average_hours = total_hours / num_centers
    else:
        average_hours = 0

    return average_hours

def site_count_by_state(data: dict) -> dict:
    """
    Count the number of healthcare centers in each state.

    Args:
        data (dict): The healthcare center data.

    Returns:
        state_counts (dict): A dictionary containing the count of centers in each state.
    """
    state_counts = {}

    for site in data['sites']:
        state = site.get('Site State Abbreviation')
        if state:
            state_counts[state] = state_counts.get(state, 0) + 1

    return state_counts
