# Federally Qualified Health Centers Analysis API

## Purpose
This repository contains a full flask application with redis to analyze data about Federally Qualified Health Centers provided by the U.S. Department of Health and Human Services. This data is useful and important to gather accurate information about FQHCs available throughout the U.S.. Overall, this project is used to gain familiarity with flask web applications, redis database, jobs and worker functionality, docker, and kubernetes, while also analyzing important FQHC data.

## Data
The FQGC data is available to the public and can be downloaded from data.world; [](https://data.world/hhs/fed-qualified-health-centers/workspace/file?filename=SITE_HCC_FCT_DET.csv). This data contains a lot of specifications for each FQHC, including the site name, address, phone number, a few subprogram indicators, and much more. For a better understanding of what the data yields, I recommend reading the paragraph provided (on the website) and taking a look at the data itself.

 ## Summary of Contents
 ### src folder
* `api.py`: Flask web application with redis database
* `worker.py`: Handles all jobs processed from the redis queue
* `jobs.py`: Contains functions for creating, retrieving, and updating jobs in the redis queue
### test folder
* `test_api.py`: Tests all the api.py functions with a sample data
* `test_jobs.py`: Tests all the jobs.py functions with a sample data
* `test_worker.py`: Tests all the worker.py functions with a sample data
### other files
* `requirements.txt`: Lists all of the necessary Python depenedencies to run our app
* `Dockerfile`: Contains instructions to build our docker image
* `docker-compose.yml`: Configuration file that allows for a simplified `docker run` command
* `diagram.png`: Software diagram that depicts our working environment  

## Instructions
### Build the Image
To build our docker image, run this command:
```python
docker-compose build 
```

### Running the image 
To launch both the services, run this command:
```python
docker-compose up -d
```
You should see something like this:
```python
Creating redis-db_1 ... done
Creating worker_1   ... done
Creating api_1      ... done 
```
The app should be running now but verify with this command:
```python
docker ps -a
```
And you should see something like this: 
```python
CONTAINER ID   IMAGE                             COMMAND                  CREATED              STATUS                     PORTS                                       NAMES
619fe36d3cf9   nicoleolv/fqhc-app:1.0            "python3 api.py"         About a minute ago   Up About a minute          0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   final_flask-api_1
3bba4811e28c   nicoleolv/fqhc-app:1.0            "python3 worker.py"      About a minute ago   Up About a minute                                                      final_worker_1
f71dfd5f4101   redis:7                           "docker-entrypoint.s…"   About a minute ago   Up About a minute          0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   final_redis-db_1
```
**p.s. : to stop the services, run: `docker-compose down`**

### Accessing the Routes 
To interact with the Flask API, use `curl` commmands as shown below:
* To put the data into Redis:
  ```python
  curl -X POST localhost:5000/data
  ```
* To get all the data from Redis:
  ```python
  curl localhost:5000/data
  ```
* To delete the data from Redis:
  ```python
  curl -X DELETE localhost:5000/data
  ```
* To get a Y (yes) or N (no) if a subprogram grant is offered in healthcenter given site name:
  ```python
  curl localhost:5000/program/<sitename>
  ```
* To get all the site names in a city given city and state
  ```python
  curl localhost:5000/location/<state>/<city>
  ```
* To get all information of a FQHC given their phone number:
  ```python
  curl localhost:5000/healthcare/<site_telephone_number>
  ```
* To get relevant information of a site given its name:
  ```python
  curl localhost:5000/sites/<sitename>
  ```
* To get all the site names in a given state:
  ```python
  curl localhost:5000/state/<state_name>
  ```
* To create a job:
   ```python
  curl localhost:5000/jobs -X POST -d {<state_name>}
* To list all jobs on the queue:
   ```python
   curl localhost:5000/jobs
   ```
* To get the results of a job:
    ```python
    curl localhost:5000/results/<jobid>
    ```
  
## Kubernetes Cluster
To set up the cluster, run these commands IN the kubernetes directory:
```python
kubectl apply -f app-prod-api-deployment.yml
kubectl apply -f app-prod-api-ingress.yml
kubectl apply -f app-prod-api-nodeport.yml
kubectl apply -f app-prod-db-deployment.yml
kubectl apply -f app-prod-db-pvc.yml
kubectl apply -f app-prod-db-service.yml
kubectl apply -f app-prod-wrk-deployment.yml
```
Use this command to make sure everything is running properly:
```python
kubectl get pods
```
You shoud see something like this:
```python
NAME                                    READY   STATUS    RESTARTS   AGE
nicoleolv-test-fqhcapi-67b8c5b8d4-hgg8s   1/1     Running   0          7m
nicoleolv-test-fqhcapi-67b8c5b8d4-w5k2r   1/1     Running   0          5m
nicoleolv-test-redis-5678f8fd88-6njcq     1/1     Running   0          4m
py-debug-deployment-f484b4b99-tp6jp     1/1     Running   0          6m
```
Then, use this command to get the service port number:
```python
kubectl get services 
```
You should see something like this:
```python
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
prod-api-nodeport-service   NodePort    10.233.3.111    <none>        5000:30312/TCP   16m
prod-redis-service          ClusterIP   10.233.17.157   <none>        6379/TCP         16m
```
Now that you have the new port service number, edit your `app-prod-api-ingress.yml` with your favorite editor and ingress this number under number: <insert here>
After you have done this, the kubernetes cluster is set up!

## Testing and Running the Kubernetes Cluster
To test the cluster and ensure the Flask api is working as intended, run this command:
```python
kubectl exec -it <py-debug-deployment pod name> -- /bin/bash
```
Now we are inside the pod and the command line should look something like this (we are now in the root):
```python
root@py-debug-deployment-f484b4b99-tprrp:/#
```
Now you can curl the routes, as below, just like in docker, but instead of localhost, we use our prod-api-nodeport-service, like shown below
```python
root@py-debug-deployment-f484b4b99-tprrp:/# curl prod-api-nodeport-service:5000/jobs
```
## Interpreting the Output 
| Route                                   | Method        | Result                                    |
| ----------------------------------------|:-------------:| -----------------------------------------:|
| `/help`                                 | GET           | Returns a string of all possible curls    |
| `/data`                                 | POST          | Posts all the FQHC data to redis          |
| `/data`                                 | GET           | Returns a list of the whole FQHC dat      |
| `/data`                                 | DELETE        | Deltes the FQHC data from redisv          |
| `/program/<sitename>`                   | GET           | Returns a Y (yes) or N (no) to specify if a subprogram grant is offered in given sitename       |
| `/location/<state>/<city>`              | GET           | Returns all the site names in a city, state     |
| `/healthcenter/<site_telephone_number>` | GET           | Returns all the data about the healthcenter     |
| `/sites/<site_name>`                    | GET           | Retirns relevant information about given FQHC name     |
| `/state/<state_name>`                   | GET           | Returns all site names in given state     |
| `/jobs`                                 | POST          | Posts/creates a job      |
| `/jobs`                                 | GET           | Returns all jobs on the queue     |
| `/results/<jobid>`                      | GET           | Returns the results of a job    |
 

## Overview
Overall, this Flask Web Application and use of the Redis Database provides an easy way to analyze this large set of data. Additionally docker and kubernetes facilitate the distribution of our project. The whole data may be returned & may be deleted, or only the data of a specific site given site name may be returned, while also being able to post a job that the worker will perform an analysis on. It returns all this data fast and efficiently with the help of Redis and Flask!  

### Software Diagram
![diagram](https://github.com/nicoleolv/Federally-Qualified-Health-Centers/blob/main/diagram.png)
