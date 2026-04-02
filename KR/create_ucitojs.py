import json

paws_json_path = "/nct11af/script/tvwsDB/KR/"
config_path = "/nct11af/config/"
#paws_json_path = "/home/kissvond/work/nct/wsm/buildroot/target/linux/nct11af_imx6ull/def_nct11af/nct11af_bs/nct11af/script/tvwsDB/KR/"

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class create_json_from_uci:
    def __init__(self):
        self.dD=Object()
        self.dD.deviceDesc=Object()
        self.dD.deviceDesc.ksCertId=""
        self.dD.deviceDesc.serialNumber=""
        self.dD.deviceDesc.ksDeviceType=""
        self.dD.deviceDesc.ksDeviceEmissionPower=""
        self.dD.deviceDesc.modelId=""
       
        self.dD.location=Object()
        self.dD.location.point=Object()
        self.dD.location.point.center=Object()
        self.dD.location.point.center.latitude=""
        self.dD.location.point.center.longitude=""

        self.dO=Object()
        self.dO.deviceOwner=Object()
        self.dO.deviceOwner.owner=Object()
        self.dO.deviceOwner.owner.kind=""
        self.dO.deviceOwner.owner.fn=""
        self.dO.deviceOwner.operator=Object()
        self.dO.deviceOwner.operator.tel=""
        self.dO.deviceOwner.operator.email=""
        self.dO.deviceOwner.operator.fn=""
        self.dO.deviceOwner.operator.adr=Object()
        self.dO.deviceOwner.operator.adr.country=""
        self.dO.deviceOwner.operator.adr.region=""
        self.dO.deviceOwner.operator.adr.code=""
        self.dO.deviceOwner.operator.adr.street=""
        self.dO.deviceOwner.operator.adr.locality=""

        self.ant=Object()
        self.ant.antennaCharacteristics=Object()
        self.ant.antennaCharacteristics.height=""
        self.ant.antennaCharacteristics.heightType=""

        self.tbl_list=["config type 'devDesc'", 
                       "config type 'deviceOwner'",
                       "config type 'locations'", 
                       "config type 'antenna'", 
                       "config type 'nct11afurl'"]
        self.devDesc_dic={}
        self.deviceOwner_dic={}
        self.location_dic={}
        self.antenn_dic={}
        self.nct11afurl_list=[]
       

    def read_uci_file(self, filepath):
        ret_data = None

        try:            
            ret_data = open(config_path+filepath).read().decode("utf-8")
            #print(ret_data)
        except IOError, e:
            print("err: {}".format(e))
            try:            
                ret_data = open(config_path+filepath).read().decode("utf-8")
                #print(ret_data)
            except IOError, e:
                print("err: {}".format(e))            

        return ret_data 
    
    def find_val(self, conf):
        i = 0
        for i in range(len(self.tbl_list)):
            if conf.find(self.tbl_list[i]) != -1:
                   return i;
        return 0

    def create_js_devDesc(self):
        devDesc_js = json.loads(self.dD.toJSON())
        devDesc_js["deviceDesc"].update(self.devDesc_dic)
        devDesc_js["location"]["point"]["center"].update(self.location_dic)
        #print(json.dumps(devDesc_js, indent=4))        
        try:
            f= open(paws_json_path+"devDesc.json", "w")
            f.write(json.dumps(devDesc_js, indent=4))
            f.close()
        except:
            print(paws_json_path+"devDesc.json open error");
            try:
                f= open("devDesc.json", "w")
                f.write(json.dumps(devDesc_js, indent=4))
                f.close()
            except:
                print("devDesc.json open error");


    def create_js_antenna(self):
        ant_js = json.loads(self.ant.toJSON())
        ant_js["antennaCharacteristics"].update(self.antenn_dic)
        #print(json.dumps(ant_js, indent=4))             

        try:
            f= open(paws_json_path+"antenna.json", "w")
            f.write(json.dumps(ant_js, indent=4))
            f.close()
        except:
            print(paws_json_path+"antenna.json open error");        
            try:
                f= open("antenna.json", "w")
                f.write(json.dumps(ant_js, indent=4))
                f.close()
            except:
                print("antenna.json open error");        
            
            
    def create_js_devOwner(self):
        lvalue = ["owner_fn", "owner_kind", "operator_fn", "operator_adr_street", "operator_adr_locality",
                 "operator_adr_region", "operator_adr_code", "operator_adr_country", "operator_tel", "operator_email"]
    
        for d in lvalue:
            #ksCertID
            data = self.deviceOwner_dic.get(d)
            if d == "owner_fn":
                if data is not None:
                    self.dO.deviceOwner.owner.fn=self.deviceOwner_dic["owner_fn"]
                else:
                    self.dO.deviceOwner.owner.fn=""
            elif d == "owner_kind":
                if data is not None:
                    self.dO.deviceOwner.owner.kind=self.deviceOwner_dic["owner_kind"]
                else:
                    self.dO.deviceOwner.owner.kind=""
            elif d == "operator_fn":
                if data is not None:
                    self.dO.deviceOwner.operator.fn=self.deviceOwner_dic["operator_fn"]
                else:
                    self.dO.deviceOwner.operator.fn=""            
            elif d == "operator_tel":
                if data is not None:
                    self.dO.deviceOwner.operator.tel=self.deviceOwner_dic["operator_tel"]
                else:
                    self.dO.deviceOwner.operator.tel=""            
            elif d == "operator_email":
                if data is not None:
                    self.dO.deviceOwner.operator.email=self.deviceOwner_dic["operator_email"]
                else:
                    self.dO.deviceOwner.operator.email=""            
            elif d == "operator_adr_street":
                if data is not None:
                    self.dO.deviceOwner.operator.adr.street=self.deviceOwner_dic["operator_adr_street"]
                else:
                    self.dO.deviceOwner.operator.adr.street=""    
            elif d == "operator_adr_locality":
                if data is not None:
                    self.dO.deviceOwner.operator.adr.locality=self.deviceOwner_dic["operator_adr_locality"]
                else:
                    self.dO.deviceOwner.operator.adr.locality=""
            elif d == "operator_adr_region":
                if data is not None:
                    self.dO.deviceOwner.operator.adr.region=self.deviceOwner_dic["operator_adr_region"]
                else:
                    self.dO.deviceOwner.operator.adr.region=""
            elif d == "operator_adr_code":
                if data is not None:
                    self.dO.deviceOwner.operator.adr.code=self.deviceOwner_dic["operator_adr_code"]
                else:
                    self.dO.deviceOwner.operator.adr.code=""
            elif d == "operator_adr_country":
                if data is not None:
                    self.dO.deviceOwner.operator.adr.country=self.deviceOwner_dic["operator_adr_country"]
                else:
                    self.dO.deviceOwner.operator.adr.country=""
                    
        devicOwner_js = json.loads(self.dO.toJSON())
        #print(json.dumps(devicOwner_js, indent=4))
        
        try:
            f= open(paws_json_path+"deviceOwner.json", "w")
            f.write(json.dumps(devicOwner_js, indent=4))
            f.close()
        except:
            print(paws_json_path+"deviceOwner.json open error");       
            try:
                f= open("deviceOwner.json", "w")
                f.write(json.dumps(devicOwner_js, indent=4))
                f.close()
            except:
                print("deviceOwner.json open error");       
            
    def uci_to_json(self):
        data = self.read_uci_file("configPAWS_KR")
        #data = self.read_uci_file("configPAWS_KR")
        #print("==================\n================\n")
        
        f = False
        cur_index = 0
        
        if data is None:
            print("open the configPAWS_KR file failed")
            return
        
        for k in data.splitlines():
            d = self.find_val(k) 
            #print("find: {}".format(d))
            if f == False and d < len(self.tbl_list):
                f = True
                cur_index = d
            else:
                if f == True:
                    if len(k) == 0: # Current getting config is done.so moving next config.
                        f = False
                    else:
                        s=k.replace("	option ", "")
                        #s_val = s.replace("'", "").split(" ")
                        s_val = s.split("'")
                        s_val[0] = s_val[0].replace(" ","")
                        if cur_index == 0: #devDesc
                            if s_val[0] == "ksDeviceEmissionPower":
                                self.devDesc_dic[s_val[0]] = int(s_val[1])
                            elif s_val[0] == "spectrumValidity":
                                self.devDesc_dic[s_val[0]] = int(s_val[1])
                            else:
                                self.devDesc_dic[s_val[0]] = s_val[1]
                        elif cur_index == 1: #deviceOwner
                            self.deviceOwner_dic[s_val[0]] = s_val[1]
                        elif cur_index == 2: #locations
                            if (s_val[0] == "latitude") or (s_val[0] == "longitude"):
                                self.location_dic[s_val[0]] = round(float(s_val[1]), 5)
                        elif cur_index == 3: #antenna
                            if s_val[0] == "height":
                                self.antenn_dic[s_val[0]] = round(float(s_val[1]), 1)
                            else:
                                self.antenn_dic[s_val[0]] = s_val[1]
                        elif cur_index == 4: #url
                            self.nct11afurl_list.append(s_val[1])
                        else:
                            print("cur: {}".format(s))
                            
        
        #print("start config = {}".format(self.tbl_list[0]))
        #print(self.devDesc_dic)
        #print("----> END\n")    
        #print("start config = {}".format(self.tbl_list[1]))
        #print(self.deviceOwner_dic)
        #print("----> END\n")    
        #print("start config = {}".format(self.tbl_list[2]))
        #print(self.location_dic)
        #print("----> END\n")    
        #print("start config = {}".format(self.tbl_list[3]))
        #print(self.antenn_dic)
        #print("----> END\n")    
        #print("start config = {}".format(self.tbl_list[4]))
        #print(self.nct11afurl_list)
        #print("----> END\n")    

        # create json format with parsing data.
        self.create_js_devDesc()
        self.create_js_devOwner()
        self.create_js_antenna()
        
        #for i in self.nct11afurl_lis:
        url=Object()
        url.url=Object()
        url.url=self.nct11afurl_list[0]
        url_js = json.loads(url.toJSON())
        try:
            f= open(paws_json_path+"nct11afurl.json", "w")
            f.write(json.dumps(url_js, indent=4))
            f.close()
        except:
            print(paws_json_path+"nct11afurl.json open error");
            try:
                f= open(paws_json_path+"nct11afurl.json", "w")
                f.write(json.dumps(url_js, indent=4))
                f.close()
            except:
                print("nct11afurl.json open error");               
        
            

cj = create_json_from_uci()
cj.uci_to_json()


