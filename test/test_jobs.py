import pytest
from jobs import add_job, get_job_by_id, update_job_status

sample_health_data = [
    {
        "health_center_site_fact_identification_number": "1",
        "site_name": "White House Clinic - Irvine",
        "site_telephone_number": "606-723-0665",
        "site_web_address": "www.whitehouseclinics.com",
        "operating_hours_per_week": "42.00",
        "health_center_grantee_identification_number": "947"
        "grant_number": "H80CS00459"
        "grantee_name": "HEALTH HELP, INCORPORATED"
        "migrant_health_centers_hrsa_grant_subprogram_indicator": "N"
        "community_health_centers_grant_subprogram_indicator": "Y"
        "school_based_health_center_hrsa_grant_subprogram_indicator": "N"
        "public_housing_hrsa_grant_subprogram_indicator": "N"
        "health_care_for_the_homeless_hrsa_grant_subprogram_indicator": "N"
        "site_address": "30 Stacy Lane Rd"
        "site_city": "Irvine"
        "site_state_abbreviation": "KY"
        # add more
    },
    {
        "..."
    },
    {
        "..."
    }
]

def test_add_job():
    # test add_job function
    job_dict = add_job(sample_gene_data[0]['date_modified'], sample_gene_data[1]['date_modified'])
    assert 'id' in job_dict
    assert job_dict['status'] == 'submitted'

def test_get_job_by_id():
    # test get_job_by_id function
    job_data = get_job_by_id('123')
    assert job_data['id'] == '123'
    assert 'status' in job_data

def test_update_job_status():
    # test update_job_status function
    with pytest.raises(Exception):
        update_job_status('invalid_job_id', 'completed')_data = []
        
def test_add_job():
    # test add_job function
    job_dict = add_job(sample_gene_data[0]['date_modified'], sample_gene_data[1]['date_modified'])
    assert 'id' in job_dict
    assert job_dict['status'] == 'submitted'

def test_get_job_by_id():
    # test get_job_by_id function
    job_data = get_job_by_id('123')
    assert job_data['id'] == '123'
    assert 'status' in job_data

def test_update_job_status():
    # test update_job_status function
    with pytest.raises(Exception):
        update_job_status('invalid_job_id', 'completed')
