# CSV Engine
The "CSV Engine" is a web server offering a set of services to handle and process CSV files. One of the main feature in the current version is an editor to create an initial version of the **[CSV on the Web metadata standard file](https://www.w3.org/2013/csvw/wiki/Main_Page)**. 

We hope that people find this tool useful and will join or contribute to the project by providing feedback, bug reports, feature requests or code contributions.

## Under the hood
The tool is implemented in Python 2.7 using the FLASK web server framework and the Jinja2 template engine. 

The frontend is using the [Material Design Lite](http://www.getmdl.io/index.html) framework for the layout and some basic Javascripts.


## Requirements
1) **anycsv**
`pip install git+git://github.com/sebneu/anycsv.git`

2) **pyyacp** `pip install git+git://github.com/ODInfoBiz/pyyacp.git`


##Setup
* `$ git clone git@github.com:ODInfoBiz/csvengine-ui.git`
* `$ cd csvengine-ui`
* (optionally) setup virtual environment
* install github requirements 
* `$ python setup.py install`
* `$ ./runner -h`  to show help
* `$ ./runner -c template_config.yaml -p 3333`  to start the UI at port 3333

In case you host this service, please make sure to regularly delete the temp filder

## Config file
The config file is in the YAML format and contains parameter for the local file storage and UI setup.

##TODO's
* Restful API for the services

## Team
This project is an effort of serval people and was created in  as part of a bachelor thesis of Manuel Undesser at the WU Vienna.
The following people currently contributed to the code base:
* Jürgen Umbrich 
* Sebastian Neumaier
* Nina Mrzeli
* Manual Undesser

## Similar projects
**Python**
* ..


##License
The MIT License (MIT)

Copyright (c) 2016 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.