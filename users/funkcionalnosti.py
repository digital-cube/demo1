
import redis

def f1():
    r = redis.Redis()
    r.set('test', 'dada')


def f2():
    r = redis.Redis()
    return r.get('test')
