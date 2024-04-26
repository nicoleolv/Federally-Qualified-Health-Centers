from job import get_job_by_id, update_job_status,q,rd
from FinalProject import get_health_centers, get_type_of_healthcenter

@q.worker()
def do_work(jobid):

    job_details = get_job_by_id(jobid)
    update_job_status(jobid, 'in progress')
    if job_details['type'] == 'health_center_lookup':
        city = job_details['site city']
        state = job_details['site state abbreviation']

        health_centers = get_health_centers(city,state)
        for center in health_centers:
            print(center)
    elif job_details['type'] == 'type_of_healthcenter':
        city = job_details['site city']
        state = job_details['site state abbreviation']
        typeofcenter = job_details['params']['type of center']
        result = get_type_of_healthcenter(city, state, typeofcenter)
        print(result)
    update_job_status(jobid, 'complete')
#which site have the program you need
