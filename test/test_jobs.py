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
        "site_postal_code": "40336-7356"
        "health_center_site_population_type_description": "Rural"
        "site_status_description": "Active"
        "complete_county_name": "Estill"
        "name_of_u_s_senator_number_one": "Mitch McConnell"
        "geocoding_artifact_address_primary_x_coordinate": "-84.00052000"
        "geocoding_artifact_address_primary_y_coordinate": "37.70306100"
        # site open date? 
    },
    {
        "health_center_site_fact_identification_number": "2",
        "site_name": "La Clinica School-Based Health Center",
        "site_telephone_number": "541-535-6239",
        "site_web_address": "www.laclinicahealth.org",
        "operating_hours_per_week": "42.50",
        "health_center_grantee_identification_number": "943"
        "grant_number": "H80CS00759"
        "grantee_name": "LA CLINICA DEL VALLE FAMILY HEALTH CARE CENTER"
        "migrant_health_centers_hrsa_grant_subprogram_indicator": "Y"
        "community_health_centers_grant_subprogram_indicator": "Y"
        "school_based_health_center_hrsa_grant_subprogram_indicator": "N"
        "public_housing_hrsa_grant_subprogram_indicator": "N"
        "health_care_for_the_homeless_hrsa_grant_subprogram_indicator": "Y"
        "site_address": "215 N Rose St"
        "site_city": "Phoenix"
        "site_state_abbreviation": "OR"
        "site_postal_code": "97535-5734"
        "health_center_site_population_type_description": "Urban"
        "site_status_description": "Active"
        "complete_county_name": "Jackson County"
        "name_of_u_s_senator_number_one": "Jeff Merkley"
        "geocoding_artifact_address_primary_x_coordinate": "-122.81958200"
        "geocoding_artifact_address_primary_y_coordinate": "42.27330700"
    },
    {
         "health_center_site_fact_identification_number": "3",
        "site_name": "Nicole's Clinic",
        "site_telephone_number": "214-601-4478",
        "site_web_address": "www.nicolesclinic.com",
        "operating_hours_per_week": "85.00",
        "health_center_grantee_identification_number": "33"
        "grant_number": "NIC33000"
        "grantee_name": "NICOLE HEALTH INCORPORATED"
        "migrant_health_centers_hrsa_grant_subprogram_indicator": "Y"
        "community_health_centers_grant_subprogram_indicator": "Y"
        "school_based_health_center_hrsa_grant_subprogram_indicator": "Y"
        "public_housing_hrsa_grant_subprogram_indicator": "Y"
        "health_care_for_the_homeless_hrsa_grant_subprogram_indicator": "Y"
        "site_address": "935 Oak Gate Ln"
        "site_city": "Dallas"
        "site_state_abbreviation": "TX"
        "site_postal_code": "80588-75149"
        "health_center_site_population_type_description": "Unknown"
        "site_status_description": "Active"
        "complete_county_name": "Dallas County"
        "name_of_u_s_senator_number_one": "Ted Cruz"
        "geocoding_artifact_address_primary_x_coordinate": "-33.090909"
        "geocoding_artifact_address_primary_y_coordinate": "33.090909"
        # maybe remove site status? 
    }
]

def test_add_job():
    # test add_job function
    job_dict = add_job(sample_health_data[0][''], sample_health_data[1]['date_modified'])
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
    job_dict = add_job(sample_health_data[0]['date_modified'], sample_gene_data[1]['date_modified'])
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
