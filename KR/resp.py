import json
import time
from datetime import datetime
import os
import sys
import subprocess


# path = "/nct11af/script/tvwsDB/KR/"
path = "D:\\pythonproj\\paws\\KR\\"
#path = "/home/kissvond/work/nct/wsm/buildroot/target/linux/nct11af_imx6ull/def_nct11af/nct11af_bs/nct11af/script/tvwsDB/KR/"

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class resp_handler:
    def __init__ (self):
        self.js_data = None
        self.devDesc_js = None
        self.maxPollingSecs = 0
        self.timestamp = 0
        self.eventtime_start = 0
        self.eventtime_end = 0
        self.bandwidth = 0
        self.frq_startHz = 0
        self.frq_channelId = 0
        self.frq_stopHz = 0
        self.bPAWSError = True

    def read_js_file(self, filepath):
        ret_js = None
        
        try:            
            ret_data = open(filepath).read().decode("utf-8")
            ret_js = json.loads(ret_data)
        except IOError, e:
            print("err: {}".format(e))
        
        return ret_js        

        
    def get_maxPollingSecs(self):
        return self.maxPollingSecs
    
    def set_timestampval(self, time_str):
        ret_timestamp = time.mktime(datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').timetuple())
        return ret_timestamp

    def select_spectra_index_in_list(self, js):
        if len(js) == 1: return 0
        
        eventtime_gap_list = list()
        
        for data in js:
            timestamp_start = self.set_timestampval(data['eventTime']['startTime'])
            timestamp_stop  = self.set_timestampval(data['eventTime']['stopTime'])
            eventtime_gap_list.append(timestamp_stop -  timestamp_start)
        #print(eventtime_gap_list)
        temp = sorted(eventtime_gap_list, reverse=True)[0]
        #print(temp)
        i = 0
        for data in eventtime_gap_list:
            if data == temp: break;
            i += 1   
        
        return i
    
    def set_event_time(self, js):
        self.eventtime_start = self.set_timestampval(js['eventTime']['startTime'])
        self.eventtime_end = self.set_timestampval(js['eventTime']['stopTime'])   
        #print("event time: start:{}, stop{}".format(self.eventtime_start, self.eventtime_end))
    
    def set_spectra_bandwith(self, js, index):
        self.bandwidth = js[index]['spectra'][0]['bandwidth']
        #print("self.bandwidth: {}". format(self.bandwidth))

    def set_spectra_frq(self, js, index):
        ret = True
	#print(json.dumps(js[0]['spectra'][0]['frequencyRanges'],indent=4))
        if len(js[index]['spectra'][0]['frequencyRanges']) > 0:
            self.bPAWSError = True
            self.frq_stopHz = js[index]['spectra'][0]['frequencyRanges'][0]['stopHz']
            self.frq_startHz = js[index]['spectra'][0]['frequencyRanges'][0]['startHz']
            self.frq_channelId = js[index]['spectra'][0]['frequencyRanges'][0]['channelId']
        else:
            self.frq_startHz = 0
            self.frq_channelId = 0
            self.frq_stopHz = 0
            ret = False

        return ret

    def set_spectra_stafrq(self, js, index, channel):
        ret = True
      
        for data in js[index]['spectra'][0]['frequencyRanges']:
            if int(data['channelId']) == int(channel):
                print("python "+path+"change_json.py "+str(data['channelId'])+" 6")
                os.system("python "+path+"change_json.py "+str(data['channelId'])+" 6")
                self.frq_stopHz = data['stopHz']
                self.frq_startHz = data['startHz']
                self.frq_channelId = data['channelId']
                break;
            else:
                self.frq_startHz = 0
                self.frq_channelId = 0
                self.frq_stopHz = 0
                ret = False

        return ret

    def activate_channel(self):
        #print(data)
        channel = ""
        with open(path+"setChannel.json","r") as data:
            json_data = json.load(data)
            channel = str(json_data['frequencyRanges'][0]['channelId'])

        f= open(path+"active_channel.json", "w")
        json_data = Object()
        json_data.channel = str(channel)
        date = datetime.now()
        json_data.active_date = datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
        active_data= json.loads(json_data.toJSON())
        data = json.dumps(active_data, indent=4)
        f.write(data)
        f.close()
        os.system("nohup python ../check_activate.py KR 1> /dev/null 2>&1 &")

    def error_resp(self):
        ret = None
        if 'error' in self.js_data and 'message' in self.js_data['error'] and 'code' in self.js_data['error']:
            ret = "Error Code: {}\nmessage: {}".format(self.js_data['error']['code'],self.js_data['error']['message'])
        return ret
    
    def get_cur_time(self):
        return "[" +  datetime.now().strftime("%c") + "]"

    def get_result_str(self, freq_str=None):
        ret_str = None
            
        if self.js_data is not None:
            # get error first
            if 'error' in self.js_data and 'message' in self.js_data['error'] and 'code' in self.js_data['error']:                
                ret_str = self.get_cur_time() + " ERROR_RESP code: {}\n".format(self.js_data['error']['code'])
                ret_str += self.get_cur_time() + " ERROR_RESP message: {}\n".format(self.js_data['error']['message'])

            # get message 
            if 'result' in self.js_data and 'type' in self.js_data['result'] and 'id' in self.js_data:
                if ret_str is None:
                    ret_str = self.get_cur_time() + " RESP Type: {}\n".format(self.js_data['result']['type'])
                else:
                    ret_str += self.get_cur_time() + " RESP Type: {}\n".format(self.js_data['result']['type'])
                ret_str += self.get_cur_time() + " RESP Id: {}\n".format(self.js_data['id'])

        if freq_str is not None:
            if ret_str is None:
                ret_str = self.get_cur_time() + " {}\n".format(freq_str)
            else:
                ret_str += self.get_cur_time() + " {}\n".format(freq_str)
        #ret_str += "resp data:\ {}".format(json.dumps(self.js_data, indent=4))
        #ret_str += "**************************\n"
        return ret_str
     
    
    # compare self.id(response) with index:FIX ME
    def handle (self, index, data, callback=None, req_type=None):
        ret_str = None
        self.bPAWSError = True
        self.js_data = json.loads(data)
        #self.devDesc_js = self.read_js_file("devDesc.json")
        
        #if self.devDesc_js is None: return "FILE OPEN FAILED"
        
        #print("*************************")
        #print('resp data:\ {}'.format(json.dumps(self.js_data, indent=4)))        
        #print("*************************\n")
        
        # get message
        write_data=self.get_result_str(req_type)
        
        ret_str = self.error_resp()
        if  ret_str is not None: # get error message
            return ret_str
        
        if ('result'in self.js_data) == False:
            #do something I guess that it needs to start init request.
            return "INIT_START_AGAIN"
        
        # set maxPollingSecs : Max running time of frequency
        if 'rulesetInfo' in self.js_data['result'] and \
        'maxPollingSecs' in self.js_data['result']['rulesetInfo']:
            maxPollingSecs_tmp = self.js_data['result']['rulesetInfo']['maxPollingSecs']

            if self.maxPollingSecs != maxPollingSecs_tmp:
                self.maxPollingSecs = int(maxPollingSecs_tmp)
            
        #cmp_id = int(self.js_data['id'])
        
        #print('response index:{}, index:{} '.format(cmp_id, index))
        
        #if cmp_id != int(index):
        #    return "IGNORE_RESP"
        
        if self.js_data['result']['type'] == "INIT_RESP":
            if 'rulesetInfo' in self.js_data['result'] and\
            'maxLocationChange' in self.js_data['result']['rulesetInfo']:
                self.maxLocationChange = int(self.js_data['result']['rulesetInfo']['maxLocationChange'])
                if self.maxLocationChange > 100:
                    ret_str = "INIT_REQ"
                    self.bPAWSError = True
                else:
                    ret_str = "REGISTRATION_REQ"
                    self.bPAWSError = False
                    os.system("echo "+self.js_data['result']['type']+" > /tmp/paws_status")
                
        elif self.js_data['result']['type'] == "REGISTRATION_RESP":
            self.bPAWSError = False
            ret_str = "AVAIL_SPECTRUM_REQ"
            os.system("echo "+self.js_data['result']['type']+" > /tmp/paws_status")
        elif self.js_data['result']['type'] == "AVAIL_SPECTRUM_RESP":
            ret_str = "SPECTRUM_USE_NOTIFY"
            index = 0
            
            # get Timestamp
            if 'timestamp' in self.js_data['result'] :
                self.timestamp = self.set_timestampval(self.js_data['result']['timestamp'])
                #print("time: {}".format(self.timestamp))
            else:
                # Must send asking spectrum request again in order to get timestamp : Not in Protocol (My opt) 
                ret_str = "AVAIL_SPECTRUM_REQ"
            
            # get start time and end time in event time attribute of response data.
            if 'spectrumSchedules' in self.js_data['result'] :
                # create & write file
                if os.path.exists(path+"spectrumSpecs.json"):
                    os.remove(path+"spectrumSpecs.json")                
                f= open(path+"spectrumSpecs.json", "w")
                f.write(json.dumps(self.js_data['result'], indent=4))
                f.close()
                index = self.select_spectra_index_in_list(self.js_data['result']['spectrumSchedules'])
                #print(index)
                
                # set event time: start time and stop time
                self.set_event_time(self.js_data['result']['spectrumSchedules'][0])
                
                # get bandwidth value in event time attribute of response data.
                self.set_spectra_bandwith(self.js_data['result']['spectrumSchedules'], index)
               
                ret_freq = self.set_spectra_frq(self.js_data['result']['spectrumSchedules'], index)
                #get frequency rage
                
                #set bandwith & frequency
                if callback is not None:
                    callback(self.bandwidth, self.frq_startHz, self.frq_channelId, self.frq_stopHz) 
                    os.system("echo "+self.js_data['result']['type']+" > /tmp/paws_status")
                else:
                    print("callback is none")
                 
                if ret_freq == False: 
                    ret_str = "ERROR_RESP: No frequency availble"
                    write_data = self.get_result_str(ret_str)
            else:
                ret_str = None
            
        elif self.js_data['result']['type'] == "SPEC_USE_RESP":
            self.bPAWSError = False
            # set time or thread with self.maxPollingSecs value.
            ret_str = "PAWS_DONE"
            str_output = "RF Channel\n"
            str_output += "                                ChannelId:      {}\n".format(self.frq_channelId)
            str_output += "                                Bandwidth:      {}\n".format(self.bandwidth)
            str_output += "                                Frequency:      {} MHz ~ {} MHz\n".format(self.frq_startHz, self.frq_stopHz)
            write_data = self.get_result_str(str_output)
            #print("\n\n---------------------------------")
            #print("RF Channel")
            #print("Channel:      {}".format(self.frq_channelId))
            #print("bandwidth:    {}".format(self.bandwidth))
            #print("Frequency:    {} MHz ~ {} MHz".format(self.frq_startHz, self.frq_stopHz))
            #print("Output:       On")
            #print("---------------------------------")
            os.system("echo "+ret_str+" > /tmp/paws_status")
            self.activate_channel()
        
        return ret_str

        
