# -*- coding: utf-8 -*-
'''
数据库操作的基础
created by HanFei on 20/2/22
'''
import os
import threading

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from pymongo import MongoClient

from utils.parse_dburi import parse_db_str
from utils.tools import dict_obj_to_str


# Mysql的操作句柄
class MySQLDB:
    
    _instance_lock = threading.Lock()
    _instance = {}
    _firstinit = {}

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if args[0] not in cls._instance:
                cls._instance[args[0]] = super(MySQLDB, cls).__new__(cls)
            return cls._instance[args[0]]

    def __init__(self, mysql_uri):
        if mysql_uri not in MySQLDB._firstinit:
            mysql_config = parse_db_str(os.environ.get(mysql_uri))
            self.__pool = PooledDB(
                creator=MySQLdb, mincached=1, maxcached=20,
                host=mysql_config['host'], port=mysql_config['port'], user=mysql_config['user'],
                passwd=mysql_config['passwd'],
                db=mysql_config['db'], use_unicode=False, charset='utf8', 
                cursorclass=DictCursor
            )
            
            MySQLDB._firstinit[mysql_uri] = True
            
    def get_db(self):
        db = self.__pool.connection()
        return (db, db.cursor())
        

class MySQLBase(object):

    _db_uri = 'MYSQL_URI'

    def __init__(self):
        self.db, self.cursor = MySQLDB(self._db_uri).get_db()


# Mongo的操作句柄
class MongoDB():

    _instance_lock = threading.Lock()
    _instance = {}
    _firstinit = {}

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if args[0] not in cls._instance:
                cls._instance[args[0]] = super(MongoDB, cls).__new__(cls)
        return cls._instance[args[0]]

    def __init__(self, mongo_uri):
        if mongo_uri not in MongoDB._firstinit:
            if not mongo_uri:
                print('Can\'t get the MongolUri: {0}'.format(mongo_uri))
            self.mc = MongoClient(os.environ.get(mongo_uri), maxPoolSize=2000)
            mongo_config = parse_db_str(os.environ.get(mongo_uri))
            self.db = self.mc.get_database(mongo_config['db'])

            MongoDB._firstinit[mongo_uri] = True

    def get_db(self):
        '''
        '''
        return self.db


class MongoDBCollection(object):

    _db_uri = 'MONGO_URI'
    _collection = None

    def __init__(self):
        self.db = MongoDB(self._db_uri).get_db()
        
        if self._collection:
            self.coll = self.db[self._collection]