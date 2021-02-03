import inspect

from django.db import models

from .LoadBalancerFactory import LoadBalancerFactory
from .Query import Query, Wait, QueryType

load_balancer=LoadBalancerFactory.create_load_balancer()

def make_f(method,name):
    def new_function(self, *args, **kwargs):
        return load_balancer.run_query(Query(Wait.WAIT, QueryType.QUERYSET, method=name, args=args, kwargs=kwargs, model=self.model))
    return new_function

def load_balance(cls):
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_') and 'alters_data' in dir(method):
            setattr(cls, name, make_f(method,name))
    return cls


@load_balance
class LoadBalancerQuerySet(models.QuerySet):
    pass

class BaseLoadBalancerManager(models.Manager):
    def get_queryset(self):
        return LoadBalancerQuerySet(self.model)

class LoadBalancerManager(BaseLoadBalancerManager):
    def __init__(self, load_balancer):
        super(LoadBalancerManager, self).__init__()
        self.load_balancer = load_balancer

    def get_queryset(self):
        return self.load_balancer.run_query(Query(Wait.DONT_WAIT, QueryType.NO_QUERYSET, super().get_queryset))

class LoadBalancerModel(models.Model):
    helper = models.Manager()
    load_balancer = load_balancer
    objects = LoadBalancerManager(load_balancer)

    def save(self, *args, **kwargs):
        self.load_balancer.run_query(Query(Wait.WAIT, QueryType.NO_QUERYSET, super().save, args, kwargs))

    def delete(self, *args, **kwargs):
        self.load_balancer.run_query(Query(Wait.WAIT, QueryType.NO_QUERYSET, super().delete, args, kwargs))

    class Meta:
        abstract = True