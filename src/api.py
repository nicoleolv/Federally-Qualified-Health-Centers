# api.py

from flask import Flask, jsonify
import os
from redis import Redis
from hotqueue import HotQueue
import json
from jobs import add_job, parse_csv_data, get_data

# Get the Redis service hostname from the environment
redis_host = os.environ.get('REDIS_HOST', 'redis')

# Define the Redis connection
rd = Redis(host=redis_host, port=6379, db=0)
q = HotQueue('queue', host=redis_host, port=6379, db=1)
rd2 = Redis(host=redis_host, port=6379, db=2)
app = Flask(__name__)

# Define the path to the CSV file
csv_file_path = './data/SITE_HCC_FCT_DET.csv'

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

@app.route('/jobs', methods=['GET'])
def get_list_of_jobs():
    jobsList = list_of_jobs()
    # Convert bytes objects to strings before jsonify
    jobsList = [job.decode('utf-8') if isinstance(job, bytes) else job for job in jobsList]
    return jsonify(jobsList)

@app.route('/jobs/<string:route>', methods=['POST'])
def post_job(route: str) -> dict:
    jid = add_job(q, route)  # Pass 'q' as an argument
    return f'Successfully queued a job! \nTo view the status of the job, curl /jobs.\nHere is the job ID: {jid}\n'

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

# Get list of site names
@app.route('/sites', methods=['GET'])
def get_site_names():
    # Retrieve data from Redis
    data_json = rd2.get('healthcare_data')
    if not data_json:
        return jsonify({'error': 'Healthcare data not found. Please load data first using /data endpoint.'}), 404
    
    data = json.loads(data_json)
    site_names = [site['Site Name'] for site in data]
    return jsonify(site_names)

@app.route('/jobs/clear', methods=['DELETE'])
def clear_jobs() -> str:
    rd.flushdb()
    return 'Successfully cleared the jobs list!\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
