#coding=utf-8

import os
import hashlib
import urllib.request

from app import logger

log = logger.getLogger(__name__)

class ResourceManager:
    '''
    Manager for bandwidth consuming resources.
    Get resources through memory, disk, Internet in turn.
    '''
    # TODO: improve network module performance
    
    def __init__(self, path, proxy={}):
        self.path = path
        try:
            os.makedirs(self.path)
        except:
            pass
        self.resource = {}
        
        # Make a copy of proxy dict
        self.setProxy(dict(proxy))
        
    def setProxy(self, proxy={}):
        for k,v in proxy.items():
            if not v.startswith('http'):
                proxy[k] = ''.join(('http://', v))
        self.opener = urllib.request.URLopener(proxy)
        
    def get(self, url, report_hook=None):
        '''
        Get resource specified by url.
        @param url: string.
        @return: string. Absolute file path of resource.
        '''
        
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        
        # Resource in memory
        if url_hash in self.resource:
            #log.debug('Found in memory')
            return self.resource[url_hash]
        
        # Resource in disk
        abs_path = os.path.join(self.path, url_hash)
        if os.path.exists(abs_path):
            #log.debug('Found in disk')
            #res = QImage(abs_path, imghdr.what(abs_path))
            self.resource[url_hash] = abs_path
            return abs_path
        
        # Resource from Internet
        #log.debug('Found from Internet')
        self.opener.retrieve(url, abs_path, report_hook)
        #res = QImage(abs_path, imghdr.what(abs_path))
        self.resource[url_hash] = abs_path
        return abs_path