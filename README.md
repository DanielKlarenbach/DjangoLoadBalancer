# DjangoLoadBalancer
Package enabling to load balance requests to databases in django projects. It creates a separate process, where all requests to databases from user's app instances are sent. The process creates one thread for every database that was specified in settings.py. Each thread is responsible for managing one database.

## Installation
`pip install djangoloadbalancer`

## How to use
1. Rather than extending models.Model, your models must extend LoadBalancerModel, example:
```python
import django_load_balancer.load_balancer_model
from django.db import models

class Destination(django_load_balancer.load_balancer_model.LoadBalancerModel):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
```

2. Specify load balancer's settings in project's settings.py file, example:
```python
LOAD_BALANCER={
    'CUD_ALGORITHM': 'MULTITHREADING',
    'R_ALGORITHM': {
        'NAME':'ROUND_ROBIN',
    },
    'DATABASES': ['default','DB1','DB2','DB3','DB4'],
    'WAIT_TIME': 2,
    'ADDRESS': {
        'HOST' : 'localhost',
        'PORT' : 6000,
        'AUTHKEY' : 'pass'
    }
}
```
* R_ALGORITHM - algorithm that will determine to which database will be the next READ query sent
    * ROUND_ROBIN - next database for READ query is just the next in list 
    * INTERVAL_TIME - regularly sends queries to databases to determine their response time. This response time is later used to choose database for READ query - the database with the smallest response time will be chosen. Queries to determine response time are send every INTERVAL seconds.
* DATABASES - names of databases from settings.py's DATABASES that will be used for loadbalancing
* WAIT_TIME - amount of time that load balancer will wait to check if the database, that went down, is up
* ADDRESS - address of load balancer process 

3. Add 'django_load_balancer' to INSTALLED_APPS in project's settings before 'django.contrib.staticfiles', example:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_load_balancer',
    'django.contrib.staticfiles',
    'LoadBalancer',
]
```

4. Run djangoloadbalancer.py:
```
user1@user1:~/djangoProject1$ python3 venv/bin/djangoloadbalancer.py
```