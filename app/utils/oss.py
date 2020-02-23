# -*- coding: utf-8 -*-
'''
@author:HanFei
@version: 2019-05-23
@function:
oss接口
'''

import os
import oss2
from . import fileCache


class OssDataProcess(object):
    '''
    以OSS为数据源
    '''

    def __init__(self):
        self.init_oss()
        self.CachePath = fileCache.__path__[0]
        self.ossPre = 'http://contract-spider.oss-cn-beijing.aliyuncs.com'

    def init_oss(self):
        auth = oss2.Auth(os.environ.get('OSS_APPKEY'), os.environ.get('OSS_APPSECRET'))
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        self.bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'contract-spider')

    def getfile_object(self, url):
        # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
        # md5handler = hashlib.md5()
        # md5handler.update(url)
        # _id = md5handler.hexdigest()
        savePath = os.path.join(self.CachePath, '{0}.pdf'.format(url))
        if not os.path.exists(savePath):
            try:
                self.bucket.get_object_to_file(url, savePath)
            except:
                print('Get oss file {0} Error!'.format(url))
                return None

        return savePath

    def upload_file(self, id, input):
        self.bucket.put_object(id, input)


ossHandler = OssDataProcess()