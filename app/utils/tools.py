# -*- coding: utf-8 -*-
'''
通用工具和对象
created by hanfei on 17/8/23
'''
import hashlib
import time,datetime
import json
import math
from Crypto.Cipher import DES,AES
from binascii import b2a_hex, a2b_hex
import numpy as np


BS = 16
PKCS5Padding_pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
PKCS5Padding_unpad = lambda s : s[0:-ord(s[-1])]


def get_md5(data):
    if isinstance(data, str):
        encrypt_data = data.encode('utf-8')
    elif isinstance(data, bytes):
        encrypt_data = data
    else:
        return None

    return hashlib.md5(encrypt_data).hexdigest().upper()


class TokenCryptor(object):

    passphrase = '_(&%#!_L'
    iv = "1234567890123456"
    padding = '\0'
    length = 16

    def encrypt(self,text):
        t = hashlib.md5(text).hexdigest()
        print('md5:',t)
        return self.aes_encrypt(t)

    def aes_encrypt(self,text):
        aes = AES.new(self.passphrase, AES.MODE_ECB, self.iv)
        #补位
        if len(text)%self.length!=0:
            text += (self.length-len(text)%self.length) * self.padding
            print('do padding!',len(text))

        ciphertext = aes.encrypt(text)
        return b2a_hex(ciphertext)

    def des_encrypt(self,text):
        des = DES.new(self.passphrase, DES.MODE_ECB, self.iv)
        #补位
        if len(text)%self.length!=0:
            text += (self.length-len(text)%self.length) * self.padding
        ciphertext = des.encrypt(text)
        return b2a_hex(ciphertext)

    def des_decrypt(self,encrypted):
        des = DES.new(self.passphrase, DES.MODE_ECB, self.iv)
        return des.decrypt( a2b_hex(encrypted) )


class ToolsException(Exception):pass


'''
-------------------------------------------------------------------------------------------------------
时间字符串转换
-------------------------------------------------------------------------------------------------------
'''


def datetime2str(t=None, format='%Y-%m-%d %H:%M:%S'):
    '''
    将数据转换为字符串形式
    :param t:  datetime 格式时间； int 长度10 秒时间戳格式， int 长度13 毫秒时间戳
    :param format:
    :return:
    '''
    if t is None:
        return datetime.datetime.now().strftime(format)

    if isinstance(t, datetime.datetime):
        return t.strftime(format)
    elif isinstance(t, int):
        if len(str(t)) == 10:
            return datetime.datetime.fromtimestamp(t).strftime(format)
        elif len(str(t)) == 13:
            return datetime.datetime.fromtimestamp(t//1000).strftime(format)
        else:
            return None


def str2datetime(tstr, format='%Y-%m-%d %H:%M:%S'):
    '''
    字符串为datetime格式
    :param tstr:  时间的字符串
    :param format:
    :return:
    '''
    if tstr is None:
        return datetime.datetime.strptime("1970-01-01 00:00:00", format)
    elif isinstance(tstr, str):
        return datetime.datetime.strptime(tstr, format)


'''
-------------------------------------------------------------------------------------------------------
时间字符串---间隔转换
-------------------------------------------------------------------------------------------------------
'''


def humanread_date(timestr):
    if timestr == None:
        return u"Null"
    d = datetime.datetime.strptime(timestr, "%Y-%m-%d")
    now = datetime.datetime.now()
    dist = now - d

    if dist.days == 0:
        return u'今天'
    elif dist.days == 1:
        return u'昨天'
    elif dist.days == 2:
        return u'前天'
    else:
        return u'{0}天前'.format(dist.days)


def humanread_time(t):
    if t is None:
        return u"Null"
    if isinstance(t, datetime.datetime):
        d = t
    elif isinstance(t, int):
        d = datetime.datetime.fromtimestamp(t/1000)
    else:
        raise ToolsException(u"unknown time type:%s" %(type(t)))

    now = datetime.datetime.now()
    dist = now - d
    #当天
    if dist.days==0:
        if dist.seconds <= 60:
            return u'1分钟内'
        elif dist.seconds <= 60*60:
            return u'{0}分钟前'.format(int(math.ceil(dist.seconds/60)))
        else:
            return u'{0}小时前'.format(int(math.ceil(dist.seconds/3600)))
    elif dist.days < 0:
        return u'刚才'
    else:
        return d.strftime(u"%Y-%m-%d %H:%M")


def humanread_timelong(sec):
    ds = int(sec)
    print('time long diff',sec)
    if ds < 60:
        return u'%d秒前'.format(ds)
    elif ds < 3600:
        return u'{0}分{1}秒前'.format(int(math.floor(ds/60)), int(ds % 60))
    else:
        return u'{0}小时{1}分{2}秒前'.format(int(math.floor(ds/3600)), int(math.floor(ds % 3600/60)), int(ds % 60))


def get_pretty_print(obj):
    if isinstance(obj,dict):
        return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    else:
        return obj


def dict_obj_to_str(result_dict):
    """把字典里面的bytes和datetime对象转成字符串，使json转换不出错"""
    if result_dict:
        for k, v in result_dict.items():
            if isinstance(v, bytes):
                result_dict[k] = str(v, encoding='utf-8')
            if isinstance(v, datetime.datetime):
                result_dict[k] = time.mktime(v.timetuple()) * 1000
    return result_dict


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8');
        return json.JSONEncoder.default(self, obj)


