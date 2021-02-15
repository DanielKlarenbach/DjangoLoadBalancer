# DjangoLoadBalancer
Package enabling to load balance requests to databases in django projects.

## Instalation
`pip install djangoloadbalancer`

## How to use
1. Rather than extending models.Model, your models must extend LoadBalancerModel, example:
```python
from django.db import models
from DjangoLoadBalancer.django_load_balancer import load_balancer_model

class Destination(load_balancer_model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
```

2. Specify load balancer's settings in project's settings.py file, examples:
```python
LOAD_BALANCER={
    'CUD_ALGORITHM': 'MULTITHREADING',
    'R_ALGORITHM': {
        'NAME':'ROUND_ROBIN',
    },
    'DATABASES': ['default','DB1','DB2'],
    'WAIT_TIME': 10,
}
```
```python
LOAD_BALANCER={
    'CUD_ALGORITHM': 'MULTITHREADING',
    'R_ALGORITHM': {
        'NAME':'INTERVAL_TIME',
        'INTERVAL' : 5
    },
    'DATABASES': ['default','DB1','DB2'],
    'WAIT_TIME': 10,
}
```
* R_ALGORITHM - algorithm that will determine to which database will be the next READ query sent
    * ROUND_ROBIN - next database for READ query is just the next in list 
    * INTERVAL_TIME - regularly sends queries to databases to determine their response time. This response time is later used to choose database for READ query - the database with the smallest response time will be chosen. Queries to determine response time are send every INTERVAL seconds.
* DATABASES - names of databases from settings.py's DATABASES that will be used for loadbalancing
* WAIT_TIME - amount of time that load balancer will wait to check if the database, that went down, is up