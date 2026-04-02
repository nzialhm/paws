import urllib2
import ssl # because of python2
import json
import create_json
import resp
import time
import socket
from threading import Thread
import os
import ctypes
import sys
import ast
#import enter_master_info

#if hasattr(ssl, '_create_unverified_context'):
#   ssl._create_default_https_context = ssl._create_unverified_context

path = "/nct11af/script/tvwsDB/"

class paws:
    def __init__(self):
        opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1)))
        urllib2.install_opener(opener)
        self.resp = resp.resp_handler()
        self.cj = create_json.create_json_data()
        self.index = 1
        self.maxPollingSecs = 0
        #self.doi = enter_master_info.MasterInfo()
        
        #try:
            #libc = ctypes.CDLL('libc.so.6')
            #libc = ctypes.cdll.LoadLibrary('libc.so.6')
            ##self.res_init = getattr(libc, '__res_init')  
        #except:
        #    print("Error calling libc.__res_init")

    def get_nct11af_server_url(self):
        url_str= None
        ret_data = None
        try:            
            ret_data = open(path+"nct11afurl.json").read().decode("utf-8")
        except IOError, e:
            print("err4: {}".format(e))
            try:
                ret_data = open(path+"nct11afurl.json").read().decode("utf-8")
            except IOError, e:
                print("err3: {}".format(e))

        if ret_data is not None:
            ret_js = json.loads(ret_data)
            url_str = ret_js['url']
            
        return url_str
    
    #rogie 210524
    def setChannel(self,data):
        f = open(path+"setChannel.json").read().decode("utf-8")
        fJson = json.loads(f)
       # print("----------fJson json : \n"+json.dumps(fJson,indent=4)+"\n"); 
        #print("----------fJson json : \n"+json.dumps(data,indent=4)+"\n"); 
        
        #tmp = json.loads(ast.literal_eval(data))
        #tmp = json.loads(data)
        data["params"]["spectra"]["bandwidth"] = fJson["bandwidth"]
        data["params"]["spectra"]["frequencyRanges"][0]["startHz"] = fJson["frequencyRanges"][0]["startHz"]
        data["params"]["spectra"]["frequencyRanges"][0]["channelId"] = fJson["frequencyRanges"][0]["channelId"]
        data["params"]["spectra"]["frequencyRanges"][0]["stopHz"] = fJson["frequencyRanges"][0]["stopHz"]
        
        #data = tmp
        #print("----------make json : \n"+json.dumps(data,indent=4)+"\n"); 
        
    
    def send_request(self, req_type, index, url,bUseNotify):
        ret_str = None
        chk = False

        data = self.cj.create(req_type, index)
        
        print(bUseNotify)
        #rogie
        if bUseNotify=='True':
            self.setChannel(data)
            
        if data is not None:
            response = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})

            #socket.setdefaulttimeout(120)
            
            #201204 rogie
            print("send json : \n"+json.dumps(data,indent=4)+"\n"); 
            
            try:
                #os.environ['https_proxy']=''
                ##self.res_init(None)
                print(response);
                res = urllib2.urlopen(response,timeout=2)
                chk = True
            except IOError, e:
                print("err1: {}".format(e))

            if chk == True:
                msg = res.read()
               # print("--------------------read json--------------------\n")
                print("\n--------------------\nread json :"+json.dumps(json.loads(msg.decode("utf-8")),indent=4))
               # print("\n--------------------end result--------------------\n")
                res_js=json.loads(msg.decode("utf-8"))
                ret_str = self.resp.handle(id, json.dumps(res_js), self.cj.callback_freq, req_type)
                
        return ret_str    
    
    def paws_run(self,start,end,bUseNotify):
        nct11af_url=self.get_nct11af_server_url()
    
        if nct11af_url is not None:
            #next_cmd_str = self.send_request("INIT_REQ", self.index, nct11af_url)
            next_cmd_str = self.send_request(start, self.index, nct11af_url,bUseNotify)

            # INIT_REQ -> REGISTRATION_REQ -> AVAIL_SPECTRUM_REQ -> SPECTRUM_USE_NOTIFY
            while True: #index < 3:
                if next_cmd_str is not None:

                    if next_cmd_str == end :
                        print("\nend! \n");
                        break; 
                    
                    time.sleep(1)
                    next_cmd_str = self.send_request(next_cmd_str, self.index, nct11af_url,bUseNotify)
                    
                    #rogie#if next_cmd_str == "PAWS_DONE" : 
                        
                        # set time or thread with self.maxPollingSecs value.
                        #rogie#self.maxPollingSecs = self.resp.get_maxPollingSecs()
                        #print("maxPollingSecs is {}".format(self.maxPollingSecs))
                       #rogie# time.sleep(self.maxPollingSecs)
                       #rogie# next_cmd_str = "AVAIL_SPECTRUM_REQ"
                   
                    
                else: 
                    #print("BREAK loop=> Next cmd: {}".format(next_cmd_str))
                    #print("\n\n---------------------------------")
                    #print("RF Channel")
                    #print("Channel:      Not determind")
                    #print("bandwidth:    0 MHz")
                    #print("Frequency:    0 MHz ~ 0 MHz")
                    #print("Output:       Off")
                    #print("---------------------------------")
                    break;

                self.index += 1

start = "INIT_REQ"
end = "PAWS_DONE" #SPECTRUM_USE_NOTIFY
bUseNotify = False

#start = "INIT_REQ"
#end = "SPECTRUM_USE_NOTIFY" #SPECTRUM_USE_NOTIFY
#bUseNotify = False

#start = "SPECTRUM_USE_NOTIFY" 
#end = "PAWS_DONE"#"AVAIL_SPECTRUM_REQ"
#bUseNotify = True

if len(sys.argv) > 1:
    start = sys.argv[1]
    if len(sys.argv) > 2:
        end = sys.argv[2]
        if len(sys.argv) > 3:
            bUseNotify = sys.argv[3]


pw = paws()
#if pw.doi.select_inq() is True:
pw.paws_run(start,end,bUseNotify)
#else:
print("END")
#work = Thread(target=pw.paws_run)
#work.setDaemon(True) #background
#work.start()

    





