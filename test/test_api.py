import os
import json
import pytest
from unittest.mock import patch, MagicMock
from your_flask_app import app, delete_data, post_data, list_of_jobs, get_list_of_jobs, post_job, get_job, get_site_names, clear_jobs

# Mocking Redis and HotQueue instances
@patch('api.Redis')
@patch('api.HotQueue')
def test_post_data(mock_HotQueue, mock_Redis):
    # Mocking parse_csv_data function
    with patch('api.parse_csv_data', return_value=[{"example": "data"}]):
        # Test POST data endpoint
        with app.test_client() as client:
            response = client.post('/data')
            assert response.status_code == 200
            assert b"Data stored in Redis successfully." in response.data

@patch('api.rd2')
def test_delete_data(mock_rd2):
    # Test DELETE data endpoint
    with app.test_client() as client:
        response = client.delete('/data')
        assert response.status_code == 200
        assert b"Successfully deleted all the data from the dictionary!" in response.data

@patch('api.rd2')
def test_list_of_jobs(mock_rd2):
    # Test list_of_jobs function
    mock_rd2.keys.return_value = [b'job1', b'job2']
    assert list_of_jobs() == [b'job1', b'job2']

def test_get_list_of_jobs():
    # Test GET list of jobs endpoint
    with app.test_client() as client:
        response = client.get('/jobs')
        assert response.status_code == 200
        assert b'job1' in response.data
        assert b'job2' in response.data

@patch('api.q')
def test_post_job(mock_q):
    # Test POST job endpoint
    with app.test_client() as client:
        response = client.post('/jobs/test_route')
        assert response.status_code == 200
        assert b"Successfully queued a job!" in response.data

@patch('api.rd2')
def test_get_job(mock_rd2):
    # Mocking Redis data for a job
    mock_rd2.get.return_value = json.dumps({'id': 'test_job_id', 'status': 'submitted', 'route': 'test_route'})
    # Test GET job endpoint
    with app.test_client() as client:
        response = client.get('/jobs/test_job_id')
        assert response.status_code == 200
        assert b'"id": "test_job_id"' in response.data
        assert b'"status": "submitted"' in response.data

@patch('api.rd2')
def test_get_site_names(mock_rd2):
    # Mocking Redis healthcenter data
    mock_rd2.get.return_value = json.dumps([
        {"Site Name": "Site 1"},
        {"Site Name": "Site 2"}
    ])
    # Test GET site names endpoint
    with app.test_client() as client:
        response = client.get('/sites')
        assert response.status_code == 200
        assert b'Site 1' in response.data
        assert b'Site 2' in response.data

@patch('api.rd')
def test_clear_jobs(mock_rd):
    # Test DELETE jobs endpoint
    with app.test_client() as client:
        response = client.delete('/jobs/clear')
        assert response.status_code == 200
        assert b"Successfully cleared the jobs list!" in response.data
