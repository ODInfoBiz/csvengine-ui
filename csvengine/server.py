# -*- coding: utf-8 -*-
'''
Created on Dec 2, 2015

@author: jumbrich
'''
#!flask/bin/python



#from csvengine.csvengine_blueprint import ui
#from csvengine.api_blueprint import api

from flask import render_template, Flask

from csvengine.datacache.error_handler import ErrorHandler as eh, ErrorHandler
from csvengine import utils, data_cache


import structlog
import argparse
from csvengine.csv_blueprint import csvb
from csvengine.datacache.datacache_blueprint import datacache_bp
from csvengine.csvmeta.csvmeta_blueprint import csvm_bp
log =structlog.get_logger()



app = Flask(__name__)


def my_render_template(templ, **kwargs):
    return render_template(templ,  navigation_bar=app.config['navigation_bar'], **kwargs)

@app.route("/csvengine/")
def index():
    return my_render_template("index.html")


@app.route("/csvengine/privacy")
def privacy():
    return my_render_template("privacy.html")

@app.route("/csvengine/about")
def about():
    return my_render_template("about.html")



import logging

def parseArgs():
    pa = argparse.ArgumentParser(description='CSVEngine UI', prog='csvengine')
    
    logg=pa.add_argument_group("Logging")
    logg.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    logg.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )
    
    pa.add_argument('-c','--config', help="config file", dest='config')
    pa.add_argument('-p','--port', help="Set port of UI (default is 2340)", type=int, dest='port', default=2340)
    
    return pa.parse_args()

def parseServices():
    return [ ('index', 'index', 'Info'),
             ('csv.csvclean', 'csvclean', 'CSV Clean'),
             ('csvm.csvmeditor', 'csvm.createcsvm', 'CSV MetaData Editor'),
             ('about', 'about', 'About')
            ]


def start():
    args= parseArgs()
    print 'args',args
    try:
        config = utils.load_config(args.config)
    except Exception as e:
        ErrorHandler.DEBUG=True
        eh.handleError(log,"Exception during config initialisation", exception=e)
        return 
    
    #setup the data cache for storing uploaded files
    maxFileSize=config['ui']['maxFileSize']
    datacache = data_cache.DataCache(config['data'], maxFileSize)
    app.config['DATACACHE'] = datacache

    #get the port
    port=config['ui']['port']
    if args.port:
        #cli argument overwrites config port
        port = args.port


    log.info('Starting CSVEngine on http://localhost:{}/'.format(port))

    app.config['MAX_CONTENT_LENGTH'] = maxFileSize
    app.config['navigation_bar'] = parseServices()
    
    app.register_blueprint(csvb, url_prefix='/csvengine')
    app.register_blueprint(datacache_bp,url_prefix='/csvengine')
    app.register_blueprint(csvm_bp,url_prefix='/csvengine')
    
    
    app.run(debug=True, port=port)

if __name__ == "__main__":
    start()