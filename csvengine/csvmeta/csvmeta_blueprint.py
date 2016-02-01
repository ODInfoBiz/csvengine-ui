'''
Created on Dec 24, 2015

@author: jumbrich
'''

from flask import Blueprint, render_template,current_app

from flask import Flask, request, redirect, url_for


from werkzeug.exceptions import RequestEntityTooLarge

from csvengine.datacache.error_handler import ErrorHandler as eh

import structlog
from csvengine.data_cache import DataCache
from csvengine.csvmeta.csvw_json import CSVMCreator
from flask.json import jsonify
log =structlog.get_logger()


csvm_bp = Blueprint('csvm', __name__,
                    template_folder='templates',
                    static_folder='static',
                    )


def decode_utf8(string):
    if isinstance(string, str):
        for encoding in (('utf-8',), ('windows-1252',), ('utf-8', 'ignore')):
            try:
                return string.decode(*encoding)
            except:
                pass
        return string # Don't know how to handle it...
    return unicode(string, 'utf-8')

def my_render_template(templ, **kwargs):
    return render_template(templ,  navigation_bar=current_app.config['navigation_bar'], **kwargs)

@csvm_bp.route('/csvm/editor/service')
def csvmeditor_service():
    fileID = request.args.get("fileID")
    url = request.args.get("url")

    datacache = current_app.config['DATACACHE']
    
    # TODO use URL for getting file
    if not fileID and url:
        fileID = datacache.getFileName(url)
    if not fileID:
        data={
              "message": 'Arguments missing: fileID required',
              'title':"Input Error",
              'exception': "",
              "filename": "No CSV file specified"
        }
        return render_template("input_error.html", **data)

    # current_app.logger.debug("Reading "+fileID+" from disk:"+datacache.submit_folder[folder])
    # table = datacache.getParser(fileID,folder=datacache.submit_folder[folder])
    current_app.logger.debug("Reading "+fileID+" from disk")
    table = datacache.getParser(fileID, original=True)

    title = url if url else fileID
    original = datacache.getSubmit(fileID)
    rows = len(original.split('\n'))
    results={ 'orig': decode_utf8(original), 'table': table.__dict__, 'title': title, 'cols': table.columns, 'rows': rows}

    #d= decode_utf8(data)
    #results={'orig':decode_utf8(original),'cleaned': table.generate().decode('utf-8'), 'table':table.__dict__}

    import datetime
    #sets the variable "today" as the datetime object.
    
    today = datetime.datetime.today()
    results['time']=today.strftime('%Y-%m-%d')
    if url:
        results['url']=url
    return my_render_template("csvm_editor_result.html", data=results)

@csvm_bp.route('/createcsvm', methods=['POST'])
def createcsvm_service():
    meta= CSVMCreator.create(request.form)
    resp = jsonify(meta)
    resp.status_code = 200
    return resp
    
@csvm_bp.route("/csvm/editor")
def csvmeditor():
    return my_render_template("csvm_editor.html")



@csvm_bp.route("/csvm/validator")
def csvmval():
    return my_render_template("csvm_val.html")

