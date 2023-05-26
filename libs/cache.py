import datetime as dt
import pydash as py_

# import pickle
from bson import json_util

from functools import wraps


class BaseCache(object):
    def __init__(self):
        self.DEFAULT_TIMEOUT = 3600

    def get(self, key):
        pass

    def set(self, key, value, timeout):
        pass

    def flush(self, key):
        pass


class RamCache(BaseCache):
    """
    Implement Ramcache
    Author: Whoiskp 

    Args:
        BaseCache (class): 
    """

    def __init__(self):
        super(RamCache, self).__init__()
        self.CACHE_STORED = {}
        self.KEY_VALUE = 'value'
        self.KEY_EXPRIED = 'expried'

    def set(self, key, value, timeout=0):
        timeout = timeout or self.DEFAULT_TIMEOUT

        self.CACHE_STORED[key] = {
            self.KEY_VALUE: value,
            self.KEY_EXPRIED: dt.datetime.utcnow() + dt.timedelta(seconds=timeout)
        }

    def get(self, key):
        print("RAM CACHE", key)
        obj = self.CACHE_STORED.get(key)
        if obj and dt.datetime.utcnow() < obj.get(self.KEY_EXPRIED):
            return obj.get(self.KEY_VALUE)
        return None

    def flush(self, key):
        if py_.get(self.CACHE_STORED, key):
            del self.CACHE_STORED[key]


class RedisCache(BaseCache):
    """
    Implement Redis Cache for multi Server use redis as instance
    Author: Whoiskp

    Args:
        BaseCache (class)
    """

    def __init__(self, redis):
        super(RedisCache, self).__init__()
        self.redis = redis

    def get(self, key):
        # print("REDIS CACHE", key)
        res = self.redis.get(key)
        return json_util.loads(res) if res else None

    def set(self, key, value, timeout=-1):
        if timeout < 0:
            timeout = self.DEFAULT_TIMEOUT

        value = json_util.dumps(value)
        if timeout > 0:
            self.redis.setex(key, timeout, value)
        else:
            self.redis.set(key, value)

    def flush(self, key):
        self.redis.delete(key)


class CacheFactory(object):
    def get_cache(self, cache_type, instance=None):
        """
        This implement Factory Pattern
        Author: Whoiskp

        Args:
            cache_type (str): redis | ram | file.
            instance ([type], optional): instance for init. Defaults to None.
                - redis with RedisCache.
                - path_dir with FileSystemCache.

        Raises:
            Exception: Not found with your cache type

        Returns:
            [BaseCache]: Cache Instance - Singleton Pattern
        """
        if cache_type == 'redis':
            return self._get_instance_redis(instance)
        if cache_type == 'ram':
            return self._get_instance_ramcache()

        raise Exception('Not found your Cache Type!')


    def _get_instance_redis(self, redis):
        if not py_.get(self, 'redis'):
            self.redis = RedisCache(redis)
        return self.redis


    def _get_instance_ramcache(self):
        if not py_.get(self, 'ram_cache'):
            self.ram_cache = RamCache()
        return self.ram_cache


    ## decorators cache
    def get_cache_key(self, *args, **kwargs):
        key = ""
        # First args
        for i in args:
            if isinstance(i, type):
                continue
            key += ":%s" % i

        # Attach any kwargs
        for k in sorted(kwargs):
            key += ":{}|{}".format(k, kwargs[k])
        return key


    def cache_function(self, icache, timeout=300, key_prefix='common'):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                key = "%s:%s%s" % (key_prefix, f.__name__,
                                self.get_cache_key(*args, **kwargs))
                value = icache.get(key)
                if not value:
                    value = f(*args, **kwargs)
                    icache.set(key, value, timeout)
                return py_.clone(value)
            return wrapper
        return decorator


    def ram_cache_function(self, timeout=300, key_prefix='common'):
        icache = self.get_cache('ram')
        return self.cache_function(icache, timeout, key_prefix)


    def redis_cache_funtion(self, timeout=300, key_prefix='common'):
        icache = self.get_cache('redis')
        return self.cache_function(icache, timeout, key_prefix)

