'''
Created on Dec 24, 2015

@author: jumbrich
'''

from flask import Blueprint, render_template,current_app

from flask import request, redirect, url_for

from werkzeug.exceptions import RequestEntityTooLarge

from csvengine.datacache.error_handler import ErrorHandler as eh

import structlog
from flask.helpers import make_response


log =structlog.get_logger()


datacache_bp = Blueprint('datacache', __name__,
                    template_folder='templates',
                    static_folder='static',
                    )


### HELPER FUNCTIONS
####################
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def decode_utf8(string):
    if isinstance(string, str):
        for encoding in (('utf-8',), ('windows-1252',), ('utf-8', 'ignore')):
            try:
                return string.decode(*encoding)
            except:
                pass
        return string # Don't know how to handle it...
    return unicode(string, 'utf-8')


### SUBMIT 
##########
@datacache_bp.route('/submit', methods=['POST'])
def submit():
    file, url, filename = None, None, ''
    try:
        #debug print
        current_app.logger.debug(request.form)
        service = request.form.get('service')

        ### CHECK INPUT PARAMETERS
        ###########################
        
        #check for url
        url = request.form.get('url')

        #check for file uploads
        file = request.files['uploadBtn']
        fileID = request.form.get('fileID')
        if file and file.filename != '':
            filename = file.filename
        elif url:
            filename = url
        else:
            filename = fileID

        #check for copy paste
        textUpload = request.form.get('textUpload')

        #debug
        #current_app.logger.debug('textUpload:'+textUpload+" url:"+url+" fileID:"+fileID+" file:"+file.filename)

        # don't store data checkbox
        store_data = 'check' not in request.form

        datacache = current_app.config['DATACACHE']

        # error handling
        if file and not allowed_file(file.filename):
            data={
              "message":'"'+filename+'" is not a valid filename.',
              'title':"Format Error",
              'exception': ValueError.__class__.__name__,
              "filename": filename
              }
            
            return render_template("input_error.html", **data)
        if fileID:
            if not datacache.exists(fileID):
                data={
                      "message":"Unfortunately we cannot find your file with the ID "+fileID+". Please re-submit the file or URL.",
                      'title':"File not found",
                      'exception': ValueError.__class__.__name__,
                      "filename": filename
                      }
                return render_template("input_error.html", **data)

        if url or (file and file.filename != '') or textUpload:
            # store content in web or tmp folder
            if store_data:
                fileID = datacache.submitToWeb(file=file, url=url, content=textUpload)
            else:
                fileID = datacache.submitToTmp(file=file, url=url, content=textUpload)
            # set parameter in URL
            if url and fileID:
                return redirect(url_for(service, url=url, fileID=fileID))
            else:
                return redirect(url_for(service, fileID=fileID))

        # error if no input is specified
        data={
              "message": 'Arguments missing: fileID or url required',
              'title':"Input Error",
              'exception': "",
              "filename": "No CSV file specified"
        }
        return render_template("input_error.html", **data)

    except RequestEntityTooLarge as e:
        max_in_mb = current_app.config['MAX_CONTENT_LENGTH']/1000000.0
        data={
              "message":'The file '+filename+' exceeds the capacity limit of '+str(max_in_mb)+' MB.',
              'title':"Input File Too Large",
              'exception': e.__class__.__name__,
              "filename": filename
        }
        return render_template("input_error.html", **data)
    except Exception as e:
        eh.handleError(log, "Error", exception=e)
        
        data={
              "message":e.message,
              'title':"Submit Error",
              'exception': e.__class__.__name__,
              "filename": filename
        }
        return render_template("input_error.html", **data )

### method for downloading CSV file
@datacache_bp.route('/get/cleaned', methods=['GET', 'POST'])
def get_cleand_file():
    fileID = request.args.get("fileID")
    url = request.args.get("url")
    
    datacache = current_app.config['DATACACHE']
    
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
    
    table = datacache.getParser(fileID)
    
    output = make_response(table.generate())
    output.headers["Content-Disposition"] = "attachment; filename="+fileID+".csv"
    output.headers["Content-type"] = "text/csv"
    return output