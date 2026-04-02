# nct11af_send_req.py
# -*- coding: utf-8 -*-

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
import subprocess
#import enter_master_info

#if hasattr(ssl, '_create_unverified_context'):
#   ssl._create_default_https_context = ssl._create_unverified_context

path = "/nct11af/script/tvwsDB/KR/"
# path = "D:\\pythonproj\\paws\\KR\\"
log_file = "/tmp/paws_log"
# log_file = "paws_log"
#path = "/home/kissvond/work/nct/wsm/buildroot/target/linux/nct11af_imx6ull/def_nct11af/nct11af_bs/nct11af/script/tvwsDB/KR/"
f_log = open(log_file, "w")

class paws:
    def __init__(self):
        opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1)))
        urllib2.install_opener(opener)
        self.resp = resp.resp_handler()
        self.cj = create_json.create_json_data()
        self.index = 1
        self.maxPollingSecs = 0
        self.bPAWSError = True
        
        #self.doi = enter_master_info.MasterInfo()
        
        #try:
        ##libc = ctypes.CDLL("libc.so.6")
        #print("111 : "+libc)
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
            print("{}".format(e))
            try:
                ret_data = open(path+"nct11afurl.json").read().decode("utf-8")
            except IOError, e:
                print("{}".format(e))

        if ret_data is not None:
            ret_js = json.loads(ret_data)
            url_str = ret_js['url']
            
        return url_str
    
    #rogie 210524
    def setChannel(self,data):
        if os.path.getsize(path+"setChannel.json") > 0:
            f = open(path+"setChannel.json").read().decode("utf-8")
            fJson = json.loads(f)
        else:
            print("setChannel Open error")
	    return
        #print("----------fJson4 json : \n"+json.dumps(fJson,indent=4)+"\n"); 
        #print("----------fJson5 json : \n"+json.dumps(data,indent=4)+"\n"); 
        
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
        use_notify = False


        data = self.cj.create(req_type, index);

        if req_type == "SPECTRUM_USE_NOTIFY":
            use_notify = True
            if bUseNotify=='True':
                self.setChannel(data)
        
        #d = json.loads(data)
        #error check
       #data.hasOwnProperty('error');
        '''
        if "error" in data:
           print("ddddd-----------------------------------------------------\n")
           print(data)
           print("dddddd-----------------------------------------------------\n")
        '''             

        #print("send json : \n"+json.dumps(data,indent=4)+"\n");
        f_log.write("send json : \n"+json.dumps(data,indent=4)+"\n")
        #rogie
        # 에러 체크
        self.bPAWSError = True
            
        if data is not None:
            response = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})

            #socket.setdefaulttimeout(120)
            
            #201204 rogie
            
            try:
                res = urllib2.urlopen(response, timeout=5)
                chk = True
            except urllib2.HTTPError as e:
                print("HTTPError:", e.code)
                self.bPAWSError = True
                return "HTTP_ERROR"

            except urllib2.URLError as e:
                print("URLError:", e.reason)
                self.bPAWSError = True
                return "URL_ERROR"

            except Exception as e:
                print("Exception:", e)
                self.bPAWSError = True
                return "UNKNOWN_ERROR"

            if chk == True:
                msg = res.read()
                msg = msg.replace("[,", "[")
                #msg err ck #210604 rogie
                if '"error"' in msg :
                    f_log.write("\n-ERROR -------------------\nread json :"+json.dumps(json.loads(msg.decode("utf-8")),indent=4))
                #    ret_str = "error"
                #    print("\n-ERROR -------------------\nread json :"+json.dumps(json.loads(msg.decode("utf-8")),indent=4))
                else:
                    f_log.write("\n--------------------\nread json :"+json.dumps(json.loads(msg.decode("utf-8")),indent=4))
                #    print("--------------------read json--------------------\n")
                #    print("\n--------------------\nread json :"+json.dumps(json.loads(msg.decode("utf-8")),indent=4))
                #    print("\n--------------------end result--------------------\n")
                res_js=json.loads(msg.decode("utf-8"))
                ret_str = self.resp.handle(id, json.dumps(res_js), self.cj.callback_freq, req_type)
                # 에러 체크
                self.bPAWSError = self.resp.bPAWSError
                if use_notify == True:
                    if ret_str != "PAWS_DONE":
                        f= open(path+"active_channel.json", "w")
                        f.write(data)
                        f.close()
           
        #print(ret_str)
        return ret_str    
    
    def paws_run(self,start,end,bUseNotify):
        nct11af_url=self.get_nct11af_server_url()
    
        if nct11af_url is not None:
            #next_cmd_str = self.send_request("INIT_REQ", self.index, nct11af_url)
            cur_cmd_str = start
            next_cmd_str = self.send_request(start, self.index, nct11af_url,bUseNotify)
            retry_cnt = 0

            # INIT_REQ -> REGISTRATION_REQ -> AVAIL_SPECTRUM_REQ -> SPECTRUM_USE_NOTIFY
            while True: #index < 3:
                if next_cmd_str is not None:
                    if next_cmd_str == end :
                        #print("\nend! \n");
                        break; 
                    elif next_cmd_str == "500":
                        if retry_cnt > 3:
                            break;
                        next_cmd_str = cur_cmd_str
                        retry_cnt = retry_cnt+1
                    else : 
                        cur_cmd_str = next_cmd_str
                        retry_cnt = 0
                    #elif next_cmd_str == "error" :
                        #print("\nerror! \n");
                        
                        #sys.exit()
                        #break;
                    
                    #time.sleep(1)
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

if pw.bPAWSError:
    f_log.write("\n--------------------\ninterface down ")
    try:
        # 1. 파일 목록 가져오기
        ret = subprocess.check_output(["ls", "/proc/nct11af/"]).decode()

        if "nct11af1" in ret:
            f_log.write("\nnct11af1 exist")

            # 2. 인터페이스 상태 확인
            try:
                subprocess.check_output(["ifconfig", "nct11af1"])
                f_log.write("\nnct11af1 active")

                # 3. 인터페이스 down
                subprocess.call(["ifconfig", "nct11af1", "down"])
                f_log.write("\nnct11af1 down")

            except subprocess.CalledProcessError:
                f_log.write("\nnct11af1 deactive")

        else:
            f_log.write("\nnct11af1 not exist")

    except Exception as e:
        f_log.write("\n--------------------\ninterface down exception ")
#else:
#print("END")
#work = Thread(target=pw.paws_run)
#work.setDaemon(True) #background
#work.start()
