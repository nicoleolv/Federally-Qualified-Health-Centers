# Healthcare Center Data Management System
This project provides a system for managing and analyzing data related to healthcare centers. It includes a Flask API for data manipulation and job handling, as well as worker processes for executing jobs asynchronously. The system utilizes Redis for data storage and task queue management.
## Installation
1. Clone the repository:
```bash
git clone <repository_url>
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up Redis:Ensure that Redis is installed and running. Set the environment variable REDIS_IP to the Redis server's IP address.
## Usage
### Starting the API
Run the Flask API using the following command:
```bash
python api.py
```
The API will be accessible at http://localhost:5000.
### Executing Jobs
Worker processes can be started to execute jobs from the task queue. Run the worker using:
```bash
python worker.py
```
### API Endpoints
- POST /data: Reloads the data from the web and stores it in Redis.
- DELETE /data: Deletes all data from the Redis database.
- GET /jobs: Retrieves a list of all queued jobs.
- POST /jobs/:route: Queues a new job with the specified route.
- GET /jobs/:jid: Retrieves the result of a specific job by its ID.
- DELETE /jobs/clear: Clears all queued jobs.
### Available Routes
- get_sites_by_state-<state>: Retrieves a list of healthcare centers in the specified state.
### Example Usage
1. Load Data:
```bash
curl -X POST http://localhost:5000/data
```
2. Queue a job:
```bash
curl -X POST http://localhost:5000/jobs/get_sites_by_state-TX
```
3. Check job status:
```bash
curl http://localhost:5000/jobs/:job_id
```
## Analysis of Healthcare Center Data
The provided data contains information about healthcare centers, including their names, addresses, and states. Analyzing this data can provide insights into the distribution and density of healthcare facilities across different states.

One possible analysis is to identify the number of healthcare centers in each state. This information can be useful for healthcare resource allocation and planning. By counting the number of healthcare centers in each state, we can identify regions with higher or lower concentrations of healthcare facilities.

Additionally, we can analyze the distribution of healthcare centers within specific regions. For example, we can determine the average distance between healthcare centers in urban areas compared to rural areas. This analysis can inform decisions related to healthcare access and infrastructure development.

Furthermore, we can analyze trends in healthcare center growth over time. By comparing data from different time periods, we can identify regions experiencing significant changes in healthcare infrastructure and address emerging needs accordingly.

Overall, analyzing healthcare center data can provide valuable insights for policymakers, healthcare providers, and researchers to improve healthcare access and delivery.