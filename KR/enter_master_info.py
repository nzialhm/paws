import json
try:
   import readline
except:
   # No means
   print("Not readline module available")

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

#device Owner and description, Antenna infomation    
class MasterInfo:
    def __init__(self):
        # questions
        self.inputreq_mode=("Set Admin Mode: 1. admin, 2: usr, 3. End: ")
        self.inputreq_type=("Set device type: 1. Master, 2: Slave, 3.end: ")

        self.inputreq_deviceOwner_list=[]
        self.inputreq_deviceOwner_list.append("Owner:fn")
        self.inputreq_deviceOwner_list.append("Owner:kind")
        self.inputreq_deviceOwner_list.append("Operator:fn")
        self.inputreq_deviceOwner_list.append("Operator:adr:street")
        self.inputreq_deviceOwner_list.append("Operator:adr:locality")
        self.inputreq_deviceOwner_list.append("Operator:adr:region")
        self.inputreq_deviceOwner_list.append("Operator:adr:code")
        self.inputreq_deviceOwner_list.append("Operator:adr:country")
        self.inputreq_deviceOwner_list.append("Operator:tel")
        self.inputreq_deviceOwner_list.append("Operator:email")
        self.inputreq_deviceDesc_list = []
        self.inputreq_deviceDesc_list.append("KsCertId")
        self.inputreq_deviceDesc_list.append("SerialNumber")
        self.inputreq_deviceDesc_list.append("ksDeviceType")
        self.inputreq_deviceDesc_list.append("ModelId")
        self.inputreq_deviceDesc_list.append("Power[dBm]")
        self.inputreq_antenna_list = []
        self.inputreq_antenna_list.append("height")
        self.inputreq_antenna_list.append("eightType: 1. AGL, 2. AMSL")        
        self.inputreq_location_list = []
        self.inputreq_location_list.append("latitude")
        self.inputreq_location_list.append("longitude")
        self.inq_list=[self.inputreq_deviceOwner_list, self.inputreq_deviceDesc_list,self.inputreq_antenna_list,self.inputreq_location_list ]
        self.load_file=["deviceOwner.json", "devDesc.json", "antenna.json"]

        self.devOwner_js = self.read_js_file(self.load_file[0])
        self.devDesc_js = self.read_js_file(self.load_file[1])
        self.antenna_js  = self.read_js_file(self.load_file[2])         

        #create deviceOwner json
        if self.devOwner_js is None:
           dD=Object()
           dD.deviceOwner=Object()
           dD.deviceOwner.owner=Object()
           dD.deviceOwner.owner.fn=""
           dD.deviceOwner.owner.kind=""
           dD.deviceOwner.operator=Object()
           dD.deviceOwner.operator.adr=Object()
           dD.deviceOwner.operator.adr.street=""
           dD.deviceOwner.operator.adr.locality=""
           dD.deviceOwner.operator.adr.region=""
           dD.deviceOwner.operator.adr.code=""
           dD.deviceOwner.operator.adr.country=""
           dD.deviceOwner.operator.tel=""
           dD.deviceOwner.operator.fn=""
           dD.deviceOwner.operator.email=""

           d_js = json.loads(dD.toJSON())
           self.devOwner_js = d_js
           self.devOwner_Write(0)

        #create devDesc json
        if self.devDesc_js is None:
           dD=Object()
           dD.deviceDesc=Object()
           dD.deviceDesc.ksCertId=""
           dD.deviceDesc.serialNumber=""
           dD.deviceDesc.ksDeviceType=""
           dD.deviceDesc.modelId=""
           dD.deviceDesc.ksDeviceEmissionPower=""
           dD.location=Object()
           dD.location.point=Object()
           dD.location.point.center=Object()
           dD.location.point.center.latitude=""
           dD.location.point.center.longitude=""

           d_js = json.loads(dD.toJSON())
           self.devDesc_js = d_js 
           self.devOwner_Write(1)

        #create antenna json
        if self.antenna_js is None:
           dD=Object()
           dD.antennaCharacteristics=Object()
           dD.antennaCharacteristics.height=""
           dD.antennaCharacteristics.heightType=""
        
           d_js = json.loads(dD.toJSON())
           self.antenna_js  = d_js 
           self.devOwner_Write(2)
           


    def read_js_file(self, filepath):
        ret_js = None
        
        try:            
            ret_data = open(filepath).read().decode("utf-8")
            ret_js = json.loads(ret_data) # str to dict type of python
        except IOError, e:
            print("err: {}".format(e))
        
        return ret_js
  
    def select_inq(self):
       while True:
         #select mode
         mode = raw_input(" {}".format(self.inputreq_mode))
         #select device type
         if not mode:
            print("No imput!")
            return False
         mode = int(mode)
         if mode == 1: # admin
            print("Admin Mode")
         elif mode == 2: # user
            print("User Mode")
         elif mode == 3: # end
            print("Bye!")
            return False
         else:
            print("No set")
            continue
          
         dtype = raw_input(" {}".format(self.inputreq_type))
         if not dtype:
            print("No imput!")
            return False
         dtype = int(dtype)
         # Master 
         if dtype == 1: #master
            print("Master Mode")
            if mode == 1:
               return self.master_mode_inq()
            else:
               return self.master_mode_inq(False)
         elif dtype == 2: #slave
            print("Slave Mode")
            if mode == 1:
               return self.slave_mode_inq()
            else:
               return self.slave_mode_inq(False)
         elif dtype == 3: #end
            print("Bye!")
            return False
         else:
            continue

    def slave_mode_inq(self, admin=True):
        ret = False
        # show Master spectrum Information form DB server.
        qes_str=" Select type: 1. Device Owner, 2. Device Descrition, 3. antenna, 4. location, 5. End: "
        print(qes_str)

        spc_js = self.read_js_file("spectrumSchedules.json")
        if spc_js is not None:
           # device Owner
           print("\n Slave Information ---------")
           print("    Owner:fn = {}".format(self.devOwner_js['deviceOwner']['owner']['fn']))
           print("    Owner:kind = {}".format(self.devOwner_js['deviceOwner']['owner']['kind']))
           print("    Operator:fn = {}".format(self.devOwner_js['deviceOwner']['operator']['fn']))
           print("    Operator:addr:street = {}".format(self.devOwner_js['deviceOwner']['operator']['adr']['street']))
           print("    Operator:addr:locality = {}".format(self.devOwner_js['deviceOwner']['operator']['adr']['locality']))
           print("    Operator:addr:region = {}".format(self.devOwner_js['deviceOwner']['operator']['adr']['region']))
           print("    Operator:addr:code = {}".format(self.devOwner_js['deviceOwner']['operator']['adr']['code']))
           print("    Operator:addr:country = {}".format(self.devOwner_js['deviceOwner']['operator']['adr']['country']))
           print("    Operator:tel = {}".format(self.devOwner_js['deviceOwner']['operator']['tel']))
           print("    Operator:email = {}".format(self.devOwner_js['deviceOwner'] ['operator']['email']))
           print("\n")
           print("    KsCertId = {}".format(self.devDesc_js['deviceDesc']['ksCertId']))
           print("    SerialNumber = {}".format(self.devDesc_js['deviceDesc']['serialNumber']))
           print("    ksDeviceType = {}".format(self.devDesc_js['deviceDesc']['ksDeviceType']))
           print("    ModelId = {}".format(self.devDesc_js['deviceDesc']['modelId']))
           print("    Power[dBm] = {}".format(self.devDesc_js['deviceDesc']['ksDeviceEmissionPower']))
           print("\n")
           print("    height= {}".format(self.antenna_js['antennaCharacteristics']['height']))
           print("    heightType= {}".format(self.antenna_js['antennaCharacteristics']['heightType']))
           print(" ----------------------------")


           i = 0
           l = len(spc_js['spectrumSchedules'])
           while i < l:
              print("\n The result of avaliable spectrumSchedules[{}] information for Master device - below -".format(i))
              k = 0
              while k < len(spc_js['spectrumSchedules'][i]['spectra']):
                 print("   spectra[{}]:".format(k))
                 print("      bandwidth: {}".format(spc_js['spectrumSchedules'][i]['spectra'][k]['bandwidth']))
                 
                 print("      ----------------------------")
                 j  = 0
                 while j < len(spc_js['spectrumSchedules'][i]['spectra'][k]['frequencyRanges']):
                    print("      channelId [{}]: {}".format(j, spc_js['spectrumSchedules'][i]['spectra'][k]['frequencyRanges'][j]['channelId']))
                    print("      start     [{}]: {} Hz".format(j, spc_js['spectrumSchedules'][i]['spectra'][k]['frequencyRanges'][j]['startHz']))
                    print("      stop      [{}]: {} Hz".format(j, spc_js['spectrumSchedules'][i]['spectra'][k]['frequencyRanges'][j]['stopHz']))
                    print("      ----------------------------")
                    j += 1

                 print(" ***********************************************")
                 k += 1

              i += 1

           #Show selected frequency by Master device.
           print("\n")
           print("\n Selected frequency information by Master device")
           print("     channelId : {}".format(spc_js['spectrumSchedules'][0]['spectra'][0]['frequencyRanges'][0]['channelId']))
           print("     start     : {} Hz".format(spc_js['spectrumSchedules'][0]['spectra'][0]['frequencyRanges'][0]['startHz']))
           print("     stop      : {} Hz".format(spc_js['spectrumSchedules'][0]['spectra'][0]['frequencyRanges'][0]['stopHz']))
           print(" ***********************************************")

           print("\n")
           print("admin: {}".format(admin))
           data = raw_input("1. location, 2. End: ")
           if not data:
              print("No input Data. Done!")
           else:
              if int(data) == 1:
                 if admin == True:
                   self.ask_input(3)
                   ret = True
                 else:
                   print("In User Mode, Changing the values of location attributes are not available.")

        return ret
    
    def master_mode_inq(self, admin=True):
        i = 0 
        sel_list=[1,2,3,4]
        ret = False
        qes_str = None
        while i < 4:
            qes_str=" Select type: 1. Device Owner, 2. Device Descrition, 3. antenna, 4. location, 5. End: "

            data = raw_input(qes_str)               
            inq_list=[" 1. Device Owner","2. Device Descrition", "3. antenna", "4. location" ]

            if not data:
                print("No input Data. Done!")
                return False
            else:
                inq_index = int(data) - 1
                ret = True
                if inq_index < 4:
                    print("Start Enter {}: -below-".format(inq_list[inq_index]))
                    if inq_index == 3:
                       if admin == True:
                          self.ask_input(inq_index)
                       else:
                          print("In User Mode, Changing the values of location attributes are not available.")
                    else:
                       self.ask_input(inq_index)
                    ind = 0
                    for s in sel_list:
                        if inq_index == s: sel_list.pop(ind)
                        ind += 1
                else:
                    print("Done!")
                    break
            i += 1
            
        return ret       
    
    def ask_input(self, inq_index):
        inq_list=self.inq_list[inq_index]
        index = 0
        for i in inq_list:
            data = raw_input('    {} = '.format(i))
            if not data:
                #print "No input! (using default value)"
                if inq_index == 0:
                    if index == 0: self.devOwner_js['deviceOwner']['owner']['fn']=""
                    elif index == 1: self.devOwner_js['deviceOwner']['owner']['kind']=""
                    elif index == 2: self.devOwner_js['deviceOwner']['operator']['fn']=""
                    elif index == 3: self.devOwner_js['deviceOwner']['operator']['adr']['street']=""
                    elif index == 4: self.devOwner_js['deviceOwner']['operator']['adr']['locality']=""
                    elif index == 5: self.devOwner_js['deviceOwner']['operator']['adr']['region']=""
                    elif index == 6: self.devOwner_js['deviceOwner']['operator']['adr']['code']=""
                    elif index == 7: self.devOwner_js['deviceOwner']['operator']['adr']['country']=""
                    elif index == 8: self.devOwner_js['deviceOwner']['operator']['tel']=""
                    elif index == 9: 
                        self.devOwner_js['deviceOwner'] ['operator']['email']=""
                        self.devOwner_Write(inq_index)
                        print(json.dumps(self.devOwner_js, indent=4))
                elif inq_index == 1:
                    if index == 0: self.devDesc_js['deviceDesc']['ksCertId']=""
                    elif index == 1: self.devDesc_js['deviceDesc']['serialNumber']=""
                    elif index == 2: self.devDesc_js['deviceDesc']['ksDeviceType']=""
                    elif index == 3: self.devDesc_js['deviceDesc']['modelId']=""
                    elif index == 4: 
                        self.devDesc_js['deviceDesc']['ksDeviceEmissionPower']=""
                        self.devOwner_Write(inq_index)
                        print(json.dumps(self.devDesc_js, indent=4))
                
                elif inq_index == 2:
                    if index == 0: 
                        self.antenna_js['antennaCharacteristics']['height']=""
                    elif index == 1:
                        if len(data) > 0 and (int(data) == 1 or int(data) == 2):
                            data_str="AGL"
                            if int(data) == 2: data_str="AMSL"
                            self.antenna_js['antennaCharacteristics']['heightType']=data_str
                        else:
                            print ("No input! (using default value:{})".format(self.antenna_js['antennaCharacteristics']['heightType'])) 
                        
                        self.devOwner_Write(inq_index)
                        
                    print(json.dumps(self.antenna_js, indent=4))                    
                    
                elif inq_index == 3:
                    if index == 0: 
                        self.devDesc_js['location']['point']['center']['latitude']=""
                    elif index == 1:
                        self.devDesc_js['location']['point']['center']['longitude']=""
                        self.devOwner_Write(inq_index)
                        print(json.dumps(self.devDesc_js, indent=4))

            else:
                if inq_index == 0:
                    if index == 0: self.devOwner_js['deviceOwner']['owner']['fn']=data
                    elif index == 1: self.devOwner_js['deviceOwner']['owner']['kind']=data
                    elif index == 2: self.devOwner_js['deviceOwner']['operator']['fn']=data
                    elif index == 3: self.devOwner_js['deviceOwner']['operator']['adr']['street']=data
                    elif index == 4: self.devOwner_js['deviceOwner']['operator']['adr']['locality']=data
                    elif index == 5: self.devOwner_js['deviceOwner']['operator']['adr']['region']=data
                    elif index == 6: self.devOwner_js['deviceOwner']['operator']['adr']['code']=data
                    elif index == 7: self.devOwner_js['deviceOwner']['operator']['adr']['country']=data    
                    elif index == 8: self.devOwner_js['deviceOwner']['operator']['tel']=data
                    elif index == 9: 
                        self.devOwner_js['deviceOwner'] ['operator']['email']=data
                        self.devOwner_Write(inq_index)
                        print(json.dumps(self.devOwner_js, indent=4))
                elif inq_index == 1:
                    if index == 0: self.devDesc_js['deviceDesc']['ksCertId']=data
                    elif index == 1: self.devDesc_js['deviceDesc']['serialNumber']=data
                    elif index == 2: self.devDesc_js['deviceDesc']['ksDeviceType']=data
                    elif index == 3: self.devDesc_js['deviceDesc']['modelId']=data
                    elif index == 4: 
                        self.devDesc_js['deviceDesc']['ksDeviceEmissionPower']=int(data)
                        self.devOwner_Write(inq_index)
                        print(json.dumps(self.devDesc_js, indent=4))
                
                elif inq_index == 2:
                    if index == 0: 
                        data_f=float(data)
                        self.antenna_js['antennaCharacteristics']['height']=round(data_f, 1)
                    elif index == 1:
                        if int(data) == 1 or int(data) == 2:
                            data_str="AGL"
                            if int(data) == 2: data_str="AMSL"
                            self.antenna_js['antennaCharacteristics']['heightType']=data_str
                        else:
                            print ("No input! (using default value:{})".format(self.antenna_js['antennaCharacteristics']['heightType'])) 
                        
                        self.devOwner_Write(inq_index)
                        
                    print(json.dumps(self.antenna_js, indent=4))                    
                    
                elif inq_index == 3:
                    data_f=float(data)
                    if index == 0: 
                        self.devDesc_js['location']['point']['center']['latitude']=round(data_f, 5)
                    elif index == 1:
                        self.devDesc_js['location']['point']['center']['longitude']=round(data_f, 5)
                        self.devOwner_Write(inq_index)
                        print(json.dumps(self.devDesc_js, indent=4))

            
            
                        
            index += 1
        
    def devOwner_Write(self, index):
       #print(index)
        try:
            if index == 0:
                print("write deviceOwner.json")
                f = open(self.load_file[0], "w")
                f.write(json.dumps(self.devOwner_js, indent=4))
                f.close()
            elif index == 1 or index == 3:
                print("write devDesc.json")
                f = open(self.load_file[1], "w")
                f.write(json.dumps(self.devDesc_js, indent=4))
                f.close()
            elif index == 2:
                print("write antenna.json")
                f = open(self.load_file[2], "w")
                f.write(json.dumps(self.antenna_js, indent=4))                
                f.close()
           
            self.devOwner_js = self.read_js_file(self.load_file[0])
            self.devDesc_js = self.read_js_file(self.load_file[1])
            self.antenna_js  = self.read_js_file(self.load_file[2])                
        except IOError, e:
            print("err: {}".format(e))
            
        
   

