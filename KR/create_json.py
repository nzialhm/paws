# create_json.py
# -*- coding: utf-8 -*-

import json
import collections

# path = "/nct11af/script/tvwsDB/KR/"
path = "D:\\pythonproj\\paws\\KR\\"
#path = "/home/kissvond/work/nct/wsm/buildroot/target/linux/nct11af_imx6ull/def_nct11af/nct11af_bs/nct11af/script/tvwsDB/KR/"

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class create_json_data:
    def __init__(self):
        self.def_val = Object()
        self.def_val.method = ""
        #self.def_val.jsonrpc = "2.0"    #rogie 210517
        self.type = ""
        self.def_val.params = Object()
        self.def_val.params.version="1.0"
        self.bandwith = 0
        self.startHz = 0
        self.channel = 0
        self.stopHz = 0
    
    def read_js_file(self, filepath):
        ret_js = None
        #collections.OrderedDict()
        
        try:            
            ret_data = open(filepath).read().decode("utf-8")
            #ret_data = open("/nct11af/paws/"+filepath).read().decode("utf-8")
            ret_js = json.loads(ret_data)
        except IOError, e:
            print("err: {}".format(e))
            try:            
                ret_data = open(filepath).read().decode("utf-8")
                ret_js = json.loads(ret_data)
            except IOError, e:
                print("err: {}".format(e))
                    
        return ret_js
    
    def add_owner_antenna_info(self, deviceDesc_js, onlyant =True):
        js = None 
        reg_req_devOwner_js = None
        reg_req_antenna_js = None
        
        #load deviceowner & antenna
        if onlyant == False:
            reg_req_devOwner_js = self.read_js_file(path+"deviceOwner.json")
        
        reg_req_antenna_js  = self.read_js_file(path+"antenna.json")        
        
        js = json.loads(self.def_val.toJSON())
        js['params'].update(deviceDesc_js)
        
        if onlyant == False and reg_req_devOwner_js is not None:        
            js['params'].update(reg_req_devOwner_js)
            
        if reg_req_antenna_js is not None:
            js['params'].update(reg_req_antenna_js)

        return js
        
        #print("add owner antenna:{}".format(json.dumps(js, indent=4)))
    def switching_key_value(self, deviceDesc_js):
        #load Master device Description with rename "deviceDesc" to "masterDeviceDesc". location too.
        sw_str = json.dumps(deviceDesc_js)
        sw_str = sw_str.replace('location', 'masterDeviceLocation').replace('deviceDesc', 'masterDeviceDesc')
        ret_js = json.loads(sw_str)
        
        return ret_js

    def callback_freq(self, bandwith, startHz, channel, stopHz):
        self.bandwith = bandwith
        self.startHz = startHz
        self.channel = channel
        self.stopHz = stopHz
        
            
    def create (self, type, id):
        self.type = type
        self.def_val.params.type = self.type
        self.def_val.id = str_output = '{:0>6}'.format(id) #switch int to string with leading zeros.(00000X)
        
        # load device description file as json format
        devDesc_js = self.read_js_file(path+"devDesc.json")

        # return value as json format       
        ret_js = None
        
        if devDesc_js is None: return ret_js
        
        if self.type == "INIT_REQ":
            #print("Send Request: INIT_REQ")
    
            # default values to json format
            self.def_val.method = "spectrum.paws.init"
            #print("\n 1 == "+json.dumps(ret_js,indent=4,sort_keys=True))
        
            ret_js = json.loads(self.def_val.toJSON())
            #print("\n 2 == "+json.dumps(ret_js,indent=4,sort_keys=True))
            
            ret_js['params'].update(devDesc_js)
            #print("\n 3 == "+json.dumps(ret_js,indent=4,sort_keys=True))	#,ensure_ascii=False, sort_keys=False
            
            #print(json.dumps(ret_js, indent=4))
        
        elif self.type == "REGISTRATION_REQ":
            #print("\n\nSend Request: REGISTRATION_REQ")
            # default values to json format
            self.def_val.method = "spectrum.paws.register"
            
            #load deviceowner & antenna
            ret_js = self.add_owner_antenna_info(devDesc_js, False)
            
            #print(json.dumps(ret_js, indent=4))

        elif self.type == "AVAIL_SPECTRUM_REQ":
            #print("Send Request: AVAIL_SPECTRUM_REQ")
            
            # default values to json format
            self.def_val.method = "spectrum.paws.getSpectrum"
            
            #load deviceowner & antenna
            ret_js = self.add_owner_antenna_info(devDesc_js, False)
            
            #load Master device Description with rename "deviceDesc" to "masterDeviceDesc". location too.
            devDesc_js = self.switching_key_value(devDesc_js)
            ret_js['params'].update(devDesc_js) # set again with changing key values.
            
            #print(json.dumps(ret_js, indent=4))
            
        elif self.type == "SPECTRUM_USE_NOTIFY":
            #print("\n\nSend Request: SPECTRUM_USE_NOTIFY")
            
            # default values to json format
            self.def_val.method = "spectrum.paws.notifySpectrumUse"            

            #load deviceowner & antenna
            ret_js = self.add_owner_antenna_info(devDesc_js)
            
            #load Master device Description with rename "deviceDesc" to "masterDeviceDesc". location too.
            devDesc_js = self.switching_key_value(devDesc_js)
            ret_js['params'].update(devDesc_js) # set again with changing key values.
            
            # set spectrum that is given from TVWS database.
            temp_js = Object()
            temp_js.spectra = Object()
            temp_js.spectra.bandwidth = self.bandwith
            temp_js.spectra.frequencyRanges = list()
            
            temp_freq = Object()
            temp_freq.startHz = self.startHz
            temp_freq.stopHz = self.stopHz
            temp_freq.channelId =self.channel
            
            spec_js = json.loads(temp_js.toJSON())
            spec_freq_js = json.loads(temp_freq.toJSON())
            
            spec_js['spectra']['frequencyRanges'].append(spec_freq_js)
            
            ret_js['params'].update(spec_js)
            
            #print(json.dumps(ret_js, indent=4))
            
        return ret_js
        
