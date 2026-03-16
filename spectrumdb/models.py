# models.py
# -*- coding: utf-8 -*-

class InitResponse:
    def __init__(self, result):
        """
        서버 응답 딕셔너리를 직접 받아서 내부 데이터를 파싱합니다.
        :param resp_dict: {u'result': {...}, u'id': u'000001'} 형태의 딕셔너리
        """
        # 1. 'result' 키 추출 (없으면 빈 딕셔너리)
        # 전체 응답 딕셔너리일 수도 있고, result 부분만 넘어올 수도 있으므로 체크
        self.type = result.get('type', '')
        
        # 2. 'rulesetInfo' 추출
        ruleset_info = result.get('rulesetInfo', {})
        
        # 3. 'resultId' 추출하여 ruleset_ids 리스트에 저장
        # 서버 응답 예시: 'KsTvBandWhiteSpace-2015'
        self.device_id = ruleset_info.get('resultId', '')

        self.maxPollingSecs = ruleset_info.get('maxPollingSecs', '')

        self.authority = ruleset_info.get('authority', '')

        self.maxLocationChange = ruleset_info.get('maxLocationChange', '')
        
        # 추가 정보가 필요하다면 여기서 더 추출할 수 있습니다.
        self.version = result.get('version', '')
        
    def __repr__(self):
        return "<InitResponse: type=%s, device_id=%s>" % (self.type, self.device_id)

    def uci_update(self, uci, file):
        uci.set(file, 'InitResponse', 'type', self.type)
        uci.set(file, 'InitResponse', 'resultId', self.device_id)
        uci.set(file, 'InitResponse', 'maxPollingSecs', self.maxPollingSecs)
        uci.set(file, 'InitResponse', 'authority', self.authority)
        uci.set(file, 'InitResponse', 'maxLocationChange', self.maxLocationChange)
    
class RegisterResponse:
    def __init__(self, result):
        """
        REGISTRATION_RESP 결과를 받아 device_id를 설정합니다.
        :param resp_dict: {u'result': {...}, u'id': u'xxxxxx'} 형태의 딕셔너리
        """
        # 1. 'result' 데이터 추출
        self.type = result.get('type', '')
        
        # 2. 서버 응답의 오타('ruelsetInfo')와 정상('rulesetInfo') 모두 대응
        # get('A')가 None이면 get('B')를 시도합니다.
        ruleset_info = result.get('ruelsetInfo') or result.get('rulesetInfo') or {}
        
        # 3. device_id로 사용할 값 추출
        # 보통 rulesetId를 device_id의 식별자로 사용하므로 이를 할당합니다.
        # 만약 별도의 기기 ID가 응답에 포함된다면 해당 키값으로 수정하세요.
        self.device_id = ruleset_info.get('resultId', '')

        self.maxPollingSecs = ruleset_info.get('maxPollingSecs', '')

        self.authority = ruleset_info.get('authority', '')

        self.maxLocationChange = ruleset_info.get('maxLocationChange', '')

    def __repr__(self):
        return "<RegisterResponse: type=%s, device_id=%s>" % (self.type, self.device_id)

    def uci_update(self, uci, file):
        uci.set(file, 'RegisterResponse', 'type', self.type)
        uci.set(file, 'RegisterResponse', 'resultId', self.device_id)
        uci.set(file, 'RegisterResponse', 'maxPollingSecs', self.maxPollingSecs)
        uci.set(file, 'RegisterResponse', 'authority', self.authority)
        uci.set(file, 'RegisterResponse', 'maxLocationChange', self.maxLocationChange)

class Channel(object):
    """개별 채널 정보를 담는 보조 객체"""
    def __init__(self, start_hz, stop_hz, bandwidth, ksDeviceEmissionPower, channel_id, startTime, stopTime):
        self.start_hz = start_hz
        self.stop_hz = stop_hz
        self.bandwidth = bandwidth
        self.ksDeviceEmissionPower = ksDeviceEmissionPower
        self.channel_id = channel_id
        self.startTime = startTime
        self.stopTime = stopTime

    def __repr__(self):
        return "<Channel ID: %s, start_hz: %sMHz, stop_hz: %sMHz, BW: %sMHz>" % (
            self.channel_id, self.start_hz, self.stop_hz, self.bandwidth)

class AvailableSpectrumResponse(object):
    def __init__(self, result):
        """
        서버 응답 딕셔너리를 받아 가용 채널 리스트를 파싱합니다.
        """
        self.profiles = []  # 파싱된 Channel 객체들이 담길 리스트
        
        # 1. 'result' 데이터 추출
        self.type = result.get('type', '')
        
        # 2. 공통 EIRP 정보 추출 (deviceDesc 내 ksDeviceEmissionPower)
        # 서버 응답에 'serealNumber' 오타가 있어도 안전하게 처리하도록 구성
        device_desc = result.get('deviceDesc', {})
        
        self.modelId = device_desc.get('modelId', '')
        self.serealNumber = device_desc.get('serealNumber', '')
        self.ksDeviceEmissionPower = device_desc.get('ksDeviceEmissionPower', 0.0)
        
        # 3. 중첩된 스펙트럼 데이터 순회
        # spectrumSchedules -> spectra -> frequencyRanges 순서로 접근
        schedules = result.get('spectrumSchedules', [])
        
        

        for schedule in schedules:
            eventTime = schedule.get('eventTime', {})
            startTime = eventTime.get('startTime', '')
            stopTime = eventTime.get('stopTime', '')
            spectra_list = schedule.get('spectra', [])

            for spectrum in spectra_list:
                # 공통 대역폭(bandwidth) 추출
                bw = spectrum.get('bandwidth', 0)
                
                # 개별 주파수 범위(frequencyRanges) 추출
                ranges = spectrum.get('frequencyRanges', [])
                for freq_range in ranges:
                    start_hz = freq_range.get('startHz')
                    stop_hz = freq_range.get('stopHz')
                    channel_id = freq_range.get('channelId')
                    
                    # 4. 개별 채널 객체 생성 및 메인 리스트에 추가
                    new_channel = Channel(
                        start_hz=start_hz,
                        stop_hz=stop_hz,
                        bandwidth=bw,
                        ksDeviceEmissionPower=self.ksDeviceEmissionPower,
                        channel_id=channel_id,
                        startTime=startTime,
                        stopTime=stopTime
                    )
                    self.profiles.append(new_channel)

    def __repr__(self):
        return "<SpectrumProfile: type=%s, Total %d channels found>" % (self.type, len(self.profiles))

    def uci_update(self, uci, file):
        uci.set(file, 'AvailableSpectrumResponse', 'type', self.type)
        uci.set(file, 'AvailableSpectrumResponse', 'modelId', self.modelId)
        uci.set(file, 'AvailableSpectrumResponse', 'serealNumber', self.serealNumber)
        uci.set(file, 'AvailableSpectrumResponse', 'ksDeviceEmissionPower', self.ksDeviceEmissionPower)
        channel_ids = []
        start_hzs = []
        stop_hzs = []
        loop = 0
        for ch in self.profiles:
            if loop == 0:
                uci.set(file, 'AvailableSpectrumResponse', 'startTime', ch.startTime)
                uci.set(file, 'AvailableSpectrumResponse', 'stopTime', ch.stopTime)
            channel_ids.append(str(ch.channel_id))
            start_hzs.append(str(ch.start_hz))
            stop_hzs.append(str(ch.stop_hz))
            loop = loop + 1

        uci.set(file, 'AvailableSpectrumResponse', 'channelId', ",".join(channel_ids))
        uci.set(file, 'AvailableSpectrumResponse', 'startHz', ",".join(start_hzs))
        uci.set(file, 'AvailableSpectrumResponse', 'stopHz', ",".join(stop_hzs))


class NotifyResponse:
    def __init__(self, result, channel):

        self.select_channel=channel
        # 1. 'result' 데이터 추출
        self.type = result.get('type', '')
        
       
    def __repr__(self):
        return "<UseNotify: type=%s>" % (self.type)

    def uci_update(self, uci, file):
        uci.set(file, 'NotifyResponse', 'type', self.type)
        uci.set(file, 'NotifyResponse', 'ksDeviceEmissionPower', self.select_channel.ksDeviceEmissionPower)
        uci.set(file, 'NotifyResponse', 'startTime', self.select_channel.startTime)
        uci.set(file, 'NotifyResponse', 'stopTime', self.select_channel.stopTime)
        uci.set(file, 'NotifyResponse', 'channelId', self.select_channel.channel_id)
        uci.set(file, 'NotifyResponse', 'startHz', self.select_channel.start_hz)
        uci.set(file, 'NotifyResponse', 'stopHz', self.select_channel.stop_hz)
