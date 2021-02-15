import inspect
import pickle
from multiprocessing.connection import Client

from django.db import models

from .query import Query, Wait, QueryType


def send_query_to_listener(query):
    from .local_settings import LOAD_BALANCER
    address = (LOAD_BALANCER['ADDRESS']['HOST'], LOAD_BALANCER['ADDRESS']['PORT'])
    connection = Client(address, authkey=bytes(LOAD_BALANCER['ADDRESS']['AUTHKEY'], 'utf-8'))
    payload = pickle.dumps(query)
    connection.send(payload)
    result = pickle.loads(connection.recv())
    connection.send('close')
    connection.close()
    return result


def loadbalance_function(name):
    def loadbalanced_function(self, *args, **kwargs):
        query = Query(Wait.WAIT.value, QueryType.QUERYSET.value, method=name, args=args, kwargs=kwargs, model=self.model)
        result = send_query_to_listener(query)
        return result

    return loadbalanced_function


def load_balance(cls):
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_') and 'alters_data' in dir(method):
            setattr(cls, name, loadbalance_function(name))
    return cls


@load_balance
class LoadBalancerQuerySet(models.QuerySet):
    pass


class BaseLoadBalancerManager(models.Manager):
    def get_queryset(self):
        return LoadBalancerQuerySet(self.model)


class LoadBalancerManager(BaseLoadBalancerManager):
    def __init__(self):
        super(LoadBalancerManager, self).__init__()

    def get_queryset(self):
        query = Query(Wait.DONT_WAIT.value, QueryType.NO_QUERYSET.value, method='get_queryset', model=self.model)
        result = send_query_to_listener(query)
        return result


class LoadBalancerModel(models.Model):
    models_manager = models.Manager()
    loadbalancer_base_manager = BaseLoadBalancerManager()
    objects = LoadBalancerManager()

    def save(self, *args, **kwargs):
        query = Query(wait=Wait.WAIT.value, type=QueryType.NO_QUERYSET.value, method='save', model=self, args=args, kwargs=kwargs)
        result = send_query_to_listener(query)
        return result

    def delete(self, *args, **kwargs):
        query = Query(wait=Wait.WAIT.value, type=QueryType.NO_QUERYSET.value, method='delete', model=self, args=args, kwargs=kwargs)
        result = send_query_to_listener(query)
        return result

    class Meta:
        abstract = True
