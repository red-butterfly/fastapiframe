# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-06-15
@function:
cache frame
'''
import os
import json
import threading
from utils.parse_dburi import parse_db_str


class CacheDecorator(object):

    def __init__(self):
        self.cache = None
        self.lastkey = None

    def is_enable(self):
        return self.cache is not None

    def set(self, key, value, expire=3600):
        """
        用于添加或者更新缓存
        :param key:
        :param value:
        :param expire: 过期时间
        :return:
        """
        raise NotImplementedError()

    def get(self, key):
        """
        获取缓存数据
        :param key:
        :return: 缓存中的数据
        """
        raise NotImplementedError()

    def delete(self, key):
        """
        删除key对应的缓存
        :param key:
        :return:
        """
        raise NotImplementedError()


class CacheDB(object):
    
    _instance_lock = threading.Lock()
    _instance = {}
    _firstinit = {}

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if args[0] not in cls._instance:
                cls._instance[args[0]] = super(CacheDB, cls).__new__(cls)
        return cls._instance[args[0]]

    def __init__(self, cache_uri, ctype):
        if cache_uri not in CacheDB._firstinit:
            if not cache_uri:
                print('Can\'t get the CachelUri: {0}'.format(cache_uri))
            if ctype == 'redis':
                import redis
                redis_config = parse_db_str(os.getenv(cache_uri, None))
                _redis_config = {k: redis_config[k] for k in ['host', 'port', 'db'] if k in redis_config}
                if 'passwd' in redis_config:
                    _redis_config['password'] = redis_config['passwd']
                self.pool = redis.ConnectionPool(**_redis_config)
                self.cache = redis.Redis(connection_pool=self.pool)

                CacheDB._firstinit[cache_uri] = True
            elif ctype == 'memcache':
                import memcache
                self.cache = memcache.Client([os.environ.get(cache_uri)], debug=True)
                CacheDB._firstinit[cache_uri] = True
    
    def get_cache(self):
        return self.cache


class RedisCache(CacheDecorator):

    _db_uri = 'CACHE_REDIS_URI'

    def __init__(self):
        super(RedisCache, self).__init__()
        self.cache = CacheDB(self._db_uri, 'redis').get_cache()

    def get(self, key):
        value = self.cache.get(key)
        try:
            value = json.loads(value)
        except:
            return None

        # print("redis get:", key, value)
        return value 

    def set(self, key, value, expire=None):
        if isinstance(value, (dict, set, list)):
            result = json.dumps(value)
        else:
            result = str(value)

        if expire:
            self.cache.set(key, result, int(expire))
        else:
            self.cache.set(key, result)
        # print("redis set:", key, result, expire)

    def delete(self, key):
        if self.cache.exists(key):
            self.cache.delete(key)

    def exists(self, key):
        return self.cache.exists(key)


class MemCache(CacheDecorator):

    _db_uri = 'CACHE_MEMCACHE_URI'

    def __init__(self):
        super(MemCache, self).__init__()
        self.cache = CacheDB(self._db_uri, 'memcache').get_cache()

    def get(self, key):
        if self.cache :
            self.lastkey = key
            return self.cache.get(key)
        return None

    def set(self, key, data, expire=3600):
        if self.cache:
            print('saving cache ... %s timeout_hours=%d' %(key, expire))
            self.lastkey = key
            return self.cache.set(key, data, expire)
        return None

    def set_multi(self, key, data, expire=3600):
        if self.cache:
            print('saving cache ... %s timeout_hours=%d' %(key, expire))
            self.lastkey = key
            return self.cache.set_multi(key, data, expire)
        return None

    def delete(self, key):
        self.cache.delete(key)