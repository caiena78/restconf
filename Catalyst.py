
from tokenize import String
from urllib import response
import requests
import json
import os
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import datetime
from enum import Flag

from jinja2 import Template


class Catalyst:
    templetsPath='lib/templets/'
    base={}
    def __init__(self,host,user,password,port=443):
        self.host=host
        self.user=user
        self.password=password
        self.port=port
        self.base=json.loads(self.__getTemplate("base.j2"))
    
    
    def __getTemplate(self,file:String,vars:dict={}):
        with open(self.templetsPath+file,'r') as r:
            tempate=Template(r.read())
        if len(vars)==0:
            return tempate.render()   
        return tempate.render(vars)

    def __attach(self,element:dict):
        for i,(k,v) in enumerate(element.items()):
            self.base["Cisco-IOS-XE-native:native"][k]=v

    def setHostname(self,hostname:String):
        vars={
            "hostname":hostname
            }
        file="hostname.j2" 
        element=self.__getTemplate(file,vars)
        print(element)
        element=json.loads(element)
        self.__attach(element) 
    


device = {"ip": os.getenv('switch_ip'), "port": "443", "user": os.getenv('switch_user'), "password": os.getenv('switch_pwd')}
x=Catalyst(device['ip'],device['user'],device['password'],device['port'])
x.setHostname("NETSW")
print(json.dumps(x.base))