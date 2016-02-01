# CSV Engine



## UI
We are currently the [Material Design Lite](http://www.getmdl.io/index.html) framework.


## Requirements
1) **anycsv**
`pip install git+git://github.com/sebneu/anycsv.git`

2) **pyyacp** `pip install git+git://github.com/ODInfoBiz/pyyacp.git`

3) 

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