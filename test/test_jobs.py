import pytest
import json
import os
from unittest.mock import patch, MagicMock
from jobs import parse_csv_data, compute_average_hours, site_count_by_state, add_job, get_data

# Defining sample data for testing
sample_health_data = [
    {
        "health_center_site_fact_identification_number": "1",
        "site_name": "White House Clinic - Irvine",
        "site_telephone_number": "606-723-0665",
        "site_web_address": "www.whitehouseclinics.com",
        "operating_hours_per_week": "42.00",
        "migrant_health_centers_hrsa_grant_subprogram_indicator": "N",
        "community_health_centers_grant_subprogram_indicator": "Y",
        "school_based_health_center_hrsa_grant_subprogram_indicator": "N",
        "public_housing_hrsa_grant_subprogram_indicator": "N",
        "health_care_for_the_homeless_hrsa_grant_subprogram_indicator": "N",
        "site_address": "30 Stacy Lane Rd",
        "site_city": "Irvine",
        "site_state_abbreviation": "KY",
        "site_postal_code": "40336-7356",
        "health_center_site_population_type_description": "Rural",
        "site_status_description": "Active",
        "geocoding_artifact_address_primary_x_coordinate": "-84.00052000",
        "geocoding_artifact_address_primary_y_coordinate": "37.70306100" 
    },
    {
        "health_center_site_fact_identification_number": "2",
        "site_name": "La Clinica School-Based Health Center",
        "site_telephone_number": "541-535-6239",
        "site_web_address": "www.laclinicahealth.org",
        "migrant_health_centers_hrsa_grant_subprogram_indicator": "Y",
        "community_health_centers_grant_subprogram_indicator": "Y",
        "school_based_health_center_hrsa_grant_subprogram_indicator": "N",
        "public_housing_hrsa_grant_subprogram_indicator": "N",
        "health_care_for_the_homeless_hrsa_grant_subprogram_indicator": "Y",
        "site_address": "215 N Rose St",
        "site_city": "Phoenix",
        "site_state_abbreviation": "OR",
        "site_postal_code": "97535-5734",
        "health_center_site_population_type_description": "Urban",
        "site_status_description": "Active",
        "geocoding_artifact_address_primary_x_coordinate": "-122.81958200",
        "geocoding_artifact_address_primary_y_coordinate": "42.27330700"
    },
    {
        "health_center_site_fact_identification_number": "3",
        "site_name": "Nicole's Clinic",
        "site_telephone_number": "214-601-4478",
        "site_web_address": "www.nicolesclinic.com",
        "operating_hours_per_week": "85.00",
        "migrant_health_centers_hrsa_grant_subprogram_indicator": "Y",
        "community_health_centers_grant_subprogram_indicator": "Y",
        "school_based_health_center_hrsa_grant_subprogram_indicator": "Y",
        "public_housing_hrsa_grant_subprogram_indicator": "Y",
        "health_care_for_the_homeless_hrsa_grant_subprogram_indicator": "Y",
        "site_address": "935 Oak Gate Ln",
        "site_city": "Dallas",
        "site_state_abbreviation": "TX",
        "site_postal_code": "80588-75149",
        "health_center_site_population_type_description": "Unknown",
        "site_status_description": "Active",
        "geocoding_artifact_address_primary_x_coordinate": "-33.090909",
        "geocoding_artifact_address_primary_y_coordinate": "33.090909" 
    }
]

@patch('jobs.Redis')
@patch('jobs.HotQueue')
def test_add_job(mock_HotQueue, mock_Redis):
    # test add_job function
    with patch('jobs._generate_jid', return_value='test_job_id'):
        add_job(q=None, route='test_route')
        mock_Redis.assert_called_once_with(host=os.environ.get('REDIS_IP'), port=6379, db=2)
        mock_Redis().set.assert_called_once_with('test_job_id', json.dumps({'id': 'test_job_id', 'status': 'submitted', 'route': 'test_route'}))
        mock_HotQueue.assert_called_once_with('queue', host=os.environ.get('REDIS_IP'), port=6379, db=1)
        mock_HotQueue().put.assert_called_once_with('test_job_id')

def test_parse_csv_data(tmp_path):
    # test parse_csv_data
    csv_file_path = tmp_path / "test.csv"
    with open(csv_file_path, 'w') as f:
        f.write("health_center_site_fact_identification_number,site_name,site_telephone_number,site_web_address,operating_hours_per_week,site_state_abbreviation\n")
        f.write("1,White House Clinic - Irvine,606-723-0665,www.whitehouseclinics.com,42.00,KY\n")
        f.write("2,La Clinica School-Based Health Center,541-535-6239,www.laclinicahealth.org,42.50,OR\n")
        f.write("3,Nicole's Clinic,214-601-4478,www.nicolesclinic.com,85.00,TX\n")

    parsed_data = parse_csv_data(csv_file_path)
    assert len(parsed_data) == 3
    assert parsed_data[0]['site_name'] == "White House Clinic - Irvine"
    assert parsed_data[1]['site_state_abbreviation'] == "OR"
    assert parsed_data[2]['operating_hours_per_week'] == "85.00"

def test_compute_average_hours():
    # test computing average operating hours
    average_hours = compute_average_hours({'sites': sample_health_data})
    assert average_hours == (42.0 + 42.5 + 85.0) / 3

def test_site_count_by_state():
    # test counting sites by state
    state_counts = site_count_by_state({'sites': sample_health_data})
    assert state_counts['KY'] == 1
    assert state_counts['OR'] == 1
    assert state_counts['TX'] == 1

@patch('your_script_name.rd')
def test_get_data(mock_rd):
    # mock storing data in Redis
    get_data()
    mock_rd.set.assert_called_once()
