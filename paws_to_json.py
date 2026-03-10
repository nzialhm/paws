# paws_to_json.py
# -*- coding: utf-8 -*-

import json

# 1. 속성을 자유롭게 추가하기 위한 기본 클래스
class Object(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def toJSON(self):
        # 객체를 딕셔너리로 변환 (재귀적 처리)
        return json.dumps(self, default=lambda o: o.__dict__, 
                          sort_keys=True, indent=4)

# 2. 메인 데이터 생성 클래스
class create_json_data:
    def __init__(self):
        # 전체를 담을 기본 객체
        self.def_val = Object()
        self.def_val.method = ""
        self.def_val.id = ""
        
        # params와 그 하위 구조 정의
        self.def_val.params = Object()
        self.def_val.params.version = "1.0"
        self.def_val.params.type = ""
        
        # [NEW] devDesc.json 내용을 객체 형태로 직접 내장
        self.setup_device_info()

    def setup_device_info(self):
        """파일 없이 내부 변수로 데이터를 직접 설정"""
        # deviceDesc 설정
        self.def_val.params.deviceDesc = Object(
            serialNumber="WS20-224-0000004",
            ksDeviceEmissionPower=20,
            ksCertId="R-R-nZc-NZC-WS20",
            ksDeviceType="Portable Master",
            modelId="NZC-WS20"
        )
        
        # location -> point -> center 설정
        self.def_val.params.location = Object()
        self.def_val.params.location.point = Object()
        self.def_val.params.location.point.center = Object(
            latitude=37.586,
            longitude=126.8172
        )

    def create(self, req_type, id_index):
        # 요청 타입 설정
        self.type = req_type
        self.def_val.params.type = self.type
        
        # ID 포맷팅 (000001 형식)
        self.def_val.id = '{:0>6}'.format(id_index)
        
        if self.type == "INIT_REQ":
            self.def_val.method = "spectrum.paws.init"
            
        # Object 구조를 최종 dict/json으로 변환
        # Python 2.7 환경의 json.loads는 unicode를 반환하므로 주의하세요.
        return json.loads(self.def_val.toJSON())

# # --- 실제 사용 예시 ---
# cj = create_json_data()
# data = cj.create("INIT_REQ", 1)

# # 결과 확인
# if data:
#     print(json.dumps(data, indent=4))
