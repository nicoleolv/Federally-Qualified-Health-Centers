# Federally Qualified Health Centers Analysis API

## Purpose
This repository contains a full flask application with redis to analyze data about Federally Qualified Health Centers provided by the U.S. Department of Health and Human Services. This data is useful and important to gather accurate information about FQHCs available throughout the U.S.. Overall, this project is used to gain familiarity with flask web applications, redis database, jobs and worker functionality, docker, and kubernetes, while also analyzing important FQHC data.

 ## Summary of Contents
* `api.py`: Flask web application with redis database
* `worker.py`: Handles all jobs processed from the redis queue
* `jobs.py`: Contains functions for creating, retrieving, and updating jobs in the redis queue
* `test_api.py`: Tests all the api.py functions with a sample data
* `test_jobs.py`: Tests all the jobs.py functions with a sample data
* `test_worker.py`: Tests all the worker.py functions with a sample data
* `requirements.txt`: Lists all of the necessary Python depenedencies to run our app
* `Dockerfile`: Contains instructions to build our docker image
* `docker-compose.yml`: Configuration file that allows for a simplified `docker run` command
* `diagram.png`: Software diagram that depicts our working environment 

## Data
The FQGC data is available to the public and can be downloaded from data.world; [](https://data.world/hhs/fed-qualified-health-centers/workspace/file?filename=SITE_HCC_FCT_DET.csv). This data contains a lot of specifications for each FQHC, including the site name, address, phone number, a few subprogram . For a better understanding of what the data yields, I recommend reading the paragraphs provided (on the website) and taking a look at the data itself. 

