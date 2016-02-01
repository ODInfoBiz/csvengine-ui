'''
Created on Dec 7, 2015

@author: jumbrich
'''

import hashlib
import requests
from StringIO import  StringIO
import os
import urllib
import urlnorm
from werkzeug.exceptions import RequestEntityTooLarge

from pyyacp.yacp import YACParser

from csvengine.utils import assure_path_exists

import structlog
log =structlog.get_logger()


class DataCache(object):

    DB="db"
    WEB="web"
    TMP="tmp"

    def __init__(self, config, max_file_size):
        self.submit_folder = {
            DataCache.WEB: assure_path_exists(config['web_submit']),
            DataCache.DB: assure_path_exists(config['db_submit']),
            DataCache.TMP: assure_path_exists(config['tmp_submit'])
        }
        self.cleaned_folder = {
            DataCache.WEB: assure_path_exists(config['web_cleaned']),
            DataCache.DB: assure_path_exists(config['db_cleaned']),
            DataCache.TMP: assure_path_exists(config['tmp_cleaned'])
        }

        self.max_file_size = max_file_size

    def submitToWeb(self, file=None, url=None, content=None):
        return self.submit(file=file, url=url, content=content, toFolder=DataCache.WEB)

    def submitToTmp(self, file=None, url=None, content=None):
        return self.submit(file=file, url=url, content=content, toFolder=DataCache.TMP)

    def submitToDB(self, file=None, url=None, content=None):
        return self.submit(file=file, url=url, content=content, toFolder=DataCache.DB)


    def submit(self, file=None, url=None, content=None, toFolder=None):
        """
        1) retrieve and compute hash of original content

        2) store submitted content using hash as filename IFF not exist
            optional URL as symlink

        :param file:
        :param url:
        :param content:
        :param toFolder:
        :return: the md5 of the original file
        """
        if toFolder in self.submit_folder and toFolder in self.cleaned_folder:
            s_folder = self.submit_folder[toFolder]
            c_folder = self.cleaned_folder[toFolder]
        else:
            return None

        if file:
            md5 = storeFile(file, s_folder)
        elif url:
            md5 = storeURL(url, s_folder, max_file_size=self.max_file_size)
        elif content:
            md5 = storeContent(content, s_folder)
        else:
            return None

        # check if cleaned exists
        submitted_path=os.path.join(s_folder, md5)
        cleaned_path = os.path.join(c_folder, md5)
        # at first look for stored cleaned version
        if os.path.exists(cleaned_path):
            return md5
        else:
            # generate and store cleaned version
            table = YACParser(filename=submitted_path)
            cleaned = table.generate()
            storeContent(cleaned, c_folder, md5=md5)
            return md5


    def getParser(self, fileHash, folder=None, original=False):
        """
        returns a parser and stores cleaned file if not already available
        """
        if folder:
            file_path = os.path.join(folder, fileHash)
            if os.path.exists(file_path):
                if folder in self.cleaned_folder.values():
                    return YACParser(filename=file_path, skip_guess_encoding=True)
                else:
                    return YACParser(filename=file_path)
        else:
            if not original:
                for f in self.cleaned_folder:
                    cleaned_path = os.path.join(self.cleaned_folder[f], fileHash)
                    if os.path.exists(cleaned_path):
                        return YACParser(filename=cleaned_path, skip_guess_encoding=True)

            for f in self.submit_folder:
                submit_path = os.path.join(self.submit_folder[f], fileHash)
                cleaned_path = os.path.join(self.cleaned_folder[f], fileHash)
                if os.path.exists(submit_path):
                    table = YACParser(filename=submit_path)
                    if not os.path.exists(cleaned_path):
                        cleaned = table.generate()
                        storeContent(cleaned, cleaned_path, md5=fileHash)
                    return table
        return None

    def exists(self, fileHash):
        for f in self.cleaned_folder:
            cleaned_path = os.path.join(self.cleaned_folder[f], fileHash)
            if os.path.exists(cleaned_path):
                return True
        return False

    def getSubmit(self, fileHash, folder=False):
        if folder:
            submit_file = getFileContent(fileHash, self.submit_folder[folder])
            if submit_file:
                return submit_file
        else:
            for f in self.submit_folder:
                submit_file = getFileContent(fileHash, self.submit_folder[f])
                if submit_file:
                    return submit_file
        return None


    def getFileName(self, url, folder=None):
        url_norm = urlnorm.norm(url.strip())
        url_fname = urllib.quote_plus(url_norm)
        if folder:
            submit_path = os.path.join(self.submit_folder[folder], url_fname)
            if os.path.exists(submit_path):
                return os.readlink(submit_path)
        else:
            for f in self.submit_folder:
                submit_path = os.path.join(self.submit_folder[f], url_fname)
                if os.path.exists(submit_path):
                    return os.readlink(submit_path)
        return None

def getFileContent(fileID, path=None):
    if path:
        fileID = os.path.join(path,fileID)
    if not os.path.exists(fileID):
        return None
    with open(fileID) as f:
        return f.read()


def getFileName(url, path):
    url_norm = urlnorm.norm(url.strip())
    url_fname = urllib.quote_plus(url_norm)
    f=os.path.join(path,url_fname)
    return os.readlink(f)

def getURLContent(url, path):
    with open(getFileName(url, path)) as f:
        return f.read()

def storeFile(f, path):
    c = f.read()
    md5 = hashlib.md5(c).hexdigest()
    
    fpath = os.path.join(path, md5)
    log.debug("storing file", file=fpath)
    with open(fpath,'w') as f:
        f.write(c)
    log.info("file stored", file=fpath)
    return md5

def storeContent(content, path, md5=None):
    if not md5:
        md5 = hashlib.md5(content).hexdigest()

    fpath = os.path.join(path, md5)
    log.debug("storing content", file=fpath)
    with open(fpath,'w') as f:
        f.write(content)

    log.info("content stored", file=fpath)
    return md5

def storeURL(url, path, max_file_size):
    #download URL and send fileID
    log.debug("downloading url", url=url, max_file_size=max_file_size )
    try:
        r = requests.get(url, stream=True)
        size = 0
        ctt = StringIO()
    
        sig = hashlib.md5()
        for chunk in r.iter_content(2048):
            size += len(chunk)
            ctt.write(chunk)
            sig.update(chunk)
            if size >  max_file_size:
                r.close()
                raise RequestEntityTooLarge()
    
        md5 = sig.hexdigest()
        ctt.seek(0)
        
        fpath=os.path.join(path, md5)
        if os.path.exists(fpath):
            print 'file exists', fpath
            return md5
        log.debug("storing url", url=url, file=fpath)
        with open (fpath,'w') as fd:
            t = ctt.read(1048576)
            while t:
                fd.write(t)
                t = ctt.read(1048576)
        
        url_norm = urlnorm.norm(url.strip())
        url_fname = urllib.quote_plus(url_norm)
        f = os.path.join(path, url_fname)

        
        os.symlink(fpath,f)
        log.debug("url stored", url=url, file=fpath)
        
        return md5
    except Exception as e:
        raise e