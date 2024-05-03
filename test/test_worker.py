import os
import json
import pytest
from unittest.mock import patch, MagicMock
from worker import execute_job, update_job_status, get_data, compute_average_hours, site_count_by_state

# Mocking Redis and HotQueue instances
@patch('worker.Redis')
@patch('worker.HotQueue')
def test_execute_job(mock_HotQueue, mock_Redis):
    # Mocking data in Redis
    mock_rd = MagicMock()
    mock_rd.get.return_value = json.dumps({'id': 'test_job_id', 'route': 'compute_average_hours'})
    mock_Redis.return_value = mock_rd

    # Mocking get_data function
    with patch('worker.get_data', return_value={"sites": [{"Operating Hours per Week": "40"}, {"Operating Hours per Week": "50"}]}):
        # Mocking compute_average_hours function
        with patch('worker.compute_average_hours', return_value=45.0):
            # Test execute_job function
            execute_job('test_job_id')
            assert mock_rd.set.called_once_with('test_job_id', json.dumps(45.0))
            assert update_job_status.called_once_with('test_job_id', 'completed')

    # Mocking a different job route
    mock_rd.get.return_value = json.dumps({'id': 'test_job_id', 'route': 'site_count_by_state'})
    # Mocking site_count_by_state function
    with patch('worker.site_count_by_state', return_value={'NY': 2, 'CA': 3}):
        # Test execute_job function with different route
        execute_job('test_job_id')
        assert mock_rd.set.called_once_with('test_job_id', json.dumps({'NY': 2, 'CA': 3}))
        assert update_job_status.called_once_with('test_job_id', 'completed')

    # Test execute_job function with invalid data
    mock_rd.get.return_value = None
    execute_job('test_job_id')
    assert mock_rd.set.called_once_with('test_job_id', json.dumps('The data does not exist, make sure to POST the data!'))
    assert update_job_status.called_once_with('test_job_id', 'incompleted')

@patch('worker.rd2')
def test_update_job_status(mock_rd2):
    # Mocking rd2.set
    update_job_status('test_job_id', 'completed')
    assert mock_rd2.set.called_once_with('test_job_id', json.dumps({'status': 'completed'}))


