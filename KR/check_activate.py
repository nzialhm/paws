#!/usr/bin/python

import json
import time
from datetime import datetime
import os
import sys
import subprocess
import socket, struct
import threading
import select
import json
import traceback
from math import sin, cos, sqrt, atan2, radians


path = "/nct11af/script/tvwsDB/"
#path = "/home/kissvond/work/nct/wsm/buildroot/target/linux/nct11af_imx6ull/def_nct11af/nct11af_bs/nct11af/script/tvwsDB/"
client_path = "/nct11af/script/tvwsDB/client/config/"

org_lat=0.0
org_lon=0.0
interface=" "

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

class check_activate:
    def BS_Client_thread(self, cpe_ip, data):
        clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSock.connect((cpe_ip, 9090))
        while True:
            try:
                ret_val = str(data)+"|"+str(validity)
                clientSock.sendall(ret_val.encode(encoding='utf-8'))
                ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".server_inform.spectrumValidity"])
                validity = ret.strip()
                print("Send to Slave : "+str(data)+"|"+str(validity))
                break
            except:
                print("reconnect")
                clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                clientSock.connect((cpe_ip, 9090))
                clientSock.sendall(data.encode(encoding='utf-8'))
                break
        clientSock.close()

    def BS_server_thread(self):
        dest = ('<broadcast>',10100)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        host = ''
        port = 10101
        r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        r.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        r.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        r.bind((host,port))
        print "Start BS INFO"

        while 1:
            try:
                message, address = r.recvfrom(port)
                print "Got data from", address
                print "Got data from", message
                if message == "NZIA GBI":
                    own_ip = self.get_own_ipaddr(interface)
                    s.sendto(own_ip, dest)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()

    def CPE_server_thread(self):
        HOST = ''
        PORT = 9090

        serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        serverSock.bind((HOST, PORT))
        serverSock.listen(1)
        print('Start Server')

        readsocks = [serverSock]
        answers = {}

        ret = subprocess.check_output(["uci","get","system.@system[0].countrycode"])
        c_code = ret.strip()
        while 1:
            readables, writeables, excpetions = select.select(readsocks, [], [])
            for sock in readables:
                if sock == serverSock:
                    newsock, addr = serverSock.accept()
                    print('connected BS')
                    readsocks.append(newsock)
                else:
                    conn = sock
                    data = conn.recv(1024).decode('utf-8')
                    print("Recv from BS : "+str(data))
                    result = data.split('|')
                    if len(result) > 0 and result[0].find("Err") == -1:
                        os.system("echo "+result[0]+" > /tmp/paws_status")
                        if result[0] == 'PAWS_DONE':	
                            buf = subprocess.check_output(["ifconfig","-a"])
                            iface = buf[buf.find('nct11af'):buf.find('nct11af')+8]
                            buf = subprocess.check_output(["uci","get","wireless."+iface+".channel"])
                            channel = buf.strip()

                            f= open(path+c_code+"/active_channel.json", "w")
                            json_data = Object()
                            json_data.channel = str(channel)
                            date = datetime.now()
                            json_data.active_date = datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
                            active_data= json.loads(json_data.toJSON())
                            active_data = json.dumps(active_data, indent=4)
                            print active_data
                            f.write(active_data)
                            f.close()
                        conn.close()
                        readsocks.remove(conn)
                    else:
                        print("disconnect")
                        conn.close()
                        readsocks.remove(conn)

    def Get_BS_IPAddr(self, ifr):
# after modified : send to the default gateway
        try:
            out = subprocess.check_output("ip route | grep default | awk '{print $3}'", shell=True)
            return out.strip()
        except:
            return None
#        251222 BELLA modified - temporary workaround using a for-loop because
#        the response is slow after arp-scan but running arp-scan multiple
#        times causes network congestion/bottlenecks 
#        ap_mac = subprocess.check_output("iwconfig "+ifr+" | grep 'Access Point:' | awk '{print $6}'", shell=True).strip().lower()
#        for i in range(10):
#           cmd = "arp-scan --interface="+ifr+" --localnet"
#           proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#           out, err = proc.communicate()
#           out = out.lower()
#
#           for line in out.splitlines():
#               if ap_mac in line:
#                   return line.split()[0]
#
#           time.sleep(0.5)
#       return out.strip()


    def activate_client(self, c_code, configfile, s_flag, e_flag, use_ch):
        os.system("python /nct11af/script/tvwsDB/client/"+c_code+"/create_ucitojs.py "+configfile)
        print("python /nct11af/script/tvwsDB/client/"+c_code+"/create_ucitojs.py "+configfile)
        #os.system("python /nct11af/script/tvwsDB/client/"+c_code+"/nct11af_send_req.py "+s_flag+" "+e_flag+" "+use_ch)
        print("python /nct11af/script/tvwsDB/client/"+c_code+"/nct11af_send_req.py "+s_flag+" "+e_flag+" "+use_ch)
        ret = subprocess.check_output(["python", "/nct11af/script/tvwsDB/client/"+c_code+"/nct11af_send_req.py", s_flag, e_flag, use_ch])
        paws_status = ret[ret.rfind("NZIA_PAWS_RESULT")+17:].strip()
        ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".server_inform.spectrumValidity"])
        validity = ret.strip()
        print("Client Status : "+str(paws_status)+"|"+str(validity))
        os.system("rm /nct11af/script/tvwsDB/client/config/"+configfile)
        os.system("rm /nct11af/script/tvwsDB/client/config/paws_url")
        return str(paws_status)+"|"+str(validity)
        
    def check_client_active(self, c_code):
        print(c_code)
        entries = os.listdir(client_path)
        for entry in entries:
            if os.path.isfile(client_path+entry) :
                if entry != "paws_urls" :
                   clientinfo = entry.split('-')
               	   ret_data = self.activate_client(c_code, entry, clientinfo[1], clientinfo[2], clientinfo[3])
                   print(ret_data)
               	   t = threading.Thread(target=self.BS_Client_thread, args=(clientinfo[0], ret_data))
               	   t.start()

    def get_own_ipaddr(self, ifr):
        def_route = self.Get_BS_IPAddr(ifr)
        print("["+def_route+"]")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect((def_route, 80))
        except:
            now_date = time.time()
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
            print("Internet is Down")
            return ""
        return sock.getsockname()[0]

    def get_default_route(self):
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                    continue
                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

    def cal_distance(self, o_lat, o_lon, lat, lon):
        R = 6373.0
       	
        lat1 = radians(float(o_lat))
        lon1 = radians(float(o_lon))
        lat2 = radians(float(lat))
        lon2 = radians(float(lon))
 
        print(lat1, lon1, lat2, lon2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c * 1000

        print("Result:", distance)
        return distance

    def try_bs_activate(self, ifr, lat, lon):
        org_lat = lat
        org_lon = lon
        init_fail=0
        t = threading.Thread(target=self.BS_server_thread, args=())
        t.start()
        ret = subprocess.check_output(["uci","get","system.@system[0].countrycode"])
        c_code = ret.strip()

        ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".nct11afurl.url"])
        org_url = ret.strip()
        os.system("python "+path+c_code+"/create_ucitojs.py")
        os.system("touch /tmp/paws_status")
        filename = "/nct11af/config/configPAWS_"+c_code
        lasttime = int(os.path.getmtime(filename))
        os.system("touch "+path+c_code+"/active_channel.json")
        f = open(path+c_code+"/active_channel.json").read().decode("utf-8")

        if len(f) < 1: # activated 
            print("First Master cease transmission")
            os.system("ifconfig "+ifr+" down")

        while True:
            own_ip = self.get_own_ipaddr(interface)
            if len(own_ip) > 0 :
                break
            time.sleep(5)

        while True:
            if init_fail > 1:
                print("Init First Fail")
                os.system("ifconfig "+ifr+" down")
                os.system("echo '' > "+path+c_code+"/active_channel.json")
            
            ret = subprocess.check_output(["cat", "/tmp/paws_status"])
            paws_status = ret.strip()
            if len(paws_status) < 3:
                os.system("python /nct11af/script/tvwsDB/"+c_code+"/nct11af_send_req.py INIT_REQ REGISTRATION_REQ False")
                init_fail = init_fail + 1
            else:
                break


        while True:
            check_internet=10
            while True:
                own_ip = self.get_own_ipaddr(interface)
                if len(own_ip) == 0 :
                    check_internet = check_internet - 1
                    if check_internet < 1 :
                        print("GLSD did not connect")
                        os.system("rm "+path+c_code+"/active_channel.json")
                        os.system("touch "+path+c_code+"/active_channel.json")
                        break
                    else :
                        time.sleep(10)
                else :
                    break
            ################ Check channel mode ##################
            ret = subprocess.check_output(["uci","get","wireless."+ifr+".chmode"])
            chmode = ret.strip()
            print("Channel Mode : "+chmode)
            if chmode == "N":
                time.sleep(5)
                continue

            ############## initialize for changed server url ####################
            ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".nct11afurl.url"])
            cur_url = ret.strip()
            if org_url != cur_url:
                print("Detect changed server url")
                os.system("echo '' > "+path+c_code+"/active_channel.json")
                os.system("python "+path+c_code+"/create_ucitojs.py")
                os.system("python /nct11af/script/tvwsDB/"+c_code+"/nct11af_send_req.py INIT_REQ REGISTRATION_REQ False")
                org_url = cur_url

            ############## registration for changed configuration ####################
            curtime = int(os.path.getmtime(filename))
            if lasttime != curtime:
                print('Modify Detected.')
                ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".locations.latitude"])
                lat = ret.strip()
                ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".locations.longitude"])
                lon = ret.strip()
                cmd=["diff /nct11af/config/configPAWS_"+c_code+" /tmp/configPAWS_"+c_code+" | grep itude | grep +"]
                ret=subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                (diff,err) = ret.communicate()
                if self.cal_distance(float(org_lat), float(org_lon), float(lat), float(lon)) > 100:
                    org_lat = lat
                    org_lon = lon
                    os.system("echo '' > "+path+c_code+"/active_channel.json")
                    os.system("python "+path+c_code+"/create_ucitojs.py")
                    os.system("python /nct11af/script/tvwsDB/"+c_code+"/nct11af_send_req.py INIT_REQ AVAIL_SPECTRUM_REQ False")
                    os.system("cp /nct11af/config/configPAWS_"+c_code+"	/tmp/configPAWS_"+c_code);
                elif len(diff) < 5:
                    os.system("echo '' > "+path+c_code+"/active_channel.json")
                    os.system("python "+path+c_code+"/create_ucitojs.py")
                    os.system("python /nct11af/script/tvwsDB/"+c_code+"/nct11af_send_req.py INIT_REQ AVAIL_SPECTRUM_REQ False")
                    os.system("cp /nct11af/config/configPAWS_"+c_code+"	/tmp/configPAWS_"+c_code);
               
                     
                lasttime = curtime

            os.system("touch "+path+c_code+"/active_channel.json")
            f = open(path+c_code+"/active_channel.json").read().decode("utf-8")
            print(len(f))

            if len(f) > 10: # activated 
                cmd =["ifconfig | grep "+ifr]
                is_ifr_up = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                (out, err) = is_ifr_up.communicate()
                if len(out.strip()) < 1:
                    os.system("ifconfig "+ifr+" up")

                json_data = json.loads(f)
                active_date = str(json_data['active_date'])
                now_date = time.time()
                print(time.strftime('%Y-%m-%d %H:%M:%S'))
                ret_timestamp = time.mktime(datetime.strptime(active_date, '%Y-%m-%d %H:%M:%S').timetuple())
                ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".server_inform.spectrumValidity"])
                validity = ret.strip()
                print("spectrumValidity : "+validity)
                print("Remain "+ str(int(ret_timestamp) + int(validity) - int(now_date))+" Sec")

                if int(ret_timestamp) + int(validity) < int(now_date):
                    print("time out")
                    os.system("rm "+path+c_code+"/active_channel.json")
                    os.system("touch "+path+c_code+"/active_channel.json")
                    os.system("python "+path+c_code+"/nct11af_send_req.py INIT_REQ PAWS_DONE True")
                elif int(ret_timestamp) + int(validity) > int(now_date):
                    print("delay time")
                else:
                    print("reactivate")
                    os.system("rm "+path+c_code+"/active_channel.json")
                    os.system("touch "+path+c_code+"/active_channel.json")
                    os.system("python "+path+c_code+"/nct11af_send_req.py AVAIL_SPECTRUM_REQ PAWS_DONE True")
                # check connected client file
                self.check_client_active(c_code)
            else: # none activated 
                print("Master cease transmission")
                os.system("ifconfig "+ifr+" down")
                os.system("python "+path+c_code+"/nct11af_send_req.py INIT_REQ PAWS_DONE True")
                f = open(path+c_code+"/setChannel.json").read().decode("utf-8")
                if len(f) > 10:
                    fJson = json.loads(f)
                    if c_code == "KR" and int(fJson["frequencyRanges"][0]["channelId"] == 0):
                        print("channel not exist, interface down")
                        os.system("ifconfig "+ifr+" down")
                    else :
                        af = open(path+c_code+"/active_channel.json").read().decode("utf-8")
                        if len(af) > 0: # activated 
                            os.system("ifconfig "+ifr+" up")
            time.sleep(2)

    def try_cpe_activate(self, ifr, lat, lon):
        t = threading.Thread(target=self.CPE_server_thread, args=())
        t.start()
        ret = subprocess.check_output(["uci","get","system.@system[0].countrycode"])
        c_code = ret.strip()
        ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".nct11afurl.url"])
        org_url = ret.strip()
        os.system("python "+path+c_code+"/create_ucitojs.py")
        os.system("touch /tmp/paws_status")
        filename = "/nct11af/config/configPAWS_"+c_code
        lasttime = int(os.path.getmtime(filename))

        while True:
            ret = subprocess.check_output(["cat","/proc/nct11af/"+ifr+"/status"])
            connected = ret.strip()
            if connected == "connected":
                def_route = ""
                own_ip = self.get_own_ipaddr(ifr)
                if len(own_ip) < 1 :
                    time.sleep(2)
                    continue 

                while True:           
                    ret = subprocess.check_output(["cat", "/tmp/paws_status"])
                    paws_status = ret.strip()
                    if len(paws_status) < 3:
                        while(len(def_route) == 0):
                            def_route = self.Get_BS_IPAddr(ifr)
                        cmd = "ftpput -u root -p admin1234!@#$ "+def_route+" "+client_path+own_ip+"-INIT_REQ-REGISTRATION_REQ-False /nct11af/config/configPAWS_"+c_code
                        print cmd
                        os.system("ftpput -u root -p admin1234!@#$ "+def_route+" "+client_path+own_ip+"-INIT_REQ-REGISTRATION_REQ-False /nct11af/config/configPAWS_"+c_code)
                        time.sleep(30)         
                    else:
                        break

                ############## initialize for changed server url ####################
                ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".nct11afurl.url"])
                cur_url = ret.strip()
                if org_url != cur_url:
                    print("Detect changed server url")
                    os.system("python "+path+c_code+"/create_ucitojs.py")
                    while(len(def_route) == 0):
                        def_route = self.Get_BS_IPAddr(ifr)
                    os.system("ftpput -u root -p admin1234!@#$ "+def_route+" "+client_path+own_ip+"-INIT_REQ-REGISTRATION_REQ-False /nct11af/config/configPAWS_"+c_code)
                    org_url = cur_url
   
                ############## registration for changed configuration ####################
                os.system("touch "+path+c_code+"/active_channel.json")
                f = open(path+c_code+"/active_channel.json").read().decode("utf-8")

                if len(f) > 0: # activated 
                    json_data = json.loads(f)
                    active_date = str(json_data['active_date'])
                    now_date = time.time()
                    print(time.strftime('%Y-%m-%d %H:%M:%S'))
                    ret_timestamp = time.mktime(datetime.strptime(active_date, '%Y-%m-%d %H:%M:%S').timetuple())
                    ret = subprocess.check_output(["uci","get","configPAWS_"+c_code+".server_inform.spectrumValidity"])
                    validity = ret.strip()
                    print("spectrumValidity : "+validity)
                    print("Remain "+ str(int(ret_timestamp) + int(validity) - int(now_date))+" Sec")
                    if int(ret_timestamp) + int(validity) < int(now_date):
                        print("time out")
                        while(len(def_route) == 0):
                            def_route = self.Get_BS_IPAddr(ifr)
                            time.sleep(3)
                        os.system("rm "+path+c_code+"/active_channel.json")
                        os.system("touch "+path+c_code+"/active_channel.json")
                        os.system("ftpput -u root -p admin1234!@#$ "+def_route+" "+client_path+own_ip+"-INIT_REQ-PAWS_DONE-True /nct11af/config/configPAWS_"+c_code)
                        time.sleep(40)         
                    #elif int(ret_timestamp) + 83200 > int(now_date):
                    elif int(ret_timestamp) + int(validity) > int(now_date):
                        print("delay time")
                    else:
                        print("reactivate")
                        while(len(def_route) == 0):
                            def_route = self.Get_BS_IPAddr(ifr)
                            time.sleep(3)
                        os.system("rm "+path+c_code+"/active_channel.json")
                        os.system("touch "+path+c_code+"/active_channel.json")
                        os.system("ftpput -u root -p admin1234!@#$ "+def_route+" "+client_path+own_ip+"-AVAIL_SPECTRUM_REQ-PAWS_DONE-True /nct11af/config/configPAWS_"+c_code)
                        time.sleep(40)         
                    # check connected client file
                else: # none activated 
                        while(len(def_route) == 0):
                            def_route = self.Get_BS_IPAddr(ifr)
                        os.system("ftpput -u root -p admin1234!@#$ "+def_route+" "+client_path+own_ip+"-INIT_REQ-PAWS_DONE-True /nct11af/config/configPAWS_"+c_code)
                        print("ftpput -u root -p admin1234!@#$ "+def_route+" "+client_path+own_ip+"-INIT_REQ-PAWS_DONE-True /nct11af/config/configPAWS_"+c_code)
                        time.sleep(40)         
            else:
                os.system("rm "+path+c_code+"/active_channel.json")
                os.system("touch "+path+c_code+"/active_channel.json")

            print("CPE") 
            time.sleep(2)      
               
    def try_activate(self):
        ret = subprocess.check_output(["/nct11af/script/get_uid.py","nct11af_mode"])
        nct11af_mode = ret.strip()
        ret = subprocess.check_output(["ls", "/proc/nct11af/"])
        interface = ret[ret.find('nct11af'): 8].strip()
        if nct11af_mode == "ap":
            print("Check BS Activate Start")
            self.try_bs_activate(interface, org_lat, org_lon)
        else :
            print("Check CPE Activate Start")
            self.try_cpe_activate(interface, org_lat, org_lon)

ca = check_activate()
ca.try_activate()

