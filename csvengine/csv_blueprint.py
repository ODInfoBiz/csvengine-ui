'''
Created on Dec 24, 2015

@author: jumbrich
'''

from flask import Blueprint, render_template,current_app

from flask import  request

import structlog


log =structlog.get_logger()


csvb = Blueprint('csv', __name__,
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

### UI service entry pages
###########################


def my_render_template(templ, **kwargs):
    return render_template(templ,  navigation_bar=current_app.config['navigation_bar'], **kwargs)


### CSV CLEAN SERVICE
###########################
@csvb.route("/csv/clean")
def csvclean():
    return my_render_template("csv_clean.html")

@csvb.route('/csv/clean/service', methods=['GET'])
def csvclean_service():
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
    
    current_app.logger.debug("csvclean_service fileId=" + str(fileID) +" url=" + str(url))

    #current_app.logger.debug("Reading "+fileID+" from disk")
    table = datacache.getParser(fileID)
    
    #current_app.logger.debug("Parsed content of file.")
    
    title = url if url else fileID
    original = datacache.getSubmit(fileID)
    rows = len(original.split('\n'))
    results={ 'orig': decode_utf8(original), 'sample': table.sample, 'title': title, 'cols': table.columns, 'rows': rows}

    return my_render_template("csv_clean_results.html", data=results)
    #return Response(smart_table.generate(table), mimetype='text/csv')


