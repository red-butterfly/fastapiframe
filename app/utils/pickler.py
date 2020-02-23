# -*- coding: utf-8 -*-
'''
pickle的封装
created by HanFei on 19/2/28
'''
import os
import pickle


def _get_save_path(filename):
    if filename.endswith('.pkl'):
        return filename
    else:
        return os.path.join(os.environ.get('HOST_PATH'), '{0}.pkl'.format(filename))


def pickle_dump(data, filename):
    '''
    使用pickle保存变量
    '''

    with open(_get_save_path(filename), 'wb') as f:
        pickle.dump(data, f)


def pickle_load(filename):
    '''
    使用pickle加载数据
    '''
    if os.path.exists(_get_save_path(filename)):
        with open(_get_save_path(filename), 'rb') as f:
            return pickle.load(f)
    else:
        return None