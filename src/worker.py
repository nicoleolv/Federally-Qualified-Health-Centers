# worker.py

from hotqueue import HotQueue
from redis import Redis
from jobs import update_job_status, get_data, compute_average_hours, site_count_by_state
import json
import os

# Get the Redis service hostname from the environment
redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()

# Define the Redis connection
rd = Redis(host=redis_ip, port=6379, db=0)
q = HotQueue('queue', host=redis_ip, port=6379, db=1)
rd2 = Redis(host=redis_ip, port=6379, db=2)

@q.worker
def execute_job(item: str) -> dict:
    """
    Retrieve a job id from the task queue and execute the job.
    Monitors the job to completion and updates the database accordingly.

    Args:
        Item (str): the job's id from the queue object created by jobs.py

    Returns:
        new_job (Dict): the dictionary object of the job that was completed.
    """
    current_jid = item

    update_job_status(current_jid, 'in progress')

    current_job = json.loads(rd.get(current_jid))
    current_route = current_job['route']
    args = []

    if '-' in current_route:
        args = current_route.split('-')
        function = args[0]
        args[1] = args[1].replace('_', ' ')
    else:
        function = current_route

    full_data = get_data()

    status = 'completed'
    result = None

    if full_data == 'The data does not exist.':
        result = 'The data does not exist, make sure to POST the data!'
        status = 'incompleted'
    else:
        if function == 'compute_average_hours':
            result = compute_average_hours(full_data)
        elif function == 'site_count_by_state':
            result = site_count_by_state(full_data)
        else:
            status = 'incompleted'
            result = 'Could not parse a proper function from the route provided.'

    if result is not None:
        rd2.set(current_jid, json.dumps(result))
        update_job_status(current_jid, status)

execute_job()
