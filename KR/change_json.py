import json
import collections
import sys
import math
    
path = "/nct11af/script/tvwsDB/KR/"
#path = "/home/kissvond/work/nct/wsm/buildroot/target/linux/nct11af_imx6ull/def_nct11af/nct11af_bs/nct11af/script/tvwsDB/KR/"

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True)    

def set_new_json(nameJson,dic):
    if(nameJson == 'antenna'):
        with open(path+"antenna.json","r") as data:
            json_data = json.load(data)
            if dic.get("heightType") and dic['heightType'] is not None:
                json_data['antennaCharacteristics']['heightType'] = dic['heightType']
                                
            if dic.get("height") and dic['height'] is not None:
                json_data['antennaCharacteristics']['height'] = dic['height']
                            
            with open(path+"antenna.json", 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            
    elif(nameJson == 'nct11afurl'):
        with open(path+"nct11afurl.json","r") as data:
            json_data = json.load(data)
            
            if dic.get("url") and dic['url'] is not None:
                json_data['url']= dic['url']
                                
            with open(path+"nct11afurl.json", 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            
            
    elif(nameJson == 'devDesc'):
        with open(path+"devDesc.json","r") as data:
            json_data = json.load(data)
                
            if dic.get("serialNumber") and dic['serialNumber'] is not None:
                json_data['deviceDesc']['serialNumber'] = dic['serialNumber']
            else:
                json_data['deviceDesc']['serialNumber'] = "0"
                
            if dic.get("ksDeviceType") and dic['ksDeviceType'] is not None:
                json_data['deviceDesc']['ksDeviceType'] = dic['ksDeviceType']
            else:
                json_data['deviceDesc']['ksDeviceType'] = "0"
            
            #if dic['ksDeviceEmissionPower']:
                #json_data['deviceDesc']['ksDeviceEmissionPower'] = dic['ksDeviceEmissionPower']
            
            if dic.get("latitude") and dic['latitude'] is not None: #is not None:
                 json_data['location']['point']['center']['latitude'] = dic['latitude']
            else:
                json_data['location']['point']['center']['latitude'] = "0"
                        
            if dic.get("longitude") and dic['longitude'] is not None:
                json_data['location']['point']['center']['longitude'] = dic['longitude']
            else:
                json_data['location']['point']['center']['longitude'] = "0"
                
            with open(path+"devDesc.json", 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
        
    elif(nameJson == 'setChannel'):
        json_data=Object()
        json_data.bandwidth=""
        json_data.frequencyRanges=[1]
        json_data.frequencyRanges[0]=Object()
        json_data.frequencyRanges[0].startHz=""
        json_data.frequencyRanges[0].channelId=""
        json_data.frequencyRanges[0].stopHz=""

        if dic.get("bandwidth") and dic['bandwidth'] is not None:
            json_data.bandwidth = dic['bandwidth']
        else:
            json_data.bandwidth = "6"

        if dic.get("channelId") and dic['channelId'] is not None:
            json_data.frequencyRanges[0].channelId = dic['channelId']
        else:
            json_data.frequencyRanges[0].channelId = "0"

        if dic.get("startHz") and dic['startHz'] is not None:
            json_data.frequencyRanges[0].startHz = dic['startHz']
        else:
            json_data.frequencyRanges[0].startHz = "0"

        if dic.get("stopHz") and dic['stopHz'] is not None:
            json_data.frequencyRanges[0].stopHz = dic['stopHz']
        else:
            json_data.frequencyRanges[0].stopHz = "0"

        with open(path+"setChannel.json", 'w') as outfile:
            json.dump(json.loads(json_data.toJSON()), outfile, indent=4)
                                
def read_uci_file( filepath):
    ret_data = None

    try:            
        ret_data = open("/etc/config/"+filepath).read().decode("utf-8")
    except IOError, e:
        print("err: {}".format(e))
        try:            
            ret_data = open("/nct11af/config/"+filepath).read().decode("utf-8")
        except IOError, e:
            print("err: {}".format(e))            

    return ret_data 
 
def uci_to_json(serialNumber):
    
        data = read_uci_file("configPAWS_KR")
                
        f = False 
        cur_index = 0
        
        if data is None:
            print("open the config file failed")
            return
        
        dic = {}
        dic['serialNumber'] = serialNumber
                
        for k in data.splitlines():
            s=k.replace("option", "")
            s = s.lstrip()
            s = s.replace(" '", "/")
            s_val = s.replace("'", "").split("/")
                        
            if s_val[0] == "latitude":
                #dic[s_val[0]] = '{0:0.0}'.format(float(s_val[1]))#math.trunc(float(s_val[1]), 5)
                dic[s_val[0]] = float(s_val[1])
            elif s_val[0] == "longitude":
                #dic[s_val[0]] = '{0:0.0}'.format(float(s_val[1]))
                dic[s_val[0]] = float(s_val[1])
                
            elif s_val[0] == "height":
                dic[s_val[0]] = round(float(s_val[1]), 1)                                
            elif s_val[0] == "heightType":
                dic[s_val[0]] = s_val[1]
            
            elif s_val[0] == "ksDeviceType":
                dic[s_val[0]] = s_val[1]
            
            #elif s_val[0] == "serialNumber":
            #    dic[s_val[0]] = serialNumber sssssssssssssssssssssssssssssss
                
        #print(dic)        
        set_new_json('devDesc',dic)
        set_new_json('antenna', dic)

def setUrl_json():
    
    data = read_uci_file("configPAWS_KR")
            
    f = False 
    cur_index = 0
    
    if data is None:
        print("open the config file failed")
        return
    
    dic = {}
            
    for k in data.splitlines():
        s=k.replace("option", "")
        s = s.lstrip()
        s = s.replace(" '", "|")
        s_val = s.replace("'", "").split("|")
                    
        if s_val[0] == "url":
            dic[s_val[0]] = s_val[1]
            
            
    set_new_json('nct11afurl',dic)


def setChannel_json(num,bandwidth):
    #with open(path+"spectrumSpecs.json","r") as data:
    data = open(path+"spectrumSpecs.json","r").read()
    #print("data :: "+str(len(data)))
    if data is not None:
        if len(data) > 0:
            json_data = json.loads(data)
            dic = {'bandwidth':0,'startHz':0,'channelId': 0,'stopHz':0}
            
            cnlLst = json_data['spectrumSchedules'][0]['spectra'][0]['frequencyRanges']
            
            if cnlLst is not None:
                #if bandwidth==json_data['spectrumSchedules'][0]['spectra'][0]['bandwidth']:
                    
                for c in cnlLst:
                    if str(c['channelId']) == num:
                        
                        dic['bandwidth'] = bandwidth #json_data['spectrumSchedules'][0]['spectra'][0]['bandwidth']
                        dic['startHz'] = c['startHz']
                        dic['channelId'] = c['channelId']
                        dic['stopHz'] = c['stopHz']
                
                
            set_new_json('setChannel',dic)
                
###################################################################################


msg=""
num=""

if len(sys.argv) > 1:
    msg = sys.argv[1] 
    if len(sys.argv) > 2:
        num = sys.argv[2]   

if msg == "setChannel":
    if len(sys.argv) > 3:
        bandwidth = sys.argv[3]   
    setChannel_json(num,bandwidth)    #channel number
elif msg == "setUrl":
    setUrl_json();
else:   #"getChannel"
    uci_to_json(num)    #serialNumber
    

###################################################################################

###
'''

    if len(sys.argv) > 1:
        nameJson = sys.argv[1]
        
    if(nameJson == 'antenna'):
        with open("antenna.json","r") as data:
            json_data = json.load(data)
            
            heightType = json_data['antennaCharacteristics']['heightType']
            if len(sys.argv) > 2:
                heightType = sys.argv[2]
            
            json_data['antennaCharacteristics']['heightType'] = heightType
                    
            height = json_data['antennaCharacteristics']['height']
            if len(sys.argv) > 3:
                height = sys.argv[3]
            
            json_data['antennaCharacteristics']['height'] = height
                
            with open("antenna.json", 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
            
            
    elif(nameJson == 'devDesc'):
        with open("devDesc.json","r") as data:
            json_data = json.load(data)
                
            serialNumber = json_data['deviceDesc']['serialNumber']
            if len(sys.argv) > 2:
                serialNumber = sys.argv[2]
            
            json_data['deviceDesc']['serialNumber'] = serialNumber
                    
            latitude = json_data['location']['point']['center']['latitude']
            if len(sys.argv) > 3:
                latitude = sys.argv[3]
            
            json_data['location']['point']['center']['latitude'] = latitude
            
            longitude =  json_data['location']['point']['center']['longitude']
            if len(sys.argv) > 4:
                longitude = sys.argv[4]
            
            json_data['location']['point']['center']['longitude'] = longitude
                
            with open("devDesc.json", 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
        
    elif(nameJson == 'setChannel'):
        with open("setChannel.json","r") as data:
            json_data = json.load(data)
                
            bandwidth = json_data['bandwidth']
            if len(sys.argv) > 2:
                bandwidth = sys.argv[2]
            
            json_data['bandwidth'] = bandwidth
                    
            channelId = json_data['frequencyRanges'][0]['channelId']
            if len(sys.argv) > 3:
                channelId = sys.argv[3]
            
            json_data['frequencyRanges'][0]['channelId'] = channelId
                    
            startHz = json_data['frequencyRanges'][0]['startHz']
            if len(sys.argv) > 4:
                startHz = sys.argv[4]
            
            json_data['frequencyRanges'][0]['startHz'] = startHz
                    
            stopHz = json_data['frequencyRanges'][0]['stopHz']
            if len(sys.argv) > 5:
                stopHz = sys.argv[5]
            
            json_data['frequencyRanges'][0]['stopHz'] = stopHz
                
            with open("setChannel.json", 'w') as outfile:
                json.dump(json_data, outfile, indent=4)
                
                
'''
            
