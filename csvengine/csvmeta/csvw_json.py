'''
Created on Dec 18, 2015

@author: jumbrich
'''

import re

class CSVMCreator(object):

    default_dialect= {
  "encoding": "utf-8",
  "lineTerminators": ["\r\n", "\n"],
  "quoteChar": "\"",
  "doubleQuote": True,
  "skipRows": 0,
  "commentPrefix": "#",
  "header": True,
  "headerRowCount": 1,
  "delimiter": ",",
  "skipColumns": 0,
  "skipBlankRows": False,
  "skipInitialSpace": False,
  "trim": False
}

    
    @classmethod
    def create(cls, formData):
        import pprint 
        pprint.pprint(dict(formData))
         
        
        data= {'@context': [ 'http://www.w3.org/ns/csvw' ]}
        if len(formData['language'])>0:
            data['@context'].append({"@language": formData['language']})
        print 'here'
        data["url"]= formData['tableURL']    
        data["dc:title"]= formData['tableTitle']
        data["dcat:keyword"]= formData['tableKeyword'].split(';')
        data["dc:publisher"]= {
                              "schema:name": formData['pubName'],
                              "schema:url": {"@id": formData['pubURL']}
                              }
        data["dc:license"]= {"@id": formData['license']},
        data["dc:modified"]= {"@value": formData['lastMod'], "@type": "xsd:date"}
        
        
        dialect =  {}
        for k, v in CSVMCreator.default_dialect.items():
            
            if k == 'lineTerminators':
                if 'lineTerminator' in formData:
                    dialect[k]= [formData['lineTerminator']]
            elif k in formData:
                if formData[k]== 'on':
                    dialect[k]= True
                else:
                    dialect[k]= formData[k]
            
            else:
                dialect[k]= v
        
        data['dialect']= dialect
        tableSchema = cls.parseTableSchema(formData)
        
        data['tableSchema']=tableSchema
        
        pprint.pprint(data) 
        return data
    
    @classmethod 
    def parseTableSchema(cls, data):
        primaryKey=[]
        columns=[]
        tableSchema={'columns':columns,'primaryKey':primaryKey}
        
        col={}
        for k,v in data.items():
            m= re.search('col-(.+?)--(.*?)', k)
            if m:
                colPos = m.group(1)
                label = k.split("--")[1]
                
                if colPos not in col:
                    col[colPos]={}
                
                    
                #else:
                if len(v) == 0:
                    continue
                if label == 'datatype':
                    if v=='date' or v =='dateTime' or v=='dateTimeStamp':
                        col[colPos][label]={
                                            "base": v,
                                            "format": "M/d/yyyy"
                                            }
                        print 
                    else:
                        col[colPos][label]=v 
                elif label == 'datepattern':
                    if 'datatype' in col[colPos]: 
                        col[colPos]['datatype']['format']= v
                    else:                        
                        col[colPos]['datatype']={'base': '',
                                            "format": v
                                            }
                elif label == 'required' and v == 'on':
                    col[colPos][label]=True
                elif label == 'title':
                    col[colPos]['titles']=v
                else: 
                    col[colPos][label]=v 
        for k in sorted(col.keys()):
            if 'primaryKey' in col[k] and col[k]['primaryKey'] == 'on':
                del col[k]['primaryKey']
                primaryKey.append(col[k]['name'])
            columns.append(col[k])
        return tableSchema 